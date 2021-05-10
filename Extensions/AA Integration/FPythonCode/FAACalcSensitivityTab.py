""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/aa_integration/./etc/FAACalcSensitivityTab.py"
"""----------------------------------------------------------------------------
MODULE
    FAACalcSensitivityBasedPLTab - General setting.

    (c) Copyright 2019 by FIS FRONT ARENA. All rights reserved.

DESCRIPTION

    
----------------------------------------------------------------------------"""


import acm
import FRunScriptGUI

tab_name = "_Sensitivity"
trdTagfileFilter=".aap Files (*.aap)|*.aap|All Files (*.*)|*.*||"
trdTag_file = FRunScriptGUI.InputFileSelection(trdTagfileFilter)
bookTagfileFilter=".csv Files (*.csv)|*.csv|All Files (*.*)|*.*||"
bookTag_file = FRunScriptGUI.InputFileSelection(bookTagfileFilter)
validatefileFilter="Sensitivity files Configuration (*.vtg)|*.vtg|All Files (*.*)|*.*||"
v_file = FRunScriptGUI.InputFileSelection(bookTagfileFilter)
datafileFilter=".csv Files (*.csv)|*.csv|All Files (*.*)|*.*||"
data_file = FRunScriptGUI.InputFileSelection(datafileFilter)

ttDirPath = 'The path to the directory containing the data files to upload.'

class AACalcSensitivityTab(FRunScriptGUI.AelVariablesHandler):

    def __init__(self):
        variables = [
                # [VariableName,
                #       DisplayName,
                #       Type, CandidateValues, Default,
                #       Mandatory, Multiple, Description, InputHook, Enabled]
                # ExportCalculatedValues expects these to be strings for now.
                ['runCalcSen',
                    'Run calc{0}'.format(tab_name), 'int', [0, 1], 0, True,
                    False, 'Run Sensitivity Based PL Analysis', self._enable, True],
                 ['SensitivityData',
                    'Sensitivity Data{0}'.format(tab_name),
                    data_file, None, data_file,
                    0, 1, ttDirPath],
                ['TradeTagsSen',
                    'Trade Tags Data File{0}'.format(tab_name),
                    trdTag_file, None, trdTag_file,
                    0, 1, ttDirPath],
                ['BookTagsSen',
                    'Book Tags Data File{0}'.format(tab_name),
                    bookTag_file, None, bookTag_file,
                    0, 1, ttDirPath],
                ['ValidateFileSen',
                    'Validate Market Sensitivities File{0}'.format(tab_name),
                    v_file, None, v_file,
                    0, 1, ttDirPath],
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

    ael_vars = AACalcSensitivityTab()
    ael_vars.LoadDefaultValues(__name__)

    return ael_vars