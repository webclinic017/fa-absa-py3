""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/frtb/./etc/FRTBIMAESExport.py"
"""----------------------------------------------------------------------------
MODULE
    (c) Copyright 2016 FIS Front Arena. All rights reserved.

DESCRIPTION

----------------------------------------------------------------------------"""
import acm

import FRTBIMAHierarchy

import FRTBExport
import FRTBBaseWriter
import FRTBCommon
import FRTBUtility

# Writers
class ESResultsCollector(FRTBBaseWriter.ResultsCollector):
    COLUMN_IDS = (
        FRTBCommon.IMA_ES_BASE_VALUE_COLUMN_ID,
        FRTBCommon.IMA_ES_COLUMN_ID
    )
    _BASE_VALUE_TABLE = {}

    @staticmethod
    def resetCache():
        if ESResultsCollector._BASE_VALUE_TABLE:
            ESResultsCollector._BASE_VALUE_TABLE = {}

        return

    def addResult(self, posInfoID, columnID, calculationInfos):
        if calculationInfos:
            pos_key = self._position_key_table[posInfoID]
            if columnID == FRTBCommon.IMA_ES_BASE_VALUE_COLUMN_ID:
                ESResultsCollector._BASE_VALUE_TABLE[pos_key] = \
                    calculationInfos[0].values
                return

            liquidity_horizon, risk_class, _ = columnID.split('|', 2)
            pos_result_dict = self._result_dictionary.setdefault(pos_key, {})
            risk_class_result = pos_result_dict.setdefault(risk_class, {})
            horizon_result = risk_class_result.setdefault(liquidity_horizon, {})
            for calculationInfo in calculationInfos:
                scenarioElement = calculationInfo.projectionCoordinates[0]
                calculatedValue = calculationInfo.values
                horizon_result[scenarioElement] = calculatedValue

        return

    def getData(self):
        data = {}
        for pos_key, pos_key_dict in self._result_dictionary.items():
            trade_attrs = self.getTradeAttributes(pos_key)
            base_value = ESResultsCollector._BASE_VALUE_TABLE[pos_key]
            base_value = float(base_value.Number())
            for risk_class, risk_class_result in pos_key_dict.items():
                rc = 'Foreign Exchange' if risk_class == 'FX' else risk_class
                for liq_horizon, result in risk_class_result.items():
                    abs_values = (v.Number() for idx, v in sorted(result.items()))
                    values = [float(v) - base_value for v in abs_values]
                    if not liq_horizon.endswith('+'):
                        liq_horizon += '+'

                    data_key = ('IMCC', None, rc, trade_attrs, liq_horizon)
                    data[data_key] = values

        return data

class ESBaseWriter(FRTBBaseWriter.Writer):
    def __init__(
        self, results_collector, trade_attributes,
        output_path, grouping_attributes,
        additional_writer_kwargs
    ):
        super(ESBaseWriter, self).__init__(
            results_collector=results_collector,
            trade_attributes=trade_attributes,
            output_path=output_path,
            grouping_attributes=grouping_attributes,
            additional_writer_kwargs=additional_writer_kwargs
        )
        es_type = self.CALC_NAME.rsplit(' ', 1)[-1].rsplit('_', 1)[0]
        self._es_type_long = \
            self.CALC_NAME_LONG.rsplit(' ', 1)[-1].rsplit('_', 1)[0]
        self._scenario_details = additional_writer_kwargs[
            es_type + '_scenario_details'
        ]

class ESValuesBaseWriter(ESBaseWriter):
    _DESCRIPTION_WRITER = None

    def __init__(
        self, results_collector, trade_attributes,
        output_path, grouping_attributes,
        additional_writer_kwargs
    ):
        self._DESCRIPTION_WRITER.updateName(cls=self._DESCRIPTION_WRITER)
        self.COLUMN_IDS = (self.__class__.__name__,)
        self._written = False
        super(ESValuesBaseWriter, self).__init__(
            results_collector=results_collector,
            trade_attributes=trade_attributes,
            output_path=output_path,
            grouping_attributes=grouping_attributes,
            additional_writer_kwargs=additional_writer_kwargs
        )

    def _createHeader(self):
        header = ['VaR Type', 'ES Type', 'Factor Class']
        header.extend(self._getDefaultTradeHeader())
        header.append('Liquidity Horizon')
        header.append('PV Change')
        return header

    def _getRows(self, header):
        rows = []
        wrong_num_scenarios_errors = []
        expected_num_scenarios = len(self._scenario_details)
        for data_key, values in self._results.items():
            if any(values):
                data_key = list(data_key)
                data_key[1] = self._es_type_long
                processed_data_key = data_key[:3]
                trade_attrs = self._getDefaultTradeAttributes(
                    trade_attrs=data_key[3]
                )
                processed_data_key += trade_attrs
                processed_data_key += data_key[4:]
                measurement = ';'.join(str(v) for v in values)
                row_id = ','.join(processed_data_key)
                if not self._omitResult(measurement, self._es_type_long, row_id):
                    num_scenarios = len(values)
                    if num_scenarios == expected_num_scenarios:
                        row = processed_data_key + [measurement]
                        rows.append(row)
                    else:
                        offenders = 'Expected %s, got %s - %s' % (
                            expected_num_scenarios, num_scenarios,
                            self._makeOffendingRow(row_id, measurement)
                        )
                        wrong_num_scenarios_errors.append(offenders)

        if wrong_num_scenarios_errors:
            msg = (
                'Number of exported P&L values does not match number of '
                'selected scenarios:'
            )
            wrong_num_scenarios_errors.insert(0, msg)
            msg = '\n  '.join(wrong_num_scenarios_errors)
            raise AssertionError(msg)

        self._written = bool(len(rows))
        return rows

