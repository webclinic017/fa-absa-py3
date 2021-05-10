import acm
from FillSalesOrderDealPackageBase import FillSalesOrderDealPackageBase
from DealPackageDevKit import DealPackageDefinition, DealPackageException
from DealPackageUtil import SalesTradingInfo
from RFQUtils import Misc
from FillSalesOrderDefinitionComposite import FillSalesOrderDefinitionComposite
from DealPackageUtil import UnpackPaneInfo, SalesTradingInfo
from FillSalesOrderCustomizations import FillSalesOrderCustomDefinition
from TradeCreationUtil import TABTradeCreationSetting

class FillSalesOrderDefinition(FillSalesOrderDealPackageBase):
    fillSalesOrder      = FillSalesOrderDefinitionComposite(salesOrderName='SalesOrder',
                                                            salesOrderDealPackageName='DelegatedDealPackage',
                                                            salesOrderTrade='DelegatedTrade')             

    def OnInit(self, *args, **kwargs):
        super(FillSalesOrderDefinition, self).OnInit(*args, **kwargs)
        self._salesOrder = None        
        
        
    def AssemblePackage(self, arguments, *args):
        input = arguments[0]
        self.SetSalesOrder(input)
        
    def SalesOrder(self, *args):
        return self._salesOrder
    
    '''***********************************************************************************************
    * Set Sales Order
    ***********************************************************************************************'''     
    def SetDealPackage(self):
        salesOrder = self.SalesOrder()
        if salesOrder:
            dealPackage = Misc.FindDealPackageFromImObject(salesOrder, self.DealPackage().GUI(), False)
            self.DelegatedDealPackage(dealPackage)
        
    def SetTrade(self):
        salesOrder = self.SalesOrder()
        if salesOrder and not self.DelegatedDealPackage():
            trade = Misc.FindTradeFromImObject(salesOrder, self.DealPackage().GUI())
            self.DelegatedTrade(trade)
    
    def SetSalesOrder(self, salesOrder):
        if salesOrder:
            self._salesOrder = salesOrder
            self.SetDealPackage()
            self.SetTrade()

    '''********************************************************************
    * Attribute override
    ********************************************************************'''
    def AttributeOverrides(self, overrideAccumulator):
        FillSalesOrderCustomDefinition.CustomAttributeOverrides(overrideAccumulator)
