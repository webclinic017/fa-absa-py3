import acm
from DealPackageDevKit import DealPackageUserException, CompositeAttributeDefinition
from TradeCreationUtil import TABTradeCreationSetting
from DealPackageUtil import SalesTradingInfo

from SalesTradingCustomizations import RFQTimerDefaultSettings, DefaultSalesPortfolio, SuggestDefaultCustomerRequestName, OrderBookCreation, NonConfirmedTradeStatuses

class QuoteRequestDefaultBase(CompositeAttributeDefinition):
    def OnInit(self, **kwargs):
        self._instrument = kwargs['instrumentMethod']
        self._trade = kwargs['tradeMethod']
        self._dealPackage = kwargs['dealPackageMethod']
        self._originalTradeId = kwargs['originalTradeIdMethod']
        self._customerQuoteRequestInfo = kwargs['customerQuoteRequestInfoMethod']
        self._tradingQuoteRequestInfo = kwargs['tradingQuoteRequestInfoMethod']
        
    def Instrument(self):
        return self.GetMethod(self._instrument)()

    def Trade(self):
        return self.GetMethod(self._trade)()
        
    def OriginalTrade(self):
        trade = None
        tradeId = self.GetMethod(self._originalTradeId)()
        if tradeId:
            trade = acm.FTrade[tradeId]
        return trade
        
    def DealPackage(self):
        return self.GetMethod(self._dealPackage)()
        
    def CustomerQuoteRequestInfo(self):
        return self.GetMethod(self._customerQuoteRequestInfo)()
        
    def TradingQuoteRequestInfo(self):
        return self.GetMethod(self._tradingQuoteRequestInfo)()
    
    def CustomInitiateFromQuoteRequestInfos(self):
        pass
    
    def DefaultSalesPortfolio(self, *args):
        return DefaultSalesPortfolio()

    def DefaultTrader(self, *args):
        return None
        
    def OnCreateQuoteRequest(self, quoteRequest, componentName, customDict):
        try:
            salesObject = customDict.At('salesObject')
            tabTradeCreationSetting = customDict.At('tradeCreationSetting')
            objectsToQuote = customDict.At('objectsToQuote')
            objectToQuote = objectsToQuote.At(componentName)
            customAttributes = customDict.At('customAttributes')
        except Exception as e:
            print(('OnCreateQuoteRequest failed', e))

    def CustomerPriceAsFirmOrStream(self, *args):
        return 1
        
    def QuoteRequestCounterparties(self, *args):
        return ['FCS']       
        
    def OnAcceptQuote(self, order, quoteRequest, *args):
        pass  
        
    def OnSendQuoteRequestAnswerToClient(self, quoteRequestInfo, quoteRequestAnswer):
        pass
        
    def SuggestCustomerRequestName(self, client): 
        return SuggestDefaultCustomerRequestName(client)
            
    def NominalIncrements(self, *args):
        return [('+10', 10000000), ('+20', 20000000), ('+50', 50000000), ('-10 ', -10000000), ('-20 ', -20000000), ('-50 ', -50000000)]
    
    def CheckInstrumentIsValidToSendQuoteRequest(self, requestedNominal, client, *args):
        if self.Instrument().IsExpired():
            raise DealPackageUserException('Instrument is Expired')
        if not OrderBookCreation.IsPriceBased(self.Instrument()):
            for trade in self.Instrument().Originator().Trades():
                if trade.Status() not in NonConfirmedTradeStatuses():
                    raise DealPackageUserException('There are confirmed trades in this Instrument')

    def CopyProposalText(self, summaryDict):
        summary = ''
        newLine = '\n'
        summary += 'Summary of ' + summaryDict.At('status') + ' ' + summaryDict.At('direction') + ' Quote Request:'
        if self.DealPackage() and not self.DealPackage().IsTransient():
            summary += newLine + 'Instrument Package:\t' + self.DealPackage().InstrumentPackage().Name()
        else:
            summary += newLine + 'Instrument:\t\t' + self.Instrument().Name()
        summary += newLine + 'Client:\t\t' + summaryDict.At('client')
        summary += newLine + 'Amount:\t\t' + summaryDict.At('amount')
        summary += newLine + 'Currency:\t\t' + summaryDict.At('currency')
        summary += newLine + 'All-in Price:\t\t' + summaryDict.At('allInPrice')
        return summary

    def SummaryText(self, summaryDict):
        newLine = '\n'
        summary = self.CopyProposalText(summaryDict)
        summary += newLine + 'Sales Spread:\t' + summaryDict.At('salesSpread')
        summary += newLine + 'Trader Price:\t\t' + summaryDict.At('traderPrice')
        return summary
            


