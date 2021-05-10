""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/PortfolioTrading/etc/FClosePositionTM.py"
"""--------------------------------------------------------------------------
MODULE
    FClosePositionTM

    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""
from FClosePosition import FClosePosition
from FTradeProgramTM import FTradeProgramTM
from FParameterSettings import ParameterSettingsCreator
from FTradeProgramMenuItem import TradeProgramActionMenuItem
from FTradeProgramAction import Action, OpenPositionAction


@Action
def ClosePosition(eii):
    return ClosePositionMenuItem(eii)

class ClosePositionMenuItem(TradeProgramActionMenuItem):

    def __init__(self, extObj):
        TradeProgramActionMenuItem.__init__(self, extObj)

    def InvokeAsynch(self, eii):
        closePosition = FClosePositionTM(eii)
        closePosition.Execute()
        
    def Action(self):
        return OpenPositionAction('ClosePosition')

class FClosePositionTM(FTradeProgramTM):

    def __init__(self, eii):
        self._settings = ParameterSettingsCreator.FromRootParameter('ClosePositionSettings')
        FTradeProgramTM.__init__(self, eii, action=OpenPositionAction('ClosePosition'))

    def Execute(self, trades=None):
        closePosition = FClosePosition(
            self.InstrumentRows(),
            self._settings.ColumnId())
        FTradeProgramTM.Execute(self, closePosition.Trades())
        
