""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FSalesTradingMenuItem.py"
"""-------------------------------------------------------------------------------------------------
MODULE
    FSalesTradingMenuItem

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------"""

import acm
import FUxCore
import FEvent
import FProtectionDialog
from FCurrentActiveObjects import CurrentActiveObjects
from FCTSUtils import GetDivStreamFromInstrument
from FIntegratedWorkbenchMenuItem import IntegratedWorkbenchMenuItem
from FIntegratedWorkbench import GetHandler, LaunchView
from FParameterSettings import ParameterSettingsCreator


class SalesTradingMenuItem(IntegratedWorkbenchMenuItem):

    def __init__(self, extObj, view=None):
        IntegratedWorkbenchMenuItem.__init__(self, extObj, view)

    def GetCurrentActiveObject(self, key):
        try:
            return self.CurrentActiveObjectHandler().Object(key)
        except Exception:
            return None

    def CurrentActiveObjectHandler(self):
        return GetHandler(self.View(), CurrentActiveObjects)

class ViewMenuItem(FUxCore.MenuItem, object):

    APP = None

    def __init__(self, view):
        self._view = view

    def View(self):
        raise NotImplementedError

    def Enabled(self):
        return True

    def Settings(self):
        return ParameterSettingsCreator.FromRootParameter(self._view)

    def WorkbookName(self):
        try:
            return self.Settings().Workbook()
        except AttributeError:
            return None

    def Workbook(self):
        try:
            return acm.FWorkbook[self.WorkbookName()]
        except Exception:
            return None

    @classmethod
    def SetApp(cls):
        try:
            str(cls.APP)
        except RuntimeError:
            cls.APP = None

    def Invoke(self, eii):
        cls = type(self)
        cls.SetApp()
        if cls.APP is None:
            if self.Workbook():
                cls.APP = FindAppWithWorkbook(self.Workbook()) or acm.StartApplication(self.Settings().Application(), self.Workbook())
            else:
                cls.APP = LaunchView(self.Settings().Name())
        cls.APP.Activate()



class BondViewMenuItem(ViewMenuItem):

    def __init__(self, extObj):
        super(BondViewMenuItem, self).__init__('BondView')

class ClientViewMenuItem(ViewMenuItem):


    def __init__(self, extObj):
        super(ClientViewMenuItem, self).__init__('ClientView')


class MarketMakerViewMenuItem(ViewMenuItem):

    def __init__(self, extObj):
        super(MarketMakerViewMenuItem, self).__init__('MarketMakerView')

def FindAppWithWorkbook(workbook):
    for app in acm.ApplicationList():
        if app.IsKindOf(acm.FManagerBaseFrame):
            if (app.ActiveWorkbook().StoredWorkbook() is workbook):
                return app

class SalesActivityMenuItem(SalesTradingMenuItem):

    def __init__(self, extObj):
        super(SalesActivityMenuItem, self).__init__(extObj)

    def Enabled(self):
        return True

    def CreateObjectFromCAO(self):
        sa = acm.FSalesActivity()
        ins = self.GetCurrentActiveObject('Instrument')
        sa.Instrument(ins)
        sa.Counterparty(self.GetCurrentActiveObject('Party'))
        return sa

    def Invoke(self, eii):
        acm.StartApplication('Sales Activity', self.CreateObjectFromCAO())


class SaveSheetAsTemplateMenuItem(SalesTradingMenuItem):

    def __init__(self, extObj):
        super(SaveSheetAsTemplateMenuItem, self).__init__(extObj)

    def Invoke(self, eii):
        event = FEvent.OnSaveSheetAsTemplate(eii.Parameter('sheet'))
        self._Dispatcher().Update(event)


class UnderlyingInstrumentMenuItem(SalesTradingMenuItem):

    def __init__(self, extObj):
        super(UnderlyingInstrumentMenuItem, self).__init__(extObj)

    def EnabledFunction(self):
        instrument = self.GetCurrentActiveObject('Instrument')
        return bool(instrument and instrument.Underlying())

    def Invoke(self, eii):
        acm.StartApplication("Instrument Definition",
                             self.GetCurrentActiveObject('Instrument').Underlying())


class UnderlyingDividendsMenuItem(SalesTradingMenuItem):

    def __init__(self, extObj):
        super(UnderlyingDividendsMenuItem, self).__init__(extObj)

    def EnabledFunction(self):
        return bool(self.GetCurrentActiveObject('Instrument') and
                    GetDivStreamFromInstrument(self.GetCurrentActiveObject('Instrument')))

    def Invoke(self, eii):
        dividendStream = GetDivStreamFromInstrument(self.GetCurrentActiveObject('Instrument'))
        acm.StartApplication("Dividend Estimation", dividendStream)

class DiaryMenuItem(FUxCore.MenuItem):

    KEY = 'SalesActivityDiary'

    def __init__(self, application):
        self.app = application

    def Checked(self):
        try:
            return self.app.Frame().IsDockWindowVisible(self.KEY)
        except Exception:
            return False
    
    def Invoke(self, eii):
        try:
            isVisible = self.app.Frame().IsDockWindowVisible(self.KEY)
            self.app.Frame().ShowDockWindow(self.KEY, not isVisible)
        except Exception:
            pass
        
    def Enabled(self):
        return True
        