class ESDescriptionBaseWriter(ESBaseWriter):
    @staticmethod
    def updateName(cls):
        if not cls.CALC_NAME.endswith('_Description'):
            cls.CALC_NAME += '_Description'
            cls.CALC_NAME_LONG += '_Description'

        return

    def _createHeader(self):
        header = [
            'VaR Type', 'ES Type', 'Scenario',
            'Scenario Date Start', 'Scenario Date End',
            'Is Antithetic', 'Scenario Date Linking Measure'
        ]
        return header

    def _getRows(self, header):
        for writer in list(self.INSTANCES[self.CALC_GROUP].values()):
            if getattr(writer, '_DESCRIPTION_WRITER', None) == self.__class__:
                if not writer._written:
                    return None

        rows = []
        for scenario_details in self._scenario_details:
            row = [
                'IMCC', self._es_type_long, str(scenario_details.relative_idx + 1),
                scenario_details.start_date, scenario_details.end_date,
                'FALSE', '0' # It's fine for this to be always zero
            ]
            rows.append(row)

        return rows

class ESFCWriter(ESValuesBaseWriter):
    class ESFCDescriptionWriter(ESDescriptionBaseWriter): pass
    _DESCRIPTION_WRITER = ESFCDescriptionWriter

class ESRCWriter(ESValuesBaseWriter):
    class ESRCDescriptionWriter(ESDescriptionBaseWriter): pass
    _DESCRIPTION_WRITER = ESRCDescriptionWriter

class ESRSWriter(ESValuesBaseWriter):
    class ESRSDescriptionWriter(ESDescriptionBaseWriter): pass
    _DESCRIPTION_WRITER = ESRSDescriptionWriter

