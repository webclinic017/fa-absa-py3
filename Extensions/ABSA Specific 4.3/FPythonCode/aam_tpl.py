
"""
Purpose: Calculate BESA TPL
Requestor: Naidoo, Suvarn
Developer: Bahounek, Ondrej
Description: calculate values:
    1) TheoVal_b (with BESA price of the underlying) (column: "Portfolio Theoretical Value")
    2) TheoVal_o (standard theoretical value) (column: "Portfolio Theoretical Value")
    3) MaVal (column: "Portfolio Market Value")
    4) BESA TPL = TheoVal_b - TheoVal_o + MaVal
"""

import acm


START_DATE = "1900-01-01"
COL_THVAL = "Portfolio Theoretical Value"
COL_MAVAL = "Portfolio Market Value"


def _get_adhoc_portf(trade):
    """
    Returns Adhoc Portfolio to use in calculation space
    """
    portfolio = acm.FAdhocPortfolio()
    portfolio.Add(trade)
    return portfolio


def _get_besa_price(instr, price_date):
    market = "SPOT_BESA"
    if price_date == acm.Time.DateToday():
        price = [p for p in instr.Prices() if p.Market().Name() == market
                    and p.Day() == price_date]
    else:
        price = acm.FPrice.Select("instrument='%s' and market='%s' and day='%s'" 
            % (instr.Name(), market, price_date))
    if price:
        return price[0].Settle()

        
def _fill_dict(simulated_values, params):
    for name, val in list(simulated_values.items()):
        simulated_values[name] = val.format(**params)
        
        
def _create_calc_space(portf, simulated_values):
    calc_space = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FPortfolioSheet')
    for (column_id, value) in list(simulated_values.items()):
        calc_space.SimulateValue(portf, column_id, value)
    calc_space.Refresh()
    return calc_space


def calc_value(calc_space, siat, column, sim_vals):
    if sim_vals:
        for (column_id, value) in list(sim_vals.items()):
            calc_space.SimulateValue(siat, column_id, value)
        calc_space.Refresh()
    
    calc = calc_space.CreateCalculation(siat, column)
    return calc.Value()


def calculate_besa_tpl(trade, end_date):
    underlying = trade.Instrument().ValuationUnderlying()
    if not underlying:
        return acm.Math.NotANumber()
        
    besa_price = _get_besa_price(underlying, end_date)
    if not besa_price:
        return acm.Math.NotANumber()
    
    add_vals = {"Portfolio Underlying Price": besa_price}
    
    param_dict = {"end_date": end_date}
    global_values = {
        'Portfolio Profit Loss Start Date': 'Custom Date', 
        'Portfolio Profit Loss Start Date Custom': START_DATE,
        'Portfolio Profit Loss End Date': 'Custom Date', 
        'Portfolio Profit Loss End Date Custom': "{end_date}",
        'Valuation Date': "{end_date}",
        }
    _fill_dict(global_values, param_dict)
    
    portf = _get_adhoc_portf(trade)
    calc_space = _create_calc_space(portf, global_values)
    builder = acm.Risk.CreateSingleInstrumentAndTradesBuilder(portf, trade.Instrument())
    siat = builder.GetTargetInstrumentAndTrades()  # Single Instrument and Trades
    
    ma_val = calc_value(calc_space, siat, COL_MAVAL, None)
    thval_old = calc_value(calc_space, siat, COL_THVAL, None)
    thval_besa = calc_value(calc_space, siat, COL_THVAL, add_vals)
    
    res = thval_besa - thval_old + ma_val

    return res
