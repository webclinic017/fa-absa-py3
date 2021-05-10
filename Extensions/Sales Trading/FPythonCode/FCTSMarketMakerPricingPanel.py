""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FCTSMarketMakerPricingPanel.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FCTSMarketMakerPricingPanel

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

from FMultiSheetPanel import MultiSheetPanel
from FEvent import EventCallback

class CTSMarketMakerPricingPanel(MultiSheetPanel):

    def __init__(self):
        MultiSheetPanel.__init__(self)

    @EventCallback
    def CTSMarketMakerQuoteSelected(self, event):
        underlying = [i.Underlying() for i in event.Objects()]
        self._InsertObject(0, event.Objects())
        self._InsertObject(1, underlying)
