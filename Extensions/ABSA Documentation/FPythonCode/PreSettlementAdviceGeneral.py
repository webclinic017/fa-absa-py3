"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    PreSettlementAdviceGeneral

DESCRIPTION
    This module contains general functionality related to pre-settlement advices.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-09-17      FAOPS-460       Cuen Edwards            Letitia Carboni         Initial Implementation.
2019-10-14      FAOPS-531       Cuen Edwards            Letitia Carboni         Added support for amendments.
2020-02-07      FAOPS-744       Cuen Edwards            Kgomotso Gumbo          Fix for unnecessary regeneration due to estimated rates.
2020-02-21      FAOPS-544/547   Cuen Edwards            Letitia Carboni         Added support for FRAs.
2020-02-21      FAOPS-578/591   Cuen Edwards            Letitia Carboni         Added support for Currency Swaps.
2020-04-20      FAOPS-706       Cuen Edwards            Letitia Carboni         Changed grouping of party settlements on advices from
                                                                                implicit linking via SDSID to explicit linking via advice
                                                                                party additional info.
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


LOGGER = getLogger(__name__)


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


class EventNames(object):
    """
    A class representing the event names for a document business
    process using the 'Basic Document' state chart.

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
    A class representing the parameters for a pre-settlement advice
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


class AmendmentActions(object):
    """
    A class representing the amendment actions for a pre-settlement
    advice.

    An amendment action represents what happened for a settlement
    during an amendment - i.e. it was added, amended, removed (no
    longer due).

    This should be replaced with a proper enum when we eventually
    move to Python 3.
    """
    ADDED = 'Added'
    UPDATED = 'Updated'
    REMOVED = 'Removed'


class AmendmentReasons(object):
    """
    A class representing the amendment reasons for a pre-settlement
    advice.

    An amendment reason represents what caused an amendment to occur -
    i.e. a new trade was booked, amended, voided, terminated, etc.

    This should be replaced with a proper enum when we eventually
    move to Python 3.
    """
    NEW = 'New'
    AMENDED = 'Amended'
    CANCELLED = 'Cancelled'
    TERMINATED = 'Terminated'


class Settlement(object):
    """
    A class representing the details of a settlement for display on
    a pre-settlement advice.
    """

    _estimate_able_variable_names = ['amount', 'float_rate']

    def __init__(self):
        """
        Constructor.
        """
        self.bank_trade_reference = None
        self.markitwire_trade_reference = None
        self.counterparty_trade_reference = None
        self.settlement_reference = None
        self.counterparty_name = None
        self.currency = None
        self.is_estimate = None
        self.amount = None
        self.nominal = None
        self.pay_type = None
        self.trade_date = None
        self.effective_date = None
        self.termination_date = None
        self.payment_date = None
        self.payment_business_day_convention = None
        self.payment_calendars = None
        self.float_rate_reference = None
        self.float_rate = None
        self.spread = None
        self.fixed_rate = None
        self.reset_calendars = None
        self.days = None
        self.fixing_offset = None
        self.day_count_method = None
        self.rolling_period = None
        self.reset_business_day_convention = None
        self.amendment_action = None
        self.amendment_reason = None

    def __eq__(self, other):
        """
        Override of rich comparison method for the Equals operation.

        Determines whether or not this object is considered equal to
        another object.
        """
        if not isinstance(other, type(self)):
            return False
        other_variables = vars(other)
        for variable_name, variable_value in list(vars(self).items()):
            if self.is_estimate and variable_name in self._estimate_able_variable_names:
                # Ignore values that are estimated for comparison purposes
                # in order to prevent movement of an estimated value being
                # considered erroneously as an amendment.
                continue
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
        Convert this Settlement instance to its representation as
        an XML Element.
        """
        element = _generate_xml_element('SETTLEMENT')
        if self.amendment_action is not None:
            element.set('amendment_action', str(self.amendment_action))
        if self.amendment_reason is not None:
            element.set('amendment_reason', str(self.amendment_reason))
        element.append(_generate_xml_element('BANK_TRADE_REFERENCE', str(self.bank_trade_reference)))
        if self.markitwire_trade_reference is not None:
            element.append(_generate_xml_element('MARKITWIRE_TRADE_REFERENCE', self.markitwire_trade_reference))
        if self.counterparty_trade_reference is not None:
            element.append(_generate_xml_element('COUNTERPARTY_TRADE_REFERENCE', self.counterparty_trade_reference))
        element.append(_generate_xml_element('SETTLEMENT_REFERENCE', str(self.settlement_reference)))
        element.append(_generate_xml_element('COUNTERPARTY_NAME', self.counterparty_name))
        element.append(_generate_xml_element('CURRENCY', self.currency))
        element.append(_generate_xml_element('IS_ESTIMATE', str(self.is_estimate)))
        element.append(_generate_xml_element('AMOUNT', str(self.amount)))
        if self.nominal is not None:
            element.append(_generate_xml_element('NOMINAL', str(self.nominal)))
        element.append(_generate_xml_element('PAY_TYPE', self.pay_type))
        element.append(_generate_xml_element('TRADE_DATE', self.trade_date))
        element.append(_generate_xml_element('EFFECTIVE_DATE', self.effective_date))
        element.append(_generate_xml_element('TERMINATION_DATE', self.termination_date))
        element.append(_generate_xml_element('PAYMENT_DATE', self.payment_date))
        if self.payment_business_day_convention is not None:
            element.append(_generate_xml_element('PAYMENT_BUSINESS_DAY_CONVENTION', self
                .payment_business_day_convention))
        if self.payment_calendars is not None:
            element.append(_generate_xml_element('PAYMENT_CALENDARS', self.payment_calendars))
        if self.float_rate_reference is not None:
            element.append(_generate_xml_element('FLOAT_RATE_REFERENCE', self.float_rate_reference))
        if self.float_rate is not None:
            element.append(_generate_xml_element('FLOAT_RATE', str(self.float_rate)))
        if self.spread is not None:
            element.append(_generate_xml_element('SPREAD', str(self.spread)))
        if self.fixed_rate is not None:
            element.append(_generate_xml_element('FIXED_RATE', str(self.fixed_rate)))
        if self.reset_calendars is not None:
            element.append(_generate_xml_element('RESET_CALENDARS', self.reset_calendars))
        if self.days is not None:
            element.append(_generate_xml_element('DAYS', str(self.days)))
        if self.fixing_offset is not None:
            element.append(_generate_xml_element('FIXING_OFFSET', str(self.fixing_offset)))
        if self.day_count_method is not None:
            element.append(_generate_xml_element('DAY_COUNT_METHOD', self.day_count_method))
        if self.rolling_period is not None:
            element.append(_generate_xml_element('ROLLING_PERIOD', self.rolling_period))
        if self.reset_business_day_convention is not None:
            element.append(_generate_xml_element('RESET_BUSINESS_DAY_CONVENTION', self.reset_business_day_convention))
        return element

    @classmethod
    def from_xml_element(cls, settlement_element):
        """
        Convert the XML Element representation of a Settlement
        to an instance of Settlement.
        """
        settlement = Settlement()
        amendment_action = settlement_element.get('amendment_action')
        if amendment_action is not None:
            settlement.amendment_action = amendment_action
        amendment_reason = settlement_element.get('amendment_reason')
        if amendment_reason is not None:
            settlement.amendment_reason = amendment_reason
        settlement.bank_trade_reference = int(settlement_element.find('BANK_TRADE_REFERENCE').text)
        markitwire_trade_reference_element = settlement_element.find('MARKITWIRE_TRADE_REFERENCE')
        if markitwire_trade_reference_element is not None:
            settlement.markitwire_trade_reference = markitwire_trade_reference_element.text
        counterparty_trade_reference_element = settlement_element.find('COUNTERPARTY_TRADE_REFERENCE')
        if counterparty_trade_reference_element is not None:
            settlement.counterparty_trade_reference = counterparty_trade_reference_element.text
        settlement.settlement_reference = int(settlement_element.find('SETTLEMENT_REFERENCE').text)
        settlement.counterparty_name = settlement_element.find('COUNTERPARTY_NAME').text
        settlement.currency = settlement_element.find('CURRENCY').text
        settlement.is_estimate = DocumentGeneral.boolean_from_string(settlement_element.find('IS_ESTIMATE').text)
        settlement.amount = float(settlement_element.find('AMOUNT').text)
        nominal_amount_element = settlement_element.find('NOMINAL')
        if nominal_amount_element is not None:
            settlement.nominal = float(nominal_amount_element.text)
        settlement.pay_type = settlement_element.find('PAY_TYPE').text
        settlement.trade_date = settlement_element.find('TRADE_DATE').text
        settlement.effective_date = settlement_element.find('EFFECTIVE_DATE').text
        settlement.termination_date = settlement_element.find('TERMINATION_DATE').text
        settlement.payment_date = settlement_element.find('PAYMENT_DATE').text
        payment_business_day_convention_element = settlement_element.find('PAYMENT_BUSINESS_DAY_CONVENTION')
        if payment_business_day_convention_element is not None:
            settlement.payment_business_day_convention = payment_business_day_convention_element.text
        payment_calendars_element = settlement_element.find('PAYMENT_CALENDARS')
        if payment_calendars_element is not None:
            settlement.payment_calendars = payment_calendars_element.text
        float_rate_reference_element = settlement_element.find('FLOAT_RATE_REFERENCE')
        if float_rate_reference_element is not None:
            settlement.float_rate_reference = float_rate_reference_element.text
        float_rate_element = settlement_element.find('FLOAT_RATE')
        if float_rate_element is not None:
            settlement.float_rate = float(float_rate_element.text)
        spread_element = settlement_element.find('SPREAD')
        if spread_element is not None:
            settlement.spread = float(spread_element.text)
        fixed_rate_element = settlement_element.find('FIXED_RATE')
        if fixed_rate_element is not None:
            settlement.fixed_rate = float(fixed_rate_element.text)
        reset_calendars_element = settlement_element.find('RESET_CALENDARS')
        if reset_calendars_element is not None:
            settlement.reset_calendars = reset_calendars_element.text
        days_element = settlement_element.find('DAYS')
        if days_element is not None:
            settlement.days = int(days_element.text)
        fixing_offset_element = settlement_element.find('FIXING_OFFSET')
        if fixing_offset_element is not None:
            settlement.fixing_offset = int(fixing_offset_element.text)
        day_count_method_element = settlement_element.find('DAY_COUNT_METHOD')
        if day_count_method_element is not None:
            settlement.day_count_method = day_count_method_element.text
        rolling_period_element = settlement_element.find('ROLLING_PERIOD')
        if rolling_period_element is not None:
            settlement.rolling_period = rolling_period_element.text
        reset_business_day_convention_element = settlement_element.find('RESET_BUSINESS_DAY_CONVENTION')
        if reset_business_day_convention_element is not None:
            settlement.reset_business_day_convention = reset_business_day_convention_element.text
        return settlement


