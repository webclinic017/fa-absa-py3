"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    SetSARBSecurityTransferFieldsSTPHook

DESCRIPTION
    This module contains a hook to automatically set fields on SARB security
    transfer trades.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2020-04-29      FAOPS-700       Cuen Edwards            Kgomotso Gumbo          Initial implementation.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm

from at_logging import getLogger
from OperationsSTPHook import OperationsSTPHook


LOGGER = getLogger(__name__)

TRADE_SETTLE_CATEGORY = 'SA_CUSTODIAN'
TRAD_AREA = 'SARB Transfer'


class SetSARBSecurityTransferFieldsSTPHook(OperationsSTPHook):
    """
    Definition of a hook used to automatically set fields on SARB
    security transfer trades.
    """

    def Name(self):
        """
        Get the name of the Operations STP Hook.
        """
        return 'Set SARB Security Transfer Fields STP Hook'

    def IsTriggeredBy(self, eventObject):
        """
        Determine whether or not to trigger the hooks STP action/s
        for an event on the specified object.
        """
        if not eventObject.IsKindOf(acm.FTrade):
            return False
        if not self._is_sarb_security_transfer(eventObject):
            return False
        if self._sarb_security_transfer_fields_already_set(eventObject):
            return False
        return True

    def PerformSTP(self, trade):
        """
        Perform the hooks STP action/s for an event on the specified
        object.

        Please note that the action does not necessarily occur to the
        event object itself but may occur to some related object/s.
        """
        trade = trade.StorageImage()
        self._set_trade_settle_category(trade, TRADE_SETTLE_CATEGORY)
        self._set_trad_area(trade, TRAD_AREA)
        trade.Commit()

    @classmethod
    def _is_sarb_security_transfer(cls, trade):
        """
        Determine whether or not a trade is a security transfer with the
        SARB.
        """
        if trade.Status() != 'FO Confirmed':
            return False
        if trade.Currency().Name() != 'ZAR':
            return False
        if trade.Counterparty().Name() != 'ALCO DESK ISSUER':
            return False
        if trade.Acquirer().Type() != 'Intern Dept':
            return False
        if trade.GetMirrorTrade() is None:
            return False
        instrument = trade.Instrument()
        if instrument.InsType() not in ['Bond', 'BuySellback', 'FRN', 'IndexLinkedBond', 'Repo/Reverse',
                'SecurityLoan']:
            return False
        security_issuer = cls._get_security_issuer(instrument)
        if security_issuer is None:
            return False
        if security_issuer.Name() != 'S A GOVERNMENT DOMESTIC':
            return False
        return True

    @staticmethod
    def _get_security_issuer(instrument):
        """
        Get the issuer of the security instrument associated with the
        specified instrument.

        In the case where an instrument has an underlying instrument,
        the issuer of the underlying instrument is returned.  In case
        of an instrument without an underlying instrument, the issuer
        of the base instrument is returned.
        """
        underlying_instrument = instrument.Underlying()
        if underlying_instrument is not None:
            return underlying_instrument.Issuer()
        return instrument.Issuer()

    @classmethod
    def _sarb_security_transfer_fields_already_set(cls, trade):
        """
        Determine whether or not the SARB security transfer fields
        have already been set on the specified trade.
        """
        if not cls._trade_settle_category_already_set(trade, TRADE_SETTLE_CATEGORY):
            return False
        return cls._trad_area_already_set(trade, TRAD_AREA)

    @staticmethod
    def _trade_settle_category_already_set(trade, value):
        """
        Determine whether or not the trade settle category has
        already been set on the specified trade.
        """
        trade_settle_category = trade.SettleCategoryChlItem()
        if trade_settle_category is None:
            return False
        return trade_settle_category.Name() == value

    @staticmethod
    def _trad_area_already_set(trade, value):
        """
        Determine whether or not the TradArea (Trade Optional Key 1)
        has already been set on the specified trade.
        """
        trad_area = trade.OptKey1()
        if trad_area is None:
            return False
        return trad_area.Name() == value

    @classmethod
    def _set_trade_settle_category(cls, trade, value):
        """
        Set the Trade Settle Category to the specified value if not
        already set.
        """
        if cls._trade_settle_category_already_set(trade, value):
            return
        LOGGER.info("Setting Trade Settle Category to '{value}'.".format(
            value=value
        ))
        trade.SettleCategoryChlItem(value)

    @classmethod
    def _set_trad_area(cls, trade, value):
        """
        Set the Trade Optional Key 1 (TradArea) to the specified value
        if not already set.
        """
        if cls._trad_area_already_set(trade, value):
            return
        LOGGER.info("Setting Trade Optional Key 1 (TradArea) to '{value}'.".format(
            value=value
        ))
        trade.OptKey1(value)
