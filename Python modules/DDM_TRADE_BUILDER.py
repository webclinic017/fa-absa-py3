import acm
from xml.etree.ElementTree import ElementTree, Element, tostring, fromstring
import DDM_ATS_HELPER as helper
import DDM_ATS_PARAMS as params

class DDM_TRADE_BUILDER():
    
    #Locals
    tradeCalcSpace = None
    tradePortfolioCalcSpace = None
    tradeSheetColumns = None
    tradePortfolioSheetColumns = None
    
    #Constructor
    def __init__(self):
        if params.includeDynamicAttributes:
            #Create the calculation space if dynamic attributes is required
            self.tradeCalcSpace = acm.FCalculationSpace('FTradeSheet')
            self.tradePortfolioCalcSpace = acm.FCalculationSpace('FPortfolioSheet')
            
            #Load the trade sheet columns
            tradeSheet = helper.getWorkbookSheet(params.dynamicAttributesWorkbookName, params.tradeSheetName)
            self.tradeSheetColumns = helper.getSheetColumns(tradeSheet)
            
            #Load the trade portfolio sheet columns
            tradePortfolioSheet = helper.getWorkbookSheet(params.dynamicAttributesWorkbookName, params.tradePortfolioSheetName)
            self.tradePortfolioSheetColumns = helper.getSheetColumns(tradePortfolioSheet)
 
    
    #Create a trade xml element
    def createElement(self, trade):
        try:
            #Create the return element
            staticHash = ''
            tradeElement = Element('trade')

            #Fetch the static atributes
            if params.includeStaticAttributes:
                staticAttributes = self.getStaticAttributes(trade)
                staticHash = helper.calcSHA512(str(staticAttributes))
                helper.addAttributesToElement(tradeElement, staticAttributes)
            
            #Fetch the dynamic attributes
            if params.includeDynamicAttributes:
                #get the trade sheet attributes
                tradeSheetAttributes = helper.getSheetColumnValues(self.tradeCalcSpace, self.tradeSheetColumns, trade)
                helper.addAttributesToElement(tradeElement, tradeSheetAttributes)
                
                 #get the trade sheet attributes
                tradePortfolioSheetAttributes = helper.getSheetColumnValues(self.tradePortfolioCalcSpace, self.tradePortfolioSheetColumns, trade)
                helper.addAttributesToElement(tradeElement, tradePortfolioSheetAttributes)
                
            
            #Return the XML element
            return tradeElement, staticHash
        except Exception, error:
            raise Exception('Could not create the trade element. %s' % str(error))
    
    def getStaticAttributes(self, trade):
        try:
            attributes = acm.FDictionary()
            
            #acquireDay
            attributes['acquireDay'] = trade.AcquireDay()
            
            #acquirer
            if trade.Acquirer():
                attributes['acquirerName'] = trade.Acquirer().Name()
                attributes['acquirerNumber'] = trade.Acquirer().Oid()
            
            #buySell
            attributes['buySell'] = trade.BoughtAsString()
            
            #broker
            try:
                if trade.Broker():
                    attributes['brokerName'] = trade.Broker().Name()
                    attributes['brokerNumber'] = trade.Broker().Oid()
            except Exception, error:
                #print str(error)
                #attributes['brokerName']
                attributes['brokerName'] = str(error)
                attributes['brokerNumber'] = '0'
                
            #connectedTrade 
            attributes['connectedTradeNumber'] = trade.ConnectedTrdnbr()
            
            #counterparty
            if trade.Counterparty():
                attributes['counterpartyNumber'] = trade.Counterparty().Oid()
                attributes['counterpartyName'] = trade.Counterparty().Name()
            
            #counterPortfolio
            if trade.CounterPortfolio():
                attributes['counterPortfolioName'] = trade.CounterPortfolio().Name()
            
            #createTime
            attributes['createTime'] = helper.isoDateTimeFromInt(trade.CreateTime())
            
            #createUser
            if trade.CreateUser():
                attributes['createUserName'] = trade.CreateUser().Name()
                attributes['createUserNumber'] = trade.CreateUser().Oid()
            
            #currency
            if trade.Currency():
                attributes['currencyName'] = trade.Currency().Name()
                attributes['currencyNumber'] = trade.Currency().Oid()
            
            
            #executionTime
            attributes['executionTime'] = helper.isoDateTimeFromInt(trade.ExecutionTime())
            
            #maturityDate
            attributes['maturityDate'] = trade.maturity_date()
            
            #mirrorTrade
            if trade.MirrorTrade():
                mirrorTradeNumber=''
                if trade.MirrorTrade().Oid() == trade.Oid():
                    mirrorTrades = acm.FTrade.Select('mirrorTrade=%i and oid<> %i' % (trade.Oid(), trade.Oid()))
                    if mirrorTrades:
                        if(len(mirrorTrades)>0):
                            mirrorTradeNumber = mirrorTrades[0].Oid()
                else:
                    mirrorTradeNumber = trade.MirrorTrade().Oid()
                attributes['mirrorTradeNumber'] = mirrorTradeNumber
            

            #optionalKey    
            attributes['optionalKey'] = trade.OptionalKey()
            
            #portfolio  
            if trade.Portfolio():
                attributes['portfolioName'] = trade.Portfolio().Name()
                attributes['portfolioNumber'] = trade.Portfolio().Oid()
            
            #premium  
            attributes['premium'] = helper.formatNumber(trade.Premium())
            
            
            #quantity
            attributes['quantity'] = helper.formatNumber(trade.Quantity())
            
            #quotation
            if trade.Quotation():
                attributes['quotationType'] = trade.Quotation().QuotationType()
                attributes['quotationNumber'] = trade.Quotation().Oid()
                attributes['quotationName'] = trade.Quotation().Name()
                attributes['quotationFactor'] = trade.Quotation().QuotationFactor()
                
            #price    
            attributes['price'] = helper.formatNumber(trade.Price())
                
            #status 
            attributes['status'] = trade.Status()
            
            #tradeNumber
            attributes['tradeNumber'] = trade.Oid()
            
            #tradeProcess
            attributes['tradeProcess'] = helper.formatNumber(trade.TradeProcess())
            
            #tradeTime.
            attributes['tradeTime'] = helper.dateFromDateTimeString(trade.TradeTime())
            
            #trader
            if trade.Trader():
                attributes['traderName'] = trade.Trader().Name()
                attributes['traderNumber'] = trade.Trader().Oid()
                
            #type
            attributes['type'] = trade.Type()
            
            #valueDay
            attributes['valueDay'] = trade.ValueDay()
            
            #volatilityStrike
            attributes['volatilityStrike'] =helper.formatNumber(trade.VolatilityStrike())
            
            #updateTime
            attributes['updateTime'] =helper.isoDateTimeFromInt(trade.UpdateTime())

            #updateUser
            if trade.UpdateUser():  
                attributes['updateUserName'] = trade.UpdateUser().Name()
                attributes['updateUserNumber'] = trade.UpdateUser().Oid()
            
            #yourRef
            attributes['yourRef'] = trade.YourRef()
            
            return attributes
            
                  
        except Exception, error:
            raise Exception('Could not get the trade static attributes. %s' % str(error))
        
'''

#Unit test
trade = acm.FTrade[12842617]
tradeElementBuilder = DDM_TRADE_BUILDER()
tradeElement = tradeElementBuilder.createElement(trade)
print tostring(tradeElement)
'''
