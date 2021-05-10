""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/ExecutionView/etc/FEVPricingPanel.py"
"""------------------------------------------------------------------------------------------------
MODULE
    FEVPricingPanel

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------"""

import acm
from FSheetPanel import SheetPanel
from FEvent import EventCallback

class EVPricingPanel(SheetPanel):

    @EventCallback
    def OnRowSelectionChanged(self, event):
        try:
            instruments = list()
            for rowObject in event.First().SelectedRowObjects():
                if rowObject.IsKindOf(acm.FSalesOrder):
                    if rowObject.Instrument() not in instruments:
                        instruments.append(rowObject.Instrument())
                elif rowObject.IsKindOf(acm.FOrderProgram):
                    for instrument in self.Instruments(rowObject):
                        if instrument not in instruments:
                            instruments.append(instrument)                    
            self.Sheet().InsertObject(instruments)
        except Exception:
            self.Sheet().InsertObject(None)
    
    @staticmethod
    def Instruments(orderprogram):
        return [order.Instrument() for order in orderprogram.OwnOrders()]