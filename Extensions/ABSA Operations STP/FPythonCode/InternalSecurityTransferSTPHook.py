"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    InternalSecurityTransferSTPHook

DESCRIPTION
    This module contains two hooks. The one hook automatically sets fields on Internal security
    transfer trades. The other hook auto-releases settlements for internal transfers.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2020-04-29      FAOPS-615       Ntokozo Skosana         Wandile Sithole         Initial implementation.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm
import OperationsSTPFunctions
from at_logging import getLogger
from OperationsSTPHook import OperationsSTPHook


LOGGER = getLogger(__name__)

TRADE_SETTLE_CATEGORY = 'SA_CUSTODIAN'
TRAD_AREA = 'Internal Transfer'


def _qualifying_internal_security_transfer(trade):
    """
    Determine if trade is an internal security transfer or not.
    """
    if trade.Status() != 'FO Confirmed':
        return False
    if trade.Currency().Name() != 'ZAR':
        return False
    if trade.Counterparty().Type() != 'Intern Dept':
        return False
    if trade.Acquirer().Type() != 'Intern Dept':
        return False
    if trade.GetMirrorTrade() is None:
        return False
    instrument = trade.Instrument()
    if instrument.InsType() not in ['Bond', 'BuySellback', 'FRN', 'IndexLinkedBond', 'Repo/Reverse',
                                    'SecurityLoan']:
        return False
    security_issuer = _get_security_issuer(instrument)
    if security_issuer is None:
        return False
    if security_issuer.Name() == 'S A GOVERNMENT DOMESTIC':
        return False
    return True


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


def _internal_security_transfer_fields_already_set(trade):
    """
    Determine whether or not the Internal security transfer fields
    have already been set on the specified trade.
    """
    if not _trade_settle_category_already_set(trade, TRADE_SETTLE_CATEGORY):
        return False
    return _trad_area_already_set(trade, TRAD_AREA)


def _trade_settle_category_already_set(trade, value):
    """
    Determine whether or not the trade settle category has
    already been set on the specified trade.
    """
    trade_settle_category = trade.SettleCategoryChlItem()
    if trade_settle_category is None:
        return False
    return trade_settle_category.Name() == value


def _trad_area_already_set(trade, value):
    """
    Determine whether or not the TradArea (Trade Optional Key 1)
    has already been set on the specified trade.
    """
    trad_area = trade.OptKey1()
    if trad_area is None:
        return False
    return trad_area.Name() == value


def _set_trade_settle_category(trade, value):
    """
    Set the Trade Settle Category to the specified value if not
    already set.
    """
    if _trade_settle_category_already_set(trade, value):
        return
    LOGGER.info("Setting Trade Settle Category to '{value}'.".format(
        value=value
    ))
    trade.SettleCategoryChlItem(value)


def _set_trad_area(trade, value):
    """
    Set the Trade Optional Key 1 (TradArea) to the specified value
    if not already set.
    """
    if _trad_area_already_set(trade, value):
        return
    LOGGER.info("Setting Trade Optional Key 1 (TradArea) to '{value}'.".format(
        value=value
    ))
    trade.OptKey1(value)


def _is_different_acquirer_and_counterparty_accounts(trade, settle_category):
    """
    Determines if the counterparty and acquirer SSI are different
    """
    temp_trade = trade.StorageImage()
    temp_trade.SettleCategoryChlItem(settle_category)
    acquirer = temp_trade.Acquirer()
    counterparty = temp_trade.Counterparty()
    currency = temp_trade.Currency()

    # Create a simulated settlement to get the matching SSIs.
    tmp_settlement = acm.FSettlement()
    tmp_settlement.Trade(temp_trade)
    tmp_settlement.Acquirer(acquirer)
    tmp_settlement.Counterparty(counterparty)
    tmp_settlement.Currency(currency)
    tmp_settlement.Type('Security Nominal')

    # Get Cpty and Acquirer accounts
    cp_account_number = acm.Operations.AccountAllocator().CalculateCounterpartyAccountForSettlement(
        tmp_settlement, counterparty).Account()
    acquirer_account_number = acm.Operations.AccountAllocator().CalculateCounterpartyAccountForSettlement(
        tmp_settlement, acquirer).Account()

    return cp_account_number != acquirer_account_number


class InternalSecurityTransferSTPAutoReleaseHook(OperationsSTPHook):
    """"
    Definition of a hook used to Auto-Release Internal Security Transfer Trades
    """

    def Name(self):
        """
        Get the name of the Operations STP hook.
        """
        return 'Auto Release Internal Security Transfer Settlements'

    def IsTriggeredBy(self, eventObject):
        """
        Determine whether or not to trigger the hooks STP action/s
        for an event on the specified object.
        """
        if not eventObject.IsKindOf(acm.FSettlement):
            return False
        settlement = eventObject
        trade = settlement.Trade()
        if not settlement.Status() == 'Authorised':
            return False
        if not _qualifying_internal_security_transfer(trade):
            return False
        if not _internal_security_transfer_fields_already_set(trade):
            return False
        if not _is_different_acquirer_and_counterparty_accounts(trade, TRADE_SETTLE_CATEGORY):
            return False
        return True

    def PerformSTP(self, eventObject):
        """
        Perform the hooks STP action/s for an event on the specified
        object.

        Please note that the action does not necessarily occur to the
        event object itself but may occur to some related object/s.
        """

        LOGGER.info('Performing STP for Internal Transfer Settlement')
        OperationsSTPFunctions.release_settlement(eventObject)


class SetInternalSecurityTransferFieldsSTPHook(OperationsSTPHook):
    """
    Definition of a hook used to automatically set fields on Internal
    security transfer trades.
    """
    def Name(self):
        """
        Get the name of the Operations STP Hook.
        """
        return 'Set Internal Security Transfer Fields STP Hook'

    def IsTriggeredBy(self, eventObject):
        """
        Determine whether or not to trigger the hooks STP action/s
        for an event on the specified object.
        """
        if not eventObject.IsKindOf(acm.FTrade):
            return False
        if not _qualifying_internal_security_transfer(eventObject):
            return False
        if _internal_security_transfer_fields_already_set(eventObject):
            return False
        if not _is_different_acquirer_and_counterparty_accounts(eventObject, TRADE_SETTLE_CATEGORY):
            LOGGER.info("Acquirer and Counterparty Security Account SSI's are identical")
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
        _set_trade_settle_category(trade, TRADE_SETTLE_CATEGORY)
        _set_trad_area(trade, TRAD_AREA)
        trade.Commit()
