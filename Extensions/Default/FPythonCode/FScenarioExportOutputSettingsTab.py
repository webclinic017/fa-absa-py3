""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/risk_export/./etc/FScenarioExportOutputSettingsTab.py"
"""----------------------------------------------------------------------------
MODULE
    FScenarioExportOutputSettingsTab - General output settings

    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

    This is a GUI tab in the FScenarioExport GUI which contains settings
    which are changed frequently, e.g. name of the report.

----------------------------------------------------------------------------"""


import FRunScriptGUI
import FLogger


logger = FLogger.FLogger.GetLogger('FAReporting')
trueFalse = ['False', 'True']


def getDateFormats():

    return ['%d%m%y', '%y%m%d', '%d%m%y%H%M', '%y%m%d%H%M', '%d%m%y%H%M%S',
            '%y%m%d%H%M%S']


class ScenarioExportOutputSettingsTab(FRunScriptGUI.AelVariablesHandler):

    def __init__(self):

        directorySelection = FRunScriptGUI.DirectorySelection()
        tab_name = '_Output settings'
        ttFilePath = ('The file path to the directory where the report '
                'should be put. Environment variables can be specified for '
                'Windows (%VAR%) or Unix ($VAR).')
        ttOutputFilePrefix = ('An optional text that will be placed before '
                'each output file\'s name.')
        ttPVScenarioFileName = ('Name of the file containing the scenario PV '
                'results from the scenario tab.')
        ttStressScenarioFileName = ('Name of the file containing the stress '
                'value results from the scenario tab.')
        ttMarketValueFileName = ('Name of the file containing the market '
                'value results from the scenario tab.')
        ttPLFileName = ('Name of the file containing results from the profit '
                'and loss tab, that is, profit and loss values.')
        ttCreateDirectoryWithDate = ('Create a directory with the reference '
                'date as the directory name')
        ttOverwriteIfFileExists = ('If a file with the same name and path '
                'already exist, overwrite it?')
        ttDelimiter = 'The delimiter character use in the report'
        ttSubDelimiter = 'The sub delimiter character use in the report'
        ttCreateUtilityFiles = "Create Risk Cube utility files."
        variables = [
                # [VariableName,
                #       DisplayName,
                #       Type, CandidateValues, Default,
                #       Mandatory, Multiple, Description, InputHook, Enabled]
                ['File Path',
                        'File Path' + tab_name,
                        directorySelection, None, directorySelection,
                        0, 1, ttFilePath, None, 1],
                ['Output File Prefix',
                        'Output File Prefix' + tab_name,
                        'string', None, '',
                        0, 0, ttOutputFilePrefix],
                ['PV Scenario File Name',
                        'PV Scenario File Name' + tab_name,
                        'string', None, '',
                        0, 0, ttPVScenarioFileName],
                ['Stress Scenario File Name',
                        'Stress Scenario File Name' + tab_name,
                        'string', None, '',
                        0, 0, ttStressScenarioFileName],
                ['Market Value File Name',
                        'Market Value File Name' + tab_name,
                        'string', None, '',
                        0, 0, ttMarketValueFileName],
                ['PL File Name',
                        'Profit and Loss File Name' + tab_name,
                        'string', None, '',
                        0, 0, ttPLFileName],
                ['Create directory with date',
                        'Create Directory with Reference Date' + tab_name,
                        'string', trueFalse, 'True',
                        1, 0, ttCreateDirectoryWithDate, None, 1],
                ['Overwrite if file exists',
                        'Overwrite if File Exists' + tab_name,
                        'string', trueFalse, 'True',
                        1, 0, ttOverwriteIfFileExists],
                ['delimiter',
                        'Delimiter' + tab_name,
                        'char', None, '|',
                        1, 0, ttDelimiter],
                ['sub_delimiter',
                        'Sub Delimiter' + tab_name,
                        'char', None, ',',
                        1, 0, ttSubDelimiter],
                ["create_utility_files",
                        "Create Risk Cube utility files" + tab_name,
                        "string", trueFalse, "False",
                        1, 0, ttCreateUtilityFiles],
                ]
        FRunScriptGUI.AelVariablesHandler.__init__(self, variables, __name__)


def getAelVariables():

    outtab = ScenarioExportOutputSettingsTab()
    outtab.LoadDefaultValues(__name__)
    return outtab
