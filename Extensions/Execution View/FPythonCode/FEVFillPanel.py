""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/ExecutionView/etc/FEVFillPanel.py"
"""------------------------------------------------------------------------------------------------
MODULE
    FEVFillPanel

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------"""

import acm
from FSheetPanel import SheetPanel
from FEvent import EventCallback

class EVFillPanel(SheetPanel):

    @EventCallback
    def OnRowSelectionChanged(self, event):
        try:
            order = event.First().SelectedRowObjects().First()
            if order.OrderId():
                self.Sheet().InsertObject(self._TradeQuery(order))
        except Exception:
            pass

    @staticmethod
    def _TradeQuery(order):
        folder = acm.FASQLQueryFolder()
        query = acm.CreateFASQLQuery('FTrade', 'OR')
        if order.OrderRole() == 'Execution Order':
            trades = acm.Trading.DefaultTradingSession().AttachOrder(order).MarketTrades()
            if not trades:
                return None
            for mktTrade in trades:
                query.AddAttrNode('OptionalKey', 'EQUAL', mktTrade.OptionalKey())
        else:
            query.AddAttrNode('OrderUuid', 'EQUAL', order.OrderId())
        folder.AsqlQuery(query)
        folder.Name(str(order))
        return folder