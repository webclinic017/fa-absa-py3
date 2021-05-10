"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    DocumentConfirmationGeneral

DESCRIPTION
    This module contains general functionality for document confirmations.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-09-17      FAOPS-460       Cuen Edwards            Letitia Carboni         Refactored out from DocumentGeneral.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm

from at_logging import getLogger
import DocumentGeneral
import EnvironmentFunctions


LOGGER = getLogger(__name__)


def get_confirmation_from_date_add_info_name():
    """
    Get the name of the additional info field used for storing
    on a confirmation the inclusive document from date (if
    applicable).
    """
    return 'DocumentFromDate'


def get_confirmation_to_date_add_info_name():
    """
    Get the name of the additional info field used for storing
    on a confirmation the inclusive document to date (if
    applicable).
    """
    return 'DocumentToDate'


def get_confirmation_schedule_add_info_name():
    """
    Get the name of the additional info field used for storing on
    a confirmation the communication frequency schedule that the
    document was generated for.
    """
    return 'DocumentSchedule'


def get_confirmation_redemption_event_add_info_name():
    """
    Get the name of the additional info field used for storing on
    a confirmation the Redemption Event type for Demat and DIS.
    """
    return 'Redemption_Type'


def get_confirmation_from_date(confirmation):
    """
    Get the document from date additional info value for a
    confirmation.
    """
    return confirmation.OriginalConfirmation().add_info(
        get_confirmation_from_date_add_info_name())


def get_confirmation_to_date(confirmation):
    """
    Get the document to date additional info value for a
    confirmation.
    """
    return confirmation.OriginalConfirmation().add_info(
        get_confirmation_to_date_add_info_name())


def get_confirmation_schedule(confirmation):
    """
    Get the document communication frequency schedule
    additional info value for a confirmation.
    """
    return confirmation.OriginalConfirmation().add_info(
        get_confirmation_schedule_add_info_name())


def get_confirmation_redemption_event(confirmation):
    """
    Get the document communication frequency schedule
    additional info value for a confirmation.
    """
    return confirmation.OriginalConfirmation().add_info(
        get_confirmation_redemption_event_add_info_name())


def get_original_confirmation(confirmation):
    """
    Get the original confirmation for a confirmation.
    """
    parent_confirmation = confirmation.ConfirmationReference()
    if parent_confirmation is None:
        return confirmation
    return get_original_confirmation(parent_confirmation)


def get_default_confirmation_email_from(confirmation):
    """
    Get the default From email address to use for delivery of a
    document.
    """
    contact = get_confirmation_acquirer_contact(confirmation)
    # Ensure that only one from email is specified or the email
    # may be rejected by the mail server.
    return contact.Email().split(',')[0]


def get_default_confirmation_email_to(confirmation, non_production_email_addresses=None):
    """
    Get the default To email address to use for delivery of a
    document.

    In a non-production environment, the To address will be replaced
    by either the 'non_production_email_addresses' parameter (if
    specified) or the default non-production email addresses specified
    in the documentation FParameter 'DefaultNonProductionEmailToAddresses'.
    """
    contact = get_confirmation_counterparty_contact(confirmation)
    production_email_addresses = contact.Email()
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


def get_default_confirmation_email_bcc(confirmation, non_production_email_addresses=None):
    """
    Get the default BCC email address to use for delivery of a
    document.

    In a non-production environment, the BCC address will be replaced
    by either the 'non_production_email_addresses' parameter (if
    specified) or the default non-production email addresses specified
    in the documentation FParameter 'DefaultNonProductionEmailBCCAddresses'.
    """
    contact = get_confirmation_acquirer_contact(confirmation)
    production_email_addresses = contact.Email()
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


def get_confirmation_acquirer_contact(confirmation):
    """
    Get the acquirer contact to use for a confirmation.
    """
    contact = confirmation.AcquirerContactRef()
    if contact is not None:
        return contact
    for contact in confirmation.Acquirer().Contacts():
        if contact.Fullname() == confirmation.AcquirerContact():
            return contact
    exception_message = "Unable to find acquirer contact '{full_name}'."
    raise ValueError(exception_message.format(
        full_name=confirmation.AcquirerContact()
    ))


def get_confirmation_counterparty_contact(confirmation):
    """
    Get the counterparty contact to use for a confirmation.
    """
    contact = confirmation.CounterpartyContactRef()
    if contact is not None:
        return contact
    for contact in confirmation.Counterparty().Contacts():
        if contact.Fullname() == confirmation.CounterpartyContact():
            return contact
    exception_message = "Unable to find counterparty contact '{full_name}'."
    raise ValueError(exception_message.format(
        full_name=confirmation.CounterpartyContact()
    ))


def validate_confirmation_for_event(confirmation, event_name):
    """
    Validate that a confirmation is for a specified event name.
    """
    if (confirmation.EventChlItem() is None or
            confirmation.EventChlItem().Name() != event_name):
        raise ValueError("A confirmation for event '{event_name}' must be specified.".format(
            event_name=event_name
        ))


