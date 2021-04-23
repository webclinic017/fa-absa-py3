import acm
import FBDPGui
reload(FBDPGui)
from FBDPCurrentContext import Logme
from FBDPCurrentContext import Summary
from FX_AUTOROLL_PROCESS import AUTOROLL_PROCESS


queryFolderDictionary = {}
queryFolderList = [q for q in acm.FStoredASQLQuery.Select('') if 'FX_AUTOROLL_' in q.Name()]
for queryFolder in queryFolderList:
    queryFolderDictionary[queryFolder.Name()] = queryFolder.Oid()

autorollOptionList = ['Overnight', 'Tom Next', 'Both']

ael_variables = FBDPGui.LogVariables(
                    ['query_folder', 'Query Folder', 'string', queryFolderDictionary.keys(), None, 1, 1, 'Query folder containing the aggregate trades on which processing should happen.', None, 1],
                    ['autorollRunOption', 'Run Option', 'string', autorollOptionList, 'Both', 1, 0, 'Specify which option should be used to run Autorolls. Overnight will only roll overnight position to Tom Next. Tom Next will only run Tom Next position to SPOT. Both will roll overnight to Tom Next and then Tom Next to SPOT.', None, 1],
                    ['rollZARAgainstUSD', 'Roll ZAR Against USD', 'bool', [0, 1], 0, 1, 0, 'ZAR will be rolled against USD and not the normal functionality where USD is rolled against ZAR.', None, 1]
                    )

def getQueryFolder(oid):
    return acm.FStoredASQLQuery[oid]

def ael_main(dict):
    scriptName = __name__
    queryFolderNames = dict['query_folder']
    runOption = dict['autorollRunOption']
    rollZARAgainstUSD = dict['rollZARAgainstUSD']
    
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
    for queryFolderName in queryFolderNames:
        Logme()('INFO: \t\t%s' %queryFolderName, 'INFO')
    
    if runOption in autorollOptionList:
        numberOfQueryFolders = len(queryFolderNames)
        counter = 0
        for queryFolderName in queryFolderNames:
            Logme()('\n')
            counter = counter + 1
            Logme()('INFO: Processing query folder %s : %i from %i.' %(queryFolderName, counter, numberOfQueryFolders))
            
            acmQueryFolder = getQueryFolder(queryFolderDictionary[queryFolderName])
            autoRollProcess = AUTOROLL_PROCESS(acmQueryFolder, runOption, rollZARAgainstUSD)
    else:
        Logme()('The value for the Run Option: %s is invalid. No Autorolls will be done.' %runOption, 'WARNING')
    
    Summary().log(dict)
    Logme()('%s finished successfully' %scriptName, 'FINISH')

def runFXAutorollFromMenu(self):
    acm.RunModuleWithParameters('FX_AUTOROLL', 'Standard')
