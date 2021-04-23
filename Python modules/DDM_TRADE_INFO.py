import acm
from datetime import datetime, date
from xml.etree.ElementTree import ElementTree, Element, tostring, fromstring
import DDM_ATS_HELPER as helper
import DDM_ATS_PARAMS as params

class DDM_TRADE_INFO():
    
    #properties
    trade = None
    reportDate=None
    
    #event information
    eventDateTime = None
    eventType = None
    eventSource = None
    
    #Intraday specific
    intradayEventId=0
    
    #Request specific
    requestId=0
    requestDateTime=None
    requestSource=None
    requestEventType =None
    requestType = None
    scopeNumber = None
    scopeName = None
    batchNumber=None
    batchName=None
    
    #Trade specific
    isEODVersion = None
    tradeNumber = None
    tradeDomain = None
    versionHash = None
    sourceType1 = None
    sourceType2 = None
    sourceType3 = None
    productMainType = None
    productSubType = None
    bookId = None
    nextCFDate=None
    sourceCounterpartyName=None
    sourceCounterpartyNumber=None
    sourceCounterpartySystem=None
    
    #counters
    instrumentCount=0
    legCount=0
    moneyFlowCount=0
    historicalMoneyFlowCount=0
    todayMoneyFlowCount=0
    futureMoneyFlowCount=0
    salesCreditCount=0
    
    #Constructor
    def __init__(self, reportDate, trade):
        self.reportDate = reportDate
        
        self.trade = trade
        self.tradeNumber = trade.Oid()
        self.tradeDomain = params.sourceSystem
        #Populate source type 1 with the instrument type and type2 with the underlying instrument type if any
        if trade.Instrument():
            self.sourceType1 = trade.Instrument().InsType()
            if trade.Instrument().Underlying():
                self.sourceType2 = trade.Instrument().Underlying().InsType()
        
        #Populate the source type 3 with the trade process
        self.sourceType3 = trade.TradeProcess()
        
        #fetch the product mapping
        (self.productMainType, self.productSubType) = helper.getProductMapping(self.sourceType1, self.sourceType2, self.sourceType3)
    
        #Get the trade's portfolio name as book name
        if trade.Portfolio():
            self.bookId = trade.Portfolio().Name()
        else:
            self.bookId  = ''
            
        #fetch the base counterparty for lookup purposes - hack for CFR Midas Dual Key Trades - ugly!!
        if trade.Counterparty():
            if trade.Instrument().InsType()=='Curr' and trade.Counterparty().Name()=='MIDAS DUAL KEY':
                self.sourceCounterpartyName = trade.add_info('Source Ctpy Name')
                self.sourceCounterpartyNumber = trade.add_info('Source Ctpy Id')
                self.sourceCounterpartySystem = trade.add_info('Source System')
                
            else:
                self.sourceCounterpartyName = trade.Counterparty().Name()
                self.sourceCounterpartyNumber = trade.Counterparty().Oid()
                self.sourceCounterpartySystem = params.sourceSystem 
    
    #Create a trade info xml element
    def createElement(self):
        try:
            #Create the return element
            element = Element('tradeInfo')

            #reportDate  
            xmlReportDateStr = self.reportDate.strftime("%Y-%m-%d")  
            helper.AddXmlChildElement(element, 'reportDate', str(xmlReportDateStr))

            #eventDateTime    
            eventDateTimeString = helper.dateFromDateTimeString(self.eventDateTime)
            helper.AddXmlChildElement(element, 'eventDateTime', str(eventDateTimeString))
            
            #eventType    
            helper.AddXmlChildElement(element, 'eventType', str(self.eventType))
            
            #eventSource    
            helper.AddXmlChildElement(element, 'eventSource', str(self.eventSource))
            
            #intradayEventId    
            helper.AddXmlChildElement(element, 'intradayEventId', str(self.intradayEventId))
            
            #requestId    
            helper.AddXmlChildElement(element, 'requestId', str(self.requestId))
            
            #requestDateTime    
            requestDateTimeString = helper.dateFromDateTimeString(self.requestDateTime)
            helper.AddXmlChildElement(element, 'requestDateTime', str(requestDateTimeString))
            
            #requestSource    
            helper.AddXmlChildElement(element, 'requestSource', str(self.requestSource))
            
            #requestEventType    
            helper.AddXmlChildElement(element, 'requestEventType', str(self.requestEventType))
            
            #requestType    
            helper.AddXmlChildElement(element, 'requestType', str(self.requestType))
            
            #scopeNumber    
            helper.AddXmlChildElement(element, 'scopeNumber', str(self.scopeNumber))
            
            #scopeName    
            helper.AddXmlChildElement(element, 'scopeName', str(self.scopeName))
            
            #batchNumber    
            helper.AddXmlChildElement(element, 'batchNumber', str(self.batchNumber))
            
            #batchName    
            helper.AddXmlChildElement(element, 'batchName', str(self.batchName))
            
            #isEODVersion   
            if self.isEODVersion==True:
                helper.AddXmlChildElement(element, 'isEODVersion', 'true')
            else:
                helper.AddXmlChildElement(element, 'isEODVersion', 'false')
            
            #tradeNumber    
            helper.AddXmlChildElement(element, 'tradeNumber', str(self.tradeNumber))
            
            #tradeDomain    
            helper.AddXmlChildElement(element, 'tradeDomain', str(self.tradeDomain))
            
            #versionHash    
            helper.AddXmlChildElement(element, 'versionHash', str(self.versionHash))
            
            #sourceType1    
            helper.AddXmlChildElement(element, 'sourceType1', str(self.sourceType1))
            
            #sourceType2    
            helper.AddXmlChildElement(element, 'sourceType2', str(self.sourceType2))
            
            #sourceType3    
            helper.AddXmlChildElement(element, 'sourceType3', str(self.sourceType3))
             
            #productMainType    
            helper.AddXmlChildElement(element, 'productMainType', str(self.productMainType))
            
            #productSubType    
            helper.AddXmlChildElement(element, 'productSubType', str(self.productSubType))
            
            #bookId    
            helper.AddXmlChildElement(element, 'bookId', str(self.bookId))
            
            #sourceCounterpartyName    
            helper.AddXmlChildElement(element, 'sourceCounterpartyName', str(self.sourceCounterpartyName))
            
            #sourceCounterpartyNumber    
            helper.AddXmlChildElement(element, 'sourceCounterpartyNumber', str(self.sourceCounterpartyNumber))
            
            #sourceCounterpartySystem    
            helper.AddXmlChildElement(element, 'sourceCounterpartySystem', str(self.sourceCounterpartySystem))
            
            #nextCFDate    
            helper.AddXmlChildElement(element, 'nextCFDate', str(self.nextCFDate))
            
            #instrumentCount    
            helper.AddXmlChildElement(element, 'instrumentCount', str(self.instrumentCount))
            
            #legCount    
            helper.AddXmlChildElement(element, 'legCount', str(self.legCount))
            
            #salesCreditCount    
            helper.AddXmlChildElement(element, 'salesCreditCount', str(self.salesCreditCount))
            
            #moneyFlowCount    
            helper.AddXmlChildElement(element, 'moneyFlowCount', str(self.moneyFlowCount))
            
            #historicalMoneyFlowCount    
            helper.AddXmlChildElement(element, 'historicalMoneyFlowCount', str(self.historicalMoneyFlowCount))
            
            #todayMoneyFlowCount    
            helper.AddXmlChildElement(element, 'todayMoneyFlowCount', str(self.todayMoneyFlowCount))
            
            #futureMoneyFlowCount    
            helper.AddXmlChildElement(element, 'futureMoneyFlowCount', str(self.futureMoneyFlowCount))
            
            #Return the XML element
            return element
        except Exception, error:
            raise Exception('Could not create the trade info element. %s' % str(error))
    
    
    
'''
#Unit test
reportdate = datetime.strptime('2013-12-01', '%Y-%m-%d')
trade = acm.FTrade[18537101]
tradeInfo = DDM_TRADE_INFO(reportdate,trade)
tradeInfoElement =tradeInfo.createElement()
print tostring(tradeInfoElement)
'''
