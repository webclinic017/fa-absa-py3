"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    MultiTradeConfirmationOwnerProvider

DESCRIPTION
    This module contains an object responsible for providing a dummy
    trade to own the confirmation created for a document related to 
    multiple trades.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2018-08-01      FAOPS-127       Cuen Edwards            Elaine Visagie          Refactored from a term deposit statement specific
                                                                                implementation to one that can be used for other multi-
                                                                                trade documents.
2018-12-11      FAOPS-330       Cuen Edwards            Heinrich Cronje         Ensure that the discounting type is set on confirmation
                                                                                owner trades in order to avoid update collisions with
                                                                                another process.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm
from at_logging import getLogger


LOGGER = getLogger(__name__)


class MultiTradeConfirmationOwnerProvider(object):
    """
    An object responsible for providing a trade to own any confirmation
    related to multiple trades for a given combination of acquirer and
    counterparty.

    This functionality is necessary as the relationship between a
    confirmation and a trade in Front Arena is such that a confirmation
    is physically for one and only one trade.

    As the requirements for some documents (e.g. term deposit statements) 
    call for a document that contains multiple trades for a given set of 
    criteria, we find ourselves in a situation where a confirmation is 
    logically related to multiple trades.  As a confirmation must be 
    physically related to a trade, one must be provided for this purpose.

    It has been noted that the same issue was encountered with the
    introduction of the Deal Package framework - a relatively recent
    addition to Front Arena's built-in functionality.  If confirmations
    are desired for a Deal Package then one must nominate a 'lead'
    trade against which confirmations will be generated.

    After being presented with several options, IT management have
    decided that a dummy simulated trade should be used to house any
    multi-trade document confirmations for a given combination of 
    acquirer and counterparty.

    As such, this implementation returns a dummy trade.  Dummy trades
    are created per acquirer and counterparty.  If a dummy trade for a
    given acquirer and counterparty does not exist then one will be 
    created.
    """

    def provide_owner_trade(self, acquirer, counterparty):
        """
        Provide a trade to own the confirmation created for a multi-
        trade document by returning a dummy placeholder trade.
        """
        trade = self._get_dummy_trade(acquirer, counterparty)
        if trade is not None:
            return trade
        message = "Confirmation owner trade not found for "
        message += "acquirer '{acquirer_name}' and counterparty "
        message += "'{counterparty_name}', creating..."
        LOGGER.info(message.format(
            acquirer_name=acquirer.Name(),
            counterparty_name=counterparty.Name()
        ))
        return self._create_dummy_trade(acquirer, counterparty)

    def _get_dummy_trade(self, acquirer, counterparty):
        """
        Get the dummy trade for the specified acquirer and counterparty 
        combination, if one exists.
        """
        optional_key = self._get_dummy_trade_optional_key(acquirer,
            counterparty)
        select_expression = "optionalKey = {optional_key}"
        select_expression = select_expression.format(
            optional_key=optional_key
        )
        exception_message = "Expecting zero or one trade with the "
        exception_message += "optional key '{optional_key}'."
        exception_message = exception_message.format(
            optional_key=optional_key
        )
        return acm.FTrade.Select01(select_expression, exception_message)

    def _create_dummy_trade(self, acquirer, counterparty):
        """
        Create the dummy trade for the specified acquirer and 
        counterparty combination.
        """
        optional_key = self._get_dummy_trade_optional_key(acquirer,
            counterparty)
        currency = acm.FCurrency['ZAR']
        trade = acm.FTrade()
        trade.RegisterInStorage()
        trade.Instrument(currency)
        trade.Currency(currency)
        trade.Acquirer(acquirer)
        trade.Counterparty(counterparty)
        trade.OptionalKey(optional_key)
        trade.TradeTime(acm.Time.DateToday())
        # Set Acquire Day and Value Day to a date far in future to avoid 
        # these trades being picked up for archiving and aggregation.
        trade.AcquireDay('9999-12-31')
        trade.ValueDay('9999-12-31')
        trade.Status('Simulated')
        trade.Trader(acm.FUser['ATS_CONFO'])
        trade.DiscountingType('CCYBasis')
        trade.Commit()
        return trade

    @staticmethod
    def _get_dummy_trade_optional_key(acquirer, counterparty):
        """
        Get the optional key used to identify the dummy trade for the 
        specified acquirer and counterparty.
        """
        return str(counterparty.Oid()) + '_' + str(acquirer.Oid()) + '_Document'
