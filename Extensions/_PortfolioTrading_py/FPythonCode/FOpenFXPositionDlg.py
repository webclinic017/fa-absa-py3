""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/PortfolioTrading/etc/FOpenFXPositionDlg.py"
"""--------------------------------------------------------------------------
MODULE
    FOpenFXPositionDlg

    (c) Copyright 2016 FIS Global. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""

import acm
from FTradeCreator import FXTradeFromTreeSpecCreator

FXPOSITION_APP = 'FXPositionApplication'

def StartDialog(eii, trade):
    shell = eii.ExtensionObject().Shell()
    initData = acm.DealCapturing().UX().InitDataFromTemplate(trade, FXPOSITION_APP)
    return acm.DealCapturing().UX().InstrumentDefinitionDialog(shell, initData, "Ok")
       

class OpenFXPositionDlg():

    def __init__(self, eii, spec=None):
        self._spec = spec
        self._trade = self._InitTrade()
        self._eii=eii
                
    def Trades(self):
        trades = []
        trade = self.CreateTrade()
        trades.append(trade)
        farTrade = trade.FxSwapFarLeg()
        if farTrade:
            trades.append(farTrade)
        return trades

    def CreateTrade(self):
        return StartDialog(self._eii, self.Trade())

    def TreeSpec(self):
        return self._spec

    def Trade(self):
        return self._trade

    def _InitTrade(self):
        try:
            _constObj = self.TreeSpec().Constraints().ConstraintDenominatorObject()
            if self._IsFXSpec(_constObj):
                return FXTradeFromTreeSpecCreator(self.TreeSpec()).CreateTrade()
        except Exception:
            pass

    def _IsFXSpec(self, _constObj):
        return True if _constObj.IsKindOf(acm.FFxRate) else False
