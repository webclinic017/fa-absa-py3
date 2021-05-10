"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    BrokerNoteBulkProcessor

DESCRIPTION
    This module is used to define the implementation of a document processor for
    broker notes.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2020-04-29      FAOPS-702       Joash Moodley                                   xls broker notes via business process.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import os
import traceback

import acm

from at_email import EmailHelper
from at_logging import getLogger
import DocumentGeneral
from DocumentGeneral import Formats
from DocumentProcessor import DocumentProcessor
import BrokerNoteBulkGeneral
from BrokerNoteBulkGeneral import EventNames, ParameterNames, StateNames


LOGGER = getLogger(__name__)


class BrokerNoteBulkProcessor(DocumentProcessor):
    """
    A document processor for broker notes.
    """

    def get_name(self):
        """
        Get the name of the document processor.
        """
        return '{event_name} Processor'.format(
            event_name=BrokerNoteBulkGeneral.get_broker_note_event_name()
        )

    def is_processable(self, business_process):
        """
        Determines whether or not the processor would perform any
        automated processing on a specified broker note
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
        Perform any automated processing on a broker note
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
        Get the formats supported for a broker note.
        """
        return [
            Formats.XML,
            Formats.XLSX
        ]

    def document_format_available(self, business_process, document_format):
        """
        Determines whether or not a broker note is available
        for retrieval, viewing, etc. in a specified format.
        """
        return BrokerNoteBulkGeneral.has_been_generated(business_process)

    def render_document_file(self, business_process, document_format):
        """
        Render a broker note to file in the specified format
        and return the file path.
        """
        if document_format == Formats.XML:
            return BrokerNoteBulkGeneral.generate_broker_note_xml_file(business_process)
        elif document_format == Formats.XLSX:
            return BrokerNoteBulkGeneral.generate_broker_note_xlsx_file(business_process)
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
                notes.Add("Regenerated broker note is the same as last version sent.")
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
        Generate the broker note document formats and return
        any parameters to be sent with the next business process event.
        """
        xml_content = BrokerNoteBulkGeneral.generate_broker_note_xml_content(
            business_process
        )
        xlsx_content = BrokerNoteBulkGeneral.generate_broker_note_xlsx_content(xml_content)
        parameters = acm.FDictionary()
        parameters[ParameterNames.XML_URL] = BrokerNoteBulkGeneral.store_broker_note_content(
            xml_content, Formats.XML)
        parameters[ParameterNames.XLSX_URL] = BrokerNoteBulkGeneral.store_broker_note_content(
            xlsx_content, Formats.XLSX)
        return parameters

    @classmethod
    def _last_generated_content_matches_last_content_sent(cls, business_process):
        """
        Determine whether or not the last generated version of a broker note is the same as any last version that has
        already been sent.
        """
        last_sent_xml_content = BrokerNoteBulkGeneral.retrieve_last_sent_broker_note_xml_content(business_process)

        if last_sent_xml_content is None:
            return False
        last_generated_xml_content = BrokerNoteBulkGeneral.retrieve_last_generated_broker_note_xml_content(
            business_process)
        if not BrokerNoteBulkGeneral.broker_note_xml_differs(last_sent_xml_content, last_generated_xml_content):
            return True
        return False

    @staticmethod
    def _should_automatically_send(business_process):
        """
        Determine whether or not a broker note should be
        automatically sent.
        """
        return BrokerNoteBulkGeneral.should_automatically_send()

    @staticmethod
    def _send(business_process):
        """
        Send the broker note and return any parameters to
        be sent with the next business process event.
        """
        # Unfortunately need to create a temp file if we use the EmailHelper...
        xlsx_file_path = None
        try:
            bank_contact = BrokerNoteBulkGeneral.get_bank_contact(business_process)
            acquirer_contact = BrokerNoteBulkGeneral.get_acquirer(business_process)
            counterparty_contact = BrokerNoteBulkGeneral.get_counterparty_contact(business_process)
            from_name = BrokerNoteBulkGeneral.get_email_from_name(acquirer_contact)
            from_telephone = BrokerNoteBulkGeneral.get_email_from_telephone(acquirer_contact)
            from_email_address = BrokerNoteBulkGeneral.get_email_from_address(acquirer_contact)
            to_email_addresses = BrokerNoteBulkGeneral.get_email_to_addresses(counterparty_contact)
            bcc_email_addresses = BrokerNoteBulkGeneral.get_email_bcc_addresses(acquirer_contact)
            email_subject = BrokerNoteBulkGeneral.get_email_subject(business_process)
            email_body = BrokerNoteBulkGeneral.get_email_body(from_name, from_telephone, from_email_address,
                business_process)
            xlsx_file_path = BrokerNoteBulkGeneral.generate_broker_note_xlsx_file(business_process)
            attachments = [xlsx_file_path]
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
            if xlsx_file_path and os.path.exists(xlsx_file_path):
                os.remove(xlsx_file_path)