def active_confirmation_instruction_exists(counterparty, event_name, acquirer, instype,
        underlying_instype=None):
    """
    Determine whether or not a counterparty has an active confirmation
    instruction for a specified document event name, acquirer, instype,
    and optional underlying instype.
    """
    for confirmation_instruction in counterparty.ConfInstructions().AsArray():
        if not confirmation_instruction.Active():
            continue
        if confirmation_instruction.EventChlItem() is None:
            continue
        if confirmation_instruction.EventChlItem().Name() != event_name:
            continue
        if confirmation_instruction.InternalDepartment() is not None:
            if confirmation_instruction.InternalDepartment() != acquirer:
                continue
        if confirmation_instruction.InsType() != 'None':
            if confirmation_instruction.InsType() != instype:
                continue
        if confirmation_instruction.UndInsType() != 'None':
            if confirmation_instruction.UndInsType() != underlying_instype:
                continue
        return True
    return False


def get_existing_document_confirmations(document_event_name, acquirer, counterparty,
        from_date=None, to_date=None, document_schedule=None):
    """
    Get any existing document confirmations for the specified document
    event name, confirmation owner trade, and optional inclusive
    document from date, optional inclusive document to date, and
    optional document communication frequency schedule.
    """
    asql_query = acm.CreateFASQLQuery(acm.FConfirmation, 'AND')
    asql_query.AddAttrNode('EventChlItem.Name', 'EQUAL', document_event_name)
    # Add from date attribute if specified.
    if from_date is not None:
        from_date_method_name = DocumentGeneral.get_additional_info_method_name(
            get_confirmation_from_date_add_info_name())
        from_date_attribute_name = 'AdditionalInfo.{from_date_method_name}'.format(
            from_date_method_name=from_date_method_name
        )
        asql_query.AddAttrNode(from_date_attribute_name, 'EQUAL', from_date)
    # Add to date attribute if specified.
    if to_date is not None:
        to_date_method_name = DocumentGeneral.get_additional_info_method_name(
            get_confirmation_to_date_add_info_name())
        to_date_attribute_name = 'AdditionalInfo.{to_date_method_name}'.format(
            to_date_method_name=to_date_method_name
        )
        asql_query.AddAttrNode(to_date_attribute_name, 'EQUAL', to_date)
    # Add document schedule attribute if specified.
    if document_schedule is not None:
        document_schedule_method_name = DocumentGeneral.get_additional_info_method_name(
            get_confirmation_schedule_add_info_name())
        schedule_attribute_name = 'AdditionalInfo.{document_schedule_method_name}'.format(
            document_schedule_method_name=document_schedule_method_name
        )
        asql_query.AddAttrNode(schedule_attribute_name, 'EQUAL', document_schedule)
    asql_query.AddAttrNode('Trade.Acquirer.Oid', 'EQUAL', acquirer.Oid())
    asql_query.AddAttrNode('Trade.Counterparty.Oid', 'EQUAL', counterparty.Oid())
    return asql_query.Select()


def create_document_confirmation(document_event_name, confirmation_owner_trade,
        sub_type_object=None, from_date=None, to_date=None, document_schedule=None, redemption_event_type=None):
    """
    Create a document confirmation for the specified document event
    name, confirmation owner trade, optional sub type object, optional
    inclusive document from date, optional inclusive document to date,
    and optional document communication frequency schedule.
    """
    # Importing inside function to avoid creating cyclic import
    # dependencies.
    from FConfirmationCreator import FConfirmationCreator
    from FConfirmationUnderlyingObject import UnderlyingTrade
    underlying_object = UnderlyingTrade(confirmation_owner_trade)
    event = get_confirmation_event(document_event_name)
    trade_receiver_method = acm.FMethodChain(acm.FSymbol(str(event.receiver)))
    receiver = trade_receiver_method.Call([confirmation_owner_trade])
    confirmation_receiver_method = "Trade." + event.receiver
    confirmation = acm.Operations.CreateConfirmation(underlying_object.GetTrade(),
        event.eventName, sub_type_object, receiver, confirmation_receiver_method, None)
    # Set any document parameters on confirmation add info fields so
    # that values can be read when generating the confirmation XML.
    if from_date is not None:
        confirmation.AddInfoValue(get_confirmation_from_date_add_info_name(), from_date)
    if to_date is not None:
        confirmation.AddInfoValue(get_confirmation_to_date_add_info_name(), to_date)
    if document_schedule is not None:
        confirmation.AddInfoValue(get_confirmation_schedule_add_info_name(), document_schedule)
    if redemption_event_type is not None:
        confirmation.AddInfoValue(get_confirmation_redemption_event_add_info_name(), redemption_event_type)
    FConfirmationCreator.AddConfirmationData(underlying_object, confirmation)
    confirmation.Commit()
    message = "Created '{document_event_name}' confirmation {confirmation_oid} "
    message += "on trade {trade_oid}"
    LOGGER.info(message.format(
        document_event_name=document_event_name,
        confirmation_oid=confirmation.Oid(),
        trade_oid=confirmation_owner_trade.Oid()
    ))


def get_confirmation_event(event_name):
    """
    Get the event to associate with confirmations for a specified
    event name.
    """
    # Importing inside function to avoid creating cyclic import
    # dependencies.
    from FConfirmationEventFactory import FConfirmationEventFactory
    for event in FConfirmationEventFactory.GetConfirmationEvents():
        if event.eventName == event_name:
            return event
    exception_message = "Unable to find a confirmation event with "
    exception_message += "the name '{name}'."
    raise ValueError(exception_message.format(
        name=event_name
    ))


def get_confirmation_date_range_description(confirmation):
    """
    Get a description of the date range represented by a document
    confirmation (if applicable).
    """
    from_date = get_confirmation_from_date(confirmation)
    to_date = get_confirmation_to_date(confirmation)
    return DocumentGeneral.get_date_range_description(from_date, to_date)
