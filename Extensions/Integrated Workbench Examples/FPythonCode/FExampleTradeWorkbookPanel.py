""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/IntegratedWorkbenchExamples/etc/FExampleTradeWorkbookPanel.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FExampleTradeWorkbookPanel

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

from FWorkbookPanel import WorkbookPanel
from FExampleCustomEvents import OnExampleTradesSelected



class ExampleTradeWorkbookPanel(WorkbookPanel):

    def SelectionChanged(self, selection):
        rowObjects = selection.SelectedRowObjects()
        event = OnExampleTradesSelected(self, rowObjects)
        self.SendEvent(event)
