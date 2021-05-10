"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    DocumentGeneral

DESCRIPTION
    This module contains general functionality shared by all documents.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2018-08-01      FAOPS-127       Cuen Edwards            Elaine Visagie          Refactored from a statement specific implementation to one
                                                                                that can be used for other documents.
2018-08-30                      Cuen Edwards                                    Refactored internals of function _get_documentation_parameter
                                                                                out into public get_fparameter function that can be used for
                                                                                other documents.
2018-09-25                      Cuen Edwards                                    Addition of email body defaults.
2019-09-17      FAOPS-460       Cuen Edwards            Letitia Carboni         Changes for new business process documents and refactored
                                                                                out document confirmation functionality.
2019-10-14      FAOPS-531       Cuen Edwards            Letitia Carboni         Added support for amendments.
2020-03-09      FAOPS-708       Tawanda Mukhalela       Ndivhuho Mashishimise   Added Support for ASUS confirmations.
2020-05-05      FAOPS-746       Cuen Edwards            Kgomotso Gumbo          Addition of support for Swift MT format.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import base64
import re
import uuid
import zlib

import acm
import ael
from at_logging import getLogger

import SessionFunctions


LOGGER = getLogger(__name__)
_calculation_space_collection = acm.Calculations().CreateStandardCalculationsSpaceCollection()
_content_url_base = 'adm://textobject/'


class Formats(object):
    """
    A class representing document formats.

    This should be replaced with a proper enum when we eventually
    move to Python 3.
    """
    CSV = 'CSV'
    MT = 'MT'
    PDF = 'PDF'
    XLSX = 'XLSX'
    XML = 'XML'


def get_bank_party():
    """
    Get the party whose details should be used to represent the bank.
    """
    bank_party_name = str(_get_documentation_parameter('BankPartyName'))
    bank_party = acm.FParty[bank_party_name]
    if bank_party is None:
        raise ValueError("Unable to find bank party '{bank_party_name}'.".format(
            bank_party_name=bank_party_name
        ))
    return bank_party


def get_default_bank_name():
    """
    Get the default bank name to use for any correspondence.
    """
    return str(_get_documentation_parameter('DefaultBankName'))


def get_default_bank_abbreviated_name():
    """
    Get the default bank abbreviated name to use for any correspondence.
    """
    return str(_get_documentation_parameter('DefaultBankAbbreviatedName'))


def get_default_document_from_name():
    """
    Get the default name of the from party to use for any
    correspondence.
    """
    return str(_get_documentation_parameter('DefaultDocumentFromName'))


def get_default_us_document_from_name():
    """
    Get the default name of the from party to use for any
    correspondence.
    """
    return str(_get_documentation_parameter('DefaultUSDocumentFromName'))


def get_default_document_from_website():
    """
    Get the default website URL of the from party to use for any
    correspondence.
    """
    return str(_get_documentation_parameter('DefaultDocumentFromWebSite'))


def get_default_document_footer():
    """
    Get the default website URL of the from party to use for any
    correspondence.
    """
    return str(_get_documentation_parameter('DefaultDocumentFooter'))


def get_default_email_body_from_name():
    """
    Get the default from name to display in the email body.
    """
    return str(_get_documentation_parameter('DefaultEmailBodyFromName'))


def get_default_email_body_font_colour():
    """
    Get the default email body font colour.
    """
    return str(_get_documentation_parameter('DefaultEmailBodyFontColour'))


def get_default_email_body_font_family():
    """
    Get the default email body font family.
    """
    return str(_get_documentation_parameter('DefaultEmailBodyFontFamily'))


def get_default_email_body_font_size():
    """
    Get the default email body font size.
    """
    return str(_get_documentation_parameter('DefaultEmailBodyFontSize'))


def get_default_non_production_email_to_addresses():
    """
    Get the default To email address to route documents to in a non-
    production environment.
    """
    return str(_get_documentation_parameter('DefaultNonProductionEmailToAddresses'))


def get_default_non_production_email_bcc_addresses():
    """
    Get the default BCC email address to route documents to in a non-
    production environment.
    """
    return str(_get_documentation_parameter('DefaultNonProductionEmailBCCAddresses'))