class SettlementInstruction(object):
    """
    A class representing a settlement instruction for display on a
    pre-settlement advice.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.currency = None
        self.account_number = None
        self.beneficiary_bank_name = None
        self.beneficiary_bank_bic = None
        self.correspondent_bank_name = None
        self.correspondent_bank_bic = None

    def __eq__(self, other):
        """
        Override of rich comparison method for the Equals operation.

        Determines whether or not this object is considered equal to
        another object.
        """
        if not isinstance(other, type(self)):
            return False
        other_variables = vars(other)
        for variable_name, variable_value in list(vars(self).items()):
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
        Convert this SettlementInstruction instance to its representation
        as an XML Element.
        """
        element = _generate_xml_element('SETTLEMENT_INSTRUCTION')
        element.append(_generate_xml_element('CURRENCY', self.currency))
        element.append(_generate_xml_element('ACCOUNT_NUMBER', self.account_number))
        element.append(_generate_xml_element('BENEFICIARY_BANK_NAME', self.beneficiary_bank_name))
        element.append(_generate_xml_element('BENEFICIARY_BANK_BIC', self.beneficiary_bank_bic))
        if self.correspondent_bank_name is not None:
            element.append(_generate_xml_element('CORRESPONDENT_BANK_NAME', self.correspondent_bank_name))
        if self.correspondent_bank_bic is not None:
            element.append(_generate_xml_element('CORRESPONDENT_BANK_BIC', self.correspondent_bank_bic))
        return element

    @classmethod
    def from_xml_element(cls, settlement_instruction_element):
        """
        Convert the XML Element representation of a Settlement
        Instruction to an instance of SettlementInstuction.
        """
        settlement_instruction = SettlementInstruction()
        currency = settlement_instruction_element.find('CURRENCY').text
        account_number = settlement_instruction_element.find('ACCOUNT_NUMBER').text
        beneficiary_bank_name = settlement_instruction_element.find('BENEFICIARY_BANK_NAME').text
        beneficiary_bank_bic = settlement_instruction_element.find('BENEFICIARY_BANK_BIC').text
        correspondent_bank_name = None
        correspondent_bank_name_element = settlement_instruction_element.find('CORRESPONDENT_BANK_NAME')
        if correspondent_bank_name_element is not None:
            correspondent_bank_name = correspondent_bank_name_element.text
        correspondent_bank_bic = None
        correspondent_bank_bic_element = settlement_instruction_element.find('CORRESPONDENT_BANK_BIC')
        if correspondent_bank_bic_element is not None:
            correspondent_bank_bic = correspondent_bank_bic_element.text
        settlement_instruction.currency = currency
        settlement_instruction.account_number = account_number
        settlement_instruction.beneficiary_bank_name = beneficiary_bank_name
        settlement_instruction.beneficiary_bank_bic = beneficiary_bank_bic
        settlement_instruction.correspondent_bank_name = correspondent_bank_name
        settlement_instruction.correspondent_bank_bic = correspondent_bank_bic
        return settlement_instruction


