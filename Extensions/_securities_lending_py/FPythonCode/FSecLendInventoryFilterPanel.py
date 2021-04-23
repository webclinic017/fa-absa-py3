""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendInventoryFilterPanel.py"

"""------------------------------------------------------------------------------------------------
MODULE
    FSecLendInventoryFilterPanel

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Inventory View - Panel for the selection and filtering of security loan instrument lists.

------------------------------------------------------------------------------------------------"""

import acm
import traceback

import FSecLendRecordLookup
from FPanel import Panel
from FSecLendEvents import OnInventoryViewInventoryChanged, OnInventoryViewInstrumentsSelected
from FSecLendUtils import logger


class SecLendInventoryFilterPanel(Panel):

    def __init__(self):
        super(SecLendInventoryFilterPanel, self).__init__()
        try:
            self._bindings = None
            self._instrumentCtrl = FSecLendRecordLookup.SearchControl('Instrument',
                                                                      FSecLendRecordLookup.InstrumentLookup,
                                                                      FSecLendRecordLookup._SETTINGS.InstrumentLookUpIds(),
                                                                      width=60,
                                                                      displayAllIds=FSecLendRecordLookup._SETTINGS.DisplayAllIds())
            self.InitDataBindings()
        except Exception:
            logger.error('Exception Error:{}'.format(traceback.format_exc()))

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginHorzBox('Invisible')
        self._instrumentCtrl.BuildLayoutPart(b, '')
        b.EndBox()
        return b

    def InitInstrumentControl(self, layout):
        self._instrumentCtrl.HandleCreate(layout)
        if self.Settings().RefreshOnChanging():
            self._instrumentCtrl.AddCallback('Changed', self.OnInstrumentLooseFocusActivate, self)
        self._instrumentCtrl.AddCallback('Activate', self.OnInstrumentLooseFocusActivate, self)
        self._instrumentCtrl.AddCallback('LooseFocus', self.OnInstrumentLooseFocusActivate, self)
        self._instrumentCtrl.PopulateControl()

    def InitDataBindings(self):
        self._bindings = acm.FUxDataBindings()
        self._bindings.AddDependent(self)

    def InitControls(self, layout):
        self._bindings.AddLayout(layout)
        self.InitInstrumentControl(layout)

    def ServerUpdate(self, _sender, symbol, binder):
        if str(symbol) == 'ControlValueChanged':
            self.UpdateFilter()

    def OnInstrumentLooseFocusActivate(self, *args):
        self.UpdateFilter()

    def UpdateFilter(self):
        if self._instrumentCtrl.IsValidData():
            instrument = acm.FInstrument[self._instrumentCtrl.GetData()]
            if instrument:
                self.SendEvent(OnInventoryViewInventoryChanged(self, instrument))
                self.SendEvent(OnInventoryViewInstrumentsSelected(self, instrument))


