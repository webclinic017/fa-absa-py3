""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendOrdersBlotterPanels.py"
"""--------------------------------------------------------------------------
MODULE
    FSecLendOrdersBlotterPanels

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Order Manager - Blotters for booked trades over various dates.

-----------------------------------------------------------------------------"""
import acm
from FEvent import EventCallback
from FSecLendCommon import InsertItemSheetPanel
from FSecLendEvents import OnOrderManagerTradesSelected
from DealPackageUtil import IsFObject
import FSecLendUtils
import FSecLendHooks

class SecLendOrdersBlotterPanelBase(InsertItemSheetPanel):

    def __init__(self):
        super(SecLendOrdersBlotterPanelBase, self).__init__()
        self._counterparty = None

    def DefaultInsertItemQuery(self):
        query = FSecLendHooks.ActiveLoansQuery()
        fromDate = self.Settings().FilterTradesFromDate()
        toDate = self.Settings().FilterTradesToDate()

        if fromDate and toDate:
            tradeDateNode = query.AddOpNode('AND')
            tradeDateNode.AddAttrNode('TradeTime', 'GREATER_EQUAL', fromDate)
            tradeDateNode.AddAttrNode('TradeTime', 'LESS_EQUAL', toDate)
        elif not fromDate and toDate:
            query.AddAttrNode('TradeTime', 'LESS_EQUAL', toDate)
        elif fromDate and not toDate:
            query.AddAttrNode('TradeTime', 'GREATER_EQUAL', fromDate)

        statuses = self.Settings().FilterTradeStatuses()
        FSecLendUtils.AddQueryAttrNodeList(query, 'Status', statuses)
        return query

    def ApplyAdditionalQueryFilters(self, query):
        if self._counterparty:
            query.AddAttrNodeString('Counterparty.Name', self._counterparty.Name(), 'EQUAL')
        return query

    @EventCallback
    def OnOrderManagerTradeFilterChanged(self, event):
        if self._counterparty != event.Counterparty():
            self._counterparty = event.Counterparty()
            self.UpdateSheetContents()

    def SelectionChanged(self, selection):
        rowObjects = selection.SelectedRowObjects()
        trades = self.GetTradesFromSelection(rowObjects)
        if trades:
            self.SendEvent(OnOrderManagerTradesSelected(self, trades))

    @classmethod
    def GetTradesFromSelection(cls, rowObjects):
        def GetTradesListFromObject(obj):
            if IsFObject(obj, acm.FTrade):
                alltrades.Add(obj)
            elif IsFObject(obj, acm.FTradeRow):
                alltrades.Add(obj.Trade())
            elif IsFObject(obj, acm.FPortfolioInstrumentAndTrades):
                GetTradesListFromObject(obj.Trades())
            elif IsFObject(obj, acm.FMultiInstrumentAndTrades):
                GetTradesListFromObject(obj.Trades())
            elif IsFObject(obj, acm.FCollection):
                for o in obj:
                    GetTradesListFromObject(o)
        alltrades = acm.FArray()
        if rowObjects:
            GetTradesListFromObject(rowObjects)
            return alltrades


class SecLendOrdersBlotterPositionsPanel(SecLendOrdersBlotterPanelBase):
    # TODO: All historical trades might cause performance issues

    def __init__(self):
        super(SecLendOrdersBlotterPositionsPanel, self).__init__()
        self._orders = []

    def ShowSheetContents(self):
        return bool(self._orders)

    def ApplyAdditionalQueryFilters(self, query):
        super(SecLendOrdersBlotterPositionsPanel, self).ApplyAdditionalQueryFilters(query)
        underlyings = (o.Instrument().Underlying().Name() for o in self._orders if o.Instrument().Underlying())
        FSecLendUtils.AddQueryAttrNodeList(query, 'Instrument.Underlying.Name', underlyings)
        return query

    @EventCallback
    def OnOrderManagerOrdersSelected(self, event):
        if self._orders != event.Orders():
            self._orders = event.Orders()
            self.UpdateSheetContents()
