""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FCTSClientMatrixViewerPanel.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FCTSClientMatrixViewerPanel

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

from FMatrixViewerPanel import MatrixViewerPanel
from FEvent import EventCallback

class CTSClientMatrixViewerPanel(MatrixViewerPanel):
    def __init__(self):
        super(CTSClientMatrixViewerPanel, self).__init__()

    @EventCallback
    def CTSClientNavigationChanged(self, event):
        self.DisplayMatrix(event.Objects())

    @EventCallback
    def CTSClientPositionSelected(self, event):
        self.DisplayMatrix(event.Objects())
