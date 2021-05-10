""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FCurrentActiveMarketMakerFilter.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FCurrentActiveMarketMakerFilter

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

from FCurrentActiveFilter import CurrentActiveFilter
from FCTSEvents import CTSOnFilterChanged, CTSOnFilterRemoved
from FEvent import EventCallback


class CurrentActiveMarketMakerFilter(CurrentActiveFilter):

    @EventCallback
    def CTSOnMarketMakerFilterCreated(self, event):
        self.CTSOnFilterCreated(event)

    @EventCallback
    def CTSOnMarketMakerFilterCleared(self, event):
        self.CTSOnFilterCleared(event)

    @EventCallback
    def CTSOnMarketMakerFilterActive(self, event):
        self.CTSOnFilterActive(event)

    def SendOnFilterChanged(self):
        event = self.CreateEvent('CTSOnMarketMakerFilterChanged', baseClass=CTSOnFilterChanged)
        self.SendEvent(event)

    def SendOnFilterRemoved(self):
        event = self.CreateEvent('CTSOnMarketMakerFilterRemoved', baseClass=CTSOnFilterRemoved)
        self.SendEvent(event)

    def HandleViewDestroyed(self, view):
        if view.ClassName() == 'MarketMakerView':
            self.ClearActiveFilter()
