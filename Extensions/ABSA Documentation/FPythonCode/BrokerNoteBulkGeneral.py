"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    BrokerNoteBulkGeneral

DESCRIPTION
    This module contains general functionality related to bulk broker notes generation
.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2020-04-20      FAOPS-702       Joash Moodley                                   Initial Implementation.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import io
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


class StateNames(object):
    """
    A class representing the state names for a document business
    process using the 'Broker Note Bulk' state chart.

    This should be replaced with a proper enum when we eventually
    move to Python 3.
    """
    READY = 'Ready'
    PENDING_GENERATION = 'Pending Generation'
    GENERATED = 'Generated'
    GENERATION_FAILED = 'Generation Failed'
    HOLD = 'Hold'
    PENDING_SENDING = 'Pending Sending'
    SENT = 'Sent'
    SENDING_FAILED = 'Sending Failed'
    CANCELLED = 'Cancelled'


class EventNames(object):
    """
    A class representing the event names for a document business
    process using the 'Broker Note Bulk' state chart.

    This should be replaced with a proper enum when we eventually
    move to Python 3.
    """
    GENERATE = 'Generate'
    GENERATED = 'Generated'
    GENERATION_FAILED = 'Generation Failed'
    HOLD = 'Hold'
    SEND = 'Send'
    SENT = 'Sent'
    SENDING_FAILED = 'Sending Failed'
    CANCEL = 'Cancel'
    REGENERATE = 'Regenerate'
    RESEND = 'Resend'


class ParameterNames(object):
    """
    A class representing the parameters for a broker note bulk
    business process.

    This should be replaced with a proper enum when we eventually
    move to Python 3.
    """
    XML_URL = 'xml_url'
    XLSX_URL = 'xlsx_url'
    BANK_CONTACT = 'bank_contact'
    COUNTERPARTY_CONTACT = 'counterparty_contact'
    FROM_EMAIL_ADDRESS = 'from_email_address'
    TO_EMAIL_ADDRESSES = 'to_email_addresses'
    BCC_EMAIL_ADDRESSES = 'bcc_email_addresses'
    EMAIL_SUBJECT = 'email_subject'
    EMAIL_FAILURES = 'email_failures'


