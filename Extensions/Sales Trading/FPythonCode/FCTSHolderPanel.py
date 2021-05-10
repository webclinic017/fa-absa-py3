""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FCTSHolderPanel.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FCTSHolderPanel

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""


import acm
from FSheetPanel import SheetPanel
from FSheetUtils import Trade as GetTrade
from FEvent import EventCallback

class CTSHolderPanel(SheetPanel):

    def __init__(self):
        super(CTSHolderPanel, self).__init__()
        self._instrument = None
        self._portfolio = None
        self._salesActivityListener = None
        self.Listener().StartListening()

    def Listener(self):
        if self._salesActivityListener is None:
            self._salesActivityListener = SalesActivityListener(self)
        return SalesActivityListener(self)

    def Instrument(self, instrument=Ellipsis):
        if instrument is not Ellipsis:
            self._instrument = instrument
        return self._instrument

    def Portfolio(self):
        if self._portfolio is None:
            self._portfolio = acm.FAdhocPortfolio()
            self._portfolio.Name('Holders')
        return self._portfolio

    def SelectedInstrumentChanged(self, instrument):
        return self.Instrument() != instrument

    def Selected(self, event):
        instrument = event.First()
        if self.SelectedInstrumentChanged(instrument):
            self._portfolio = None
            self.Instrument(instrument)
            if self.Instrument():
                self.Portfolio().Add(PlaceholderTrades(self.Instrument()))
            self.Update()

    def Update(self):
        self.Sheet().InsertObject(self.Portfolio())
        self.Sheet().ExpandTree(2)

    def OnNew(self, salesActivity):
        trade = GetTrade(salesActivity.Instrument())
        trade.Counterparty(salesActivity.Counterparty())
        self.Portfolio().Add(trade)

    def RemoveSubscriptions(self):
        self.Listener().StopListening()


class SalesActivityListener(object):

    def __init__(self, parent):
        self._parent = parent
        self._subject = None

    def Parent(self):
        return self._parent

    def Subject(self):
        if self._subject is None:
            self._subject = acm.FSalesActivity.Select("type = 'Holder'")
        return self._subject

    def StartListening(self):
        self.Subject().AddDependent(self)

    def StopListening(self):
        self.Subject().RemoveDependent(self)

    def ServerUpdate(self, sender, aspect, param):
        if str(aspect) == 'insert' and (param.Instrument() is self.Parent().Instrument()):
            self.Parent().OnNew(param)


def PlaceholderTrades(instrument):
    counterparties = GetCounterpartiesFromSalesActivities(instrument)
    return list(GetTrades(instrument, counterparties))

def GetCounterpartiesFromSalesActivities(instrument):
    counterparties = set()
    query = "instrument = '{0}' and type = 'Holder'".format(instrument.StringKey())
    salesActivities = acm.FSalesActivity.Select(query)
    counterparties.update(salesActivity.Counterparty() for salesActivity in salesActivities)
    return counterparties

def GetTrades(instrument, counterparties):
    for c in counterparties:
        trade = GetTrade(instrument)
        trade.Counterparty(c)
        yield trade



class CTSBondHolderPanel(CTSHolderPanel):

    def __init__(self):
        CTSHolderPanel.__init__(self)

    @EventCallback
    def CTSBondsSelected(self, event):
        self.Selected(event)


class CTSMarketMakerHolderPanel(CTSHolderPanel):

    def __init__(self):
        CTSHolderPanel.__init__(self)

    @EventCallback
    def CTSMarketMakerQuoteSelected(self, event):
        self.Selected(event)
