"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    TermStatementConfirmationCreator

DESCRIPTION
    This module contains objects used for triggering the regular or adhoc
    generation of term deposit statements via the creation of confirmations 
    for the term deposit statement event.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2018-05-15      FAOPS-127       Cuen Edwards            Elaine Visagie          Initial Implementation.
2018-09-21                      Cuen Edwards                                    Refactored to be consistent with scheduled call statement
                                                                                generation.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm

from at_logging import getLogger
from MultiTradeConfirmationOwnerProvider import MultiTradeConfirmationOwnerProvider
import StatementGeneral
import TermStatementGeneral


LOGGER = getLogger(__name__)


class TermStatementConfirmationCreator(object):
    """
    An object responsible for triggering the regular or adhoc
    generation of term deposit statements via the creation of 
    confirmations for the term deposit statement event.
    """

    _confirmation_owner_trade_provider = MultiTradeConfirmationOwnerProvider()

    @classmethod
    def create_scheduled_statement_confirmations(cls, acquirers, ignore_existing_statements):
        """
        Create scheduled term deposit statements for the specified
        acquirers.
        """
        if cls._should_create_monthly_statements():
            cls._create_monthly_statement_confirmations(acquirers, ignore_existing_statements)

    @classmethod
    def create_adhoc_statement_confirmation(cls, acquirer, counterparty, from_date,
            to_date):
        """
        Create an adhoc term deposit statement confirmation for the 
        specified acquirer, counterparty, and statement date range.
        """
        cls._validate_acquirer(acquirer)
        # Allowing generation of adhoc statements for counterparties who
        # are not configured to receive scheduled statements.
        StatementGeneral.validate_statement_date_range(from_date, to_date)
        cls._create_statement_confirmation_for_acquirer_and_counterparty(acquirer, counterparty,
            from_date, to_date, None)

    @staticmethod
    def _should_create_monthly_statements():
        """
        Determine whether or not to create the monthly statements.
        """
        date_today = acm.Time.DateToday()
        return date_today == acm.Time.FirstDayOfMonth(date_today)

    @classmethod
    def _create_monthly_statement_confirmations(cls, acquirers, ignore_existing_statements):
        """
        Create monthly term deposit statements for the specified acquirers.
        """
        message = "Creating monthly term deposit statement confirmations "
        message += "for date today '{date_today}'..."
        LOGGER.info(message.format(
            date_today=acm.Time.DateToday()
        ))
        cls._validate_acquirers(acquirers)
        month = StatementGeneral.Month.parse_month('Previous')
        from_date = month.get_first_day_of_month()
        to_date = month.get_last_day_of_month()
        for acquirer in acquirers:
            cls._create_acquirer_statement_confirmations(acquirer, from_date, to_date,
                ignore_existing_statements, TermStatementGeneral.get_monthly_statement_frequency_value())
        LOGGER.info("Completed creating monthly term deposit statement confirmations.")

    @classmethod
    def _create_acquirer_statement_confirmations(cls, acquirer, from_date, to_date,
            ignore_existing_statements, statement_frequency):
        """
        Create term deposit statements for the specified acquirer and
        any counterparties with term deposit trades between the
        inclusive statement from date and inclusive statement to date
        and who are configured to receive such statements.
        """
        message = "Creating statement confirmations for acquirer '{acquirer_name}'..."
        message = message.format(acquirer_name=acquirer.Name())
        LOGGER.info(message)
        counterparties = TermStatementGeneral.find_parties_receiving_scheduled_statements_for_acquirer_and_frequency(
            acquirer, statement_frequency)
        for counterparty in counterparties:
            if not TermStatementGeneral.statement_trades_exist(acquirer, counterparty,
                    from_date, to_date):
                message = "No statement trades found for counterparty '{counterparty_name}'"
                message += ", skipping..."
                LOGGER.info(message.format(
                    counterparty_name=counterparty.Name()
                ))
                continue
            if TermStatementGeneral.statement_confirmation_exists(acquirer, counterparty, from_date, to_date,
                    statement_frequency) and not ignore_existing_statements:
                message = "Statement already exists for counterparty '{counterparty_name}'"
                message += ", skipping..."
                LOGGER.info(message.format(
                    counterparty_name=counterparty.Name()
                ))
                continue
            try:
                cls._create_statement_confirmation_for_acquirer_and_counterparty(acquirer, counterparty,
                    from_date, to_date, statement_frequency)
            except:
                # Prevent an exception during the generation of one statement
                # from preventing the creation of others.
                message = "An exception occurred creating the statement for counterparty "
                message += "'{counterparty_name}', skipping..."
                LOGGER.warning(message.format(
                    counterparty_name=counterparty.Name()
                ), exc_info=True)

    @classmethod
    def _create_statement_confirmation_for_acquirer_and_counterparty(cls, acquirer, counterparty,
            from_date, to_date, document_schedule):
        """
        Create a term deposit statement for the specified acquirer, 
        counterparty, inclusive statement from date, inclusive
        statement to date and document communication frequency
        schedule.

        This function should only be called if the counterparty has eligible
        term deposit trades for the statement period.  If no statement trades
        are found an exception will be raised.
        """
        StatementGeneral.validate_statement_date_range(from_date, to_date)
        cls._validate_statement_trades_exist(acquirer, counterparty, from_date, to_date)
        LOGGER.info("Creating statement confirmation for counterparty '{counterparty_name}'.".format(
            counterparty_name=counterparty.Name()
        ))
        confirmation_owner_trade = cls._confirmation_owner_trade_provider.provide_owner_trade(
            acquirer, counterparty)
        TermStatementGeneral.create_statement_confirmation(confirmation_owner_trade,
            from_date, to_date, document_schedule)

    @staticmethod
    def _validate_statement_trades_exist(acquirer, counterparty, from_date, to_date):
        """
        Validate that statement trades exist for the specified acquirer,
        counterparty, inclusive statement from date and inclusive
        statement to date.
        """
        if not TermStatementGeneral.statement_trades_exist(acquirer, counterparty,
                from_date, to_date):
            exception_message = "No statement trades found for counterparty "
            exception_message += "'{counterparty_name}'."
            exception_message = exception_message.format(
                counterparty_name=counterparty.Name()
            )
            raise ValueError(exception_message)

    @classmethod
    def _validate_acquirers(cls, acquirers):
        """
        Validate a list of acquirers specified for statement creation.
        """
        if len(acquirers) == 0:
            raise ValueError('At least one acquirer must be specified.')
        for acquirer in acquirers:
            cls._validate_acquirer(acquirer)

    @staticmethod
    def _validate_acquirer(acquirer):
        """
        Validate an acquirer specified for statement creation.
        """
        if acquirer is None:
            raise ValueError('An acquirer must be specified.')
        if not acquirer.IsKindOf(acm.FInternalDepartment):
            raise ValueError('An acquirer must be an internal department.')
