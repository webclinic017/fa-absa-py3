""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FCurrentActiveFilter.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FCurrentActiveFilter

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

from FHandler import Handler

class CurrentActiveFilter(Handler):

    def __init__(self, dispatcher):
        super(CurrentActiveFilter, self).__init__(dispatcher)
        self._filter = None
        self._filterActive = False

    def FilterActive(self, active=None):
        if active is None:
            return self._filterActive
        self._filterActive = active

    def ActiveFilter(self, activeFilter=None):
        if activeFilter is None and self._filterActive:
            return self._filter
        else:
            return None

    def Filter(self, filterToSet=None):
        if filterToSet is None:
            return self._filter
        self._filter = filterToSet

    def ClearActiveFilter(self):
        self._filter = None
        self._filterActive = False

    def OnFilterCreated(self, event):
        self.Filter(event.Filter())
        self.FilterActive(True)
        self.SendOnFilterChanged()

    def OnFilterCleared(self, event):
        self.ClearActiveFilter()
        self.SendOnFilterRemoved()

    def OnFilterActive(self, event):
        self.FilterActive(event.FilterActive())
        if self.FilterActive() is True:
            self.SendOnFilterChanged()
        else:
            self.SendOnFilterRemoved()

    def SendOnFilterChanged(self):
        pass

    def SendOnFilterRemoved(self):
        pass

    def HandleViewDestroyed(self, view):
        self.ClearActiveFilter()
