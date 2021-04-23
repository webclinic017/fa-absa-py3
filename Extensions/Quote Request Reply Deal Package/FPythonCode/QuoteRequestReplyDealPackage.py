

import acm
from QuoteRequestReplyDealPackageBase import QuoteRequestReplyDealPackageBase
from DealPackageDevKit import DealPackageException, Action, Object
from DealPackageUtil import UnpackPaneInfo, SalesTradingInfo
from QuoteRequestReplyUtil import Misc
from QuoteRequestReplyCustomizations import QuoteRequestReplyCustomDefinition

# import the Quote Request Reply Compisite, either from QuoteRequestReplyComposite or from the Sales Trader interaction module
try:
    from QuoteRequestReplyCompositeOverride import QuoteRequestReplyCompositeDefinitionOverride as QuoteRequestReplyCompositeDefinition
except Exception as e:
    from QuoteRequestReplyComposite import QuoteRequestReplyCompositeDefinition

class QuoteRequestReply(QuoteRequestReplyDealPackageBase):
    qrr                     = QuoteRequestReplyCompositeDefinition(  
                                      quoteControllerName='SelectedQuoteController', 
                                      tradeMethodName='DelegatedTrade',
                                      qrrDealPackageName='DelegatedDealPackage')
                                                
    updateQuoteController   = Action( action='@UpdateQuoteController')
                                        
    def OnInit(self, *args, **kwargs):
        super(QuoteRequestReply, self).OnInit(*args, **kwargs)
        self._selectedQuoteController = None
        self._trade = None
        
    def AssemblePackage(self, arguments):
        try:
            input = arguments[0]
            self.SetSelectedQuoteController(input if input.IsKindOf(acm.FQuoteController) else None)
        except Exception as e:
            print ('QuoteRequestReply - AssemblePackage, failed', e)
    
    '''***********************************************************************************************
    * Objects
    ***********************************************************************************************'''             
    def SelectedQuoteController(self):
        return self._selectedQuoteController
    
    '''***********************************************************************************************
    * Update the currently selected Deal Package and Quote Controller
    ***********************************************************************************************'''     
    def SetDealPackage(self):
        quoteController = self.SelectedQuoteController()
        if quoteController and quoteController.QuoteRequestReply():
            dealPackage = Misc.FindDealPackageFromQuoteController(quoteController, self.DealPackage().GUI())
            self.DelegatedDealPackage(dealPackage)
        
    def SetTrade(self):
        quoteController = self.SelectedQuoteController()
        if quoteController and quoteController.QuoteRequestReply() and not self.DelegatedDealPackage():
            trade = Misc.FindTradeFromQuoteController(quoteController, self.DealPackage().GUI())
            self.DelegatedTrade(trade)
                
    def SetQuoteController(self, quoteController):
        self._selectedQuoteController = quoteController
    
    def SetSelectedQuoteController(self, quoteController):
        if quoteController and quoteController.QuoteRequestReply():
            self.SetQuoteController(quoteController)
            self.SetDealPackage()
            self.SetTrade()
        
    '''***********************************************************************************************
    * Actions
    ***********************************************************************************************'''  
    def UpdateQuoteController(self, attrName, quoteController = None):
        self.SetSelectedQuoteController(quoteController)

    '''***********************************************************************************************
    * Attribute override
    ***********************************************************************************************'''  
    def AttributeOverrides(self, overrideAccumulator):
        QuoteRequestReplyCustomDefinition.CustomAttributeOverrides(overrideAccumulator)
    
        
