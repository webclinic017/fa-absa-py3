""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BuySideOMS/./etc/FAllocationLinker.py"
"""--------------------------------------------------------------------------
MODULE
    FAllocationlinker

    (c) Copyright 2016 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Used for manually linking trades that were creted externally as part of an allocation scheme
-----------------------------------------------------------------------------"""

import acm

class AllocationLinker(object):
    
    ALLOCATION_SCHEME_NAME = 'AutoShape'
    ALLOCATION_DIMENSION_NAME = 'AutoShapeDimension'
    
    def __init__(self, trade):
        self._trade = trade
    
    def CreateAllocationForMasterTrade(self):
        if not self._AlreadyPartOfAllocation(self._trade):
            self._LinkToBusinessEvent(self._trade, self._NewBusinessEvent())
            self._LinkToAllocationScheme(self._trade, self._AllocationScheme())
        
    def LinkToMasterTrade(self, masterTrade):
        if not self._AlreadyPartOfAllocation(self._trade):
            self._LinkToBusinessEvent(self._trade, self._BusinessEventFromTrade(masterTrade))
    
    def _AllocationScheme(self):
        template = acm.FAllocationScheme[self.ALLOCATION_SCHEME_NAME] or self._NewAllocationScheme()
        return acm.Allocation.DeepCopyScheme(template)

    @staticmethod
    def _BusinessEventFromTrade(trade):
        return trade.ConnectedTrade().BusinessEvents('Allocation')[0]
    
    @staticmethod
    def _LinkToBusinessEvent(trade, event):
        link = acm.FBusinessEventTradeLink()
        link.BusinessEvent(event)
        link.Trade(trade)
        link.Commit()
    
    @staticmethod
    def _LinkToAllocationScheme(trade, allocationScheme):
        link = allocationScheme.LinkTo(trade)
        link.Commit()
    
    @staticmethod
    def _NewBusinessEvent():
        event = acm.FBusinessEvent()
        event.EventType('Allocation')
        event.Commit()
        return event
    
    @staticmethod
    def _AlreadyPartOfAllocation(trade):
        return bool(trade.BusinessEvents('Allocation'))
        
    @classmethod
    def _NewAllocationDimension(cls):
        dimension = acm.FAllocationDimension()
        dimension.Name(cls.ALLOCATION_DIMENSION_NAME)
        dimension.Type('Portfolio')
        dimension.Commit()
        return dimension
    
    @classmethod
    def _NewAllocationScheme(cls):
        scheme = acm.FAllocationScheme()
        scheme.Name(cls.ALLOCATION_SCHEME_NAME)
        scheme.FunctionName('Pro Rata')
        scheme.Dimension(acm.FAllocationDimension[cls.ALLOCATION_DIMENSION_NAME] or
                         cls._NewAllocationDimension())
        scheme.IsTemplate(True)
        scheme.Commit()
        return scheme
    
