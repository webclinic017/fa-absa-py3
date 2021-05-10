""" Compiled: 2020-08-14 16:40:05 """

#__src_file__ = "extensions/arc_writers/./etc/FMarketRiskExportPnLTab.py"
"""----------------------------------------------------------------------------
MODULE
    FMarketRiskExportPnLTab - P&L settings tab

    (c) Copyright 2019 by FIS FRONT ARENA. All rights reserved.

DESCRIPTION

    This is a GUI tab in the FMarketRiskExport GUI which contains settings
    for the P&L export.

----------------------------------------------------------------------------"""


import acm


import FRunScriptGUI


tab_name = "_Profit and loss"


class MarketRiskExportPnLTab(FRunScriptGUI.AelVariablesHandler):

    def __init__(self):

        ttPlSource = "Name of the PL source in risk cube"
        ttDailyPlSource = "Name of the daily PL source in risk cube"
        ttCleanPlSource = ('Name of the clean PL source in risk cube. '
                    'Clean PL is exported only when this field is specified')
        ttPLFileName = ('Name of the file containing results from the profit '
                'and loss tab, that is, profit and loss values.')
        variables = [
                # [VariableName,
                #       DisplayName,
                #       Type, CandidateValues, Default,
                #       Mandatory, Multiple, Description, InputHook, Enabled]
                ['runPnLReports', 'Run reports{0}'.format(tab_name),
                    'int', [0, 1], 0, True, False,
                    'Run profit and loss report', self._enable, True],
                ["daily_pl_source",
                        "Profit and loss source" + tab_name,
                        "string", None, 'DailyTotal',
                        0, 0, ttDailyPlSource, None, False],
                ["clean_pl_source",
                        "Clean profit and loss source" + tab_name,
                        "string", None, 'Hypothetical',
                        0, 0, ttCleanPlSource, None, False],
                ["total_pl_source",
                        "Total profit and loss source" + tab_name,
                        "string", None, 'Total',
                        0, 0, ttPlSource, None, False],
                ['PL File Name',
                        'Profit and loss file name' + tab_name,
                        'string', None, 'ProfitAndLoss',
                        0, 0, ttPLFileName, None, False],
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

    outtab = MarketRiskExportPnLTab()
    outtab.LoadDefaultValues(__name__)
    return outtab
