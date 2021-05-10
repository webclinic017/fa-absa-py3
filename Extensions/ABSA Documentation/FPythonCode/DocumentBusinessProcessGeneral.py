"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    DocumentBusinessProcessGeneral

DESCRIPTION
    This module contains general functionality for document business processes.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-09-17      FAOPS-460       Cuen Edwards            Letitia Carboni         Initial version.
2019-10-14      FAOPS-531       Cuen Edwards            Letitia Carboni         Added support for amendments.
2020-01-31      FAOPS-557       Tawanda Mukhalela       Khaya Mbebe             Added BP_TradeType AdditionalInfo
2020-05-04      FAOPS-746       Cuen Edwards            Kgomotso Gumbo          Added additional info field for business process that
                                                                                only require one date.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

from at_logging import getLogger
import DocumentGeneral
import EnvironmentFunctions


LOGGER = getLogger(__name__)


def get_business_process_event_add_info_name():
    """
    Get the name of the additional info field used for storing
    on a business process the related event (if
    applicable).
    """
    return 'BP_Event'


def get_business_process_instype_add_info_name():
    """
    Get the name of the additional info field used for storing
    on a business process the related instrument type (if
    applicable).
    """
    return 'BP_InsType'


def get_business_process_date_add_info_name():
    """
    Get the name of the additional info field used for storing
    on a business_process the document date (if applicable).
    """
    return 'BP_Date'


def get_business_process_from_date_add_info_name():
    """
    Get the name of the additional info field used for storing
    on a business_process the inclusive document from date (if
    applicable).
    """
    return 'BP_FromDate'


def get_business_process_to_date_add_info_name():
    """
    Get the name of the additional info field used for storing
    on a business_process the inclusive document to date (if
    applicable).
    """
    return 'BP_ToDate'


def get_business_process_trade_type_add_info_name():
    """
    Gets the name of the additional info field used for storing
    on a business_process the Trade Type
    """
    return 'BP_TradeType'


def get_business_process_event(business_process):
    """
    Get the document event additional info value for a
    business process.
    """
    return business_process.add_info(get_business_process_event_add_info_name())


def get_business_process_instrument_type(business_process):
    """
    Get the document instrument type additional info value for a
    business process.
    """
    return business_process.add_info(get_business_process_instype_add_info_name())


def get_business_process_date(business_process):
    """
    Get the document date additional info value for a business
    process.
    """
    return business_process.add_info(get_business_process_date_add_info_name())


def get_business_process_from_date(business_process):
    """
    Get the document from date additional info value for a
    business process.
    """
    return business_process.add_info(get_business_process_from_date_add_info_name())


def get_business_process_to_date(business_process):
    """
    Get the document to date additional info value for a
    business process.
    """
    return business_process.add_info(get_business_process_to_date_add_info_name())


def get_default_counterparty_business_process_bank_contact(business_process):
    """
    Get the default bank contact to use for a document business
    process belonging to a counterparty subject.
    """
    bank_party = DocumentGeneral.get_bank_party()
    return _get_business_process_party_contact(bank_party, 'bank', business_process)


def get_default_counterparty_business_process_counterparty_contact(business_process):
    """
    Get the default counterparty contact to use for a document
    business process belonging to a counterparty subject
    """
    counterparty = business_process.Subject()
    return _get_business_process_party_contact(counterparty, 'counterparty', business_process)


def get_default_counterparty_business_process_email_from_name(bank_contact):
    """
    Get the default from name to use in the email for delivery of a
    document business process belonging to a counterparty subject.
    """
    from_name = bank_contact.Attention()
    if DocumentGeneral.is_string_value_present(from_name):
        return from_name.strip()
    exception_message = "No attention specified for '{party_name}' contact '{contact_name}'."
    raise ValueError(exception_message.format(
        party_name=bank_contact.Party().Name(),
        contact_name=bank_contact.Fullname()
    ))


