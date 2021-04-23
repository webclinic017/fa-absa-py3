import acm
from datetime import datetime, date
from xml.etree.ElementTree import ElementTree, Element, tostring, fromstring
import DDM_ATS_HELPER as helper
import DDM_ATS_PARAMS as params
from DDM_TRADE_INFO import DDM_TRADE_INFO
from DDM_TRADE_BUILDER import DDM_TRADE_BUILDER
from DDM_INSTRUMENT_BUILDER import DDM_INSTRUMENT_BUILDER
from DDM_LEG_BUILDER import DDM_LEG_BUILDER
from DDM_SALES_CREDITS_BUILDER import DDM_SALES_CREDITS_BUILDER
from DDM_MONEY_FLOW_BUILDER import DDM_MONEY_FLOW_BUILDER



class DDM_TRADE_WORKER():
    
    #locals
    tradeBuilder = None
    instrumentBuilder = None
    legBuilder = None
    
    salesCreditsBuilder = None
    moneyFlowBuilder = None
    
    #Constructor
    def __init__(self):
        self.tradeBuilder = DDM_TRADE_BUILDER()
        self.instrumentBuilder = DDM_INSTRUMENT_BUILDER()
        self.legBuilder = DDM_LEG_BUILDER()
        self.salesCreditsBuilder = DDM_SALES_CREDITS_BUILDER()
        self.moneyFlowBuilder = DDM_MONEY_FLOW_BUILDER()
        
            
    def buildTrade(self, reportDate, trade, tradeLegReport):
        try:
            
            #First create the trade info
            tradeInfo = DDM_TRADE_INFO(reportDate, trade)
            
            #Fetch the trade element
            (tradeElement, staticHash) = self.tradeBuilder.createElement(trade)
            tradeInfo.versionHash = staticHash
            
            #Fetch the instrument element
            if bool(params.includeInstrument):
                tradeInfo.instrumentCount=1
                instrument = trade.Instrument()
                instrumentElement = self.instrumentBuilder.createElement(instrument)
                
                #Fetch the instrument legs
                if bool(params.includeInstrumentLegs):
                    legsElement = Element('legs')
                    
                    tradeInfo.legCount = len(tradeInfo.trade.Instrument().Legs())
                    
                    #Single legged instrument
                    if tradeInfo.legCount==1:
                        leg = tradeInfo.trade.Instrument().Legs()[0]
                        if leg:
                            legElement = self.legBuilder.createElementByLeg(trade, leg)
                            legsElement.append(legElement)
                    #Multilegged instrument                     
                    else:
                        #gets a collection of the leg reports for the trade
                        legsCollestion = helper.getLegsCollection(tradeLegReport)
                        #get the actual FLeg objects
                        legs = tradeInfo.trade.Instrument().Legs()
                        for leg in legs:
                            #fetch the leg report for the leg
                            legReport = None
                            if(legsCollestion):
                                legReport = legsCollestion[leg.Oid()]
                                
                            #Build the leg element
                            legElement = self.legBuilder.createElementByLegReport(trade, leg, legReport)
                            legsElement.append(legElement)
                            
                            
                    #add the legs element to the instrument
                    instrumentElement.append(legsElement)
                    
                #Fetch the underlying instruments
                if bool(params.includeUnderlyingInstruments):
                    underlyingInstrumentsElement = Element('underlyingInstruments')
                    #Combination
                    if tradeInfo.trade.Instrument().InsType() == 'Combination':
                        combination = acm.FCombination[instrument.Oid()]
                        for underlyingInstrument in combination.Instruments():
                            tradeInfo.instrumentCount=tradeInfo.instrumentCount + 1
                            underlyingInstrumentElement = self.instrumentBuilder.createElement(underlyingInstrument)
                            underlyingInstrumentsElement.append(underlyingInstrumentElement)
                    #Normal underlying
                    else:
                        underlyingInstrument = instrument.Underlying()
                        while underlyingInstrument:
                            tradeInfo.instrumentCount=tradeInfo.instrumentCount + 1
                            underlyingInstrumentElement = self.instrumentBuilder.createElement(underlyingInstrument)
                            underlyingInstrumentsElement.append(underlyingInstrumentElement)
                            underlyingInstrument = underlyingInstrument.Underlying()
                    
                    #Add the underlyingInstruments element to the instrument element
                    instrumentElement.append(underlyingInstrumentsElement)
                
                
                #Append the instrument element to the trade element
                tradeElement.append(instrumentElement)
                
            #Fetch the sales credits
            if bool(params.includeSalesCredits):
                (salesCreditsElement, salesCreditCounter) = self.salesCreditsBuilder.createElement(trade)
                tradeInfo.salesCreditCount = salesCreditCounter
                tradeElement.append(salesCreditsElement)
            
            #Fetch the money flows
            if bool(params.includeMoneyFlows):
                moneyFlowsElement = Element('moneyFlows')
                for moneyFlow in trade.MoneyFlows(None, None):
                
                    #By default include all money flows
                    includeMoneyFlow = True
                    
                    #Get the money flow if a cashflow and set the next cashflow date 
                    tradeInfo.nextCFDate = None
                    if moneyFlow.SourceObject().IsKindOf('FCashFlow'):
                        cashFlowDate = datetime.strptime(moneyFlow.PayDate(), '%Y-%m-%d')
                        #check if historical casflows should be included
                        if not bool(params.includeHistoricalCashFlows) and cashFlowDate < tradeInfo.reportDate:
                            includeMoneyFlow = False
                        #set the next cashflow date
                        if not tradeInfo.nextCFDate and cashFlowDate >= tradeInfo.reportDate:
                            tradeInfo.nextCFDate = cashFlowDate.strftime('%Y-%m-%d')
                        elif cashFlowDate == tradeInfo.reportDate:
                            tradeInfo.nextCFDate = cashFlowDate.strftime('%Y-%m-%d')
                        elif cashFlowDate >= tradeInfo.reportDate and cashFlowDate < tradeInfo.nextCFDate:
                            tradeInfo.nextCFDate = cashFlowDate.strftime('%Y-%m-%d')
                    
                    #Build the money flow element
                    if bool(includeMoneyFlow):
                        tradeInfo.moneyFlowCount = tradeInfo.moneyFlowCount + 1
                        moneyFlowElement = self.moneyFlowBuilder.createElement(moneyFlow)
                        moneyFlowsElement.append(moneyFlowElement)
                        
                        #Count the type of money flow
                        moneyFlowPayDate = datetime.strptime(moneyFlow.PayDate(), '%Y-%m-%d')
                        if moneyFlowPayDate == tradeInfo.reportDate:
                            tradeInfo.todayMoneyFlowCount = tradeInfo.todayMoneyFlowCount + 1
                        #Historical
                        elif moneyFlowPayDate < tradeInfo.reportDate:
                            tradeInfo.historicalMoneyFlowCount = tradeInfo.historicalMoneyFlowCount + 1
                        #Future
                        elif moneyFlowPayDate > tradeInfo.reportDate:
                            tradeInfo.futureMoneyFlowCount = tradeInfo.futureMoneyFlowCount + 1
                
                
                
                #Append the money flows element to the trade element
                tradeElement.append(moneyFlowsElement)
            
            #return the trade info and the trade element
            return tradeInfo, tradeElement
        except Exception as error:
            raise Exception('Could not get the trade element. %s' % str(error))


    
'''
#Unit test
trade = acm.FTrade[20906385]
reportdate = datetime.strptime('2013-12-01', '%Y-%m-%d')
tradeWorker = DDM_TRADE_WORKER()
tradeInfo, tradeElement = tradeWorker.buildTrade(reportdate,trade)
#print tostring(tradeInfo.createElement())
print tostring(tradeElement)
'''
