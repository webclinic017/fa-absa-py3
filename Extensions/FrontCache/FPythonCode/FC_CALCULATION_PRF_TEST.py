
import acm, datetime
from FC_UTILS import FC_UTILS as UTILS
UTILS.Initialize('FC_RT_01_ATS')
from FC_CALCULATION_SINGLETON import FC_CALCULATION_SINGLETON

def processTrade(sheetName):
    #print '&'*50
    #print 'Processing sheet %s' %sheetName
    calcSpace = FC_CALCULATION_SINGLETON.Instance().worksheetCalcSpaces[sheetName]
    #calcSpace.Clear()
    cols = FC_CALCULATION_SINGLETON.Instance().worksheetColumns[sheetName]
    
    top_node = calcSpace.InsertItem(trade)
    node = top_node
    node.Expand(True)
    calcSpace.Refresh()
    (calcResults, calcErrors) = FC_CALCULATION_SINGLETON.Instance().calcWorksheetColumnValues(sheetName, node.Item().Trade(), node)
    for result in calcResults.keys():
        print result, '-->', calcResults[result]
    print calcErrors
    
def processTradeInstrument(sheetName):
    #print '&'*50
    #print 'Processing sheet %s' %sheetName
    calcSpace = FC_CALCULATION_SINGLETON.Instance().worksheetCalcSpaces[sheetName]
    #calcSpace.Clear()
    cols = FC_CALCULATION_SINGLETON.Instance().worksheetColumns[sheetName]

    top_node = calcSpace.InsertItem(trade)
    node = top_node
    node.Expand(True)
    calcSpace.Refresh()
    
    #if node.NumberOfChildren():
    #    child_iterator = node.Iterator().FirstChild()
    #    node = child_iterator.Tree()
        
    (calcResults, calcErrors) = FC_CALCULATION_SINGLETON.Instance().calcWorksheetColumnValues(sheetName, node.Item().Trade().Instrument(), node)
    for result in calcResults:
        print result, '-->', calcResults[result]

def processTradeLeg(sheetName):
    #print '&'*50
    #print 'Processing sheet %s' %sheetName
    calcSpace = FC_CALCULATION_SINGLETON.Instance().worksheetCalcSpaces[sheetName]
    #calcSpace.Clear()
    cols = FC_CALCULATION_SINGLETON.Instance().worksheetColumns[sheetName]

    top_node = calcSpace.InsertItem(trade)
    node = top_node
    node.Expand(True)
    calcSpace.Refresh()
    
    if len(trade.Instrument().Legs()) == 1:
        try:
            print str(node.Item().ClassName()) == 'FTradeRow'
            (calcResults, calcErrors) = FC_CALCULATION_SINGLETON.Instance().calcWorksheetColumnValues(sheetName, node.Item().Trade(), node)
            for result in calcResults:
                print result, '-->', calcResults[result]
        except:
            pass
    else:
        if node.NumberOfChildren():
            child_iterator = node.Iterator().FirstChild()
            while child_iterator:
                node = child_iterator.Tree()
                if node.Item():
                    try:
                        (calcResults, calcErrors) = FC_CALCULATION_SINGLETON.Instance().calcWorksheetColumnValues(sheetName, node.Item().Leg(), node)
                        for result in calcResults:
                            print result, '-->', calcResults[result]
                    except:
                        pass
                child_iterator = child_iterator.NextSibling()

def processTradeMoneyFlow(sheetName):
    #print '&'*50
    #print 'Processing sheet %s' %sheetName
    calcSpace = FC_CALCULATION_SINGLETON.Instance().worksheetCalcSpaces[sheetName]
    #calcSpace.Clear()
    cols = FC_CALCULATION_SINGLETON.Instance().worksheetColumns[sheetName]

    top_node = calcSpace.InsertItem(trade)
    node = top_node
    node.Expand(True)
    calcSpace.Refresh()
    
    if node.NumberOfChildren():
        child_iterator = node.Iterator().FirstChild()
        while child_iterator:
            node = child_iterator.Tree()
            (calcResults, calcErrors) = FC_CALCULATION_SINGLETON.Instance().calcWorksheetColumnValues(sheetName, node.Item().MoneyFlow(), node)
            for result in calcResults:
                print result, '-->', calcResults[result]
            child_iterator = child_iterator.NextSibling()


#Initiate Calculations - Load Workbooks, Columns and create Calcualtion Spaces
sheetList = ['FC_TRADE_STATIC', 'FC_TRADE_SCALAR', 'FC_TRADE_INSTRUMENT', 'FC_TRADE_LEG', 'FC_TRADE_MONEYFLOW']
tradeProcessCount = 0
FC_CALCULATION_SINGLETON.Instance()
FC_CALCULATION_SINGLETON.Instance().ApplyGlobalSimulation(None, '2014-06-01', None)
portfolioNames = ['Swap Flow']
for portfolioName in portfolioNames:
    startTime = datetime.datetime.now()
    portfolio = acm.FPhysicalPortfolio[portfolioName]
    #portfolioTrades = portfolio.Trades()
    portfolioTrades = [acm.FTrade[45211832]]
    print 'Starting Portfolio %s at %s.' %(portfolioName, startTime)
    for trade in portfolioTrades:
        
        if tradeProcessCount >= 200:
            print tradeProcessCount
            tradeProcessCount = 0
            for sheet in sheetList:
                FC_CALCULATION_SINGLETON.Instance().worksheetCalcSpaces[sheet].Clear()
        
        tradeProcessCount = tradeProcessCount + 1
        #if trade.Oid() == 32063283:
        #print '-'*50
        #print 'Processing  trade %i' %trade.Oid()
        
        #Trade Process - Trade Scalar
        #sheetName = 'FC_TRADE_STATIC'
        #processTrade(sheetName)
        
        #sheetName = 'FC_TRADE_SCALAR'
        #processTrade(sheetName)
        
        #Instruemnt_Trade Process
        #sheetName = 'FC_TRADE_INSTRUMENT'
        #processTradeInstrument(sheetName)
        
        #Leg_Trade Process
        #sheetName = 'FC_TRADE_LEG'
        #processTradeLeg(sheetName)
        
        #MoneyFlow_Trade Process
        #sheetName = 'FC_TRADE_MONEYFLOW'
        #processTradeMoneyFlow(sheetName)
        
    endTime = datetime.datetime.now()
    print 'Ending Portfolio %s at %s.' %(portfolioName, endTime)
    processTime = endTime - startTime
    combTime = float('%s.%s' %(processTime.seconds, processTime.microseconds))
    print 'Processing Time: %s' %processTime
    length = len(portfolioTrades)
    print 'Trades Processed %i' % length
    print 'Process trades per second %s' %(length / combTime)
    print 'Final Trade Process Count: %i' %tradeProcessCount
FC_CALCULATION_SINGLETON.Instance().RemoveGlobalSimulation()