def get_bank_party_name():
    """
    Get the Bank Party Name.
    """
    return str(_get_documentation_parameter('BankPartyName'))


def get_default_bank_country_code():
    """
    Get the default bank country abbreviation.
    """
    return str(_get_documentation_parameter('DefaultBankCountry'))


def find_contact_by_contact_rules(party, acquirer=None, instrument_type=None, underlying_instrument_type=None,
        product_type=None, event_name=None, currency=None, issuance_type=None):
    """
    Attempts for find a contact according to contact rules for the
    specified criteria.

    Please note this function attempts to mimic Front Arena's
    internal contact selection behaviour which can broadly be
    summarised as follows:

    - The contact must have a rule that matches the trade and
      event (e.g. contact rule is for same acquirer as trade
      or for all acquirers, etc.).
    - If more than one matching contact is found then the closest
      match will be selected.  The closest match is determined by
      first comparing the contacts according to the priority order
      of contact rule criteria*. In the event that the contacts
      overlap in terms of rules then the most specific rule is
      selected*.

    If no matching contact is found, None is returned.

    *Refer to FCA1260 - PRIME Help.
    """
    selected_contact = None
    for contact in party.Contacts().AsArray():
        if not _contact_matches(contact, acquirer, instrument_type, underlying_instrument_type, product_type,
                event_name, currency, issuance_type):
            continue
        if selected_contact is None:
            selected_contact = contact
        else:
            selected_contact = _select_closest_matching_contact(selected_contact, contact, acquirer, instrument_type,
                underlying_instrument_type, product_type, event_name, currency, issuance_type)
    return selected_contact


def split_email_addresses(email_addresses):
    """
    Split a Front Arena email addresses string into a list of separate
    emails addresses.

    Multiple email addresses are stored in Front Arena by comma
    separators.
    """
    emails = list()
    for email in email_addresses.split(','):
        if is_string_value_present(email):
            emails.append(email.strip())
    return emails


def is_valid_email_address(email):
    """
    Determine whether or not an email address appears valid.
    """
    email_pattern = ('^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-zA-Z0-9-]+'
        '(\.[a-zA-Z0-9-]+)*(\.[a-zA-Z]+)$')
    return re.match(email_pattern, email)


def get_party_full_name_and_short_code(party):
    """
    Get the full name of a party, and if the party has a short code,
    followed by the short code in brackets.
    """
    party_name = get_party_full_name(party)
    party_short_code = get_party_short_code(party)
    if party_short_code is not None:
        party_name += ' ({party_short_code})'.format(
            party_short_code=party_short_code
        )
    return party_name


def get_party_full_name(party):
    """
    Get the full name of a party.

    If the party full name is None, empty, or only consists of
    whitespace, an exception will be raised.
    """
    if is_string_value_present(party.Fullname()):
        return party.Fullname().strip()
    raise ValueError("No full name specified for party '{party_name}'.".format(
        party_name=party.Name()
    ))


def get_party_short_code(party):
    """
    Get the short code of a party.
    """
    short_code = party.ShortCode()
    if is_string_value_present(short_code):
        return short_code.strip()
    return None


def get_fixing_source_name(fixing_source):
    """
    Get the name to display for a fixing source.
    """
    fixing_source_name_override = get_fixing_source_name_override(fixing_source)
    if fixing_source_name_override is None:
        return fixing_source.Name()
    return fixing_source_name_override


def get_fixing_source_name_override(fixing_source):
    """
    Get the name override for a fixing source if one exists else
    return None.
    """
    if fixing_source is None:
        raise ValueError('A fixing source must be specified.')
    parameters_extension = acm.GetDefaultContext().GetExtension(acm.FParameters, acm.FObject,
        'FixingSourceNameOverrides')
    if parameters_extension is None:
        return None
    parameters = parameters_extension.Value()
    if not parameters.HasKey(acm.FSymbol(fixing_source.Name())):
        return None
    return parameters.At(fixing_source.Name()).AsString()


