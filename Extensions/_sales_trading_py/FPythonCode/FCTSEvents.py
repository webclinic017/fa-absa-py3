""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FCTSEvents.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FCTSEvents

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

from FEvent import (
                BaseEvent,
                OnInstrumentsSelected,
                OnCounterpartiesSelected,
                OnObjectsSelected,
                )

class OnCreate(BaseEvent):

    def __init__(self, sender, params = None):
        BaseEvent.__init__(self, sender)
        
class OnTrade(BaseEvent):

    def Trade(self):
        return self.Parameters()

class CTSBondsSelected(OnInstrumentsSelected):
    pass

class CTSClientSelected(OnCounterpartiesSelected):
    pass

class OnSalesActivitiesSelected(OnObjectsSelected):
    pass

class CTSBondMatrixEntriesSelected(OnSalesActivitiesSelected):
    pass

class CTSClientMatrixEntriesSelected(OnSalesActivitiesSelected):
    pass

class CTSMarketMakerMatrixEntriesSelected(OnSalesActivitiesSelected):
    pass

class CTSMarketMakerQuoteSelected(OnInstrumentsSelected):
    pass

class CTSClientNavigationChanged(OnCounterpartiesSelected):
    pass

class CTSBondNavigationChanged(OnInstrumentsSelected):
    pass

class CTSMarketMakerNavigationChanged(OnInstrumentsSelected):
    pass

class CTSClientPositionsSelected(OnInstrumentsSelected):

    def __init__(self, sender, obj, client, params=None):
        OnInstrumentsSelected.__init__(self, sender, obj, params)
        self._client = client

    def Client(self):
        return self._client


class OnNavigationItemSelected(OnObjectsSelected):

    def __init__(self, sender, selection, params=None):
        OnObjectsSelected.__init__(self, sender, selection, params)

class OnSearchActivated(BaseEvent):

    def SearchString(self):
        return self.Parameters()

class CTSBondSearchActivated(OnSearchActivated):
    pass

class CTSClientSearchActivated(OnSearchActivated):
    pass

class CTSMarketMakerSearchActivated(OnSearchActivated):
    pass

class CTSOnFilterCreated(OnCreate):

    def __init__(self, sender, inFilter):
        OnCreate.__init__(self, sender)
        self._filter = inFilter

    def Filter(self):
        return self._filter


class CTSOnFilterCleared(OnCreate):
    pass


class CTSOnFilterActive(OnCreate):
    def __init__(self, sender, filterActive):
        OnCreate.__init__(self, sender)
        self._filterActive = filterActive

    def FilterActive(self):
        return self._filterActive


class CTSOnFilterChanged(OnCreate):

    def __init__(self, sender):
        OnCreate.__init__(self, sender)
        self._filter = sender.ActiveFilter()

    def Filter(self):
        return self._filter


class CTSOnFilterRemoved(CTSOnFilterChanged):
    pass


class CTSOnFilterRefreshed(CTSOnFilterChanged):
    pass


class OnBookmark(BaseEvent):
    pass
