""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/corporate_actions_workbench/./etc/FCASuggestedTasks.py"
"""--------------------------------------------------------------------------
MODULE
    FCASuggestedTasks

DESCRIPTION
    Functions supporting start Corporate Action tasks.

-----------------------------------------------------------------------------"""
import acm

PROCESSELECTIONS_MODULE_NAME = 'FProcessCorpActions'
PROCESSELECTIONS_PARAMETERS_TEXT = ('Logmode=2;MailList=;'
        'ReportMessageType=Full Log;Logfile=BDP.log;LogToConsole=1;'
        'LogToFile=0;SendReportByMail=0;CorpActions={0};')

GENERATEELECTIONS_MODULE_NAME = 'FCorpActionCalculatePositions'
GENERATEELECTIONS_PARAMETERS_TEXT = ('Logmode=2;MailList=;'
        'ReportMessageType=Full Log;Logfile=BDP.log;LogToConsole=1;'
        'LogToFile=0;SendReportByMail=0;CorpActions={0};PortfolioGrouper=;')


ROLLBACKPROCESSEDELECTIONS_MODULE_NAME = 'FStartRollback'
ROLLBACKPROCESSEDELECTIONS_PARAMETERS_TEXT = ('Logmode=2;MailList=;'
        'ReportMessageType=Full Log;Logfile=BDP.log;LogToConsole=1;'
        'LogToFile=0;SendReportByMail=0;rollbackSpec={0};void=Delete;'
	'instruments=;')


def _createTheAelTask(taskName, moduleName, paramsText=''):
    aelTask = acm.FAelTask[taskName]
    if not aelTask:
        aelTask = acm.FAelTask()
        aelTask.Name(taskName)
    aelTask.ModuleName(moduleName)
    aelTask.ParametersText(paramsText)
    aelTask.Commit()
    return aelTask


def startSuggestTask(taskName, moduleName, paramsText=''):
    theAelTask = _createTheAelTask(taskName, moduleName, paramsText)
    acm.StartApplication('Run Script', theAelTask)

