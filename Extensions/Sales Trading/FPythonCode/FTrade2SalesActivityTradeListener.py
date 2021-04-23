""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FTrade2SalesActivityTradeListener.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FTrade2SalesActivityTradeListener

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import collections

from FSalesTradingLogging import logger
from FTrade2SalesActivity import Trade2SalesActivity
from FSalesTradingTradeListener import SalesTradingTradeListener


class Trade2SalesActivityTradeListener(SalesTradingTradeListener):

    def __init__(self):
        SalesTradingTradeListener.__init__(self)
        self._taskQueue = collections.deque()
        self._trade2SalesActivity = Trade2SalesActivity()

    def Work(self):
        while len(self._taskQueue) > 0:
            try:
                acmTrade, event = self._taskQueue.popleft()
                logger.debug("Trade2SalesActivityTradeListener.Work() Trade: %d event: %s" % (acmTrade.Oid(), event))
                self._trade2SalesActivity.OnTrade(acmTrade, event)
            except Exception as exc:
                logger.error("Trade2SalesActivityTradeListener.Work Exception:")
                logger.error(exc, exc_info=True)

    # ---- Methods overriden from SalesTradingTradeListener ----

    def _OnTrade(self, acmTrade, event):
        self._taskQueue.append((acmTrade, event))
