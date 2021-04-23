""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/PortfolioTrading/etc/FTradeProgramLimitPanel.py"
"""--------------------------------------------------------------------------
MODULE
    FTradeProgramLimitPanel

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
Panel that displays changes in states on predeal limits
-----------------------------------------------------------------------------"""
import FSheetUtils
from FSheetPanel import SheetPanel
from FEvent import EventCallback

class TradeProgramLimitPanel(SheetPanel):

    COLUMNS = [
        'Limit Checked Value',
        'Limit Current State'
        ]

    def __init__(self):
        super(TradeProgramLimitPanel, self).__init__()

    def ReactOnEvent(self):
        return True

    @EventCallback
    def OnCandidateTradesCleared(self, event):
        self._RemoveSimulation()
        self._RemoveAllRowsAndHide()

    @EventCallback
    def OnLimitsChecked(self, event):
        limitsResults = event.LimitsResults()
        if limitsResults:
            self.Visible(True)
            self._InsertAsFolder(list(limitsResults.keys()), 'Limits Changing State')
            self._SimulateValues(limitsResults)
        else:
            self._RemoveAllRowsAndHide()

    @EventCallback
    def OnTradeProgramLimitMonitor(self, event):
        self._RemoveAllRows()
        relevantLimits = event.TradeProgramLimitMonitor().RelevantLimits()
        self._InsertAsFolder(relevantLimits)

    def _RemoveSimulation(self):
        if self.Sheet():
            rowTreeIterator = self.Sheet().RowTreeIterator(0)
            while rowTreeIterator.NextUsingDepthFirst():
                limit = rowTreeIterator.Tree().Item()
                for columnId in self.COLUMNS:
                    FSheetUtils.UnsimulateCell(self.Sheet(), limit, columnId)

    def _InsertAsFolder(self, limits, folderName='Limits'):
        if self.Sheet():
            folder = FSheetUtils.GetObjectsAsFolder(limits, folderName)
            self.Sheet().InsertObject(folder, 'IOAP_REPLACE')
            self.Sheet().ExpandTree()
            self.Sheet().GridBuilder().Refresh()

    def _RemoveAllRowsAndHide(self):
        try:
            self._RemoveAllRows()
            self.Visible(False)
        except RuntimeError:
            pass

    def _RemoveAllRows(self):
        try:
            self.Sheet().RemoveAllRows()
        except AttributeError:
            pass

    def _SimulateValues(self, limits, unsimulate=False):
        for limit, result in limits.items():
            FSheetUtils.SimulateCell(self.Sheet(), limit, self.COLUMNS[0],
                                     None if unsimulate else result.CheckedValue)
            FSheetUtils.SimulateCell(self.Sheet(), limit, self.COLUMNS[1],
                                     None if unsimulate else result.StateAfter)

