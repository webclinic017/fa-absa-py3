""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/IntegratedWorkbenchExamples/etc/FExampleTradesViewerPanel.py"
"""-------------------------------------------------------------------------------------------------
MODULE
    FExampleTradesViewerPanel

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------"""

import FSheetUtils
from FSheetPanel import SheetPanel
from FEvent import EventCallback

class ExampleTradesViewerPanel(SheetPanel):

    @EventCallback
    def OnInstrumentsSelected(self, event):
        selection = FSheetUtils.SelectedTrades(event.Objects())
        self.Sheet().InsertObject(selection)
