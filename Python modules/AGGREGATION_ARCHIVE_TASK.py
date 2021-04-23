import acm
from FBDPCurrentContext import Logme
from FBDPCurrentContext import Summary
import FBDPGui
reload(FBDPGui)
from AGGREGATION_GEN_HELPERS import GENERIC_HELPERS
from AGGREGATION_CASH_POSTING_ARCHIV import AGGREGATION_ARCHIVE
from AGGREGATION_CASH_POSTING_ARCHIV import AGGREGATION_DEAGGREGATE
from AGGREGATION_PARAMETERS import PARAMETERS

archive_options = {'Trade Dependencies Only' : 'Trade',
                   'Instrument Dependencies Only' : 'Instrument',
                   'Trade and Instrument Dependancies' : 'Both'
                    }

ael_variables = FBDPGui.LogVariables(
                    ['query_folder', 'Query Folder', acm.FStoredASQLQuery, acm.FStoredASQLQuery, None, 1, 1, 'Query folder containing the aggregate trades on which processing should happen.', None, 1],
                    ['deArchiveFlag', 'De-Archive', 'bool', [0, 1], 0, 0, 0, 'If not selected, archiving will take place. If selected, de-archiving will take place.', None, 1],
                    ['archivingOption', 'Archive/De-Archive Option', 'string', archive_options.keys(), 'Trade and Instrument Dependancies', 1, 0, 'The aggregated trades/instruments from the selected trades will be affected.', None, 1],
                    ['deAggregateFlag', 'De-Aggregate', 'bool', [0, 1], 0, 0, 0, 'All the aggregated trades with their trade and instrument dependencies will be de-archived and the cash posting trade will be deleted.', None, 1]
                )

def ael_main(dict):
    scriptName = __name__
    queryFolder = dict['query_folder'][0]
    PARAMETERS.summaryDict = {}
    
    import FBDPCurrentContext
    FBDPCurrentContext.CreateLog(scriptName,
                      dict['Logmode'],
                      dict['LogToConsole'],
                      dict['LogToFile'],
                      dict['Logfile'],
                      dict['SendReportByMail'],
                      dict['MailList'],
                      dict['ReportMessageType'])

    Logme()('INFO: STARTING SCRIPT: %s with QUERY FOLDER %s' %(scriptName, queryFolder.Name()), 'INFO')
    
    Logme()('DEBUG: Selecting trades from query folder.', 'DEBUG')
    aggregateTrades = queryFolder.Query().Select()
    
    nbrOfTrades = len(aggregateTrades)
    Logme()('INFO: Number of trades to process: %i' %nbrOfTrades, 'INFO')
    
    actionSelected = dict['archivingOption']
    
    idx = 0
    while idx < nbrOfTrades:
        lower = idx
        if idx + 10 > nbrOfTrades:
            upper = nbrOfTrades
        else:
            upper = idx + 10

        Logme()('*' * 150, 'INFO')
        Logme()('INFO: Processing items %i to %i from a total of: %i objects' %(lower, upper, nbrOfTrades), 'INFO')
        Logme()('*' * 150, 'INFO')
    
        trades = aggregateTrades[lower:upper]
        
        if dict['deAggregateFlag'] == 1:
            acm.BeginTransaction()
            #try:
            archiveClass = AGGREGATION_ARCHIVE(actionSelected, trades, 0)
            archiveClass.deArchiveObjects()
            aggregateClass = AGGREGATION_DEAGGREGATE(trades)
            aggregateClass.deaggregateTrades()
            aggregateClass.deleteCachPostingTrades()
            acm.CommitTransaction()
            #except Exception, e:
            #    acm.AbortTransaction()
            #    msg = 'ERROR: Could not de-aggregate trades. Got the following error: {0}'.format(e)
            #    Logme()(msg, 'ERROR')
            #continue
        else:
            deArchiveFlag = dict['deArchiveFlag']
            if deArchiveFlag == 0:
                #try:
                archiveClass = AGGREGATION_ARCHIVE(actionSelected, trades, 1)
                archiveClass.archiveObjects()
                #except Exception, e:
                #    msg = 'ERROR: Could not de-archive trade dependencies. Got the following error: {0}'.format(e)
                #    Logme()(msg, 'ERROR')
                #continue
            else:
                try:
                    archiveClass = AGGREGATION_ARCHIVE(actionSelected, trades, 0)
                    archiveClass.deArchiveObjects()
                except Exception, e:
                    msg = 'ERROR: Could not archive trade dependencies. Got the following error: {0}'.format(e)
                    Logme()(msg, 'ERROR')
                #continue
        idx = idx + 10
            
    Summary().log(dict)
    helper = GENERIC_HELPERS()
    helper.logSummry()
    Logme()('completed successfully', 'FINISH')