class Trade(object):
    """
    A class representing the details of a trade for display on
    a  broker note bulk.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.trade_date = None
        self.trade_no = None
        self.settlement_date = None
        self.security_descr = None
        self.buyer = None
        self.seller = None
        self.isin = None
        self.issuer = None
        self.maturity_date = None
        self.currency = None
        self.nominal = None
        self.yield_to_maturity = None
        self.clean_price = None
        self.clean_consideration = None
        self.consideration_interest = None
        self.all_in_consideration = None
        self.all_in_price = None
        self.companion = None
        self.companion_spread = None
        self.nutron_code = None
        self.unexcor_code = None

    def to_xml_element(self):
        """
        Convert this Trade instance to its representation as
        an XML Element.
        """
        element = _generate_xml_element('TRADE')
        element.append(_generate_xml_element('TRADE_DATE', str(self.trade_date)))
        element.append(_generate_xml_element('TRADE_NO', str(self.trade_no)))
        element.append(_generate_xml_element('SETTLEMENT_DATE', str(self.settlement_date)))
        element.append(_generate_xml_element('SECURITY_DESCR', str(self.security_descr)))
        element.append(_generate_xml_element('BUYER', str(self.buyer)))
        element.append(_generate_xml_element('SELLER', str(self.seller)))
        element.append(_generate_xml_element('ISIN', str(self.isin)))
        element.append(_generate_xml_element('ISSUER', str(self.issuer)))
        element.append(_generate_xml_element('MATURITY_DATE', str(self.maturity_date)))
        element.append(_generate_xml_element('CURRENCY', str(self.currency)))
        element.append(_generate_xml_element('NOMINAL', str(self.nominal)))
        element.append(_generate_xml_element('ALL_IN_PRICE', str(self.all_in_price)))
        element.append(_generate_xml_element('YIELD_TO_MATURITY', str(self.yield_to_maturity)))
        element.append(_generate_xml_element('CLEAN_PRICE', str(self.clean_price)))
        element.append(_generate_xml_element('CLEAN_CONSIDERATION', str(self.clean_consideration)))
        element.append(_generate_xml_element('CONSIDERATION_INTEREST', str(self.consideration_interest)))
        element.append(_generate_xml_element('ALL_IN_CONSIDERATION', str(self.all_in_consideration)))
        element.append(_generate_xml_element('COMPANION', str(self.companion)))
        element.append(_generate_xml_element('COMPANION_SPREAD', str(self.companion_spread)))
        element.append(_generate_xml_element('NUTRON_CODE', str(self.nutron_code)))
        element.append(_generate_xml_element('UNEXCOR_CODE', str(self.unexcor_code)))
        return element

    @classmethod
    def from_xml_element(cls, trade_element):
        """
        Convert the XML Element representation of a Trade
        to an instance of Trade.
        """
        trade = Trade()
        trade.trade_date = trade_element.find('TRADE_DATE').text
        trade.trade_no = trade_element.find('TRADE_NO').text
        trade.settlement_date = trade_element.find('SETTLEMENT_DATE').text
        trade.security_descr = trade_element.find('SECURITY_DESCR').text
        trade.buyer = trade_element.find('BUYER').text
        trade.seller = trade_element.find('SELLER').text
        trade.isin = trade_element.find('ISIN').text
        trade.issuer = trade_element.find('ISSUER').text
        trade.maturity_date = trade_element.find('MATURITY_DATE').text
        trade.currency = trade_element.find('CURRENCY').text
        trade.nominal = trade_element.find('NOMINAL').text
        trade.all_in_price = trade_element.find('ALL_IN_PRICE').text
        trade.yield_to_maturity = trade_element.find('YIELD_TO_MATURITY').text
        trade.clean_price = trade_element.find('CLEAN_PRICE').text
        trade.clean_consideration = trade_element.find('CLEAN_CONSIDERATION').text
        trade.consideration_interest = trade_element.find('CONSIDERATION_INTEREST').text
        trade.all_in_consideration = trade_element.find('ALL_IN_CONSIDERATION').text
        trade.companion = trade_element.find('COMPANION').text
        trade.companion_spread = trade_element.find('COMPANION_SPREAD').text
        trade.nutron_code = trade_element.find('NUTRON_CODE').text
        trade.unexcor_code = trade_element.find('UNEXCOR_CODE').text
        return trade


def get_managing_party_name(business_process):
    party = get_broker_note_managing_party(business_process)
    return party.Name()


def broker_note_xml_differs(previous_root_element, current_root_element):
    """
    Determine whether the xml is different between previous and current xml.
    """
    previous_root_element = ElementTree.fromstring(previous_root_element)
    current_root_element = ElementTree.fromstring(current_root_element)
    return _xml_differs(previous_root_element, current_root_element)


def get_broker_note_trades(trade, managing_party):
    """
    Gets all trades assigned to the counter party for grouping.
    """
    trades = []
    for connected_trade in trade.TrxTrades():

        connected_trade_managing_party = connected_trade.Counterparty().AddInfoValue('BrokerNoteParty').Oid()

        if str(connected_trade_managing_party) == str(managing_party.Oid()):
            trades.append(connected_trade)
    return trades


def _get_bulk_broker_note_event_name():
    """
    returns the name of the bulk broker note
    business process event
    """
    return 'Broker Note Bulk'


def _get_block_trade_id():
    """
    Return Add Info Field Name where block trade id
    is stored
    """
    return 'BP_ExternalId'


def get_broker_note_state_chart_name():
    """
    Get the name of the state chart used for bulk broker notes
    """
    return 'Broker Note Bulk'


def get_broker_note_event_name():
    """
    Get the name of the event to associate with
    bulk broker notes.
    """
    return 'Broker Note Bulk'


def get_supported_broker_note_instrument_types():
    """
    Get the instrument types supported by bulk broker notes.
    """
    return ['Bond', 'FRN', 'IndexLinkedBond']


def get_broker_note_managing_party(business_process):
    """
    returns the party which the xls file will be generated for.
    """
    return business_process.Subject()


def get_instrument_type_description(instrument_type):
    """
    Get a description of the bulk broker note instrument type.
    """
    if instrument_type == 'IndexLinkedBond':
        return 'Index Linked Bond'
    return instrument_type


def has_been_generated(business_process):
    """
    Determine whether or not a bulk broker note business process has been
    generated.
    """
    last_generated_step = _get_generated_step_after_last_pending_generation_step(business_process)
    return last_generated_step is not None


def generate_broker_note_xml_content(business_process):
    """
    Generate the XML content of a bulk broker note.
    """
    # Importing inside function to avoid creating cyclic import
    # dependencies.
    from BrokerNoteBulkXMLGenerator import GenerateBrokerNoteBulkXMLXRequest, BrokerNoteBulkXMLGenerator

    instrument_type = business_process.AddInfoValue(DocumentBusinessProcessGeneral
        .get_business_process_instype_add_info_name())
    from_date = business_process.AddInfoValue(DocumentBusinessProcessGeneral
        .get_business_process_from_date_add_info_name())
    to_date = business_process.AddInfoValue(DocumentBusinessProcessGeneral
        .get_business_process_to_date_add_info_name())
    block_trade_id = business_process.AddInfoValue(_get_block_trade_id())
    managing_party = get_broker_note_managing_party(business_process)
    request = GenerateBrokerNoteBulkXMLXRequest(managing_party, instrument_type,
        from_date, to_date, block_trade_id)
    return BrokerNoteBulkXMLGenerator().generate_xml(request)


def generate_broker_note_xlsx_content(xml_content):
    """
    Generate the Excel XLSX rendering of a bulk broker note.
    """
    # Importing inside function to avoid creating cyclic import
    # dependencies.
    from BrokerNoteBulkXLSXGenerator import (GenerateBrokerNoteBulkXLSXRequest,
        BrokerNoteBulkXLSXGenerator)
    bytes_io = io.BytesIO()
    request = GenerateBrokerNoteBulkXLSXRequest(xml_content, bytes_io)
    BrokerNoteBulkXLSXGenerator().generate_xlsx(request)
    return bytes_io.getvalue()


def store_broker_note_content(content, document_format):
    """
    Store the content for a generated format of a bulk
    broker note in persistent storage and return the URL of the storage
    location.
    """
    return DocumentGeneral.store_document_content(get_broker_note_event_name(), document_format, content)


def retrieve_last_generated_broker_note_xml_content(business_process):
    """
    Retrieve the XML content for the latest version of a
    bulk broker note business process that has been generated.
    """
    last_generated_step = _get_generated_step_after_last_pending_generation_step(business_process)
    if last_generated_step is None:
        return None
    generated_parameters = last_generated_step.DiaryEntry().Parameters()
    xml_content_url = generated_parameters[ParameterNames.XML_URL]
    return DocumentGeneral.retrieve_document_content(xml_content_url)


def retrieve_last_sent_broker_note_xml_content(business_process):
    """
    Retrieve the XML content for the latest version of a bulk broker note
    business process that has been sent to the associated counterparty.
    """
    last_sent_generated_step = _get_generated_step_before_last_sent_step(business_process)
    if last_sent_generated_step is None:
        return None
    generated_parameters = last_sent_generated_step.DiaryEntry().Parameters()
    xml_content_url = generated_parameters[ParameterNames.XML_URL]
    return DocumentGeneral.retrieve_document_content(xml_content_url)


def retrieve_last_generated_broker_note_xlsx_content(business_process):
    """
    Retrieve the XLSX content for the latest version of a bulk
    broker note business process that has been generated.
    """
    last_generated_step = _get_generated_step_after_last_pending_generation_step(business_process)
    if last_generated_step is None:
        return None
    generated_parameters = last_generated_step.DiaryEntry().Parameters()
    xlsx_content_url = generated_parameters[ParameterNames.XLSX_URL]
    return DocumentGeneral.retrieve_document_content(xlsx_content_url)


def generate_broker_note_xml_file(business_process):
    """
    Generate a bulk broker note XML file and return the file
    path.
    """
    xml_content = retrieve_last_generated_broker_note_xml_content(business_process)
    xml_content = minidom.parseString(xml_content).toprettyxml(indent='  ')
    xml_file_name = get_broker_note_file_name(business_process) + '.xml'
    xml_file_path = os.path.join(tempfile.mkdtemp(), xml_file_name)
    with open(xml_file_path, 'wb') as xml_file:
        xml_file.write(xml_content)
    return xml_file_path


def generate_broker_note_xlsx_file(business_process):
    """
    Generate a bulk broker note Excel XSLX file and return the
    file path.
    """
    xlsx_content = retrieve_last_generated_broker_note_xlsx_content(business_process)
    xlsx_file_name = get_broker_note_file_name(business_process) + '.xlsx'
    xlsx_file_path = os.path.join(tempfile.mkdtemp(), xlsx_file_name)
    with open(xlsx_file_path, 'wb') as xlsx_file:
        xlsx_file.write(xlsx_content)
    return xlsx_file_path


def _get_block_trade(business_process):
    """
    returns block trade
    """
    trade_id = business_process.AddInfoValue(_get_block_trade_id())
    trade = acm.FTrade[trade_id]
    return trade


def get_block_ins_type_name(business_process):
    """
    returns instrument name
    """
    trade = _get_block_trade(business_process)
    return trade.Instrument().Name()


def get_block_ins_type(business_process):
    """
    returns Instrument type
    """
    trade = _get_block_trade(business_process)
    return trade.Instrument().InsType()


def get_block_instrument_name(business_process):
    """
    returns block trade instrument name
    """
    trade = _get_block_trade(business_process)
    return trade.Instrument().Name()


def get_block_counter_party_name(business_process):
    """
    returns block trade counter party name
    """
    trade = _get_block_trade(business_process)
    return trade.Counterparty().Name()


def get_broker_note_file_name(business_process):
    """
    Get the file name to be given to a bulk broker note document.
    """
    # Create file name.
    counter_party_name = get_block_counter_party_name(business_process)
    ins_name = get_block_ins_type_name(business_process).replace('/', '-')
    file_name = '{counter_party_name} {ins_name}'.format(
        counter_party_name=counter_party_name,
        ins_name=ins_name
    )
    return DocumentGeneral.format_file_name(file_name)


def get_bank_contact(business_process):
    """
    Get the bank contact to use for the delivery of a
    bulk broker note.
    """
    return DocumentBusinessProcessGeneral.get_default_counterparty_business_process_bank_contact(business_process)


def _get_managing_party_contact(counterparty, business_process):
    """
    Get the default counterparty contact to use for a document
    business process belonging to a counterparty subject
    """
    instrument_type = DocumentBusinessProcessGeneral.get_business_process_instrument_type(business_process)
    event_name = get_broker_note_event_name()
    contact = DocumentGeneral.find_contact_by_contact_rules(
        counterparty, instrument_type=instrument_type, event_name=event_name)
    if contact is not None:
        return contact
    exception_message = "Unable find a matching contact for {event_name} and {ins_type}"
    raise ValueError(exception_message.format(
        event_name=event_name,
        ins_type=instrument_type
    ))


def get_counterparty_contact(business_process):
    """
    Get the counterparty contact to use for the delivery of a bulk broker note.
    """
    party = get_broker_note_managing_party(business_process)
    return _get_managing_party_contact(party, business_process)


def get_acquirer(business_process):
    """
    Get the acquirer contact to use for the delivery of a bulk broker note.
    """
    trade = _get_block_trade(business_process)
    return get_acquirer_contact(trade.Acquirer())


def get_acquirer_contact(acquirer):
    """
    returns the contact that will be used in the email.
    """
    for party_contact in acquirer.Contacts():
        for contact_rule in party_contact.ContactRules():
            if contact_rule.EventChlItem().Name() == _get_bulk_broker_note_event_name():
                return party_contact
    return None


def get_email_from_name(bank_contact):
    """
    Get the from name to use in the email for delivery of a bulk broker note.
    """
    return bank_contact.Attention()


def get_email_from_telephone(bank_contact):
    """
    Get the from telephone number to use in the email for delivery
    of a bulk broker note.
    """
    return bank_contact.Telephone()


def get_email_from_address(bank_contact):
    """
    Get the from email address to use for delivery of a
    bulk broker note document.
    """
    return bank_contact.Email().split(',')[0]


def get_email_to_addresses(counterparty_contact):
    """
    Get the to email addresses to use for delivery of a
    bulk broker note document.
    """
    return DocumentBusinessProcessGeneral.get_default_counterparty_business_process_email_to(counterparty_contact)


def get_email_bcc_addresses(bank_contact,  non_production_email_addresses=None):
    """
    Get any email addresses to be bcc'ed when delivering a
    bulk broker note document.
    """
    production_email_addresses = bank_contact.Email()
    if EnvironmentFunctions.is_production_environment():
        return production_email_addresses
    if non_production_email_addresses is None:
        non_production_email_addresses = DocumentGeneral.get_default_non_production_email_bcc_addresses()
    message = "Non-production environment detected - overriding 'BCC' email "
    message += "address with '{non_production_email_addresses}' (would have "
    message += "been sent to '{production_email_addresses}')."
    LOGGER.info(message.format(
        non_production_email_addresses=non_production_email_addresses,
        production_email_addresses=production_email_addresses
    ))
    return non_production_email_addresses


def get_email_subject(business_process):
    """
    Get the email subject to be used when delivering a
    bulk broker note document.
    """
    ins_type = get_block_ins_type(business_process)
    ctpy = get_block_counter_party_name(business_process)
    ins_name = get_block_instrument_name(business_process)

    subject = '{ins_type} Broker Note {ctpy} {ins_name}'.format(
        ins_type=ins_type,
        ctpy=ctpy,
        ins_name=ins_name
    )
    return subject


def get_email_body(from_name, from_telephone, from_email_address, business_process):
    """
    Get the email body to be used when delivering a
    bulk broker note document.
    """
    # Importing inside function to avoid creating cyclic import
    # dependencies.
    from EmailBodyHTMLGenerator import EmailBodyHTMLGenerator, GenerateEmailBodyHTMLRequest
    counter_party_name = get_block_counter_party_name(business_process)
    document_description = "Broker Note for {counter_party_name}".format(
        counter_party_name=counter_party_name
    )

    request = GenerateEmailBodyHTMLRequest(
        from_name,
        from_telephone,
        from_email_address,
        document_description
    )
    return EmailBodyHTMLGenerator().generate_html(request)


def should_automatically_send():
    """
    Determine whether or not a bulk broker note should be
    automatically sent.
    """
    return DocumentGeneral.boolean_from_string(str(_get_broker_note_parameter('AutomaticallySend')))


def create_broker_note_business_process(managing_party, instrument_type, trade):
    """
    Create a bulk broker note business process for the specified
    counterparty, instrument type, inclusive from date and inclusive
    to date.
    """
    acm.BeginTransaction()
    try:
        state_chart = acm.FStateChart[get_broker_note_state_chart_name()]
        business_process = acm.BusinessProcess.InitializeProcess(managing_party, state_chart)
        business_process.AddInfoValue(DocumentBusinessProcessGeneral.get_business_process_event_add_info_name(),
            get_broker_note_event_name())
        business_process.AddInfoValue(DocumentBusinessProcessGeneral.get_business_process_instype_add_info_name(),
            instrument_type)
        business_process.AddInfoValue(DocumentBusinessProcessGeneral.get_business_process_from_date_add_info_name(),
            trade.CreateDay())
        business_process.AddInfoValue(DocumentBusinessProcessGeneral.get_business_process_to_date_add_info_name(),
            trade.CreateDay())
        business_process.AddInfoValue(_get_block_trade_id(), trade.Oid())
        business_process.HandleEvent(EventNames.GENERATE)
        business_process.Commit()
        acm.CommitTransaction()
    except:
        acm.AbortTransaction()
        raise


def _get_broker_note_parameter(parameter_name):
    """
    Get bulk broker note FParameter value.
    """
    return DocumentGeneral.get_fparameter('ABSABrokerNoteBulkParameters', parameter_name)


def get_default_document_parameter(parameter_name):
    """
    Get a documentation FParameter value from the default FParameter.
    """
    return DocumentGeneral.get_fparameter('ABSADocumentationParameters', parameter_name)


def _get_generated_step_after_last_pending_generation_step(business_process):
    """
    Get the generated step from the last generation cycle, if such a
    generated step exists.

    This is useful for obtaining the latest version of a bulk
    broker note.  If a new generation cycle has been triggered but the
    bulk broker note has not yet been generated yet then None will be
    returned.
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

    This is useful for obtaining the last version of a bulk
    broker note that has been sent to the counterparty.  If the bulk broker note has
    not been sent then None will be returned.
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


def _xml_differs(element1, element2):
    """
    Determine whether or not two xml elements (identified by the
    specified xpath) differ.

    This implementation currently takes a dumb approach to XML
    comparison.  It simply determines whether or not the two XML
    elements match exactly in terms of text.  This implies that
    order of elements etc. is important to correct functioning.
    """
    compare_string1 = ElementTree.tostring(element1)
    compare_string2 = ElementTree.tostring(element2)
    return compare_string1 != compare_string2
