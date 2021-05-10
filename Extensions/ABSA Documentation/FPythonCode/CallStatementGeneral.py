"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    CallStatementGeneral

DESCRIPTION
    This module contains general functionality related to call deposit statements.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2018-08-14      FAOPS-167       Cuen Edwards            Elaine Visagie          Initial Implementation.
2020-02-11      FAOPS-747       Cuen Edwards            Michelle Fowler         Changed to hide interest settling on the current date
                                                                                if the interest cash flow is still accruing.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm

import DocumentConfirmationGeneral
import DocumentGeneral


def get_statement_event_name():
    """
    Get the name of the event to associate with call deposit
    statement confirmations.
    """
    return 'Call Statement'


def get_statement_template_name():
    """
    Get the name of the template to associate with call deposit
    statement confirmations.
    """
    return 'ABSA_Call_Statement'


def get_statement_frequency_choice_list_name():
    """
    Get the name of the choice list used for storing call deposit
    statement frequency choices.
    """
    return 'Comm Freq Call'


def get_statement_frequency_choice_list_values():
    """
    Get a list of all call deposit statement frequency choice list
    values .
    """
    statement_frequency_choice_list = get_choice_list_by_list_name_and_entry_name('MASTER',
        get_statement_frequency_choice_list_name())
    choice_list_values = list()
    for choice_list in statement_frequency_choice_list.Choices():
        choice_list_values.append(choice_list.Name())
    return choice_list_values


def get_daily_statement_frequency_value():
    """
    Get the value used to indicate that daily month-to-date call
    deposit statements should be received.
    """
    return 'Daily'


def get_weekly_statement_frequency_value():
    """
    Get the value used to indicate that weekly call deposit
    statements should be received.
    """
    return 'Weekly'


def get_monthly_statement_frequency_value():
    """
    Get the value used to indicate that monthly call deposit
    statements should be received.
    """
    return 'Monthly'


def get_all_statement_frequency_value():
    """
    Get the value used to indicate that all scheduled call deposit
    statements should be received.
    """
    return 'All'


def get_statement_frequency_add_info_name():
    """
    Get the name of the additional info field used for storing a
    party's call deposit statement frequency choice.
    """
    return 'Comm Freq Call'


def statement_confirmation_exists(trade, from_date, to_date, document_schedule=None):
    """
    Determine if a call deposit statement confirmation exists for
    the specified trade, inclusive statement from date, inclusive
    statement to date and optional document communication frequency
    schedule.
    """
    return len(get_existing_statement_confirmations(trade, from_date, to_date, document_schedule)) > 0


def get_existing_statement_confirmations(trade, from_date, to_date, document_schedule=None):
    """
    Get any existing call statement confirmations for the specified
    trade, inclusive statement from date, inclusive statement to date
    and optional document communication frequency schedule.
    """
    asql_query = acm.CreateFASQLQuery(acm.FConfirmation, 'AND')
    asql_query.AddAttrNode('Trade.Oid', 'EQUAL', trade.Oid())
    asql_query.AddAttrNode('EventChlItem.Name', 'EQUAL', get_statement_event_name())
    from_date_method_name = DocumentGeneral.get_additional_info_method_name(
        DocumentConfirmationGeneral.get_confirmation_from_date_add_info_name())
    from_date_attribute_name = 'AdditionalInfo.{from_date_method_name}'.format(
        from_date_method_name=from_date_method_name
    )
    asql_query.AddAttrNode(from_date_attribute_name, 'EQUAL', from_date)
    to_date_method_name = DocumentGeneral.get_additional_info_method_name(
        DocumentConfirmationGeneral.get_confirmation_to_date_add_info_name())
    to_date_attribute_name = 'AdditionalInfo.{to_date_method_name}'.format(
        to_date_method_name=to_date_method_name
    )
    asql_query.AddAttrNode(to_date_attribute_name, 'EQUAL', to_date)
    if document_schedule is not None:
        schedule_method_name = DocumentGeneral.get_additional_info_method_name(
            DocumentConfirmationGeneral.get_confirmation_schedule_add_info_name())
        schedule_attribute_name = 'AdditionalInfo.{schedule_method_name}'.format(
            schedule_method_name=schedule_method_name
        )
        asql_query.AddAttrNode(schedule_attribute_name, 'EQUAL', document_schedule)
    return asql_query.Select()


