""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FCTSBondWorkbookPanel.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FCTSBondWorkbookPanel

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import FSheetUtils

from FCTSEvents import CTSBondsSelected
from FEvent import EventCallback
from FFilteredWorkbookPanel import FilteredWorkbookPanel


class CTSBondWorkbookPanel(FilteredWorkbookPanel):

    def __init__(self, application):
        super(CTSBondWorkbookPanel, self).__init__(application)
        self._treeConfigurationsDict = {}

    def RowSelectionChanged(self, selection):
        selection = FSheetUtils.SelectedInstruments(selection)
        self.SendEvent(CTSBondsSelected(self, selection))

    @EventCallback
    def CTSBondNavigationChanged(self, event):
        treeConfiguration = FSheetUtils.TreeConfiguration
        self._treeConfigurationsDict = dict((ins.StringKey(), treeConfiguration(ins)) for ins in event.Objects())
        self.InsertObjects(self._treeConfigurationsDict.values())

    @EventCallback
    def CTSOnWatchlistFilterChanged(self, event):
        self.OnFilterChanged(event)

    @EventCallback
    def CTSOnWatchlistFilterRemoved(self, event):
        self.OnFilterRemoved(event)

    @EventCallback
    def CTSOnWatchlistFilterRefreshed(self, event):
        self.OnFilterRefreshed(event)

    def SourceObject(self, rowObject):
        return self._treeConfigurationsDict.get(rowObject.StringKey())

    @staticmethod
    def SortingKey(obj):
        try:
            return obj.TreeSpecification().OriginObject().Name()
        except Exception:
            return obj
