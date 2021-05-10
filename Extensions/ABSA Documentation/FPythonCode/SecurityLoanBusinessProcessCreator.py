"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    SecurityBusinessProcessCreator

DESCRIPTION
    Creates Business Processes for Counterparty.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2020-01-31      FAOPS-557       Tawanda Mukhalela       Khaya Mbebe             Initial Implementation.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm
import SecurityLoanGeneral
from at_logging import getLogger

LOGGER = getLogger(__name__)


class SecurityLoanBusinessProcessCreator(object):
    """
    An object responsible for triggering the regular or adhoc
    generation of confirmations via the creation of
    SecurityLoan Confirmations business processes.
    """
    @classmethod
    def create_sec_loan_new_trade_business_processes(cls, counterparty, instrument_type,
                                                     document_type, date=acm.Time.DateToday()):
        """
        create Business process for counterparty
        """
        if cls._is_missing_business_process(counterparty, instrument_type, date, document_type):
            cls._create_business_processes(counterparty, date, document_type)

    @classmethod
    def _create_business_processes(cls, counterparty, date, document_type):
        """
        Create confirmation business processes for
        the specified instrument types.
        """
        if SecurityLoanGeneral.get_valid_trades_for_counterparty(counterparty, document_type):

            message = "Creating Confirmation business processes "
            message += "for date today '{date_today}'..."
            date_today = acm.Time.DateToday()
            LOGGER.info(message.format(
                date_today=date_today
            ))

            for instrument_type in SecurityLoanGeneral.get_supported_instrument_types():
                cls._create_confirmation_business_process_for_counterparty_and_instrument_type(counterparty,
                                                                                               instrument_type,
                                                                                               date,
                                                                                               document_type
                                                                                               )
            LOGGER.info("Completed creating business processes.")

    @classmethod
    def _is_missing_business_process(cls, counterparty, instrument_type, date, document_type):
        """
        Determine whether or not a counterparty is missing a
        confirmation for the specified instrument
        type and date range.
        """
        should_generate = False
        if SecurityLoanGeneral.confirmation_business_process_exists(counterparty, instrument_type, date, document_type):
            message = "Security Loan Confirmation already exists for counterparty '{counterparty_name}'"
            message += ", checking for any Updates ..."
            LOGGER.info(message.format(counterparty_name=counterparty.Name()))
            active_advice_business_processes = SecurityLoanGeneral.get_active_sec_loan_business_processes(
                counterparty, instrument_type, document_type)
            for business_process in active_advice_business_processes:
                if not SecurityLoanGeneral.is_in_updateable_state(business_process):
                    continue
                message = "Sent Security Loan Confirmation {oid} content will change if regenerated,"
                message += "triggering new confirmation generation."
                LOGGER.info(message.format(oid=business_process.Oid()))
                should_generate = True
        else:
            return True

        return should_generate

    @classmethod
    def _create_confirmation_business_process_for_counterparty_and_instrument_type(cls, counterparty, instrument_type,
                                                                                   date, document_type):
        """
        Create a confirmation for the specified counterparty,
        instrument type, inclusive from date which is always TODAY's date.
        Date might change for adhoc requests in the future.
        """
        cls._validate_instrument_type(instrument_type)
        cls._validate_confirmation_generation_permitted(counterparty, instrument_type)
        LOGGER.info("Creating SecurityLoan Confirmation business process for counterparty '{counterparty_name}'.".format(
            counterparty_name=counterparty.Name()
        ))
        SecurityLoanGeneral.create_sec_loan_business_process(counterparty, instrument_type, date, document_type)

    @staticmethod
    def _validate_confirmation_generation_permitted(counterparty, instrument_type):
        """
        Validate that a confirmation may be generated for
        the specified counterparty and instrument type.
        """
        is_counterparty_receiving_confirmations = SecurityLoanGeneral.is_party_receiving_confirmations(counterparty,
                                                                                                       instrument_type)
        if is_counterparty_receiving_confirmations is False:
            exception_message = "Counterparty {counterparty_name} does not have any "
            exception_message += "Contacts Setup To receive New Loan Confirmations."
            exception_message = exception_message.format(
                counterparty_name=counterparty.Name()
            )
            raise ValueError(exception_message)

    @staticmethod
    def _validate_instrument_type(instrument_type):
        """
        Validate an instrument type specified for confirmation
        creation.
        """
        if instrument_type is None:
            raise ValueError('An instrument type must be specified.')
        if instrument_type not in SecurityLoanGeneral.get_supported_instrument_types():
            raise ValueError('A supported instrument type must be specified.')
