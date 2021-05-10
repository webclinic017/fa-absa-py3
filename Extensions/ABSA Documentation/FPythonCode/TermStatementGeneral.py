"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    TermStatementGeneral

DESCRIPTION
    This module contains general functionality related to term deposit statements.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2018-05-15      FAOPS-127       Cuen Edwards            Elaine Visagie          Initial Implementation.
2018-08-01                      Cuen Edwards                                    Refactored to use some functionality from DocumentGeneral.
2018-09-21                      Cuen Edwards                                    Refactored to be consistent with scheduled call statement
                                                                                generation.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm

import DocumentConfirmationGeneral
import StatementGeneral


def get_statement_event_name():
    """
    Get the name of the event to associate with term deposit
    statement confirmations.
    """
    return 'Term Statement'


def get_statement_template_name():
    """
    Get the name of the template to associate with term deposit
    statement confirmations.
    """
    return 'ABSA_Term_Statement'


def get_statement_frequency_choice_list_name():
    """
    Get the name of the choice list used for storing term deposit
    statement frequency choices.
    """
    return 'Comm Freq Term'


def get_monthly_statement_frequency_value():
    """
    Get the value used to indicate that monthly term deposit
    statements should be received.
    """
    return 'Monthly'


def get_statement_frequency_add_info_name():
    """
    Get the name of the additional info field used for storing a
    party's term deposit statement frequency choice.
    """
    return 'Comm Freq Term'


def statement_confirmation_exists(acquirer, counterparty, from_date, to_date,
        document_schedule=None):
    """
    Determine if a term deposit statement confirmation exists for
    the specified acquirer, counterparty, inclusive statement from
    date, inclusive statement to date and optional document
    communication frequency schedule.
    """
    return StatementGeneral.statement_confirmation_exists(get_statement_event_name(),
        acquirer, counterparty, from_date, to_date, document_schedule)


def get_existing_statement_confirmations(acquirer, counterparty, from_date, to_date,
        document_schedule=None):
    """
    Get any existing term statement confirmations for the specified
    acquirer, counterparty, inclusive statement from date, inclusive
    statement to date and optional document communication frequency
    schedule.
    """
    return DocumentConfirmationGeneral.get_existing_document_confirmations(get_statement_event_name(),
        acquirer, counterparty, from_date, to_date, document_schedule)


def create_statement_confirmation(confirmation_owner_trade, from_date, to_date,
        document_schedule):
    """
    Create a term deposit statement confirmation for the specified 
    confirmation owner trade, inclusive statement from date, inclusive
    statement to date and document communication frequency schedule.
    """
    DocumentConfirmationGeneral.create_document_confirmation(get_statement_event_name(),
        confirmation_owner_trade, None, from_date, to_date, document_schedule)


def get_statement_trades(acquirer, counterparty, from_date, to_date):
    """
    Get the trades that should appear on a term deposit statement for
    the specified acquirer, counterparty, inclusive statement from 
    date and inclusive statement to date.
    """
    trades = list()
    for trade in _get_active_trades_for_party(acquirer, counterparty, from_date, to_date):
        if not _trade_has_interest_money_flows_between_dates(trade, from_date, to_date):
            continue
        trades.append(trade)
    return trades


def is_eligible_for_statement(trade):
    """
    Determine whether or not a specified trade is eligible for
    inclusion on a term deposit statement.
    """
    return _get_base_trade_asql_query().IsSatisfiedBy(trade)


def get_interest_money_flows_between_dates(trade, from_date, to_date):
    """
    Get any interest money flows for a trade that fall between an
    inclusive from date and inclusive to date.
    """
    interest_money_flows = list()
    for money_flow in _get_interest_money_flows(trade):
        if money_flow.StartDate() > to_date:
            continue
        if money_flow.EndDate() < from_date:
            continue
        interest_money_flows.append(money_flow)
    return interest_money_flows


def find_parties_receiving_scheduled_statements_for_acquirer_and_frequency(
        acquirer, statement_frequency):
    """
    Find all parties configured to receive scheduled term deposit
    statements for the specified acquirer and statement frequency.
    """
    counterparties = set()
    select_expression = "eventChlItem = '{event_name}'".format(
        event_name=get_statement_event_name()
    )
    confirmation_instructions = acm.FConfInstruction.Select(select_expression).AsArray()
    for confirmation_instruction in confirmation_instructions:
        if not confirmation_instruction.Active():
            continue
        if confirmation_instruction.InternalDepartment() != acquirer:
            continue
        counterparty = confirmation_instruction.Counterparty()
        counterparty_statement_frequency = counterparty.AddInfoValue(get_statement_frequency_add_info_name())
        if counterparty_statement_frequency in [None, 'None']:
            continue
        if counterparty_statement_frequency == 'All' or statement_frequency in counterparty_statement_frequency:
            counterparties.add(counterparty)
    return counterparties


