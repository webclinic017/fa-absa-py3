""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/IntegratedWorkbenchExamples/etc/FExamplePortfolioPanel.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FExamplePortfolioPanel

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

from FSheetPanel import SheetPanel
from FEvent import EventCallback

class ExamplePortfolioPanel(SheetPanel):

    @EventCallback
    def OnExampleTradesSelected(self, sender):
        if sender.Objects():
            portfolio = sender.Objects().First().Trade().Portfolio()
            self.Sheet().InsertObject(portfolio)
