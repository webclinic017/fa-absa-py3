""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/scripts/FAccountingEOD.py"
import acm

# run script
import FRunScriptGUI

# operations
from FOperationsIO import GetDefaultPath
from FOperationsLoggers import CreateLogger
from FOperationsDateUtils import AdjustDateToday, GetAccountingCurrencyCalendar
from FOperationsQueries import CreateFilter

# accounting
from FAccountingTaskRunnerEOD import AccountingTaskRunnerEOD

import FAccountingParams as Params

#-------------------------------------------------------------------------
class OperationsEODGUI(FRunScriptGUI.AelVariablesHandler):

    #-------------------------------------------------------------------------
    def __init__(self):
        variables = self.__CreateAelVariables()
        FRunScriptGUI.AelVariablesHandler.__init__(self, variables)

    #-------------------------------------------------------------------------
    def LogToFileCb(self, index, fieldValues):
        self.Logfile.enable(fieldValues[index], 'You have to check Log To File to be able to select a Logfile.')
        self.LogfilePath.enable(fieldValues[index])
        return fieldValues

    #-------------------------------------------------------------------------
    def TriggerTypes(self):
        return [trigger for trigger in acm.FEnumeration['enum(JournalTriggerType)'].Enumerators() if trigger != 'None']

    #-------------------------------------------------------------------------
    def __CreateAelVariables(self):
        dirSelectionLogfile = FRunScriptGUI.DirectorySelection()
        dirSelectionLogfile.SelectedDirectory(str(GetDefaultPath()))

        #-------------------------------------------------------------------------
        bookTT = 'Only trades matching the specified books will be processed.'
        triggerTT = 'Only Accounting Instructions matching the specified trigger types will be considered during the execution.'
        aftermidnightTT = 'Select this check box if the EOD job is started after midnight. The journals will then receive the previous day as process date.'
        runTradeEODTT = 'When enabled journals will be created/updated based on trades'
        runSettlementEODTT = 'When enabled journals will be created/updated based on settlements'
        ttLogToCon = 'Defines whether logging should be done to the console'
        ttLogToFile = 'Defines whether logging should be done to file.'
        ttLogFile = 'Name of the logfile. Could include the whole path, c:\log\...'
        ttDistributed = 'When enabled the EOD process will be run in distributed mode'
        updateProcessDateTT = 'When enabled the process date on the Books will be updated'

        #-------------------------------------------------------------------------
        variables = [['books', 'Books', 'string', acm.FBook.Select(""), None, 1, 1, bookTT, None, 1],
                     ['journalTriggerType', 'Trigger Types', 'string', self.TriggerTypes(), None, 1, 1, triggerTT, None, 1],
                     ['afterMidnight', 'EOD started after midnight', 'int', [1, 0], 0, 0, 0, aftermidnightTT],
                     ['createTradeBasedJournals', 'Create Journals based on Trades', 'int', [1, 0], 1, 1, 0, runTradeEODTT],
                     ['createSettlementBasedJournals', 'Create Journals based on Settlements', 'int', [1, 0], 0, 0, 0, runSettlementEODTT],
                     ['LogToConsole', 'Log to console_Logging', 'int', [1, 0], 1, 1, 0, ttLogToCon],
                     ['LogToFile', 'Log to file_Logging', 'int', [1, 0], 0, 1, 0, ttLogToFile, self.LogToFileCb],
                     ['LogfilePath', 'Log file path_Logging', dirSelectionLogfile, None, dirSelectionLogfile, 0, 1, 'The default log file path', None, None],
                     ['Logfile', 'Log file_Logging', 'string', None, 'AccountingEOD.log', 0, 0, ttLogFile, None, None],
                     ['updateProcessDate', 'Update Book process date', 'int', [1, 0], 1, 1, 0, updateProcessDateTT],
                     ['runDistributed', 'Distributed processing', 'int', [1, 0], 0, 0, 0, ttDistributed]]

        return variables


ael_gui_parameters = {'windowCaption' : 'Accounting EOD'}

ael_variables = OperationsEODGUI()

#-------------------------------------------------------------------------
def ael_main(variablesDict):

    # Log parameters
    logToConsole = variablesDict['LogToConsole']
    logToFile = variablesDict['LogToFile']
    filePath = "{}".format(variablesDict['LogfilePath'])
    fileName = "{}".format(variablesDict['Logfile'])

    books = CreateFilter(acm.FBook, 'OR', 'Name', variablesDict['books'], 'EQUAL').Select()
    ais = CreateFilter(acm.FAccountingInstruction, 'OR', 'JournalTriggerType', variablesDict['journalTriggerType'], 'EQUAL').Select()

    endOfDayDate = acm.Time.DateToday() if variablesDict['afterMidnight'] else acm.Time.DateAddDelta(acm.Time.DateToday(), 0, 0, 1)
    processDate = acm.Time.DateAddDelta(acm.Time.DateToday(), 0, 0, -1) if variablesDict['afterMidnight'] else acm.Time.DateToday()

    eodParams = {}
    eodParams['books'] = books
    eodParams['runTradeEOD'] = variablesDict['createTradeBasedJournals']
    eodParams['runSettlementEOD'] = variablesDict['createSettlementBasedJournals']
    eodParams['afterMidnight'] = variablesDict['afterMidnight']
    eodParams['runDistributed'] = variablesDict['runDistributed'] if 'runDistributed' in variablesDict else False
    eodParams['processDate'] = processDate
    eodParams['updateProcessDate'] = variablesDict['updateProcessDate']

    engineParams = {}
    engineParams['bookIds'] = books
    engineParams['treatmentIds'] = []
    engineParams['aiIds'] = ais
    engineParams['startDate'] = AdjustDateToday(GetAccountingCurrencyCalendar(), -Params.daysBack)
    engineParams['endDate'] = AdjustDateToday(GetAccountingCurrencyCalendar(), Params.daysForward)
    engineParams['endOfDayDate'] = endOfDayDate
    engineParams['processDate'] = processDate
    engineParams['testMode'] = False

    try:
        logger = CreateLogger(logToConsole, logToFile, Params.detailedLogging, filePath, fileName)
        AccountingTaskRunnerEOD.CreateAndRun(logger, eodParams, engineParams)
    except Exception as e:
        acm.Log('Failed to complete Accounting EOD: {}'.format(str(e)))

