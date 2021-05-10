""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/PortfolioTrading/etc/FFutureRollTM.py"
"""--------------------------------------------------------------------------
MODULE
    FFutureRollTM

    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""
import acm
from FFutureRoll import FFutureRoll
from FTradeProgramTM import FTradeProgramTM
from FParameterSettings import ParameterSettingsCreator
from FTradeProgramMenuItem import TradeProgramActionMenuItem
from FTradeProgramAction import Action, RebalancingAction

@Action
def FutureRoll(eii):
    return FutureRollMenuItem(eii)

class FutureRollMenuItem(TradeProgramActionMenuItem):

    def __init__(self, extObj):
        TradeProgramActionMenuItem.__init__(self, extObj)

    def InvokeAsynch(self, eii):
        roll = FFutureRollTM(eii)
        roll.Execute()

    def _IsFutureSelected(self):
        for row in self._Selection():
            try:
                for ins in row.Instruments():
                    if ins.IsKindOf(acm.FFuture):
                        return True
            except AttributeError:
                continue
        return False

    def Enabled(self):
        return super(FutureRollMenuItem, self).Enabled() and self._IsFutureSelected()

class FFutureRollTM(FTradeProgramTM):

    def __init__(self, eii):
        self.frame = None
        self._settings = ParameterSettingsCreator.FromRootParameter('FutureRollSettings')
        FTradeProgramTM.__init__(self, eii,
                                 action=RebalancingAction(self._settings.Action()),
                                 inputColumn=self._settings.InputColumnId(),
                                 name='Future Roll')

    def Execute(self, trades=None):
        rowsAndInputs = self.RowsInputsAndCurrency(asString=True)
        roll = FFutureRoll(rowsAndInputs, self._settings.TargetColumnId())
        FTradeProgramTM.Execute(self, roll.Trades())
