""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/ExecutionView/etc/FFilteredOrderPanel.py"
"""------------------------------------------------------------------------------------------------
MODULE
    FFilteredOrderPanel

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------"""

import acm
import FOrderUtils
from FSheetPanel import SheetPanel
from FMultiSheetPanel import MultiSheetPanel
from FEvent import EventCallback

class FilterOrderedPanelBase(object):
    
    def Query(self):
        return acm.CreateFASQLQuery('FOwnOrder', 'OR')
    
    def FilterOnIds(self, query, ids, idType):
        for oid in ids:
            query.AddAttrNode(idType, 'EQUAL', oid)
        if not query.AsqlNodes():
            query.AddAttrNode('OrderId', 'EQUAL', 'No ID just to filter out everything')
        return query

    def FilterOnOrderIds(self, query, ids):
        return self.FilterOnIds(query, ids, 'OrderId')
    
    def FilterOnParentOrderIds(self, query, ids):
        return self.FilterOnIds(query, ids, 'ParentOrder.OrderId')
    
    def FilterOnOrderProgramIds(self, query, ids):
        return self.FilterOnIds(query, ids, 'OrderProgramId')
    
    def FilterOnOrderRoles(self, orderFilter, roles):
        orderFilter.OrderRoles(FOrderUtils.NumericOrderEnums('OrderRole', roles))

class FilteredOrderPanel(SheetPanel, FilterOrderedPanelBase):

    def __init__(self):
        SheetPanel.__init__(self)
        
    def OrderFilter(self):
        orderFilter = self.Sheet().Sheet().GridBuilder().GetFilter()
        orderFilter.Traders([])
        return orderFilter

class FilteredOrderMultiSheetPanel(MultiSheetPanel, FilteredOrderPanel):

    def __init__(self):
        MultiSheetPanel.__init__(self)
        
    def OrderFilters(self):
        for sheet in self.Sheets():
            try:
                orderFilter = sheet.GridBuilder().GetFilter()
                orderFilter.Traders([])
            except AttributeError as e:
                pass
            else:
                yield orderFilter