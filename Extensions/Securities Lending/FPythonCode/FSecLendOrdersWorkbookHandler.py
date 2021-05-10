""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendOrdersWorkbookHandler.py"
"""--------------------------------------------------------------------------
MODULE
    FSecLendOrdersWorkbookHandler

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Order Manager - Workbench event handler/dispatcher.

-----------------------------------------------------------------------------"""
from FHandler import Handler
from FEvent import EventCallback


class SecLendOrdersWorkbookHandler(Handler):

    def __init__(self, dispatcher):
        super(SecLendOrdersWorkbookHandler, self).__init__(dispatcher)
        self._trade = None
        self._trades = None

    def Trade(self):
        return self._trade

    def Trades(self):
        return self._trades

    @EventCallback
    def OnOrderManagerOrdersSelected(self, event):
        self._trades = event.Orders()


class SecLendOrderManagerTradesHandler(Handler):

    def __init__(self, dispatcher):
        super(SecLendOrderManagerTradesHandler, self).__init__(dispatcher)
        self._trades = None

    def Trades(self):
        return self._trades

    @EventCallback
    def OnOrderManagerTradesSelected(self, event):
        self._trades = event.Trades()