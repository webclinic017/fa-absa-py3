"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    SecurityLoanNewTradeEventHandler

DESCRIPTION
    Processes trade events to determine if any business processes can be generated for SecurityLoan
    Confirmations

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
from DocumentEventHandler import DocumentEventHandler
from SecurityLoanBusinessProcessCreator import SecurityLoanBusinessProcessCreator

LOGGER = getLogger(__name__)


class SecurityLoanNewTradeEventHandler(DocumentEventHandler):
    """
    Definition of an event-handler for SecurityLoan Confirmation.
    """

    def get_name(self):
        """
        Get the name of the Document Event Handler.
        """
        return '{event_name} Event Handler'.format(
            event_name=SecurityLoanGeneral.get_event_name()
        )

    def handles(self, message, event_object):
        """
        Determine whether or not to trigger the event handler for an
        event on the specified object.
        """
        if self._is_security_loan_trade_event(message, event_object):
            return True
        return False

    def handle_event(self, message, event_object):
        """
        Perform any event handling.
        """
        if event_object.IsKindOf(acm.FTrade):
            self._handle_security_loan_trade_event(message, event_object)
        else:
            raise ValueError('Unsupported event object {event_object_class} {event_object_oid} specified.'.format(
                event_object_class=event_object.ClassName(),
                event_object_oid=event_object.Oid()
            ))

    @classmethod
    def _is_security_loan_trade_event(cls, message, event_object):
        """
        Determine whether or not an event is for a SecurityLoan Confirmation trade.
        """
        if not event_object.IsKindOf(acm.FTrade):
            return False
        # All operations - check if the current state of the event object is eligible.
        if SecurityLoanGeneral.is_trade_eligible_for_confirmation(event_object):
            return True

        return False

    def _handle_security_loan_trade_event(self, message, trade):
        """
        Perform any event handling for a SecurityLoan Confirmation
        trade.
        """
        counterparty = SecurityLoanGeneral.get_lender_or_borrower_party(trade)
        instrument_type = trade.Instrument().InsType()
        document_type = trade.Text1()
        if counterparty:
            if not SecurityLoanGeneral.is_party_receiving_confirmations(counterparty, instrument_type):
                LOGGER.info("{party} is not setup to receive any confirmations".format(party=counterparty.Name()))
                return
            if self._is_update_operation(message):
                if trade.AdditionalInfo().SL_ConfirmationSent() is True:
                    if self.check_valid_message_changes(message):
                        self._check_trade_for_confirmation_updates(trade)

            if trade.AdditionalInfo().SL_ConfirmationSent() in [None, False]:
                self._check_for_missing_confirmations(counterparty, instrument_type, document_type)
            else:
                LOGGER.info("Trade {trade} not valid for confirmation Creation".format(trade=trade.Oid()))
        else:
            LOGGER.info("No Valid Counterparty found on Trade {trade}".format(trade=trade.Oid()))

    @classmethod
    def _is_update_operation(cls, message):
        """
        Determine whether or not the operation which triggered an
        event was an update.
        """
        return cls._get_event_operation(message) == 'UPDATE'

    @classmethod
    def _get_event_operation(cls, message):
        """
        Get the event operation that triggered the generation of
        specified AMBA message.
        """
        event_type_message = message.mbf_find_object('TYPE', 'MBFE_BEGINNING')
        event_type = event_type_message.mbf_get_value()
        index_of_underscore = event_type.index('_')
        return event_type[0: index_of_underscore]

    @classmethod
    def check_valid_message_changes(cls, message):
        """
        Returns True if the update is valid for an amentment
        """
        trade_message = SecurityLoanGeneral.find_first_mbf_child_object(message, 'TRADE', '!')
        if trade_message:
            quantity = SecurityLoanGeneral.find_first_mbf_child_object(trade_message, 'QUANTITY', '!')
            if quantity:
                LOGGER.info('Quantity Changed!')
                LOGGER.info(quantity.mbf_object_to_string())
                return True

            additional_info_message = SecurityLoanGeneral.find_first_mbf_child_object(trade_message,
                                                                                      'ADDITIONALINFO',
                                                                                      '!')
            if additional_info_message:
                updated_filed = SecurityLoanGeneral.find_first_mbf_child_object(additional_info_message,
                                                                                'ADDINF_SPECNBR.FIELD_NAME'
                                                                                )
                if updated_filed.mbf_get_value() in ['SL_G1Fee2', 'SL_SWIFT', 'SL_Minimum_Fee']:
                    LOGGER.info('Crucial Add Info Changed!')
                    LOGGER.info(updated_filed.mbf_get_value())
                    return True

        return False

    @classmethod
    def _check_trade_for_confirmation_updates(cls, trade):
        """
        Check the specified counterparty to determine if any
        updates are required.
        """
        instrument_type = trade.Instrument().InsType()
        instrument_types = SecurityLoanGeneral.get_supported_instrument_types()
        for instrument_type in instrument_types:
            # Update any existing confirmations
            SecurityLoanGeneral.check_for_confirmation_updates(trade, instrument_type)

    @classmethod
    def _check_for_missing_confirmations(cls, counterparty, instrument_type, document_type):
        """
        Check the specified counterparty to determine if any missing
        confirmations need to be created for the given instrument type
        and, if so, trigger the creation.
        """
        message = "Checking counterparty '{counterparty_name}' for missing"
        message += " '{instrument_type}' Confirmations..."
        LOGGER.info(message.format(
            counterparty_name=counterparty.Name(),
            instrument_type=instrument_type
        ))
        if not SecurityLoanGeneral.are_party_trades_eligible_for_confirmation(counterparty, document_type):
            message = "Counterparty '{counterparty_name}' is not (or no longer) eligible "
            message += "to receive '{instrument_type}' Confirmations, no "
            message += "Confirmations should be generated."
            LOGGER.info(message.format(
                counterparty_name=counterparty.Name(),
                instrument_type=instrument_type
            ))
            return

        SecurityLoanBusinessProcessCreator().create_sec_loan_new_trade_business_processes(
            counterparty, instrument_type, document_type)
