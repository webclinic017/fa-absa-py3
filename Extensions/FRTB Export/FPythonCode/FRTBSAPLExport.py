""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/frtb/./etc/FRTBSAPLExport.py"
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
        FRTBCommon.SA_PL_ACTUAL_COLUMN_ID,
        
    )
    _USE_PROJECTION_COORDINATES = False


class PLActWriter(FRTBBaseWriter.Writer):
    COLUMN_IDS = (FRTBCommon.SA_PL_ACTUAL_COLUMN_ID,)
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
        for trade_attrs, measurements in self._results.items():
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
        
        self._ael_vars.extend([
            #[VariableName,
            #    DisplayName,
            #    Type, CandidateValues, Default,
            #    Mandatory, Multiple, Description, InputHook, Enabled]
            [self.CALC_NAME + 'scenarioCalendar',
                'Scenario calendar_' + self._tab_suffix,
                'FCalendar', None, FRTBCommon.ACCOUNTING_CURRENCY_CALENDAR,
                self._end_date_required, 0, 'Calendar used to generate scenario file(s).'
            ],
        ])
        
        
        return self._ael_vars

    def makeColumns(self, parameters):
        calendar = parameters[self.CALC_NAME + 'scenarioCalendar']
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


class PLActExport(PLExport):
    #_END_DATE_REQUIRED = False
    WRITER_CLASSES = (PLActWriter,)

    def _getScenarioDates(self, parameters, end_date_str, calendar):
        end_date = FRTBUtility.getAcmDateFromString(end_date_str, calendar)
        start_date = calendar.AdjustBankingDays(end_date, -1)
        return start_date, end_date

    def _getColumns(self, parameters, column_params, start_date, end_date):
        column = self.makeColumn(
            column_id=FRTBCommon.SA_PL_ACTUAL_COLUMN_ID,
            column_name=self.CALC_NAME, params=column_params
        )
        return [column]