def find_parties_with_statement_confirmation_instructions():
    """
    Find all parties with a term deposit statement confirmation 
    instruction.

    This parties may not necessarily be configured to receive
    automatically generated statements (i.e. it is possible to
    generate adhoc statements for these parties).
    """
    asql_query = acm.CreateFASQLQuery(acm.FParty, 'AND')
    asql_query.AddAttrNode('ConfInstructions.EventChlItem.Name', 'EQUAL',
        get_statement_event_name())
    return asql_query.Select()


def statement_trades_exist(acquirer, counterparty, from_date, to_date):
    """
    Determine whether statement trades exist for the specified
    acquirer, counterparty, inclusive statement from date and
    inclusive statement to date.
    """
    statement_trades = get_statement_trades(acquirer, counterparty, from_date, to_date)
    return len(statement_trades) > 0


def _get_active_trades_for_party(acquirer, counterparty, from_date, to_date):
    """
    Get candidate active statement trades for an acquirer,
    counterparty, inclusive statement from date and inclusive
    statement to date.
    """
    asql_query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
    asql_query.AsqlNodes(_get_base_trade_asql_query())
    asql_query.AddAttrNode('Acquirer.Oid', 'EQUAL', acquirer.Oid())
    asql_query.AddAttrNode('Counterparty.Oid', 'EQUAL', counterparty.Oid())
    asql_query.AddAttrNode('ValueDay', 'LESS_EQUAL', to_date)
    asql_query.AddAttrNode('Instrument.ExpiryDate', 'GREATER_EQUAL', from_date)
    return asql_query.Select()


def _get_base_trade_asql_query():
    """
    Get the base asql query (static portion) to use for finding
    statement trades.
    """
    asql_query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
    # Only certain statuses.
    status_node = asql_query.AddOpNode('OR')
    for status in ['BO Confirmed', 'BO-BO Confirmed']:
        status_node.AddAttrNode('Status', 'EQUAL', status)
    # Only Deposits, FRNs, and two old long-term CDs.
    instrument_type_node = asql_query.AddOpNode('OR')
    for instrument_type in ['Deposit', 'FRN']:
        instrument_type_node.AddAttrNode('Instrument.InsType', 'EQUAL', instrument_type)
    cd_node = instrument_type_node.AddOpNode('AND')
    cd_node.AddAttrNode('Instrument.InsType', 'EQUAL', 'CD')
    cd_trade_node = cd_node.AddOpNode('OR')
    for trade_number in ['557162', '561101']:
        cd_trade_node.AddAttrNode('Oid', 'EQUAL', trade_number)
    # Only instruments with Fixed and Float legs.
    leg_node = asql_query.AddOpNode('OR')
    for leg_type in ['Fixed', 'Float']:
        leg_node.AddAttrNode('Instrument.Legs.LegType', 'EQUAL', leg_type)
    # Only non-Demat/DIS instruments.
    asql_query.AddAttrNode('Instrument.AdditionalInfo.Demat_Instrument', 'NOT_EQUAL', True)
    asql_query.AddAttrNode('Instrument.AdditionalInfo.DIS_Instrument', 'NOT_EQUAL', True)
    return asql_query


def _trade_has_interest_money_flows_between_dates(trade, from_date, to_date):
    """
    Determine if a trade has interest money flows during a
    period.
    """
    interest_money_flows = get_interest_money_flows_between_dates(trade,
        from_date, to_date)
    return len(interest_money_flows) > 0


def _get_interest_money_flows(trade):
    """
    Get any interest money flows for a trade.
    """
    interest_money_flows = list()
    for money_flow in trade.MoneyFlows().AsArray():
        if not _is_term_deposit_interest_money_flow(money_flow):
            continue
        interest_money_flows.append(money_flow)
    return interest_money_flows


def _is_term_deposit_interest_money_flow(money_flow):
    """
    Determine if a money flow represents a term deposit interest
    payment.
    """
    if not money_flow.SourceObject().IsKindOf(acm.FCashFlow):
        return False
    return money_flow.SourceObject().CashFlowType() in [
        'Fixed Rate',
        'Float Rate'
    ]
