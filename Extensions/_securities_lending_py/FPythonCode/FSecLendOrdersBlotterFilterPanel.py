""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendOrdersBlotterFilterPanel.py"
"""--------------------------------------------------------------------------
MODULE
    FSecLendOrdersBlotterFilterPanel

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Order Manager - Filter for trade/postion blotters.

-----------------------------------------------------------------------------"""
import acm
from FPanel import Panel
from FEvent import EventCallback
from FSecLendEvents import OnOrderManagerTradeFilterChanged
from FSecLendUtils import IsShowDropDownKey

class SecLendOrdersBlotterFilterPanel(Panel):

    def __init__(self):
        super(SecLendOrdersBlotterFilterPanel, self).__init__()
        self._clientCtrl = None
        self._clearBtn = None
        self._bindings = None
        self._selectedTrades = None
        self.InitDataBindings()

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginHorzBox()
        b.  AddSpace(10)
        self._clientCtrl.BuildLayoutPart(b, 'Counterparty Filter')
        b.  AddSpace(5)
        b.  AddButton('clear_filter', 'Clear')
        b.  AddSpace(10)
        b.EndBox()
        return b

    def InitDataBindings(self):
        self._bindings = acm.FUxDataBindings()
        self._clientCtrl = self._bindings.AddBinder(
            'client', acm.GetDomain('FCounterParty'),
            choiceListSource=acm.FCounterParty.Instances(),
            width=45, maxWidth=45)
        self._bindings.AddDependent(self)

    def InitControls(self, layout):
        self._bindings.AddLayout(layout)
        self.InitClearFilterControl(layout)
        self.InitClientCtrl(layout)
        
    def InitClearFilterControl(self, layout):
        self._clearBtn = layout.GetControl('clear_filter')
        self._clearBtn.AddCallback('Activate', self.OnClearFilterClicked, None)
        self._clearBtn.Enabled(False)
    
    def InitClientCtrl(self, layout):
        if IsShowDropDownKey():
            layout.GetControl('client').EnableShowDropDownOnKeyDown(True)

    def ServerUpdate(self, _sender, symbol, binder):
        if str(symbol) == 'ControlValueChanged':
            self.UpdateFilter()

    def OnClearFilterClicked(self, *args):
        self._clientCtrl.SetValue('')

    @EventCallback
    def OnOrderManagerTradesSelected(self, event):
        self._selectedTrades = event.Trades()

    def UpdateFilter(self):
        client = self._clientCtrl.GetValue()
        self.SendEvent(OnOrderManagerTradeFilterChanged(self, client))
        self._clearBtn.Enabled(bool(client))
