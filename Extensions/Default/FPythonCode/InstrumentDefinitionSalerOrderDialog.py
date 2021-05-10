
import acm
from FUxCore import MenuItem


class InstrumentDefinitionSalesOrderBase(MenuItem):
    def __init__(self, eii):
        self._insDefApp = eii
        self._moduleInContext = False
        self.ValidateModuleInContext()
                
    def ValidateModuleInContext(self):
        try:
            import SalesOrderDialog
            self._moduleInContext = True
        except Exception as e:
            pass
    
    def OriginalInstrument(self):
        return self._insDefApp.OriginalInstrument()
        
    def OriginalTrade(self):
        return self._insDefApp.OriginalTrade()
    
    def QuoteRequestObject(self):
        trade = self.OriginalTrade()
        instrument = self.OriginalInstrument()
        return trade if trade else instrument
        
    def Shell(self):
        return self._insDefApp.Shell()
        
    def Applicable(self):
        return self._moduleInContext
    
    def Enabled(self):
        return False
    
    def Invoke(self, eii):
        raise('Invoke not implemented') 
        
        
class InstrumentDefinitionSalesOrderDialog(InstrumentDefinitionSalesOrderBase):
    def Invoke(self, eii):
        import SalesOrderDialog
        SalesOrderDialog.StartSalesOrderDialog(self.Shell(), self.QuoteRequestObject())
        
    def Enabled(self):
        return True if self.QuoteRequestObject() else False
 
def OpenSalesOrderDialog(eii):
    return InstrumentDefinitionSalesOrderDialog(eii)



class InstrumentDefinitionSalesOrderHistoryDialog(InstrumentDefinitionSalesOrderBase):
    def Invoke(self, eii):
        from SalesOrderHistoryViewer import OpenSalesOrderHistoryViewerFromTrade
        OpenSalesOrderHistoryViewerFromTrade(self.OriginalTrade(), self.Shell())
        
    def Enabled(self):
        from SalesOrderHistoryViewer import GetSalesOrderId
        trade = self.OriginalTrade()
        return bool(trade and GetSalesOrderId(trade))
        
def OpenSalesOrderHistoryViewerDialog(eii):
    return InstrumentDefinitionSalesOrderHistoryDialog(eii)
