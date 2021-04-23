"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    PreSettlementAdviceBusinessProcessCreator

DESCRIPTION
    This module contains objects used for triggering the regular or adhoc
    generation of pre-settlement advices via the creation of business processes
    for the pre-settlement advice event.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-09-17      FAOPS-460       Cuen Edwards            Letitia Carboni         Initial Implementation.
2019-10-14      FAOPS-531       Cuen Edwards            Letitia Carboni         Added support for amendments.
2020-02-05      FAOPS-741       Cuen Edwards            Kgomotso Gumbo          Replaced pre-settlement advice event listener with task.
2020-04-20      FAOPS-706       Cuen Edwards            Letitia Carboni         Changed grouping of party settlements on advices from
                                                                                implicit linking via SDSID to explicit linking via advice
                                                                                party additional info.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm

from at_logging import getLogger
import PreSettlementAdviceGeneral
from PreSettlementAdviceGeneral import get_advice_party_add_info_name


LOGGER = getLogger(__name__)


class PreSettlementAdviceBusinessProcessCreator(object):
    """
    An object responsible for triggering the regular or adhoc
    generation of pre-settlement advices via the creation of
    Pre-settlement Advice business processes.
    """

    @classmethod
    def create_scheduled_advice_business_processes(cls):
        """
        Create scheduled pre-settlement advice business processes.
        """
        if cls._should_create_weekly_advices():
            cls._create_weekly_advice_business_processes()

    @classmethod
    def create_adhoc_advice_business_process(cls, counterparty, instrument_type, from_date, to_date):
        """
        Create an adhoc pre-settlement advice business process for
        the specified counterparty, instrument_type and date range.
        """
        # Allowing generation of pre-settlement advices for counterparties
        # who are not configured to receive scheduled advices.
        PreSettlementAdviceGeneral.validate_advice_date_range(from_date, to_date)
        cls._create_advice_business_process_for_counterparty_and_instrument_type(counterparty,
            instrument_type, from_date, to_date)

    @classmethod
    def create_missing_scheduled_advice_business_processes(cls):
        """
        Create any missing scheduled pre-settlement advice business
        processes.
        """
        cls._create_missing_weekly_advice_business_processes()

    @staticmethod
    def _should_create_weekly_advices():
        """
        Determine whether or not to create the weekly pre-settlement
        advices.
        """
        date_today = acm.Time.DateToday()
        return acm.Time.DayOfWeek(date_today) == 'Monday'

    @classmethod
    def _create_weekly_advice_business_processes(cls):
        """
        Create weekly pre-settlement advice business processes for
        the specified instrument types.
        """
        message = "Creating weekly pre-settlement advice business processes "
        message += "for date today '{date_today}'..."
        date_today = acm.Time.DateToday()
        LOGGER.info(message.format(
            date_today=date_today
        ))
        # Note: weekly advices show any settlements occurring during
        # the business week (Monday to Friday) two weeks from now.
        # Note: acm.Time.FirstDayOfWeek returns a Monday.
        first_day_of_week = acm.Time.FirstDayOfWeek(date_today)
        from_date = acm.Time.DateAddDelta(first_day_of_week, 0, 0, 14)
        to_date = acm.Time.DateAddDelta(first_day_of_week, 0, 0, 18)
        for instrument_type in PreSettlementAdviceGeneral.get_supported_advice_instrument_types():
            cls._create_instrument_type_advice_business_processes(instrument_type, from_date, to_date)
        LOGGER.info("Completed creating weekly pre-settlement advice business processes.")

    @classmethod
    def _create_missing_weekly_advice_business_processes(cls):
        """
        Create any missing weekly scheduled pre-settlement advice business
        processes.
        """
        # Note: weekly advices show any settlements occurring during
        # the business week (Monday to Friday) two weeks from now.
        # This implies that there can be at most three active weekly
        # advices:
        # - One for the date range of the current week (created two weeks ago).
        # - One for the date range of next week (created one week ago).
        # - One for the date range in two weeks time (created this week).
        #
        # Check advices present for each week.
        date_today = acm.Time.DateToday()
        from_date = acm.Time.FirstDayOfWeek(date_today)
        to_date = acm.Time.DateAddDelta(from_date, 0, 0, 4)
        for week in range(3):
            for instrument_type in PreSettlementAdviceGeneral.get_supported_advice_instrument_types():
                counterparties = PreSettlementAdviceGeneral.find_parties_receiving_advices_for_instrument_type(
                    instrument_type)
                for counterparty in counterparties:
                    cls._create_missing_weekly_advice_business_processes_for_counterparty_and_instrument_type(
                        counterparty, instrument_type, from_date, to_date)
            from_date = acm.Time.DateAddDelta(from_date, 0, 0, 7)
            to_date = acm.Time.DateAddDelta(to_date, 0, 0, 7)

    @classmethod
    def _create_missing_weekly_advice_business_processes_for_counterparty_and_instrument_type(cls, counterparty,
            instrument_type, from_date, to_date):
        """
        Create any missing weekly scheduled pre-settlement advice
        business processes for the specified counterparty, instrument
        type and date range.
        """
        message = "Checking counterparty '{counterparty_name}' for missing weekly scheduled "
        message += "'{instrument_type}' pre-settlement advice for the week of '{from_date}' "
        message += "to '{to_date}'..."
        LOGGER.info(message.format(
            counterparty_name=counterparty.Name(),
            instrument_type=instrument_type,
            from_date=from_date,
            to_date=to_date
        ))
        if cls._is_missing_weekly_scheduled_advice_business_process(counterparty, instrument_type, from_date,
                to_date):
            try:
                cls._create_advice_business_process_for_counterparty_and_instrument_type(counterparty,
                    instrument_type, from_date, to_date)
            except:
                # Prevent an exception during the generation of one advice
                # from preventing the creation of others.
                message = "An exception occurred creating the pre-settlement advice for counterparty "
                message += "'{counterparty_name}', skipping..."
                LOGGER.warning(message.format(
                    counterparty_name=counterparty.Name()
                ), exc_info=True)

    @classmethod
    def _is_missing_weekly_scheduled_advice_business_process(cls, counterparty, instrument_type, from_date, to_date):
        """
        Determine whether or not a counterparty is missing a
        scheduled pre-settlement advice for the specified instrument
        type and date range.
        """
        if to_date < acm.Time.DateToday():
            message = "Pre-settlement advice period has passed, skipping..."
            LOGGER.info(message.format(
                counterparty_name=counterparty.Name()
            ))
            return False
        if PreSettlementAdviceGeneral.advice_business_process_exists(counterparty, instrument_type,
                from_date, to_date):
            message = "Pre-settlement advice already exists for counterparty '{counterparty_name}'"
            message += ", skipping..."
            LOGGER.info(message.format(
                counterparty_name=counterparty.Name()
            ))
            return False
        if not PreSettlementAdviceGeneral.advice_money_flows_exist(counterparty, instrument_type,
                from_date, to_date):
            message = "No pre-settlement advice money flows found for counterparty '{counterparty_name}'"
            message += ", skipping..."
            LOGGER.info(message.format(
                counterparty_name=counterparty.Name()
            ))
            return False
        return True

    @classmethod
    def _create_instrument_type_advice_business_processes(cls, instrument_type, from_date, to_date):
        """
        Create pre-settlement advices for the specified instrument
        type and any counterparties with related money flows between
        the inclusive from date and inclusive to date and who are
        configured to receive such advices.
        """
        message = "Creating pre-settlement advices for instrument type '{instrument_type}'..."
        message = message.format(instrument_type=instrument_type)
        LOGGER.info(message)
        counterparties = PreSettlementAdviceGeneral.find_parties_receiving_advices_for_instrument_type(
            instrument_type)
        for counterparty in counterparties:
            if not PreSettlementAdviceGeneral.advice_money_flows_exist(counterparty, instrument_type,
                    from_date, to_date):
                message = "No pre-settlement advice money flows found for counterparty '{counterparty_name}'"
                message += ", skipping..."
                LOGGER.info(message.format(
                    counterparty_name=counterparty.Name()
                ))
                continue
            if PreSettlementAdviceGeneral.advice_business_process_exists(counterparty, instrument_type,
                    from_date, to_date):
                message = "Pre-settlement advice already exists for counterparty '{counterparty_name}'"
                message += ", skipping..."
                LOGGER.info(message.format(
                    counterparty_name=counterparty.Name()
                ))
                continue
            try:
                cls._create_advice_business_process_for_counterparty_and_instrument_type(counterparty,
                    instrument_type, from_date, to_date)
            except:
                # Prevent an exception during the generation of one advice
                # from preventing the creation of others.
                message = "An exception occurred creating the pre-settlement advice for counterparty "
                message += "'{counterparty_name}', skipping..."
                LOGGER.warning(message.format(
                    counterparty_name=counterparty.Name()
                ), exc_info=True)

    @classmethod
    def _create_advice_business_process_for_counterparty_and_instrument_type(cls, counterparty, instrument_type,
            from_date, to_date):
        """
        Create a pre-settlement advice for the specified counterparty,
        instrument type, inclusive from date and inclusive to date.

        This function should only be called if the counterparty has
        eligible money flows for the advice period.  If no money flows
        are found an exception will be raised.
        """
        cls._validate_instrument_type(instrument_type)
        cls._validate_advice_generation_permitted(counterparty)
        cls._validate_advice_money_flows_exist(counterparty, instrument_type, from_date, to_date)
        LOGGER.info("Creating pre-settlement advice business process for counterparty '{counterparty_name}'.".format(
            counterparty_name=counterparty.Name()
        ))
        PreSettlementAdviceGeneral.create_advice_business_process(counterparty, instrument_type, from_date, to_date)

    @staticmethod
    def _validate_advice_generation_permitted(counterparty):
        """
        Validate that a pre-settlement advice may be generated for
        the specified counterparty.
        """
        advice_party = counterparty.AddInfoValue(get_advice_party_add_info_name())
        if advice_party is None:
            return
        if advice_party == counterparty:
            return
        exception_message = "The party configured to receive pre-settlement advices for "
        exception_message += "'{counterparty_name}' is '{advice_party_name}'.\n\n"
        exception_message += "Please generate any advices against the configured party."
        exception_message = exception_message.format(
            counterparty_name=counterparty.Name(),
            advice_party_name=advice_party.Name()
        )
        raise ValueError(exception_message)

    @staticmethod
    def _validate_advice_money_flows_exist(counterparty, instrument_type, from_date, to_date):
        """
        Validate that pre-settlement advice money flows exist for the
        specified counterparty, instrument type, inclusive from date
        and inclusive to date.
        """
        if not PreSettlementAdviceGeneral.advice_money_flows_exist(counterparty, instrument_type,
                from_date, to_date):
            exception_message = "No pre-settlement advice money flows found for counterparty "
            exception_message += "'{counterparty_name}' and instrument type '{instrument_type}'."
            exception_message = exception_message.format(
                counterparty_name=counterparty.Name(),
                instrument_type=instrument_type
            )
            raise ValueError(exception_message)

    @staticmethod
    def _validate_instrument_type(instrument_type):
        """
        Validate an instrument type specified for pre-settlement advice
        creation.
        """
        if instrument_type is None:
            raise ValueError('An instrument type must be specified.')
        if instrument_type not in PreSettlementAdviceGeneral.get_supported_advice_instrument_types():
            raise ValueError('A supported instrument type must be specified.')
