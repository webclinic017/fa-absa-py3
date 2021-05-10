""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendInventoryInstrumentDetailsPanel.py"
"""------------------------------------------------------------------------------------------------
MODULE
    FSecLendInventoryInstrumentDetailsPanel

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Inventory View - Panel displaying addition information for a selected instrument.

------------------------------------------------------------------------------------------------"""
import acm
from FPanel import Panel
from FEvent import EventCallback
from FSecLendCommon import CalculatedFieldsPane, CalculatedPieChartsPane


class SecLendInventoryInstrumentDetailsPanel(Panel):

    def __init__(self):
        super(SecLendInventoryInstrumentDetailsPanel, self).__init__()
        self._instrument = None
        self._fieldsPane = CalculatedFieldsPane.FromSettings(
            self.Settings().CalculatedFieldsPane())
        self._chartPane = CalculatedPieChartsPane.FromSettings(
            self.Settings().CalculatedPieChartsPane())

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginHorzBox('None')
        self._fieldsPane.CreateLayout(b)
        b.AddSpace(5)
        self._chartPane.CreateLayout(b)
        b.EndBox()
        return b

    def InitControls(self, layout):
        self._fieldsPane.InitControls(layout)
        self._chartPane.InitControls(layout)
        
    def OnHandleOnIdle(self):
        self._fieldsPane.HandleOnIdle()
        self._chartPane.HandleOnIdle()

    @EventCallback
    def OnInventoryViewInstrumentsSelected(self, event):
        instrument = event.GetUnderlyingOrSelf()
        if self._instrument != instrument:
            self._instrument = instrument
            self.UpdateInstrumentInformation()

    def UpdateInstrumentInformation(self):
        if self._instrument:
            self._fieldsPane.SetObject(self._instrument)
            self._chartPane.SetObject(self._instrument)
