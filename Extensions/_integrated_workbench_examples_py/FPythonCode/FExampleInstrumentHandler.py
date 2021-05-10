""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/IntegratedWorkbenchExamples/etc/FExampleInstrumentHandler.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FExampleInstumentHandler

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Implements a handler used by a menu item in order to access the last selected instrument
-------------------------------------------------------------------------------------------------------"""

from FHandler import Handler
from FEvent import EventCallback

class ExampleInstrumentHandler(Handler):

    def __init__(self, dispatcher):
        super(ExampleInstrumentHandler, self).__init__(dispatcher)
        self.lastTradeSelected = None

    @EventCallback
    def OnExampleTradesSelected(self, event):
        if event.First():
            self.lastTradeSelected = event.First().Trade()
        else:
            self.lastTradeSelected = None

    def LastInstrumentSelected(self):
        if self.lastTradeSelected:
            return self.lastTradeSelected.Instrument()
        else:
            return None
