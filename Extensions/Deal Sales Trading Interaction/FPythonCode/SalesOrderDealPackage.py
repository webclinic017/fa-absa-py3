import acm
from SalesSideDealPackageBase import SalesSideDealPackageBase
from SalesOrderCompositeDefinition import SalesOrderDefinition
from DealPackageDevKit import DealPackageUserException
from SalesTradingCustomizations import OrderBookCreation
from SalesOrderCustomizations import SalesOrderCustomDefinition
from RFQUtils import Validation, Misc

class SalesOrder(SalesSideDealPackageBase):
    salesOrder           = SalesOrderDefinition(  trade='SalesOrderTrade',
                                                  dealPackage='SalesOrderDealPackage',
                                                  originalObject='OriginalObject',
                                                  initiatedFromTradingInterface='InitiatedFromTradingInterface',
                                                  reOpening='ReOpening',
                                                  checkLimits='CheckLimits')
                                                  
    def OnInit(self, *args):
        super(SalesOrder, self).OnInit(*args)
        self._tradingInterface = None
        self._salesOrderHandler = None
        
    def AssemblePackage(self, arguments):
        arguments = self.Arguments(arguments)
        content = arguments.At('content')
        self._originalObject, self._tradingInterface = Misc.FindOrderHandler(content)
        if self._originalObject:
            arguments.AtPut('imObject', self._originalObject)
        super(SalesOrder, self).AssemblePackage(arguments)
    
    def OnNew(self, *args):
        if self.ReOpening() and self.OriginalSalesOrder():
            self.DealPackage().GetAttribute('salesOrder_initFromOrderHandler')(self.OriginalSalesOrder())
        self.DealPackage().CalculationRefreshPeriod(300)

    
    '''***********************************************************************************************
    * Object mappings
    ***********************************************************************************************'''         
    def SalesOrderTrade(self):
        return self.DelegatedTrade()
 
    def SalesOrderInstrument(self):
        return self.SalesOrderTrade().Instrument()
        
    def SalesOrderDealPackage(self, *args):
        return self.DelegatedDealPackage()
    
    def InitiatedFromTradingInterface(self):
        return True if self._tradingInterface else False
        
    def OriginalSalesOrder(self, *args):
        originalObject = self.OriginalObject()
        return originalObject if hasattr(originalObject, 'IsKindOf') and originalObject.IsKindOf(acm.FOrderHandler) else None
        
    def CustomPanesName(self):
        return 'CustomPanes_STI_SalesOrder'
        
    '''********************************************************************
    * Send Order
    ********************************************************************'''
    def TradeCreationSetting(self):
        return self.salesOrder.tradeCreationSetting
    
    def IsModifyOrderState(self):
        return self.salesOrder._modifyOrderState
        
    def IsModifyDealPackageAllowed(self):
        return self.salesOrder.salesState == 'Pending'
        
    def CreateSaveConfig(self):
        dp = self.DelegatedDealPackage()
        saveConfig = acm.FDealPackageSaveConfiguration()
        if self.IsModifyOrderState():
            if self.IsModifyDealPackageAllowed():
                saveConfig.InstrumentPackage('Exclude')
                saveConfig.DealPackage('Save')
            else:
                saveConfig.InstrumentPackage('Exclude')
                saveConfig.DealPackage('Exclude')                
        else:
            saveConfig = super(SalesOrder, self).CreateSaveConfig()
        return saveConfig
 
    '''***********************************************************************************************
    * All fields in the Deal Package section should be grayed out when order is sent
    ***********************************************************************************************'''     
    def DelegatedDealPackageSectionEnabled(self, attrName):
        enabled = False
        if not self.IsModifyOrderState():
            if not self.OrderIsSent() and self.CreateNewInsAndTradeCreationHandling():
                enabled = self.SalesOrderDealPackage().GetAttributeMetaData(attrName[12:], 'enabled')()
        return enabled
    
    def OrderIsSent(self):
        isSent = False
        try:
            isSent = self.salesOrder.orderIsSent
        except:
            pass
        return isSent
    '''***********************************************************************************************
    * Overrides
    ***********************************************************************************************'''             
    def OnSendOrderAction(self, *args):
        if not self.salesOrder.sendInProgress:
            marketPlace = acm.FMarketPlace[OrderBookCreation.DefaultMarket(self.SalesOrderInstrument().Originator())]
            Validation.IsConnected(marketPlace)
            self.salesOrder.CheckValidToSendOrder()
            if not self.IsSaved():
                self.Save()
            self.salesOrder.SendOrder()
    
    def OnNewInsAndTradeAction(self, *args):
        super(SalesOrder, self).OnNewInsAndTradeAction(*args)
        self.salesOrder_OnNewInsAndTrade()
    
    def OnNewTradeAction(self, *args):
        super(SalesOrder, self).OnNewTradeAction(*args)
        self.salesOrder_OnNewTrade()
            
    '''********************************************************************
    * Attribute override
    ********************************************************************'''
    def AttributeOverrides(self, overrideAccumulator):
        SalesOrderCustomDefinition.CustomAttributeOverrides(overrideAccumulator)
        overrideAccumulator(
                {
                 'salesOrder_sendOrder'         : dict(action='@OnSendOrderAction'),
                 'salesOrder_quantity'          : dict(onChanged='@OnQuantityChanged'),
                 'salesOrder_nominal'          : dict(onChanged='@OnNominalChanged'),
                 'salesOrder_client'            : dict(onChanged='@OnClientChanged'),
                 'salesOrder_portfolio'         : dict(onChanged='@OnPortfolioChanged'),
                 'salesOrder_newInsAndTrade'    : dict(action='@OnNewInsAndTradeAction'),
                 'salesOrder_newTrade'          : dict(action='@OnNewTradeAction')
                }
            )  
        
