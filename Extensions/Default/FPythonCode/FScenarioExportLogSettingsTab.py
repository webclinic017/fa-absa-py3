""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/risk_export/./etc/FScenarioExportLogSettingsTab.py"
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


import FScenarioExportUtils


trueFalse = ['False', 'True']


LOG_BASE_FILE_NAME = "risk_export_log"


class ScenarioExportLogSettingsTab(FRunScriptGUI.AelVariablesHandler):

    def __init__(self):

        directorySelection = FRunScriptGUI.DirectorySelection()
        ttLogFilePath = ('The file path to the directory where the log files '
                'should be put. Environment variables can be specified for '
                'Windows (%VAR%) or Unix ($VAR).')
        ttLogFileName = 'The file name of the logging output'
        ttOverwriteIfLogFileExists = ('If a file with the same name and path '
                'already exist, overwrite it?')
        ttLogToConsole = 'Log messages to sys.stdout?'
        ttLogToPrime = 'Log messages to ael.log?'
        ttLogDebugMessages = 'Log debug messages?'
        variables = [
                # [VariableName,
                #       DisplayName,
                #       Type, CandidateValues, Default,
                #       Mandatory, Multiple, Description, InputHook, Enabled]
                ['log file path',
                        'File Path_Log settings',
                        directorySelection, None, directorySelection,
                        0, 1, ttLogFilePath, None, 1],
                ['log file name',
                        'File Name_Log settings',
                        'string', None, '',
                        0, 0, ttLogFileName],
                ['overwrite if log file exists',
                        'Overwrite if Log File Exists_Log settings',
                        'string', trueFalse, 'True',
                        1, 0, ttOverwriteIfLogFileExists],
                ['log to console',
                        'Log to Console_Log settings',
                        'string', trueFalse, 'True',
                        1, 0, ttLogToConsole],
                ['log to prime',
                        'Log to Prime Log_Log settings',
                        'string', trueFalse, 'False',
                        1, 0, ttLogToPrime],
                ['log debug messages',
                        'Log debug messages_Log settings',
                        'string', trueFalse, 'False',
                        1, 0, ttLogDebugMessages]
        ]
        FRunScriptGUI.AelVariablesHandler.__init__(self, variables, __name__)


def getAelVariables():

    outtab = ScenarioExportLogSettingsTab()
    outtab.LoadDefaultValues(__name__)
    return outtab


def base_log_file_name(supplied_file_name):

    if not supplied_file_name:
        return LOG_BASE_FILE_NAME
    else:
        return supplied_file_name


def create_log_file_path_or_not(log_file_dir_path, log_file_name, overwrite):

    if isinstance(log_file_dir_path, str):
        outdir = log_file_dir_path
    else:
        outdir = log_file_dir_path.AsString()
    pt = FScenarioExportUtils.get_output_file_name(outdir,
        base_log_file_name(log_file_name), overwrite, False)
    return pt


def logger_setup_core(log_level, log_path_or_not, logger_name, log_to_console,
    log_to_prime):

    logger = FLogger.FLogger.GetLogger(logger_name)
    if log_path_or_not:
        logger.Reinitialize(level=log_level,
            logToFileAtSpecifiedPath=log_path_or_not, lock=True,
            logToConsole=log_to_console, logToPrime=log_to_prime)
    else:
        logger.Reinitialize(level=log_level,
            logToConsole=log_to_console, logToPrime=log_to_prime,
            lock=True)


def logger_setup(ael_variables, logger_name):

    log_file_path_gui = ael_variables["log file path"]
    log_file_name = ael_variables["log file name"]
    overwrite_log_file = trueFalse.index(
        ael_variables["overwrite if log file exists"])
    log_to_console = trueFalse.index(ael_variables["log to console"])
    log_to_prime = trueFalse.index(ael_variables["log to prime"])
    log_debug_messages = trueFalse.index(ael_variables["log debug messages"])

    log_file_path = create_log_file_path_or_not(log_file_path_gui,
        log_file_name, overwrite_log_file)

    if log_debug_messages:
        log_level = 2
    else:
        log_level = 1

    logger_setup_core(log_level, log_file_path, logger_name,
        log_to_console, log_to_prime)
