import acm
from DealPackageDevKit import CompositeAttributeDefinition, DealPackageUserException
                  
class FillSalesOrderDefaultBase(CompositeAttributeDefinition):
    def OnInit(self, **kwargs):
        self._instrumentMethod = kwargs['instrumentMethod']
        self._orderHandlerMethod = kwargs['orderHandlerMethod']
        self._dealPackageMethod = kwargs['dealPackageMethod']

    def Instrument(self):
        return self.GetMethod(self._instrumentMethod)()
        
    def OrderHandler(self):
        return self.GetMethod(self._orderHandlerMethod)()
        
    def DealPackage(self):
        return self.GetMethod(self._dealPackageMethod)()
        
    def DefaultSalesOrderTradingPortfolioName(self):
        return 'TRADING'
    
