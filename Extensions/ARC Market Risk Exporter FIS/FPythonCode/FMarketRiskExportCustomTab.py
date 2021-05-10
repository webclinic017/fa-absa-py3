""" Compiled: 2020-08-14 16:40:05 """

#__src_file__ = "extensions/arc_writers/./etc/FMarketRiskExportCustomTab.py"
"""----------------------------------------------------------------------------
MODULE
    FMarketRiskExportCustomTab - Scenario settings tab

    (c) Copyright 2019 by FIS FRONT ARENA. All rights reserved.

DESCRIPTION

    This is a GUI tab in the FMarketRiskExport GUI which contains settings
    for the Market Value export.

----------------------------------------------------------------------------"""


import acm

import FRunScriptGUI
import FColumnSelectItem
from FMarketRiskExportColumnSelection import MarketRiskExportColumnSelection

tab_name = "_Custom"


class MarketRiskExportCustomTab(MarketRiskExportColumnSelection):
    @staticmethod
    def getStoredScenarios():
        return sorted([s.Name() for s in acm.FStoredScenario.Select("")])

    def __init__(self):
        ttWriter = ('Name of custom writer defined in FRiskCubeCustomWriters '
                'module for generating output file.')
        ttExportName = ('Name of the column identifier in the output file.')
        ttFileName = ('Name of the output file.')
        variables = [
                # [VariableName,
                #       DisplayName,
                #       Type, CandidateValues, Default,
                #       Mandatory, Multiple, Description, InputHook, Enabled]
                ['runCustomReports', 'Run reports{0}'.format(tab_name),
                    'int', [0, 1], 0, True, False, 'Run custom reports',
                    self._enable, True],
                ['customWriter', 'Custom writer' + tab_name,
                        "string", None, 'VectorWriter',
                        0, 0, ttWriter, None, False],
                ["exportName",
                        "Exported name" + tab_name,
                        "string", None, 'ALL-SWAP,100bp Per Currency',
                        0, 0, ttExportName, None, False],
                ['customFileName',
                        'Output file name' + tab_name,
                        'string', None, 'Custom',
                        0, 0, ttFileName, None, False],
        ]
        MarketRiskExportColumnSelection.__init__(self, variables,
                                    __name__, tab_name,
                                    'Portfolio Delta Yield Full Per Currency')
                                    # 'Portfolio Theoretical Value')

    def _enable(self, index, fieldValues):
        if fieldValues[index] == '1':
            for i in range(1, len(self)):
                self[i].enable(True)
        else:
            for i in range(1, len(self)):
                self[i].enable(False)
        return fieldValues


def getAelVariables():
    outtab = MarketRiskExportCustomTab()
    outtab.LoadDefaultValues(__name__)
    return outtab
