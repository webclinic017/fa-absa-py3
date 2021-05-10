"""-----------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no Developer           Description
--------------------------------------------------------------------------------
2012-04-13 C134733   Bhavnisha Sarawan   Updated to exclude Redemption Amount 
                                         from cashflows to be used in calc.
2014-02-20 CHNG0001742125 Sanele Macanda Excluded Interest Reinvestments 
                                         cashflows and returned the 'ZAR' 
                                         equivalent for all currencies.
2015-04-14 Andrei Conicov Excluding Simulated, Voided and Terminated trades.
2015-06-03 2865089   Libor Svoboda       Redesigned to leg-level based 
                                         calculations.
2015-10-15 CHNG0003118360 Mike Schaefer  Added the calculation for Index Linked
                                         Bonds.
2016-01-21 3384605   Libor Svoboda       Removed the calculation for Index
                                         Linked Bonds.
2016-03-11	     Mighty Mkansi       Added logic for Current nominal = 
					 Face nominal X CPI scalar where 
					 CPI scalar = Ref CPI on Measure date/ Initial index
2020-05-18 FAFO-99   Amit Kardile        Fixed the bug in 'CurrentNominal' for inflation bonds
--------------------------------------------------------------------------------
"""

import acm, ael

cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()


def is_call_deposit(leg):
    return (leg.Instrument().InsType() == 'Deposit'
            and leg.LegType() in ['Call Fixed', 'Call Float', 'Call Fixed Adjustable'])


def get_cash_flows(leg):
    """Return cash flows belonging to the input leg."""
    if is_call_deposit(leg):
        return [cf for cf in leg.CashFlows() if cf.CashFlowType() in 
                ['Fixed Amount', 'Redemption Amount', 'Interest Reinvestment']]
    else:    
        return [cf for cf in leg.CashFlows() if cf.CashFlowType() not in 
                ['Fixed Amount', 'Redemption Amount', 'Interest Reinvestment']]


def calculate_nominal(cash_flow, trade):
    """Calculate nominal for a single cash flow and trade."""
    if cash_flow.CashFlowType() == 'Redemption Amount':
        return cash_flow.Calculation().Projected(cs, trade).Number()
    
    orig_curr = cash_flow.Leg().Currency()
    try:
        return cash_flow.Calculation().Nominal(cs, trade, orig_curr).Number()
    except TypeError:
        return 0
        

def get_call_deposit_nominal(cash_flows, trades, date):
    """Calculate nominal across cash flows and trades for 
    Call Fixed/Call Float Deposits.
    """
    nominal = 0.0
    for cf in cash_flows:
        if cf.PayDate() > date:
            for trade in trades:
                if trade.Status() in ['Terminated', 'Void']:
                    continue
                if trade.ValueDay() > date:
                    continue
                nominal += calculate_nominal(cf, trade)
    return nominal


def get_nominal(cash_flows, trades, date):
    """Calculate nominal across cash flows and trades."""
    nominal = 0.0
    start_date = '0001-01-01'
    end_date = '0001-01-01'
    cash_flows.sort(key=lambda cf: (cf.StartDate(), cf.EndDate()))
    for cf in cash_flows:
        if (date >= cf.StartDate() and date < cf.EndDate()
                and start_date != cf.StartDate() and end_date != cf.EndDate()):
            start_date = cf.StartDate()
            end_date = cf.EndDate()
            for trade in trades:
                if trade.Status() in ['Simulated', 'Terminated', 'Void']:
                    continue
                if trade.ValueDay() > date:
                    continue
                nominal += calculate_nominal(cf, trade)
    return nominal


def get_cpi_unscaled_nominal(leg, trades, valuation_date):
    nominal = 0.0
    for trade in trades:
        if trade.Status() in ['Void'] or trade.ValueDay() > valuation_date:
            continue
        trade_nominal = 0.0
        for cash_flow in leg.CashFlows().SortByProperty('PayDate', True):
            if cash_flow.CashFlowType() != 'Fixed Amount':
                if valuation_date >= cash_flow.StartDate() and valuation_date <= cash_flow.EndDate():
                    trade_nominal = trade.Quantity() * cash_flow.NominalFactor() * 1000000
        nominal += trade_nominal
    return nominal


def currentNominal(leg, date, trades):
    """Return leg-level based current nominal."""
    cash_flows = get_cash_flows(leg)   
    current_nom = 0.0
    if is_call_deposit(leg):
        current_nom = get_call_deposit_nominal(cash_flows, trades, date)
    elif (leg.InflationScalingRef()):
        cpi_reference = leg.InflationScalingRef()
        initial_index_value = leg.InflationBaseValue()
        current_cpi_value = cpi_reference.Calculation().ForwardPrice(cs, date).Number()
        cpi_scalar = float(current_cpi_value) / float(initial_index_value)
        current_nom = get_cpi_unscaled_nominal(leg, trades, date) * cpi_scalar
    else:
        current_nom = get_nominal(cash_flows, trades, date)
    return current_nom
