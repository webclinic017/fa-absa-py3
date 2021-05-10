"""--------------------------------------------------------------------------------------------------
MODULE
    SecurityTransferSTPHook

DESCRIPTION
    This module contains STP logic for Creation of Security Tranfers for
    Euroclear trades.

----------------------------------------------------------------------------------------------------
HISTORY
====================================================================================================
Date            Change no       Developer               Description
----------------------------------------------------------------------------------------------------
2020-02-30      FAOPS-685       Tawanda Mukhalela       Creation of Security Transfer trades.
----------------------------------------------------------------------------------------------------
"""
import acm
from at_logging import getLogger
from OperationsSTPHook import OperationsSTPHook
import OperationsSTPFunctions


LOGGER = getLogger(__name__)

SECURITY_TRANSFER_PORTFOLIO = acm.FPhysicalPortfolio[15046]

SUPPORTED_INSTYPES = ('Bond', 'FRN', 'Repo/Reverse')


class SecurityTransferCreationSTPHook(OperationsSTPHook):

    def Name(self):
        """
        Get the name of the Operations STP Hook.
        """
        return 'Security Transfer Creation STP Hook'

    def IsTriggeredBy(self, eventObject):
        """
        Hook to define if the stp rule should be triggered
        """

        if not eventObject.IsKindOf(acm.FTrade):
            return False

        trade = eventObject
        if trade.Status() != 'BO Confirmed':
            return False
        if trade.Type() == 'Security Transfer':
            return False
        if trade.OptKey1AsEnum() == 'Block Trade':
            return False
        instrument = trade.Instrument()
        if instrument.InsType() not in SUPPORTED_INSTYPES:
            return False
        if not _is_zag_isin(instrument):
            return False
        if instrument.Currency().Name() != 'ZAR':
            return False
        if not trade.SettleCategoryChlItem():
            return False
        if trade.SettleCategoryChlItem().Name() != 'Euroclear':
            return False
        if _has_transfer_trades(trade):
            return False

        return True

    def PerformSTP(self, eventObject):
        """
        Perform the security transfer for given trade object
        """
        trade = eventObject
        LOGGER.info('Creating Security Transfer for Trade {trade}'.format(trade=trade.Oid()))
        _create_security_transfer(trade)
        LOGGER.info('Created Security Transfer Trade')


class SecurityTransferUpdateSTPHook(OperationsSTPHook):

    def Name(self):
        """
        Get the name of the Operations STP Hook.
        """
        return 'Security Transfer Update STP Hook'

    def IsTriggeredBy(self, eventObject):
        """
        Hook to define if the stp rule should be triggered
        """

        if not eventObject.IsKindOf(acm.FTrade):
            return False
        trade = eventObject
        if trade.Status() != 'BO Confirmed':
            return False
        if trade.Type() != 'Security Transfer':
            return False
        instrument = trade.Instrument()
        if instrument.InsType() not in SUPPORTED_INSTYPES:
            return False
        if not _is_zag_isin(instrument):
            return False
        if instrument.Currency().Name() != 'ZAR':
            return False
        if trade.SettleCategoryChlItem():
            return False

        return True

    def PerformSTP(self, eventObject):
        """
        Update settle category for trade object
        """
        trade = eventObject
        related_transfer_trade = get_related_security_transfer_trade(trade)
        trx_trade = related_transfer_trade.TrxTrade()
        if related_transfer_trade.SettleCategoryChlItem().Name() == 'SA_CUSTODIAN':
            trade.SettleCategoryChlItem('Euroclear')
            LOGGER.info('Settle Category set to Euroclear for Trade {trade}'.format(trade=trade.Oid()))
        else:
            trade.SettleCategoryChlItem('SA_CUSTODIAN')
            LOGGER.info('Settle Category set to SA_CUSTODIAN for Trade {trade}'.format(trade=trade.Oid()))
        trade.OptKey1AsEnum('External Transfer')
        trade.TrxTrade(trx_trade)
        trade.Commit()
        LOGGER.info('Updated Security Transfer Trade')


class SecurityTransferVoidSTPHook(OperationsSTPHook):

    def Name(self):
        """
        Get the name of the Operations STP Hook.
        """
        return 'Void Security Transfer STP Hook'

    def IsTriggeredBy(self, eventObject):
        """
        Hook to define if the stp rule should be triggered
        """

        if not eventObject.IsKindOf(acm.FTrade):
            return False

        trade = eventObject
        if trade.Status() != 'Void':
            return False
        if trade.Type() == 'Security Transfer':
            return False
        if trade.OptKey1AsEnum() == 'Block Trade':
            return False
        instrument = trade.Instrument()
        if instrument.InsType() not in SUPPORTED_INSTYPES:
            return False
        if not _is_zag_isin(instrument):
            return False
        if instrument.Currency().Name() != 'ZAR':
            return False
        if not trade.SettleCategoryChlItem():
            return False
        if trade.SettleCategoryChlItem().Name() != 'Euroclear':
            return False
        if not _has_transfer_trades(trade):
            return False

        return True

    def PerformSTP(self, eventObject):
        """
        Perform the security transfer for given trade object
        """
        _void_related_security_transfer_trades(eventObject)


