""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FCTSMarketMakerPositionsPanel.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FCTSMarketMakerPositionsPanel

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

from FCTSPositionsPanel import CTSPositionsPanel
from FEvent import EventCallback

class CTSMarketMakerPositionsPanel(CTSPositionsPanel):

    def __init__(self):
        CTSPositionsPanel.__init__(self)

    @EventCallback
    def CTSMarketMakerQuoteSelected(self, event):
        self._ShowObjects(event.Objects())
