""" SEQ_VERSION_NR = PRIME 2.8.1 """




"""----------------------------------------------------------------------------
MODULE
    FEqUtilsPRIME - Small help functions used by several AEL modules
    
    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.
 
 ---------------------------------------------------------------------------"""
import math

"""----------------------------------------------------------------------------
AsList() 
    The function converts a tuple into a list.
    (PRIME always returns arrays but AEL wants lists.)
----------------------------------------------------------------------------"""    
def AsList(tupl):
    res = []
    for item in tupl: res.append(item)
    return res

"""----------------------------------------------------------------------------
AsMatrix() 
    The function converts a tuple of tuples into a list of lists.
    (PRIME always returns arrays but AEL wants lists.)
----------------------------------------------------------------------------"""    
def AsMatrix(tupl):
    res = []
    for item in tupl: res.append(AsList(item))
    return res
    
"""----------------------------------------------------------------------------
transform_dividends() 
    The function creates a dividend vector on the form
    [(div1,time1),(div2,time2),...,()]
----------------------------------------------------------------------------"""    
def transform_dividends(div_times_, div_vals_):
    div_times = AsList(div_times_)
    div_vals = AsList(div_vals_)
    dividends = []
    for i in range(len(div_times)):
        dividends.append((div_vals[i], div_times[i]))
    return dividends

"""----------------------------------------------------------------------------
get_dividends() 
    The function fetches future dividends for a derivative. 
    Vector on form [(div1,time1),(div2,time2),...,()].
----------------------------------------------------------------------------"""    
def get_dividends(i, valuation_date, texp):
    dividends = []
    has_past_div = 0
    for d in i.und_insaddr.dividends(i.exp_day):
        div_date = valuation_date.years_between(d.ex_div_day, 'Act/365')
        # Only take in account the dividends that are payed out before the expiry of the option. 
        if div_date <= texp and d.dividend > 0.0:
            if div_date < 0.0: has_past_div = 1
            else: dividends.append((d.dividend, div_date))           
        if len(dividends)==0 and has_past_div:
            dividends.append((0, texp/2.0))
    return dividends

"""----------------------------------------------------------------------------
has_greeks() 
    The function returns 0 if the barrier result has not porduced greeks, 1
    if the barrier option has been priced with a trinomial tree and greeks are
    returned from the tree.
----------------------------------------------------------------------------"""    
def has_greeks(res_dict):
    greeks = res_dict.copy()
    del greeks['PV']
    has_greek = 0
    for greek in greeks.values():
        if greek != -1:
            has_greek = 1
            break
    return has_greek
    
"""----------------------------------------------------------------------------
check_has_greeks() 
    The function checks if the result includes also the greeks.
----------------------------------------------------------------------------"""    
def check_has_greeks(res):
    if str(type(res)) == "<type 'dict'>" or str(type(res)) == "<type 'dictionary'>":
        if has_greeks(res): return res
        else: return {"PV":res["PV"]}
    return {"PV":res}
    
"""----------------------------------------------------------------------------
fetch_corr_stock_fx() 
    The function returns the correlation between the underlying asset and the 
    currency pair "Instrument curr / Strike curr".
----------------------------------------------------------------------------"""    
def fetch_corr_stock_fx(i):
    import FEqBasketUtils
    F_BASKET_EXCEPT   = 'f_eq_basket_xcp'  
    
    try: CORR = FEqBasketUtils.get_corr_matrix(i)
    except F_BASKET_EXCEPT, msg: 
        raise Exception, msg
    
    if i.curr == i.strike_curr:
        raise Exception, "The option currency and the strike currency are the same! The option can not be quanto."
    curr_pair = i.curr.currency_pair(i.strike_curr.insid)
    
    corr_stock_fx = CORR.used_correlation(i.und_insaddr, curr_pair)
    if corr_stock_fx == 0.0:
        raise Exception, "The correlation between " + i.und_insaddr.insid + " and the currency pair " + curr_pair.name + " equals zero."
    return [corr_stock_fx, CORR.name]
    
"""----------------------------------------------------------------------------
get_discount_factor() 
    The function returns the discount factor for the settlement days, with 
    which the present value is multiplied.
----------------------------------------------------------------------------"""    
def get_discount_factor(i):
    exp_offset = i.exp_day.add_banking_day(i.curr, i.pay_day_offset)
    yc = i.used_yield_curve(i.curr)
    riskfree_rate_exp = yc.yc_rate(i.exp_day, exp_offset, 'Annual Comp', 'Act/365', 'Spot Rate')
    time_offset = i.exp_day.years_between(exp_offset, 'Act/365')
    return math.pow(1 + riskfree_rate_exp, -time_offset)


