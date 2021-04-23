"""
FX Cash Extract

This module is used for extracting realized cash from all FX trades.

Functions:
    write_cash_file - export cash info into file


Changelog:

Purpose:   This Module has been updated to handle new FX Cash Instruments.
Requester: Mathew Berry
Developer: Babalo Edwana
CR Number: 261644

Changes:   Updated Module, change date formatting for filename to use
           quick_time instead of packed time.
Developer: Babalo Edwana
Date:      06/04/2010
CR Number: 279327

Changes:   Updated Module, Added new class for retreiving the Portfolio
           Accumulated Cash value from Trading Manager
Developer: Babalo Edwana
Date:      20/04/2010
CR Number: 286190

Changes:   Added error handling for a wrong FX Swap trade.
Developer: Babalo Edwana
Date:      02/12/2010
CR Number: 513835

Changes:   Refactored to allow usage for FX trades (MOPL) and all trades (CRE).
Developer: Balazs Juraj
Date:      04/10/2011
CR Number: 789095

Changes:   Updated Combination trades to eliminate double counting for Payments
           and also fixed value date issue.
           Refactored code to use valuedate and paydate consistently.
Developer: Babalo Edwana
Date:      04/01/2012
CR Number: 870983

Changes:   update pritn statement for output file.
Developer: Babalo Edwana
Date:      13/01/2012
CR Number: 875705

Changes:   Count cashflows on trades with trade_process = 0
Developer: Frantisek Jahoda
Date:      4/11/2015
CR Number: 3235450

Changes:   Convert TradeProcess into FxIsSwapNearLeg, FxIsSwapFarLeg, ...
           Completely rewritten to ACM
Developer: Frantisek Jahoda
Date:      7/12/2015
CR Number: ...
"""

import csv
from collections import namedtuple, defaultdict

import acm
from DateUtils import PDate


CashFlow = namedtuple("CashFlow", "amount currency")


def _get_aggregates(flows):
    """
    Sum cashflows according to their currencies
    """
    aggr = defaultdict(float)
    for flow in flows:
        aggr[flow.currency] += flow.amount
    return [(curr, amount) for curr, amount in aggr.items() if amount]


def _get_realized_cash(trade, repdate):
    """Compute realized cash on instrument with PayType=Future"""
    cspace = acm.FCalculationSpace('FPortfolioSheet')
    try:
        cspace.SimulateGlobalValue(
                'Portfolio Profit Loss End Date',
                'Custom Date')
        cspace.SimulateGlobalValue(
                'Portfolio Profit Loss End Date Custom',
                repdate.strftime())
        calc = cspace.CreateCalculation(
                trade,
                'Portfolio Realized Profit and Loss')
        return calc.Value().Number()
    finally:
        cspace.RemoveGlobalSimulation('Portfolio Profit Loss End Date')
        cspace.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')


def _get_combination_currencies(trade, repdate):
    """
    Return all currencies present in the combination trade upto repdate
    """
    instrument = trade.Instrument()
    currencies = set()
    for c_instr in instrument.Instruments():
        if c_instr.IsKindOf(acm.FFxSwap):
            for leg in c_instr.Legs():
                for cashflow in leg.CashFlows():
                    if PDate(cashflow.PayDate()) <= repdate:
                        currencies.add(leg.Currency().Name())
        elif c_instr.IsKindOf(acm.FCurrency):
            paydate = PDate(trade.ValueDay())
            if paydate <= repdate:
                # Why to add instrument currency?
                # That was not explained by business.
                currencies.add(instrument.Currency().Name())
        else:
            print(("WARNING: Unknown instrument type (%s) in combination "
                   "for trade %d" % (c_instr.Class().Name(), trade.Oid())))
    return currencies


def _get_combination_cashflows(trade, repdate):
    """
    Return all cashflows on combination trades
    """
    currencies = _get_combination_currencies(trade, repdate)
    cspace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
    calculation = trade.Calculation()
    for curr in currencies:
        cash_incep = calculation.Cash(
                cspace,
                '', # startDate (since inception)
                repdate.strftime(), # endDate
                curr, # results will be transformed into this currency
                curr  # include only cashflow in this currency
        )
        cash_incep = cash_incep.Number()
        yield CashFlow(cash_incep, curr)