def create_statement_confirmation(trade, from_date, to_date, document_schedule):
    """
    Create a call deposit statement confirmation for the specified 
    trade, inclusive statement from date, inclusive statement to date 
    and document communication frequency schedule.
    """
    DocumentConfirmationGeneral.create_document_confirmation(get_statement_event_name(),
        trade, None, from_date, to_date, document_schedule)


def get_statement_trades(acquirer, counterparty, from_date, to_date):
    """
    Get the trades for which call deposits statements should be
    generated for the specified acquirer, counterparty, inclusive
    statement from date and inclusive statement to date.
    """
    trades = list()
    for trade in _get_active_trades_for_party(acquirer, counterparty, from_date, to_date):
        if not statement_money_flows_exist(trade, from_date, to_date):
            continue
        trades.append(trade)
    return trades


def is_eligible_for_statement(trade):
    """
    Determine whether or not a specified trade is eligible for
    inclusion on a call deposit statement.
    """
    return _get_base_trade_asql_query().IsSatisfiedBy(trade)


def find_parties_receiving_scheduled_statements_for_acquirer_and_frequency(
        acquirer, statement_frequency):
    """
    Find all parties configured to receive scheduled call deposit
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


def statement_money_flows_exist(trade, from_date, to_date):
    """
    Determine whether statement money flows exist for the specified
    trade, inclusive statement from date and nclusive statement to
    date.
    """
    _statement_money_flows = get_statement_money_flows(trade, from_date, to_date)
    return len(_statement_money_flows) > 0


def get_statement_money_flows(trade, from_date, to_date):
    """
    Get any money flows that affect a trade during a statement
    period.
    """
    statement_money_flows = list()
    for money_flow in trade.MoneyFlows().AsArray():
        if _is_statement_money_flow(money_flow, from_date, to_date):
            statement_money_flows.append(money_flow)
    return statement_money_flows


def money_flow_affects_account_balance(money_flow):
    """
    Determine whether or not a money flow affects the balance of a
    call deposit.
    """
    return (is_fixed_amount_money_flow(money_flow) or
        is_interest_reinvestment_money_flow(money_flow))


def is_fixed_amount_money_flow(money_flow):
    """
    Determine whether or not a money flow is a fixed-amount money
    flow.
    """
    if not DocumentGeneral.is_cash_flow_money_flow(money_flow):
        return False
    return money_flow.SourceObject().CashFlowType() in ('Fixed Amount', 'Aggregated Fixed Amount')


def is_interest_money_flow(money_flow):
    """
    Determine whether or not a money flow is an interest money flow.
    """
    return (is_call_fixed_rate_adjustable_money_flow(money_flow) or
        is_fixed_rate_adjustable_money_flow(money_flow))


def is_call_fixed_rate_adjustable_money_flow(money_flow):
    """
    Determine whether or not a money flow is a call fixed rate
    adjustable interest money flow.
    """
    if not DocumentGeneral.is_cash_flow_money_flow(money_flow):
        return False
    return money_flow.SourceObject().CashFlowType() == 'Call Fixed Rate Adjustable'


def is_fixed_rate_adjustable_money_flow(money_flow):
    """
    Determine whether or not a money flow is a fixed rate adjustable
    interest money flow.
    """
    if not DocumentGeneral.is_cash_flow_money_flow(money_flow):
        return False
    return money_flow.SourceObject().CashFlowType() == 'Fixed Rate Adjustable'


def is_interest_reinvestment_money_flow(money_flow):
    """
    Determine whether or not a money flow is an interest reinvestment
    money flow.
    """
    if not DocumentGeneral.is_cash_flow_money_flow(money_flow):
        return False
    return money_flow.SourceObject().CashFlowType() == 'Interest Reinvestment'


def get_money_flow_value_date(money_flow):
    """
    Get the value date (intended pay date) of a money flow for
    statement purposes.
    """
    if _is_back_dated_fixed_amount_money_flow(money_flow):
        return money_flow.StartDate()
    return money_flow.PayDate()


def is_interest_money_flow_still_accruing(money_flow):
    """
    Determine whether or not an interest money flow is still
    accruing.

    This can only be true when all of the following apply:
        - The interest money flow end date is equal to today.
        - There is no current interest cash flow as the account
          has not been rolled (cash flow end is exclusive).
    """
    if money_flow.EndDate() != acm.Time.DateToday():
        return False
    leg = money_flow.SourceObject().Leg()
    current_cash_flow = leg.GetCurrentCashFlow(money_flow.EndDate())
    return current_cash_flow is None


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
    # Only Deposits.
    asql_query.AddAttrNode('Instrument.InsType', 'EQUAL', 'Deposit')
    # Only Deposits with Call Fixed Adjustable
    asql_query.AddAttrNode('Instrument.Legs.LegType', 'EQUAL', 'Call Fixed Adjustable')
    # Only non-Demat/DIS instruments.
    asql_query.AddAttrNode('Instrument.AdditionalInfo.Demat_Instrument', 'NOT_EQUAL', True)
    asql_query.AddAttrNode('Instrument.AdditionalInfo.DIS_Instrument', 'NOT_EQUAL', True)
    return asql_query


def _is_statement_money_flow(money_flow, from_date, to_date):
    """
    Determine whether or not a money flow affects a trade during a
    statement period.
    """
    if _is_statement_interest_money_flow(money_flow, from_date, to_date):
        return True
    elif _is_statement_fixed_amount_money_flow(money_flow, from_date, to_date):
        return True
    elif _is_statement_interest_reinvestment_money_flow(money_flow, from_date, to_date):
        return True
    return False


def _is_statement_interest_money_flow(money_flow, from_date, to_date):
    """
    Determine whether or not a money flow is an interest money flow
    affecting a trade during a statement period.
    """
    if not is_interest_money_flow(money_flow):
        return False
    if money_flow.StartDate() > to_date:
        return False
    if money_flow.PayDate() < from_date:
        return False
    if DocumentGeneral.is_zero_amount_money_flow(money_flow):
        return False
    return True


def _is_statement_fixed_amount_money_flow(money_flow, from_date, to_date):
    """
    Determine whether or not a money flow is a fixed-amount money
    flow affecting a trade during a statement period.
    """
    if not is_fixed_amount_money_flow(money_flow):
        return False
    value_date = get_money_flow_value_date(money_flow)
    if value_date > to_date:
        return False
    if value_date < from_date:
        return False
    if DocumentGeneral.is_zero_amount_money_flow(money_flow):
        return False
    return True


def _is_statement_interest_reinvestment_money_flow(money_flow, from_date, to_date):
    """
    Determine whether or not a money flow is an interest reinvestment
    money flow affecting a trade during a statement period.
    """
    if not is_interest_reinvestment_money_flow(money_flow):
        return False
    if money_flow.PayDate() > to_date:
        return False
    if money_flow.PayDate() < from_date:
        return False
    if DocumentGeneral.is_zero_amount_money_flow(money_flow):
        return False
    return True


def _is_back_dated_fixed_amount_money_flow(money_flow):
    """
    Determine whether or not a money flow is a back-dated fixed
    amount money flow.
    """
    if not is_fixed_amount_money_flow(money_flow):
        return False
    if not money_flow.StartDate():
        return False
    return money_flow.StartDate() < money_flow.PayDate()


def get_choice_list_by_list_name_and_entry_name(list_name, entry_name):
    """
    Get a choice list by list name and entry name.
    """
    select_expression = "list = '{list_name}' and name = '{entry_name}'".format(
        list_name=list_name,
        entry_name=entry_name
    )
    error_message = "Expecting zero or one choice list for list "
    error_message += "'{list_name}' and name '{entry_name}'".format(
        list_name=list_name,
        entry_name=entry_name
    )
    choice_list = acm.FChoiceList.Select01(select_expression, error_message)
    return choice_list
