""" Compiled: 2020-08-14 16:40:05 """

#__src_file__ = "extensions/arc_writers/./etc/FArtiQMarketRiskExportStressTab.py"
"""----------------------------------------------------------------------------
MODULE
    FMarketRiskExportStressTab - Stressed VaR settings tab

    (c) Copyright 2019 by FIS FRONT ARENA. All rights reserved.

DESCRIPTION

    This is a GUI tab in the FMarketRiskExport GUI which contains settings
    that set up stress calculations.

----------------------------------------------------------------------------"""


import acm


import FRunScriptGUI
from FMarketRiskExportColumnSelection import MarketRiskExportColumnSelection
import FMarketRiskExportColumnSelection 

DISPLAY_TYPE_ABSOLUTE = "Absolute"
DISPLAY_TYPE_RELATIVE = "Relative"

tab_name = "_Stress"
displayTypes = [DISPLAY_TYPE_ABSOLUTE, DISPLAY_TYPE_RELATIVE]


class MarketRiskExportStressTab(MarketRiskExportColumnSelection):

    def __init__(self):

        ttStressType = ('Freely defined mandatory text describing the Stress type. '
                'For instance \'2008 crisis\'.')
        ttStressFileName = ('Name of the file containing the stress '
                'value results from the scenario tab.')
        ttScenarios = ('The stored scenario applied for calculation.')
        variables = [
                # [VariableName,
                #       DisplayName,
                #       Type, CandidateValues, Default,
                #       Mandatory, Multiple, Description, InputHook, Enabled]
                ['runStressReports',
                    'Run reports{0}'.format(tab_name), 'int', [0, 1], 0, True,
                    False, 'Run Spot/Vol Reports', self._enable, True],
                ["stress_Scenarios",
                        ("Stored scenarios"
                            + tab_name),
                        "string",
                        FMarketRiskExportColumnSelection.getStoredScenarios(), "",
                        0, True, ttScenarios, None, False],
                ["stress_type",
                        "Stress type" + tab_name,
                        "string", None, "",
                        0, 0, ttStressType, None, False],
                ['Stress File Name',
                        'Stress file name' + tab_name,
                        'string', None, 'Stress',
                        0, 0, ttStressFileName, None, False],
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

    outtab = MarketRiskExportStressTab()
    outtab.LoadDefaultValues(__name__)
    return outtab
