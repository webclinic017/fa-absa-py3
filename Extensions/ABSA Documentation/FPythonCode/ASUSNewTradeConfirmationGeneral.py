"""------------------------------------------------------------------------------------------------------------------
MODULE
    ASUSNewTradeConfirmationGeneral

DESCRIPTION
    All general functions for the ASUS Business.

---------------------------------------------------------------------------------------------------------------------
HISTORY
=====================================================================================================================
Date            Change no       Developer               Requester               Description
---------------------------------------------------------------------------------------------------------------------
2020-02-17      FAOPS-708       Tawanda Mukhalela       Ndivhuwo Mashishimise   ASUS New Trade Confirmations
2020-04-29      FAOPS-748       Tawanda Mukhalela       Ndivhuwo Mashishimise   ASUS DMA New Trade Confirmations
2021-02-24      FAOPS-1088      Metse Moshobane         Ndivhuho Mashishimise   Added a restriction to the code (line 446)
---------------------------------------------------------------------------------------------------------------------
"""

from datetime import datetime

import acm

import DocumentGeneral
from at_logging import getLogger
from FDocumentationCompression import ZlibToXml, HexToZlib


LOGGER = getLogger(__name__)


def get_asus_event_name():
    """
    Returns the ASUS New Trade event name
    """
    return '10B10 Confirmation'


def get_asus_template_name():
    """
    Returns the ASUS New Trade event name
    """
    return 'ABSA_10B10_New_Trade_Confirmation'


def is_valid_asus_bond_trade(trade):
    """
    Validates the trade against asus rules.
    """
    instrument_type = trade.Instrument().InsType()
    if instrument_type != 'Bond':
        return False
    if not trade.Counterparty().LegalForm():
        return False
    if trade.Counterparty().LegalForm().Name() != '15a6 US client':
        return False
    if trade.OptKey1AsEnum() != 'Block Trade':
        return False
    if trade.Type() != 'Normal':
        return False
    if not evaluate_conf_instruction_and_rule_setup(trade.Counterparty(), instrument_type):
        return False
    if trade.Instrument().AdditionalInfo().Demat_Instrument():
        return False

    return True


def format_string_to_asus_format(date_string, date_format='%m/%d/%Y'):
    """
    Formats a date string to the date format needed by ASUS.
    """
    date = datetime(*acm.Time.DateToYMD(date_string)).strftime(date_format)

    return date


def get_current_usd_pot_price(usd_currency_instrument, local_currency_instrument,
                              date=acm.Time.DateToday(), market='SPOT'):
    """
    Calculate the current Spot Price
    """
    calculation_space = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()
    parameter_dict = acm.FDictionary()
    parameter_dict['priceDate'] = date
    if local_currency_instrument:
        parameter_dict['currency'] = local_currency_instrument
    if market:
        parameter_dict['marketPlace'] = market
        parameter_dict['useSpecificMarketPlace'] = True
    spot_price = usd_currency_instrument.Calculation().MarketPriceParams(calculation_space, parameter_dict)
    if not spot_price:
        raise ValueError('Spot price for USD not Defined Yet!, Failed to convert Local Currency to USD')

    return spot_price.Value().Number()


def evaluate_conf_instruction_and_rule_setup(counterparty, instype):
    for conf_instruction in counterparty.ConfInstructions():
        if conf_instruction.EventChlItem() is None:
            continue
        if conf_instruction.EventChlItem().Name() != get_asus_event_name():
            continue
        if conf_instruction.InsType() != instype:
            continue
        if not evaluate_conf_instruction_rule(conf_instruction):
            continue
        return True

    return False


def evaluate_conf_instruction_rule(conf_instruction):
    """
    Evaluates if rules are valid
    """
    for rule in conf_instruction.ConfInstructionRules():
        if rule.TemplateChoiceList() is None:
            continue
        if rule.TemplateChoiceList().Name() == get_asus_template_name():
            return True

    return False


def formated_display_value(currency, partten, value):
    """
    Formats and returns the value for display Purposes
    """
    display_value = currency + ' ' + partten.format(abs(value))

    return display_value


