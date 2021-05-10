""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/ExecutionView/etc/FEVBulkedOrdersPanel.py"
"""------------------------------------------------------------------------------------------------
MODULE
    FEVBulkedOrdersPanel

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------"""

import acm
import FOrderUtils
import FSheetUtils
from FFilteredOrderPanel import FilteredOrderMultiSheetPanel
from FEvent import EventCallback

class EVBulkedOrdersPanel(FilteredOrderMultiSheetPanel):

    def InitCustomControls(self, layout):
        self.Filter([])
    
    def OrderIds(self, orders):
        ids = []
        for order in orders:
            try:
                for o in FOrderUtils.AsOrderHandler(order).LinkedFromOrders() or []:
                    ids.append(o.OrderId())
            except (AttributeError, TypeError):
                continue
        return ids
    
    def Filter(self, orders):
        query = self.Query()
        self.FilterOnOrderIds(query, self.OrderIds(orders))
        for orderFilter in self.OrderFilters():
            orderFilter.Query(query)
            self.FilterOnOrderRoles(orderFilter, ['Sales Order', 'Order Program Sales Order'])
            orderFilter.Changed()

    @EventCallback
    def OnRowSelectionChanged(self, event):
        orders = FSheetUtils.SelectedOrders(event.First())
        self.Filter(orders)
        self._TradeSheet().RemoveAllRows()
        
    def _OrderSheet(self):
        return self._GetSheetByIndex(0)

    def _TradeSheet(self):
        return self._GetSheetByIndex(1)

    def _SendSheetChanged(self, sheet):
        if sheet == self._OrderSheet():
            tradeSheet = self._TradeSheet()
            tradeSheet.RemoveAllRows()
            selection = sheet.Selection()
            if selection:
                self._InsertTradeFolder(tradeSheet, selection)

    def _InsertTradeFolder(self, sheet, selection):
        sheet.InsertObject(None, 'IOAP_REPLACE')
        for order in selection.SelectedOrders():
            folder = self._TradeFolder(order)
            sheet.InsertObject(folder, 'IOAP_LAST')

    def _TradeFolder(self, order):
        if order.OrderId():
            folder = acm.FASQLQueryFolder()
            query = acm.CreateFASQLQuery('FTrade', 'OR')
            query.AddAttrNode('OrderUuid', 'EQUAL', order.OrderId())
            folder.AsqlQuery(query)
            folder.Name(str(order))
            return folder