""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/arc_writers/./etc/FMarketRiskExportRiskFactorTab.py"
"""----------------------------------------------------------------------------
MODULE
    FMarketRiskExportRiskFactorTab - Scenario settings tab

    (c) Copyright 2019 by FIS FRONT ARENA. All rights reserved.

DESCRIPTION

    This is a GUI tab in the FMarketRiskExport GUI which contains settings
    for the RiskFactor export.

----------------------------------------------------------------------------"""


import acm


import FRunScriptGUI
from FMarketRiskExportColumnSelection import MarketRiskExportRiskFactorColumnSelection

tab_name = "_Risk Factor"


class MarketRiskExportRiskFactorTab(MarketRiskExportRiskFactorColumnSelection):

    def __init__(self):

        accounting_curr = (acm.GetFunction("mappedValuationParameters", 0)(
                ).Parameter().AccountingCurrency())
        calendars = acm.FCalendar.Select("")
        ttRiskFactorFileName = ('Name of the file containing the risk factor '
                'results from the risk factor tab.')
        variables = [
                # [VariableName,
                #       DisplayName,
                #       Type, CandidateValues, Default,
                #       Mandatory, Multiple, Description, InputHook, Enabled]
                ['runRiskFactorReports', 'Run reports{0}'.format(tab_name),
                    'int', [0, 1], 0, True, False, 'Run risk factor report',
                    self._enable, True],
                ['Risk Factor File Name',
                        'Risk Factor file name' + tab_name,
                        'string', None, 'RiskFactorEquityPriceDelta',
                        0, 0, ttRiskFactorFileName, None, False]
        ]
                                    
        MarketRiskExportRiskFactorColumnSelection.__init__(self, variables,
                                    __name__, tab_name,
                                    'Position Delta Per Equity Price Risk Factor')

    def _enable(self, index, fieldValues):
        if fieldValues[index] == '1':
            for i in range(1, len(self)):
                self[i].enable(True)
        else:
            for i in range(1, len(self)):
                self[i].enable(False)
        return fieldValues


def getAelVariables():

    outtab = MarketRiskExportRiskFactorTab()
    outtab.LoadDefaultValues(__name__)
    return outtab