def get_default_counterparty_business_process_email_from_telephone(bank_contact):
    """
    Get the from telephone number to use in the email for delivery of
    a document business process belonging to a counterparty subject.
    """
    telephone_number = bank_contact.Telephone()
    if DocumentGeneral.is_string_value_present(telephone_number):
        return telephone_number.strip()
    exception_message = "No telephone number specified for '{party_name}' contact '{contact_name}'."
    raise ValueError(exception_message.format(
        party_name=bank_contact.Party().Name(),
        contact_name=bank_contact.Fullname()
    ))


def get_default_counterparty_business_process_email_from_address(bank_contact):
    """
    Get the default from email address to use for delivery of a
    document business process belonging to a counterparty subject.
    """
    from_email_addresses = bank_contact.Email()
    if DocumentGeneral.is_string_value_present(from_email_addresses):
        # Ensure that only one from email is specified or the email
        # may be rejected by the mail server.
        return from_email_addresses.split(',')[0]
    exception_message = "No email address specified for '{party_name}' contact '{contact_name}'."
    raise ValueError(exception_message.format(
        party_name=bank_contact.Party().Name(),
        contact_name=bank_contact.Fullname()
    ))


def get_default_counterparty_business_process_email_to(counterparty_contact, non_production_email_addresses=None):
    """
    Get the default to email address to use for delivery of a document
    business process belonging to a counterparty subject.

    In a non-production environment, the To address will be replaced
    by either the 'non_production_email_addresses' parameter (if
    specified) or the default non-production email addresses specified
    in the documentation FParameter 'DefaultNonProductionEmailToAddresses'.
    """
    production_email_addresses = counterparty_contact.Email()
    if EnvironmentFunctions.is_production_environment():
        return production_email_addresses
    if non_production_email_addresses is None:
        non_production_email_addresses = DocumentGeneral.get_default_non_production_email_to_addresses()
    message = "Non-production environment detected - overriding 'To' email "
    message += "address with '{non_production_email_addresses}' (would have "
    message += "been sent to '{production_email_addresses}')."
    LOGGER.info(message.format(
        non_production_email_addresses=non_production_email_addresses,
        production_email_addresses=production_email_addresses
    ))
    return non_production_email_addresses


def get_default_counterparty_business_process_email_bcc(bank_contact, non_production_email_addresses=None):
    """
    Get the default bcc email address to use for delivery of a document
    business process belonging to a counterparty subject.

    In a non-production environment, the BCC address will be replaced
    by either the 'non_production_email_addresses' parameter (if
    specified) or the default non-production email addresses specified
    in the documentation FParameter 'DefaultNonProductionEmailBCCAddresses'.
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


def is_document_business_process(business_process):
    """
    Determine whether or not an event object is a document
    business process.
    """
    # Importing inside function to avoid creating cyclic import
    # dependencies.
    import DocumentProcessingParameters
    state_chart_name = business_process.StateChart().Name()
    return state_chart_name in DocumentProcessingParameters.state_chart_names


def get_document_processor(business_process):
    """
    Get the document processor for a specified document business
    process.
    """
    # Importing inside function to avoid creating cyclic import
    # dependencies.
    import DocumentProcessingParameters
    event_name = get_business_process_event(business_process)
    return DocumentProcessingParameters.event_name_to_processor_map[event_name]


def get_business_process_date_range_description(business_process):
    """
    Get a description of the date range represented by a document
    business_process (if applicable).
    """
    from_date = get_business_process_from_date(business_process)
    to_date = get_business_process_to_date(business_process)
    return DocumentGeneral.get_date_range_description(from_date, to_date)


def _get_business_process_party_contact(party, party_description, business_process):
    """
    Get the party contact to use for a document business process.
    """
    instrument_type = get_business_process_instrument_type(business_process)
    event_name = get_business_process_event(business_process)
    contact = DocumentGeneral.find_contact_by_contact_rules(party, instrument_type=instrument_type,
        event_name=event_name)
    if contact is not None:
        return contact
    exception_message = "Unable to matching find {party_description} contact."
    raise ValueError(exception_message.format(
        party_description=party_description
    ))
