""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/arc_writers/./etc/FMarketRiskExportMVTab.py"
"""----------------------------------------------------------------------------
MODULE
    FMarketRiskExportMVTab - Scenario settings tab

    (c) Copyright 2019 by FIS FRONT ARENA. All rights reserved.

DESCRIPTION

    This is a GUI tab in the FMarketRiskExport GUI which contains settings
    for the Market Value export.

----------------------------------------------------------------------------"""


import acm


import FRunScriptGUI


tab_name = "_Market value"


class MarketRiskExportMVTab(FRunScriptGUI.AelVariablesHandler):
    def __init__(self):

        accounting_curr = (acm.GetFunction("mappedValuationParameters", 0)(
                ).Parameter().AccountingCurrency())
        calendars = acm.FCalendar.Select("")
        ttMarketValueFileName = ('Name of the file containing the market '
                'value results from the scenario tab.')
        variables = [
                # [VariableName,
                #       DisplayName,
                #       Type, CandidateValues, Default,
                #       Mandatory, Multiple, Description, InputHook, Enabled]
                ['runMarketValueReports', 'Run reports{0}'.format(
                    tab_name), 'int', [0, 1], 0, True, False,
                    'Run market value report', self._enable, True],
                ['Market Value File Name',
                        'Market value file name' + tab_name,
                        'string', None, 'MarketValue',
                        0, 0, ttMarketValueFileName, None, False]
        ]
        FRunScriptGUI.AelVariablesHandler.__init__(self, variables, __name__)

    def _enable(self, index, fieldValues):
        if fieldValues[index] == '1':
            for i in range(1, len(self)):
                self[i].enable(True)
        else:
            for i in range(1, len(self)):
                self[i].enable(False)
        return fieldValues



def getAelVariables():

    outtab = MarketRiskExportMVTab()
    outtab.LoadDefaultValues(__name__)
    return outtab
