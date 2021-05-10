""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/PortfolioTrading/etc/FTradeProgramOrderPanel.py"
"""--------------------------------------------------------------------------
MODULE
    FTradeProgramOrderPanel

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Order Sheet that displays the current orders for the selected Trade Program
-----------------------------------------------------------------------------"""

import acm
from FSheetPanel import SheetPanel
from FEvent import EventCallback
import time

class TradeProgramOrderPanel(SheetPanel):
    
    def InitCustomControls(self, layout):
        self.Filter()
        
    def ReactOnEvent(self):
        return True

    @EventCallback
    def OnOrdersSuccessfullyCreated(self, event):
        if not self.IsVisible():
            self.Visible(True)
        self.Refresh()
    
    def Refresh(self):
        self.Sheet().Sheet().GridBuilder().GetFilter().Changed()
    
    def FilterQuery(self):
        return acm.CreateFASQLQuery('FOwnOrder', 'OR')
    
    def Filter(self):
        orderRoles = self.NumericOrderEnums('OrderRole', ['Order Program'])
        orderFilter = self.Sheet().Sheet().GridBuilder().GetFilter()
        orderFilter.Query(self.FilterQuery())
        orderFilter.OrderRoles(orderRoles)
        orderFilter.Traders([acm.User()])
        #The time is set as utc date time double, converted to days - and we want the time 00:00:00
        orderFilter.ActFromTime(time.timezone / 86400.0)
        orderFilter.ActFromDaysBack(0)
        orderFilter.Changed()
    
    @staticmethod
    def NumericOrderEnums(enum, values):
        enumType = acm.FEnumeration[enum]
        return [enumType.Enumeration(value) for value in values]