class EditDiaryMenuItem(FUxCore.MenuItem):
    
    KEY = 'SalesActivityDiary'
    
    def __init__(self, application):
        self.app = application
        self.diaryPanel = self.app.diaryPane
        self.diaryCtrl = self.diaryPanel.diaryCtrl
        self.historyCtrl = self.diaryPanel.historyCtrl
        
    def Checked(self):
        try:
            return self.historyCtrl.Editable()
        except AttributeError:
            pass
        
    def Invoke(self, eii):
        self.diaryPanel.ChangeActiveField()
            
    def Enabled(self):
        return self.app.Frame().IsDockWindowVisible(self.KEY) and bool(self.app.editObjectDiary)
            

class SalesActivityVolatilityMenuItem(FUxCore.MenuItem):

    def __init__(self, extObj):
        self.app = extObj

    def Applicable(self):
        return True

    def Enabled(self):
        return bool(self.app.DealPackage().GetAttribute('salesActivityPanel_priceAdjType') != 'Vega Nuke') and \
                bool(self.app.DealPackage().GetAttribute('salesActivityPanel_instrument'))

    def Invoke(self, eii):
        value = CalculatedValue(self.app.DealPackage().Object(), 'impliedVolatility')
        try:
            self.app.DealPackage().SetAttribute('salesActivityPanel_volatility', value)
        except Exception:
            pass
            
def CalculatedValue(obj, expression):
    value = None
    try:
        value = acm.GetCalculatedValueFromString(
            obj.Clone() if obj else acm.FUndefinedObject(),
            acm.GetDefaultContext(),
            expression,
            acm.GetGlobalEBTag()
            ).Value()
        return value.Number()
    except Exception:
        pass
    return value
    
class ViewProtection(FUxCore.MenuItem):

    def __init__(self, extObj):
        self._app = extObj
       
    def Applicable(self):
        return True
        
    def Enabled(self):
        return True
        
    def Invoke(self, eii):
        FProtectionDialog.ViewProtection(self._app.DealPackage().Object(), self._app.Shell(), True)
        
class SalesActivityContact(FUxCore.MenuItem):

    def __init__(self, extObj):
        self.app = extObj
        
    def Enabled(self):
        if self.app.DealPackage().GetAttribute('salesActivityPanel_contact'):
            return True
        else:
            return False
            
    def GetContact(self):
        contactKey = self.app.DealPackage().GetAttribute('salesActivityPanel_contact')
        counterparty = self.app.DealPackage().GetAttribute('salesActivityPanel_counterparty')
        for contact in counterparty.Contacts():
            if contact.StringKey() == contactKey:
                return contact
        
    def Invoke(self, eii):
        contact = self.GetContact()
        AttributeApplicationInvoker(contact)
        
class SalesActivityOpenAttribute(FUxCore.MenuItem):

    def __init__(self, extObj, attribute):
        self.app = extObj
        self.attribute = attribute
        
    def Applicable(self):
        return True
        
    def Enabled(self):
        if self.app.DealPackage().GetAttribute('salesActivityPanel_' + self.attribute):
            return True
        else:
            return False

    def Invoke(self, eii):
        attribute = self.app.DealPackage().GetAttribute('salesActivityPanel_' + self.attribute)
        AttributeApplicationInvoker(attribute)
        
class InspectorMenuItem(FUxCore.MenuItem):

    def __init__(self, extObj):
        self.app = extObj
        
    def Applicable(self):
        return True
        
    def Enabled(self):
        return True

    def Invoke(self, eii):
        acm.UX.Dialogs().ShowInspector(self.app.Shell(),  self.app.DealPackage().Object())
    
def AttributeApplicationInvoker(obj):
    try:
        app = acm.GetDefaultApplication(obj.Class())
        acm.StartApplication(app, obj)
    except Exception:
        pass

def CreateBondViewMenuItem(eii):
    return BondViewMenuItem(eii)

def CreateClientViewMenuItem(eii):
    return ClientViewMenuItem(eii)

def CreateMarketMakerViewMenuItem(eii):
    return MarketMakerViewMenuItem(eii)

def CreateSalesActivityMenuItem(eii):
    return SalesActivityMenuItem(eii)

def CreateDiaryMenuItem(eii):
    return SalesActivityDiaryMenuItem(eii)

def CreateEditDiaryMenuItem(eii):
    return SalesActivityEditDiaryMenuItem(eii)

def CreateVolatilityMenuItem(eii):
    return SalesActivityVolatilityMenuItem(eii)

def CreateSaveSheetAsTemplateMenuItem(eii):
    return SaveSheetAsTemplateMenuItem(eii)

def CreateUnderlyingInstrumentMenuItem(eii):
    return UnderlyingInstrumentMenuItem(eii)

def CreateUnderlyingDividendsMenuItem(eii):
    return UnderlyingDividendsMenuItem(eii)

def StartSalesActivityApplication(eii):
    acm.StartApplication('Sales Activity Application', 'Sales Activity')