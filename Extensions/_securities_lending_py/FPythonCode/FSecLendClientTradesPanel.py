""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendClientTradesPanel.py"
"""------------------------------------------------------------------------------------------------
MODULE
    FSecLendClientTradesPanel

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Client View - Panel showing trades for the currently selected client position(s).

------------------------------------------------------------------------------------------------"""
from FEvent import EventCallback
from FSheetPanel import SheetPanel
import FSheetUtils

class SecLendClientTradesPanel(SheetPanel):

    def __init__(self):
        super(SecLendClientTradesPanel, self).__init__()

    @staticmethod
    def QueryFolderLabel(trades):
        instruments = list(set(trade.Instrument().Underlying() for trade in trades))
        label = ', '.join(ins.Name() for ins in instruments[:2] if ins)
        if len(instruments) > 2:
            label += '...'
        return label

    @EventCallback
    def OnClientViewInstrumentsSelected(self, event):
        trades = set()
        for row in event.Selection().SelectedRowObjects():
            trades.update(row.Trades())
        folder = FSheetUtils.GetTradesAsFolder(trades, self.QueryFolderLabel(trades))
        self.Sheet().InsertObject(folder, 'IOAP_REPLACE')
        
    @EventCallback
    def OnClientViewCounterpartySelected(self, event):
        self.Sheet().RemoveAllRows()