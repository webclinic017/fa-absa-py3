"""
This module is used to do the processing for incoming messages related to the security settlement messages (540-543).

History
=======
2018-05-11      CHG1000406751   Willie vd Bank          Initial deployment
2019-06-20      FAOPS-504
                FAOPS-508       Joash Moodley           Added code to handle MT544/5/6/7/8
2020-07-02      FAOPS-858       Tawanda Mukhalela       Refactored code to improve performance
"""

import re

import acm
import at_logging
import FSettlementActions

from gen_swift_functions import get_text_from_tag, get_trans_ref_from_tag

LOGGER = at_logging.getLogger(__name__)


def get_tag_and_split(field, mtmessage, split_by=None):
    ref = get_text_from_tag(field, mtmessage)
    if ref and split_by and split_by in ref:
        ref = ref.split(split_by)
        return ref[1]
    else:
        return ref


def change_settlement_status(settlement, status):
    """
    Update Settlement Status
    """
    settlement.Status(status)
    settlement.Commit()
    message = 'Settlement {settlement} status moved to {status}'
    LOGGER.info(message.format(settlement=settlement.Oid(), status=status))


def change_settlement_text(settlement, text_ref):
    """
    Update settlement text
    """
    settlement.Text(text_ref)
    settlement.Commit()
    LOGGER.info('Settlement {settlement} text updated'.format(settlement=settlement.Oid()))


def find_settlement_top_parent(settlement):
    top_settlement = settlement
    while top_settlement.Parent():
        top_settlement = find_settlement_top_parent(top_settlement.Parent())
    return top_settlement


def update_540s_status_for_NEWCAN(mtmessage, settlement):
    """
    Update security settlement status and Text
    """
    message_type = get_tag_and_split(':23G:', mtmessage)
    message = '{message_type} received for settlement {oid}.'
    LOGGER.info(message.format(message_type=message_type, oid=str(settlement.Oid())))
    if message_type == 'NEWM':
        status_ref = 'Settled'
        change_settlement_text(settlement, status_ref)
        status = 'Settled'
        change_settlement_status(settlement, status)
    else:
        error_message = 'Error processing security settlement: unknown type {message_type} received.'
        LOGGER.warning(error_message.format(message_type=message_type))


def update_540s_status_for_548(mtmessage, settlement, has_exchange_ref=False):
    """
    Update security settlement status and Text
    """
    part = get_tag_and_split(':25D::', mtmessage)
    if part:
        if 'CPRC' in part:      # Cancellations
            top_parent_settlement = _get_top_parent_for_settlement(settlement)
            if part == 'CPRC//CAND' and not has_exchange_ref:
                change_settlement_text(top_parent_settlement, part)  # Has to be done before the Close update otherwise no further updates are possible
                change_settlement_status(top_parent_settlement, 'Pending Closure')
                change_settlement_status(top_parent_settlement, 'Closed')
                return

            elif part == 'CPRC//CAND' and has_exchange_ref:
                settlement = cancell_settlement(top_parent_settlement)
                return change_settlement_text(settlement, part)

            elif part == 'CPRC//DEND':
                return change_settlement_text(top_parent_settlement, part)

            elif part == 'CPRC//REJT':
                return change_settlement_text(top_parent_settlement, part)

        elif 'SETT//PENF' in part:
            field_24b = get_tag_and_split(':24B::', mtmessage)
            if field_24b == 'PENF//ADEA':
                settlement = _get_top_parent_for_settlement(settlement)
            return change_settlement_text(settlement, 'SETT//PENF')

        else:
            status_ref = get_tag_and_split(':25D::', mtmessage, '//')
            part = get_tag_and_split(':24B::', mtmessage, '//')
            if part:
                status_ref += '//' + part
                if 'NARR' == part:
                    part = get_tag_and_split(':70D::', mtmessage, '//')
                    if part:
                        status_ref += ' ' + part

            return change_settlement_text(settlement, status_ref)


def _get_top_parent_for_settlement(settlement):
    """
    Gets the top parent settlement for a given settlement hierarchy
    """
    if settlement.Trade() and settlement.Trade().Status() == 'Void':
        settlement = find_settlement_top_parent(settlement)

    return settlement


