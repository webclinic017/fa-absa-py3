"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    LoanRepaymentNoticeScript.

DESCRIPTION
    This module contains an AEL main script used for the bulk generation of
    repayment notices.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2018-11-20      FAOPS-160       Stuart Wilson           Loan Ops                Initial Implementation.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

from datetime import datetime

import acm

from at_logging import getLogger
from at_ael_variables import AelVariableHandler
import DocumentConfirmationGeneral
import DocumentGeneral
import LoanNoticeGeneral
import MultiTradeConfirmationOwnerProvider


confirmation_owner_trade_provider = MultiTradeConfirmationOwnerProvider.MultiTradeConfirmationOwnerProvider()
LOGGER = getLogger(__name__)
ael_variables = AelVariableHandler()
PAY_DAY = acm.Time().DateAddDelta(acm.Time().DateNow(), 0, 0, 7)


ael_variables.add(
    'query_folder',
    label='Query Folder',
    collection=[0, 1],
    cls='int',
    default=0)


ael_variables.add(
    'query_folder_name',
    label='Query name',
    cls=acm.FStoredASQLQuery,
    collection=acm.FStoredASQLQuery.Select(
      "subType='FTrade'"),
    mandatory=False,
    alt="Query folder that will be used to generate confirmation for loan notices")

    
def get_trades_from_query_folder(name, date=acm.Time.DateToday()):
    query_name = name
    query_nodes = acm.FStoredASQLQuery[query_name].Query().AsqlNodes()
    asql_query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
    asql_query.AsqlNodes(query_nodes)
    asql_query.AddAttrNode('Instrument.Legs.CashFlows.PayDate', 'EQUAL', date)
    return asql_query.Select()


def get_currencies_from_trades(trades):
    currency_list = list()
    for trade in trades:
        if trade.Currency() not in currency_list:
            currency_list.append(trade.Currency())
    return currency_list
   
 
def get_valid_trades_per_party_acquirer_pair(party_acquirer_tuple, date=acm.Time.DateToday()):
    query_name = 'ABSA_REPAYMENT_NOTICE'
    query_nodes = acm.FStoredASQLQuery[query_name].Query().AsqlNodes()
    asql_query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
    asql_query.AsqlNodes(query_nodes)
    asql_query.AddAttrNode('Instrument.Legs.CashFlows.PayDate', 'EQUAL', date)
    asql_query.AddAttrNode('Counterparty.Oid', 'EQUAL', party_acquirer_tuple[0].Oid())
    asql_query.AddAttrNode('Acquirer.Oid', 'EQUAL', party_acquirer_tuple[1].Oid())
    valid_trades = list()
    for trade in asql_query.Select():
        if not DocumentGeneral.is_almost_zero(LoanNoticeGeneral.sum_nominal_before_payday_repayment_notice(trade, PAY_DAY)):
            valid_trades.append(trade)
            
    return valid_trades


def seven_days_before_pay_day_cashflow(trade, date):
    seven_days_future = acm.Time().DateAddDelta(date, 0, 0, 7)
    list_of_types = ['Fixed Amount', 'Redemption Amount']
    for cashflow in trade.Instrument().MainLeg().CashFlows():
        if cashflow.PayDate() == seven_days_future and cashflow.CashFlowType() not in list_of_types:
            
            return cashflow


def seven_days_before_pay_day_fixed_cashflow(trade, date):
    seven_days_future = acm.Time().DateAddDelta(date, 0, 0, 7)
    redemption_cashflow = None
    fixed_cashflow = None

    for cashflow in trade.Instrument().MainLeg().CashFlows():
        if cashflow.PayDate() == seven_days_future and cashflow.CashFlowType() == 'Fixed Amount' \
                and cashflow.FixedAmount() > 0:
            fixed_cashflow = cashflow

        elif cashflow.PayDate() == seven_days_future and cashflow.CashFlowType() == 'Redemption Amount':
               redemption_cashflow = cashflow

    return fixed_cashflow, redemption_cashflow


def ael_main(ael_parameters):
    """
    AEL Main Function.
    """
    document_event_name = 'Repayment Notice'
    query_folder_name = ael_parameters['query_folder_name']

    try:
        start_date_time = datetime.today()
        LOGGER.info('Starting at {start_date_time}'.format(start_date_time=start_date_time))
        trades = get_trades_from_query_folder(query_folder_name.Name(), PAY_DAY)
        party_acquirer_list = list()

        for trade in trades:
            
            if not DocumentGeneral.is_almost_zero(LoanNoticeGeneral.sum_nominal_before_payday_repayment_notice(trade, PAY_DAY)):
                if not seven_days_before_pay_day_cashflow(trade, acm.Time.DateToday()):
                    if not seven_days_before_pay_day_fixed_cashflow(trade, acm.Time.DateToday()):
                        continue
                if (trade.Counterparty(), trade.Acquirer()) not in party_acquirer_list:
                    party_acquirer_list.append((trade.Counterparty(), trade.Acquirer()))

        for party_acquirer in party_acquirer_list:
            party_linked_trades = get_valid_trades_per_party_acquirer_pair(party_acquirer, PAY_DAY)
            confo_owner_trade = confirmation_owner_trade_provider.provide_owner_trade(
                party_linked_trades[0].Acquirer(), party_linked_trades[0].Counterparty())

            DocumentConfirmationGeneral.create_document_confirmation(document_event_name, confo_owner_trade)

        end_date_time = datetime.today()
        LOGGER.info('Completed successfully at {end_date_time}'.format(end_date_time=end_date_time))
        duration = end_date_time - start_date_time
        LOGGER.info('Duration: {duration}'.format(duration=duration))
    except Exception as exception:
        DocumentGeneral.handle_script_exception(exception)
