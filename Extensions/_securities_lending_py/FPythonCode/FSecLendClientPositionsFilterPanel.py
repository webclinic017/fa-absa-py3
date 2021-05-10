""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendClientPositionsFilterPanel.py"
"""------------------------------------------------------------------------------------------------
MODULE
    FSecLendClientPositionsFilterPanel

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Client View - Panel containing filter controls for the displayed client positions.

------------------------------------------------------------------------------------------------"""
import acm
from FPanel import Panel
import FSecLendUtils
import FSecLendRecordLookup
from FSecLendEvents import OnClientViewPositionFilterChanged, OnClientViewPositionInstrumentSearch
import traceback

class SecLendClientPositionsFilterPanel(Panel):

    def __init__(self):
        super(SecLendClientPositionsFilterPanel, self).__init__()
        self._marketCtrl = None
        self._currCtrl = None
        self._clearBtn = None
        self._searchField = None
        self._bindings = None
        self.InitDataBindings()

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginHorzBox('Invisible')
        self._marketCtrl.BuildLayoutPart(b, 'Market')
        self._currCtrl.BuildLayoutPart(b, 'Currency')
        b.  AddButton('clear', 'Clear')
        b.  AddFill()
        b.  AddInput('search', 'Security', 20, 45)
        b.EndBox()
        return b

    def InitControls(self, layout):
        self._bindings.AddLayout(layout)
        self.InitMarketControl(layout)
        self.InitCurrencyControl(layout)
        self.InitClearFilterControl(layout)
        self.InitSearchField(layout)
        
    def InitMarketControl(self, layout):
        if FSecLendUtils.IsShowDropDownKey():
            layout.GetControl('market').EnableShowDropDownOnKeyDown(True)
        
    def InitCurrencyControl(self, layout):
        if FSecLendUtils.IsShowDropDownKey():
            layout.GetControl('currency').EnableShowDropDownOnKeyDown(True)

    def InitClearFilterControl(self, layout):
        self._clearBtn = layout.GetControl('clear')
        self._clearBtn.Enabled(False)
        self._clearBtn.ToolTip('Clear the filter fields')
        self._clearBtn.AddCallback('Activate', self.OnClearFilterClicked, None)

    def InitSearchField(self, layout):
        self._searchField = layout.GetControl('search')
        self._searchField.ToolTip('Search for instrument')
        self._searchField.AddCallback('Changed', self.OnSearchChanged, None)

    def InitDataBindings(self):
        self._bindings = acm.FUxDataBindings()
        self._marketCtrl = self._bindings.AddBinder(
            'market', acm.GetDomain('FMarketPlace'),
            choiceListSource=acm.FMarketPlace.Instances(),
            width=20, maxWidth=45)
        self._currCtrl = self._bindings.AddBinder(
            'currency', acm.GetDomain('FCurrency'),
            choiceListSource=acm.FCurrency.Instances(),
            width=20, maxWidth=45)
        self._bindings.AddDependent(self)

    def OnClearFilterClicked(self, *args):
        self._marketCtrl.SetValue('')
        self._currCtrl.SetValue('')

    def OnSearchChanged(self, *args):
        text = self._searchField.GetData()
        self.SendEvent(OnClientViewPositionInstrumentSearch(self, text))

    def ServerUpdate(self, _sender, symbol, binder):
        if str(symbol) == 'ControlValueChanged':
            self.UpdateFilter()

    def UpdateFilter(self):
        market = self._marketCtrl.GetValue()
        currency = self._currCtrl.GetValue()
        self._clearBtn.Enabled((bool(market) or bool(currency)))
        self.SendEvent(OnClientViewPositionFilterChanged(self, market, currency))

