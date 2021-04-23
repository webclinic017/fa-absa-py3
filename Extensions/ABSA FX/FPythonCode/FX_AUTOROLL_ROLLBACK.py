import acm
import FBDPGui
import importlib
importlib.reload(FBDPGui)
from FBDPCurrentContext import Logme
from FBDPCurrentContext import Summary
from FX_AUTOROLL_ROLLBACK_PROCESS import ROLLBACK_PROCESS

ael_variables = FBDPGui.LogVariables(
                    ['query_folder', 'Query Folder', acm.FStoredASQLQuery, acm.FStoredASQLQuery, None, 1, 1, 'Query Folders where the trades with type Rollout will be voided that was created on the selected date.', None, 1],
                    ['reportDate', 'Date', 'string', None, acm.Time.DateToday(), 0, 0, 'Date on which trades were created that will be Voided.', None, 1]
                    )

def ael_main(dict):
    scriptName = __name__
    query_folders = dict['query_folder']
    reportDate = dict['reportDate']
    
    import FBDPCurrentContext
    FBDPCurrentContext.CreateLog(scriptName,
                      dict['Logmode'],
                      dict['LogToConsole'],
                      dict['LogToFile'],
                      dict['Logfile'],
                      dict['SendReportByMail'],
                      dict['MailList'],
                      dict['ReportMessageType'])

    Logme()('INFO: STARTING SCRIPT: %s with QUERY FOLDERS:' %(scriptName), 'INFO')
    for queryFolder in query_folders:
        Logme()('INFO: \t\t%s' %queryFolder.Name(), 'INFO')
    
    numberOfQueryFolders = len(query_folders)
    counter = 0
    for queryFolder in query_folders:
        Logme()('\n')
        counter = counter + 1
        Logme()('INFO: Processing query folder %s : %i from %i.' %(queryFolder.Name(), counter, numberOfQueryFolders))
        rollBack = ROLLBACK_PROCESS(queryFolder, reportDate)
        rollBack.voidTradePackets()
        
    Summary().log(dict)
    Logme()('%s finished successfully' %scriptName, 'FINISH')

def runFXAutorollRollbackFromMenu(self):
    acm.RunModuleWithParameters('FX_AUTOROLL_ROLLBACK', 'Standard')
