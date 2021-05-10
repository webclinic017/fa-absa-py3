""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/aa_integration/./etc/FAACalcFileImportTab.py"
"""----------------------------------------------------------------------------
MODULE
    FAACalcSensitivityBasedPLTab - General setting.

    (c) Copyright 2019 by FIS FRONT ARENA. All rights reserved.

DESCRIPTION

    
----------------------------------------------------------------------------"""


import acm
import FRunScriptGUI

tab_name = "_CSV File Import"
fileFilter=".csv Files (*.csv)|*.csv|All Files (*.*)|*.*||"
data_file = FRunScriptGUI.InputFileSelection(fileFilter)
ttDirPath = 'The path to the directory containing the data files to upload.'
directorySelection = FRunScriptGUI.DirectorySelection()

class AACalcFileImportTab(FRunScriptGUI.AelVariablesHandler):

    def __init__(self):
        variables = [
                # [VariableName,
                #       DisplayName,
                #       Type, CandidateValues, Default,
                #       Mandatory, Multiple, Description, InputHook, Enabled]
                # ExportCalculatedValues expects these to be strings for now.
                ['runCalcCVAImport',
                    'Run calc{0}'.format(tab_name), 'int', [0, 1], 0, True,
                    False, 'Run Sensitivity Based PL Analysis', self._enable, True],
                ['FilePath',
                    'Import File Path{0}'.format(tab_name),
                    directorySelection, None, directorySelection,
                    1, 1, ttDirPath],
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

    ael_vars = AACalcFileImportTab()
    ael_vars.LoadDefaultValues(__name__)

    return ael_vars
