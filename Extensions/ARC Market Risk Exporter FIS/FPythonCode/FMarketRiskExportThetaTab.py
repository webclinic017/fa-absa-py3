""" Compiled: 2020-08-14 16:40:05 """

#__src_file__ = "extensions/arc_writers/./etc/FMarketRiskExportThetaTab.py"
"""----------------------------------------------------------------------------
MODULE
    FMarketRiskExportThetaTab - Scenario settings tab

    (c) Copyright 2019 by FIS FRONT ARENA. All rights reserved.

DESCRIPTION

    This is a GUI tab in the FMarketRiskExport GUI which contains settings
    for the Theta export.

----------------------------------------------------------------------------"""


import acm


import FRunScriptGUI
from FMarketRiskExportColumnSelection import MarketRiskExportColumnSelection

tab_name = "_Theta"


class MarketRiskExportThetaTab(MarketRiskExportColumnSelection):

    def __init__(self):

        accounting_curr = (acm.GetFunction("mappedValuationParameters", 0)(
                ).Parameter().AccountingCurrency())
        calendars = acm.FCalendar.Select("")
        ttThetaFileName = ('Name of the file containing the theta '
                'results from the scenario tab.')
        variables = [
                # [VariableName,
                #       DisplayName,
                #       Type, CandidateValues, Default,
                #       Mandatory, Multiple, Description, InputHook, Enabled]
                ['runThetaReports', 'Run reports{0}'.format(tab_name),
                    'int', [0, 1], 0, True, False, 'Run theta report',
                    self._enable, True],
                ['Theta File Name',
                        'Theta file name' + tab_name,
                        'string', None, 'Theta',
                        0, 0, ttThetaFileName, None, False]
        ]
        MarketRiskExportColumnSelection.__init__(self, variables,
                                    __name__, tab_name,
                                    'Portfolio Theta')

    def _enable(self, index, fieldValues):
        if fieldValues[index] == '1':
            for i in range(1, len(self)):
                self[i].enable(True)
        else:
            for i in range(1, len(self)):
                self[i].enable(False)
        return fieldValues


def getAelVariables():

    outtab = MarketRiskExportThetaTab()
    outtab.LoadDefaultValues(__name__)
    return outtab