def get_float_rate_reference_name(float_rate_reference):
    """
    Get the name to display for a float rate reference.
    """
    float_rate_reference_name_override = get_float_rate_reference_name_override(float_rate_reference)
    if float_rate_reference_name_override is None:
        return float_rate_reference.Name()
    return float_rate_reference_name_override


def get_float_rate_reference_name_override(float_rate_reference):
    """
    Get the name override for a float rate reference if one exists
    else return None.
    """
    if float_rate_reference is None:
        raise ValueError('A float rate reference must be specified.')
    free_text = float_rate_reference.FreeText()
    if is_string_value_present(free_text):
        return free_text.strip()
    return None


def get_date_range_description(from_date, to_date):
    """
    Get a description of the date range represented by a from date
    and a to date.
    """
    if _is_date_range_for_single_complete_year(from_date, to_date):
        # Single complete year - return e.g. 2018.
        return _format_date_as_year(from_date)
    elif _is_date_range_for_complete_years(from_date, to_date):
        # Multiple complete years - return e.g. 2017 to 2018.
        return '{from_year} to {to_year}'.format(
            from_year=_format_date_as_year(from_date),
            to_year=_format_date_as_year(to_date)
        )
    elif _is_date_range_for_single_complete_month(from_date, to_date):
        # Single complete month - return e.g. May 2018.
        return _format_date_as_month(from_date)
    elif _is_date_range_for_complete_months(from_date, to_date):
        # Multiple complete months - return e.g. May 2018 to June 2018.
        return '{from_month} to {to_month}'.format(
            from_month=_format_date_as_month(from_date),
            to_month=_format_date_as_month(to_date)
        )
    elif _is_date_range_for_single_day(from_date, to_date):
        # Single day - return e.g. 11 May 2018.
        return _format_date_as_full_date(from_date)
    else:
        # Format as full date range - return e.g. 11 May 2018 to 22 June 2018.
        return '{from_date} to {to_date}'.format(
            from_date=_format_date_as_full_date(from_date),
            to_date=_format_date_as_full_date(to_date)
        )


def validate_document_date_range(document_name, from_date, to_date):
    """
    Validate a document date range.
    """
    if from_date is None:
        raise ValueError('A {document_name} from date must be specified.'.format(
            document_name=document_name
        ))
    if to_date is None:
        raise ValueError('A {document_name} to date must be specified.'.format(
            document_name=document_name
        ))
    if from_date > to_date:
        raise ValueError('A {document_name} from date may not be after a {document_name} to date.'.format(
            document_name=document_name
        ))


def format_file_name(file_name):
    """
    Format a file_name into a cleaned-up and safe format for
    file systems.
    """
    file_name = file_name.strip()
    # Remove any characters that are not alphanumerics,
    # underscores, spaces, dots, dashes, and brackets.
    file_name = re.sub(r'(?u)[^\w ().-]', '', file_name)
    # Replace multiple spaces with a single space.
    file_name = re.sub(r' {2,}', ' ', file_name)
    return file_name


def show_confirm_dialog(title, message):
    """
    Display a dialog prompting the user to confirm whether or not
    to continue.
    """
    message_box = acm.GetFunction('msgBox', 3)
    yes_no_buttons = 4
    question_icon = 32
    yes_option = 6
    return message_box(title, message, yes_no_buttons |
        question_icon) == yes_option


def handle_script_exception(exception):
    """
    General error handler for AEL scripts.

    This function has the following behaviour:

    If running via Prime:
        - Display a more user-friendly error dialog than the default run script error dialog.
        - Ensure that the exception traceback is logged.

    If running via ATS, etc.:
        - re-raise the last thrown exception causing the script to exit.
        - Whether or not the the process exits with an error will depend on
          the settings of the relevant ATS, etc.
        - The exception traceback should be visible in the process output.
    """
    if SessionFunctions.is_prime():
        _show_error_dialog(exception)
        LOGGER.exception(exception)
    else:
        raise


def get_additional_info_method_name(additional_info_name):
    """
    Convert an additional info name to the corresponding name of a
    method on an FAdditionalInfoProxy object.
    """
    return additional_info_name.replace(' ', '_')


