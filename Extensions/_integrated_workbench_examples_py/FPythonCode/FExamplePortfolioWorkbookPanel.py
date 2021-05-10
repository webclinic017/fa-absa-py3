""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/IntegratedWorkbenchExamples/etc/FExamplePortfolioWorkbookPanel.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FExamplePortfolioWorkbookPanel

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

from FWorkbookPanel import WorkbookPanel
from FEvent import OnInstrumentsSelected



class ExamplePortfolioWorkbookPanel(WorkbookPanel):

    def SelectionChanged(self, selection):
        rowObjects = selection.SelectedRowObjects()
        self.SendEvent(OnInstrumentsSelected(self, rowObjects))