def get_advice_state_chart_name():
    """
    Get the name of the state chart used for pre-settlement advices.
    """
    return 'Pre-settlement Advice'


def get_advice_event_name():
    """
    Get the name of the event to associate with pre-settlement
    advices.
    """
    return 'Pre-settlement Advice'


def get_advice_party_add_info_name():
    """
    Get the name of the additional info field used for storing the
    party on whose advice a party's settlements are displayed.

    If no advice party is specified for a party then the party will
    receive it's own advice.
    """
    return 'SettleAdviceParty'


def get_supported_advice_instrument_types():
    """
    Get the instrument types supported by pre-settlement advices.
    """
    return ['CurrSwap', 'FRA', 'Swap']


def get_advice_description(business_process):
    """
    Get a description for a pre-settlement advice.
    """
    description = ""
    if _is_amended(business_process):
        description = "Amended "
    instrument_type = DocumentBusinessProcessGeneral.get_business_process_instrument_type(business_process)
    description += "{instrument_type_description} {document_type}".format(
        instrument_type_description=get_instrument_type_description(instrument_type),
        document_type=get_advice_event_name()
    )
    return description


def get_instrument_type_description(instrument_type):
    """
    Get a description of the pre-settlement advice instrument type.
    """
    if instrument_type == 'CurrSwap':
        return 'Currency Swap'
    return instrument_type


def has_been_generated(business_process):
    """
    Determine whether or not a document business process has been
    generated.
    """
    last_generated_step = _get_generated_step_after_last_pending_generation_step(business_process)
    return last_generated_step is not None


def generate_advice_xml_content(business_process, show_amendments):
    """
    Generate the XML content of a pre-settlement advice.
    """
    # Importing inside function to avoid creating cyclic import
    # dependencies.
    from PreSettlementAdviceXMLGenerator import GeneratePreSettlementAdviceXMLRequest, PreSettlementAdviceXMLGenerator
    advice_party = business_process.Subject()
    instrument_type = business_process.AddInfoValue(DocumentBusinessProcessGeneral
        .get_business_process_instype_add_info_name())
    from_date = business_process.AddInfoValue(DocumentBusinessProcessGeneral
        .get_business_process_from_date_add_info_name())
    to_date = business_process.AddInfoValue(DocumentBusinessProcessGeneral
        .get_business_process_to_date_add_info_name())
    previous_xml_content = None
    if show_amendments:
        previous_xml_content = retrieve_last_sent_advice_xml_content(business_process)
    request = GeneratePreSettlementAdviceXMLRequest(advice_party, instrument_type, from_date, to_date,
        previous_xml_content)
    return PreSettlementAdviceXMLGenerator().generate_xml(request)


def generate_advice_xlsx_content(xml_content):
    """
    Generate the Excel XLSX rendering of a pre-settlement advice.
    """
    # Importing inside function to avoid creating cyclic import
    # dependencies.
    from PreSettlementAdviceXLSXGenerator import (GeneratePreSettlementAdviceXLSXRequest,
        PreSettlementAdviceXLSXGenerator)
    bytes_io = io.BytesIO()
    request = GeneratePreSettlementAdviceXLSXRequest(xml_content, bytes_io)
    PreSettlementAdviceXLSXGenerator().generate_xlsx(request)
    return bytes_io.getvalue()


def store_advice_content(content, document_format):
    """
    Store the content for a generated format of a pre-settlement
    advice in persistent storage and return the URL of the storage
    location.
    """
    return DocumentGeneral.store_document_content(get_advice_event_name(), document_format, content)


def retrieve_last_generated_advice_xml_content(business_process):
    """
    Retrieve the XML content for the latest version of a pre-settlement
    advice business process that has been generated.
    """
    last_generated_step = _get_generated_step_after_last_pending_generation_step(business_process)
    if last_generated_step is None:
        return None
    generated_parameters = last_generated_step.DiaryEntry().Parameters()
    xml_content_url = generated_parameters[ParameterNames.XML_URL]
    return DocumentGeneral.retrieve_document_content(xml_content_url)


def retrieve_last_sent_advice_xml_content(business_process):
    """
    Retrieve the XML content for the latest version of a pre-
    settlement advice business process that has been sent to the
    associated counterparty.
    """
    last_sent_generated_step = _get_generated_step_before_last_sent_step(business_process)
    if last_sent_generated_step is None:
        return None
    generated_parameters = last_sent_generated_step.DiaryEntry().Parameters()
    xml_content_url = generated_parameters[ParameterNames.XML_URL]
    return DocumentGeneral.retrieve_document_content(xml_content_url)


def retrieve_last_generated_advice_xlsx_content(business_process):
    """
    Retrieve the XLSX content for the latest version of a pre-settlement
    advice business process that has been generated.
    """
    last_generated_step = _get_generated_step_after_last_pending_generation_step(business_process)
    if last_generated_step is None:
        return None
    generated_parameters = last_generated_step.DiaryEntry().Parameters()
    xlsx_content_url = generated_parameters[ParameterNames.XLSX_URL]
    return DocumentGeneral.retrieve_document_content(xlsx_content_url)


def generate_advice_xml_file(business_process):
    """
    Generate a pre-settlement advice XML file and return the file
    path.
    """
    xml_content = retrieve_last_generated_advice_xml_content(business_process)
    xml_content = minidom.parseString(xml_content).toprettyxml(indent='  ')
    xml_file_name = get_advice_file_name(business_process) + '.xml'
    xml_file_path = os.path.join(tempfile.mkdtemp(), xml_file_name)
    with open(xml_file_path, 'wb') as xml_file:
        xml_file.write(xml_content)
    return xml_file_path


def generate_advice_xlsx_file(business_process):
    """
    Generate a pre-settlement advice Excel XSLX file and return the
    file path.
    """
    xlsx_content = retrieve_last_generated_advice_xlsx_content(business_process)
    xlsx_file_name = get_advice_file_name(business_process) + '.xlsx'
    xlsx_file_path = os.path.join(tempfile.mkdtemp(), xlsx_file_name)
    with open(xlsx_file_path, 'wb') as xlsx_file:
        xlsx_file.write(xlsx_content)
    return xlsx_file_path


