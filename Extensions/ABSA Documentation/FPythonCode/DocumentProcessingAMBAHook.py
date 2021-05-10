"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    DocumentProcessingAMBAHook
    
DESCRIPTION
    This module contains an AMBA hook used for filtering out

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-10-14      FAOPS-531       Cuen Edwards            Letitia Carboni         Initial Implementation.
2020-01-31      FAOPS-557       Tawanda Mukhalela       Khaya Mbebe             Added Support Security Loan Instrument
-----------------------------------------------------------------------------------------------------------------------------------------
"""
from at_logging import getLogger
import DocumentProcessingParameters


LOGGER = getLogger(__name__)


def sender_modify(message, subject):
    """
    AEL sender_modify hook used for filtering out-going (ADS to AMB)
    document processing AMBA messages.

    This hook is called when a change occurs in the ADS and an out-going
    message will be generated and sent to the AMB.  The hook is called
    before the message is sent, allowing one the opportunity to modify
    or suppress the message before sending.
    """
    event_type_message = message.mbf_find_object('TYPE', 'MBFE_BEGINNING')
    event_type = event_type_message.mbf_get_value()
    txnbr_message = message.mbf_find_object('TXNBR', 'MBFE_BEGINNING')
    txnbr = txnbr_message.mbf_get_value()
    if _matches_inclusion_criteria(message):
        LOGGER.info("'{event_type}' message with txnbr {txnbr} matches inclusion criteria - sending...".format(
            event_type=event_type,
            txnbr=txnbr
        ))
        return message, subject
    LOGGER.info("'{event_type}' message with txnbr {txnbr} does not match inclusion criteria - suppressing...".format(
        event_type=event_type,
        txnbr=txnbr
    ))
    return None


def _matches_inclusion_criteria(message):
    """
    Determine whether or not a message matches the inclusion criteria
    for the document processing AMBA.

    Any messages that do match the inclusion criteria are suppressed.
    """
    if _matches_business_process_inclusion_criteria(message):
        return True
    if _matches_instrument_inclusion_criteria(message):
        return True
    if _matches_trade_inclusion_criteria(message):
        return True
    if _matches_party_inclusion_criteria(message):
        return True
    if _matches_block_trade_void_criteria(message):
        return True
    return False


def _matches_business_process_inclusion_criteria(message):
    """
    Determine whether or not a message matches the inclusion criteria
    for document business processes.
    """
    # Is included event type.
    event_type_message = message.mbf_find_object('TYPE', 'MBFE_BEGINNING')
    if not _is_included_business_process_event_type(event_type_message):
        return False
    # Is included state chart.
    business_process_message = _find_first_mbf_child_object(message, 'BUSINESSPROCESS')
    state_chart_name_message = _find_first_mbf_child_object(business_process_message, 'STATE_CHART_SEQNBR.NAME')
    if not _is_included_state_chart_name(state_chart_name_message):
        return False
    # Is included archive status.
    archive_status_message = _find_first_mbf_child_object(business_process_message, 'ARCHIVE_STATUS')
    if not _is_included_archive_status(archive_status_message):
        return False
    return True


def _matches_instrument_inclusion_criteria(message):
    """
    Determine whether or not a message matches the inclusion criteria
    for instruments that relate to document processing.
    """
    # Is included event type.
    event_type_message = message.mbf_find_object('TYPE', 'MBFE_BEGINNING')
    if not _is_included_instrument_event_type(event_type_message):
        return False
    # Is included instrument type.
    instrument_message = _find_first_mbf_child_object(message, 'INSTRUMENT')
    instype_message = _find_first_mbf_child_object(instrument_message, 'INSTYPE')
    if not _is_included_instype(instype_message):
        return False
    # Is generic instrument.
    generic_message = _find_first_mbf_child_object(instrument_message, 'GENERIC')
    if not _is_included_non_generic_instrument(generic_message):
        return False
    # Is included archive status.
    archive_status_message = _find_first_mbf_child_object(instrument_message, 'ARCHIVE_STATUS')
    if not _is_included_archive_status(archive_status_message):
        return False
    return True


def _matches_block_trade_void_criteria(message):
    """
    determine whether an update is a block trade update.
    """
    event_type_message = message.mbf_find_object('TYPE', 'MBFE_BEGINNING')
    if not _is_included_trade_event_type(event_type_message):
        return False
    trade_message = _find_first_mbf_child_object(message, 'TRADE')
    instype_message = _find_first_mbf_child_object(trade_message, 'INSADDR.INSTYPE')
    instype = instype_message.mbf_get_value()
    trade_status_message = _find_first_mbf_child_object(trade_message, 'STATUS')
    status = trade_status_message.mbf_get_value()
    
    if instype not in ['Bond', 'FRN', 'IndexLinkedBond']:
        return False

    if status not in ['Void', 'FO Confirmed']:
        return False
    
    return True


def _matches_trade_inclusion_criteria(message):
    """
    Determine whether or not a message matches the inclusion criteria
    for trades that relate to document processing.
    """
    # Is included event type.
    event_type_message = message.mbf_find_object('TYPE', 'MBFE_BEGINNING')
    if not _is_included_trade_event_type(event_type_message):
        return False
    # Is included instrument type.
    trade_message = _find_first_mbf_child_object(message, 'TRADE')
    instype_message = _find_first_mbf_child_object(trade_message, 'INSADDR.INSTYPE')
    if not _is_included_instype(instype_message):
        return False
    # Is included trade type.
    trade_type_message = _find_first_mbf_child_object(trade_message, 'TYPE')
    if not _is_included_trade_type(trade_type_message):
        return False
    # Is included archive status.
    archive_status_message = _find_first_mbf_child_object(trade_message, 'ARCHIVE_STATUS')
    if not _is_included_archive_status(archive_status_message):
        return False
    return True


def _matches_party_inclusion_criteria(message):
    """
    Determine whether or not a message matches the inclusion criteria
    for parties that relate to document processing.
    """
    # Is included event type.
    event_type_message = message.mbf_find_object('TYPE', 'MBFE_BEGINNING')
    if not _is_included_party_event_type(event_type_message):
        return False
    # Is included party type.
    party_message = _find_first_mbf_child_object(message, 'PARTY')
    party_type_message = _find_first_mbf_child_object(party_message, 'TYPE')
    if not _is_included_party_type(party_type_message):
        return False
    # Is included archive status.
    archive_status_message = _find_first_mbf_child_object(party_message, 'ARCHIVE_STATUS')
    if not _is_included_archive_status(archive_status_message):
        return False
    return True


def _is_included_business_process_event_type(event_type_message):
    """
    Determine whether or not an event type message relates to an
    included operation on a business process.
    """
    event_type = event_type_message.mbf_get_value()
    return event_type in ['INSERT_BUSINESSPROCESS', 'UPDATE_BUSINESSPROCESS']


def _is_included_state_chart_name(state_chart_name_message):
    """
    Determine whether or not a state chart message is for a document
    business process.
    """
    state_chart_name = state_chart_name_message.mbf_get_value()
    return state_chart_name in DocumentProcessingParameters.state_chart_names


def _is_included_instrument_event_type(event_type_message):
    """
    Determine whether or not an event type message relates to an
    included operation on an instrument.
    """
    event_type = event_type_message.mbf_get_value()
    return event_type in ['INSERT_INSTRUMENT', 'UPDATE_INSTRUMENT']


def _is_included_instype(instype_message):
    """
    Determine whether or not an instrument type message is for an
    included instrument type related to document processing.
    """
    instype = instype_message.mbf_get_value()
    return instype in ['Swap', 'SecurityLoan']


def _is_included_non_generic_instrument(generic_message):
    """
    Determine whether or not a generic message is for a non-generic
    instrument.
    """
    generic = generic_message.mbf_get_value()
    return generic != 'Yes'


def _is_included_archive_status(archive_status_message):
    """
    Determine whether or not a archive message is for a non-archived
    entity.
    """
    archive_status = archive_status_message.mbf_get_value()
    return archive_status == '0'


def _is_included_trade_event_type(event_type_message):
    """
    Determine whether or not an event type message relates to an
    included operation on a trade.
    """
    event_type = event_type_message.mbf_get_value()
    return event_type in ['INSERT_TRADE', 'UPDATE_TRADE']


def _is_included_trade_type(trade_type_message):
    """
    Determine whether or not an trade type message is for an included
    trade type related to document processing.
    """
    trade_type = trade_type_message.mbf_get_value()
    return trade_type not in [
        'Rollout',
        'Aggregate',
        'Static Aggregate',
        'FX Aggregate'
    ]


def _is_included_party_event_type(event_type_message):
    """
    Determine whether or not an event type message relates to an
    included operation on a party.
    """
    event_type = event_type_message.mbf_get_value()
    return event_type in ['INSERT_PARTY', 'UPDATE_PARTY']


def _is_included_party_type(party_type_message):
    """
    Determine whether or not an party type message is for an included
    party type related to document processing.
    """
    party_type = party_type_message.mbf_get_value()
    return party_type not in [
        'Market',
        'MtM Market',
        'Depot',
        'Clearing House',
        'Middleware',
        'Repository',
        'Venue'
    ]


def _find_first_mbf_child_object(parent_mbf_object, name, name_prefixes=None):
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