def get_last_released_xml(confirmation):
    """
    Get the xml from the last post-released confirmation.

    This function should only be called when a confirmation has
    been released.
    """
    previous_confirmation = confirmation.ConfirmationReference()
    if previous_confirmation.IsPostRelease():
        operations_document = previous_confirmation.Documents()[0]
        return ZlibToXml(HexToZlib(operations_document.Data()))
    else:
        return get_last_released_xml(previous_confirmation)


def is_void_and_has_allocations(trade):
    """
    Checks If there are allocations available
    """
    if not trade.TrxTrades():
        return False
    if not _validate_allocations(trade.TrxTrades()):
        return False

    return True


def _validate_allocations(trades):
    """
    Determines is allocations on a block are still valid.
    """
    voided_trades = 0
    for trx_trade in trades:
        if trx_trade.Status() == 'Void':
            voided_trades += 1
    if len(trades) == voided_trades:
        return False

    return True


def get_commission_amount(block_trade):
    """
    Calculates commision amount for an equity block trade.
    Amount is derived from adding all fees on allocations
    """
    if block_trade.Portfolio().Name() == 'DMA':
        payments = block_trade.Payments()
        return _get_allocation_payment_amount(payments)

    if _is_part_of_combination(block_trade):
        commission = _process_split_block_trade(block_trade)
        return commission

    allocations = block_trade.TrxTrades()
    commission = 0
    for allocation in allocations:
        if _is_valid_xtp_broker_note(allocation):
            payments = allocation.Payments()
            payments_total_amount = _get_allocation_payment_amount(payments)
            commission += payments_total_amount

    return commission


def _get_allocation_payment_amount(payments):
    """
    adds payment amounts for an allocation
    """
    payments_total_amount = 0
    for payment in payments:
        payments_total_amount += payment.Amount()

    return payments_total_amount


def get_counterparty_contact(block_trade):
    """
    Returns applicable contact for the counterparty
    """
    counterparty = get_counterparty_for_trade(block_trade)
    instrument_type = block_trade.Instrument().InsType()

    return _get_contact_for_party(counterparty, instrument_type)


def get_counterparty_for_trade(block_trade):
    """
    Returns the Portfolio counterparty from the block trade
    """
    if _get_single_block_counterparty(block_trade):
        return _get_single_block_counterparty(block_trade)
    elif _get_combination_block_trades_counterpaty(block_trade):
        return _get_combination_block_trades_counterpaty(block_trade)
    else:
        return block_trade.Counterparty()


def _get_single_block_counterparty(block_trade):
    """
    Gets allocation counterparty for one to one matches
    """
    allocations = block_trade.TrxTrades().AsArray()
    for allocation in allocations:
        if not _is_valid_xtp_broker_note(allocation):
            continue
        return allocation.Counterparty()

    return None


def _get_combination_block_trades_counterpaty(block_trade):
    """
    Gets the related allocation counterparty from related trades
    """
    party_related_trades = block_trade.Portfolio().Trades().AsArray().SortByProperty('TradeTime',
                                                                                     ascending=False)
    for linked_trade in party_related_trades:
        if not _is_valid_xtp_broker_note(linked_trade):
            continue
        return linked_trade.Counterparty()

    return None


def _is_valid_xtp_broker_note(trade):
    """
    Checks if trade is a valid XTP broker note trade
    """
    if trade.AdditionalInfo().XtpTradeType() != 'OBP_BROKER_NOTE':
        return False

    if not trade.Counterparty().LegalForm():
        return False
    legal_form = trade.Counterparty().LegalForm().Name()
    if legal_form != '15a6 US client':
        return False

    return True


def _get_contact_for_party(counterparty, instrument_type):
    """
    Gets applicable contact for the given party and asus event
    """
    for contact in counterparty.Contacts():
        if not _evaluate_contact_rules(contact, instrument_type):
            continue
        return contact

    raise ValueError('No Contact Rules setup on party : {party}'.format(party=counterparty.Name()))