def get_advice_file_name(business_process):
    """
    Get the file name to be given to a pre-settlement advice.
    """
    # Counterparty name.
    counterparty_name = DocumentGeneral.get_party_full_name_and_short_code(
        business_process.Subject())
    # Period description.
    period_description = DocumentBusinessProcessGeneral.get_business_process_date_range_description(
        business_process)
    # Create file name.
    file_name_template = "{advice_description} {counterparty_name} {period_description}"
    file_name = file_name_template.format(
        advice_description=get_advice_description(business_process),
        counterparty_name=counterparty_name,
        period_description=period_description
    )
    return DocumentGeneral.format_file_name(file_name)


def get_bank_contact(business_process):
    """
    Get the bank contact to use for the delivery of a pre-settlement
    advice.
    """
    return DocumentBusinessProcessGeneral.get_default_counterparty_business_process_bank_contact(business_process)


def get_counterparty_contact(business_process):
    """
    Get the counterparty contact to use for the delivery of a pre-
    settlement advice.
    """
    return DocumentBusinessProcessGeneral.get_default_counterparty_business_process_counterparty_contact(
        business_process)


def get_email_from_name(bank_contact):
    """
    Get the from name to use in the email for delivery of a pre-
    settlement advice.
    """
    return DocumentBusinessProcessGeneral.get_default_counterparty_business_process_email_from_name(bank_contact)


def get_email_from_telephone(bank_contact):
    """
    Get the from telephone number to use in the email for delivery
    of a pre-settlement advice.
    """
    return DocumentBusinessProcessGeneral.get_default_counterparty_business_process_email_from_telephone(bank_contact)


def get_email_from_address(bank_contact):
    """
    Get the from email address to use for delivery of a pre-settlement
    advice.
    """
    return DocumentBusinessProcessGeneral.get_default_counterparty_business_process_email_from_address(bank_contact)


def get_email_to_addresses(counterparty_contact):
    """
    Get the to email addresses to use for delivery of a pre-settlement
    advice.
    """
    return DocumentBusinessProcessGeneral.get_default_counterparty_business_process_email_to(counterparty_contact)


def get_email_bcc_addresses(bank_contact):
    """
    Get any email addresses to be bcc'ed when delivering a pre-settlement
    advice.
    """
    return DocumentBusinessProcessGeneral.get_default_counterparty_business_process_email_bcc(bank_contact)


def get_email_subject(business_process):
    """
    Get the email subject to be used when delivering a pre-settlement
    advice.
    """
    return get_advice_file_name(business_process) + '.xlsx'


