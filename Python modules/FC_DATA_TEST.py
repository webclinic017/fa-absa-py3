import FC_DATA_HELPER
from FC_DATA_TRD_BUILDER_OPTIONS import FC_DATA_TRD_BUILDER_OPTIONS as  fcDataTradeBuilderOptions
import FC_UTILS
from FC_UTILS import FC_UTILS as UTILS
from FC_MESSAGE_OBJECT_REQUEST import FC_MESSAGE_OBJECT_REQUEST as fcMessageObjectRequest
from datetime import datetime, date
import acm

UTILS.Initialize('FC_RT_01_ATS')
import FC_ENUMERATIONS

#Helper methods
def getPortfolioTrades(portfolioNumber, portfolioName):
    try:
        #first fetch the porfolio
        portfolio = None
        try:
            if int(portfolioNumber)!= 0:
                portfolio = acm.FPhysicalPortfolio.Select01('oid=%i' % int(portfolioNumber), 'Portfolio not found')
            else:
                portfolio = acm.FPhysicalPortfolio.Select01("name='%s'" % str(portfolioName), 'Portfolio not found')
        except Exception, error:
            portfolio = None
        
        if not portfolio:
            return None
        
        portfolioTradeQuery="portfolio=%s and status<>'Void' and status<>'Simulated'" % str(portfolio.Oid())
        
        return acm.FTrade.Select(portfolioTradeQuery) 
    except Exception, error:
        raise Exception('Could not get the portfolio trades. %s' % str(error))


def getTradeIndexBatches(batchSize, tradeCount):
    
    try:
        batches = acm.FList()  
        if tradeCount==0:
            batches.Add((0, 0))
        elif tradeCount <= batchSize:
            batches.Add((0, tradeCount-1))
        else:
            i = 1
            startIndex=0
            endIndex = (i * batchSize) - 1
            remainder=0
            while endIndex <= tradeCount-1:
                batches.Add((startIndex, endIndex))
                startIndex = endIndex + 1
                i = i + 1
                endIndex = (i * batchSize) - 1
                
            
            #Get the remainder
            previousEndIndex = ((i-1) * batchSize) - 1
            remainder = tradeCount - previousEndIndex
            if (remainder) > 0:
                startIndex = previousEndIndex + 1
                endIndex = tradeCount-1
                batches.Add((startIndex, tradeCount-1))
            
        return batches
            
    except Exception, error:
        raise Exception('Could not get the trade index batches. %s' % str(error))
        



def processRequest(requestMessage, batchSize, builderOptions):
    

    #1 Register the request
    requestMessage.requestId = FC_DATA_HELPER.RegisterRequest(requestMessage)

    #3 Send the request message to the Request Type ATS
    #Fetch all the trades
    portfolioTrades = getPortfolioTrades(requestMessage.scopeNumber, requestMessage.scopeName,)
    tradeCount=0
    if portfolioTrades:
        tradeCount = len(portfolioTrades)
    print'%i trades found' % (int(tradeCount)) 
    #Update the request tracker with the total expected
    FC_DATA_HELPER.SetRequestTrackerStart(requestMessage.requestId, tradeCount )
    print 'request start, send request start response'
        
    #Break into batch sizes, ek process elke batch sommer ook hier
    batches = getTradeIndexBatches(batchSize, tradeCount)
    print '  %i collection batch(s) created (maxBatchSize:%i)' % (len(batches), batchSize)
    batchCounter = 0

    for batch in batches:
        #print batch
        batchCounter = batchCounter+1
        startIndex, endIndex = batch
        batchTradeCount=0
        if tradeCount>0:
            batchTradeCount=(endIndex - startIndex) + 1 
        
        #print portfolioTrades.FromTo(startIndex, endIndex+1)
        #The above can be sent to the collection ats's for processing

        
        #processing batches as if i am the collection ATS (save to DB)
        print 'processing collection batch %i of %i (%i trades)' % (batchCounter, len(batches), batchTradeCount)
        expectedTradeCount = batchTradeCount
        actualTradeCount = 0
        
        #COunting success and errors
        processCount = 0
        errorCount = 0
        tradeIndex = int(startIndex)
        tradeRange = portfolioTrades.FromTo(tradeIndex, endIndex+1)
                
        
        #Or do a whole batch - one liner
        #need a list of tradenumbers
        tradeNumbers=[]
        for trade in tradeRange:
            tradeNumbers.append(trade.Oid())
            
        #(tradeStaticIds, errors) = FC_DATA_HELPER.BuildAndSaveTrades(requestMessage.requestId,requestMessage.reportDate, tradeIndex, tradeNumbers,builderOptions)
        (tradeStaticIds, errors) = FC_DATA_HELPER.BuildAndSaveTrades(requestMessage.requestId, requestMessage.reportDate, tradeIndex, tradeNumbers, builderOptions)
        processCount = len(tradeStaticIds)
        errorCount = len(errors)
        
        print 'trades saved - processed:%s, errors:%s' % (str(processCount), str(errorCount))
        for error in errors:
            print errors[error]
        #Trade batch complete, update the request tracker
        trackerResult = FC_DATA_HELPER.SetRequestTrackerEnd(requestMessage.requestId, processCount, errorCount )
        print 'trackerResult %s' % trackerResult
        #too lazy for bitwise....and dont know how in pythonand too lazy to google :)
        
        if trackerResult=='11':
            print 'collection batch %i done (%i processed, %i errors)' % (batchCounter, processCount, errorCount)
            print 'request processed, all collection batches done, send request complete response'
            print 'batch %s complete processed, all requests processed, send request complete response' % batchId
           
        elif trackerResult=='10':
            print 'collection batch %i done (%i processed, %i errors)' % (batchCounter, processCount, errorCount)
            print 'request processed, all collection batches done, send request complete response'
        elif trackerResult=='00':
            print 'collection batch %i done (%i processed, %i errors)' % (batchCounter, processCount, errorCount)
        else:
            print 'Houston we have a problem!'
        

