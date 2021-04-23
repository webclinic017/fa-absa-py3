""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/PortfolioTrading/etc/FTradeProgramMenuItem.py"
"""-------------------------------------------------------------------------------------------------
MODULE
    FTradeProgramMenuItem

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Contains base classes that are used by other menu items in Portfolio Trading
-------------------------------------------------------------------------------------------------"""

import acm
import FSheetUtils

from FTradeProgramEvents import OnTradeProgramActionInvoked
from FIntegratedWorkbenchMenuItem import IntegratedWorkbenchMenuItem
from FParameterSettings import ParameterSettingsCreator
from FCurrentActiveCandidateTrades import CurrentActiveCandidateTrades
from FIntegratedWorkbench import GetHandler, GetView

class TradeProgramMenuItem(IntegratedWorkbenchMenuItem):

    def __init__(self, extObj):
        super(TradeProgramMenuItem, self).__init__(extObj,
                                                   view='TradeProgramView')

    def _CurrentActiveCandidateTrades(self):
        try:
            return self._CurrentActiveCandidateTradesHandler().CandidateTrades()
        except AttributeError:
            return None

    def _CurrentActiveCandidateTradesHandler(self):
        return GetHandler(self.View(), CurrentActiveCandidateTrades)

class TradeProgramActionMenuItem(TradeProgramMenuItem):

    def __init__(self, extObj):
        TradeProgramMenuItem.__init__(self, extObj)
        self._settings = None
        self._selection = None

    def Settings(self):
        return self._settings

    def Sheet(self):
        return self._frame.ActiveSheet()

    def EnabledFunction(self):
        return (bool(self._Selection().Size()) and
                bool(self.Sheet().SheetClass() is acm.FPortfolioSheet))

    def _Selection(self):
        try:
            return self.Sheet().Selection().SelectedRowObjects()
        except Exception:
            return acm.FArray()

    def _InsertColumn(self, columnId):
        FSheetUtils.AddColumn(self.Sheet(), columnId)

    def Action(self):
        return None

    def InvokeAsynch(self, _eii):
        raise NotImplementedError

    def Invoke(self, eii):
        self._Dispatcher().Update(OnTradeProgramActionInvoked(self, self.Action()))
        self._frame.Shell().CallAsynch(self.InvokeAsynch, eii)


class ToggleParameterMenuItem(TradeProgramMenuItem):

    NO = 'No'
    YES = 'Yes'

    def __init__(self, extObj, parameterName, event=None, refresh=False,
                 parameterExtension='TradeProgramSettings'):
        TradeProgramMenuItem.__init__(self, extObj)
        self._settings = ParameterSettingsCreator.FromRootParameter(parameterExtension)
        self._parameterName = str(parameterName).replace(' ', '')
        self.refresh = refresh
        self._event = event

    def ReadParameter(self):
        return getattr(self._settings, self._parameterName)()

    def IsYes(self):
        return self.ReadParameter()

    def SetParameter(self, value):
        getattr(self._settings, self._parameterName)(value)
        self._settings.Commit()

    def ToggleParameter(self):
        self.SetParameter(self.NO if self.IsYes() else self.YES)

    def InvokeAsynch(self, _eii):
        self.ToggleParameter()
        if self.refresh:
            event = self._event(self.IsYes())
            self._Dispatcher().Update(event)

    def Checked(self):
        return self.IsYes()


def ContextCategory(eii):
    view = GetView(eii.ExtensionObject())
    return view and view.ClassName() == 'TradeProgramView'
