"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    SecurityLoanGeneral

DESCRIPTION
    This module contains general functionality related to Security Loan functions

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2020-01-31      FAOPS-557       Tawanda Mukhalela       Khaya Mbebe             Initial Implementation.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import io
import os
import tempfile
import traceback
from datetime import date
import xml.dom.minidom as minidom
import xml.etree.ElementTree as ElementTree

import acm
from at_logging import getLogger

import DocumentGeneral
import DocumentBusinessProcessGeneral

LOGGER = getLogger(__name__)
TODAY = date.today()


class StateNames(object):
    """
    A class representing the state names for a document business
    process using the 'Basic Document' state chart.

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
    ERROR = 'Error'


class EventNames(object):
    """
    A class representing the event names for a document business
    process using the 'SecurityLoan Confirmation' state chart.

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
    A class representing the parameters for a SecurityLoan Confirmation advice
    business process.

    This should be replaced with a proper enum when we eventually
    move to Python 3.
    """
    XML_URL = 'xml_url'
    PDF_URL = 'pdf_url'
    BANK_CONTACT = 'bank_contact'
    COUNTERPARTY_CONTACT = 'counterparty_contact'
    FROM_EMAIL_ADDRESS = 'from_email_address'
    TO_EMAIL_ADDRESSES = 'to_email_addresses'
    BCC_EMAIL_ADDRESSES = 'bcc_email_addresses'
    EMAIL_SUBJECT = 'email_subject'
    EMAIL_FAILURES = 'email_failures'


class Trade(object):
    """
    A class representing the details of a Trade for display on
    a SecurityLoan Confirmation.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.amendment_action = None
        self.amendment_reason = None
        self.trade_number = None
        self.isin = None
        self.security_instrument = None
        self.quantity = None
        self.trade_date = None
        self.value_date = None
        self.rate_excluding_vat = None
        self.rate_including_vat = None
        self.original_loan_value = None
        self.vatable = None
        self.recall_period = None
        self.delivery_mode = None
        self.min_fee = None
        self.text1 = None
        self.original_date = None
        self.original_price = None
        self.original_quantity = None
        self.original_rate = None
        self.loan_price = None

    def __eq__(self, other):
        """
        Override of rich comparison method for the Equals operation.

        Determines whether or not this object is considered equal to
        another object.
        """
        if not isinstance(other, type(self)):
            return False
        other_variables = vars(other)
        for variable_name, variable_value in vars(self).items():
            other_variable_value = other_variables[variable_name]
            if str(variable_value) != str(other_variable_value):
                return False
        return True

    def __ne__(self, other):
        """
        Override of rich comparison method for the Not Equals
        operation.

        Determines whether or not this object is considered not
        equal to another object.
        """
        return not self == other

    def to_xml_element(self):
        """
        Convert this Trade instance to its representation as
        an XML Element.
        """
        element = _generate_xml_element('TRADE')
        if self.amendment_action is not None:
            element.set('amendment_action', str(self.amendment_action))
        if self.amendment_reason is not None:
            element.set('amendment_reason', str(self.amendment_reason))
        element.append(_generate_xml_element('TRADE_DNUMBER', str(self.trade_number)))
        element.append(_generate_xml_element('ISIN', str(self.isin)))
        element.append(_generate_xml_element('SECURITY', str(self.security_instrument)))
        element.append(_generate_xml_element('QUANTITY', str(self.quantity)))
        element.append(_generate_xml_element('TRADE_DATE', str(self.trade_date)))
        element.append(_generate_xml_element('SETTLEMENT_DATE', str(self.value_date)))
        element.append(_generate_xml_element('RATE_EXL_VAT', str(self.rate_excluding_vat)))
        element.append(_generate_xml_element('RATE_INC_VAT', str(self.rate_including_vat)))
        element.append(_generate_xml_element('LOAN_PRICE', str(self.loan_price)))
        element.append(_generate_xml_element('LOAN_VALUE', str(self.original_loan_value)))
        element.append(_generate_xml_element('VATABLE', str(self.vatable)))
        element.append(_generate_xml_element('RECALL_PERIOD', str(self.recall_period)))
        element.append(_generate_xml_element('DELIVERY_MODE', str(self.delivery_mode)))
        element.append(_generate_xml_element('MIN_FEE', str(self.min_fee)))
        element.append(_generate_xml_element('TEXT1', str(self.text1)))
        element.append(_generate_xml_element('ORIGINAL_DATE', str(self.original_date)))
        element.append(_generate_xml_element('ORIGINAL_PRICE', str(self.original_price)))
        element.append(_generate_xml_element('ORIGINAL_QUANTITY', str(self.original_quantity)))
        element.append(_generate_xml_element('ORIGINAL_RATE', str(self.original_rate)))

        return element

    @classmethod
    def from_xml_element(cls, trade_element):
        """
        Convert the XML Element representation of a Trade
        to an instance of Trade.
        """
        trade = Trade()
        amendment_action = trade_element.get('amendment_action')
        if amendment_action is not None:
            trade.amendment_action = amendment_action
        amendment_reason = trade_element.get('amendment_reason')
        if amendment_reason is not None:
            trade.amendment_reason = amendment_reason
        trade.trade_number = trade_element.find('TRADE_DNUMBER').text
        trade.isin = trade_element.find('ISIN').text
        trade.security_instrument = trade_element.find('SECURITY').text
        trade.quantity = trade_element.find('QUANTITY').text
        trade.trade_date = trade_element.find('TRADE_DATE').text
        trade.value_date = trade_element.find('SETTLEMENT_DATE').text
        trade.rate_excluding_vat = trade_element.find('RATE_EXL_VAT').text
        trade.rate_including_vat = trade_element.find('RATE_INC_VAT').text
        trade.original_loan_value = trade_element.find('LOAN_VALUE').text
        trade.vatable = trade_element.find('VATABLE').text
        trade.recall_period = trade_element.find('RECALL_PERIOD').text
        trade.delivery_mode = trade_element.find('DELIVERY_MODE').text
        trade.min_fee = trade_element.find('MIN_FEE').text
        trade.text1 = trade_element.find('TEXT1').text
        trade.original_date = trade_element.find('ORIGINAL_DATE').text
        trade.original_price = trade_element.find('ORIGINAL_PRICE').text
        trade.original_quantity = trade_element.find('ORIGINAL_QUANTITY').text
        trade.original_rate = trade_element.find('ORIGINAL_RATE').text
        trade.loan_price = trade_element.find('LOAN_PRICE').text

        return trade


