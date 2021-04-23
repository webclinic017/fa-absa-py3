""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendMenuItem.py"
"""--------------------------------------------------------------------------
MODULE
    FSecLendMenuItem

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Base class for menu items used in the securities lending workbenches.

---------------------------------------------------------------------------"""

import acm
import FUxCore
import FViewCreator
import FHandlerCreator
import ctypes
from FIntegratedWorkbench import GetView, LaunchView
from FIntegratedWorkbenchMenuItem import IntegratedWorkbenchMenuItem
from FViewUtils import ViewSettings
from FApplicationCreator import ManagerBaseApplcationCreator


def ContextCategory(eii):
    view = GetView(eii.ExtensionObject())
    return view and IsSecLendWorkbench(view.ClassName())

def IsSecLendWorkbench(viewName):
    if viewName in ['SecLendOrdersView', 'SecLendClientView', 'SecLendInventoryView', 'SecLendPortfolioView']:
        return True
    return False
    
def ContextCategoryOrdersView(eii):
    view = GetView(eii.ExtensionObject())
    if view and view.ClassName() in ['SecLendOrdersView']:
        return True
    return False

def ContextCategoryClientView(eii):
    view = GetView(eii.ExtensionObject())
    if view and view.ClassName() in ['SecLendClientView']:
        return True
    return False

def ContextCategoryInventoryView(eii):
    view = GetView(eii.ExtensionObject())
    if view and view.ClassName() in ['SecLendInventoryView']:
        return True
    return False


def ContextCategoryPortfolioView(eii):
    view = GetView(eii.ExtensionObject())
    if view and view.ClassName() in ['SecLendPortfolioView']:
        return True
    return False


class SecLendMenuItemBase(IntegratedWorkbenchMenuItem):
    """ Base class for all securities lending menu items """
    def __init__(self, extObj):
        super(SecLendMenuItemBase, self).__init__(extObj, None)

    def Enabled(self):
        view = self.View()
        if view and IsSecLendWorkbench(view.ClassName()):
            return self.EnabledFunction()
        return False

    def EnabledFunction(self):
        return True

    def _ViewName(self):
        view = self.View()
        return view.Name() if view else ''


class SecLendWorkbenchMenuItem(FUxCore.MenuItem, object):
    """ Base class for the workbench launcher menu items. """
    APP = None

    def __init__(self, extObj, view):
        self._frame = extObj
        self._view = view

    def View(self):
        return GetView(self._frame)

    def Enabled(self):
        return True

    def Settings(self):
        return ViewSettings(self._view)

    def Workbook(self):
        """ Get the view's workbook. First check for the main panel's
        workbook attribute, but if there is none - return the view's.
        """
        settings = self.Settings()
        if settings:
            try:
                if settings.Main().Workbook():
                    return acm.FWorkbook[settings.Main().Workbook()]
            except AttributeError:
                pass
            try:
                return acm.FWorkbook[settings.Workbook()]
            except AttributeError:
                pass
            return None

    @classmethod
    def SetApp(cls):
        try:
            str(cls.APP)
        except RuntimeError as e:
            cls.APP = None

    def getWindowText(self, hWnd):
        text_length = ctypes.windll.user32.GetWindowTextLengthW(hWnd)
        buff = ctypes.create_unicode_buffer(text_length + 1)
        ctypes.windll.user32.GetWindowTextW(hWnd, buff, text_length + 1)
        return str(buff.value)

    def Invoke(self, eii):
        """ Check if there is any instance of the view open to activate
            it, otherwise launch a new instance of the view.
        """
        cls = type(self)
        cls.SetApp()
        if cls.APP is None:
            # Add workbook checks if needed
            defaultWorkbook = self.Workbook()
            if defaultWorkbook:
                cls.APP = FindAppWithWorkbook(defaultWorkbook) or\
                acm.StartApplication(self.Settings().Application(), defaultWorkbook)
            else:
                cls.APP = LaunchView(self._view)
        cls.APP.Restore() #Restore minimized applications
        cls.APP.Activate()
        hWnd = ctypes.windll.user32.GetForegroundWindow()
        title = self.getWindowText(hWnd)
        ctypes.windll.user32.SetWindowTextA(hWnd, title.replace('Trading Manager',\
            self.Settings().ViewDisplayName()))

def FindAppWithWorkbook(workbook):
    for app in acm.ApplicationList():
        if app.IsKindOf(acm.FManagerBaseFrame):
            if app.ActiveWorkbook().StoredWorkbook() is workbook:
                return app

def LaunchViewWithName(viewId):
    settings = ViewSettings(viewId)
    view = FViewCreator.CreateView(viewId)
    app = DoStartApplication(settings)
    view.Application(app)
    FViewCreator.CreatePanelsForView(view, settings)
    if hasattr(settings, 'Handlers'):
        FHandlerCreator.CreateHandlers(settings.Handlers(), view.Dispatcher())
    return app

def DoStartApplication(settings):
    return NamedManagerBaseApplicationCreator(settings).CreateApplication()

class NamedManagerBaseApplicationCreator(ManagerBaseApplcationCreator):
    """ Custom instance of ApplicationCreator to be able to read a
    specified name from the view settings for a manager based application.
    """

    def _CreateApplication(self):
        app = self._StartApplication(self.GetSimulatedWorkbook())
        if self._HasSheets():
            uxWorkbook = app.ActiveWorkbook()
            for sheet in self._Sheets():
                if self.IsValid(sheet):
                    self.AddSheet(uxWorkbook, sheet)
            uxWorkbook.ActivateSheet(uxWorkbook.Sheets().First())
        return app

    def GetSimulatedWorkbook(self):
        wb = acm.FWorkbook()
        wb.Name(self._SimulatedWorkbookName())
        wb.Simulate()
        return wb

    def _SimulatedWorkbookName(self):
        try:
            return self.Settings().ViewDisplayName()
        except AttributeError:
            return self.Settings().Name()
