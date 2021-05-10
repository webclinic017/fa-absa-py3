""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FTradeTableEventAdapter.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FTradeTableEventAdapter

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import FCTSEvents
import acm

from FHandler import Handler
from FSalesTradingTradeListener import SalesTradingTradeListener

class TradeTableEventAdapter(SalesTradingTradeListener, Handler):

    def __init__(self, dispatcher):
        SalesTradingTradeListener.__init__(self)
        Handler.__init__(self, dispatcher)
        self._rootPageGroup = None
        self.HandleViewCreated()

    def RootPageGroup(self):
        if self._rootPageGroup is None:
            self._rootPageGroup = acm.FPageGroup[self.Settings().RootPageGroupName()]
        return self._rootPageGroup

    def HandleViewCreated(self):
        self.StartSubscription()

    def HandleViewDestroyed(self, _view):
        self.EndSubscription()

    # ---- Methods overriden from SalesTradingTradeListener ----

    def _OnTrade(self, acmTrade, event):
        if (self.RootPageGroup() != None) and (acmTrade.Instrument() != None):
            if self.RootPageGroup().IncludesRecursively(acmTrade.Instrument()):
                self.SendEvent(FCTSEvents.OnTrade(self, acmTrade))
