""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FCTSMarketMakerWorkbookPanel.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FCTSMarketMakerWorkbookPanel

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import FSheetUtils

from FCTSEvents import CTSMarketMakerQuoteSelected
from FEvent import EventCallback
from FFilteredWorkbookPanel import FilteredWorkbookPanel


class CTSMarketMakerWorkbookPanel(FilteredWorkbookPanel):

    def RowSelectionChanged(self, selection):
        selection = FSheetUtils.SelectedInstruments(selection)
        self.SendEvent(CTSMarketMakerQuoteSelected(self, selection, None))

    @EventCallback
    def CTSMarketMakerNavigationChanged(self, event):
        orderbooks = FSheetUtils.OrderBooks(event.Objects())
        self.InsertObjects(orderbooks)

    @EventCallback
    def CTSOnMarketMakerFilterChanged(self, event):
        self.OnFilterChanged(event)

    @EventCallback
    def CTSOnMarketMakerFilterRemoved(self, event):
        self.OnFilterRemoved(event)

    @EventCallback
    def CTSOnMarketMakerFilterRefreshed(self, event):
        self.OnFilterRefreshed(event)

    def SourceObject(self, rowObject):
        return rowObject.TradingInterface().StoredOrderBook()
