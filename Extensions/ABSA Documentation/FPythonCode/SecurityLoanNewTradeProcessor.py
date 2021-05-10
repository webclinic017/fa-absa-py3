"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    SecurityLoanNewTradeProcessor

DESCRIPTION
    Processes FBusinessProcess events to determine if any business processes can be generated/updated
    for SecurityLoan Confirmations

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2020-01-31      FAOPS-557       Tawanda Mukhalela       Khaya Mbebe             Initial Implementation.
-----------------------------------------------------------------------------------------------------------------------------------------
"""
import os
import acm
import traceback
import DocumentGeneral
import SecurityLoanGeneral
from at_email import EmailHelper
from at_logging import getLogger
from DocumentGeneral import Formats
from DocumentProcessor import DocumentProcessor
from SecurityLoanGeneral import EventNames, ParameterNames, StateNames

LOGGER = getLogger(__name__)


class SecurityLoanNewTradeProcessor(DocumentProcessor):
    """
    A document processor for SecurityLoan Confirmation.
    """

    def get_name(self):
        """
        Get the name of the document processor.
        """
        return '{event_name} Processor'.format(
            event_name=SecurityLoanGeneral.get_event_name()
        )

    def is_processable(self, business_process):
        """
        Determines whether or not the processor would perform any
        automated processing on a specified SecurityLoan Confirmation
        business process.
        """
        current_state_name = business_process.CurrentStateName()
        return current_state_name in [
            StateNames.PENDING_GENERATION,
            StateNames.GENERATED,
            StateNames.PENDING_SENDING
        ]

    def process(self, business_process):
        """
        Perform any automated processing on a SecurityLoan Confirmation
        business process.
        """
        acm.BeginTransaction()
        try:
            current_state_name = business_process.CurrentStateName()
            if current_state_name == StateNames.PENDING_GENERATION:
                self._process_pending_generation_state(business_process)
            elif current_state_name == StateNames.GENERATED:
                self._process_generated_state(business_process)
            elif current_state_name == StateNames.PENDING_SENDING:
                self._process_pending_sending_state(business_process)
            else:
                raise RuntimeError('Unsupported business process state encountered.')
            acm.CommitTransaction()
        except:
            acm.AbortTransaction()
            raise

    def get_supported_formats(self):
        """
        Get the formats supported for a SecurityLoan Confirmation.
        """
        return [
            Formats.XML,
            Formats.PDF
        ]

    def document_format_available(self, business_process, document_format):
        """
        Determines whether or not a SecurityLoan Confirmation is available
        for retrieval, viewing, etc. in a specified format.
        """
        return SecurityLoanGeneral.has_been_generated(business_process)

    def render_document_file(self, business_process, document_format):
        """
        Render a SecurityLoan Confirmation to file in the specified format
        and return the file path.
        """
        if document_format == Formats.XML:
            return SecurityLoanGeneral.generate_sec_loan_xml_file(business_process)
        elif document_format == Formats.PDF:
            return SecurityLoanGeneral.generate_sec_loan_pdf_file(business_process)
        raise ValueError("Unsupported document format '{document_format}' specified.".format(
            document_format=document_format
        ))

    @classmethod
    def _process_pending_generation_state(cls, business_process):
        """
        Perform the processing for a document business process in the
        'Pending Generation' state.
        """
        try:
            parameters = cls._generate(business_process)
            business_process.HandleEvent(EventNames.GENERATED, parameters)
            business_process.Commit()
        except Exception as exception:
            LOGGER.exception(exception)
            notes = acm.FArray()
            notes.Add(traceback.format_exc())
            business_process.HandleEvent(EventNames.GENERATION_FAILED, None, notes)
            business_process.Commit()

    @classmethod
    def _process_generated_state(cls, business_process):
        """
        Perform the processing for a document business process in the
        'Generated' state.
        """
        try:
            next_event = None
            notes = acm.FArray()
            if cls._last_generated_content_matches_last_content_sent(business_process):
                # Regenerated content is the same as last version sent.
                next_event = EventNames.SENT
                notes.Add("Regenerated Security Loan Confirmation is the same as last version sent.")
            else:
                # Not previous sent or content differs.
                if cls._should_automatically_send(business_process):
                    next_event = EventNames.SEND
                    notes.Add("STP enabled - sending.")
                else:
                    next_event = EventNames.HOLD
                    notes.Add("STP disabled - holding.")
            business_process.HandleEvent(next_event, None, notes)
            business_process.Commit()
        except Exception as exception:
            LOGGER.exception(exception)
            business_process.ForceToErrorState(traceback.format_exc())
            business_process.Commit()

    @classmethod
    def _process_pending_sending_state(cls, business_process):
        """
        Perform the processing for a document business process in the
        'Pending Sending' state.
        """
        try:
            parameters = cls._send(business_process)
            business_process.HandleEvent(EventNames.SENT, parameters)
            business_process.Commit()
        except Exception as exception:
            LOGGER.exception(exception)
            notes = acm.FArray()
            notes.Add(traceback.format_exc())
            business_process.HandleEvent(EventNames.SENDING_FAILED, None, notes)
            business_process.Commit()

    @staticmethod
    def _generate(business_process):
        """
        Generate the SecurityLoan Confirmation document formats and return
        any parameters to be sent with the next business process event.
        """
        xml_content = SecurityLoanGeneral.generate_confirmation_xml_content(business_process)
        pdf_content = SecurityLoanGeneral.generate_confirmation_pdf_content(xml_content)
        parameters = acm.FDictionary()
        parameters[ParameterNames.XML_URL] = SecurityLoanGeneral.store_confirmation_content(xml_content, Formats.XML)
        parameters[ParameterNames.PDF_URL] = SecurityLoanGeneral.store_confirmation_content(pdf_content, Formats.PDF)

        acm.BeginTransaction()
        try:
            SecurityLoanGeneral.update_sl_confirmation_sent_on_trades(xml_content)
            SecurityLoanGeneral.add_confirmation_oid_on_trades(xml_content, business_process)
            acm.CommitTransaction()
        except:
            acm.AbortTransaction()
            raise
        return parameters

    @classmethod
    def _last_generated_content_matches_last_content_sent(cls, business_process):
        """
        Determine whether or not the last generated version of a SecurityLoan
        Confirmation is the same as any last version that has
        already been sent.
        """
        last_sent_xml_content = SecurityLoanGeneral.retrieve_last_sent_confirmation_xml_content(business_process)
        if last_sent_xml_content is None:
            return False
        last_generated_xml_content = SecurityLoanGeneral.retrieve_last_generated_confirmation_xml_content(
            business_process)
        return not SecurityLoanGeneral.content_differs(last_sent_xml_content, last_generated_xml_content)

    @staticmethod
    def _should_automatically_send(business_process):
        """
        Determine whether or not a SecurityLoan Confirmation should be
        automatically sent.
        """
        return SecurityLoanGeneral.should_automatically_send()

    @staticmethod
    def _send(business_process):
        """
        Send the SecurityLoan Confirmation and return any parameters to
        be sent with the next business process event.
        """
        # Unfortunately need to create a temp file if we use the EmailHelper...
        pdf_file_path = None
        try:
            bank_contact = SecurityLoanGeneral.get_bank_contact(business_process)
            counterparty_contact = SecurityLoanGeneral.get_counterparty_contact(business_process)
            from_name = SecurityLoanGeneral.get_email_from_name(bank_contact)
            from_telephone = SecurityLoanGeneral.get_email_from_telephone(bank_contact)
            from_email_address = SecurityLoanGeneral.get_email_from_address(bank_contact)
            to_email_addresses = SecurityLoanGeneral.get_email_to_addresses(counterparty_contact)
            bcc_email_addresses = SecurityLoanGeneral.get_email_bcc_addresses(bank_contact)
            email_subject = SecurityLoanGeneral.get_email_subject(business_process)
            email_body = SecurityLoanGeneral.get_email_body(from_name, from_telephone, from_email_address,
                business_process)
            pdf_file_path = SecurityLoanGeneral.generate_sec_loan_pdf_file(business_process)
            attachments = [pdf_file_path]
            mail_from = from_email_address
            mail_to = DocumentGeneral.split_email_addresses(to_email_addresses)
            mail_bcc = DocumentGeneral.split_email_addresses(bcc_email_addresses)
            email_helper = EmailHelper(body=email_body, subject=email_subject, mail_to=mail_to,
                mail_from=mail_from, attachments=attachments, body_type=EmailHelper.BODY_TYPE_HTML,
                sender_type=EmailHelper.SENDER_TYPE_SMTP, host=EmailHelper.get_acm_host(),
                mail_bcc=mail_bcc)
            failures = email_helper.send()
            parameters = acm.FDictionary()
            parameters[ParameterNames.BANK_CONTACT] = bank_contact.Fullname()
            parameters[ParameterNames.COUNTERPARTY_CONTACT] = counterparty_contact.Fullname()
            parameters[ParameterNames.FROM_EMAIL_ADDRESS] = from_email_address
            parameters[ParameterNames.TO_EMAIL_ADDRESSES] = to_email_addresses
            parameters[ParameterNames.BCC_EMAIL_ADDRESSES] = bcc_email_addresses
            parameters[ParameterNames.EMAIL_SUBJECT] = email_subject
            if failures:
                parameters[ParameterNames.EMAIL_FAILURES] = str(failures)
            return parameters
        finally:
            if pdf_file_path and os.path.exists(pdf_file_path):
                os.remove(pdf_file_path)