def _evaluate_contact_rules(contact, instrument_type):
    """
    Evaluates contact rules
    """
    for contact_rule in contact.ContactRules().AsArray():
        if contact_rule.EventChlItem() is None:
            continue
        if contact_rule.EventChlItem().Name() != get_asus_event_name():
            continue
        if contact_rule.InsType() != instrument_type:
            continue

        return True

    return False


def has_valid_10b10_confirmation_already_created(trade):
    for confirmation in trade.Confirmations():
        if confirmation.EventChlItem().Name() == get_asus_event_name():
            return True

    return False


def get_unmatched_block_trades(block_trades):
    """
    Groups all unmatched blocks based on a Composite key (Portfolio, Price)
    """
    unallocated_blocks_dict = dict()
    for block_trade in block_trades:
        portfolio = block_trade.Portfolio().Name()
        price = block_trade.Price()
        if not list(unallocated_blocks_dict.keys()):
            unallocated_blocks_dict[(portfolio, price)] = [block_trade]
        elif (portfolio, price) in list(unallocated_blocks_dict.keys()):
            current_trades_in_list = unallocated_blocks_dict[(portfolio, price)]
            trade_list = [block_trade]
            for trade in current_trades_in_list:
                if trade.Portfolio().Name() != portfolio:
                    continue
                if round(trade.Price(), 2) != round(price, 2):
                    continue
                trade_list.append(trade)
                unallocated_blocks_dict[(portfolio, price)] = trade_list
        else:
            unallocated_blocks_dict[(portfolio, price)] = [block_trade]

    return unallocated_blocks_dict


def get_unprocessed_blocks():
    """
    Gets all blocks that have not been allocated/processed
    """
    trades = get_all_block_trades()
    unprocessed_blocks = list()
    for block_trade in trades:
        if has_been_processed(block_trade):
            continue
        unprocessed_blocks.append(block_trade)

    return unprocessed_blocks


def get_all_block_trades(block_trade=None):
    """
    All applicable Block Trades
    """
    today = acm.Time.DateToday()
    booking_date = acm.Time.DateAddDelta(today, 0, 0, -10)
    asql_query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
    instrument_type_node = asql_query.AddOpNode('OR')
    for instype in ['Stock', 'ETF']:
        instrument_type_node.AddAttrNode('Instrument.InsType', 'EQUAL', instype)

    asql_query.AddAttrNode('TradeTime', 'GREATER_EQUAL', booking_date)
    asql_query.AddAttrNode('TradeTime', 'LESS', today)
    asql_query.AddAttrNode('Status', 'EQUAL', 'BO Confirmed')
    asql_query.AddAttrNode('AdditionalInfo.XtpTradeType', 'EQUAL', 'OBP_BLOCK_TRADE')
    asql_query.AddAttrNode('Trader.Name', 'EQUAL', 'OBP_USER_PRD')
    if block_trade is not None:
        asql_query.AddAttrNode('Portfolio.Name', 'EQUAL', block_trade.Portfolio().Name())
        asql_query.AddAttrNode('Instrument.Name', 'EQUAL', block_trade.Instrument().Name())
    return asql_query.Select()


def get_all_applicable_allocations():
    """
    Gets all applicable allocations
    """
    today = acm.Time.DateToday()
    booking_date = acm.Time.DateAddDelta(today, 0, 0, -10)
    asql_query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
    asql_query.AddAttrNode('TradeTime', 'GREATER_EQUAL', booking_date)
    instrument_type_node = asql_query.AddOpNode('OR')
    for instype in ['Stock', 'ETF']:
        instrument_type_node.AddAttrNode('Instrument.InsType', 'EQUAL', instype)

    asql_query.AddAttrNode('Status', 'EQUAL', 'BO Confirmed')
    asql_query.AddAttrNode('Counterparty.LegalForm.Name', 'EQUAL', '15a6 US client')
    asql_query.AddAttrNode('AdditionalInfo.XtpTradeType', 'EQUAL', 'OBP_BROKER_NOTE')
    asql_query.AddAttrNode('Trader.Name', 'EQUAL', 'OBP_USER_PRD')

    return asql_query.Select()


