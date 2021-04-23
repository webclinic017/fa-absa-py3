""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/aa_integration/./etc/AAIntegrationGuiCommon.py"
import os

import acm

import FRunScriptGUI

import AAIntegrationUtility
import importlib
importlib.reload(AAIntegrationUtility)

ACCOUNTING_CURRENCY_CALENDAR = acm.GetFunction(
    'mappedValuationParameters', 0
)().Parameter().AccountingCurrency().Calendar()

def getPathSelector(is_dir, is_input, types=None, path=None):
    selector = None
    if is_dir:
        selector = FRunScriptGUI.DirectorySelection()
    else:
        types = types or 'All Files (*.*)|*.*||'
        if is_input:
            selector = FRunScriptGUI.InputFileSelection(types)
        else:
            selector = FRunScriptGUI.OutputFileSelection(types)

    if path:
        if is_dir:
            selector.selectedDirectory = AAIntegrationUtility.forwardSlashedPath(
                path=path, real=False, check=is_input
            )
        else:
            selector.SelectedFile = AAIntegrationUtility.forwardSlashedPath(
                path=path, real=False, check=is_input
            )

    return selector

def getLoggingAelVariables(caller, log_filename):
    def logfile_cb(index, fieldValues):
        caller.ael_variables.Logfile.enable(
            fieldValues[index],
            'You have to check Log To File to be able to select a Logfile.'
        )
        return fieldValues

    logFileSelection = getPathSelector(
        is_dir=False, is_input=False,
        path=os.path.join('C:\\', 'temp', log_filename)
    )
    ttLogMode = 'Defines the amount of logging produced.'
    ttLogToCon = (
        'Whether logging should be done in the Log Console or not.'
    )
    ttLogToFile = 'Defines whether logging should be done to file.'
    ttLogFile = (
        'Name of the logfile. Could include the whole path, c:\log\...'
    )
    ael_variables = [
        #[VariableName,
        #    DisplayName,
        #    Type, CandidateValues, Default,
        #    Mandatory, Multiple, Description, InputHook, Enabled]
        ['Logmode',
            'Logmode_Logging',
            'int', [1, 2, 3, 4], 1,
            1, 0, ttLogMode],
        ['LogToConsole',
            'Log to console_Logging',
            'int', [0, 1], 1,
            1, 0, ttLogToCon],
        ['LogToFile',
            'Log to file_Logging',
            'int', [0, 1], 0,
            1, 0, ttLogToFile, logfile_cb],
        ['Logfile',
            'Logfile_Logging',
            logFileSelection, None, logFileSelection,
            0, 1, ttLogFile, None, None],
    ]
    return ael_variables