def get_state_chart_name():
    """
    Get the name of the state chart used for SecurityLoan Confirmations.
    """
    return 'SecurityLoan Confirmation'


def get_event_name():
    """
    Get the name of the event to associate with SecurityLoan Confirmations.
    """
    return 'SecurityLoan Confirmation'


def get_supported_instrument_types():
    """
    Get the instrument types supported by SecurityLoan Confirmations.
    """
    return ['SecurityLoan']


def get_description(business_process):
    """
    Get a description for a SecurityLoan Confirmation.
    """
    description = ""
    document_type_add_info_name = DocumentBusinessProcessGeneral\
        .get_business_process_trade_type_add_info_name()
    document_type = business_process.AddInfoValue(document_type_add_info_name)
    if document_type in (None, ''):
        document_type = 'New Loan Confirmation'
    elif document_type in ('PARTIAL_RETURN', 'FULL_RETURN'):
        document_type = 'Return Confirmation'
    if _is_amended(business_process):
        description = "Amendment"
    if _is_cancelled(business_process):
        description = "Cancellation"
    description += " {document_type}".format(
        document_type=document_type
    )
    return description


def has_been_generated(business_process):
    """
    Determine whether or not a document business process has been
    generated.
    """
    last_generated_step = _get_generated_step_after_last_pending_generation_step(business_process)
    return last_generated_step is not None


def generate_confirmation_xml_content(business_process):
    """
    Generate the XML content of a SecurityLoan Confirmation.
    """
    # Importing inside function to avoid creating cyclic import
    # dependencies.
    from SecurityLoanXMLGenerator import GenerateSecurityLoanConfirmationXMLRequest, SecurityLoanXMLGenerator

    previous_xml = retrieve_last_sent_confirmation_xml_content(business_process)
    request = GenerateSecurityLoanConfirmationXMLRequest(business_process, previous_xml)
    return SecurityLoanXMLGenerator().generate_xml(request)


def generate_confirmation_pdf_content(xml_content):
    """
    Generate the Excel XLSX rendering of a SecurityLoan Confirmation.
    """
    # Importing inside function to avoid creating cyclic import
    # dependencies.
    from SecurityLoanPDFGenerator import (GenerateSecurityLoanPDFRequest, SecurityLoanPDFGenerator)
    output_dir = get_temporary_output_dir()
    request = GenerateSecurityLoanPDFRequest(xml_content, output_dir)
    pdf_url = SecurityLoanPDFGenerator().generate_pdf(request)
    try:
        with open(pdf_url, 'rb') as pdf:
            bytes_io = io.BytesIO(pdf.read())
    except Exception as e:
        LOGGER.exception(e)
    finally:
        # Delete the url after getting the PDF File Bytes
        if pdf_url and os.path.exists(pdf_url):
            os.remove(pdf_url)

    return bytes_io.getvalue()


def store_confirmation_content(content, document_format):
    """
    Store the content for a generated format of a SecurityLoan
Confirmation in persistent storage and return the URL of the storage
    location.
    """
    return DocumentGeneral.store_document_content(get_event_name(), document_format, content)


