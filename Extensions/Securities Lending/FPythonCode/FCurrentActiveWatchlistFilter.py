""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FCurrentActiveWatchlistFilter.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FCurrentActiveWatchlistFilter

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
from FEvent import EventCallback
from FSecLendEvents import OnFilterChanged, OnFilterRemoved
from FCurrentActiveFilter import CurrentActiveFilter

class CurrentActiveWatchlistFilter(CurrentActiveFilter):

    @EventCallback
    def OnWatchlistFilterCreated(self, event):
        self.OnFilterCreated(event)

    @EventCallback
    def OnWatchlistFilterCleared(self, event):
        self.OnFilterCleared(event)

    @EventCallback
    def OnWatchlistFilterActive(self, event):
        self.OnFilterActive(event)

    def SendOnFilterChanged(self):
        event = self.CreateEvent('OnWatchlistFilterChanged', baseClass=OnFilterChanged)
        self.SendEvent(event)

    def SendOnFilterRemoved(self):
        event = self.CreateEvent('OnWatchlistFilterRemoved', baseClass=OnFilterRemoved)
        self.SendEvent(event)

    def HandleViewDestroyed(self, view):
        if view.ClassName() == 'SecLendPortfolioView':
            self.ClearActiveFilter()
