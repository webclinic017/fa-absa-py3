"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    OperationsSTPMessageAdaptations

DESCRIPTION
    This module contains any message adaptation hooks for the Operations STP AMBA.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2020-04-30      FAOPS-700       Cuen Edwards            Kgomotso Gumbo          Initial implementation.
2020-12-10      FAOPS-821       Tawanda Mukhalela       Cuen Edwards            Exclude BULK_UPDATE user updates
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm

from at_logging import getLogger
import OperationsSTPParameters


LOGGER = getLogger(__name__)


def sender_modify(amba_message, subject):
    """
    Sender modify hook used to modify or suppress any outgoing (ADS
    to AMB) messages for the Operations STP AMBA.

    The hook function receives the outgoing message and message
    subject as arguments and returns a tuple with the modified
    message and subject to be sent. If None is returned, the AMBA
    will not send the message to the AMB.
    """
    try:
        if _should_suppress_outgoing_amba_message(amba_message):
            return None
        amba_message = _modify_outgoing_amba_message(amba_message)
        return amba_message, subject
    except:
        exception_message = 'Exception in sender_modify for message:\n{message}'
        LOGGER.exception(exception_message.format(
            message=amba_message.mbf_object_to_string()
        ))
        raise


def _should_suppress_outgoing_amba_message(amba_message):
    """
    Determine whether or not to suppress an outgoing AMBA message.
    """
    table_name = _get_event_table_name(amba_message)
    if not _is_stp_event_table_name(table_name):
        LOGGER.info("Message for non-STP event table '{table_name}' received - suppressing...".format(
            table_name=table_name
        ))
        return True
    if table_name == 'CONFIRMATION':
        return _should_suppress_outgoing_confirmation_message(amba_message)
    elif table_name == 'INSTRUMENT':
        return _should_suppress_outgoing_instrument_message(amba_message)
    elif table_name == 'SETTLEMENT':
        return _should_suppress_outgoing_settlement_message(amba_message)
    elif table_name == 'TRADE':
        return _should_suppress_outgoing_trade_message(amba_message)
    return False


def _modify_outgoing_amba_message(amba_message):
    """
    Perform any modifications to an outgoing AMBA message.
    """
    return amba_message


def _is_stp_event_table_name(table_name):
    """
    Determine whether or not the specified table name represents a
    subscribed STP event table.
    """
    return table_name in OperationsSTPParameters.eventTables


def _should_suppress_outgoing_confirmation_message(amba_message):
    """
    Determine whether or not to suppress an outgoing confirmation
    AMBA message.
    """
    confirmation_message = _mbf_find_single_current_list_object_by_name(amba_message, 'CONFIRMATION')
    if _is_archived_entity_message(confirmation_message):
        LOGGER.info('Message for archived confirmation received - suppressing...')
        return True
    if _is_bulk_update_user(confirmation_message):
        return True
    return False


def _should_suppress_outgoing_instrument_message(amba_message):
    """
    Determine whether or not to suppress an outgoing instrument AMBA
    message.
    """
    instrument_message = _mbf_find_single_current_list_object_by_name(amba_message, 'INSTRUMENT')
    if _is_archived_entity_message(instrument_message):
        LOGGER.info('Message for archived instrument received - suppressing...')
        return True
    if _is_generic_instrument_message(instrument_message):
        LOGGER.info('Message for generic instrument received - suppressing...')
        return True
    if _is_ignored_update_user_instrument_message(instrument_message):
        LOGGER.info('Message for ignored instrument update user received - suppressing...')
        return True
    if _is_ignored_fixing_event_message(instrument_message):
        LOGGER.info('Message for ignored fixing event received - suppressing...')
        return True
    return False


def _is_ignored_update_user_instrument_message(instrument_message):
    """
    Determine whether or not an instrument message has been generated
    due to an update by a user for which updates are ignored.

    Please note that the history behind why updates for these users
    are ignored is not known.  This exclusion has been included due
    to it currently being an exclusion in place on the confirmation
    AMBA.
    """
    update_user_message = _mbf_find_single_current_tag_object_by_name(instrument_message, 'UPDAT_USRNBR.USERID')
    update_user_name = update_user_message.mbf_get_value()
    return update_user_name in [
        'ATS_ECONTRD_AMD_PRD',
        'SDF_WRITE_PRD',
        'BULK_UPDATE'
    ]


def _is_generic_instrument_message(instrument_message):
    """
    Determine whether or not a instrument message is for a generic
    instrument.
    """
    generic_message = _mbf_find_single_current_tag_object_by_name(instrument_message, 'GENERIC')
    generic = generic_message.mbf_get_value()
    return generic == 'Yes'


def _is_ignored_fixing_event_message(instrument_message):
    """
    Determine whether or not an instrument message has been generated
    due to a rate fixing event having occurred but where the new rate
    does not differ from the previous rate.

    Please note that this logic is a refactored version based on the
    similar check performed for the confirmation AMBA.
    """
    update_user_message = _mbf_find_single_current_tag_object_by_name(instrument_message, 'UPDAT_USRNBR.USERID')
    update_user_name = update_user_message.mbf_get_value()
    if update_user_name != 'ATS_FRERATE_PRD':
        return False
    additional_info_message = _find_current_additional_info_message(instrument_message, 'CallFloatRef')
    if additional_info_message is None:
        return False
    field_value_message = _mbf_find_single_current_tag_object_by_name(additional_info_message, 'VALUE')
    field_value = field_value_message.mbf_get_value()
    rate_reference = acm.FInstrument[field_value]
    if rate_reference is None:
        return False
    currency = rate_reference.Currency()
    calendar = currency.Calendar()
    today = acm.Time.DateToday()
    previous_business_day = calendar.AdjustBankingDays(today, -1)
    current_price = rate_reference.UsedPrice(today, currency.Name(), 'SPOT_SOB')
    previous_price = rate_reference.UsedPrice(previous_business_day, currency.Name(), 'SPOT')
    return current_price == previous_price