def createDummyRequestMessage(reportDate, batchId, scopeName, scopeNumber):
    requestMessage = fcMessageObjectRequest()
    requestMessage.ambaTxNbr = 0
    requestMessage.batchId = batchId
    requestMessage.reportDate = reportDate
    requestMessage.isEOD = True
    requestMessage.requestDateTime = FC_UTILS.formatDate('2014-02-25 18:50:25')
    requestMessage.requestEventType = 'EOD_PORTFOLIO_TRADES'
    requestMessage.requestId = 0
    requestMessage.requestSource = 'FC_DATA_TEST'
    requestMessage.requestType = 'PORTFOLIO_TRADES'
    requestMessage.requestUserId = 'mombergh'
    requestMessage.scopeName = scopeName
    requestMessage.scopeNumber = scopeNumber
    requestMessage.topic = 'OfficialEODBatchTrades'
    requestMessage.type = 'Request'
    return requestMessage

#TEST
reportDate = FC_UTILS.formatDate('2014-02-25')
portfolioName1='Kenya Equities'
portfolioNumber1=3591
portfolioName2='ST Islamic Hedges'
portfolioNumber2=1331

batchSize=200 #CONFIG SETTING 
builderoptions = fcDataTradeBuilderOptions()
builderoptions.HistoricalCashflowRange=5
builderoptions.SerializationType=FC_ENUMERATIONS.SerializationType.XML
#builderoptions.SerializationType=FC_ENUMERATIONS.SerializationType.XML_COMPRESSED_BASE64


#Create the batch
batchId = FC_DATA_HELPER.RegisterBatch(reportDate, True, "Test", 1)
print batchId
#print 'batchId %s' % str(batchId)
#Create mock request Messages
requestMessage1 =createDummyRequestMessage(reportDate, batchId, portfolioName1, portfolioNumber1 )
#requestMessage2 =createDummyRequestMessage(reportDate,batchId,portfolioName2,portfolioNumber2 ) 
#Process
processRequest(requestMessage1, batchSize, builderoptions)
#processRequest(requestMessage2,batchSize, builderoptions)
#find a portfolio to play with
#p = acm.FPhysicalPortfolio['JOB1']
#print p.Oid(), len(p.Trades())
#trackerResult=FC_DATA_HELPER.GetRequestTrackerResult(147)
#print trackerResult


#Test Leg Factory
#tradeNumber=18955023

#tradeNumber=3177703
#import FC_DATA_TRD_LEG_FACTORY as fcDataTradeLegFactory
#t = acm.FTrade[tradeNumber]
#legEntities = fcDataTradeLegFactory.CreateFromInstrumentAddress(reportDate, t.Instrument().Oid())
#for leg in legEntities:
#    print leg.DynamicAttributesXml