def get_fparameter(parameters_name, parameter_name):
    """
    Get an FParameter value.
    """
    parameters_extension = acm.GetDefaultContext().GetExtension(acm.FParameters, acm.FObject,
        parameters_name)
    if parameters_extension is None:
        exception_message = "Unable to find FParameters extension '{parameters_name}'"
        raise ValueError(exception_message.format(
            parameters_name=parameters_name
        ))
    parameters = parameters_extension.Value()
    if not parameters.HasKey(acm.FSymbol(parameter_name)):
        exception_message = "Unable to find '{parameters_name}' FParameters parameter "
        exception_message += "'{parameter_name}'"
        raise ValueError(exception_message.format(
            parameters_name=parameters_name,
            parameter_name=parameter_name
        ))
    return parameters.At(parameter_name)


def boolean_from_string(string_value):
    """
    Safely parse a string to a boolean value.
    """
    string_value_normalised = string_value.lower().strip()
    if string_value_normalised in ['true', '1']:
        return True
    if string_value_normalised in ['false', '0']:
        return False
    raise ValueError("Invalid boolean value '{string_value}' specified.".format(
        string_value=string_value
    ))


def get_money_flow_reference(money_flow):
    """
    Get a reference for the money flow.
    """
    return money_flow.SourceObject().Oid()


def get_money_flow_amount(money_flow):
    """
    Get the amount of a money flow.
    """
    return money_flow.Calculation().Projected(_calculation_space_collection).Number()


def is_zero_amount_money_flow(money_flow):
    """
    Determine whether or not a money flow has a zero value.
    """
    return is_almost_zero(get_money_flow_amount(money_flow))


def is_estimated_money_flow(money_flow):
    """
    Determine whether or not a money flow has a estimated (vs an
    known) value.
    """
    if is_cash_flow_money_flow(money_flow):
        # Consider adding explicit types here in order to make more robust.
        cash_flow = money_flow.SourceObject()
        for reset in cash_flow.Resets():
            if not reset.IsFixed():
                return True
        return False
    elif is_payment_money_flow(money_flow):
        return False
    # Add support for other money flows types as needed.
    raise NotImplementedError()


def is_cash_flow_money_flow(money_flow):
    """
    Determine whether or not a money flow represents an instrument
    cash flow.
    """
    return money_flow.IsKindOf(acm.FCashFlowMoneyFlow)


def is_payment_money_flow(money_flow):
    """
    Determine whether or not a money flow represents a trade payment.
    """
    return money_flow.IsKindOf(acm.FPaymentMoneyFlow)


def get_trade_buyer_name(trade):
    """
    Get the name of the buyer of a trade.
    """
    if trade.Bought():
        return get_default_bank_name()
    return get_party_full_name(trade.Counterparty())


def get_trade_seller_name(trade):
    """
    Get the name of the seller of a trade.
    """
    if trade.Bought():
        return get_party_full_name(trade.Counterparty())
    return get_default_bank_name()


def get_leg_payer_name(trade, leg):
    """
    Get the name of the payer of the cashflows of a trade leg.
    """
    if trade.Bought():
        if leg.PayLeg():
            return get_default_bank_name()
        else:
            return get_party_full_name(trade.Counterparty())
    else:
        if leg.PayLeg():
            return get_party_full_name(trade.Counterparty())
        else:
            return get_default_bank_name()


def get_leg_payment_calendars(leg):
    """
    Get a description of the leg payment calendars.
    """
    payment_calendars = ''
    calendars = [
        leg.PayCalendar(),
        leg.Pay2Calendar(),
        leg.Pay3Calendar(),
        leg.Pay4Calendar(),
        leg.Pay5Calendar()
    ]
    for calendar in calendars:
        if calendar is None:
            continue
        if len(payment_calendars) > 0:
            payment_calendars += ', '
        payment_calendars += calendar.Name()
    return payment_calendars


