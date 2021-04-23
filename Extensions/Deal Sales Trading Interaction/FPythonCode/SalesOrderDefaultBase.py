import acm
from DealPackageDevKit import CompositeAttributeDefinition, DealPackageUserException
from DealPackageUtil import SalesTradingInteraction
from SalesTradingCustomizations import DefaultSalesPortfolio, SuggestDefaultCustomerRequestName, OrderBookCreation, NonConfirmedTradeStatuses

class SalesOrderDefaultBase(CompositeAttributeDefinition):
    def OnInit(self, **kwargs):
        self._instrumentMethod = kwargs['instrumentMethod']
        self._orderHandlerMethod = kwargs['orderHandlerMethod']
        self._dealPackageMethod = kwargs['dealPackageMethod']

    def Instrument(self):
        return self.GetMethod(self._instrumentMethod)()
        
    def OrderHandler(self):
        return self.GetMethod(self._orderHandlerMethod)().OrderHandler()
        
    def DealPackage(self):
        return self.GetMethod(self._dealPackageMethod)()
        
    def DefaultSalesPortfolio(self, *args):
        return DefaultSalesPortfolio() 
     
    def OnCreateSalesOrder(self, componentName, customDict):
        try:
            salesObject = customDict.At('salesObject')
            tabTradeCreationSetting = customDict.At('tradeCreationSetting')
            objectToQuote = customDict.At('objectsToQuote').At(componentName)
            customAttributes = customDict.At('customAttributes')
        except Exception as e:
            print(('OnCreateSalesOrder failed', e))

    def SuggestCustomerRequestName(self, client):
        return SuggestDefaultCustomerRequestName(client)

    def CheckInstrumentIsValidToSendOrder(self, buyOrSell, quantity, client, portfolio):
        if self.Instrument().IsExpired():
            raise DealPackageUserException('Instrument is Expired')
        if not quantity:
            raise DealPackageUserException('Cannot send order with zero quantity')
        if not OrderBookCreation.IsPriceBased(self.Instrument()):
            for trade in self.Instrument().Originator().Trades():
                if trade.Status() not in NonConfirmedTradeStatuses():
                    raise DealPackageUserException('There are confirmed trades in this Instrument')
        
        return True
