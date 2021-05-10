"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    PreSettlementAdviceProcessor

DESCRIPTION
    This module is used to define the implementation of a document processor for
    pre-settlement advices.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-09-17      FAOPS-460       Cuen Edwards            Letitia Carboni         Initial Implementation.
2019-10-14      FAOPS-531       Cuen Edwards            Letitia Carboni         Added support for amendments.
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
import PreSettlementAdviceGeneral
from PreSettlementAdviceGeneral import EventNames, ParameterNames, StateNames



LOGGER = getLogger(__name__)


class PreSettlementAdviceProcessor(DocumentProcessor):
    """
    A document processor for pre-settlement advices.
    """

    def get_name(self):
        """
        Get the name of the document processor.
        """
        return '{event_name} Processor'.format(
            event_name=PreSettlementAdviceGeneral.get_advice_event_name()
        )

    def is_processable(self, business_process):
        """
        Determines whether or not the processor would perform any
        automated processing on a specified pre-settlement advice
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
        Perform any automated processing on a pre-settlement advice
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
        Get the formats supported for a pre-settlement advice.
        """
        return [
            Formats.XML,
            Formats.XLSX
        ]

    def document_format_available(self, business_process, document_format):
        """
        Determines whether or not a pre-settlement advice is available
        for retrieval, viewing, etc. in a specified format.
        """
        return PreSettlementAdviceGeneral.has_been_generated(business_process)

    def render_document_file(self, business_process, document_format):
        """
        Render a pre-settlement advice to file in the specified format
        and return the file path.
        """
        if document_format == Formats.XML:
            return PreSettlementAdviceGeneral.generate_advice_xml_file(business_process)
        elif document_format == Formats.XLSX:
            return PreSettlementAdviceGeneral.generate_advice_xlsx_file(business_process)
        raise ValueError("Unsupported document format '{document_format}' specified.".format(
            document_format=document_format
        ))

    @classmethod
    def check_for_updates(cls, business_process):
        """
        Determine whether or not a pre-settlement advice needs to be
        updated and, if so, trigger the regeneration.
        """
        acm.BeginTransaction()
        try:
            cls._check_for_updates(business_process)
            acm.CommitTransaction()
        except:
            acm.AbortTransaction()
            raise

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
                notes.Add("Regenerated pre-settlement advice is the same as last version sent.")
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
            cls._ensure_last_generated_content_not_empty(business_process)
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
        Generate the pre-settlement advice document formats and return
        any parameters to be sent with the next business process event.
        """
        xml_content = PreSettlementAdviceGeneral.generate_advice_xml_content(business_process,
            show_amendments=True)
        xlsx_content = PreSettlementAdviceGeneral.generate_advice_xlsx_content(xml_content)
        parameters = acm.FDictionary()
        parameters[ParameterNames.XML_URL] = PreSettlementAdviceGeneral.store_advice_content(
            xml_content, Formats.XML)
        parameters[ParameterNames.XLSX_URL] = PreSettlementAdviceGeneral.store_advice_content(
            xlsx_content, Formats.XLSX)
        return parameters

    @classmethod
    def _last_generated_content_matches_last_content_sent(cls, business_process):
        """
        Determine whether or not the last generated version of a pre-
        settlement advice is the same as any last version that has
        already been sent.
        """
        last_sent_xml_content = PreSettlementAdviceGeneral.retrieve_last_sent_advice_xml_content(business_process)
        if last_sent_xml_content is None:
            return False
        last_generated_xml_content = PreSettlementAdviceGeneral.retrieve_last_generated_advice_xml_content(
            business_process)
        return not PreSettlementAdviceGeneral.content_differs(last_sent_xml_content, last_generated_xml_content)

    @staticmethod
    def _should_automatically_send(business_process):
        """
        Determine whether or not a pre-settlement advice should be
        automatically sent.
        """
        return PreSettlementAdviceGeneral.should_automatically_send()

    @staticmethod
    def _ensure_last_generated_content_not_empty(business_process):
        """
        Ensure that the last generated version of a pre-settlement
        advice is not empty.

        This is used to guard against race-conditions that may result
        in the creation of a pre-settlement advice being triggered
        due to settlements initially existing and then those
        settlements no longer existing at the time of generation.
        """
        last_generated_xml_content = PreSettlementAdviceGeneral.retrieve_last_generated_advice_xml_content(
            business_process)
        if PreSettlementAdviceGeneral.content_is_empty(last_generated_xml_content):
            raise ValueError("Pre-settlement advice contains no settlements.")

    @staticmethod
    def _send(business_process):
        """
        Send the pre-settlement advice and return any parameters to
        be sent with the next business process event.
        """
        # Unfortunately need to create a temp file if we use the EmailHelper...
        xlsx_file_path = None
        try:
            bank_contact = PreSettlementAdviceGeneral.get_bank_contact(business_process)
            counterparty_contact = PreSettlementAdviceGeneral.get_counterparty_contact(business_process)
            from_name = PreSettlementAdviceGeneral.get_email_from_name(bank_contact)
            from_telephone = PreSettlementAdviceGeneral.get_email_from_telephone(bank_contact)
            from_email_address = PreSettlementAdviceGeneral.get_email_from_address(bank_contact)
            to_email_addresses = PreSettlementAdviceGeneral.get_email_to_addresses(counterparty_contact)
            bcc_email_addresses = PreSettlementAdviceGeneral.get_email_bcc_addresses(bank_contact)
            email_subject = PreSettlementAdviceGeneral.get_email_subject(business_process)
            email_body = PreSettlementAdviceGeneral.get_email_body(from_name, from_telephone, from_email_address,
                business_process)
            xlsx_file_path = PreSettlementAdviceGeneral.generate_advice_xlsx_file(business_process)
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

    @classmethod
    def _check_for_updates(cls, business_process):
        """
        Perform the check to determine whether or not a pre-settlement
        advice needs to be updated and, if so, trigger the regeneration.
        """
        try:
            LOGGER.info("Checking pre-settlement advice {oid} for updates...".format(
                oid=business_process.Oid()
            ))
            if not PreSettlementAdviceGeneral.is_in_updateable_state(business_process):
                message = "Pre-settlement advice {oid} is not in an update-able state, "
                message += "nothing to update."
                LOGGER.info(message.format(
                    oid=business_process.Oid()
                ))
                return
            if PreSettlementAdviceGeneral.advice_should_be_cancelled(business_process):
                message = "Pre-settlement advice {oid} has not been sent and would be empty "
                message += "if regenerated, triggering cancellation."
                LOGGER.info(message.format(
                    oid=business_process.Oid()
                ))
                notes = acm.FArray()
                notes.Add('Pre-settlement advice has not been sent and is no longer required - cancelling.')
                business_process.HandleEvent(EventNames.CANCEL, None, notes)
                business_process.Commit()
            elif PreSettlementAdviceGeneral.advice_should_be_regenerated(business_process):
                message = "Pre-settlement advice {oid} content will change if regenerated, "
                message += "triggering regeneration."
                LOGGER.info(message.format(
                    oid=business_process.Oid()
                ))
                notes = acm.FArray()
                notes.Add('Pre-settlement advice update required - regenerating.')
                business_process.HandleEvent(EventNames.REGENERATE, None, notes)
                business_process.Commit()
            else:
                message = "Pre-settlement advice {oid} content will not change if regenerated, "
                message += "nothing to update."
                LOGGER.info(message.format(
                    oid=business_process.Oid()
                ))
        except Exception as exception:
            LOGGER.exception(exception)
            business_process.ForceToErrorState(traceback.format_exc())
            business_process.Commit()
