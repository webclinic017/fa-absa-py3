""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/frtb/./etc/FRTBIMASESExport.py"
"""----------------------------------------------------------------------------
MODULE
    (c) Copyright 2017 FIS Front Arena. All rights reserved.

DESCRIPTION

----------------------------------------------------------------------------"""
import acm

import FVaRFileParsing

import FRTBStressedCapitalAddOnPerRiskFactor

import FRTBExport
import FRTBBaseWriter
import FRTBCommon
import FBDPCommon

NMRFAttributeName = FBDPCommon.valueFromFParameter(
                'FRTBNMRFMap', 'AttributeName')

NMRFEquity = FBDPCommon.valueFromFParameter(
                'FRTBNMRFMap', 'Equity')

NMRFCredit = FBDPCommon.valueFromFParameter(
                'FRTBNMRFMap', 'Credit')

# Writers
class SESResultsCollector(FRTBBaseWriter.ResultsCollector):
    COLUMN_IDS = (FRTBCommon.IMA_SES_COLUMN_ID,)

    def addResult(self, posInfoID, columnID, calculationInfos):
        if calculationInfos and (columnID in self.COLUMN_IDS):
            position_key = self._position_key_table[posInfoID]
            pos_result = self._result_dictionary.setdefault(position_key, {})
            result = pos_result.setdefault(columnID, {})
            rf_names = self._dimension_names.get(columnID)
            rf_values = [ci.values for ci in calculationInfos]
            for name, value in zip(rf_names, rf_values):
                result[name] = value

        return

    def getData(self):
        data = {}
        for pos_key, pos_key_dict in self._result_dictionary.items():
            trade_attrs = self.getTradeAttributes(pos_key)
            for column_id, results in pos_key_dict.items():
                for rf_name, result in results.items():
                    data_key = (rf_name, trade_attrs)
                    data[data_key] = result

        return data

class SESWriter(FRTBBaseWriter.Writer):
    def __init__(
        self, results_collector, trade_attributes,
        output_path, grouping_attributes,
        additional_writer_kwargs
    ):
        super(SESWriter, self).__init__(
            results_collector=results_collector,
            trade_attributes=trade_attributes,
            output_path=output_path,
            grouping_attributes=grouping_attributes,
            additional_writer_kwargs=additional_writer_kwargs
        )
        self._eid_map = additional_writer_kwargs[self.CALC_NAME + '_eid_map']
        self._modellable_map = additional_writer_kwargs[self.CALC_NAME + '_modellable_map']


    def _createHeader(self):
        header = self._getDefaultTradeHeader()
        header.append('Factor.ID')
        header.append('Factor Class')
        header.append('Factor.Modellable')
        header.append('Factor.NMRF')
        header.append('SES Input')
        return header

    def _getRows(self, header):
        rows = []
        for data_key, result in self._results.items():
            result = result.Number()
            if not result:
                continue

            risk_name, trade_attrs = data_key
            trade_attrs = self._getDefaultTradeAttributes(trade_attrs=trade_attrs)
            row_id = ','.join([risk_name] + trade_attrs)
            result = str(result)
            if self._omitResult(result=result, measurement=risk_name, row_id=row_id):
                continue
                
            risk_class = self._eid_map[risk_name]
            factor_modellable = self._modellable_map[risk_name]
            instType = self._getAttrOnName(trade_attrs, NMRFAttributeName)
            factor_NMRF = ""
            if instType in NMRFEquity:
                factor_NMRF = "Equity"
            elif instType in NMRFCredit:
                factor_NMRF = "Credit"
            else:
                factor_NMRF = "Other"
            row = trade_attrs + [risk_name, risk_class, factor_modellable, factor_NMRF, result]
            rows.append(row)

        return rows

    def _omitResult(self, result, measurement, row_id):
        omit = super(SESWriter, self)._omitResult(
            result=result, measurement=measurement, row_id=row_id
        )
        if measurement not in self._eid_map:
            warning_type = (
                '%s - unknown risk factor name (external ID), ignoring row' % (
                    measurement
                )
            )
            row = self._makeOffendingRow(row_id, result)
            self._warnings.setdefault(warning_type, []).append(row)
            return True

        return omit

# Exporters
class SESExport(FRTBExport.Export):
    RESULTS_COLLECTOR_CLASS = SESResultsCollector
    WRITER_CLASSES = (SESWriter,)

    def getAelVariables(self):
        ttScenarioFile = (
            'Scenario file containing scenarios for the '
            'non-modellable risk factors'
        )
        scenarioFileSelection = FRTBExport.getInputFileSelector()
        self._ael_vars.append(
            super(SESExport, self).getPerformCalculationAelVariable(
                tab_suffix=self.CALC_NAME_LONG
            )
        )
        self._ael_vars.append([
            self.CALC_NAME + 'ScenarioFile',
                'Scenario file_' + self.CALC_NAME_LONG,
                scenarioFileSelection, None, scenarioFileSelection,
                0, 1, ttScenarioFile, None, True
        ])
        return self._ael_vars

    def setInternalParameters(self, parameters):
        super(SESExport, self).setInternalParameters(parameters=parameters)
        if not self.isEnabled():
            return

        scenario_file = str(parameters[self.CALC_NAME + 'ScenarioFile'])
        rf_setup = parameters['riskFactorSetup']
        eids = []
        for k in FVaRFileParsing.scenario_file_data(scenario_file).Keys():
            eids.append(str(k))

        eid_map = {}
        modellable_map = {}
        for collection in rf_setup.RiskFactorCollections():
            for instance in collection.RiskFactorInstances():
                eid = str(acm.RiskFactor.RiskFactorExternalId(instance))
                if eid in eids:
                    
                    eid_map[eid] = str(collection.DisplayName())
                    modellable_map[eid] = 'Yes' if instance.AdditionalInfo().Modellable() == True else 'No'

        self._additional_writer_kwargs[self.CALC_NAME + '_eid_map'] = eid_map
        self._additional_writer_kwargs[self.CALC_NAME + '_modellable_map'] = modellable_map
        return

    def makeColumns(self, parameters):
        assert parameters.get(self.CALC_NAME + 'ScenarioFile'), \
            self.CALC_NAME_LONG + ' scenario file required'
        columns = super(SESExport, self).makeColumns(parameters=parameters)
        scenario_params = {
            'filename': parameters[self.CALC_NAME + 'ScenarioFile'],
            'rfsetup': parameters['riskFactorSetup'].Name()
        }
        vector = FRTBStressedCapitalAddOnPerRiskFactor.ael_main_ex(
            scenario_params, None
        )
        columns.append(self.makeColumn(
            column_id=FRTBCommon.IMA_SES_COLUMN_ID, vector=vector
        ))
        return columns
