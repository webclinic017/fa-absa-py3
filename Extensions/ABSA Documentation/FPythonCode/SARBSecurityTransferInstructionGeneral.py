"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    SARBSecurityTransferInstructionGeneral

DESCRIPTION
    This module contains general functionality related to SARB security transfer instructions.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2020-05-04      FAOPS-746       Cuen Edwards            Kgomotso Gumbo          Initial implementation.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import os
import tempfile
import xml.dom.minidom as minidom
import xml.etree.ElementTree as ElementTree

import acm

from at_logging import getLogger
import DocumentBusinessProcessGeneral
import DocumentGeneral
import EnvironmentFunctions


LOGGER = getLogger(__name__)

REFERENCE_PREFIX = 'SSTI-'


class StateNames(object):
    """
    A class representing the state names for a document business
    process using the 'SARB Sec Transfer Instruction' state chart.

    This should be replaced with a proper enum when we eventually
    move to Python 3.
    """
    READY = 'Ready'
    PENDING_GENERATION = 'Pending Generation'
    GENERATED = 'Generated'
    GENERATION_FAILED = 'Generation Failed'
    CANCELLED = 'Cancelled'
    HOLD = 'Hold'
    PENDING_SENDING = 'Pending Sending'
    SENT = 'Sent'
    SENDING_FAILED = 'Sending Failed'
    ACKNOWLEDGED = 'Acknowledged'
    NOT_ACKNOWLEDGED = 'Not Acknowledged'


class EventNames(object):
    """
    A class representing the event names for a document business
    process using the 'SARB Sec Transfer Instruction' state chart.

    This should be replaced with a proper enum when we eventually
    move to Python 3.
    """
    GENERATE = 'Generate'
    GENERATED = 'Generated'
    GENERATION_FAILED = 'Generation Failed'
    CANCEL = 'Cancel'
    HOLD = 'Hold'
    SEND = 'Send'
    SENT = 'Sent'
    SENDING_FAILED = 'Sending Failed'
    ACKNOWLEDGED = 'Acknowledged'
    NOT_ACKNOWLEDGED = 'Not Acknowledged'
    REGENERATE = 'Regenerate'
    RESEND = 'Resend'


class ParameterNames(object):
    """
    A class representing the parameters for a SARB security transfer
    instruction business process.

    This should be replaced with a proper enum when we eventually
    move to Python 3.
    """
    XML_URL = 'xml_url'
    MQ_QUEUE_MANAGER = 'mq_queue_manager'
    MQ_CONNECTION_NAME = 'mq_connection_name'
    MQ_CHANNEL_NAME = 'mq_channel_name'
    MQ_QUEUE_NAME = 'mq_queue_name'
    MT_URL = 'mt_url'
    SWIFT_ERROR_CODE = 'swift_error_code'


