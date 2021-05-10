import acm
import FUxCore
try:
    import FIntegratedWorkbench
except:
    FIntegratedWorkbench = None
from SalesRFQDialog import StartSalesRFQDialog
from SalesOrderDialog import StartSalesOrderDialog
from DealPackageAsDialog import OpenDealPackageDialogWithClose
from StiwUtils import GetNotificationSetting
from QuoteRequestHistoryViewer import GetQuoteRequestId, OpenQuoteRequestHistoryViewer, OpenQuoteRequestHistoryViewerFromTrade
from DealPackageAsDialog import OpenDealPackageDialogWithNoButtons
from StiwNotifyUserOnQuoteRequestUpdate import StiwNotifyUserOnQuoteRequestUpdate, FilterSelectionDlg
from RFQUtils import Direction

'''********************************************************************
* Utils
********************************************************************'''
def WorkbenchHandler(extObj):
    handler = None
    if FIntegratedWorkbench is not None:
        view = FIntegratedWorkbench.GetView(extObj)
        handler = FIntegratedWorkbench.GetHandlerByName(view, 'StiwHandler')
    return handler

def Get(attribute, extObj):
    # For example, attribute = "Client" gives WorkbenchHandler(extObj).Client()
    wh = WorkbenchHandler(extObj)
    return wh and getattr(wh, attribute)()

def CreateDealAndDealPackageSubMenu(action, extObj):
    
    def CreateSubMenu(parentMenu, label, items, extObj, templates=None):
        submenu = parentMenu.AddSubMenu(label)
        for ext in items:
            obj = ext.Value()
            definition = obj.DisplayName() if hasattr(obj, 'DisplayName') else str(obj.Caption())
            submenu.AddItem(action, [extObj, definition], definition, None)
            if templates and definition in templates:
                CreateSubMenu(submenu, definition+' Templates', templates[definition], extObj)
    
    menu = acm.FUxMenu()
    extensions = acm.GetDefaultContext().GetAllExtensions('FDealPackageDefinition')
    deals = [e for e in extensions if e.Value().CustomApplicationName() == 'Deal']
    dealPackages = [e for e in extensions if e.Value().CustomApplicationName() == 'Deal Package']
    templates = GetTemplateDeals()
    if deals:
        CreateSubMenu(menu, 'Deal', deals, extObj, templates)
    if dealPackages:
        CreateSubMenu(menu, 'Deal Package', dealPackages, extObj)
    return menu

def GetTemplateDeals():
    # Returns all templates as a dict on the format:
    #   return {"Name of base deal": ["List of", "All Templates"],
    #           "Swap Deal": [FCustomInstrumentDefinition("CAD Swap Deal"), FCustomInstrumentDefinition("CHF Swap Deal")]}
    
    customInstrumentDefinitions = acm.GetDefaultContext().GetAllExtensions('FCustomInstrumentDefinition')
    templates = [cid for cid in customInstrumentDefinitions if str(cid.Value().InstantiatedAs()) == "Template"]
    
    def extends_deal(cid):
        extends = None
        if cid.ExtendsConfiguration():
            extendsConfiguration = acm.GetDefaultContext().GetExtension('FCustomInstrumentDefinition', acm.FObject, cid.ExtendsConfiguration())
            if extendsConfiguration and extendsConfiguration.Value():
                candidate = extendsConfiguration.Value()
                if candidate != cid:
                    if candidate.DealPackageDefinition():
                        dpDef = acm.GetDefaultContext().GetExtension('FDealPackageDefinition', acm.FObject, candidate.DealPackageDefinition())
                        extends = str(dpDef.Value().DisplayName()) if dpDef else None
                    else:
                        extends = extends_deal(candidate)
        return extends

    templateDict = {}
    for customInsDef in templates:
        deal = extends_deal(customInsDef.Value())
        if deal:
            l = templateDict.setdefault(deal, [])
            l.append(customInsDef)
            
    return templateDict

'''********************************************************************
* Quote Request History
********************************************************************'''
def OpenSelectedTradeRfqHistory(extObj):
    trade = Get('SelectedTrade', extObj)
    shell = extObj.Shell()
    OpenQuoteRequestHistoryViewerFromTrade(trade, shell)

def OpenSelectedQrRfqHistory(extObj):
    qr = Get('SelectedQuoteRequest', extObj)
    if qr:
        shell = extObj.Shell() 
        OpenQuoteRequestHistoryViewer(qr.Id(), shell)

class QuoteRequestHistory(FUxCore.SubMenu):
    def __init__(self, extObj):
        self._extObj = extObj
     
    def TradeRFQHistoryEnabled(self, extObj):
        trade = Get('SelectedTrade', extObj)
        return bool(trade and GetQuoteRequestId(trade))

    def QrRFQHistoryEnabled(self, extObj):
        return bool(Get('SelectedQuoteRequest', extObj))
    
    def Applicable(self):
        return FIntegratedWorkbench is not None and WorkbenchHandler(self._extObj) is not None

    def Invoke(self, eii):
        extObj = eii.ExtensionObject()
        menu = acm.FUxMenu()
        menu.AddItem(OpenSelectedTradeRfqHistory, extObj, 'Selected Trade', None, self.TradeRFQHistoryEnabled(extObj))
        menu.AddItem(OpenSelectedQrRfqHistory, extObj, 'Selected QR', None, self.QrRFQHistoryEnabled(extObj))
        return menu

