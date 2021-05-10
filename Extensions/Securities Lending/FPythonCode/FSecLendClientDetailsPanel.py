""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendClientDetailsPanel.py"
"""------------------------------------------------------------------------------------------------
MODULE
    FSecLendClientDetailsPanel

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Client View - Panel displaying information and statistics for a selected client.

------------------------------------------------------------------------------------------------"""
import acm
from FPanel import Panel
from FEvent import EventCallback
from FSecLendCommon import CalculatedFieldsPane, CalculatedPieChartsPane


class SecLendClientDetailsPanel(Panel):

    FONT = 'Nirmala UI'

    def __init__(self):
        super(SecLendClientDetailsPanel, self).__init__()
        self._counterparty = None
        self._nameCtrl = None
        self._fieldsPane = CalculatedFieldsPane.FromSettings(
            self.Settings().CalculatedFieldsPane())
        self._chartPane = CalculatedPieChartsPane.FromSettings(
            self.Settings().CalculatedPieChartsPane())

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginHorzBox('Invisible')
        b.  BeginVertBox()
        b.    BeginHorzBox()
        b.      AddLabel('counterpartyName', '', 400, -1)
        b.      AddFill()
        b.    EndBox()
        b.    AddSpace(2)
        b.    BeginHorzBox()
        self._fieldsPane.CreateLayout(b)
        b.    EndBox()
        b.  EndBox()
        b.AddSpace(5)
        self._chartPane.CreateLayout(b)
        b.EndBox()
        return b

    def InitControls(self, layout):
        self.InitNameControl(layout)
        self._fieldsPane.InitControls(layout)
        self._chartPane.InitControls(layout)
    
    def OnHandleOnIdle(self):
        self._fieldsPane.HandleOnIdle()
        self._chartPane.HandleOnIdle()

    def InitNameControl(self, layout):
        self._nameCtrl = layout.GetControl('counterpartyName')
        self._nameCtrl.SetFont(self.FONT, 14, True, False)

    @EventCallback
    def OnClientViewCounterpartySelected(self, event):
        self._counterparty = event.Counterparty()
        self.UpdateCounterpartyInformation()

    def UpdateCounterpartyInformation(self):
        name = self._counterparty.Name()
        self._nameCtrl.SetData(name)
        self._fieldsPane.SetObject(self._counterparty)
        self._chartPane.SetObject(self._counterparty)

