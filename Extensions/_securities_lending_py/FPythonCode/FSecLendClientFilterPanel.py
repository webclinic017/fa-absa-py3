""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendClientFilterPanel.py"
"""------------------------------------------------------------------------------------------------
MODULE
    FSecLendClientFilterPanel
    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Client Loan View - Panel for selecting a client.

------------------------------------------------------------------------------------------------"""
import acm
from FPanel import Panel
from FEvent import EventCallback
import ChoicesExprTrade
from FSecLendEvents import OnClientViewCounterpartySelected, OnClientViewCounterpartyChangedFromOrderCapture
import FSecLendUtils

class SecLendClientFilterPanel(Panel):

    def __init__(self):
        super(SecLendClientFilterPanel, self).__init__()
        self._clientCtrl = None
        self._bindings = None
        self.InitDataBindings()

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginHorzBox('Invisible')
        self._clientCtrl.BuildLayoutPart(b, 'Client')
        b.EndBox()
        return b
    
    def InitControls(self, layout):
        self._bindings.AddLayout(layout)
        self.InitCounterpartyControl(layout)
    
    def InitCounterpartyControl(self, layout):
        if FSecLendUtils.IsShowDropDownKey():
            layout.GetControl('Client').EnableShowDropDownOnKeyDown(True)
        
    def InitDataBindings(self):
        self._bindings = acm.FUxDataBindings()
        self._clientCtrl = self._bindings.AddBinder(
            'Client', acm.GetDomain('FParty'),
            choiceListSource=FSecLendUtils.getCounterparties(),
            width=30, maxWidth=45)
        self._bindings.AddDependent(self)

    def OnClientChanged(self, client):
        if client:
            self.SendEvent(OnClientViewCounterpartySelected(self, client))
        
    def ServerUpdate(self, sender, symbol, binder):
        if str(symbol) == 'ControlValueChanged':
            self.OnClientChanged(binder.GetValue())
                   
    @EventCallback
    def OnClientViewCounterpartyChangedFromOrderCapture(self, event):
        self._clientCtrl.SetValue('')
