
import acm
from DealPackageDevKit import DealPackageDefinition, DealPackageException, Delegate
from RFQUtils import MethodDirection, Misc
from DealPackageUtil import UnpackPaneInfo

class FillSalesOrderDealPackageBase(DealPackageDefinition):

    delegatedDP     = Delegate( attributeMapping='DelegatedDealPackage',
                                enabled=False,
                                customPanes='@DealPackageCustomPanes')

    '''***********************************************************************************************
    * Deal Package interface
    ***********************************************************************************************'''                                                                     
    def OnInit(self, *args, **kwargs):
        self._delegatedDP = None

    '''***********************************************************************************************
    * Object mappings
    ***********************************************************************************************'''                                                     
    def DelegatedDealPackageAttribute(self):
        return self.delegatedDP
        
    def DelegatedDealPackage(self, dealPackage = MethodDirection.asGetMethod):
        if dealPackage == MethodDirection.asGetMethod:
            return self._delegatedDP
        else:
            self._delegatedDP = dealPackage
    
    def DelegatedTrade(self, trade = MethodDirection.asGetMethod):
        if trade == MethodDirection.asGetMethod:
            delegatedTrade = Misc.GetTradeFromDealPackage(self.DelegatedDealPackage())
            if not delegatedTrade:
                delegatedTrade = self._delegatedTrade
            return delegatedTrade
        else:
            self._delegatedTrade = trade
    
    '''***********************************************************************************************
    * UX Layout
    ***********************************************************************************************'''  
    def CustomPanesName(self):
        return 'CustomPanes_STI_FillSalesOrder'
        
    def DealPackageCustomPanes(self):
        return Misc.DealPackageCustomPanes(self.DelegatedDealPackage(), self.GetCustomPanesFromExtValue, 'tradingCustomPane')
        
    def CustomPanes(self):
        if self.DelegatedDealPackage():
            tabControls = self.DelegatedDealPackageAttribute().GetLayout()
            tabCtrlName, tabCtrlLayout = UnpackPaneInfo(tabControls[0])
            tabName, paneLayout = UnpackPaneInfo(tabCtrlLayout[0])
            
            panes = self.GetCustomPanesFromExtValue(self.CustomPanesName())
            key = list(panes[0].keys())[0]
            panes[0][key] = paneLayout + panes[0][key]
        else:
            panes = self.GetCustomPanesFromExtValue(self.CustomPanesName())
        return panes
