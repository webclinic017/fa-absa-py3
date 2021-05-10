""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FSalesTradingGraphPanel.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FSalesTradingGraphPanel

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
from FTimeSeriesGraphPanel import TimeSeriesGraphPanel
from FCTSPayoffGraphPanel import CTSPayoffGraphPanel
from FEvent import EventCallback

class CTSMarketMakerHistoricalGraphPanel(TimeSeriesGraphPanel):

    def __init__(self):
        TimeSeriesGraphPanel.__init__(self)

    @EventCallback
    def CTSMarketMakerQuoteSelected(self, event):
        self.Selected(event)

class CTSWatchlistHistoricalGraphPanel(TimeSeriesGraphPanel):

    def __init__(self):
        TimeSeriesGraphPanel.__init__(self)

    @EventCallback
    def CTSBondsSelected(self, event):
        self.Selected(event)

class CTSMarketMakerPayoffGraphPanel(CTSPayoffGraphPanel):

    def __init__(self):
        CTSPayoffGraphPanel.__init__(self)

    @EventCallback
    def CTSMarketMakerQuoteSelected(self, event):
        self.Selected(event)

class CTSWatchlistPayoffGraphPanel(CTSPayoffGraphPanel):

    def __init__(self):
        CTSPayoffGraphPanel.__init__(self)

    @EventCallback
    def CTSBondsSelected(self, event):
        self.Selected(event)