def _create_security_transfer(trade):
    """
    Create Security Transfer Trade
    """
    instrument = trade.Instrument()
    transfer_trade = acm.DealCapturing().CreateNewCustomTrade('Security Transfer', instrument)
    transfer_trade.Acquirer(trade.Acquirer().Name())
    transfer_trade.Counterparty(trade.Acquirer().Name())
    transfer_trade.Portfolio(SECURITY_TRANSFER_PORTFOLIO)
    transfer_trade.Price(0.0)
    transfer_trade.Quantity(trade.Quantity())
    transfer_trade.AcquireDay(trade.AcquireDay())
    if trade.Bought():
        transfer_trade.SettleCategoryChlItem('Euroclear')
        quantity = trade.Quantity() * -1
        transfer_trade.Quantity(quantity)
    else:
        transfer_trade.SettleCategoryChlItem('SA_CUSTODIAN')

    transfer_trade.TrxTrade(trade)
    transfer_trade.OptKey1AsEnum('External Transfer')
    transfer_trade.Status('BO Confirmed')
    _populate_source_and_destination_for_transfer(transfer_trade, trade)


def _populate_source_and_destination_for_transfer(transfer_trade, trade):
    """
    Populate transfer Destination and Source Acquirer
    """
    security_transfer = acm.FSecurityTransfer(transfer_trade)
    security_transfer.RegisterInStorage()
    security_transfer.Destination(transfer_trade)
    security_transfer.Source(trade)
    security_transfer.DestinationAcquirer(trade.Acquirer())
    security_transfer.SourceAcquirer(trade.Acquirer())
    security_transfer.AcquireDay(trade.AcquireDay())
    security_transfer.Portfolio(SECURITY_TRANSFER_PORTFOLIO)
    security_transfer.Status('BO Confirmed')
    security_transfer.Commit()


def _has_transfer_trades(trade):
    """
    Checks if the given trade already has Security Transfer
    Trades linked to it
    """
    if not trade.TrxTrades():
        return False
    for trade in trade.TrxTrades():
        if trade.Type() == 'Security Transfer':
            return True

    return False


def get_related_security_transfer_trade(trade):
    business_event = _get_security_transfer_business_event(trade)
    trade_links = business_event.TradeLinks().AsArray()
    if len(trade_links) != 2:
        error_message = "Expecting 2 trade links for 'Security Transfer' business "
        error_message += "event {business_event_oid}."
        LOGGER.exception(error_message.format(business_event_oid=business_event.Oid()))
    for trade_link in trade_links:
        if trade_link.Trade() != trade:
            return trade_link.Trade()
    error_message = "Unable to find related security transfer trade for trade "
    error_message += "{trade_oid}."
    LOGGER.exception(error_message.format(trade_oid=trade.Oid()))


def _get_security_transfer_business_event(trade):
    business_events = trade.BusinessEvents('Security Transfer')
    if len(business_events) != 1:
        error_message = "Expecting 1 business event of type 'Security Transfer' for "
        error_message += "trade {trade_oid}."
        LOGGER.exception(error_message.format(trade_oid=trade.Oid()))

    return business_events[0]


def _is_zag_isin(instrument):
    """
    Checks if the instrument or underlying has a ZAG ISIN
    """
    if instrument.Isin().startswith('ZAG'):
        return True
    if instrument.Underlying():
        if instrument.Underlying().Isin().startswith('ZAG'):
            return True
        return False

    return False


def _void_related_security_transfer_trades(original_trade):
    """
    Void all security transfer trades linked to the original voided trade
    """
    for trade in original_trade.TrxTrades():
        if trade.Type() != 'Security Transfer':
            continue
        if _has_released_settlements(trade):
            continue
        LOGGER.info('Found Security Transfer {trade_oid} on a voided Trade..'.format(trade_oid=trade.Oid()))
        OperationsSTPFunctions.void_trade(trade)


def _has_released_settlements(trade):
    """
    Checks if the trade has any released settlements:

    Idea is to maintain a good audit, we can't void a
    Sec Transfer if we have already transfered the securities
    """
    post_released_statuses = ('Released', 'Acknowledged', 'Not Acknowledged', 'Settled', 'Pending Closure', 'Closed')
    return any([settlement for settlement in trade.Settlements()
                if settlement.Status() in post_released_statuses]
               )