def get_unprocessed_allocations():
    """
    Gets all allocations that have not been allocated/processed
    """
    unprocessed_allocations = list()
    allocations = get_all_applicable_allocations()
    for allocation in allocations:
        if allocation.TrxTrade():
            continue
        unprocessed_allocations.append(allocation)

    return unprocessed_allocations


def has_been_processed(block_trade):
    """
    Checks if the block has already beeb processed
    """
    if has_valid_10b10_confirmation_already_created(block_trade):
        return True
    if block_trade.TrxTrades():
        for allocation in block_trade.TrxTrades():
            if _is_valid_xtp_broker_note(allocation):
                return True

    return False


def get_allocations_and_blocks_to_process(unallocated_blocks_dict):
    """
    Gets a pair of unprocessed Blocks and theirs respective allocations
    """
    allocations = get_unprocessed_allocations()
    unprocessed_trades_dict = dict()

    for portfolio_price_pair, trades_list in list(unallocated_blocks_dict.items()):
        portfolio = portfolio_price_pair[0]
        price = portfolio_price_pair[1]
        matching_allocations = list()
        total_block_quantity = 0
        total_allocation_quantity = 0
        for allocation in allocations:
            if round(allocation.Price(), 2) != round(price, 2):
                continue
            if allocation.Portfolio().Name() != portfolio:
                continue
            if allocation.Instrument().Name() != trades_list[0].Instrument().Name():
                continue
            matching_allocations.append(allocation)
            total_allocation_quantity += allocation.Quantity()

        for xtp_block_trade in trades_list:
            total_block_quantity += xtp_block_trade.Quantity()

        if not (DocumentGeneral.is_almost_zero(total_allocation_quantity) and DocumentGeneral.is_almost_zero(total_block_quantity)):
            diff_between_total_allocation_quantity_and_total_block_quantity = (abs(total_allocation_quantity) - abs(total_block_quantity))
            if DocumentGeneral.is_almost_zero(diff_between_total_allocation_quantity_and_total_block_quantity):
                message = 'Found {0} Matching Allocations for trades {1} {2}'
                LOGGER.info(message.format(len(matching_allocations), trades_list[0].Oid(), trades_list[1].Oid()))
                unprocessed_trades_dict[tuple(trades_list)] = matching_allocations

    return unprocessed_trades_dict


def _is_part_of_combination(block_trade):
    """
    this is to determine if the block quantity is split accross 2 trades,
    or the Bond trade does not have allocation equating to its quantity
    """
    if not block_trade.TrxTrades():
        return True
    if _check_quantity_equality(block_trade):
        return True

    return False


def _check_quantity_equality(block_trade):
    """
    Checks if block quantity equates to the allocations' quantity
    """
    quantity = 0
    for allocation in block_trade.TrxTrades():
        if _is_valid_xtp_broker_note(allocation):
            quantity += allocation.Quantity()

    return abs(quantity) != abs(block_trade.Quantity())


def _process_split_block_trade(block_trade):
    """
    Gets commission of the Block Trade
    """
    block_trades = get_all_block_trades(block_trade)
    allocations_quantity = 0
    block_trades_quantity = 0
    payments_total = 0
    for trade in block_trades:
        if round(trade.Price(), 2) != round(block_trade.Price(), 2):
            continue
        if _has_past_confirmation(trade):
            continue
        block_trades_quantity += trade.Quantity()
        if not trade.TrxTrades():
            continue
        for allocation in trade.TrxTrades():
            if _is_valid_xtp_broker_note(allocation):
                allocations_quantity += allocation.Quantity()
                payments_total += _get_allocation_payment_amount(allocation.Payments())

    apportioned_fees = (block_trade.Quantity()/block_trades_quantity) * payments_total
    if abs(block_trades_quantity) != abs(allocations_quantity):
        raise ValueError('Could not match block trade quantities to allocations, failed to calculate fees!')

    return apportioned_fees


def _has_past_confirmation(trade):
    for confirmation in trade.Confirmations():
        if confirmation.EventChlItem().Name() == get_asus_event_name():
            if acm.Time.DateFromTime(confirmation.CreateTime()) != acm.Time.DateToday():
                return True

    return False
