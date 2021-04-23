
import acm
from FBDPCurrentContext import Logme
from FBDPCurrentContext import Summary
from collections import defaultdict
import FBDPGui
reload(FBDPGui)
import AGGREGATION_CASH_POSTING_HELPER as helper

delete_options = {'Trade Dependencies Only' : 'Trade',
                   'Instrument Dependencies Only' : 'Instrument',
                   'Trade and Instrument Dependancies' : 'Both'
                    }

ael_variables = FBDPGui.LogVariables(
                    ['query_folder', 'Query Folder', acm.FStoredASQLQuery, acm.FStoredASQLQuery, None, 1, 1, 'Query folder containing the aggregate trades on which processing should happen.', None, 1],
                    ['deleteHighestLevel', 'Delete Highest Level Trade', 'bool', [0, 1], 0, 0, 0, 'If the selected trades need to be deleted.', None, 1],
                    ['deleteOption', 'Delete Option', 'string', delete_options.keys(), 'Trade and Instrument Dependancies', 1, 0, 'The aggregated trades/instruments from the selected trades will be affected.', None, 1]
                )

def ael_main(dict):
    scriptName = __name__
    queryFolder = dict['query_folder'][0]
    trades_per_grouper = defaultdict(list)
    
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
    
    Logme()('DEBUG: Building and applying grouper.', 'DEBUG')
    for trade in aggregateTrades:
        if trade.Portfolio():
            portf = trade.Portfolio().Name()
        else:
            portf = None
        if trade.Counterparty():
            cp = trade.Counterparty().Name()
        else:
            cp = None
        insOverride = trade.AdditionalInfo().InsOverride()
        
        trades_per_grouper[(portf, cp, insOverride)].append(trade)
        
    nbrOfNodes = len(trades_per_grouper)
    Logme()('INFO: Number of grouper nodes to process: %i' %nbrOfNodes, 'INFO')
    
    actionSelected = dict['deleteOption']
    counter = 0
    helper.resetSummaryTracker()
    for portf, cp, insOverride in trades_per_grouper:
        counter = counter + 1
        Logme()('*' * 150, 'INFO')
        Logme()('INFO: Portfolio: %s       Counterparty: %s      Ins Override: %s     Progress: %i of %i' %(portf, cp, insOverride, counter, nbrOfNodes), 'INFO')
        Logme()('*' * 150, 'INFO')
    
        trades = trades_per_grouper[(portf, cp, insOverride)]
        dependencies = helper.getAggregationDependencyTree(trades, 'Trade')
        
        dependencyLevels = dependencies.keys()
        dependencyLevels.reverse()
        totalLevels = len(dependencyLevels)
        
        for dependencyLevel in dependencyLevels:
            Logme()('Deleting %s from a total of %i levels' %(dependencyLevel, totalLevels))
            if dependencyLevel == 'Level_0':
                helper.deleteDependencies(dependencies[dependencyLevel], 0)
            else:
                helper.deleteDependencies(dependencies[dependencyLevel], 1)
                    
    Summary().log(dict)
    helper.writeSummaryInst()
    Logme()('completed successfully', 'FINISH')