def get_leg_reset_calendars(leg):
    """
    Get a description of the leg reset calendars.
    """
    reset_calendars = ''
    calendars = [
        leg.ResetCalendar(),
        leg.Reset2Calendar(),
        leg.Reset3Calendar(),
        leg.Reset4Calendar(),
        leg.Reset5Calendar()
    ]
    for calendar in calendars:
        if calendar is None:
            continue
        if len(reset_calendars) > 0:
            reset_calendars += ', '
        reset_calendars += calendar.Name()
    return reset_calendars


def get_leg_rolling_period(leg):
    """
    Get a description of the leg rolling period.
    """
    period_count = acm.Time.DatePeriodCount(leg.RollingPeriod())
    period_unit = acm.Time.DatePeriodUnit(leg.RollingPeriod())
    return '{period_count} {period_unit}'.format(
        period_count=period_count,
        period_unit=period_unit
    )


def get_leg_payment_start_date(leg):
    """
    Get the first payment date for a swap leg.
    """
    cash_flows = leg.CashFlows().AsArray().SortByProperty('PayDate')
    for cash_flow in cash_flows:
        return cash_flow.PayDate()
    return None


def is_almost_zero(amount, epsilon=0.009):
    """
    Determine if an amount is 'almost zero'.
    """
    almost_zero = acm.GetFunction('almostZero', 2)
    return almost_zero(abs(amount), epsilon)


def format_amount(amount):
    """
    Ensure that any amounts that are very small are formatted as
    zero.
    """
    if is_almost_zero(amount):
        # Prevent values like -0.0 showing on the document.
        amount = 0.0
    return amount


def is_string_value_present(value):
    """
    Determine whether or not a string value is present (not None,
    empty, or only consisting of whitespace).
    """
    if value is None:
        return False
    return value.strip() != ''


def strip_dti_notation_from_funding_instype(funding_instype):
    """
    Removes DTI and NonDTI from trades funding instype addinfo field
    """
    return funding_instype.replace('NonDTI', '').replace('DTI', '').strip()


def store_document_content(event_name, document_format, content):
    """
    Store the content for a generated document format in persistent
    storage and return the URL of the storage location.
    """
    content_type = '{event_name} {document_format} Content'.format(
        event_name=event_name,
        document_format=document_format
    )
    name = str(uuid.uuid4())
    text_object = acm.FCustomTextObject()
    text_object.Name(name)
    text_object.SubType(content_type)
    text_object.Text(_encode_to_ascii(content))
    text_object.Commit()
    return _content_url_base + name


def retrieve_document_content(content_url):
    """
    Retrieve and return the document content identified by the
    specified URL from persistent storage.
    """
    name = content_url.replace(_content_url_base, '')
    text_object = acm.FCustomTextObject[name]
    if text_object is None:
        raise ValueError("No content found for url '{content_url}'.".format(
            content_url=content_url
        ))
    return _decode_from_ascii(text_object.Text())


def _get_documentation_parameter(parameter_name):
    """
    Get a documentation FParameter value.
    """
    return get_fparameter('ABSADocumentationParameters', parameter_name)


def _contact_matches(contact, acquirer, instrument_type, underlying_instrument_type, product_type, event_name,
        currency, issuance_type):
    """
    Determine whether or not a contact matches the specified criteria
    according to Front Arena's contact selection rules.
    """
    return len(_find_matching_contact_rules(contact, acquirer, instrument_type, underlying_instrument_type,
        product_type, event_name, currency, issuance_type)) > 0


def _find_matching_contact_rules(contact, acquirer, instrument_type, underlying_instrument_type, product_type,
        event_name, currency, issuance_type):
    """
    Attempts to find any contact rules that match the specified
    criteria according to Front Arena's contact selection rules.
    """
    matching_contact_rules = list()
    for contact_rule in contact.ContactRules().AsArray():
        # Acquirer.
        if contact_rule.Acquirer() is not None:
            if contact_rule.Acquirer() != acquirer:
                continue
        # InsType.
        if contact_rule.InsType() != 'None':
            if contact_rule.InsType() != instrument_type:
                continue
        # Underlying InsType.
        if contact_rule.UndInsType() != 'None':
            if contact_rule.UndInsType() != underlying_instrument_type:
                continue
        # Product Type.
        if contact_rule.ProductTypeChlItem() is not None:
            if contact_rule.ProductTypeChlItem() != product_type:
                continue
        # Event.
        if contact_rule.EventChlItem() is not None:
            if contact_rule.EventChlItem().Name() != event_name:
                continue
        # Currency.
        if contact_rule.Currency() is not None:
            if contact_rule.Currency() != currency:
                continue
        # Issuance Type.
        if contact_rule.IssuanceType() != 'None':
            if contact_rule.IssuanceType() != issuance_type:
                continue
        matching_contact_rules.append(contact_rule)
    return matching_contact_rules


