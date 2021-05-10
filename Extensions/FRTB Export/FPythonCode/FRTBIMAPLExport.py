""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/frtb/./etc/FRTBIMAPLExport.py"
"""----------------------------------------------------------------------------
MODULE
    (c) Copyright 2017 FIS Front Arena. All rights reserved.

DESCRIPTION

----------------------------------------------------------------------------"""
import re

import acm

import FRTBExport
import FRTBBaseWriter
import FRTBCommon
import FRTBUtility

# Writers
class PLResultsCollector(FRTBBaseWriter.ResultsCollector):
    COLUMN_IDS = (
        FRTBCommon.IMA_PL_HYPOTHETICAL_COLUMN_ID,
        FRTBCommon.IMA_PL_ACTUAL_COLUMN_ID,
        FRTBCommon.IMA_PL_RISK_COLUMN_ID
        
    )
    _USE_PROJECTION_COORDINATES = False

class PLHypWriter(FRTBBaseWriter.Writer):
    COLUMN_IDS = (FRTBCommon.IMA_PL_HYPOTHETICAL_COLUMN_ID,)
    OUTPUT_SUB_DIR = 'pl_hypothetical'
    _MEASUREMENT_RISK_FACTOR_ATTRIBUTES = (
        'ID', 'Group', 'Sub Group', 'Type'
    )

    def _createHeader(self):
        header = []
        prefix = 'Factor.'
        for label in self._MEASUREMENT_RISK_FACTOR_ATTRIBUTES:
            header.append(prefix + label)

        header.extend(self._getDefaultTradeHeader())
        header.append('Profit and Loss')
        return header

    def _getRows(self, header):
        measurement = self._getResultsFilters()[0]
        rows = []
        risk_factors = ['Residual'] * len(self._MEASUREMENT_RISK_FACTOR_ATTRIBUTES)
        idx_group = self._MEASUREMENT_RISK_FACTOR_ATTRIBUTES.index('Group')
        risk_factors[idx_group] = 'Other'
        for trade_attrs, measurements in self._results_iterator:
            result = measurements[measurement].Number()
            if result:
                result = str(result)
                trade_attrs = self._getDefaultTradeAttributes(
                    trade_attrs=trade_attrs
                )
                row_id = ','.join(risk_factors + trade_attrs[:-1])
                if not self._omitResult(result, measurement, row_id):
                    row = risk_factors + trade_attrs + [result]
                    rows.append(row)

        return rows

    def _getResultsFilters(self):
        measurement = re.split(r' |\-', self.CALC_NAME)[0]
        return (measurement,)


class PLActWriter(FRTBBaseWriter.Writer):
    COLUMN_IDS = (FRTBCommon.IMA_PL_ACTUAL_COLUMN_ID,)
    OUTPUT_SUB_DIR = 'pl_actual'
    _MEASUREMENT_RISK_FACTOR_ATTRIBUTES = (
        'ID', 'Group', 'Sub Group', 'Type'
    )

    def _createHeader(self):
        header = []
        prefix = 'Factor.'
        for label in self._MEASUREMENT_RISK_FACTOR_ATTRIBUTES:
            header.append(prefix + label)

        header.extend(self._getDefaultTradeHeader())
        header.append('Profit and Loss')
        header.append('P&L Source')
        return header

    def _getRows(self, header):
        measurement = self._getResultsFilters()[0]
        rows = []
        risk_factors = ['Residual'] * len(self._MEASUREMENT_RISK_FACTOR_ATTRIBUTES)
        idx_group = self._MEASUREMENT_RISK_FACTOR_ATTRIBUTES.index('Group')
        risk_factors[idx_group] = 'Other'
        for trade_attrs, measurements in self._results_iterator:
            result = measurements[measurement].Number()
            if result:
                result = str(result)
                trade_attrs = self._getDefaultTradeAttributes(
                    trade_attrs=trade_attrs
                )
                row_id = ','.join(risk_factors + trade_attrs[:-1] + ['Actual'])
                if not self._omitResult(result, measurement, row_id):
                    row = risk_factors + trade_attrs + [result] + ['Actual']
                    rows.append(row)

        return rows

    def _getResultsFilters(self):
        measurement = re.split(r' |\-', self.CALC_NAME)[0]
        return (measurement,)


class PLRiskWriter(PLHypWriter):
    CALC_NAME = CALC_NAME_LONG = None
    COLUMN_IDS = (FRTBCommon.IMA_PL_RISK_COLUMN_ID,)
    OUTPUT_SUB_DIR = 'pl_risk_theoretical'
    _MEASUREMENT_RISK_FACTOR_ATTRIBUTES = \
        PLHypWriter._MEASUREMENT_RISK_FACTOR_ATTRIBUTES + (
            'Commodity', 'Credit Quality', 'Location', 'Grade'
        )