# Exporters
class ESExport(FRTBExport.Export):
    _ADD_BASE_COLUMN = False

    def __init__(self):
        super(ESExport, self).__init__()
        ESResultsCollector.resetCache()

    def getAelVariables(self):
        ttScenarioFile = (
            'The name or path to an external file contain %s scenarios.' % (
                self.CALC_NAME_LONG.lower()
            )
        )
        scenarioFileSelection = FRTBExport.getInputFileSelector()
        ttIncludeCalc = 'Include scenario file in calculation.'
        ttScenarioHorizon = (
            'Scenario horizon (business days between start and end date).'
        )
        ttFirstEndDate = (
            'The first end date to use in the external scenario file. '
            'This corresponds to the start of the range of dates that will be used.'
        )
        ttLastEndDate = (
            'The last end date to use in the external scenario file. '
            'This corresponds to the end of the range of dates that will be used.'
        )
        tab_suffix = 'ES ' + self._getScenarioType()
        ael_vars = [
            #[VariableName,
            #    DisplayName,
            #    Type, CandidateValues, Default,
            #    Mandatory, Multiple, Description, InputHook, Enabled]
            self.getPerformCalculationAelVariable(
                tab_suffix=tab_suffix, tooltip=ttIncludeCalc
            ),
            [self.CALC_NAME + 'ScenarioFile',
                'Scenario file_' + tab_suffix,
                scenarioFileSelection, None, scenarioFileSelection,
                0, 1, ttScenarioFile, None, True],
            [self.CALC_NAME + 'ScenarioHorizon',
                'Scenario horizon_' + tab_suffix,
                'int', None, 10,
                0, 0, ttScenarioHorizon],
            [self.CALC_NAME + 'FirstEndDate',
                'First scenario end date_' + tab_suffix,
                'string', None, None,
                0, 0, ttFirstEndDate],
            [self.CALC_NAME + 'LastEndDate',
                'Last scenario end date_' + tab_suffix,
                'string', FRTBCommon.DEFAULT_DAYS, 'Today',
                0, 0, ttLastEndDate],
        ]
        return ael_vars

    def setInternalParameters(self, parameters):
        ESExport._ADD_BASE_COLUMN = True
        ESResultsCollector.resetCache()
        super(ESExport, self).setInternalParameters(parameters=parameters)
        if not self.isEnabled():
            return

        first_end_date_key = self.CALC_NAME + 'FirstEndDate'
        last_end_date_key = self.CALC_NAME + 'LastEndDate'
        scenario_file = parameters[self.CALC_NAME + 'ScenarioFile']
        scenario_details = FRTBUtility.getScenarioDetails(
            scenario_file=str(scenario_file).strip(),
            first_end_date=parameters[first_end_date_key],
            last_end_date=parameters[last_end_date_key],
            horizon=parameters[self.CALC_NAME + 'ScenarioHorizon'],
            calendar=parameters['scenarioCalendar']
        )
        self._additional_writer_kwargs[self.CALC_NAME + '_scenario_details'] = \
            scenario_details
        return

    def makeColumns(self, parameters):
        columns = super(ESExport, self).makeColumns(parameters=parameters)

        # define some useful variables
        file_key = acm.FSymbol('file')
        start_idx_key = acm.FSymbol('startIndex')
        end_idx_key = acm.FSymbol('endIndex')
        reduced_fs_key = acm.FSymbol('reducedFactorSet')
        risk_class_key = acm.FSymbol('riskClass')
        horizon_key = acm.FSymbol('liquidityHorizon')
        hierarchy_name = str(parameters['hierarchy'].Name()).strip()
        rf_setup = parameters['riskFactorSetup'].Name()
        scenario_params = {
            acm.FSymbol('riskFactorSetup'): rf_setup,
            acm.FSymbol('hierarchy'): hierarchy_name
        }
        calc_name = 'Expected Shortfall'
        scenario_details = \
            self._additional_writer_kwargs[self.CALC_NAME + '_scenario_details']
        start_idx = scenario_details[0].column_idx + 1
        end_idx = scenario_details[-1].column_idx + 1
        scenario_template_name = 'FRTBIMAScenarioFromFile'
        scenario_dimension_names = ['IMA Scenario']
        risk_classes = parameters['riskClassNames']
        scenario_type = self._getScenarioType()
        liquidity_horizons = parameters.get('liquidityHorizons')
        hierarchy = FRTBIMAHierarchy.FRTBIMAHierarchy(
            hierarchy_name, rf_setup
        )
        horizon_candidates = \
            hierarchy.FRTBLiquidityHorizonCandidates(liquidity_horizons)
        get_horizons = lambda risk_class: \
            hierarchy.FRTBValidLiquidityHorizonsFiltered(
                risk_class, horizon_candidates
            )

        # create colum
        scenario_params[file_key] = \
            str(parameters[self.CALC_NAME + 'ScenarioFile']).strip()
        scenario_params[start_idx_key] = start_idx
        scenario_params[end_idx_key] = end_idx
        scenario_params[reduced_fs_key] = \
            str(self.CALC_NAME.startswith(self.CALC_NAME + 'R'))
        for risk_class in risk_classes:
            scenario_params[risk_class_key] = risk_class
            for liquidity_horizon in get_horizons(risk_class=risk_class):
                scenario_params[horizon_key] = liquidity_horizon
                scenario = self.makeDynamicScenario(
                    template_name=scenario_template_name,
                    scenario_params=scenario_params
                )
                liquidity_horizon = str(liquidity_horizon)
                #if liquidity_horizon == '120':
                #    continue

                column_name = '|'.join(
                    (liquidity_horizon, risk_class, scenario_type, calc_name)
                )
                column = self.makeColumn(
                    column_id=FRTBCommon.IMA_ES_COLUMN_ID,
                    column_name=column_name,
                    scenario=scenario,
                    dimension_names=scenario_dimension_names
                )
                columns.append(column)

        if not columns:
            return columns

        if ESExport._ADD_BASE_COLUMN:
            ESExport._ADD_BASE_COLUMN = False
            base_column = self.makeColumn(
                column_id=FRTBCommon.IMA_ES_COLUMN_ID,
                column_name=FRTBCommon.IMA_ES_BASE_VALUE_COLUMN_ID
            )
            columns.insert(0, base_column)

        return columns

    def _getScenarioType(self):
        return self.CALC_NAME_LONG.split('_', 1)[0].rsplit(' ', 1)[-1]

class ESFCResultsCollector(ESResultsCollector): pass
class ESRCResultsCollector(ESResultsCollector): pass
class ESRSResultsCollector(ESResultsCollector): pass

class ESFCExport(ESExport):
    RESULTS_COLLECTOR_CLASS = ESFCResultsCollector
    WRITER_CLASSES = (ESFCWriter, ESFCWriter._DESCRIPTION_WRITER)

class ESRCExport(ESExport):
    RESULTS_COLLECTOR_CLASS = ESRCResultsCollector
    WRITER_CLASSES = (ESRCWriter, ESRCWriter._DESCRIPTION_WRITER)

class ESRSExport(ESExport):
    RESULTS_COLLECTOR_CLASS = ESRSResultsCollector
    WRITER_CLASSES = (ESRSWriter, ESRSWriter._DESCRIPTION_WRITER)