def _select_closest_matching_contact(contact1, contact2, acquirer, instrument_type, underlying_instrument_type,
        product_type, event_name, currency, issuance_type):
    """
    Selects the closest match, out of two contacts, for the specified
    criteria according to Front Arena's contact selection based on
    priority order and most specific.
    """
    contact_rules = list()
    contact_rules.extend(_find_matching_contact_rules(contact1, acquirer, instrument_type,
        underlying_instrument_type, product_type, event_name, currency, issuance_type))
    contact_rules.extend(_find_matching_contact_rules(contact2, acquirer, instrument_type,
        underlying_instrument_type, product_type, event_name, currency, issuance_type))
    selected_contact_rule = None
    for contact_rule in contact_rules:
        if selected_contact_rule is None:
            selected_contact_rule = contact_rule
        else:
            selected_contact_rule = _select_closest_matching_contact_rule(selected_contact_rule,
                contact_rule)
    if selected_contact_rule is not None:
        return selected_contact_rule.Contact()
    return None


def _select_closest_matching_contact_rule(contact_rule1, contact_rule2):
    """
    Selects the closest match, out of two contact rules, for the specified
    criteria according to Front Arena's contact selection based on
    priority order and most specific.
    """
    # Acquirer.
    if contact_rule1.Acquirer() is not None and contact_rule2.Acquirer() is None:
        return contact_rule1
    if contact_rule2.Acquirer() is not None and contact_rule1.Acquirer() is None:
        return contact_rule2
    if contact_rule1.Acquirer() != contact_rule2.Acquirer():
        raise RuntimeError('Expecting to receive two matching contact rules.')
    # Issuance Type.
    if contact_rule1.IssuanceType() != 'None' and contact_rule2.IssuanceType() == 'None':
        return contact_rule1
    if contact_rule2.IssuanceType() != 'None' and contact_rule1.IssuanceType() == 'None':
        return contact_rule2
    if contact_rule1.IssuanceType() != contact_rule2.IssuanceType():
        raise RuntimeError('Expecting to receive two matching contact rules.')
    # Product Type.
    if (contact_rule1.ProductTypeChlItem() is not None and
            contact_rule1.ProductTypeChlItem() != contact_rule2.ProductTypeChlItem()):
        return contact_rule1
    if (contact_rule2.ProductTypeChlItem() is not None and
            contact_rule2.ProductTypeChlItem() != contact_rule1.ProductTypeChlItem()):
        return contact_rule2
    if contact_rule1.ProductTypeChlItem() != contact_rule2.ProductTypeChlItem():
        raise RuntimeError('Expecting to receive two matching contact rules.')
    # Underlying InsType.
    if contact_rule1.UndInsType() != 'None' and contact_rule1.UndInsType() != contact_rule2.UndInsType():
        return contact_rule1
    if contact_rule2.UndInsType() != 'None' and contact_rule2.UndInsType() != contact_rule1.UndInsType():
        return contact_rule2
    if contact_rule1.UndInsType() != contact_rule2.UndInsType():
        raise RuntimeError('Expecting to receive two matching contact rules.')
    # InsType.
    if contact_rule1.InsType() != 'None' and contact_rule1.InsType() != contact_rule2.InsType():
        return contact_rule1
    if contact_rule2.InsType() != 'None' and contact_rule2.InsType() != contact_rule1.InsType():
        return contact_rule2
    if contact_rule1.InsType() != contact_rule2.InsType():
        raise RuntimeError('Expecting to receive two matching contact rules.')
    # Event.
    if contact_rule1.EventChlItem() is not None and contact_rule1.EventChlItem() != contact_rule2.EventChlItem():
        return contact_rule1
    if contact_rule2.EventChlItem() is not None and contact_rule2.EventChlItem() != contact_rule1.EventChlItem():
        return contact_rule2
    if contact_rule1.EventChlItem() != contact_rule2.EventChlItem():
        raise RuntimeError('Expecting to receive two matching contact rules.')
    # Currency.
    if contact_rule1.Currency() is not None and contact_rule1.Currency() != contact_rule2.Currency():
        return contact_rule1
    if contact_rule2.Currency() is not None and contact_rule2.Currency() != contact_rule1.Currency():
        return contact_rule2
    if contact_rule1.Currency() != contact_rule2.Currency():
        raise RuntimeError('Expecting to receive two matching contact rules.')
    return contact_rule1


