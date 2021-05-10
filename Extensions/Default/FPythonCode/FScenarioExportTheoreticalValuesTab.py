""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/risk_export/./etc/FScenarioExportTheoreticalValuesTab.py"
"""----------------------------------------------------------------------------
MODULE
    FOutputFileSettingsTab - Scenario settings tab

    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

    This is a GUI tab in the FScenarioExportReport GUI which contains settings
    that sets up scenario calculations.

----------------------------------------------------------------------------"""


import acm


import FRunScriptGUI


from FScenarioExportScenarioPVManager import (DISPLAY_TYPE_ABSOLUTE,
        DISPLAY_TYPE_RELATIVE)


tab_name = "_scenario settings"
trueFalse = ["False", "True"]
displayTypes = [DISPLAY_TYPE_ABSOLUTE, DISPLAY_TYPE_RELATIVE]


class ScenarioExportTheoreticalValuesTab(FRunScriptGUI.AelVariablesHandler):

    def __init__(self):

        cvRiskTypes = acm.FEnumeration["EnumRiskFactorTypes"].Values()
        ttScenarioFile = ('The name or path to an external scenario file. If '
                'no path is given, the path fallbacks to the FCS_RISK_DIR '
                'environment variable first and then the current working '
                'directory. ')
        ttRiskTypes = ('The Risk Factor Type. Only Risk Factor Specifications '
                'with Risk Factor Group of this type will be shifted.')
        ttVarType = ('Freely defined mandatory text describing the VaR Type. '
                'For instance \'Historical\'.')
        ttStressScenarioFile = ('The name or path to an external scenario '
                'file. If no path is given, the path fallbacks to the '
                'FCS_RISK_DIR environment variable first and then the current '
                'working directory. ')
        ttDisplayType = 'Export Absolute or Relative scenario values.'
        ttCreateMarketValue = "Calculate market value and feed into report?"
        variables = [
                # [VariableName,
                #       DisplayName,
                #       Type, CandidateValues, Default,
                #       Mandatory, Multiple, Description, InputHook, Enabled]
                ["scenario_file",
                        "PV Scenario File" + tab_name,
                        "FFileSelection", None, None,
                        0, 1, ttScenarioFile],
                ["risk_types",
                        "Risk Types" + tab_name,
                        "EnumRiskFactorTypes", cvRiskTypes, None,
                        0, 1, ttRiskTypes],
                ["var_type",
                        "VaR Type" + tab_name,
                        "string", None, "",
                        0, 0, ttVarType],
                ["stress_scenario_file",
                        "Stress Scenario File" + tab_name,
                        "FFileSelection", None, None,
                        0, 1, ttStressScenarioFile],
                ["display_type",
                        "Display Type" + tab_name,
                        "string", displayTypes, displayTypes[1],
                        0, 0, ttDisplayType],
                ["create_market_value",
                        "Market Value" + tab_name,
                        "string", trueFalse, "False",
                        1, 0, ttCreateMarketValue]
        ]
        FRunScriptGUI.AelVariablesHandler.__init__(self, variables, __name__)


def getAelVariables():

    outtab = ScenarioExportTheoreticalValuesTab()
    outtab.LoadDefaultValues(__name__)
    return outtab


def incl_in_residual_value(risk_types_incl, risk_type):

    if risk_type in risk_types_incl:
        return 1
    else:
        return 0