'''********************************************************************
* New OTC Quote Request
********************************************************************'''
def CreateNewQuoteRequest(args):
    extObj, definition = args
    client = Get('Client', extObj)
    shell = extObj.Shell()
    StartSalesRFQDialog(shell, definition, False, {'rfq_request_client' : client})
    
class NewOtcQuoteRequest(FUxCore.SubMenu):
    def __init__(self, extObj):
        self.m_menu = None
    
    def Invoke(self, eii):
        if self.m_menu is None:
            extObj = eii.ExtensionObject()
            self.m_menu = self.InitMenu(extObj)
        return self.m_menu
    
    def InitMenu(self, extObj):
        return CreateDealAndDealPackageSubMenu(action=CreateNewQuoteRequest, extObj=extObj)

'''********************************************************************
* New OTC Order
********************************************************************'''
def CreateNewOrder(args):
    extObj, definition = args
    shell = extObj.Shell()
    client = Get('Client', extObj)
    StartSalesOrderDialog(shell, definition, False, {'salesOrder_client' : client})
    
class NewOtcOrder(FUxCore.SubMenu):
    def __init__(self, extObj):
        self.m_menu = None
    
    def Invoke(self, eii):
        if self.m_menu is None:
            extObj = eii.ExtensionObject()
            self.m_menu = self.InitMenu(extObj)
        return self.m_menu
    
    def InitMenu(self, extObj):
        return CreateDealAndDealPackageSubMenu(action=CreateNewOrder, extObj=extObj)

'''********************************************************************
* New Quote Request from Trade
********************************************************************'''
class NewQuoteRequestFromTrade(FUxCore.MenuItem):
    def __init__(self, extObj):
        self._extObj = extObj
        
    def Invoke(self, eii):
        extObj = eii.ExtensionObject()
        trade = Get('SelectedTrade', extObj)
        shell = extObj.Shell()
        StartSalesRFQDialog(shell, trade, False)
    
    def Applicable(self):
        return FIntegratedWorkbench is not None and WorkbenchHandler(self._extObj) is not None
    
    def Enabled(self):
        return bool(Get('SelectedTrade', self._extObj))
    
    def Checked(self):
        return False

'''********************************************************************
* New Quote Request from Quote Request
********************************************************************'''
class NewQuoteRequestFromQuoteRequest(FUxCore.MenuItem):
    def __init__(self, extObj):
        self._extObj = extObj
        
    def Invoke(self, eii):
        extObj = eii.ExtensionObject()
        qr = Get('SelectedQuoteRequest', extObj)
        shell = extObj.Shell()
        StartSalesRFQDialog(shell, qr, False)
    
    def Applicable(self):
        return FIntegratedWorkbench is not None and WorkbenchHandler(self._extObj) is not None
        
    def Enabled(self):
        return bool(Get('SelectedQuoteRequest', self._extObj))
    
    def Checked(self):
        return False

'''********************************************************************
* New Order from Trade
********************************************************************'''
class NewOrderFromTrade(FUxCore.MenuItem):
    def __init__(self, extObj):
        self._extObj = extObj
        
    def Invoke(self, eii):
        extObj = eii.ExtensionObject()
        shell = extObj.Shell()
        trade = Get('SelectedTrade', self._extObj)
        StartSalesOrderDialog(shell, trade, False)
    
    def Applicable(self):
        return FIntegratedWorkbench is not None and WorkbenchHandler(self._extObj) is not None
    
    def Enabled(self):
        enabled = False
        trade = Get('SelectedTrade', self._extObj)
        if trade:
            enabled = trade.Status() != 'Internal'
        return enabled
        
    def Checked(self):
        return False

'''********************************************************************
* New Order from Order
********************************************************************'''
class NewOrderFromOrder(FUxCore.MenuItem):
    def __init__(self, extObj):
        self._extObj = extObj
        
    def Invoke(self, eii):
        extObj = eii.ExtensionObject()
        shell = extObj.Shell()
        order = Get('SelectedSalesOrder', self._extObj)
        StartSalesOrderDialog(shell, order, False)
    
    def Applicable(self):
        return FIntegratedWorkbench is not None and WorkbenchHandler(self._extObj) is not None
    
    def Enabled(self):
        return bool(Get('SelectedSalesOrder', self._extObj))
    
    def Checked(self):
        return False

'''********************************************************************
* Quote Request Notifications
********************************************************************'''
class NotifyUserOnQuoteRequestUpdated(FUxCore.MenuItem):
    def __init__(self, extObj):
        self.m_notify = StiwNotifyUserOnQuoteRequestUpdate(extObj)
        if GetNotificationSetting('EnabledByDefault'):
            self.SetDefaultStatuses()
        
    def Invoke(self, eii):
        if not self.m_notify.Statuses():
            # Do not pop dialog, just apply default statuses
            self.SetDefaultStatuses()
        else:
            statuses = self.m_notify.Statuses()
            
            filterDlg = FilterSelectionDlg(statuses)
            builder = filterDlg.CreateLayout()
            result = acm.UX().Dialogs().ShowCustomDialogModal(eii.ExtensionObject().Shell(), builder, filterDlg )
            
            if result is not None:
                self.m_notify.Statuses(result)
    
    def SetDefaultStatuses(self):
        self.m_notify.Statuses(GetNotificationSetting('DefaultStatuses'))
    
    def Checked(self):
        return bool(self.m_notify.Statuses())