# Exporters
class PLExport(FRTBExport.Export):
    _END_DATE_REQUIRED = True
    RESULTS_COLLECTOR_CLASS = PLResultsCollector

    def __init__(self):
        super(PLExport, self).__init__()
        self._long_name = self.CALC_NAME_LONG.split(' ', 5)[-1]
        self._tab_suffix = 'PL ' + self._long_name
        self._end_date_required = int(bool(self._END_DATE_REQUIRED))
        self._long_name += ' P&L'

    def getAelVariables(self):
        ttCalculate = 'Generate %s values.' % self._long_name.lower()
        self._ael_vars.append(
            super(PLExport, self).getPerformCalculationAelVariable(
                calc_name=self._long_name, tab_suffix=self._tab_suffix,
                tooltip=ttCalculate
            )
        )
        self._ael_vars.extend(self._getScenarioAelVariables())
        return self._ael_vars

    def makeColumns(self, parameters):
        calendar = parameters['scenarioCalendar']
        end_date_str = parameters[self.CALC_NAME + 'oneDayScenarioEndDate']
        start_date, end_date = self._getScenarioDates(
            parameters=parameters, end_date_str=end_date_str, calendar=calendar
        )
        columns = super(PLExport, self).makeColumns(parameters=parameters)
        column_params = {
            acm.FSymbol('PortfolioProfitLossStartDate'): 'Custom Date',
            acm.FSymbol('PortfolioProfitLossStartDateCustom'): start_date,
            acm.FSymbol('PortfolioProfitLossEndDate'): 'Custom Date',
            acm.FSymbol('PortfolioProfitLossEndDateCustom'): end_date,
        }
        columns = self._getColumns(
            parameters=parameters, column_params=column_params,
            start_date=start_date, end_date=end_date
        )
        return columns

    def _getScenarioAelVariables(self):
        ttEndDate = 'The end date to use in the external scenario file.'
        ael_var = [self.CALC_NAME + 'oneDayScenarioEndDate',
            'Scenario end date_' + self._tab_suffix,
            'string', FRTBCommon.DEFAULT_DAYS, 'Today',
            self._end_date_required, 0, ttEndDate
        ]
        return [ael_var]

    def _getScenarioDates(self, parameters, end_date_str, calendar):
        raise NotImplementedError

    def _getColumns(self, parameters, column_params, start_date, end_date):
        raise NotImplementedError

class PLHypExport(PLExport):
    WRITER_CLASSES = (PLHypWriter,)

    def _getScenarioDates(self, parameters, end_date_str, calendar):
        end_date = FRTBUtility.getAcmDateFromString(end_date_str, calendar)
        start_date = calendar.AdjustBankingDays(end_date, -1)
        return start_date, end_date

    def _getColumns(self, parameters, column_params, start_date, end_date):
        column = self.makeColumn(
            column_id=FRTBCommon.IMA_PL_HYPOTHETICAL_COLUMN_ID,
            column_name=self.CALC_NAME, params=column_params
        )
        return [column]

class PLActExport(PLExport):
    #_END_DATE_REQUIRED = False
    WRITER_CLASSES = (PLActWriter,)

    def _getScenarioDates(self, parameters, end_date_str, calendar):
        end_date = FRTBUtility.getAcmDateFromString(end_date_str, calendar)
        start_date = calendar.AdjustBankingDays(end_date, -1)
        return start_date, end_date

    def _getColumns(self, parameters, column_params, start_date, end_date):
        column = self.makeColumn(
            column_id=FRTBCommon.IMA_PL_ACTUAL_COLUMN_ID,
            column_name=self.CALC_NAME, params=column_params
        )
        return [column]


class PLRiskExport(PLExport):
    _END_DATE_REQUIRED = False
    WRITER_CLASSES = (PLRiskWriter,)

    def _getScenarioAelVariables(self):
        scenarioFileSelection = FRTBExport.getInputFileSelector()
        ttScenarioFile = (
            'The name or path to an external file contain 1-day scenario file.'
        )
        ael_vars = [
            #[VariableName,
            #    DisplayName,
            #    Type, CandidateValues, Default,
            #    Mandatory, Multiple, Description, InputHook, Enabled]
            [self.CALC_NAME + 'oneDayScenarioFile',
                'Risk theoretical scenario file_' + self._tab_suffix,
                scenarioFileSelection, None, scenarioFileSelection,
                0, 1, ttScenarioFile, None, True],
        ] + super(PLRiskExport, self)._getScenarioAelVariables()
        return ael_vars

    def _getScenarioDates(self, parameters, end_date_str, calendar):
        assert parameters.get(self.CALC_NAME + 'oneDayScenarioFile'), \
            self.CALC_NAME_LONG + ' scenario file required'
        start_date = end_date = None
        if end_date_str:
            end_date = FRTBUtility.getAcmDateFromString(end_date_str, calendar)
            start_date = calendar.AdjustBankingDays(end_date, -1)

        scenario_file = parameters[self.CALC_NAME + 'oneDayScenarioFile']
        scenario_details = FRTBUtility.getScenarioDetails(
            scenario_file=str(scenario_file).strip(),
            first_end_date=end_date_str, last_end_date=end_date_str,
            horizon=1, calendar=calendar
        )
        assert len(scenario_details) == 1, \
            'Expected to retrieve only a single scenario column'
        sd = scenario_details[0]
        assert (not start_date) or (start_date == sd.start_date), \
            'Start date incorrectly determined'
        assert (not end_date) or (end_date == sd.end_date), \
            'End date incorrectly determined'
        end_date = end_date if start_date else sd.end_date
        start_date = start_date or sd.start_date
        return start_date, end_date

    def _getColumns(self, parameters, column_params, start_date, end_date):
        scenario_file = parameters[self.CALC_NAME + 'oneDayScenarioFile']
        scenario_params = {
            acm.FSymbol('Scenario File'): str(scenario_file).strip(),
            acm.FSymbol('Scenario End Date'): 'Custom Date',
            acm.FSymbol('Scenario End Date Custom'): end_date,
            acm.FSymbol('Calendar'): parameters['scenarioCalendar'],
            acm.FSymbol('Risk Factor Setup'): parameters['riskFactorSetup']
        }
        scenario = self.makeDynamicScenario(
            template_name='FRTBRiskTheoreticalPLScenarioFromFile',
            scenario_params=scenario_params
        )
        scenario_dimension_names = ['Scenario File Scenario']
        column = self.makeColumn(
            column_id=FRTBCommon.IMA_PL_RISK_COLUMN_ID,
            column_name=self.CALC_NAME,
            scenario=scenario, params=column_params,
            dimension_names=scenario_dimension_names
        )
        return [column]