def retrieve_last_generated_confirmation_xml_content(business_process):
    """
    Retrieve the XML content for the latest version of a SecurityLoan
    Confirmation business process that has been generated.
    """
    last_generated_step = _get_generated_step_after_last_pending_generation_step(business_process)
    if last_generated_step is None:
        return None
    generated_parameters = last_generated_step.DiaryEntry().Parameters()
    xml_content_url = generated_parameters[ParameterNames.XML_URL]
    return DocumentGeneral.retrieve_document_content(xml_content_url)


def retrieve_last_sent_confirmation_xml_content(business_process):
    """
    Retrieve the XML content for the latest version of a SecurityLoan
    Confirmation business process that has been sent to the
    associated counterparty.
    """
    last_sent_generated_step = _get_generated_step_before_last_sent_step(business_process)
    if last_sent_generated_step is None:
        return None
    generated_parameters = last_sent_generated_step.DiaryEntry().Parameters()
    xml_content_url = generated_parameters[ParameterNames.XML_URL]
    return DocumentGeneral.retrieve_document_content(xml_content_url)


def retrieve_last_generated_pdf_confirmation_content(business_process):
    """
    Retrieve the PDF content for the latest version of a sec loan
    business process that has been generated.
    """
    last_generated_step = _get_generated_step_after_last_pending_generation_step(business_process)
    if last_generated_step is None:
        return None
    generated_parameters = last_generated_step.DiaryEntry().Parameters()
    pdf_content_url = generated_parameters[ParameterNames.PDF_URL]
    return DocumentGeneral.retrieve_document_content(pdf_content_url)


def generate_sec_loan_xml_file(business_process):
    """
    Generate a SecurityLoan Confirmation XML file and return the file
    path.
    """
    xml_content = retrieve_last_sent_confirmation_xml_content(business_process)
    xml_content = minidom.parseString(xml_content).toprettyxml(indent='  ')
    xml_file_name = get_sec_loan_file_name(business_process) + '.xml'
    xml_file_path = os.path.join(tempfile.mkdtemp(), xml_file_name)
    with open(xml_file_path, 'wb') as xml_file:
        xml_file.write(xml_content)
    return xml_file_path


def generate_sec_loan_pdf_file(business_process):
    """
    Generate a SecurityLoan Confirmation Excel XSLX file and return the
    file path.
    """
    pdf_content = retrieve_last_generated_pdf_confirmation_content(business_process)
    pdf_file_name = get_sec_loan_file_name(business_process) + '.pdf'
    pdf_file_path = os.path.join(tempfile.mkdtemp(), pdf_file_name)
    print(pdf_file_name, pdf_content)
    with open(pdf_file_path, 'wb') as pdf_file:
        pdf_file.write(pdf_content)
    return pdf_file_path


def get_sec_loan_file_name(business_process):
    """
    Get the file name to be given to a SecurityLoan Confirmation.
    """
    counterparty_name = None
    if business_process.Subject().IsKindOf(acm.FParty):
        counterparty_name = DocumentGeneral.get_party_full_name_and_short_code(business_process.Subject())
    elif business_process.Subject().IsKindOf(acm.FTrade):
        counterparty_name = DocumentGeneral.get_party_full_name_and_short_code(
            get_lender_or_borrower_party(business_process.Subject()))
    # Create file name.
    file_name_template = "{description} {counterparty_name}"
    file_name = file_name_template.format(
        description=get_description(business_process),
        counterparty_name=counterparty_name
    )
    return DocumentGeneral.format_file_name(file_name)


def get_bank_contact(business_process):
    """
    Get the bank contact to use for the delivery.
    """
    from_party = acm.FParty['SECURITY LENDINGS DESK']
    instrument_type = DocumentBusinessProcessGeneral.get_business_process_instrument_type(business_process)
    bank_contact = get_party_contacts(from_party, instrument_type)[0]
    if bank_contact:
        return bank_contact
    raise ValueError('No contact Setup on SECURITY LENDINGD DESK')


def get_counterparty_contact(business_process):
    """
    Get the counterparty contact to use for the delivery.
    """
    to_party = business_process.Subject()
    if business_process.Subject().IsKindOf(acm.FTrade):
        to_party = get_lender_or_borrower_party(business_process.Subject())
    instrument_type = DocumentBusinessProcessGeneral.get_business_process_instrument_type(business_process)
    counterparty_contact = get_party_contacts(to_party, instrument_type)[0]

    if counterparty_contact:
        return counterparty_contact
    raise ValueError('No contact Setup on {party}'.format(party=to_party.Name()))


def get_email_from_name(bank_contact):
    """
    Get the from name to use in the email for delivery.
    """
    return DocumentBusinessProcessGeneral.get_default_counterparty_business_process_email_from_name(bank_contact)


def get_email_from_telephone(bank_contact):
    """
    Get the from telephone number to use in the email for delivery.
    """
    return DocumentBusinessProcessGeneral.get_default_counterparty_business_process_email_from_telephone(bank_contact)


