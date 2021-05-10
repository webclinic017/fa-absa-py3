""" Compiled: 2020-08-14 16:40:05 """

#__src_file__ = "extensions/arc_writers/./etc/FMarketRiskExportStressedVaRTab.py"
"""----------------------------------------------------------------------------
MODULE
    FMarketRiskExportStressedVaRTab - Stressed VaR settings tab

DESCRIPTION

    This is a GUI tab in the FMarketRiskExport GUI which contains settings
    that set up stressed VaR calculations.

----------------------------------------------------------------------------"""


import acm


import FRunScriptGUI

DISPLAY_TYPE_ABSOLUTE = "Absolute"
DISPLAY_TYPE_RELATIVE = "Relative"

tab_name = "_Stressed VaR "
displayTypes = [DISPLAY_TYPE_ABSOLUTE, DISPLAY_TYPE_RELATIVE]


class MarketRiskExportStressedVaRTab(FRunScriptGUI.AelVariablesHandler):

    def __init__(self):

        cvRiskTypes = acm.FEnumeration["EnumRiskFactorTypes"].Values()
        ttRiskTypes = ('The risk factor type. Only risk factor specifications '
                'with risk factor group of this type will be shifted.')
        ttVarType = ('Freely defined mandatory text describing the VaR type. '
                'For instance \'Historical\'.')
        ttStressedVaRScenarioFile = ('The name or path to an external scenario '
                'file. If no path is given, the path fallbacks to the '
                'FCS_RISK_DIR environment variable first and then the current '
                'working directory. ')
        ttStressedVaRFileName = ('Name of the file containing the stress '
                'value results from the scenario tab.')
        ttScenarioCountFileName = ('Name of the file containing the scenario '
                'count results. if not specified, the file name will be '
                'sv_scenariocount')
        ttScenarioDatesFileName = ('Name of the file containing the scenario '
                'dates. if not specified, the file name will be '
                'sv_scenariodates')
        ttDecayFactor = ('The value of the decay factor to use for '
                'VaR calculations. If not specified, no decay factor '
                'will be used.')
        ttDecayFactorFileName = ('Name of the file containing the decay '
                'factor value. if not specified, the file name will be '
                'decay_factor')
        variables = [
                # [VariableName,
                #       DisplayName,
                #       Type, CandidateValues, Default,
                #       Mandatory, Multiple, Description, InputHook, Enabled]
                ['runStressedVaRReports',
                    'Run reports{0}'.format(tab_name), 'int', [0, 1], 0, True,
                    False, 'Run Stressed VaR Reports', self._enable, True],
                ["stressed_var_scenario_file",
                        "Stressed VaR scenario file" + tab_name,
                        "FFileSelection", None, None,
                        0, 1, ttStressedVaRScenarioFile, None, False],
                ["stressed_var_risk_types",
                        "Risk types" + tab_name,
                        "EnumRiskFactorTypes", cvRiskTypes, None,
                        0, 1, ttRiskTypes, None, False],
                ["stressed_var_type",
                        "VaR type" + tab_name,
                        "string", None, "",
                        0, 0, ttVarType, None, False],
                ["stressed_var_decay_factor",
                        "Decay factor" + tab_name,
                        "string", None, "",
                        0, 0, ttDecayFactor, None, False],
                ['Stressed VaR File Name',
                        'Stressed VaR file name' + tab_name,
                        'string', None, 'StressedVaR',
                        0, 0, ttStressedVaRFileName, None, False],
                ['stressed_var_scenario_count_file_name',
                        'Scenario count file name' + tab_name,
                        'string', None, 'sv_scenario_count',
                        0, 0, ttScenarioCountFileName, None, False],
                ['stressed_var_scenario_dates_file_name',
                        'Scenario dates file name' + tab_name,
                        'string', None, 'sv_scenario_dates',
                        0, 0, ttScenarioDatesFileName, None, False],
                ['stressed_var_decay_factor_file_name',
                        'Decay factor file name' + tab_name,
                        'string', None, 'sv_decay_factor',
                        0, 0, ttDecayFactorFileName, None, False]
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

    outtab = MarketRiskExportStressedVaRTab()
    outtab.LoadDefaultValues(__name__)
    return outtab
