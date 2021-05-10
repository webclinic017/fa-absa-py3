""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FCTSMarketMakerMatrixViewerPanel.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FCTSMarketMakerMatrixViewerPanel

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

from FMatrixViewerPanel import MatrixViewerPanel
from FEvent import EventCallback

class CTSMarketMakerMatrixViewerPanel(MatrixViewerPanel):

    @EventCallback
    def CTSMarketMakerQuoteSelected(self, event):
        self.DisplayMatrix(event.Objects())
