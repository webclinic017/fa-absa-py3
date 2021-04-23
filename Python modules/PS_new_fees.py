'''
Date                    : [2012-02-15]
Purpose                 : [Calculate fees according to trade and portfolio type (fixed vs cost plus methodology)]
                           
Department and Desk     : [Prime Services]
Requester               : [Francois Henrion]
Developer               : [Peter Fabian]
CR Number               : [C000000892151]

HISTORY
================================================================================
Date        Change no Developer          Description
--------------------------------------------------------------------------------
2012-05-16  C194115   Peter Fabian       Added new calculation for strate fee, cap for IPL and added VAT to JSE cost
2013-02-18  C809119   Peter Kutnik       Updates for Voice fees on Equities
2014-06-05  C2018916  Jakub Tomaga       On-tree, off-tree execution fee calculations.
2014-06-12  C1997018  Peter Fabian       Strate fee renamed to broker fixed fee plus VAT added to it
2016-05-16  3661849   Jakub Tomaga       Calculate exec fee for CFDs from payments (if present).
2017-04-04  4452477   Libor Svoboda      JSE cost updates 2017.
2018-07-03  CHG1000166517  Libor Svoboda      JSE cost updates 2018.
2019-03-19  INC1010780841  Tibor Reiss   Cater for trades without payment and rollout deleting the contract trade
2019-06-13  CHG1001882656  Tibor Reiss   Cater for update of allocation scripts
'''

import acm
import PS_TimeSeriesFunctions
import PS_TradeFees
import SAEQ_BrokerFees
from FBDPCommon import is_acm_object
from PS_AllocateTrades import (XTP_TRADE_TYPE_ALLOCATION, XTP_TRADE_TYPE_BLOCK_TRADE)


def markup_fee(trade_value, portfolio, trade_date):
    """ Calculates markup fee for the trade
        Uses PSExtExecPremRate additional information from portfolio
    """
    return trade_value * PS_TimeSeriesFunctions.GetExecutionPremiumRate(portfolio, trade_date) / 100.0


def calculate_cost_plus_dma_fee(trade_value, portfolio, trade_date):
    cost_incl_vat = SAEQ_BrokerFees.calculate_jse_cost(trade_value,
                                                       portfolio.Name(),
                                                       acm_trade_date=trade_date)

    return -1 * cost_incl_vat + markup_fee(trade_value, portfolio, trade_date)


def addFee(trade):
    if not is_acm_object(trade):
        try:
            trade = acm.FTrade[trade.trdnbr]
        except Exception as ex:
            acm.Log('Parameter is not a trade object: ' + str(ex))

    portfolio = trade.Portfolio()

    if  trade.Instrument().QuoteType() == 'Per 100 Units':
        trade_value = abs(trade.Price()/100.0 * trade.Quantity())
    else:
        trade_value = abs(trade.Price() * trade.Quantity())

    trade_type = trade.EquityTradeType()

    trade_date = PS_TradeFees._RemoveTime(trade.TradeTime())
    fee = 0
    # make empty fee default to fixed fee
    if (portfolio.add_info('PS_FixedFee') == 'Fixed' or portfolio.add_info('PS_FixedFee') == ''):
        # fixed fee
        if trade_type == 'Trade Report':
            fee = trade_value * PS_TimeSeriesFunctions.GetExecutionPremiumRate(portfolio, trade_date, 'Non-DMA') / 100.0
        elif trade_type == 'Voice':
            fee = trade_value * PS_TimeSeriesFunctions.GetExecutionPremiumRate(portfolio, trade_date, 'Voice') / 100.0
        else:
            fee = trade_value * PS_TimeSeriesFunctions.GetExecutionPremiumRate(portfolio, trade_date) / 100.0
    elif (portfolio.add_info('PS_FixedFee') == 'CostPlus'):
        # cost plus methodology

        if trade_type == 'Trade Report':
            fee = trade_value * PS_TimeSeriesFunctions.GetExecutionPremiumRate(portfolio, trade_date, 'Non-DMA') / 100.0
        elif trade_type == 'Voice':
            fee = trade_value * PS_TimeSeriesFunctions.GetExecutionPremiumRate(portfolio, trade_date, 'Voice') / 100.0
        else:
            fee = calculate_cost_plus_dma_fee(trade_value, portfolio, trade_date)
    return fee



