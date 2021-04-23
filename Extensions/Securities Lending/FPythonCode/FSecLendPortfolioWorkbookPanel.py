""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendPortfolioWorkbookPanel.py"
from __future__ import print_function
"""------------------------------------------------------------------------------------------------
MODULE
    FSecLendPortfolioWorkbookPanel

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Portfolio View - Main workbook panel.

------------------------------------------------------------------------------------------------"""
import traceback
import acm
from FSecLendEvents import OnPositionSelection
from FFilteredWorkbookPanel import FilteredWorkbenchSheet
from FWorkbookPanel import DefaultWorkbookPanel
from FEvent import EventCallback
import FSecLendHooks

class SecLendPortfolioWorkbookPanel(DefaultWorkbookPanel):
    
    def RowSelectionChanged(self, selection):
        self.SendEvent(OnPositionSelection(self, selection.SelectedRowObjects()))
    
    
class MasterSecLoanSheet(FilteredWorkbenchSheet):

    ON_IDLE_FREQ = 0.5

    def __init__(self, workbookPanel, settings):
        try:
            super(MasterSecLoanSheet, self).__init__(workbookPanel, settings)
            self._secLoanSheetCache = {}
            self.UpdateSheetCache()
        except Exception:
            print("MasterSecLoanSheet", traceback.format_exc())

    def UpdateSheetCache(self):
        contents = self.GetSheetContents()
        self._secLoanSheetCache = dict(
                (trade.Instrument().Name(), trade) for trade in contents.Query().Select())
        self.SourceObjects(self._secLoanSheetCache.values())
        return contents

    @EventCallback
    def OnWatchlistFilterChanged(self, event):
        if self.IsSheetActive():
            self.OnFilterChanged(event)

    @EventCallback
    def OnWatchlistFilterRemoved(self, event):
        if self.IsSheetActive():
            self.OnFilterRemoved(event)

    @EventCallback
    def OnWatchlistFilterRefreshed(self, event):
        if self.IsSheetActive():
            self.OnFilterRefreshed(event)

    def SourceObject(self, rowObject):
        return self._secLoanSheetCache.get(rowObject.StringKey())

    def DefaultInsertItemQuery(self):
        return FSecLendHooks.MasterSecurityLoansQuery()

    def QueryFolderLabel(self):
        try:
            return FSecLendHooks.DefaultPortfolio().Name()
        except AttributeError:
            return 'No portfolio'