def process_incoming(mtmessage, msg_type):
    msg_ref = get_tag_and_split(':20C::RELA', mtmessage, '-')
    exchange_ref = get_trans_ref_from_tag(':20C::RELA//', mtmessage)

    if re.search(r"^[0-9]{10}$", exchange_ref[0]):
        process_incoming_exchange_ref(mtmessage, msg_type)

    elif msg_ref:
        settlement = acm.FSettlement[msg_ref]
        if settlement and '54' in settlement.MTMessages():
            _update_security_settlement(msg_type, mtmessage, settlement)
        else:
            LOGGER.warning('Settlement with reference id {id} not found on Front Arena!'.format(id=msg_ref))

    else:
        LOGGER.warning('Matching reference {ref} not found for incoming security message!'.format(ref=msg_ref))


def process_incoming_exchange_ref(mtmessage, msg_type):

    related_reference = get_trans_ref_from_tag(':20C::RELA//', mtmessage)

    if related_reference:
        related_reference = related_reference[0][1:] + '/NUTRON'
    else:
        LOGGER.warning('Could not find any Related Reference.. skipping processing')
        return

    trades = find_all_trades_for_exchange_ref(related_reference)
    for trade in trades:
        for settlement in trade.Settlements().AsArray():
            if settlement.Type() not in ("Security Nominal", "End Security"):
                continue
            _update_security_settlement(msg_type, mtmessage, settlement, has_exchange_ref=True)


def _update_security_settlement(msg_type, mtmessage, settlement, has_exchange_ref=False):
    """
    Updates the settlement
    """
    if msg_type in ('544', '545', '546', '547'):
        update_540s_status_for_NEWCAN(mtmessage, settlement)
    elif msg_type == '548':
        update_540s_status_for_548(mtmessage, settlement, has_exchange_ref)


def cancell_settlement(settlement):
    trade_settlements = settlement.Trade().Settlements().AsArray()
    has_cancelled = False
    for trade_settlement in trade_settlements:
        if trade_settlement.Type() == settlement.Type() and trade_settlement.Status() == 'Cancelled':
            has_cancelled = True
            break

    if not has_cancelled:
        old_settlement, new_settlement, = FSettlementActions.InstructToCancel(settlement)
        parent = new_settlement[0]
        parent.Status('Cancelled')
        parent.Commit()
        old_settlement[0].Parent(parent)
        old_settlement[0].Commit()
        old_settlement[0].Status('Void')
        old_settlement[0].Commit()
        return parent
    return settlement


def find_trades_by_exchange_ref(exchange_ref):
    """
    Finds Trades based on Exchange ref 1 or 2 matching the Related Reference
    """

    exchange_ref1_spec = retrieve_additional_info_spec_by_name('ExchangeRef1')
    exchange_ref2_spec = retrieve_additional_info_spec_by_name('ExchangeRef2')
    additional_infos_ref1 = find_additional_infos_by_spec_and_field_value(exchange_ref1_spec, exchange_ref)
    additional_infos_ref2 = find_additional_infos_by_spec_and_field_value(exchange_ref2_spec, exchange_ref)
    trades = set()
    trades.update(_get_trades_from_add_info(additional_infos_ref1))
    trades.update(_get_trades_from_add_info(additional_infos_ref2))

    return trades


def _get_trades_from_add_info(additional_infos):
    """
    Gets all trades related to a particular list of additional infos
    """
    trades = [additional_info.Parent() for additional_info in additional_infos]
    return trades


def find_additional_infos_by_spec_and_field_value(additional_info_spec, field_value):
    """
    Gets all applicable Additional infos with the Value of the related Reference
    """
    return acm.FAdditionalInfo.Select("addInf = {additional_info_spec_oid} and fieldValue = '{field_value}'".format(
        additional_info_spec_oid=additional_info_spec.Oid(),
        field_value=field_value
    )).AsArray()


def retrieve_additional_info_spec_by_name(name):
    """
    Gets additional info spec by name
    """
    additional_info_spec = acm.FAdditionalInfoSpec[name]
    if additional_info_spec is None:
        raise ValueError("An additional info spec with the name '{name}' does not exist.".format(
            name=name
        ))
    return additional_info_spec


def find_all_trades_for_exchange_ref(exchange_ref):
    """
    Finds all trades related to the Exchange Ref
    """
    trades = find_trades_by_exchange_ref(exchange_ref)
    number_of_trades = len(trades)
    if number_of_trades > 0:
        trade_numbers = ", ".join([str(trade.Oid()) for trade in trades])
        LOGGER.info("Trades {trade_numbers} found for Exchange Ref '{exchange_ref}'".format(
            trade_numbers=trade_numbers,
            exchange_ref=exchange_ref
        ))
    else:
        LOGGER.info("No trades found for Exchange Ref '{exchange_ref}'".format(
            exchange_ref=exchange_ref
        ))

    return trades
