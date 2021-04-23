

import acm
from FUxCore import MenuItem


class InstrumentDefinitionQuoteRequestBase(MenuItem):
    def __init__(self, eii):
        self._insDefApp = eii
        self._moduleInContext = False
        self.ValidateModuleInContext()
                
    def ValidateModuleInContext(self):
        try:
            import SalesRFQDialog
            import RFQDefinitionComposite
            self._moduleInContext = True
        except Exception as e:
            #print ('ValidateModuleInContext', e)
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
        
        
class InstrumentDefinitionQuoteRequestDialog(InstrumentDefinitionQuoteRequestBase):
    def Invoke(self, eii):
        import SalesRFQDialog
        SalesRFQDialog.StartSalesRFQDialog(self.Shell(), self.QuoteRequestObject())
        
    def Enabled(self):
        return True if self.QuoteRequestObject() else False
 
def OpenRequestQuoteDialog(eii):
    return InstrumentDefinitionQuoteRequestDialog(eii)


class InstrumentDefinitionQuoteRequestHistoryDialog(InstrumentDefinitionQuoteRequestBase):
    def Invoke(self, eii):
        from QuoteRequestHistoryViewer import OpenQuoteRequestHistoryViewerFromTrade
        OpenQuoteRequestHistoryViewerFromTrade(self.OriginalTrade(), self.Shell())
        
    def Enabled(self):
        from QuoteRequestHistoryViewer import GetQuoteRequestId
        trade = self.OriginalTrade()
        return bool(trade and GetQuoteRequestId(trade))
        
def OpenQuoteRequestViewerDialog(eii):
    return InstrumentDefinitionQuoteRequestHistoryDialog(eii)
    
