
import acm
from SalesSideDealPackageBase import SalesSideDealPackageBase
from RFQDefinitionComposite import RFQDefinition
from RFQUtils import Validation, Misc
from DealPackageDevKit import DealPackageUserException
from SalesTradingCustomizations import OrderBookCreation
from QuoteRequestCustomizations import QuoteRequestCustomDefinition
from TradeCreationUtil import TradeCreation

class QuoteRequest(SalesSideDealPackageBase):
    rfq           = RFQDefinition(  trade='RFQTrade', 
                                    dealPackage='RFQDealPackage',
                                    originalObject='OriginalObject',
                                    reOpening='ReOpening',
                                    checkLimits='CheckLimits')

        
    '''***********************************************************************************************
    * Deal Package Interface
    ***********************************************************************************************'''             
    def OnInit(self, *args):
        super(QuoteRequest, self).OnInit(*args)
        
    def AssemblePackage(self, arguments):
        arguments = self.Arguments(arguments)
        content = arguments.At('content')
        # Must init with customerQR. The customerQR holds the dealpackage/trade to be opened.
        # The async query to find customerQR from tradingQR cannot be made in AssemblePackage, it must be done prior.
        self._originalObject = content if content and hasattr(content, 'IsKindOf') and content.IsKindOf(acm.FQuoteRequestInfo) else None 
        if self._originalObject:
            arguments.AtPut('imObject', self._originalObject)
        super(QuoteRequest, self).AssemblePackage(arguments)
        
    def OnNew(self, *args):
        if self.ReOpening() and self.OriginalCustomerQuoteRequest():
            self.DealPackage().GetAttribute('rfq_initFromQuoteRequestInfo')(self.OriginalCustomerQuoteRequest())
        self.DealPackage().CalculationRefreshPeriod(300)
        
    '''***********************************************************************************************
    * Object mappings
    ***********************************************************************************************'''         
    def RFQDealPackage(self):
        return self.DelegatedDealPackage()

    def RFQTrade(self):
        return self.DelegatedTrade()
    
    def OriginalCustomerQuoteRequest(self):
        originalObject = self.OriginalObject()
        return originalObject if hasattr(originalObject, 'IsKindOf') and originalObject.IsKindOf(acm.FQuoteRequestInfo) else None
        
    def CustomPanesName(self):
        return 'CustomPanes_STI_QuoteRequest'
    
    '''***********************************************************************************************
    * Save
    ***********************************************************************************************'''
    def Save(self):
        super(QuoteRequest, self).Save()
        self.rfq.SetUpQRData()
        
    '''***********************************************************************************************
    * Send Quote Request
    ***********************************************************************************************'''
    def TradeCreationSetting(self):
        return self.rfq.request.tradeCreationSetting
    
    def CheckValidToSendQuoteRequest(self):
        self.rfq_request.CheckValidToSendQuoteRequest()
    
    def SendOrderOrQuoteRequest(self, isOrder):
        try:
            if isOrder:
                self.rfq_request.SendOrder()
            else:
                self.rfq_request.RequestQuote()
        except Exception as e:
            actionStr = 'Send Order' if isOrder else 'Request Quote'
            errorStr = 'Failed to ' + actionStr + ': ' + str(e)
            raise DealPackageUserException(errorStr)
    
    def OnSendOrderOrRequest(self, isOrder):
        marketPlace = acm.FMarketPlace[OrderBookCreation.DefaultMarket(self.RFQTrade().Instrument().Originator())]
        Validation.IsConnected(marketPlace)
        self.CheckValidToSendQuoteRequest()
        readyToSend = True
        if not self.IsSaved():
            self.Save()
        self.SendOrderOrQuoteRequest(isOrder)
        self._UpdateDelegations()
        
    def OnRequestQuoteAction(self, *args):
        self.OnSendOrderOrRequest(False)
    
    def OnSendOrderAction(self, *args):
        self.OnSendOrderOrRequest(True)
    
    def OnNewInsAndTradeAction(self, *args):
        super(QuoteRequest, self).OnNewInsAndTradeAction(*args)
        self.rfq_request_OnNewInsAndTrade()
    
    def OnNewTradeAction(self, *args):
        super(QuoteRequest, self).OnNewTradeAction(*args)
        self.rfq_request_OnNewTrade()
    
    '''***********************************************************************************************
    * All fields in the Deal Package section should be grayed out when request is sent
    ***********************************************************************************************'''  
    def DelegatedDealPackageSectionEnabled(self, attrName):
        enabled = False
        if not self.RequestIsSent() and self.CreateNewInsAndTradeCreationHandling():
            enabled = self.RFQDealPackage().GetAttributeMetaData(attrName[12:], 'enabled')()
        return enabled
        
    def RequestIsSent(self):
        isSent = False
        try:
            isSent = self.rfq_request.requestButtonClicked
        except:
            pass
        return isSent
    
    

    '''***********************************************************************************************
    * Overrides
    ***********************************************************************************************'''        
    def AttributeOverrides(self, overrideAccumulator):
        QuoteRequestCustomDefinition.CustomAttributeOverrides(overrideAccumulator)
        overrideAccumulator(
                {'rfq_request_client'                   : dict(onChanged='@OnClientChanged'),
                 'rfq_request_salesPortfolio'           : dict(onChanged='@OnPortfolioChanged'),
                 'rfq_request_requestedQuantity'        : dict(onChanged='@OnQuantityChanged'),
                 'rfq_request_requestedNominal'         : dict(onChanged='@OnNominalChanged'),
                 'rfq_request_request'                  : dict(action='@OnRequestQuoteAction'),
                 'rfq_request_sendOrder'                : dict(action='@OnSendOrderAction'),
                 'rfq_request_newInsAndTrade'           : dict(action='@OnNewInsAndTradeAction'),
                 'rfq_request_newTrade'                 : dict(action='@OnNewTradeAction')
                }
            )    


        
        
