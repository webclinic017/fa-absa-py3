""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/arc_writers/./etc/FMarketRiskExportStressGridTab.py"
"""----------------------------------------------------------------------------
MODULE
    FMarketRiskExportStressGridTab - Scenario settings tab

    (c) Copyright 2019 by FIS FRONT ARENA. All rights reserved.

DESCRIPTION

    This is a GUI tab in the FMarketRiskExport GUI which contains settings
    for the Market Value export.

----------------------------------------------------------------------------"""


import acm

import FRunScriptGUI
import FColumnSelectItem
from FMarketRiskExportColumnSelection import MarketRiskExportColumnSelection

tab_name = "_Stress Grid"


class MarketRiskExportStressGridTab(MarketRiskExportColumnSelection):
    @staticmethod
    def getStoredScenarios():
        return sorted([s.Name() for s in acm.FStoredScenario.Select("")])

    def __init__(self):

        ttScenarios = ('Names of a stored scenarios containing different'
                ' shifts, specified in % relative terms.')
        ttFilePrefix = ('Prefix for the files containing the scenario results.'
                ' The actual output file names will be '
                '<prefix>_<scenarioName>.dat for each scenario.')
        ttStressName = ('Specify stress name.')
        variables = [
                # [VariableName,
                #       DisplayName,
                #       Type, CandidateValues, Default,
                #       Mandatory, Multiple, Description, InputHook, Enabled]
                ['runStressGridReports', 'Run reports{0}'.format(tab_name),
                    'int', [0, 1], 0, True, False, 'Run stress grid report',
                    self._enable, True],
                ["stress_grid_scenarios",
                        ("Stress grid scenarios"
                            + tab_name),
                        "string",
                        MarketRiskExportStressGridTab.getStoredScenarios(), "",
                        0, True, ttScenarios, None, False],
                ['stress_grid_file',
                        "Output file prefix" + tab_name,
                        'string', None, 'StressGrid', 0, 0, ttFilePrefix, None,
                        False],
                ['stress_name',
                        "Stress name" + tab_name,
                        'string', None, 'Spot and Volatility Grid',
                        0, 0, ttStressName, None,
                        False]
        ]
        MarketRiskExportColumnSelection.__init__(self, variables,
                                    __name__, tab_name,
                                    'Portfolio Theoretical Value')

    def _enable(self, index, fieldValues):
        if fieldValues[index] == '1':
            for i in range(1, len(self)):
                self[i].enable(True)
        else:
            for i in range(1, len(self)):
                self[i].enable(False)
        return fieldValues


def getAelVariables():

    outtab = MarketRiskExportStressGridTab()
    outtab.LoadDefaultValues(__name__)
    return outtab
