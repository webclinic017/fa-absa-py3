""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FCurrentActiveWatchlistFilter.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FCurrentActiveWatchlistFilter

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

from FCurrentActiveFilter import CurrentActiveFilter
from FCTSEvents import CTSOnFilterChanged, CTSOnFilterRemoved
from FEvent import EventCallback


class CurrentActiveWatchlistFilter(CurrentActiveFilter):

    @EventCallback
    def CTSOnWatchlistFilterCreated(self, event):
        self.CTSOnFilterCreated(event)

    @EventCallback
    def CTSOnWatchlistFilterCleared(self, event):
        self.CTSOnFilterCleared(event)

    @EventCallback
    def CTSOnWatchlistFilterActive(self, event):
        self.CTSOnFilterActive(event)

    def SendOnFilterChanged(self):
        event = self.CreateEvent('CTSOnWatchlistFilterChanged', baseClass=CTSOnFilterChanged)
        self.SendEvent(event)

    def SendOnFilterRemoved(self):
        event = self.CreateEvent('CTSOnWatchlistFilterRemoved', baseClass=CTSOnFilterRemoved)
        self.SendEvent(event)

    def HandleViewDestroyed(self, view):
        if view.ClassName() == 'BondView':
            self.ClearActiveFilter()
