""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/IntegratedWorkbenchExamples/etc/FExampleOrderBookPanel.py"

"""-------------------------------------------------------------------------------------------------------
MODULE
    FExampleOrderBookPanel

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

from FSheetPanel import SheetPanel
from FEvent import EventCallback

class ExampleOrderBookPanel(SheetPanel):

    @EventCallback
    def OnExampleTradesSelected(self, sender):
        if sender.Objects():
            orderBooks = sender.Objects().First().Trade().Instrument().OrderBooks()
            self.Sheet().InsertObject(orderBooks)
