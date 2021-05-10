""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/RiskCompliance/etc/FRiskComplianceOrdersPanel.py"
"""--------------------------------------------------------------------------
MODULE
    FRiskComplianceOrdersPanel

    (c) Copyright 2016 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""

import acm
from FSheetPanel import SheetPanel
from FRiskComplianceLogging import logger
import FEvent
import time

class RiskComplianceOrdersPanel(SheetPanel):

    def InitCustomControls(self, layout):
        self.Filter([])

    @FEvent.EventCallback
    def OnBusinessProcessSelected(self, event):
        try:
            id = event.BusinessProcess().Subject().OptionalId()
            self.Filter(id, startTime = event.BusinessProcess().CreateTime())
        except IndexError as e:
            logger.debug(e)
            self.Sheet().InsertObject(None)
        except AttributeError as e:
            logger.debug(e)
            self.Sheet().InsertObject(None)

    def FilterQuery(self, id):
        query = acm.CreateFASQLQuery('FOwnOrder', 'OR')
        if id:
            query.AddAttrNode('OrderProgramId', 'EQUAL', id)
            query.AddAttrNode('ParentOrder.OrderProgramId', 'EQUAL', id)
        if not query.AsqlNodes():
            query.AddAttrNode('OrderId', 'EQUAL', 'No ID just to filter out everything')
        return query

    def Filter(self, id, startTime = None):
        gridBuilder = self.Sheet().Sheet().GridBuilder()
        orderFilter = gridBuilder.GetFilter()
        orderFilter.Query(self.FilterQuery(id))
        orderFilter.OrderRoles(self.NumericOrderEnums('OrderRole', ['Order Program']))
        if startTime is not None:
            startDay = acm.GetFunction('time_to_day', 1)(startTime)
            daysBack = acm.Time.DateDifference(acm.Time.DateToday(), startDay)
            #The time is set as utc date time double, converted to days - and we want the time 00:00:00
            orderFilter.InactFromTime(time.timezone / 86400.0)
            orderFilter.InactFromDaysBack(daysBack)
        
        # Should be changed or revised
        orderFilter.Traders([])
        orderFilter.Changed()
        
        child = gridBuilder.RowTreeIterator().FirstChild()
        if child:
            child.Tree().Expand(True)
                   
    @staticmethod
    def NumericOrderEnums(enum, values):
        enumType = acm.FEnumeration[enum]
        return [enumType.Enumeration(value) for value in values]
