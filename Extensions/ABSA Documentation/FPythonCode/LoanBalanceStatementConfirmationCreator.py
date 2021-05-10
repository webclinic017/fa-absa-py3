"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    LoanBalanceStatementConfirmationCreator

DESCRIPTION
    This module contains objects used for triggering the regular generation of loan balance statements
    via the creation of confirmations for the loan balance statement event.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-05-29      FAOPS-513       Stuart Wilson           Kershia Perumal         Initial Implementation.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm

from at_logging import getLogger
import DocumentConfirmationGeneral
from MultiTradeConfirmationOwnerProvider import MultiTradeConfirmationOwnerProvider


LOGGER = getLogger(__name__)


class LoanBalanceStatementConfirmationCreator(object):
    """
    An object responsible for triggering the adhoc
    generation of loan balance statements via the creation of
    confirmations for the loan balance statement event.
    """

    def __init__(self):
        """
        Constructor.
        """
        self._confirmation_owner_trade_provider = MultiTradeConfirmationOwnerProvider()

    def create_adhoc_statement_confirmation(self, acquirer, counterparty, from_date,
            to_date):
        """
        Create an adhoc loan balance statement confirmation for the
        specified acquirer, counterparty, and statement date range.
        """
        self._validate_acquirer(acquirer)
        # Allowing generation of adhoc statements for counterparties who
        # are not configured to receive scheduled statements.
        self._create_statement_confirmation_for_acquirer_and_counterparty(acquirer, counterparty,
            from_date, to_date, None)

    def _create_statement_confirmation_for_acquirer_and_counterparty(self, acquirer, counterparty,
            from_date, to_date, document_schedule):
        """
        Create a loan balance statement for the specified acquirer,
        counterparty, exclusive statement from date, inclusive
        statement to date and document communication frequency
        schedule.

        This function should only be called if the counterparty has eligible
        loan balance trades for the statement period.  If no statement trades
        are found an exception will be raised.
        """
        LOGGER.info("Creating statement confirmation for counterparty '{counterparty_name}'.".format(
            counterparty_name=counterparty.Name()
        ))
        confirmation_owner_trade = self._confirmation_owner_trade_provider.provide_owner_trade(
            acquirer, counterparty)
        DocumentConfirmationGeneral.create_document_confirmation('Loan Balance Statement',
            confirmation_owner_trade, None, from_date, to_date, document_schedule)

    def _validate_acquirers(self, acquirers):
        """
        Validate a list of acquirers specified for statement creation.
        """
        if len(acquirers) == 0:
            raise ValueError('At least one acquirer must be specified.')
        for acquirer in acquirers:
            self._validate_acquirer(acquirer)

    @staticmethod
    def _validate_acquirer(acquirer):
        """
        Validate an acquirer specified for statement creation.
        """
        if acquirer is None:
            raise ValueError('An acquirer must be specified.')
        if not acquirer.IsKindOf(acm.FInternalDepartment):
            raise ValueError('An acquirer must be an internal department.')