class SecurityTransfer(object):
    """
    A class representing the details of a security transfer.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.security_name = None
        self.amount = None

    def to_xml_element(self):
        """
        Convert this SecurityTransfer instance to its representation
        as an XML Element.
        """
        element = _generate_xml_element('SECURITY_TRANSFER')
        element.append(_generate_xml_element('SECURITY_NAME', self.security_name))
        element.append(_generate_xml_element('AMOUNT', str(self.amount)))
        return element

    @classmethod
    def from_xml_element(cls, settlement_element):
        """
        Convert the XML Element representation of a security transfer
        to an instance of SecurityTransfer.
        """
        security_transfer = SecurityTransfer()
        security_transfer.security_name = settlement_element.find('SECURITY_NAME').text
        security_transfer.amount = float(settlement_element.find('AMOUNT').text)
        return security_transfer


def get_sarb_party():
    """
    Get the party whose details should be used to represent the SARB.
    """
    sarb_party_name = str(_get_instruction_parameter('SARBPartyName'))
    sarb_party = acm.FParty[sarb_party_name]
    if sarb_party is None:
        raise ValueError("Unable to find SARB party '{sarb_party_name}'.".format(
            sarb_party_name=sarb_party_name
        ))
    return sarb_party


def get_instruction_state_chart_name():
    """
    Get the name of the state chart used for SARB security transfer
    instructions.
    """
    return 'SARB Sec Transfer Instruction'


def get_transfer_from_custodian_event_name():
    """
    Get the name of the event to associate with SARB security
    transfer instructions for transfers from the custodian to the
    SARB.
    """
    return 'SARB Security Transfer From CD'


def get_transfer_to_custodian_event_name():
    """
    Get the name of the event to associate with SARB security
    transfer instructions for transfers from the SARB to the
    custodian.
    """
    return 'SARB Security Transfer To CD'


def get_transfer_event_names():
    """
    Get the event names supported by SARB security transfer
    instructions.
    """
    return [
        get_transfer_from_custodian_event_name(),
        get_transfer_to_custodian_event_name()
    ]


def security_transfers_exist(event_name, transfer_date):
    """
    Determine whether or not security transfers exist for the
    specified event name and transfer date.
    """
    for security_transfers in get_security_transfers(event_name, transfer_date):
        return True
    return False


def get_security_transfers(event_name, transfer_date):
    """
    Create SecurityTransfer objects for the specified event name
    and transfer date.
    """
    # Get security transfers based on current settlements.
    settlement_security_transfers_by_security_name = _get_settlement_security_transfers_by_security_name(transfer_date)
    # Get security transfers based on previous sent instructions.
    sent_security_transfers_by_security_name = _get_sent_security_transfers_by_security_name(transfer_date)
    # Get set of all security names.
    security_names = set()
    security_names.update(list(settlement_security_transfers_by_security_name.keys()))
    security_names.update(list(sent_security_transfers_by_security_name.keys()))
    # Calculate new security transfers to send.
    event_security_transfers = list()
    for security_name in security_names:
        amount = 0.0
        # Add any current amount.
        if security_name in list(settlement_security_transfers_by_security_name.keys()):
            settlement_security_transfers = settlement_security_transfers_by_security_name[security_name]
            for settlement_security_transfer in settlement_security_transfers:
                amount += settlement_security_transfer.amount
        # Remove any previous sent amount.
        if security_name in list(sent_security_transfers_by_security_name.keys()):
            sent_security_transfers = sent_security_transfers_by_security_name[security_name]
            for sent_security_transfer in sent_security_transfers:
                amount -= sent_security_transfer.amount
        # Omit zero amount transfers.
        if DocumentGeneral.is_almost_zero(amount):
            continue
        # Only add transfers for the correct event.
        security_transfer = SecurityTransfer()
        security_transfer.security_name = security_name
        security_transfer.amount = round(amount, 2)
        if event_name == get_transfer_from_custodian_event_name():
            if amount < 0.0:
                event_security_transfers.append(security_transfer)
        elif event_name == get_transfer_to_custodian_event_name():
            if amount > 0.0:
                event_security_transfers.append(security_transfer)
        else:
            raise ValueError("Unsupported event '{event_name}' specified.".format(
                event_name=event_name
            ))
    return event_security_transfers


def get_bank_contact(event_name):
    """
    Get the bank contact to use for SARB security transfer
    instructions for the specified event name.
    """
    return _get_party_contact(DocumentGeneral.get_bank_party(), 'bank', event_name)


def get_sarb_contact(event_name):
    """
    Get the SARB contact to use for SARB security transfer
    instructions for the specified event name.
    """
    return _get_party_contact(get_sarb_party(), 'SARB', event_name)


def get_bank_from_name(bank_contact):
    """
    Get the bank from name to use for SARB security transfer
    instructions.
    """
    from_name = bank_contact.Attention()
    if DocumentGeneral.is_string_value_present(from_name):
        return from_name.strip()
    exception_message = "No attention specified for '{party_name}' contact '{contact_name}'."
    raise ValueError(exception_message.format(
        party_name=bank_contact.Party().Name(),
        contact_name=bank_contact.Fullname()
    ))


def get_bank_from_telephone(bank_contact):
    """
    Get the bank from telephone number for SARB security transfer
    instructions.
    """
    telephone_number = bank_contact.Telephone()
    if DocumentGeneral.is_string_value_present(telephone_number):
        return telephone_number.strip()
    exception_message = "No telephone number specified for '{party_name}' contact '{contact_name}'."
    raise ValueError(exception_message.format(
        party_name=bank_contact.Party().Name(),
        contact_name=bank_contact.Fullname()
    ))


def get_bank_bic(bank_contact):
    """
    Get the bank BIC code to use for SARB security transfer
    instructions.
    """
    production_bic = _get_party_bic(bank_contact, 'bank')
    if EnvironmentFunctions.is_production_environment():
        return production_bic
    non_production_bic = str(_get_instruction_parameter('NonProductionBankBIC'))
    message = "Non-production environment detected - overriding bank BIC with "
    message += "'{non_production_bic}' (would have been '{production_bic}')."
    LOGGER.info(message.format(
        non_production_bic=non_production_bic,
        production_bic=production_bic
    ))
    return non_production_bic


def get_sarb_bic(sarb_contact):
    """
    Get the bank BIC code to use for SARB security transfer
    instructions.
    """
    production_bic = _get_party_bic(sarb_contact, 'SARB')
    if EnvironmentFunctions.is_production_environment():
        return production_bic
    non_production_bic = str(_get_instruction_parameter('NonProductionSARBBIC'))
    message = "Non-production environment detected - overriding SARB BIC with "
    message += "'{non_production_bic}' (would have been '{production_bic}')."
    LOGGER.info(message.format(
        non_production_bic=non_production_bic,
        production_bic=production_bic
    ))
    return non_production_bic


def should_automatically_send():
    """
    Determine whether or not a SARB security transfer instruction
    should be automatically sent.
    """
    return DocumentGeneral.boolean_from_string(str(_get_instruction_parameter('AutomaticallySend')))


def create_instruction_business_process(event_name, transfer_date):
    """
    Create a SARB security transfer instruction business process for
    the specified event name and transfer date.
    """
    acm.BeginTransaction()
    try:
        state_chart = acm.FStateChart[get_instruction_state_chart_name()]
        business_process = acm.BusinessProcess.InitializeProcess(DocumentGeneral.get_bank_party(), state_chart)
        business_process.AddInfoValue(DocumentBusinessProcessGeneral.get_business_process_event_add_info_name(),
            event_name)
        business_process.AddInfoValue(DocumentBusinessProcessGeneral.get_business_process_date_add_info_name(),
            transfer_date)
        business_process.HandleEvent(EventNames.GENERATE)
        business_process.Commit()
        acm.CommitTransaction()
    except:
        acm.AbortTransaction()
        raise


def has_been_generated(business_process):
    """
    Determine whether or not a document business process has been
    generated.
    """
    last_generated_step = _get_generated_step_after_last_pending_generation_step(business_process)
    return last_generated_step is not None


def generate_instruction_xml_content(business_process):
    """
    Generate the XML content of a SARB security transfer instruction.
    """
    # Importing inside function to avoid creating cyclic import
    # dependencies.
    from SARBSecurityTransferInstructionXMLGenerator import (
        GenerateSARBSecurityTransferInstructionXMLRequest,
        SARBSecurityTransferInstructionXMLGenerator
    )
    reference = '{reference_prefix}{business_process_oid}'.format(
        reference_prefix=REFERENCE_PREFIX,
        business_process_oid=business_process.Oid()
    )
    event_name = DocumentBusinessProcessGeneral.get_business_process_event(business_process)
    transfer_date = DocumentBusinessProcessGeneral.get_business_process_date(business_process)
    request = GenerateSARBSecurityTransferInstructionXMLRequest(reference, event_name, transfer_date)
    return SARBSecurityTransferInstructionXMLGenerator().generate_xml(request)


def generate_instruction_mt_content(xml_content):
    """
    Generate the SWIFT MT message rendering of a SARB security
    transfer instruction.
    """
    # Importing inside function to avoid creating cyclic import
    # dependencies.
    from SARBSecurityTransferInstructionMTGenerator import (
        GenerateSARBSecurityTransferInstructionMTRequest,
        SARBSecurityTransferInstructionMTGenerator
    )
    request = GenerateSARBSecurityTransferInstructionMTRequest(xml_content)
    return SARBSecurityTransferInstructionMTGenerator().generate_mt_message(request)


def store_instruction_content(event_name, content, document_format):
    """
    Store the content for a generated format of a SARB security
    transfer instruction in persistent storage and return the URL of
    the storage location.
    """
    return DocumentGeneral.store_document_content(event_name, document_format, content)


def retrieve_last_generated_instruction_xml_content(business_process):
    """
    Retrieve the XML content for the latest version of a SARB
    security transfer instruction business process that has been
    generated.
    """
    last_generated_step = _get_generated_step_after_last_pending_generation_step(business_process)
    if last_generated_step is None:
        return None
    generated_parameters = last_generated_step.DiaryEntry().Parameters()
    xml_content_url = generated_parameters[ParameterNames.XML_URL]
    return DocumentGeneral.retrieve_document_content(xml_content_url)


def retrieve_last_sent_instruction_xml_content(business_process):
    """
    Retrieve the XML content for the latest version of a SARB
    security transfer instruction business process that has been
    sent to the SARB.
    """
    last_sent_generated_step = _get_generated_step_before_last_sent_step(business_process)
    if last_sent_generated_step is None:
        return None
    generated_parameters = last_sent_generated_step.DiaryEntry().Parameters()
    xml_content_url = generated_parameters[ParameterNames.XML_URL]
    return DocumentGeneral.retrieve_document_content(xml_content_url)


def retrieve_last_generated_instruction_mt_content(business_process):
    """
    Retrieve the SWIFT MT message content for the latest version of a
    SARB security transfer instruction business process that has been
    generated.
    """
    last_generated_step = _get_generated_step_after_last_pending_generation_step(business_process)
    if last_generated_step is None:
        return None
    generated_parameters = last_generated_step.DiaryEntry().Parameters()
    mt_content_url = generated_parameters[ParameterNames.MT_URL]
    return DocumentGeneral.retrieve_document_content(mt_content_url)


def generate_instruction_xml_file(business_process):
    """
    Generate a SARB security transfer instructione XML file and
    return the file path.
    """
    xml_content = retrieve_last_generated_instruction_xml_content(business_process)
    xml_content = minidom.parseString(xml_content).toprettyxml(indent='  ')
    xml_file_name = get_instruction_file_name(business_process) + '.xml'
    xml_file_path = os.path.join(tempfile.mkdtemp(), xml_file_name)
    with open(xml_file_path, 'wb') as xml_file:
        xml_file.write(xml_content)
    return xml_file_path


def generate_instruction_mt_file(business_process):
    """
    Generate a SARB security transfer instruction SWIFT MT message
    file and return the file path.
    """
    mt_content = retrieve_last_generated_instruction_mt_content(business_process)
    mt_file_name = get_instruction_file_name(business_process) + '.mt'
    mt_file_path = os.path.join(tempfile.mkdtemp(), mt_file_name)
    with open(mt_file_path, 'wb') as mt_file:
        mt_file.write(mt_content)
    return mt_file_path


def get_instruction_file_name(business_process):
    """
    Get the file name to be given to a SARB security transfer
    instruction.
    """
    event_name = DocumentBusinessProcessGeneral.get_business_process_event(business_process)
    transfer_date = DocumentBusinessProcessGeneral.get_business_process_date(business_process)
    # Create file name.
    file_name_template = "{event_name} {transfer_date} {reference}"
    file_name = file_name_template.format(
        event_name=event_name,
        transfer_date=transfer_date,
        reference=business_process.Oid()
    )
    return DocumentGeneral.format_file_name(file_name)


def content_is_empty(xml_content):
    """
    Determine whether or not specified xml content constitutes an
    empty SARB security transfer instruction.
    """
    root_element = ElementTree.fromstring(xml_content)
    return root_element.find('SECURITY_TRANSFERS/SECURITY_TRANSFER') is None


def _get_instruction_parameter(parameter_name):
    """
    Get a SARB security transfer instruction FParameter value.
    """
    return DocumentGeneral.get_fparameter('ABSASARBSecurityTransferInstructionParameters', parameter_name)


def _get_settlement_security_transfers_by_security_name(transfer_date):
    """
    Get security transfers for any settlements for the specified
    transfer date by security name.
    """
    security_transfers = _get_security_transfers_from_settlements(transfer_date)
    return _get_security_transfers_by_security_name(security_transfers)


def _get_sent_security_transfers_by_security_name(transfer_date):
    """
    Get security transfers for any sent instructions for the
    specified transfer date by security name.
    """
    security_transfers = _get_security_transfers_from_sent_instructions(transfer_date)
    return _get_security_transfers_by_security_name(security_transfers)


def _get_security_transfers_by_security_name(security_transfers):
    """
    Group the specified security transfers by security name and
    return as a dictionary with security name as dictionary key
    and security transfer for the security as dictionary value.
    """
    security_transfers_by_security_name = dict()
    for security_transfer in security_transfers:
        security_name = security_transfer.security_name
        if security_name not in list(security_transfers_by_security_name.keys()):
            security_transfers_by_security_name[security_name] = list()
        security_transfers_by_security_name[security_name].append(security_transfer)
    return security_transfers_by_security_name


def _get_security_transfers_from_settlements(transfer_date):
    """
    Get security transfers for any settlements for the specified
    transfer date.
    """
    security_transfers = list()
    transfer_settlements = _get_transfer_settlements(transfer_date)
    for transfer_settlement in transfer_settlements:
        security_transfer = _get_security_transfer_from_settlement(transfer_settlement)
        security_transfers.append(security_transfer)
    return security_transfers


def _get_transfer_settlements(transfer_date):
    """
    Get the transfer settlements for the specified transfer date.
    """
    asql_query = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
    asql_query.AddAttrNode('ValueDay', 'EQUAL', transfer_date)
    asql_query.AddAttrNode('Currency.Name', 'EQUAL', 'ZAR')
    asql_query.AddAttrNode('Counterparty.Name', 'EQUAL', 'ALCO DESK ISSUER')
    asql_query.AddAttrNode('Acquirer.Type', 'EQUAL', 'Intern Dept')
    asql_query.AddAttrNode('SecurityInstrument.Issuer.Name', 'EQUAL', 'S A GOVERNMENT DOMESTIC')
    status_node = asql_query.AddOpNode('OR')
    # Only look at active post-release settlements.
    for status in ['Acknowledged', 'Released', 'Settled']:
        status_node.AddAttrNode('Status', 'EQUAL', status)
    message_type_node = asql_query.AddOpNode('OR')
    for message_type in [540, 542]:
        message_type_node.AddAttrNode('Documents.SwiftMessageType', 'EQUAL', message_type)
    return asql_query.Select()


def _get_settlements_by_security(settlements):
    """
    Group the specified settlements by security and return as
    a dictionary with security as dictionary key and settlements
    for the security as dictionary value.
    """
    settlements_by_security = dict()
    for settlement in settlements:
        security = settlement.SecurityInstrument()
        if security not in list(settlements_by_security.keys()):
            settlements_by_security[security] = list()
        settlements_by_security[security].append(settlement)
    return settlements_by_security


def _get_security_transfer_from_settlement(settlement):
    """
    Create a SecurityTransfer object from the specified
    transfer settlement.
    """
    security_transfer = SecurityTransfer()
    security = settlement.SecurityInstrument()
    external_id = security.ExternalId1()
    if not DocumentGeneral.is_string_value_present(external_id):
        error_message = "External ID 1 not specified for security '{security_name}'."
        raise ValueError(error_message.format(
            security_name=security.Name()
        ))
    security_transfer.security_name = external_id
    security_transfer.amount = round(settlement.Amount(), 2)
    return security_transfer


def _get_security_transfers_from_sent_instructions(transfer_date):
    """
    Get security transfers for any sent SARB security transfer
    instructions for the specified transfer date.
    """
    security_transfers = list()
    business_processes = _get_existing_instruction_business_processes(transfer_date)
    for business_process in business_processes:
        current_state_name = business_process.CurrentStateName()
        if current_state_name not in [StateNames.SENT, StateNames.ACKNOWLEDGED]:
            continue
        xml_content = retrieve_last_sent_instruction_xml_content(business_process)
        instruction_security_transfers = _get_security_transfers_from_xml_content(xml_content)
        security_transfers.extend(instruction_security_transfers)
    return security_transfers


def _get_security_transfers_from_xml_content(xml_content):
    """
    Create SecurityTransfer objects from the specified xml content.
    """
    security_transfers = list()
    root_element = ElementTree.fromstring(xml_content)
    for security_transfer_element in root_element.iterfind('SECURITY_TRANSFERS/SECURITY_TRANSFER'):
        security_transfer = SecurityTransfer.from_xml_element(security_transfer_element)
        security_transfers.append(security_transfer)
    return security_transfers


def _get_existing_instruction_business_processes(transfer_date):
    """
    Get any existing SARB security transfer instruction business
    processes for the specified transfer date.
    """
    asql_query = acm.CreateFASQLQuery(acm.FBusinessProcess, 'AND')
    asql_query.AddAttrNode('StateChart.Name', 'EQUAL', get_instruction_state_chart_name())
    asql_query.AddAttrNode('Subject_type', 'EQUAL', 'Party')
    asql_query.AddAttrNode('Subject_seqnbr', 'EQUAL', DocumentGeneral.get_bank_party().Oid())
    date_method_name = DocumentGeneral.get_additional_info_method_name(
        DocumentBusinessProcessGeneral.get_business_process_date_add_info_name())
    to_date_attribute_name = 'AdditionalInfo.{date_method_name}'.format(
        date_method_name=date_method_name
    )
    asql_query.AddAttrNode(to_date_attribute_name, 'EQUAL', transfer_date)
    return asql_query.Select()


def _get_generated_step_after_last_pending_generation_step(business_process):
    """
    Get the generated step from the last generation cycle, if such a
    generated step exists.

    This is useful for obtaining the latest version of a SARB
    security transfer instruction.  If a new generation cycle has
    been triggered but the SARB security transfer instruction has
    not yet been generated yet then None will be returned.
    """
    ordered_steps = _get_ordered_steps(business_process)
    last_index_of_pending_generation = _get_last_index_of_state(ordered_steps, StateNames.PENDING_GENERATION)
    if last_index_of_pending_generation == -1:
        return None
    index = last_index_of_pending_generation + 1
    number_of_steps = len(ordered_steps)
    while index < number_of_steps:
        step = ordered_steps[index]
        if step.State().Name() == StateNames.GENERATED:
            return step
        index += 1
    return None


def _get_generated_step_before_last_sent_step(business_process):
    """
    Get the generated step preceding the last send step, if a send
    step exists.

    This is useful for obtaining the last version of a SARB security
    transfer instruction that has been sent to the SARB.  If the
    instruction has not been sent then None will be returned.
    """
    ordered_steps = _get_ordered_steps(business_process)
    last_index_of_sent = _get_last_index_of_state(ordered_steps, StateNames.SENT)
    if last_index_of_sent == -1:
        return None
    index = last_index_of_sent - 1
    while index > -1:
        step = ordered_steps[index]
        if step.State().Name() == StateNames.GENERATED:
            return step
        index -= 1
    raise RuntimeError("Unable to find '{generated_state}' step preceding '{sent_state}' step.".format(
        generated_state=StateNames.GENERATED,
        sent_state=StateNames.SENT
    ))


def _get_ordered_steps(business_process):
    """
    Get the steps of a business process ordered by create time.
    """
    return sorted(business_process.Steps().AsArray(), key=lambda step: step.CreateTime())


def _get_last_index_of_state(ordered_steps, state_name):
    """
    Get the index of the last step for a specified state from a list
    of ordered steps.
    """
    index = len(ordered_steps) - 1
    while index > -1:
        step = ordered_steps[index]
        if step.State().Name() == state_name:
            return index
        index -= 1
    return -1


def _generate_xml_element(element_name, element_text=''):
    """
    Generate an XML element with the specified name and text.
    """
    element = ElementTree.Element(element_name)
    element.text = element_text
    return element


def _get_party_contact(party, party_description, event_name):
    """
    Get the party contact to use for the specified event name.
    """
    contact = DocumentGeneral.find_contact_by_contact_rules(party, event_name=event_name)
    if contact is not None:
        return contact
    exception_message = "Unable to matching find {party_description} contact."
    raise ValueError(exception_message.format(
        party_description=party_description
    ))


def _get_party_bic(contact, party_description):
    """
    Get the party BIC to use for SARB security transfer instructions.
    """
    # Allow override of BIC contact.
    party_bic = contact.NetworkAlias()
    if party_bic is None:
        # Fallback on party BIC.
        party_bic = contact.Party().Swift()
    if party_bic is not None:
        return party_bic
    exception_message = "Unable to matching find {party_description} BIC."
    raise ValueError(exception_message.format(
        party_description=party_description
    ))