def get_email_body(from_name, from_telephone, from_email_address, business_process):
    """
    Get the email body to be used when delivering a pre-settlement
    advice.
    """
    # Importing inside function to avoid creating cyclic import
    # dependencies.
    from EmailBodyHTMLGenerator import EmailBodyHTMLGenerator, GenerateEmailBodyHTMLRequest
    document_description = 'your {advice_description} for {period_description}'
    document_description = document_description.format(
        advice_description=get_advice_description(business_process),
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
    Determine whether or not a pre-settlement advice should be
    automatically sent.
    """
    return DocumentGeneral.boolean_from_string(str(_get_advice_parameter('AutomaticallySend')))


def advice_business_process_exists(counterparty, instrument_type, from_date, to_date):
    """
    Determine if a pre-settlement advice business process exists for
    the specified counterparty, instrument type, inclusive from date
    and inclusive to date.
    """
    return len(get_existing_advice_business_processes(counterparty, instrument_type, from_date, to_date)) > 0


def get_existing_advice_business_processes(counterparty, instrument_type, from_date, to_date):
    """
    Get any existing pre-settlement advice business processes for the
    specified counterparty, instrument type, inclusive from date and
    inclusive to date.
    """
    asql_query = acm.CreateFASQLQuery(acm.FBusinessProcess, 'AND')
    asql_query.AddAttrNode('StateChart.Name', 'EQUAL', get_advice_state_chart_name())
    asql_query.AddAttrNode('Subject_type', 'EQUAL', 'Party')
    asql_query.AddAttrNode('Subject_seqnbr', 'EQUAL', counterparty.Oid())
    event_method_name = DocumentGeneral.get_additional_info_method_name(
        DocumentBusinessProcessGeneral.get_business_process_event_add_info_name())
    event_attribute_name = 'AdditionalInfo.{event_method_name}'.format(
        event_method_name=event_method_name
    )
    asql_query.AddAttrNode(event_attribute_name, 'EQUAL', get_advice_event_name())
    instrument_type_method_name = DocumentGeneral.get_additional_info_method_name(
        DocumentBusinessProcessGeneral.get_business_process_instype_add_info_name())
    instrument_type_attribute_name = 'AdditionalInfo.{instrument_type_method_name}'.format(
        instrument_type_method_name=instrument_type_method_name
    )
    asql_query.AddAttrNode(instrument_type_attribute_name, 'EQUAL', instrument_type)
    # Add from date attribute if specified.
    if from_date is not None:
        from_date_method_name = DocumentGeneral.get_additional_info_method_name(
            DocumentBusinessProcessGeneral.get_business_process_from_date_add_info_name())
        from_date_attribute_name = 'AdditionalInfo.{from_date_method_name}'.format(
            from_date_method_name=from_date_method_name
        )
        asql_query.AddAttrNode(from_date_attribute_name, 'EQUAL', from_date)
    # Add to date attribute if specified.
    if to_date is not None:
        to_date_method_name = DocumentGeneral.get_additional_info_method_name(
            DocumentBusinessProcessGeneral.get_business_process_to_date_add_info_name())
        to_date_attribute_name = 'AdditionalInfo.{to_date_method_name}'.format(
            to_date_method_name=to_date_method_name
        )
        asql_query.AddAttrNode(to_date_attribute_name, 'EQUAL', to_date)
    return asql_query.Select()


def create_advice_business_process(counterparty, instrument_type, from_date, to_date):
    """
    Create a pre-settlement advice business process for the specified
    counterparty, instrument type, inclusive from date and inclusive
    to date.
    """
    acm.BeginTransaction()
    try:
        state_chart = acm.FStateChart[get_advice_state_chart_name()]
        business_process = acm.BusinessProcess.InitializeProcess(counterparty, state_chart)
        business_process.AddInfoValue(DocumentBusinessProcessGeneral.get_business_process_event_add_info_name(),
            get_advice_event_name())
        business_process.AddInfoValue(DocumentBusinessProcessGeneral.get_business_process_instype_add_info_name(),
            instrument_type)
        business_process.AddInfoValue(DocumentBusinessProcessGeneral.get_business_process_from_date_add_info_name(),
            from_date)
        business_process.AddInfoValue(DocumentBusinessProcessGeneral.get_business_process_to_date_add_info_name(),
            to_date)
        business_process.HandleEvent(EventNames.GENERATE)
        business_process.Commit()
        acm.CommitTransaction()
    except:
        acm.AbortTransaction()
        raise


def get_active_advice_business_processes():
    """
    Get all active pre-settlement advice business processes.
    """
    asql_query = acm.CreateFASQLQuery(acm.FBusinessProcess, 'AND')
    asql_query.AddAttrNode('StateChart.Name', 'EQUAL', get_advice_state_chart_name())
    event_method_name = DocumentGeneral.get_additional_info_method_name(
        DocumentBusinessProcessGeneral.get_business_process_event_add_info_name())
    event_attribute_name = 'AdditionalInfo.{event_method_name}'.format(
        event_method_name=event_method_name
    )
    asql_query.AddAttrNode(event_attribute_name, 'EQUAL', get_advice_event_name())
    to_date_method_name = DocumentGeneral.get_additional_info_method_name(
        DocumentBusinessProcessGeneral.get_business_process_to_date_add_info_name())
    to_date_attribute_name = 'AdditionalInfo.{to_date_method_name}'.format(
        to_date_method_name=to_date_method_name
    )
    asql_query.AddAttrNode(to_date_attribute_name, 'GREATER_EQUAL', acm.Time.DateToday())
    return asql_query.Select()


def is_advice_receiving_party(counterparty):
    """
    Determine whether or not a party is configured to receive
    scheduled pre-settlement advices.
    """
    if counterparty.Type() == 'Intern Dept':
        return False
    if counterparty == DocumentGeneral.get_bank_party():
        return False
    advice_party = counterparty.AddInfoValue(get_advice_party_add_info_name())
    if advice_party not in [None, counterparty]:
        return False
    if len(_get_advice_contacts(counterparty)) == 0:
        return False
    return True


def find_parties_receiving_advices_for_instrument_type(instrument_type):
    """
    Find all parties configured to receive scheduled pre-settlement
    advices for the specified instrument type.
    """
    counterparties = set()
    select_expression = "eventChlItem = '{event_name}'".format(
        event_name=get_advice_event_name()
    )
    contact_rules = acm.FContactRule.Select(select_expression).AsArray()
    for contact_rule in contact_rules:
        if contact_rule.InsType() not in ['None', instrument_type]:
            continue
        counterparty = contact_rule.Contact().Party()
        if not is_advice_receiving_party(counterparty):
            continue
        counterparties.add(counterparty)
    return counterparties


def advice_money_flows_exist(advice_party, instrument_type, from_date, to_date):
    """
    Determine whether advice settlements exist for the specified
    advice party, instrument type, inclusive from date and inclusive
    to date.
    """
    for money_flow in get_advice_money_flows(advice_party, instrument_type, from_date, to_date):
        return True
    return False


def get_advice_money_flows(advice_party, instrument_type, from_date, to_date):
    """
    Get any pre-settlement advice money flows for the specified
    advice party, instrument type, inclusive from date and inclusive
    to date.
    """
    if not is_advice_receiving_party(advice_party):
        return []
    if instrument_type == 'Swap':
        return _get_swap_advice_money_flows(advice_party, from_date, to_date)
    elif instrument_type == 'FRA':
        return _get_fra_advice_money_flows(advice_party, from_date, to_date)
    elif instrument_type == 'CurrSwap':
        return _get_currency_swap_advice_money_flows(advice_party, from_date, to_date)
    raise ValueError("Unsupported instrument type '{instrument_type}' specified.".format(
        instrument_type=instrument_type
    ))


def validate_advice_date_range(from_date, to_date):
    """
    Validate a pre-settlement advice date range.
    """
    document_name = get_advice_event_name().lower()
    DocumentGeneral.validate_document_date_range(document_name, from_date, to_date)
    # Only permit creation of pre-settlement advices for the future.
    if from_date < acm.Time.DateToday():
        raise ValueError('A pre-settlement advice from date must be after today.')


def is_in_updateable_state(business_process):
    """
    Determine whether or not a pre-settlement advice is in an update-
    able state.
    """
    return business_process.CurrentStateName() not in [
        StateNames.READY,
        StateNames.PENDING_GENERATION,
        StateNames.GENERATION_FAILED
    ]


def advice_should_be_cancelled(business_process):
    """
    Determine whether or not a pre-settlement advice should be
    cancelled by determining whether or not there are no settlements
    eligible to appear on the advice and that no previous version of
    the pre-settlement advice has been sent.
    """
    if business_process.CurrentStateName() == StateNames.CANCELLED:
        return False
    counterparty = business_process.Subject()
    instrument_type = DocumentBusinessProcessGeneral.get_business_process_instrument_type(business_process)
    from_date = DocumentBusinessProcessGeneral.get_business_process_from_date(business_process)
    to_date = DocumentBusinessProcessGeneral.get_business_process_to_date(business_process)
    # Determine if money flows currently exist.
    if advice_money_flows_exist(counterparty, instrument_type, from_date, to_date):
        return False
    # No current money flows - determine if sent.
    return not _has_ever_been_sent(business_process)


def advice_should_be_regenerated(business_process):
    """
    Determine whether or not a pre-settlement advice should be
    regenerated by determining whether or not the content will change
    if regenerated.
    """
    previous_xml_content = retrieve_last_generated_advice_xml_content(business_process)
    current_xml_content = generate_advice_xml_content(business_process, show_amendments=True)
    return content_differs(previous_xml_content, current_xml_content)


def content_differs(xml_content1, xml_content2):
    """
    Determine whether or not the xml content of two pre-settlement
    advices differ in terms of current pre-settlement advice data.
    """
    root_element1 = ElementTree.fromstring(xml_content1)
    _normalise_for_comparison(root_element1)
    root_element2 = ElementTree.fromstring(xml_content2)
    _normalise_for_comparison(root_element2)
    if _settlements_xml_differs(root_element1, root_element2):
        return True
    if _settlement_instructions_xml_differs(root_element1, root_element2):
        return True
    return False


def content_is_empty(xml_content):
    """
    Determine whether or not specified xml content constitutes an
    empty pre-settlement advice.
    """
    root_element = ElementTree.fromstring(xml_content)
    return root_element.find('SETTLEMENTS/SETTLEMENT') is None


def _get_advice_parameter(parameter_name):
    """
    Get a documentation FParameter value.
    """
    return DocumentGeneral.get_fparameter('ABSAPreSettlementAdviceParameters', parameter_name)


def _is_swap_instrument_eligible_for_advice(instrument):
    """
    Determine whether or not an instrument is a swap that is a
    potential candidate to appear on a pre-settlement advice.
    """
    if instrument.InsType() != 'Swap':
        return False
    return True


def _is_fra_instrument_eligible_for_advice(instrument):
    """
    Determine whether or not an instrument is a FRA that is a
    potential candidate to appear on a pre-settlement advice.
    """
    if instrument.InsType() != 'FRA':
        return False
    return True


def _is_currency_swap_instrument_eligible_for_advice(instrument):
    """
    Determine whether or not an instrument is a currency swap that is
    a potential candidate to appear on a pre-settlement advice.
    """
    if instrument.InsType() != 'CurrSwap':
        return False
    return True


def _is_swap_trade_eligible_for_advice(trade):
    """
    Determine whether or not a trade is a swap that is a potential
    candidate to appear on a pre-settlement advice.
    """
    if not _is_swap_instrument_eligible_for_advice(trade.Instrument()):
        return False
    if not _get_base_swap_trade_asql_query().IsSatisfiedBy(trade):
        return False
    if trade.Counterparty().Type() == 'Intern Dept':
        return False
    acquirer_query_folder = _get_swap_acquirer_query_folder()
    if not acquirer_query_folder.IsSatisfiedBy(trade.Acquirer()):
        return False
    portfolio_query_folder = _get_swap_portfolio_query_folder()
    if not portfolio_query_folder.IsSatisfiedBy(trade.Portfolio()):
        return False
    return True


def _is_fra_trade_eligible_for_advice(trade):
    """
    Determine whether or not a trade is a FRA that is a potential
    candidate to appear on a pre-settlement advice.
    """
    if not _is_fra_instrument_eligible_for_advice(trade.Instrument()):
        return False
    if not _get_base_fra_trade_asql_query().IsSatisfiedBy(trade):
        return False
    if trade.Counterparty().Type() == 'Intern Dept':
        return False
    acquirer_query_folder = _get_fra_acquirer_query_folder()
    if not acquirer_query_folder.IsSatisfiedBy(trade.Acquirer()):
        return False
    portfolio_query_folder = _get_fra_portfolio_query_folder()
    if not portfolio_query_folder.IsSatisfiedBy(trade.Portfolio()):
        return False
    return True


def _is_currency_swap_trade_eligible_for_advice(trade):
    """
    Determine whether or not a trade is a currency swap that is a
    potential candidate to appear on a pre-settlement advice.
    """
    if not _is_currency_swap_instrument_eligible_for_advice(trade.Instrument()):
        return False
    if not _get_base_currency_swap_trade_asql_query().IsSatisfiedBy(trade):
        return False
    if trade.Counterparty().Type() == 'Intern Dept':
        return False
    acquirer_query_folder = _get_currency_swap_acquirer_query_folder()
    if not acquirer_query_folder.IsSatisfiedBy(trade.Acquirer()):
        return False
    portfolio_query_folder = _get_currency_swap_portfolio_query_folder()
    if not portfolio_query_folder.IsSatisfiedBy(trade.Portfolio()):
        return False
    return True


def _get_advice_contacts(counterparty):
    """
    Get any contacts for a party that are configured to receive
    scheduled pre-settlement advices.
    """
    contacts = set()
    for contact in counterparty.Contacts().AsArray():
        for contact_rule in contact.ContactRules().AsArray():
            if contact_rule.EventChlItem() is None:
                continue
            if contact_rule.EventChlItem().Name() != get_advice_event_name():
                continue
            contacts.add(contact)
    return contacts


def _get_swap_advice_money_flows(advice_party, from_date, to_date):
    """
    Get any swap pre-settlement advice money flows for the specified
    advice party, inclusive from date and inclusive to date.
    """
    money_flows = list()
    for trade in _get_active_swap_trades_for_advice_party(advice_party, from_date, to_date):
        if not _is_swap_trade_eligible_for_advice(trade):
            continue
        for money_flow in trade.MoneyFlows().AsArray():
            if not _is_swap_advice_money_flow(money_flow, from_date, to_date):
                continue
            money_flows.append(money_flow)
    return _remove_nett_zero_money_flows(money_flows)


def _get_active_swap_trades_for_advice_party(advice_party, from_date, to_date):
    """
    Get candidate active swap pre-settlement advice trades for an
    advice party, inclusive from date and inclusive to date.
    """
    trades = set()
    for party in _find_parties_with_advice_party(advice_party):
        party_trades = _get_active_swap_trades_for_party(party, from_date, to_date)
        trades.update(party_trades)
    return trades


def _get_active_swap_trades_for_party(party, from_date, to_date):
    """
    Get candidate active swap pre-settlement advice trades for a
    party, inclusive from date and inclusive to date.
    """
    asql_query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
    asql_query.AsqlNodes(_get_base_swap_trade_asql_query())
    asql_query.AddAttrNode('Counterparty.Oid', 'EQUAL', party.Oid())
    asql_query.AddAttrNode('ValueDay', 'LESS_EQUAL', to_date)
    asql_query.AddAttrNode('Instrument.ExpiryDate', 'GREATER_EQUAL', from_date)
    return asql_query.Select()


def _get_fra_advice_money_flows(advice_party, from_date, to_date):
    """
    Get any FRA pre-settlement advice money flows for the specified
    advice party, inclusive from date and inclusive to date.
    """
    money_flows = list()
    for trade in _get_active_fra_trades_for_advice_party(advice_party, from_date, to_date):
        if not _is_fra_trade_eligible_for_advice(trade):
            continue
        for money_flow in trade.MoneyFlows().AsArray():
            if not _is_fra_advice_money_flow(money_flow, from_date, to_date):
                continue
            money_flows.append(money_flow)
    return _remove_nett_zero_money_flows(money_flows)


def _get_active_fra_trades_for_advice_party(advice_party, from_date, to_date):
    """
    Get candidate active FRA pre-settlement advice trades for an
    advice party, inclusive from date and inclusive to date.
    """
    trades = set()
    for party in _find_parties_with_advice_party(advice_party):
        party_trades = _get_active_fra_trades_for_party(party, from_date, to_date)
        trades.update(party_trades)
    return trades


def _get_active_fra_trades_for_party(party, from_date, to_date):
    """
    Get candidate active FRA pre-settlement advice trades for a
    party, inclusive from date and inclusive to date.
    """
    asql_query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
    asql_query.AsqlNodes(_get_base_fra_trade_asql_query())
    asql_query.AddAttrNode('Counterparty.Oid', 'EQUAL', party.Oid())
    asql_query.AddAttrNode('ValueDay', 'LESS_EQUAL', to_date)
    asql_query.AddAttrNode('Instrument.ExpiryDate', 'GREATER_EQUAL', from_date)
    return asql_query.Select()


def _get_currency_swap_advice_money_flows(advice_party, from_date, to_date):
    """
    Get any currency swap pre-settlement advice money flows for the
    specified advice _party, inclusive from date and inclusive to date.
    """
    money_flows = list()
    for trade in _get_active_currency_swap_trades_for_advice_party(advice_party, from_date, to_date):
        if not _is_currency_swap_trade_eligible_for_advice(trade):
            continue
        for money_flow in trade.MoneyFlows().AsArray():
            if not _is_currency_swap_advice_money_flow(money_flow, from_date, to_date):
                continue
            money_flows.append(money_flow)
    return _remove_nett_zero_money_flows(money_flows)


def _get_active_currency_swap_trades_for_advice_party(advice_party, from_date, to_date):
    """
    Get candidate active currency swap pre-settlement advice trades
    for an advice party, inclusive from date and inclusive to date.
    """
    trades = set()
    for party in _find_parties_with_advice_party(advice_party):
        party_trades = _get_active_currency_swap_trades_for_party(party, from_date, to_date)
        trades.update(party_trades)
    return trades


def _get_active_currency_swap_trades_for_party(party, from_date, to_date):
    """
    Get candidate active currency swap pre-settlement advice trades
    for a party, inclusive from date and inclusive to date.
    """
    asql_query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
    asql_query.AsqlNodes(_get_base_currency_swap_trade_asql_query())
    asql_query.AddAttrNode('Counterparty.Oid', 'EQUAL', party.Oid())
    asql_query.AddAttrNode('ValueDay', 'LESS_EQUAL', to_date)
    asql_query.AddAttrNode('Instrument.ExpiryDate', 'GREATER_EQUAL', from_date)
    return asql_query.Select()


def _find_parties_with_advice_party(advice_party):
    """
    Find all parties whose settlements should appear on the advice
    for the specified advice party.
    """
    # Note this approach was taken as doing it with a Query Folder seems
    # rather slow.
    additional_info_spec = acm.FAdditionalInfoSpec[get_advice_party_add_info_name()]
    select_expression = "addInf = {spec_oid} and fieldValue = '{advice_party_name}'".format(
        spec_oid=additional_info_spec.Oid(),
        advice_party_name=advice_party.Name()
    )
    additional_infos = acm.FAdditionalInfo.Select(select_expression)
    parties = set()
    parties.add(advice_party)
    for additional_info in additional_infos:
        party = additional_info.Parent()
        if party is None:
            # This shouldn't happen but just in case
            # there are orphaned additional infos.
            continue
        if party == advice_party:
            # Party pointing to itself.
            continue
        # Add the current party.
        parties.add(party)
        # Add any parties referencing the current party -
        # allowing for tree structures.
        parties.update(_find_parties_with_advice_party(party))
    return parties


def _get_base_swap_trade_asql_query():
    """
    Get the base asql query (static portion) to use for finding
    swap pre-settlement advice trades.
    """
    asql_query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
    # Only certain statuses.
    status_node = asql_query.AddOpNode('OR')
    for status in ['BO Confirmed', 'BO-BO Confirmed', 'Terminated']:
        status_node.AddAttrNode('Status', 'EQUAL', status)
    # Only certain trade types.
    trade_type_node = asql_query.AddOpNode('OR')
    for trade_type in ['Normal', 'Closing']:
        trade_type_node.AddAttrNode('Type', 'EQUAL', trade_type)
    # Only non-Approx load trades.
    asql_query.AddAttrNode('AdditionalInfo.Approx_46_load', 'NOT_EQUAL', True)
    # Only the specified instrument type.
    asql_query.AddAttrNode('Instrument.InsType', 'EQUAL', 'Swap')
    return asql_query


def _get_base_fra_trade_asql_query():
    """
    Get the base asql query (static portion) to use for finding
    FRA pre-settlement advice trades.
    """
    asql_query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
    # Only certain statuses.
    status_node = asql_query.AddOpNode('OR')
    for status in ['BO Confirmed', 'BO-BO Confirmed', 'Terminated']:
        status_node.AddAttrNode('Status', 'EQUAL', status)
    # Only certain trade types.
    trade_type_node = asql_query.AddOpNode('OR')
    for trade_type in ['Normal', 'Closing']:
        trade_type_node.AddAttrNode('Type', 'EQUAL', trade_type)
    # Only non-Approx load trades.
    asql_query.AddAttrNode('AdditionalInfo.Approx_46_load', 'NOT_EQUAL', True)
    # Only the specified instrument type.
    asql_query.AddAttrNode('Instrument.InsType', 'EQUAL', 'FRA')
    return asql_query


def _get_base_currency_swap_trade_asql_query():
    """
    Get the base asql query (static portion) to use for finding
    currency swap pre-settlement advice trades.
    """
    asql_query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
    # Only certain statuses.
    status_node = asql_query.AddOpNode('OR')
    for status in ['BO Confirmed', 'BO-BO Confirmed', 'Terminated']:
        status_node.AddAttrNode('Status', 'EQUAL', status)
    # Only certain trade types.
    trade_type_node = asql_query.AddOpNode('OR')
    for trade_type in ['Normal', 'Closing']:
        trade_type_node.AddAttrNode('Type', 'EQUAL', trade_type)
    # Only non-Approx load trades.
    asql_query.AddAttrNode('AdditionalInfo.Approx_46_load', 'NOT_EQUAL', True)
    # Only the specified instrument type.
    asql_query.AddAttrNode('Instrument.InsType', 'EQUAL', 'CurrSwap')
    return asql_query


def _is_swap_advice_money_flow(money_flow, from_date, to_date):
    """
    Determine whether or not a money flow should appear on a
    swap pre-settlement advice for the specified period.
    """
    if money_flow.Type() not in ['Fixed Rate', 'Float Rate', 'Termination Fee']:
        return False
    if not _is_money_flow_settling_during_period(money_flow, from_date, to_date):
        return False
    if DocumentGeneral.is_zero_amount_money_flow(money_flow):
        return False
    return True


def _is_fra_advice_money_flow(money_flow, from_date, to_date):
    """
    Determine whether or not a money flow should appear on a
    FRA pre-settlement advice for the specified period.
    """
    if money_flow.Type() not in ['Float Rate', 'Termination Fee']:
        return False
    if not _is_money_flow_settling_during_period(money_flow, from_date, to_date):
        return False
    if DocumentGeneral.is_zero_amount_money_flow(money_flow):
        return False
    return True


def _is_currency_swap_advice_money_flow(money_flow, from_date, to_date):
    """
    Determine whether or not a money flow should appear on a
    currency swap pre-settlement advice for the specified period.
    """
    if money_flow.Type() not in ['Fixed Amount', 'Fixed Rate', 'Float Rate', 'Return', 'Termination Fee']:
        return False
    if not _is_money_flow_settling_during_period(money_flow, from_date, to_date):
        return False
    if DocumentGeneral.is_zero_amount_money_flow(money_flow):
        return False
    return True


def _is_money_flow_settling_during_period(money_flow, from_date, to_date):
    """
    Determine whether or not a money flow is settling between the
    specified from and to dates.
    """
    if money_flow.PayDate() > to_date:
        return False
    if money_flow.PayDate() < from_date:
        return False
    return True


def _remove_nett_zero_money_flows(money_flows):
    """
    Remove any money flows that nett to zero and, as such, will not
    need to be settled.
    """
    money_flows_by_netting_key = _get_money_flows_by_netting_key(money_flows)
    netted_money_flows = list()
    for netting_money_flows in list(money_flows_by_netting_key.values()):
        nett_amount = sum([DocumentGeneral.get_money_flow_amount(money_flow) for money_flow in netting_money_flows])
        if DocumentGeneral.is_almost_zero(nett_amount):
            continue
        netted_money_flows.extend(netting_money_flows)
    return netted_money_flows


def _get_money_flows_by_netting_key(money_flows):
    """
    Group the specified money flows by netting key and return as
    a dictionary with netting key as dictionary key and grouped money
    flows as dictionary value.
    """
    money_flows_by_netting_key = dict()
    for money_flow in money_flows:
        money_flow_type = money_flow.Type()
        money_flow_reference = DocumentGeneral.get_money_flow_reference(money_flow)
        netting_key = '{money_flow_type}_{money_flow_reference}'.format(
            money_flow_type=money_flow_type,
            money_flow_reference=money_flow_reference
        )
        if netting_key in list(money_flows_by_netting_key.keys()):
            money_flows_by_netting_key[netting_key].append(money_flow)
        else:
            money_flows_by_netting_key[netting_key] = [money_flow]
    return money_flows_by_netting_key


def _get_swap_acquirer_query_folder():
    """
    Get the query folder used to see if trades belonging to a specific
    acquirer should be included in swap pre-settlement advices.
    """
    name = str(_get_advice_parameter('SwapAcquirerQueryFolder'))
    return _get_query_folder_by_name(name, 'swap acquirer').Query()


def _get_fra_acquirer_query_folder():
    """
    Get the query folder used to see if trades belonging to a specific
    acquirer should be included in FRA pre-settlement advices.
    """
    name = str(_get_advice_parameter('FRAAcquirerQueryFolder'))
    return _get_query_folder_by_name(name, 'fra acquirer').Query()


def _get_currency_swap_acquirer_query_folder():
    """
    Get the query folder used to see if trades belonging to a specific
    acquirer should be included in currency swap pre-settlement advices.
    """
    name = str(_get_advice_parameter('CurrencySwapAcquirerQueryFolder'))
    return _get_query_folder_by_name(name, 'currency swap acquirer').Query()


def _get_swap_portfolio_query_folder():
    """
    Get the query folder used to see if trades belonging to a specific
    portfolio should be included in swap pre-settlement advices.
    """
    name = str(_get_advice_parameter('SwapPortfolioQueryFolder'))
    return _get_query_folder_by_name(name, 'swap portfolio').Query()


def _get_fra_portfolio_query_folder():
    """
    Get the query folder used to see if trades belonging to a specific
    portfolio should be included in FRA pre-settlement advices.
    """
    name = str(_get_advice_parameter('FRAPortfolioQueryFolder'))
    return _get_query_folder_by_name(name, 'fra portfolio').Query()


def _get_currency_swap_portfolio_query_folder():
    """
    Get the query folder used to see if trades belonging to a specific
    portfolio should be included in currency swap pre-settlement advices.
    """
    name = str(_get_advice_parameter('CurrencySwapPortfolioQueryFolder'))
    return _get_query_folder_by_name(name, 'currency swap portfolio').Query()


def _get_query_folder_by_name(name, description):
    """
    Get the stored query folder with the specified name.

    If a query folder cannot be found then an exception will be
    raised.
    """
    query_folder = acm.FStoredASQLQuery[name]
    if query_folder is None:
        raise ValueError("Unable to find {description} query folder '{name}'.".format(
            description=description,
            name=name
        ))
    return query_folder


def _get_generated_step_after_last_pending_generation_step(business_process):
    """
    Get the generated step from the last generation cycle, if such a
    generated step exists.

    This is useful for obtaining the latest version of a pre-settlement
    advice.  If a new generation cycle has been triggered but the pre-
    settlement advice has not yet been generated yet then None will be
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

    This is useful for obtaining the last version of a pre-settlement
    advice that has been sent to the counterparty.  If the advice has
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


def _is_amended(business_process):
    """
    Determine whether or not a pre-settlement advice business process
    has been amended (content altered since last version sent).
    """
    xml_content = retrieve_last_generated_advice_xml_content(business_process)
    root_element = ElementTree.fromstring(xml_content)
    return root_element.find('SETTLEMENTS/SETTLEMENT[@amendment_action]') is not None


def _has_ever_been_sent(business_process):
    """
    Determine whether or not a pre-settlement advice has ever been
    in a sent state.
    """
    for step in business_process.Steps().AsArray():
        if step.State().Name() == StateNames.SENT:
            return True
    return False


def _generate_xml_element(element_name, element_text=''):
    """
    Generate an XML element with the specified name and text.
    """
    element = ElementTree.Element(element_name)
    element.text = element_text
    return element


def _normalise_for_comparison(root_element):
    """
    Normalise the specified pre-settlement advice XML content for
    comparison purposes by removing any elements, etc. that may
    result in the generation of false amendments.
    """
    settlements_element = root_element.find("SETTLEMENTS")
    _remove_estimated_values(settlements_element)


def _remove_estimated_values(settlements_element):
    """
    Remove any estimated value elements from the specified pre-
    settlement advice XML content.
    """
    estimated_settlement_elements = settlements_element.findall("SETTLEMENT[IS_ESTIMATE='True']")
    for estimated_settlement_element in estimated_settlement_elements:
        for estimated_element_name in ["AMOUNT", "FLOAT_RATE"]:
            estimated_element = estimated_settlement_element.find(estimated_element_name)
            if estimated_element is not None:
                estimated_settlement_element.remove(estimated_element)


def _settlements_xml_differs(previous_root_element, current_root_element):
    """
    Determine whether or not the SETTLEMENTS elements of two pre-
    settlement advice XML content differ.
    """
    return _xml_differs(previous_root_element, current_root_element, 'SETTLEMENTS')


def _settlement_instructions_xml_differs(previous_root_element, current_root_element):
    """
    Determine whether or not the SETTLEMENT_INSTRUCTIONS elements of
    two pre-settlement advice XML content differ.
    """
    return _xml_differs(previous_root_element, current_root_element, 'SETTLEMENT_INSTRUCTIONS')


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
