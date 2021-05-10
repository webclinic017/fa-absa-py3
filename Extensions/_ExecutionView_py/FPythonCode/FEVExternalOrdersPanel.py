""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/ExecutionView/etc/FEVExternalOrdersPanel.py"
"""------------------------------------------------------------------------------------------------
MODULE
    FEVExternalOrdersPanel

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------"""

import FSheetUtils
from FFilteredOrderPanel import FilteredOrderPanel
from FEvent import EventCallback

class EVExternalOrdersPanel(FilteredOrderPanel):
    
    ORDER_ROLES = ['Moved Order', 'Execution Order']
    
    def InitCustomControls(self, layout):
        self.Filter([])
    
    def OrderIds(self, orders):
        return [order.OrderId() for order in orders
                if order.OrderRole() in self.ORDER_ROLES]
                
    def ParentOrderIds(self, orders):
        return [order.OrderId() for order in orders
                if not order.OrderRole() in self.ORDER_ROLES] 
    
    def Filter(self, orders):
        query = self.Query()
        self.FilterOnOrderIds(query, self.OrderIds(orders))
        self.FilterOnParentOrderIds(query, self.ParentOrderIds(orders))
        orderFilter = self.OrderFilter()
        orderFilter.Query(query)
        self.FilterOnOrderRoles(orderFilter, self.ORDER_ROLES)
        orderFilter.Changed()
        
    @EventCallback
    def OnRowSelectionChanged(self, event):
        orders = FSheetUtils.SelectedOrders(event.First())
        self.Filter(orders)