def alloc_trade_fee(trade):
    """Retrun respective portion of total fee

    For trades that went through the allocation process we must calculate
    the fees according to the original allocation trades. Then we sum that
    up and repartition the sum of fees according to quantity per repartitioned
    trade.

    """
    # first get the total fee for all allocation trades
    # (the fees has to be calculated per allocation trade [business reason])
    TotalFee = 0
    total_quantity = 0
    trades = get_alloc_trades(trade)
    for allocTrade in trades:
        TotalFee += addFee(allocTrade)
        total_quantity += allocTrade.Quantity()

    if total_quantity == 0:
        acm.Log("Warning: Trade %d: " % trade.Oid() +
                "Total quantity of allocation trades is Zero. " +
                "Zero fee will be calculated.")
        return 0

    # While calculating fees, we want to use original allocation quantity.
    ratio = trade.Quantity() / total_quantity

    # return the respective portion of the total fee
    return TotalFee * ratio


def get_alloc_trades(trade):
    """Return all allocation trades for particular trade.

    Meant to be after aggregation & splitting up into books in PB_RISK
    portfolio tree.

    """
    mirrorTradeInAllocPf = trade.Contract()
    aggregatedTrade = mirrorTradeInAllocPf.ContractTrdnbr()
    aggregatedTrades = acm.FTrade.Select("contractTrdnbr=%d" % aggregatedTrade)
    allocTrades = []
    for aggregatedTrade in aggregatedTrades:
        # We want only the original allocation trades.
        if aggregatedTrade.add_info('XtpTradeType') not in ["", XTP_TRADE_TYPE_ALLOCATION, XTP_TRADE_TYPE_BLOCK_TRADE] \
                and aggregatedTrade.Status != 'Void' \
                and aggregatedTrade.Portfolio() \
                and aggregatedTrade.Portfolio().add_info('PS_PortfolioType') == "CFD Allocation" \
                and aggregatedTrade.Text1() == "Allocation Process":
            allocTrades.append(aggregatedTrade)

    return allocTrades


def execution_fee_on_tree(trade):
    """Return execution fee (on tree)."""
    execution_fee = 0.0

    # Verify trade's status
    if trade.Status() in ['FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed']:
        # Check first the off-tree trade
        off_tree_trade = acm.FTrade.Select("contractTrdnbr=%d" % trade.Oid())
        payment = None
        if off_tree_trade.Size() == 1:  # Backwards compatibility: old alloc method would return more than 1 trade
            payment = get_cfd_exec_fee_payment(off_tree_trade[0])
            if payment:
                execution_fee = payment.Amount()
        if not payment:
            # Don't charge execution fee for 'PS No Fees' trades
            if not(PS_TradeFees.isTakeonTrade(trade)):
                if trade.Text1() == 'Allocation Process':
                    execution_fee = alloc_trade_fee(trade)
                else:
                    execution_fee = addFee(trade)
                
    return execution_fee


def execution_fee_off_tree(reporting_trade):
    """Return execution fee (off tree)."""

    # Check object type
    if not is_acm_object(reporting_trade):
        try:
            reporting_trade = acm.FTrade[reporting_trade.trdnbr]
        except Exception as ex:
            acm.Log('Parameter is not a trade object: ' + str(ex))
    
    # Check if the trade has CFD execution fee payments (new methodology)
    payment = get_cfd_exec_fee_payment(reporting_trade)
    if payment:
        return payment.Amount()

    # Calculate execution fee on-the-fly if trade has no CFD payments
    trade = reporting_trade.Contract()
    # If the trade does not have a payment and the trade rollout deleted the referenced
    # contract trade (there is no constraint on contract trdnbr), the variable trade is
    # None so need to return 0.0.
    if not trade:
        return 0.0
    # Skip if trade is connected to itself
    if trade.Oid() == reporting_trade.Oid():
        return 0.0
    
    return execution_fee_on_tree(trade)


def get_cfd_exec_fee_payment(trade):
    """Return execution fee payment on CFD off-tree trade."""
    for payment in trade.Payments():
        if payment.Type() == "CFD Execution Fee":
            return payment
    return None


def add_cfd_execution_fee(trade):
    """Calculate execution fee from on-tree stock and add it as a payment."""
    execution_fee = execution_fee_off_tree(trade)
    payment = get_cfd_exec_fee_payment(trade)
    if payment:
        # Amend existing payment
        payment.Amount(execution_fee)
        payment.PayDay(trade.ValueDay())
        payment.ValidFrom(trade.ValueDay())
        payment.Commit()
    else:
        # Create new payment
        payment = acm.FPayment()
        payment.Trade(trade)
        payment.Currency(acm.FInstrument['ZAR'])
        payment.Type('CFD Execution Fee')
        payment.Party(acm.FParty["PRIME SERVICES DESK"])
        payment.Amount(execution_fee)
        payment.PayDay(trade.ValueDay())
        payment.ValidFrom(trade.ValueDay())
        payment.Commit()
    return execution_fee
