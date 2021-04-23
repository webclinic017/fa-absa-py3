""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/ExecutionView/etc/FExecutionViewMenuItem.py"
"""-------------------------------------------------------------------------------------------------
MODULE
    FExecutionViewMenuItem

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Functionality for menu items in or related to workbench "Execution View"
-------------------------------------------------------------------------------------------------"""
import acm
import FUxCore
import FIntegratedWorkbench
import FOrderUtils
from FViewUtils import ViewSettings
from FSheetUtils import GetWorkbook, FindAppWithWorkbook

class StartExecutionViewMenuItem(FUxCore.MenuItem, object):
    
    APP = None

    def __init__(self, extObj, view='ExecutionView'):
        self._frame = extObj
        self._view = view
    
    def Settings(self):
        return ViewSettings(self._view)
    
    def _IsShared(self):
        return self.Settings().IsShared()
            
    def Workbook(self):
        try:
            name = self.Settings().Workbook()
            return GetWorkbook(name, self._IsShared())
        except Exception:
            pass
        
    @classmethod
    def SetApp(cls):
        try:
            str(cls.APP)
        except RuntimeError:
            cls.APP = None

    def Invoke(self, _eii):
        cls = type(self)
        cls.SetApp()
        if cls.APP is None:
            defaultWorkbook = self.Workbook()
            if defaultWorkbook:
                cls.APP = FindAppWithWorkbook(defaultWorkbook) or\
                acm.StartApplication(self.Settings().Application(), defaultWorkbook)
            else:
                cls.APP = FIntegratedWorkbench.LaunchView(self._view)
        cls.APP.Restore()
        cls.APP.Activate()
        
def StartExecutionView(eii):
    return StartExecutionViewMenuItem(eii)
    
def CreateManualFillMenuItem(eii):
    return ManualFillMenuItem(eii)

def OpenInstrument(eii):
    return OpenInstrumentMenuItem(eii)
    
def AcceptOrder(eii):
    return AcceptOrderMenuItem(eii)


class ExecutionViewMenuItem(FUxCore.MenuItem, object):

    ACTIVE_ORDER_SALES_STATE = (set(acm.FEnumeration['salesStateType'].Values()) - 
                                {"Completed", "Cancelled", "Req Cancel", "Inactive", "Done", "Done Exec", "Indication"})

    def __init__(self, eii):
        self._frame = eii

    def Sheet(self):
        return self._frame.ActiveSheet()

    def TradingSession(self):
        return FOrderUtils.TradingSession()
        
    def _SelectedSalesOrder(self):
        try:
            return self.Sheet().Selection().SelectedOrders()[0]
        except IndexError:
            return None

    def _SelectedSalesOrders(self):
        return [order for order in self.Sheet().Selection().SelectedOrders()
                if order.OrderRole() in ['Order Program Sales Order', 'Sales Order', 'Bulk Order']]

    def SelectedSalesOrderHandlers(self):
        return [FOrderUtils.AsOrderHandler(order) for order in self._SelectedSalesOrders()]
    
    def ValidateOrderStates(self, errorMsg='Not possible in state {0}', validStates=ACTIVE_ORDER_SALES_STATE):
        for order in self._SelectedSalesOrders():
            if order.SalesState() not in validStates:
                msg = errorMsg.format(order.SalesState())
                acm.UX().Dialogs().MessageBoxInformation(self._frame.Shell(), msg)
                return False
        return True
    
    def Invoke(self, _eii):
        self.InvokeAsynch(_eii)
    
    def Enabled(self):
        return True

    def InvokeAsynch(self, eii):
        ''' Override in child classes'''
        pass

class OpenInstrumentMenuItem(ExecutionViewMenuItem):
    
    def InvokeAsynch(self, eii):
        instrument = self._SelectedSalesOrder().Instrument()
        acm.StartApplication('Instrument Definition', instrument)
    
    def Enabled(self):
        return bool(self._SelectedSalesOrders())
        
class ManualFillMenuItem(ExecutionViewMenuItem):
    
    def Enabled(self):
        return bool(self._SelectedSalesOrders())
        
    def GetManualFillDialog(self, eii):
        mod, cls = eii.MenuExtension().GetString('DialogClass').split('.')
        return getattr(__import__(mod), cls)
        
    def InvokeAsynch(self, eii):
        if self.ValidateOrderStates(errorMsg='Not possible to manually fill order in state {0}'):
            customDlg = self.GetManualFillDialog(eii)(self._SelectedSalesOrder(), self._frame.Shell())
            acm.UX().Dialogs().ShowCustomDialogModal(self._frame.Shell(), customDlg.CreateLayout(), customDlg)
            

class AcceptOrderMenuItem(ExecutionViewMenuItem):
    
    def Accept(self, order):
        order.UserId(acm.User().Name())
        FOrderUtils.SetSalesState(order, 'Accepted')
        FOrderUtils.OrderSender(order).SendOrder()

    def Unaccept(self, order):
        order.UserId(order.SalesPerson())
        FOrderUtils.SetSalesState(order, 'Pending')
        FOrderUtils.OrderSender(order).SendOrder()
    
    def IsAccepted(self, order):
        return order.SalesState() == 'Accepted' and order.UserId().lower() == str(acm.User().Name()).lower()
    
    def Checked(self):
        return all(self.IsAccepted(order) for order in self._SelectedSalesOrders())
    
    def InvokeAsynch(self, eii):            
        if self.Checked():
            for order in self.SelectedSalesOrderHandlers():
                self.Unaccept(order)
        else:
            if self.ValidateOrderStates(errorMsg='Can only accept orders in state Pending', validStates=['Pending']):
                for order in self.SelectedSalesOrderHandlers():
                    self.Accept(order)

    def Enabled(self):
        return bool(self._SelectedSalesOrders())
