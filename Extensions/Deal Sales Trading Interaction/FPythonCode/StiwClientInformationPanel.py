import acm
from FPanel import Panel
import FEvent
from StiwEvents import OnClientChanged, OnUnderlyingChanged

from DealPackageUxTraitsTabPane import TraitsPane
from DealPackageUtil import RefreshDealPackageProxy, UnpackPaneInfo, WrapAsTabControlList
from DealPackageUtil import DealPackageException


class StiwClientInformationPanel(Panel):
    def __init__(self):
        super(StiwClientInformationPanel, self).__init__()
        
        self._dealPackage = None
        self._onIdleCallback = None
        self._customPane = None
        self._refreshProxy = None
        self._currentClient = None
        self._currentUnderlying = None
        self._dealPackage = acm.DealPackage().NewAsDecorator('Client Statistics STIW')
             
        self.InitOnIdleCallback()
            
    @FEvent.InternalEventCallback
    def OnPanelDestroyed(self, event):
        self.RemoveOnIdleCallback()    
        self.DealPackage().Dismantle()
                
    def InitOnIdleCallback(self):
        if self._onIdleCallback is None:
            self._onIdleCallback = acm.Time.Timer().CreatePeriodicTimerEvent(0.15, self.PeriodicTimerEvent, None)
            
    def RemoveOnIdleCallback(self):
        if self._onIdleCallback:
            acm.Time.Timer().RemoveTimerEvent(self._onIdleCallback)
            self._onIdleCallback = None   
                
    def PeriodicTimerEvent(self, *args):
        if self.RefreshProxy():
            self.RefreshProxy().Refresh() 
        self.SendEvents()
        
    def SendEvents(self):
        if self.DealPackage():
            self.SendClientEvent()
            self.SendUnderlyingEvent()
            
    def SendClientEvent(self):
        newClient = self.DealPackage().GetAttribute('client')
        if newClient != self._currentClient:
            self._currentClient = newClient
            self.SendEvent(OnClientChanged(self, newClient))
            
    def SendUnderlyingEvent(self):
        newUnderlying = self.DealPackage().GetAttribute('underlying')
        if newUnderlying != self._currentUnderlying:
            self._currentUnderlying = newUnderlying
            self.SendEvent(OnUnderlyingChanged(self, newUnderlying))
         
    def Application(self):
        return self

    def GetAttribute(self, traitName):
        return self.DealPackage().GetAttribute(traitName)
        
    def GetAttributeMetaData(self, traitName, metaKey):
        return self.DealPackage().GetAttributeMetaData(traitName, metaKey)

    def CustomPane(self):
        return self._customPane
        
    def InitControls(self, *args):
        pass
        
    def CreateDealPackageLayout(self, paneName, customLayout):
        fuxLayoutBuilder = acm.FUxLayoutBuilder()
        self._customPane = TraitsPane(self, paneName)
        self.CustomPane().BuildPaneLayout(fuxLayoutBuilder, customLayout) 
        layout = self.SetLayout( fuxLayoutBuilder )
        self.CustomPane().AddLayoutToBindingsAndInitControls(layout)
    
    def CreateLayout(self):
        self.CreateDealPackage()
        paneName, customLayout = self._GetCustomPaneInfo()
        self.CreateDealPackageLayout(paneName, customLayout)        
     
    def CustomPanes(self):
        return self.DealPackage().GetAttribute('customPanes')
    
    def _GetCustomPaneInfo(self):
        paneInfos = []
        customPaneInfos = self.CustomPanes()
        customPaneInfos = WrapAsTabControlList(customPaneInfos)
        for tabsInfo in customPaneInfos:
            tabContolName, tabControlLayout = UnpackPaneInfo(tabsInfo)
            for paneInfo in tabControlLayout:
                paneInfos.append(paneInfo)
        if len(paneInfos) != 1:
            raise DealPackageException('Dock Panels do not support tabbed layouts')
        return UnpackPaneInfo(paneInfos[0])
       
    def _UpdateTraitsTabValues(self):
        self.CustomPane().HandleOnIdle()

    def DealPackage(self):
        return self._dealPackage
        
    def RefreshProxy(self):
        return self._refreshProxy
        
    def CreateDealPackage(self):
        gui = acm.FBusinessLogicGUIShell()
        gui.SetFUxShell(self.Shell())
        self._dealPackage = acm.DealPackage().NewAsDecorator('Client Statistics STIW', gui, None)
        self._refreshProxy = RefreshDealPackageProxy(self.DealPackage())
        self.RefreshProxy().RegisterObserver(self._UpdateTraitsTabValues)