def _should_suppress_outgoing_settlement_message(amba_message):
    """
    Determine whether or not to suppress an outgoing confirmation
    AMBA message.
    """
    settlement_message = _mbf_find_single_current_list_object_by_name(amba_message, 'SETTLEMENT')
    if _is_archived_entity_message(settlement_message):
        LOGGER.info('Message for archived settlement received - suppressing...')
        return True
    if _is_bulk_update_user(settlement_message):
        return True
    return False


def _should_suppress_outgoing_trade_message(amba_message):
    """
    Determine whether or not to suppress an outgoing trade AMBA
    message.
    """
    trade_message = _mbf_find_single_current_list_object_by_name(amba_message, 'TRADE')
    if _is_archived_entity_message(trade_message):
        LOGGER.info('Message for archived trade received - suppressing...')
        return True
    if _is_aggregated_trade_message(trade_message):
        LOGGER.info('Message for aggregated trade received - suppressing...')
        return True
    if _is_bulk_update_user(trade_message):
        return True
    return False


def _is_aggregated_trade_message(trade_message):
    """
    Determine whether or not a trade message is for an aggregated
    trade.
    """
    aggregate_message = _mbf_find_single_current_tag_object_by_name(trade_message, 'AGGREGATE')
    aggregate = aggregate_message.mbf_get_value()
    return aggregate != '0'


def _get_event_table_name(amba_message):
    """
    Get the name of the table for which an AMBA message is being sent.
    """
    message_type = amba_message.mbf_find_object('TYPE', 'MBFE_BEGINNING').mbf_get_value()
    table_name = message_type.replace('INSERT_', '').replace('UPDATE_', '').replace('DELETE_', '')
    return table_name


def _is_archived_entity_message(entity_message):
    """
    Determine whether or not an entity message is for an archived
    entity.
    """
    archive_status_message = _mbf_find_single_current_tag_object_by_name(entity_message, 'ARCHIVE_STATUS')
    archive_status = archive_status_message.mbf_get_value()
    return archive_status == '1'


def _find_current_additional_info_message(entity_message, additional_info_name):
    """
    Find any current additional info child message for the specified entity
    message and additional info name.

    If no matching additional info message is found, None is
    returned.
    """
    for additional_info_message in _mbf_find_current_list_objects_by_name(entity_message, 'ADDITIONALINFO'):
        field_name_message = _mbf_find_single_current_tag_object_by_name(additional_info_message,
            'ADDINF_SPECNBR.FIELD_NAME')
        field_name = field_name_message.mbf_get_value()
        if field_name == additional_info_name:
            return additional_info_message
    return None


def _mbf_find_current_list_objects_by_name(mbf_object, name):
    """
    Find any child list MBF objects with the specified name.
    """
    return _mbf_find_objects_by_name(mbf_object, name, ['', '+', '!'])


def _mbf_find_current_tag_objects_by_name(mbf_object, name):
    """
    Find any child tag MBF objects with the specified name.
    """
    return _mbf_find_objects_by_name(mbf_object, name, [''])


def _mbf_find_single_current_list_object_by_name(mbf_object, name):
    """
    Find a single child list MBF object with the specified nam.

    If more than one child list MBF object is found an exception will
    be raised.
    """
    return _mbf_find_single_object_by_name(mbf_object, name, ['', '+', '!', '-'])


def _mbf_find_single_current_tag_object_by_name(mbf_object, name):
    """
    Find a single child tag MBF object with the specified nam.

    If more than one child tag MBF object is found an exception will
    be raised.
    """
    return _mbf_find_single_object_by_name(mbf_object, name, [''])


def _mbf_find_objects_by_name(mbf_object, name, name_prefixes=None):
    """
    Find any child MBF objects with the specified name and optional
    prefixes.

    If no name prefixes are specified then objects matching any
    possible prefix will be returned.
    """
    if name_prefixes is None:
        name_prefixes = ['', '+', '!', '-']
    names = list()
    for name_prefix in name_prefixes:
        names.append(name_prefix + name)
    mbf_objects = list()
    child_mbf_object = mbf_object.mbf_first_object()
    while child_mbf_object is not None:
        if child_mbf_object.mbf_get_name() in names:
            mbf_objects.append(child_mbf_object)
        child_mbf_object = mbf_object.mbf_next_object()
    return mbf_objects


def _mbf_find_single_object_by_name(mbf_object, name, name_prefixes=None):
    """
    Find a single child MBF object with the specified name and
    optional prefixes.

    If more than one child MBF object is found an exception will be
    raised.
    """
    mbf_objects = _mbf_find_objects_by_name(mbf_object, name, name_prefixes)
    number_of_mbf_objects = len(mbf_objects)
    if number_of_mbf_objects == 0:
        return None
    if number_of_mbf_objects == 1:
        return mbf_objects[0]
    exception_message = "More than one object found for name '{name}' in object '{parent_name}'."
    raise ValueError(exception_message.format(
        name=name,
        parent_name=mbf_object.mbf_get_name()
    ))


def _is_bulk_update_user(message):
    """
    Checks for update user BULK_UPDATE
    """
    update_user_message = _mbf_find_single_current_tag_object_by_name(message, 'UPDAT_USRNBR.USERID')
    update_user_name = update_user_message.mbf_get_value()
    if update_user_name == 'BULK_UPDATE':
        return True
    return False