def get_email_from_address(bank_contact):
    """
    Get the from email address to use for delivery.
    """
    return DocumentBusinessProcessGeneral.get_default_counterparty_business_process_email_from_address(bank_contact)


def get_email_to_addresses(counterparty_contact):
    """
    Get the to email addresses to use for delivery.
    """
    return DocumentBusinessProcessGeneral.get_default_counterparty_business_process_email_to(counterparty_contact)


def get_email_bcc_addresses(bank_contact):
    """
    Get any email addresses to be bcc'ed when delivering.
    """
    return DocumentBusinessProcessGeneral.get_default_counterparty_business_process_email_bcc(bank_contact)


def get_email_subject(business_process):
    """
    Get the email subject to be used when delivering.
    """
    return get_sec_loan_file_name(business_process) + '.pdf'


def get_email_body(from_name, from_telephone, from_email_address, business_process):
    """
    Get the email body to be used when delivering a SecurityLoan Confirmation.
    """
    # Importing inside function to avoid creating cyclic import
    # dependencies.
    from EmailBodyHTMLGenerator import EmailBodyHTMLGenerator, GenerateEmailBodyHTMLRequest
    document_description = 'your {description} for {period_description}'
    document_description = document_description.format(
        description=get_description(business_process),
        period_description=DocumentBusinessProcessGeneral.get_business_process_date_range_description(business_process)
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
    Determine whether or not a SecurityLoan Confirmation should be
    automatically sent.
    """
    return DocumentGeneral.boolean_from_string(str(_get_security_loan_parameter('AutomaticallySend')))


def confirmation_business_process_exists(counterparty, instrument_type, bp_date, document_type):
    """
    Determine if a SecurityLoan Confirmation business process exists for
    the specified counterparty, instrument type, inclusive from date
    and inclusive to date.
    """
    return len(get_existing_confirmation_business_processes(counterparty, instrument_type, bp_date, document_type)) > 0


def get_existing_confirmation_business_processes(counterparty, instrument_type, bp_date, document_type):
    """
    Get any existing SecurityLoan Confirmation business processes for the
    specified counterparty, instrument type, inclusive from date and
    inclusive to date.
    """
    asql_query = acm.CreateFASQLQuery(acm.FBusinessProcess, 'AND')
    asql_query.AddAttrNode('StateChart.Name', 'EQUAL', get_state_chart_name())
    asql_query.AddAttrNode('Subject_type', 'EQUAL', 'Party')
    asql_query.AddAttrNode('Subject_seqnbr', 'EQUAL', counterparty.Oid())
    event_method_name = DocumentGeneral.get_additional_info_method_name(
        DocumentBusinessProcessGeneral.get_business_process_event_add_info_name())
    event_attribute_name = 'AdditionalInfo.{event_method_name}'.format(
        event_method_name=event_method_name
    )
    asql_query.AddAttrNode(event_attribute_name, 'EQUAL', get_event_name())
    instrument_type_method_name = DocumentGeneral.get_additional_info_method_name(
        DocumentBusinessProcessGeneral.get_business_process_instype_add_info_name())
    instrument_type_attribute_name = 'AdditionalInfo.{instrument_type_method_name}'.format(
        instrument_type_method_name=instrument_type_method_name
    )
    asql_query.AddAttrNode(instrument_type_attribute_name, 'EQUAL', instrument_type)
    asql_query.AddAttrNode('CurrentStateName', 'NOT_EQUAL', StateNames.CANCELLED)
    # Add from date attribute if specified.
    if bp_date is not None:
        from_date_method_name = DocumentGeneral.get_additional_info_method_name(
            DocumentBusinessProcessGeneral.get_business_process_from_date_add_info_name())
        from_date_attribute_name = 'AdditionalInfo.{from_date_method_name}'.format(
            from_date_method_name=from_date_method_name
        )
        asql_query.AddAttrNode(from_date_attribute_name, 'EQUAL', bp_date)
    # Add to date attribute if specified.
    if bp_date is not None:
        to_date_method_name = DocumentGeneral.get_additional_info_method_name(
            DocumentBusinessProcessGeneral.get_business_process_to_date_add_info_name())
        to_date_attribute_name = 'AdditionalInfo.{to_date_method_name}'.format(
            to_date_method_name=to_date_method_name
        )
        asql_query.AddAttrNode(to_date_attribute_name, 'EQUAL', bp_date)
    trade_type = DocumentGeneral.get_additional_info_method_name(
        DocumentBusinessProcessGeneral.get_business_process_trade_type_add_info_name())
    trade_type_attribute_name = 'AdditionalInfo.{trade_type}'.format(
            trade_type=trade_type
        )
    asql_query.AddAttrNode(trade_type_attribute_name, 'EQUAL', document_type)

    return asql_query.Select()


def create_sec_loan_business_process(subject, instrument_type, bp_date, document_type):
    """
    Create a SecurityLoan Confirmation business process for the specified
    counterparty, instrument type, inclusive from date and inclusive
    to date.
    """
    acm.BeginTransaction()
    try:
        state_chart = acm.FStateChart[get_state_chart_name()]
        business_process = acm.BusinessProcess.InitializeProcess(subject, state_chart)
        business_process.AddInfoValue(DocumentBusinessProcessGeneral.get_business_process_event_add_info_name(),
                                      get_event_name())
        business_process.AddInfoValue(DocumentBusinessProcessGeneral.get_business_process_instype_add_info_name(),
                                      instrument_type)
        business_process.AddInfoValue(DocumentBusinessProcessGeneral.get_business_process_from_date_add_info_name(),
                                      bp_date)
        business_process.AddInfoValue(DocumentBusinessProcessGeneral.get_business_process_to_date_add_info_name(),
                                      bp_date)
        business_process.AddInfoValue(DocumentBusinessProcessGeneral.get_business_process_trade_type_add_info_name(),
                                      document_type)
        business_process.HandleEvent(EventNames.GENERATE)
        business_process.Commit()
        acm.CommitTransaction()
    except Exception as e:
        acm.AbortTransaction()
        raise e


def get_active_sec_loan_business_processes(business_process_subject, instrument_type, document_type):
    """
    Get all active SecurityLoan Confirmation business processes for the
    specified counterparty and instrument type.
    """
    asql_query = acm.CreateFASQLQuery(acm.FBusinessProcess, 'AND')
    asql_query.AddAttrNode('StateChart.Name', 'EQUAL', get_state_chart_name())
    if business_process_subject.IsKindOf(acm.FParty):
        asql_query.AddAttrNode('Subject_type', 'EQUAL', 'Party')
    elif business_process_subject.IsKindOf(acm.FTrade):
        asql_query.AddAttrNode('Subject_type', 'EQUAL', 'Trade')
    asql_query.AddAttrNode('Subject_seqnbr', 'EQUAL', business_process_subject.Oid())
    event_method_name = DocumentGeneral.get_additional_info_method_name(
        DocumentBusinessProcessGeneral.get_business_process_event_add_info_name())
    event_attribute_name = 'AdditionalInfo.{event_method_name}'.format(
        event_method_name=event_method_name
    )
    asql_query.AddAttrNode(event_attribute_name, 'EQUAL', get_state_chart_name())
    instrument_type_method_name = DocumentGeneral.get_additional_info_method_name(
        DocumentBusinessProcessGeneral.get_business_process_instype_add_info_name())
    instrument_type_attribute_name = 'AdditionalInfo.{instrument_type_method_name}'.format(
        instrument_type_method_name=instrument_type_method_name
    )
    asql_query.AddAttrNode(instrument_type_attribute_name, 'EQUAL', instrument_type)
    asql_query.AddAttrNode('CurrentStateName', 'NOT_EQUAL', StateNames.CANCELLED)
    to_date_method_name = DocumentGeneral.get_additional_info_method_name(
        DocumentBusinessProcessGeneral.get_business_process_to_date_add_info_name())
    to_date_attribute_name = 'AdditionalInfo.{to_date_method_name}'.format(
        to_date_method_name=to_date_method_name
    )
    asql_query.AddAttrNode(to_date_attribute_name, 'GREATER_EQUAL', acm.Time.DateToday())
    trade_type = DocumentGeneral.get_additional_info_method_name(
        DocumentBusinessProcessGeneral.get_business_process_trade_type_add_info_name())
    trade_type_attribute_name = 'AdditionalInfo.{trade_type}'.format(
        trade_type=trade_type
    )
    asql_query.AddAttrNode(trade_type_attribute_name, 'EQUAL', document_type)
    return asql_query.Select()


def is_instrument_eligible_for_confirmation(instrument):
    """
    Determine whether or not an instrument is a potential candidate
    to appear on a SecurityLoan Confirmation.
    """
    if _is_sec_loan_instrument_eligible_for_confirmation(instrument):
        return True
    return False


def is_trade_eligible_for_confirmation(trade):
    """
    Determine whether or not a trade is a potential candidate to
    appear on a SecurityLoan Confirmation.
    """
    if _is_sec_loan_trade_eligible_for_confirmation(trade):
        return True
    return False


def are_party_trades_eligible_for_confirmation(counterparty, document_type):
    """
    Determine whether or not trades for the specified counterparty are
    potential candidates to appear on a Confirmation.
    """
    trades = _get_active_sec_loan_trades_for_party(counterparty, document_type)
    valid_trades = list()
    for trade in trades:
        if trade.AdditionalInfo().SL_ConfirmationSent() in [False, None]:
            valid_trades.append(trade)

    if len(valid_trades) > 0:
        return True

    return False


def is_in_updateable_state(business_process):
    """
    Determine whether or not a SecurityLoan Confirmation is in an update-
    able state.
    """
    return business_process.CurrentStateName() in [
        StateNames.READY,
        StateNames.GENERATION_FAILED,
        StateNames.HOLD,
        StateNames.SENDING_FAILED,
        StateNames.ERROR,
        StateNames.SENT
        ]


def confirmation_should_be_regenerated(business_process):
    """
    Determine whether or not a SecurityLoan Confirmation should be
    regenerated by determining whether or not the content will change
    if regenerated.`````
    """
    if business_process.CurrentStateName() == StateNames.SENT:
        previous_xml_content = retrieve_last_sent_confirmation_xml_content(business_process)
    else:
        previous_xml_content = retrieve_last_generated_confirmation_xml_content(business_process)
    current_xml_content = generate_confirmation_xml_content(business_process)
    return content_differs(previous_xml_content, current_xml_content)


def content_differs(xml_content1, xml_content2):
    """
    Determine whether or not the xml content of two SecurityLoan
Confirmations differ in terms of current SecurityLoan Confirmation data.
    """
    root_element1 = ElementTree.fromstring(xml_content1)
    root_element2 = ElementTree.fromstring(xml_content2)
    if _trades_xml_differs(root_element1, root_element2):
        return True
    return False


def _get_security_loan_parameter(parameter_name):
    """
    Get a documentation FParameter value.
    """
    return DocumentGeneral.get_fparameter('ABSASecurityLoanConfirmationParameters', parameter_name)


def _is_sec_loan_instrument_eligible_for_confirmation(instrument):
    """
    Determine whether or not an instrument is a swap that is a
    potential candidate to appear on a SecurityLoan Confirmation.
    """
    if instrument.InsType() != 'SecurityLoan':
        return False
    return True


def _is_sec_loan_trade_eligible_for_confirmation(trade):
    """
    Determine whether or not a trade is a swap that is a potential
    candidate to appear on a SecurityLoan Confirmation.
    """
    if not _is_sec_loan_instrument_eligible_for_confirmation(trade.Instrument()):
        return False
    if not _get_base_sec_loan_trade_asql_query().IsSatisfiedBy(trade):
        return False
    return True


def is_party_receiving_confirmations(counterparty, instrument_type):
    """
    Determine whether or not a party is configured to receive
    scheduled SecurityLoan Confirmations for the any instrument
    type.
    """
    return len(get_party_contacts(counterparty, instrument_type)) > 0


def get_party_contacts(counterparty, instrument_type):
    """
    Get any contacts for a party that are configured to receive
    confirmations.
    """
    contacts = list()
    for contact in counterparty.Contacts().AsArray():
        for contact_rule in contact.ContactRules().AsArray():
            if contact_rule.EventChlItem() is None:
                continue
            if contact_rule.EventChlItem().Name() != get_event_name():
                continue
            if contact_rule.InsType() != instrument_type:
                continue
            contacts.append(contact)
    return contacts


def get_valid_trades_for_counterparty(counterparty, document_type):
    """
    Gets all Sec Loan Confirmations Valid Trades
    """
    party_security_loan_trades = _get_active_sec_loan_trades_for_party(counterparty, document_type)
    valid_trades = list()
    for trade in party_security_loan_trades:
        if trade.AdditionalInfo().SL_ConfirmationSent() in [False, None]:
            valid_trades.append(trade)

    if len(valid_trades) > 0:
        return valid_trades

    return False


def _get_active_sec_loan_trades_for_party(party, trade_text1_field=''):
    """
    Get candidate active  trades for a
    party, inclusive from date and inclusive to date.
    """
    if trade_text1_field is None:
        trade_text1_field = ''
    asql_query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
    asql_query.AsqlNodes(_get_base_sec_loan_trade_asql_query())
    party_node = asql_query.AddOpNode('OR')
    party_node.AddAttrNode('AdditionalInfo.SL_G1Counterparty1', 'EQUAL', party.Name())
    party_node.AddAttrNode('AdditionalInfo.SL_G1Counterparty2', 'EQUAL', party.Name())
    asql_query.AddAttrNode('Text1', 'EQUAL', trade_text1_field)
    valid_status_node = asql_query.AddOpNode('OR')
    for valid_status in ['FO Confirmed', 'BO Confirmed']:
        valid_status_node.AddAttrNode('Status', 'EQUAL', valid_status)

    return asql_query.Select()


def _get_base_sec_loan_trade_asql_query():
    """
    Get the base asql query (static portion) to use for finding
    sec loan trades.
    """
    asql_query = acm.CreateFASQLQuery(acm.FTrade, 'AND')

    asql_query.AddAttrNode('Instrument.InsType', 'EQUAL', 'SecurityLoan')
    valid_text_node = asql_query.AddOpNode('OR')
    for valid_text in ['', None, 'PARTIAL_RETURN', 'FULL_RETURN']:
        valid_text_node.AddAttrNode('Text1', 'EQUAL', valid_text)
    asql_query.AddAttrNode('Acquirer.Name', 'EQUAL', 'SECURITY LENDINGS DESK')
    valid_status_node = asql_query.AddOpNode('OR')
    for valid_status in ['FO Confirmed', 'BO Confirmed', 'Void']:
        valid_status_node.AddAttrNode('Status', 'EQUAL', valid_status)
    asql_query.AddAttrNode('Instrument.ExpiryDate', 'GREATER_EQUAL', acm.Time.DateToday())
    asql_query.AddAttrNode('AdditionalInfo.SL_G1Counterparty1', 'NOT_EQUAL', None)
    asql_query.AddAttrNode('AdditionalInfo.SL_G1Counterparty2', 'NOT_EQUAL', None)

    return asql_query


def _get_generated_step_after_last_pending_generation_step(business_process):
    """
    Get the generated step from the last generation cycle, if such a
    generated step exists.
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

    This is useful for obtaining the last version of a SecurityLoan Confirmation that has been sent to the counterparty.
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


def _is_amended(business_process):
    """
    Determine whether or not a  business process
    has been amended (content altered since last version sent).
    """
    xml_content = retrieve_last_generated_confirmation_xml_content(business_process)
    root_element = ElementTree.fromstring(xml_content)
    return 'Amendment' in root_element.find('SUBJECT').text


def _is_cancelled(business_process):
    """
    Determine whether or not a  business process
    has been amended (content altered since last version sent).
    """
    xml_content = retrieve_last_generated_confirmation_xml_content(business_process)
    root_element = ElementTree.fromstring(xml_content)
    return 'Cancellation' in root_element.find('SUBJECT').text


def _generate_xml_element(element_name, element_text=''):
    """
    Generate an XML element with the specified name and text.
    """
    element = ElementTree.Element(element_name)
    element.text = element_text
    return element


def _trades_xml_differs(previous_root_element, current_root_element):
    """
    Determine whether or not the TRADES elements of two  XML content differ.
    """
    return _xml_differs(previous_root_element, current_root_element, 'TRADES')


def _xml_differs(element1, element2, xpath):
    """
    Determine whether or not two xml elements (identified by the
    specified xpath) differ.

    This implementation currently takes a dumb approach to XML
    comparison.  It simply determines whether or not the two XML
    elements match exactly in terms of text.  This implies that
    order of elements etc. is important to correct functioning.
    """
    compare_element1 = element1.find(xpath)
    compare_string1 = ElementTree.tostring(compare_element1)
    compare_element2 = element2.find(xpath)
    compare_string2 = ElementTree.tostring(compare_element2)
    return compare_string1 != compare_string2


def get_lender_or_borrower_party(trade):
    """
    Gets The actual lender or borrower party from SL_G1*
    add infos
    """
    party_name = trade.AdditionalInfo().SL_G1Counterparty1()
    if party_name and 'PRINCIPAL' in party_name:
        party_name = trade.AdditionalInfo().SL_G1Counterparty2()

    if party_name:
        return acm.FParty[party_name]

    return None


def is_lender(party):
    """
    Checks if party is the lender or Borrower
    """
    party_name = party.Name()
    lender_abrreviation = 'SLL'
    if party_name.startswith(lender_abrreviation):
        return True

    return False


def get_secloan_quantity(trade):
    quantity = acm.GetCalculatedValue(trade, acm.GetDefaultContext(), 'sl_quantity').Value()
    return quantity


def get_secloan_rate(trade):
    rate = acm.GetCalculatedValue(trade, acm.GetDefaultContext(), 'sl_rate').Value()
    return rate


def get_secloan_rate_excl_vat(rate):
    new_rate = '{0:.3f}'.format(rate/float(1.15))
    return new_rate


def get_return_value(trade):
    """
    Calculates the return value of the current trade
    """
    return trade.AdditionalInfo().SL_ReturnedQty()


def get_temporary_output_dir():
    return tempfile.mkdtemp()


def unix_chmod(path, mode):
    if os.name != 'nt':
        os.chmod(path, mode)


def check_for_confirmation_updates(trade, instrument_type):
    """
    Check for any confirmation updates on the Business Process
    """
    message = "Checking Trade '{trade}' for '{instrument_type}' "
    message += "Confirmations updates..."
    LOGGER.info(message.format(
        trade=trade.Oid(),
        instrument_type=instrument_type
    ))
    active_advice_business_processes = get_active_sec_loan_business_processes(
        trade, instrument_type, trade.Text1())
    if len(active_advice_business_processes) == 0:
        message = "No active '{instrument_type}' Confirmations found for "
        message += "Trade '{trade}', nothing to update."
        LOGGER.info(message.format(
            instrument_type=instrument_type,
            trade=trade.Oid()
        ))
        message1 = "Creating Amendment Confirmation for Trade '{trade}'"
        LOGGER.info(message1.format(
            trade=trade.Oid()
        ))
        create_sec_loan_business_process(trade, instrument_type, acm.Time.DateToday(), trade.Text1())
        return
    for business_process in active_advice_business_processes:
        check_for_updates(business_process)


def check_for_updates(business_process):
    """
    Determine whether or not a business process needs to be
    updated and, if so, trigger the regeneration.
    """
    acm.BeginTransaction()
    try:
        _check_for_updates(business_process)
        acm.CommitTransaction()
    except Exception as e:
        acm.AbortTransaction()
        raise e


def get_trades_from_previons_xml(previous_xml):

    trades = list()
    previous_root_element = ElementTree.fromstring(previous_xml)
    for element in previous_root_element.iterfind('TRADES/TRADE'):
        trade_element = Trade.from_xml_element(element)
        trades.append(trade_element)
    return trades


def update_sl_confirmation_sent_on_trades(xml_content):
    """

    """
    trade_elements = get_trades_from_previons_xml(xml_content)
    for trade in trade_elements:
        acm_trade = acm.FTrade[trade.trade_number]
        if acm_trade.AdditionalInfo().SL_ConfirmationSent() is True:
            continue
        try:
            acm_trade.AddInfoValue('SL_ConfirmationSent', True)            
            acm_trade.Commit()
            LOGGER.info('Changed SL_ConfirmationSent to Yes on trade {trade}'.format(trade=acm_trade.Oid()))
        except Exception as e:
            raise e


def add_confirmation_oid_on_trades(xml_content, business_process):
    """

    """
    trade_elements = get_trades_from_previons_xml(xml_content)
    for trade in trade_elements:
        acm_trade = acm.FTrade[trade.trade_number]
        try:
            acm_trade.AddInfoValue('SL_ConfirmationBP', business_process.Oid())
            acm_trade.Commit()
        except Exception as e:
            raise e


def _check_for_updates(business_process):
    """
    Perform the check to determine whether or not a Security Loan Confirmation
    needs to be updated and, if so, trigger the regeneration.
    """
    try:
        LOGGER.info("Checking Security Loan Confirmation {oid} for updates...".format(
            oid=business_process.Oid()
        ))
        if not is_in_updateable_state(business_process):
            message = "Security Loan Confirmation {oid} is not in an update-able state, "
            message += "nothing to update."
            LOGGER.info(message.format(
                oid=business_process.Oid()
            ))
            return

        elif confirmation_should_be_regenerated(business_process):
            message = "Security Loan Confirmation {oid} content will change if regenerated, "
            message += "triggering regeneration."
            LOGGER.info(message.format(
                oid=business_process.Oid()
            ))
            notes = acm.FArray()
            notes.Add('Confirmation Update Required - regenerating.')
            business_process.HandleEvent(EventNames.REGENERATE, None, notes)
            business_process.Commit()
        else:
            message = "Security Loan Confirmation {oid} content will not change if regenerated, "
            message += "nothing to update."
            LOGGER.info(message.format(
                oid=business_process.Oid()
            ))
    except Exception as exception:
        LOGGER.exception(exception)
        business_process.ForceToErrorState(traceback.format_exc())
        business_process.Commit()


def find_first_mbf_child_object(parent_mbf_object, name, name_prefixes=None):
    """
    Find the first child MBF message with the specified name.
    """
    for child_mbf_object in _find_mbf_child_objects(parent_mbf_object, name, name_prefixes):
        return child_mbf_object
    return None


def _find_mbf_child_objects(parent_mbf_object, name, name_prefixes=None):
    """
    Find all child MBF messages with the specified name.
    """
    names = _mbf_get_object_names(name, name_prefixes)
    current_child_mbf_object = parent_mbf_object.mbf_first_object()
    while current_child_mbf_object:
        if current_child_mbf_object.mbf_get_name() in names:
            yield current_child_mbf_object
        current_child_mbf_object = parent_mbf_object.mbf_next_object()


def _mbf_get_object_names(name, name_prefixes=None):
    """
    Get all possible variations of an MBF object name.
    """
    if name_prefixes is None:
        name_prefixes = _mbf_get_name_prefixes()
    else:
        _mbf_validate_name_prefixes(name_prefixes)
    return [name_prefix + name for name_prefix in name_prefixes]


def _mbf_validate_name_prefixes(name_prefixes):
    """
    Validate that the specified list of name prefixes are valid MBF
    name prefixes.
    """
    for name_prefix in name_prefixes:
        if name_prefix not in _mbf_get_name_prefixes():
            raise ValueError("Invalid mbf name prefix '{name_prefix}' specified.".format(
                name_prefix=name_prefix
            ))


def _mbf_get_name_prefixes():
    """
    Get all valid MBF name prefixes.
    """
    return ['', '+', '-', '!']
