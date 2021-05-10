""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/corporate_actions_workbench/./etc/FCorpActionsWorkbenchLogger.py"
import FIntegratedWorkbenchLogging


LOGGING_LEVEL = 2

def GetLogger():
    caLogger = FIntegratedWorkbenchLogging.GetLogger('CorpAction:')
    FIntegratedWorkbenchLogging.SetLoggingLevel(caLogger, LOGGING_LEVEL)
    return caLogger

logger = GetLogger()