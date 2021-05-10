"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    CallStatementConfirmationCreator

DESCRIPTION
    This module contains objects used for triggering the regular or adhoc
    generation of call deposit statements via the creation of confirmations 
    for the call deposit statement event.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2018-08-14      FAOPS-167       Cuen Edwards            Elaine Visagie          Initial Implementation
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm

from at_logging import getLogger
import CallStatementGeneral
import StatementGeneral


LOGGER = getLogger(__name__)


class CallStatementConfirmationCreator(object):
    """
    An object responsible for triggering the regular or adhoc
    generation of call deposit statements via the creation of 
    confirmations for the call deposit statement event.
    """

    @classmethod
    def create_scheduled_statement_confirmations(cls, acquirers, ignore_existing_statements):
        """
        Create scheduled call deposit statements for the specified
        acquirers.
        """
        if cls._should_create_monthly_statements():
            cls._create_monthly_statement_confirmations(acquirers, ignore_existing_statements)
        if cls._should_create_weekly_statements():
            cls._create_weekly_statement_confirmations(acquirers, ignore_existing_statements)
        if cls._should_create_daily_statements():
            cls._create_daily_statement_confirmations(acquirers, ignore_existing_statements)

    @classmethod
    def create_adhoc_statement_confirmation(cls, trade, from_date, to_date):
        """
        Create an adhoc call deposit statement confirmation for the 
        specified trade and statement date range.
        """
        # Allowing generation of adhoc statements for counterparties who
        # are not configured to receive scheduled statements.
        # Ensure that the trade has something that can appear on a
        # statement during the period.
        cls._validate_statement_money_flows_exist(trade, from_date, to_date)
        # Adjust from and to dates if necessary.
        from_date = cls._adjust_statement_from_date_for_trade(trade, from_date)
        to_date = cls._adjust_statement_to_date_for_trade(trade, to_date)
        cls._create_statement_confirmation_for_trade(trade, from_date, to_date, None)

    @staticmethod
    def _should_create_monthly_statements():
        """
        Determine whether or not to create the monthly statements.
        """
        date_today = acm.Time.DateToday()
        return date_today == acm.Time.FirstDayOfMonth(date_today)

    @staticmethod
    def _should_create_weekly_statements():
        """
        Determine whether or not to create the weekly statements.
        """
        date_today = acm.Time.DateToday()
        return acm.Time.DayOfWeek(date_today) == 'Saturday'

    @staticmethod
    def _should_create_daily_statements():
        """
        Determine whether or not to create the daily statements.
        """
        return True

    @classmethod
    def _create_monthly_statement_confirmations(cls, acquirers, ignore_existing_statements):
        """
        Create monthly call deposit statements for the specified acquirers.
        """
        message = "Creating monthly call deposit statement confirmations "
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
                ignore_existing_statements, CallStatementGeneral.get_monthly_statement_frequency_value())
        LOGGER.info("Completed creating monthly call deposit statement confirmations.")

    @classmethod
    def _create_weekly_statement_confirmations(cls, acquirers, ignore_existing_statements):
        """
        Create weekly call deposit statements for the specified acquirers.
        """
        message = "Creating weekly call deposit statement confirmations "
        message += "for date today '{date_today}'..."
        date_today = acm.Time.DateToday()
        LOGGER.info(message.format(
            date_today=date_today
        ))
        cls._validate_acquirers(acquirers)
        from_date = acm.Time.DateAddDelta(date_today, 0, 0, -8)
        to_date = acm.Time.DateAddDelta(date_today, 0, 0, -1)
        for acquirer in acquirers:
            cls._create_acquirer_statement_confirmations(acquirer, from_date, to_date,
                ignore_existing_statements, CallStatementGeneral.get_weekly_statement_frequency_value())
        LOGGER.info("Completed creating weekly call deposit statement confirmations.")

    @classmethod
    def _create_daily_statement_confirmations(cls, acquirers, ignore_existing_statements):
        """
        Create daily call deposit statements for the specified acquirers.
        """
        message = "Creating daily call deposit statement confirmations "
        message += "for date today '{date_today}'..."
        date_today = acm.Time.DateToday()
        LOGGER.info(message.format(
            date_today=date_today
        ))
        cls._validate_acquirers(acquirers)
        to_date = acm.Time.DateAddDelta(date_today, 0, 0, -1)
        from_date = acm.Time.FirstDayOfMonth(to_date)
        for acquirer in acquirers:
            cls._create_acquirer_statement_confirmations(acquirer, from_date, to_date,
                ignore_existing_statements, CallStatementGeneral.get_daily_statement_frequency_value())
        LOGGER.info("Completed creating daily call deposit statement confirmations.")

    @classmethod
    def _create_acquirer_statement_confirmations(cls, acquirer, from_date, to_date,
            ignore_existing_statements, statement_frequency):
        """
        Create call deposit statements for the specified acquirer and
        any counterparties with call deposit trades between the
        inclusive statement from date and inclusive statement to date
        and who are configured to receive such statements.
        """
        message = "Creating statement confirmations for acquirer '{acquirer_name}'..."
        message = message.format(acquirer_name=acquirer.Name())
        LOGGER.info(message)
        counterparties = CallStatementGeneral.find_parties_receiving_scheduled_statements_for_acquirer_and_frequency(
            acquirer, statement_frequency)
        for counterparty in counterparties:
            trades = CallStatementGeneral.get_statement_trades(acquirer, counterparty,
                from_date, to_date)
            if len(trades) == 0:
                message = "No statement trades found for counterparty '{counterparty_name}'"
                message += ", skipping..."
                LOGGER.info(message.format(
                    counterparty_name=counterparty.Name()
                ))
                continue
            for trade in trades:
                # Adjust from and to dates if necessary.
                trade_from_date = cls._adjust_statement_from_date_for_trade(trade, from_date)
                trade_to_date = cls._adjust_statement_to_date_for_trade(trade, to_date)
                if CallStatementGeneral.statement_confirmation_exists(trade, trade_from_date, trade_to_date,
                        statement_frequency) and not ignore_existing_statements:
                    message = "Statement already exists for trade '{trade_oid}'"
                    message += ", skipping..."
                    LOGGER.info(message.format(
                        trade_oid=trade.Oid()
                    ))
                    continue
                try:
                    cls._create_statement_confirmation_for_trade(trade, trade_from_date, trade_to_date,
                        statement_frequency)
                except:
                    # Prevent an exception during the generation of one statement
                    # from preventing the creation of others.
                    message = "An exception occurred creating the statement for trade "
                    message += "'{trade_oid}', skipping..."
                    LOGGER.warning(message.format(
                        trade_oid=trade.Oid()
                    ), exc_info=True)

    @staticmethod
    def _adjust_statement_from_date_for_trade(trade, from_date):
        """
        Adjust a statement from date so that a statement is not run
        for a period before a deposit starts.
        """
        if trade.ValueDay() > from_date:
            message = "Trade value day is after statement from date - "
            message += "adjusting statement from date to {value_day}."
            LOGGER.info(message.format(
                value_day=trade.ValueDay()
            ))
            return trade.ValueDay()
        return from_date

    @staticmethod
    def _adjust_statement_to_date_for_trade(trade, to_date):
        """
        Adjust a statement to date so that a statement is not run
        for a period after a deposit ends.
        """
        instrument_end_date = trade.Instrument().EndDate()
        if instrument_end_date < to_date:
            message = "Instrument end date is before statement to date - "
            message += "adjusting statement to date to {end_date}."
            LOGGER.info(message.format(
                end_date=instrument_end_date
            ))
            return instrument_end_date
        return to_date

    @classmethod
    def _create_statement_confirmation_for_trade(cls, trade, from_date, to_date,
            document_schedule):
        """
        Create a call deposit statement for the specified acquirer,
        counterparty, inclusive statement from date, inclusive
        statement to date and document communication frequency
        schedule.

        This function should only be called if the trade has money
        flows for the statement period.  If no statement money flows
        are found an exception will be raised.
        """
        StatementGeneral.validate_statement_date_range(from_date, to_date)
        cls._validate_statement_money_flows_exist(trade, from_date, to_date)
        LOGGER.info("Creating statement confirmation for trade '{trade_oid}'.".format(
            trade_oid=trade.Oid()
        ))
        CallStatementGeneral.create_statement_confirmation(trade, from_date, to_date,
            document_schedule)

    @staticmethod
    def _validate_statement_money_flows_exist(trade, from_date, to_date):
        """
        Validate that statement money flows exist for the specified
        trade, inclusive statement from date and inclusive statement
        to date.
        """
        if not CallStatementGeneral.statement_money_flows_exist(trade, from_date, to_date):
            exception_message = "No statement money flows found for trade "
            exception_message += "'{trade_oid}'."
            exception_message = exception_message.format(
                trade_oid=trade.Oid()
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
