import acm
from DealPackageDevKit import DealPackageUserException, CompositeAttributeDefinition
         
def ValOrNone(obj):
    if hasattr(obj, 'StorageId'):
        obj = obj.StorageId()
    return obj
    
class QuoteRequestReplyDefaultBase(CompositeAttributeDefinition):
    def OnInit(self, **kwargs):
        self._instrumentMethod = kwargs['instrumentMethod']
        self._originalTradeMethod = kwargs['originalTradeMethodName']
        self._quoteControllerMethod = kwargs['quoteControllerMethod']
        self._dealPackageMethod = kwargs['dealPackageMethod']
        
    def Instrument(self):
        return self.GetMethod(self._instrumentMethod)()
        
    def OriginalTrade(self):
        return self.GetMethod(self._originalTradeMethod)()
        
    def DealPackage(self):
        return self.GetMethod(self._dealPackageMethod)()
        
    def QuoteController(self):
        return self.GetMethod(self._quoteControllerMethod)()

    def TopPanelActions(self):
        return []
