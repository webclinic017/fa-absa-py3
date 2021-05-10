""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendEvents.py"
"""------------------------------------------------------------------------------------------------
MODULE
    FSecLendEvents

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Events for workbench activity and interaction.

------------------------------------------------------------------------------------------------"""
from FEvent import BaseEvent, OnInstrumentsSelected


# ----------------------------------------------------------------------------------------------
#  Client workbench events

class OnClientViewPositionFilterChanged(BaseEvent):
    """The user has changed position filtering parameters."""

    def __init__(self, sender, market=None, currency=None, params=None):
        super(OnClientViewPositionFilterChanged, self).__init__(sender, params)
        self._market = market
        self._currency = currency

    def Market(self):
        return self._market

    def Currency(self):
        return self._currency


class OnClientViewPositionInstrumentSearch(BaseEvent):
    """The user has searched (or cleared a search) for a specific instrument."""

    def SearchText(self):
        return self.Parameters()


class OnClientViewCounterpartySelected(BaseEvent):
    """A counterparty to display information for has been selected."""

    def Counterparty(self):
        return self.Parameters()


class OnClientViewInstrumentsSelected(BaseEvent):
    """Instruments traded by the current client have been selected."""

    def Selection(self):
        try:
            return self.Parameters()
        except IndexError:
            return None


class OnClientViewCounterpartyChangedFromOrderCapture(BaseEvent):
    """The counterparty has been changed in the order capture panel."""

    def CounterpartyName(self):
        return self.Parameters().Name()

    def Counterparty(self):
        return self.Parameters()

# ----------------------------------------------------------------------------------------------
#  Inventory workbench events

class OnInventoryViewInstrumentsSelected(OnInstrumentsSelected):
    """Instruments in the inventory have been selected."""

    def Instrument(self):
        return self.First()

    def GetUnderlyingOrSelf(self):
        return self.First().UnderlyingOrSelf() if self.First() else None


class OnInventoryViewInstrumentDoubleClick(BaseEvent):
    """An instrument in the inventory has been doubleclicked."""

    def Instrument(self):
        return self.Parameters()


class OnInventoryViewInventoryChanged(BaseEvent):
    """The active inventory list has been changed or filtered."""

    def Instrument(self):
        return self.Parameters()


class OnInventoryViewInventoryChangedFromOrderCapture(BaseEvent):
    """The instrument has been changed in the order capture panel."""

    def Instrument(self):
        return self.Parameters()


class OnInventoryViewInventoryViewPositionSelected(BaseEvent):
    """A position is selected in the positions tab"""

    def PositionRows(self):
        return self.Parameters()


# ----------------------------------------------------------------------------------------------
#  Order Manager events


class OnOrderManagerOrdersEntered(BaseEvent):
    """Orders (reserved trades) have been saved from the order capture panel."""

    def Orders(self):
        return self.Parameters()


class OnOrderManagerOrdersSelected(BaseEvent):
    """Orders (reserved trades) have been selected in the main sheet."""

    def Orders(self):
        return self.Parameters()


class OnOrderManagerTradeFilterChanged(BaseEvent):
    """The filter on trade details has been changed."""

    def Counterparty(self):
        # TODO: Other attributes, or pass the entire filter instead
        return self.Parameters()


class OnOrderManagerTradesSelected(BaseEvent):
    """Booked trades have been selected in a trade blotter."""

    def Trades(self):
        return self.Parameters()


class OnOrderCaptureCounterpartyChanged(BaseEvent):
    """The counterparty has been changed in the order capture panel."""

    def Counterparty(self):
        return self.Parameters()


class OnOrderCaptureInstrumentChanged(BaseEvent):
    """The instrument has been changed in the order capture panel."""

    def Instrument(self):
        return self.Parameters()


# ----------------------------------------------------------------------------------------------
#  Rerate panel events used by Portfolio View and Client View

class OnPositionSelection(BaseEvent):
    """ The selection has been changed in the portfolio workbook panel."""

    def SelectedRowObjects(self):
        return self.Parameters()


class OnRerateButtonClicked(BaseEvent):
    """When the Rerate Button is clicked on Portfolio View."""

    def SelectedRowObjects(self):
        return self.Parameters()

# ----------------------------------------------------------------------------------------------
#  Portfolio Viewer workbench events




class OnFilterCreated(BaseEvent):
    def __init__(self, sender, inFilter):
        BaseEvent.__init__(self, sender)
        self._filter = inFilter

    def Filter(self):
        return self._filter


class OnFilterCleared(BaseEvent):
    pass


class OnFilterActive(BaseEvent):
    def __init__(self, sender, filterActive):
        BaseEvent.__init__(self, sender)
        self._filterActive = filterActive

    def FilterActive(self):
        return self._filterActive


class OnFilterChanged(BaseEvent):
    def __init__(self, sender):
        BaseEvent.__init__(self, sender)
        self._filter = sender.ActiveFilter()

    def Filter(self):
        return self._filter


class OnFilterRemoved(OnFilterChanged):
    pass


class OnFilterRefreshed(OnFilterChanged):
    pass
