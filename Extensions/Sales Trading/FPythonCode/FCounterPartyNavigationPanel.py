""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FCounterPartyNavigationPanel.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FCounterPartyNavigationPanel

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import acm

from FNavigationPanel import NavigationPanel
from FSalesTradingLogging import logger
from FIntegratedWorkbenchUtils import IsKindOf
from FEvent import EventCallback

class CounterPartyNavigationPanel(NavigationPanel):

    def __init__(self):
        NavigationPanel.__init__(self)

    # ---- Overrides from NavigationPanel ----

    def BuildTree(self):
        try:
            allParties = acm.FCounterParty.Select('').SortByProperty('Name')

            struct = [self.Node(self._BookmarkedLabel(), self._Bookmarks().Get(), True),
                      self.Node(self._RecentLabel(), self._MRUList().Items(), True),
                      self.Node(self._AllLabel(), allParties, False)]
            self.UpdateNodes(struct)
        except Exception as exc:
            self.Logger().error("CounterPartyNavigationPanel.BuildTree Exception:")
            self.Logger().error(exc, exc_info=True)

    # ---- Event handling ----

    @EventCallback
    def OnBookmark(self, event):
        logger.debug("CounterPartyNavigationPanel.OnBookmark()")
        struct = [self.Node(self._BookmarkedLabel(), self._Bookmarks().Get(), True)]
        self.UpdateNodes(struct)

    @EventCallback
    def OnTrade(self, event):
        party = event.Trade().Counterparty()
        if party and IsKindOf(party, acm.FCounterParty):
            self._MRUList().AddUnique(party)
            self.Logger().debug("CounterPartyNavigationPanel.OnTrade() party: %s" % (party.Name()))
            self.UpdateNodes([self.Node(self._RecentLabel(), self._MRUList().Items(), True)])