def _show_error_dialog(exception):
    """
    Display an error dialog to the user.
    """
    message_box = acm.GetFunction('msgBox', 3)
    ok_button = 0
    error_icon = 16
    message_box('Error', str(exception), ok_button | error_icon)


def _is_date_range_for_single_complete_year(from_date, to_date):
    """
    Determine whether or not a date range represents a single
    complete year.
    """
    if not _is_date_range_for_complete_years(from_date, to_date):
        return False
    from_date_year = acm.Time.DateToYMD(from_date)[0]
    to_date_year = acm.Time.DateToYMD(to_date)[0]
    return from_date_year == to_date_year


def _is_date_range_for_complete_years(from_date, to_date):
    """
    Determine whether or not a date range represents complete
    years.
    """
    if not _is_first_day_of_year(from_date):
        return False
    if not _is_last_day_of_year(to_date):
        return False
    return True


def _is_date_range_for_single_complete_month(from_date, to_date):
    """
    Determine whether or not a date range represents a single
    complete month.
    """
    if not _is_date_range_for_complete_months(from_date, to_date):
        return False
    from_date_month = acm.Time.DateToYMD(from_date)[1]
    to_date_month = acm.Time.DateToYMD(to_date)[1]
    return from_date_month == to_date_month


def _is_date_range_for_complete_months(from_date, to_date):
    """
    Determine whether or not a date range represents complete
    months.
    """
    if not _is_first_day_of_month(from_date):
        return False
    if not _is_last_day_of_month(to_date):
        return False
    return True


def _is_date_range_for_single_day(from_date, to_date):
    """
    Determine whether or not a date range represents a single
    day.
    """
    return from_date == to_date


def _is_first_day_of_year(date):
    """
    Determine whether or not a date is the first day of a year.
    """
    return date == acm.Time.FirstDayOfYear(date)


def _is_last_day_of_year(date):
    """
    Determine whether or not a date is the last day of a year.
    """
    year = acm.Time.DateToYMD(date)[0]
    return date == acm.Time.DateFromYMD(year, 12, 31)


def _is_first_day_of_month(date):
    """
    Determine whether or not a date is the first day of a month.
    """
    return date == acm.Time.FirstDayOfMonth(date)


def _is_last_day_of_month(date):
    """
    Determine whether or not a date is the last day of a month.
    """
    return acm.Time.DayOfMonth(date) == acm.Time.DaysInMonth(date)


def _format_date_as_year(date):
    """
    Format a date as a year (e.g. 2018).
    """
    return ael.date(date).to_string('%Y')


def _format_date_as_month(date):
    """
    Format a date as a month (e.g. June 2018).
    """
    return ael.date(date).to_string('%B %Y')


def _format_date_as_full_date(date):
    """
    Format a date as a full date (e.g. 11 June 2018).
    """
    return ael.date(date).to_string('%d %B %Y')


def _encode_to_ascii(value):
    """
    Encode a value to ascii.
    """
    return base64.b64encode(zlib.compress(value, 9))


def _decode_from_ascii(value):
    """
    Decode a value from ascii.
    """
    return zlib.decompress(base64.b64decode(value))