def _get_payments_cashflows(payments, repdate):
    """
    Generate cashflows from payments

    Handle payments in payment table
    premiums, brokerage, trade settlements,
    exercise cash and additional payments.
    """
    for payment in payments:
        paydate = PDate(payment.PayDay())
        if paydate <= repdate and payment.Amount():
            yield CashFlow(payment.Amount(), payment.Currency().Name())


def _get_fxswap_cashflows(far_trade, repdate):
    """
    Return all cashflows for fx swap
    """
    near_trade = far_trade.FxSwapNearLeg()
    if not near_trade:
        print("ERROR: Near leg is misssing for trade %d" % far_trade.Oid())
        return
    
    instrument = near_trade.Instrument()
    trade_curr = near_trade.Currency().Name()
    instr_curr = instrument.Currency().Name()
    
    if not near_trade.IsArchived():
        for flow in _get_payments_cashflows(near_trade.Payments(), repdate):
            yield flow

        near_date = PDate(near_trade.ValueDay())
        if near_date <= repdate:
            yield CashFlow(near_trade.Quantity(), instr_curr)
            yield CashFlow(near_trade.Premium(), trade_curr)

    far_date = PDate(far_trade.ValueDay())
    if far_date <= repdate:
        if not near_trade.IsArchived():
            yield CashFlow(near_trade.Fee(), trade_curr)
            yield CashFlow(near_trade.AggregatePl(), trade_curr)
        yield CashFlow(far_trade.Quantity(), instr_curr)
        yield CashFlow(far_trade.Premium(), trade_curr)


def _get_currency_cashflows(trade, repdate):
    """
    Return all cashflows on currency trades
    """
    if trade.IsFxSwapFarLeg():
        for flow in _get_fxswap_cashflows(trade, repdate):
            yield flow
        return

    instrument = trade.Instrument()
    trade_curr = trade.Currency().Name()
    instr_curr = instrument.Currency().Name()
    valuedate = PDate(trade.ValueDay())

    for flow in _get_payments_cashflows(trade.Payments(), repdate):
        yield flow

    # Handle premium and broker fee
    if valuedate <= repdate:
        yield CashFlow(trade.Fee(), trade_curr)
        yield CashFlow(trade.AggregatePl(), trade_curr)

        is_aggregate = trade.Aggregate() != 0
        if is_aggregate or trade.IsFxSpot() or trade.IsFxForward():
            yield CashFlow(trade.Quantity(), instr_curr)
            yield CashFlow(trade.Premium(), trade_curr)


def _get_other_cashflows(trade, repdate):
    """
    Return all cashflows for all other instrument types
    """
    trade_curr = trade.Currency().Name()
    instrument = trade.Instrument()

    for flow in _get_payments_cashflows(trade.Payments(), repdate):
        yield flow

    valuedate = PDate(trade.ValueDay())
    if valuedate <= repdate:
        yield CashFlow(trade.Fee(), trade_curr)
        yield CashFlow(trade.AggregatePl(), trade_curr)

        if trade.Premium():
            yield CashFlow(trade.Premium(), trade_curr)
        elif instrument.PayType() == "Future":
            yield CashFlow(_get_realized_cash(trade, repdate),
                    trade_curr)


def _get_trade_cashflows(trade, repdate):
    """
    Return all cashflows for a trade before repdate
    """
    if trade.IsFxSwapNearLeg():
        # both legs are processed together in near leg
        return []
    archive_date = PDate(trade.UpdateTime())
    if trade.IsArchived() and archive_date <= repdate:
        # trade was already archived
        return []

    instrument = trade.Instrument()
    if instrument.IsKindOf(acm.FCombination):
        generator = _get_combination_cashflows
    elif instrument.IsKindOf(acm.FCurrency):
        generator = _get_currency_cashflows
    else:
        generator = _get_other_cashflows

    flows = generator(trade, repdate)
    return _get_aggregates(flows)


def write_cash_file(filename, trades, date):
    """Write cash flows on trades into a file

    Parameters
    ----------
    filename : str
        Path to the output file
    trades : [acm.FTrade]
        Trades which should be processed
    date : PDate
        Write cash flows up to that date
    """
    with open(filename, "wb") as fout:
        writer = csv.writer(fout, lineterminator='\n')
        print("-- Getting flows --")
        writer.writerow('Trade,Amount,Currency'.split(','))

        for trade in trades:
            flows = _get_trade_cashflows(trade, date)
            for curr, amount in flows:
                writer.writerow((str(trade.Oid()), str(amount), curr))

        print('Done\nWrote to secondary output %s' % filename)
