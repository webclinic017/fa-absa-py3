""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FSalesTradingTradeListener.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FSalesTradingTradeListener

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import acm
import ael

from FSalesTradingLogging import logger


class SalesTradingTradeListener(object):

    def __init__(self):
        self._started = False

    def StartSubscription(self):
        if not self._started:
            logger.debug("SalesTradingTradeListener.StartSubscription() Subscribing")
            ael.Trade.subscribe(self._TradeNotify, self)
            self._started = True
        else:
            logger.debug("SalesTradingTradeListener.StartSubscription() Already subscribing")

    def EndSubscription(self):
        if self._started:
            logger.debug("SalesTradingTradeListener.EndSubscription() Unsubscribing")
            ael.Trade.unsubscribe(self._TradeNotify, self)
            self._started = False
        else:
            logger.debug("SalesTradingTradeListener.EndSubscription() Subscription already ended")

    # ---- AEL Subscription ----

    @staticmethod
    def _TradeNotify(obj, ael_ent, _arg, event):
        try:
            if not hasattr(ael_ent, 'insaddr'):
                return
            if not _arg:
                return
            acmTrade = acm.Ael.AelToFObject(ael_ent)
            _arg._OnTrade(acmTrade, event)
        except Exception as exc:
            logger.error("SalesTradingTradeListener._TradeNotify Exception: %s", exc)

    # ---- Methods to be implemented in sub classes ----

    def _OnTrade(self, acmTrade, event):
        raise NotImplementedError
