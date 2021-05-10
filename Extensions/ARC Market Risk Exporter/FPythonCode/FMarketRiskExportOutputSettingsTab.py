""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/arc_writers/./etc/FMarketRiskExportOutputSettingsTab.py"
"""----------------------------------------------------------------------------
MODULE
    FMarketRiskExportOutputSettingsTab - General output settings

    (c) Copyright 2019 by FIS FRONT ARENA. All rights reserved.

DESCRIPTION

    This is a GUI tab in the FMarketRiskExport GUI which contains common 
    output settings for all writers.

----------------------------------------------------------------------------"""


import FRunScriptGUI
import FLogger


logger = FLogger.FLogger.GetLogger('FAReporting')
trueFalse = ['False', 'True']


def getDateFormats():

    return ['%d%m%y', '%y%m%d', '%d%m%y%H%M', '%y%m%d%H%M', '%d%m%y%H%M%S',
            '%y%m%d%H%M%S']

    
class MarketRiskExportOutputSettingsTab(FRunScriptGUI.AelVariablesHandler):

    def __init__(self):

        directorySelection = FRunScriptGUI.DirectorySelection()
        tab_name = '_Output settings'
        ttFilePath = ('Path to the directory where the reports should be '
                'created. Environment variables can be used for '
                'Windows (%VAR%) or Unix ($VAR).')
        ttOutputFilePrefix = ('Optional prefix for output file names.')
        ttCreateDirectoryWithDate = ('Create a directory with the reference '
                'date as the directory name')
        ttOverwriteIfFileExists = ('If a file with the same name and path '
                'already exist, overwrite it.')
        ttDelimiter = 'The delimiter character use in the report'
        ttSubDelimiter = 'The sub delimiter character use in the report'
        ttCreateUtilityFiles = "Create Risk Cube utility files."
        ttExportFormat = "Export to Adaptiv Memory Cube or ArtiQ Cube"
        variables = [
                # [VariableName,
                #       DisplayName,
                #       Type, CandidateValues, Default,
                #       Mandatory, Multiple, Description, InputHook, Enabled]
                ['output_dir',
                        'Directory path' + tab_name,
                        directorySelection, None, directorySelection,
                        0, 1, ttFilePath, None, 1],
                ['Output File Prefix',
                        'Output file prefix' + tab_name,
                        'string', None, '',
                        0, 0, ttOutputFilePrefix],
                ['Create directory with date',
                        'Create directory with reference date' + tab_name,
                        'string', trueFalse, 'True',
                        1, 0, ttCreateDirectoryWithDate, None, 1],
                ['Overwrite if file exists',
                        'Overwrite if files exist' + tab_name,
                        'string', trueFalse, 'True',
                        1, 0, ttOverwriteIfFileExists],
                ['delimiter',
                        'Delimiter' + tab_name,
                        'char', None, '|',
                        1, 0, ttDelimiter, None, 1],
                ['sub_delimiter',
                        'Sub-delimiter' + tab_name,
                        'char', None, ',',
                        1, 0, ttSubDelimiter, None, 1],
                ]
        FRunScriptGUI.AelVariablesHandler.__init__(self, variables, __name__)


def getAelVariables():

    outtab = MarketRiskExportOutputSettingsTab()
    outtab.LoadDefaultValues(__name__)
    return outtab
