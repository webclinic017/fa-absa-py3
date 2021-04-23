""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/PortfolioTrading/etc/FTradeProgramSessionMenuItem.py"
"""-------------------------------------------------------------------------------------------------
MODULE
    FTradeProgramSessionMenuItem

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------"""
from itertools import chain

import acm
import FIntegratedWorkbench
import FRunScriptGUI
import FUxCore
import FEvent
from FTradeProgramMenuItem import TradeProgramMenuItem, ToggleParameterMenuItem
from FIntegratedWorkbenchLogging import logger
from FViewUtils import ViewSettings
from FSheetUtils import GetWorkbook, FindAppWithWorkbook
from FTradeProgramEvents import (OnTradeProgramActionCleared,
                                 OnIncludeCandidateChanged,
                                 OnTradeProgramExport,
                                 OnOrdersCreatedFromCandidateTrades
                                )
try:
    import FAlertGenerator
    import FComplianceRulesUtils
    COMPLIANCE_RULE_MODULE_LOADED = True
except ImportError:
    COMPLIANCE_RULE_MODULE_LOADED = False

    
def ClearTradeProgram(eii):
    return ClearTradeProgramMenuItem(eii)

def ExportToFile(eii):
    return ExportToFileMenuItem(eii)

def LaunchTradeProgramView(eii):
    return TradeProgramViewMenuItem(eii)

def IncludeCandidateTrades(eii):
    return IncludeCandidateMenuItem(eii)

def RestrictToLimits(eii):
    return ToggleParameterMenuItem(eii, parameterName='Restrict Program To Limits')

def LocalLimitCheck(eii):
    return LocalLimitCheckMenuItem(eii)

def QuickMode(eii):
    return QuickModeMenuItem(eii)

def CreateOrders(eii):
    return CreateOrdersMenuItem(eii)


class CreateOrdersMenuItem(TradeProgramMenuItem):

    def __init__(self, extObj):
        TradeProgramMenuItem.__init__(self, extObj)

    def EnabledFunction(self):
        return bool(self._CurrentActiveCandidateTrades())

    def InvokeAsynch(self, _eii):
        try:
            self._Dispatcher().Update(OnOrdersCreatedFromCandidateTrades(self))
        except Exception as e:
            logger.error(e, exc_info=True)

    def Invoke(self, eii):
        self.InvokeAsynch(eii)


class ClearTradeProgramMenuItem(TradeProgramMenuItem):

    def __init__(self, extObj):
        TradeProgramMenuItem.__init__(self, extObj)

    def InvokeAsynch(self, _eii):
        self._Dispatcher().Update(OnTradeProgramActionCleared(self))

    def Invoke(self, eii):
        self.InvokeAsynch(eii)


class ExportToFileMenuItem(TradeProgramMenuItem):

    def __init__(self, extObj):
        TradeProgramMenuItem.__init__(self, extObj)

    def EnabledFunction(self):
        return bool(self._CurrentActiveCandidateTrades())

    @staticmethod
    def FileSelection():
        fileFilters = ('CSV Files (*.csv)|*.csv',
                       'Text Files (*.txt)|*.txt',
                       'All Files (*.*)|*.*')
        return FRunScriptGUI.OutputFileSelection('|'.join(fileFilters))

    def InvokeAsynch(self, _eii):
        selection = self.FileSelection()
        if acm.UX.Dialogs().BrowseForFile(self._frame.Shell(), selection):
            path = str(selection.SelectedFile())
            self._Dispatcher().Update(OnTradeProgramExport(self, path))


class IncludeCandidateMenuItem(TradeProgramMenuItem):

    def __init__(self, extObj):
        TradeProgramMenuItem.__init__(self, extObj)

    def Checked(self):
        try:
            return self._CurrentActiveCandidateTradesHandler().IncludeCandidateTrades()
        except AttributeError:
            return False

    def EnabledFunction(self):
        try:
            return bool(self._CurrentActiveCandidateTrades())
        except AttributeError:
            return True

    def InvokeAsynch(self, _eii):
        self._Dispatcher().Update(OnIncludeCandidateChanged(self, not self.Checked()))


class LocalLimitCheckMenuItem(TradeProgramMenuItem):
    
    def EnabledFunction(self):
        return bool(self._CurrentActiveCandidateTrades())
        
    def InvokeAsynch(self, _eii):
        if COMPLIANCE_RULE_MODULE_LOADED:
            self._RunComplianceCheck()
        else:
            msg = 'Module Compliance Rules must be in context in order to do local complance checks'
            acm.UX.Dialogs().MessageBoxInformation(self._frame.Shell(), msg) 
    
    def _RunComplianceCheck(self):
        appliedRules = self._RelevantAppliedRules()
        alerts = self._Alerts(appliedRules)
        if alerts:
            dlg = FComplianceRulesUtils.AlertSheetDialog(alerts)
            builder = dlg.CreateLayout()
            acm.UX.Dialogs().ShowCustomDialog(self._frame.Shell(), builder, dlg)
        else:
            msg = 'Compliance check OK'
            acm.UX.Dialogs().MessageBoxInformation(self._frame.Shell(), msg) 

    def _Alerts(self, appliedRules):
        alerts = []
        for appliedRule in appliedRules:
            alertGenerator = FAlertGenerator.Create(appliedRule)
            checkResult = appliedRule.Check()
            alerts.append(alertGenerator.AlertsFromCheck(checkResult))
        return alerts
    
    def _RelevantAppliedRules(self):
        trades = self._CurrentActiveCandidateTrades()
        portfolios = FComplianceRulesUtils.AllPortfoliosForTrades(trades)
        return chain.from_iterable(FComplianceRulesUtils.GetAppliedRules(portfolio) for portfolio in portfolios)
    
    
class QuickModeMenuItem(ToggleParameterMenuItem):
    
    def __init__ (self, extObj):
        super(QuickModeMenuItem, self).__init__(extObj, parameterName='QuickMode')
                                                        


class TradeProgramViewMenuItem(FUxCore.MenuItem, object):
    
    APP = None

    def __init__(self, extObj, view='TradeProgramView'):
        self._frame = extObj
        self._view = view

    def Enabled(self):
        return self._frame.IsKindOf(acm.FSessionManagerFrame)
    
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

    @staticmethod
    def _ModulesNotInContext():
        modules = {'Deal Package':'FreeForm'}
        for extModule, module in modules.items():
            try:
                __import__(module)
            except ImportError:
                yield extModule

    def Invoke(self, _eii):
        missingModules = list(self._ModulesNotInContext())
        if missingModules:
            msg = ('Required module(s) {0} missing from context. Portfolio Trading '
                   'will not work.'.format(','.join(m for m in missingModules)))
            acm.UX.Dialogs().MessageBox(self._frame.Shell(), 'Error', msg, 'OK',
                                        None, None, 'Button1', 'Button1')
        else:
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
