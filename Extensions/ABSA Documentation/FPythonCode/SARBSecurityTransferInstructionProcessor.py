"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    SARBSecurityTransferInstructionProcessor

DESCRIPTION
    This module is used to define the implementation of a document processor for
    SARB security transfer instructions.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2020-05-04      FAOPS-746       Cuen Edwards            Kgomotso Gumbo          Initial implementation.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import traceback

import acm

from at_logging import getLogger
import gen_swift_functions
import DocumentBusinessProcessGeneral
from DocumentGeneral import Formats
from DocumentProcessor import DocumentProcessor
import SARBSecurityTransferInstructionGeneral
from SARBSecurityTransferInstructionGeneral import EventNames, ParameterNames, StateNames



LOGGER = getLogger(__name__)


class SARBSecurityTransferInstructionProcessor(DocumentProcessor):
    """
    A document processor for SARB security transfer instructions.
    """

    def get_name(self):
        """
        Get the name of the document processor.
        """
        return 'SARB Security Transfer Instruction Processor'

    def is_processable(self, business_process):
        """
        Determines whether or not the processor would perform any
        automated processing on a specified SARB security transfer
        instruction business process.
        """
        current_state_name = business_process.CurrentStateName()
        return current_state_name in [
            StateNames.PENDING_GENERATION,
            StateNames.GENERATED,
            StateNames.PENDING_SENDING
        ]

    def process(self, business_process):
        """
        Perform any automated processing on a SARB security transfer
        instruction business process.
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
        Get the formats supported for a SARB security transfer
        instruction.
        """
        return [
            Formats.MT,
            Formats.XML
        ]

    def document_format_available(self, business_process, document_format):
        """
        Determines whether or not a SARB security transfer
        instruction is available for retrieval, viewing, etc. in a
        specified format.
        """
        return SARBSecurityTransferInstructionGeneral.has_been_generated(business_process)

    def render_document_file(self, business_process, document_format):
        """
        Render a SARB security transfer instruction to file in the
        specified format and return the file path.
        """
        if document_format == Formats.MT:
            return SARBSecurityTransferInstructionGeneral.generate_instruction_mt_file(business_process)
        elif document_format == Formats.XML:
            return SARBSecurityTransferInstructionGeneral.generate_instruction_xml_file(business_process)
        raise ValueError("Unsupported document format '{document_format}' specified.".format(
            document_format=document_format
        ))

    @classmethod
    def is_handled_swift_ack_nack(cls, mt_message):
        """
        Determine whether or not the specified SWIFT MT message is
        an Ack/Nack for a SARB security transfer instruction MT199.
        """
        message_function = gen_swift_functions.get_msg_function(mt_message)
        if message_function != 'F21':
            # Not an Ack/Nack message.
            return False
        message_type = gen_swift_functions.get_msg_type(mt_message)
        if message_type != '199':
            # Not an Ack/Nack for an MT199.
            return False
        reference = gen_swift_functions.get_text_from_tag(':108:', mt_message)
        return reference.startswith(SARBSecurityTransferInstructionGeneral.REFERENCE_PREFIX)

    @classmethod
    def handle_swift_ack_nack(cls, mt_message):
        """
        Handle the specified SWIFT Ack/Nack MT message for a SARB
        security transfer instruction MT199.
        """
        reference = gen_swift_functions.get_text_from_tag(':108:', mt_message)
        business_process = cls._get_instruction_business_process(reference)
        if business_process.CurrentStateName() != StateNames.SENT:
            state_chart_name = SARBSecurityTransferInstructionGeneral.get_instruction_state_chart_name()
            error_message = "'{state_chart_name}' business process {reference} is not in '{state}' state."
            raise ValueError(error_message.format(
                state_chart_name=state_chart_name,
                reference=reference,
                state=StateNames.SENT
            ))
        acm.BeginTransaction()
        try:
            cls._handle_swift_ack_nack(business_process, mt_message)
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
            next_event = None
            parameters = None
            notes = acm.FArray()
            if cls._should_be_cancelled(business_process):
                next_event = EventNames.CANCEL
                notes.Add("SARB security transfer instruction is no longer required - cancelling.")
            else:
                next_event = EventNames.GENERATED
                parameters = cls._generate(business_process)
            business_process.HandleEvent(next_event, parameters, notes)
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
            if SARBSecurityTransferInstructionGeneral.should_automatically_send():
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
        Generate the SARB security transfer instruction document
        formats and return any parameters to be sent with the next
        business process event.
        """
        event_name = DocumentBusinessProcessGeneral.get_business_process_event(business_process)
        xml_content = SARBSecurityTransferInstructionGeneral.generate_instruction_xml_content(business_process)
        mt_content = SARBSecurityTransferInstructionGeneral.generate_instruction_mt_content(xml_content)
        parameters = acm.FDictionary()
        parameters[ParameterNames.XML_URL] = SARBSecurityTransferInstructionGeneral.store_instruction_content(
            event_name, xml_content, Formats.XML)
        parameters[ParameterNames.MT_URL] = SARBSecurityTransferInstructionGeneral.store_instruction_content(
            event_name, mt_content, Formats.MT)
        return parameters

    @staticmethod
    def _should_be_cancelled(business_process):
        """
        Determine whether or not a SARB security transfer instruction
        should be cancelled by determining whether or not there are no
        security transfers eligible to appear on the advice.
        """
        event_name = DocumentBusinessProcessGeneral.get_business_process_event(business_process)
        transfer_date = DocumentBusinessProcessGeneral.get_business_process_date(business_process)
        return not SARBSecurityTransferInstructionGeneral.security_transfers_exist(event_name, transfer_date)

    @staticmethod
    def _ensure_last_generated_content_not_empty(business_process):
        """
        Ensure that the last generated version of a SARB security
        transfer instruction is not empty.

        This is used to guard against race-conditions that may result
        in the creation of a SARB security transfer instruction being
        triggered due to settlements initially existing and then those
        settlements no longer existing at the time of generation.
        """
        last_generated_xml_content = (SARBSecurityTransferInstructionGeneral
            .retrieve_last_generated_instruction_xml_content(business_process))
        if SARBSecurityTransferInstructionGeneral.content_is_empty(last_generated_xml_content):
            raise ValueError("SARB security transfer instruction contains no settlements.")

    @staticmethod
    def _send(business_process):
        """
        Send the SARB security transfer instruction and return any
        parameters to be sent with the next business process event.
        """
        # Importing inside function as pymqi module not generally
        # available for PRIME users.
        from gen_absa_xml_config_settings import MqXmlConfig
        import gen_mq
        mq_xml_config_name = 'MeridianOutCustMq'
        mq_xml_config = MqXmlConfig(mq_xml_config_name)
        queue_manager = mq_xml_config.QueueManager
        connection_name = mq_xml_config.Client
        channel_name = mq_xml_config.Channel
        queue_name = mq_xml_config.QueueName
        mt_message = SARBSecurityTransferInstructionGeneral.retrieve_last_generated_instruction_mt_content(
            business_process)
        mq_messenger = gen_mq.MqMessenger(mq_xml_config_name)
        mq_messenger.Put(mt_message)
        parameters = acm.FDictionary()
        parameters[ParameterNames.MQ_QUEUE_MANAGER] = queue_manager
        parameters[ParameterNames.MQ_CONNECTION_NAME] = connection_name
        parameters[ParameterNames.MQ_CHANNEL_NAME] = channel_name
        parameters[ParameterNames.MQ_QUEUE_NAME] = queue_name
        return parameters

    @staticmethod
    def _get_instruction_business_process(reference):
        """
        Get the SARB security transfer instruction related to the
        specified MT199 message reference.
        """
        business_process_oid = int(reference.replace(SARBSecurityTransferInstructionGeneral.REFERENCE_PREFIX, ''))
        business_process = acm.FBusinessProcess[business_process_oid]
        state_chart_name = SARBSecurityTransferInstructionGeneral.get_instruction_state_chart_name()
        if business_process is None or business_process.StateChart().Name() != state_chart_name:
            error_message = "No '{state_chart_name}' business process found for reference {reference}."
            raise ValueError(error_message.format(
                state_chart_name=state_chart_name,
                reference=reference
            ))
        return business_process

    @staticmethod
    def _handle_swift_ack_nack(business_process, mt_message):
        """
        Handle the specified SWIFT Ack/Nack MT message for a SARB
        security transfer instruction MT199.
        """
        try:
            next_event = None
            parameters = None
            ack_nack = gen_swift_functions.get_text_from_tag(':451:', mt_message)
            if ack_nack == '0':
                next_event = EventNames.ACKNOWLEDGED
            else:
                next_event = EventNames.NOT_ACKNOWLEDGED
                error_code = gen_swift_functions.get_text_from_tag(':405:', mt_message)
                parameters = acm.FDictionary()
                parameters[ParameterNames.SWIFT_ERROR_CODE] = error_code
            notes = acm.FArray()
            notes.Add(mt_message)
            business_process.HandleEvent(next_event, parameters, notes)
            business_process.Commit()
        except Exception as exception:
            LOGGER.exception(exception)
            business_process.ForceToErrorState(traceback.format_exc())
            business_process.Commit()
