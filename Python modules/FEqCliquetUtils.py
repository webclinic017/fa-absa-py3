""" SEQ_VERSION_NR = PRIME 2.8.1 """




"""-----------------------------------------------------------------------------
MODULE
    FEqCliquetUtils - Forward Start and Cliquet options common code for ATLAS and 
                      PRIME.
        
    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
   
NOTE
   At the forward start day, the strike price must be manually set in the 
   Instrument definition window. 

-----------------------------------------------------------------------------"""
import ael
from FEqUtilsPRIME import *
import math
import sys

F_CLIQUET_EXCEPT = 'f_eq_cliquet_fwdstart_xcp'
F_CLIQUET_END = 'Cliquet End'
F_CLIQUET_GO  = 'Cliquet Go'


"""-----------------------------------------------------------------------------
convert_alpha()
    The function converts a string alpha (AddInfo) to a float.
-----------------------------------------------------------------------------"""
def convert_alpha(alpha_str):
    alpha = 1
    try:
        if sys.version[0] == '1':
            import string
            for ch in [",", " ", "'", "`", '"']:
                if string.find(alpha_str, ch, 0) >= 0:
                    alpha_str = string.joinfields(string.splitfields(alpha_str, ch), "")
        else:
            for ch in [",", " ", "'", "`", '"']:
                if alpha_str.find(ch, 0) >= 0:
                    alpha_str = "".join(alpha_str.split(ch))
        alpha = float(alpha_str)
    except: 
        print "\n## !! NO VALUE !! ##"
        raise F_CLIQUET_EXCEPT, "No 'FFwdStartAlpha' found."
    return alpha


"""-----------------------------------------------------------------------------
convert_start_day()
    The function converts a string date (AddInfo) to an AEL date entity.
-----------------------------------------------------------------------------"""
def convert_start_day(start_day_str,trading = 0):
    start_day = ael.date_valueday()
    try: start_day = ael.date_from_string(start_day_str)
    except: 
        if trading: return "No forward start day is given. Please update the field 'FFwdStartDay'"
        print "\n## !! NO VALUE !! ##"
        raise F_CLIQUET_EXCEPT, "No forward start day is given. Please update the field 'FFwdStartDay'"
    return start_day  


"""-----------------------------------------------------------------------------
get_reset_dates()
    The function creates lists with reset dates. Arrays are returned also for
    forward start options.
-----------------------------------------------------------------------------"""
def get_reset_dates(reset_dates_tot,price,mapped_module,valuation_date,exp_day,trading=0,insid=None):
    try:
        if reset_dates_tot == (): 
            return ['No TimeSeries is created!', 'No TimeSeries is created!', 'No TimeSeries is created!', 'No TimeSeries is created!', []]
        
        # Determine whether or not the first reset day alredy has occured:
        if reset_dates_tot[0][0] < valuation_date:
            first_reset_occured = 1
        else: first_reset_occured = 0

        # Computing the reset_dates, reset_prices:
        reset_dates  = []
        reset_prices = []
        last_reset_price = -1.0
        for date_price in reset_dates_tot:
            if date_price[0] < valuation_date:
            # Extract the last reset prices:
            # First dealing with the case if any reset day is between today and the 
            # valuation date. In this case we let the reset price be equal to todays  
            # price of the underlying asset.
                if date_price[0] >= ael.date_today():
                    reset_prices.append(price) 
                else:
                    if date_price[1] < 0.0:
                        if mapped_module == "FEqCliquet.pv":
                            if trading: 
                                return ['Negative cliquet resets!', 'Negative cliquet resets!', 'Negative cliquet resets!', 'Negative cliquet resets!', [0]]
                            print "\n## !! TIMESERIES EXCEPTION !! ##"
                            raise F_CLIQUET_EXCEPT, 'One reset price is negative for the instrument.'
                        else:
                            if trading:
                                return ['Negative strike price!', 'Negative strike price!', 'Negative strike price!', 'Negative strike price!', [0]]
                            print "\n## !! EXCEPTION !! ##"
                            raise F_CLIQUET_EXCEPT, 'The strike price is negative for the instrument.'
                    else:
                        reset_prices.append(date_price[1])
                last = date_price
            elif date_price[0] >= valuation_date: 
                if reset_dates == []:
                    if first_reset_occured:
                        reset_dates.append(last[0]) 
                        reset_dates.append(date_price[0])
                        last_reset_price = reset_prices[-1]
                    elif date_price[0] < exp_day:
                        reset_dates.append(date_price[0])
                    elif date_price[0] >= exp_day:
                        if mapped_module == "FEqCliquet.pv":
                            #print F_CLIQUET_WARNING,'One reset day , ',date_price[0],', is at or later than the expiry date, this reset day is removed.'
                            pass
                        else: 
                            if trading:
                                return ['Forward start day after expiry!', 'Forward start day after expiry!', 'Forward start day after expiry!', 'Forward start day after expiry!', [0]]
                            print "\n## !! TIMESERIES EXCEPTION !! ##"
                            raise F_CLIQUET_EXCEPT, 'The forward start day , ' + str(date_price[0]) + ', is at or later than the expiry date. '
                elif (date_price[0] < exp_day) and (date_price[0] <> reset_dates[-1]):
                    reset_dates.append(date_price[0])
                elif date_price[0] == reset_dates[-1]:
                    #print F_CLIQUET_WARNING,'Some reset days are given twice.'
                    pass
                elif date_price[0] >= exp_day:
                    if mapped_module == "FEqCliquet.pv":
                        #print F_CLIQUET_WARNING,'One reset day, ',date_price[0],', is at or later than the expiry date, this reset day is removed.'
                        pass
                    else: 
                        if trading:
                            return ['Forward start day after expiry!', 'Forward start day after expiry!', 'Forward start day after expiry!', 'Forward start day after expiry!', [0]]
                        print "\n## !! EXCEPTION !! ##"
                        raise F_CLIQUET_EXCEPT, 'The forward start day , '+ str(date_price[0]) + ', is at or later than the expiry date.'

        # Handling the case if all the reset days are before the valuation date.
        if (reset_dates == []) and first_reset_occured:
            reset_dates.append(last[0])
            if last[0] >= ael.date_today():
                last_reset_price = price  
            else:
                if last[1] < 0.0:
                    if mapped_module == "FEqCliquet.pv": x = 'reset price'
                    else: x = 'strike price'
                    if trading: 
                        return ['Negative ' + str(x) + '!', 'Negative ' + str(x) + '!', 'Negative ' + str(x) + '!', 'Negative ' + str(x) + '!', [0]]
                    else:
                        print "\n## !! VALUE EXCEPTION !! ##"
                        raise F_CLIQUET_EXCEPT, 'Negative ' + str(x) + ' for the instrument ' + i.insid
                else:
                    last_reset_price = last[1]

        if reset_dates == []:
            print "\n## !! VALUE EXCEPTION !! ##"
            if mapped_module == "FEqCliquet.pv":
                pass
                #raise F_CLIQUET_EXCEPT,"One reset day, " + str(date_price[0]) + ", is at or later than the expiry date."
            else: 
                if trading:
                    return ['Forward start day after expiry!', 'Forward start day after expiry!', 'Forward start day after expiry!', 'Forward start day after expiry!', [0]]
                print "\n## !! TIMESERIES EXCEPTION !! ##"
                raise F_CLIQUET_EXCEPT, 'The forward start day , ' + str(date_price[0]) + ', is at or later than the expiry date. '

        # Finally, add the expiry time to the reset dates:
        reset_dates.append(exp_day)

        # Computing the reset_times
        reset_times = []    
        for date in reset_dates:       
            reset_times.append(valuation_date.years_between(date, 'Act/365'))
        return [first_reset_occured, reset_dates, reset_prices, last_reset_price, reset_times]
    except F_CLIQUET_EXCEPT, msg:
        if trading:
            print '\nModule:  FEqCliquetUtils'
            print 'Error : ', msg
            print 'Instr : ', insid
            return []
        else:
            raise F_CLIQUET_EXCEPT, msg
            
"""-----------------------------------------------------------------------------
get_carry_cost()
    The function returns the carry cost for each reset dates. Special handling if 
    the underlying instrument is a currency.
-----------------------------------------------------------------------------"""
def get_carry_cost(und_instype, reset_dates, yc_repo, valuation_date, rate):
    if und_instype == 'Stock' or und_instype == 'EquityIndex':
        for date in reset_dates[1:]:
            repo = yc_repo.yc_rate(valuation_date, date, 'Continuous', 'Act/365', 'Spot Rate')
            texp_carry = valuation_date.years_between(date, 'Act/365')
            temp = valuation_date.years_between(date, 'Act/365')
            self.carry_cost.append(repo)
    # The underlying is a currency.
    else:
        j = 0;
        yc_und_rate = i.und_insaddr.used_repo_curve(i.und_insaddr.curr)
        for date in self.reset_dates[1:]:
            und_rate = yc_und_rate.yc_rate(valuation_date, date, 'Continuous', 'Act/365', 'Spot Rate')
            carry_cost.append((rate[j]-und_rate))
            j = j+1
    return carry_cost

"""----------------------------------------------------------------------------
get_cliquet_vola
    The function returns a vector with all cliquet volatilities
----------------------------------------------------------------------------"""    
def get_cliquet_vola(first_vola, vola_array, reset_dates):
    cliquet_vol = [first_vola]
    j = 2
    for date in reset_dates[2:]:
        sigma_fwd = vola_array[j-1]
        sigma_exp = vola_array[j]
        fvol = forward_vol(sigma_fwd, sigma_exp, ael.date_valueday(), reset_dates[j-1], date)
        cliquet_vol.append(fvol)
        j = j + 1
    return cliquet_vol


"""-----------------------------------------------------------------------------
forward_vol()
    The function returns a forward volatility for the period between the forward
    start day and expiry.
-----------------------------------------------------------------------------"""
def forward_vol(sigma_fwd, sigma_exp, valuation_date, fwd_date, exp_date):
    time_to_fwd = valuation_date.years_between(fwd_date, 'Act/365')
    time_to_exp = valuation_date.years_between(exp_date, 'Act/365')
    if time_to_fwd == 0 or time_to_fwd == 0: return sigma_exp
    elif time_to_fwd == time_to_exp: return sigma_exp
    try: 
        if sigma_exp == 0.0 or sigma_fwd == 0.0: return 0.0
        float(sigma_exp);float(sigma_fwd)
    except: return 0.0
    if time_to_fwd > 0:
        sigma_square = (pow(sigma_exp, 2)*time_to_exp - pow(sigma_fwd, 2)*time_to_fwd)/(time_to_exp-time_to_fwd)
        if sigma_square >= 0:
            sigma = math.sqrt(sigma_square)
        else: sigma = 0.0
    else: sigma = sigma_exp     
    return sigma
    
"""-----------------------------------------------------------------------------
fwdstart_val_meth()
    The method returns the valuation method to use when valuing cliquet and 
    forward start options. 
    One can choose between 
        - "analytical"  For analytical formulas
        - "trinomial"   For trinomial formulas
        - "MonteCarlo"  Monte Carlo simulations
-----------------------------------------------------------------------------"""
def fwdstart_val_meth(dividends):
    val_meth = "analytical" 
    steps = 0.0
      #if len(dividends) > 0:
      #val_meth = "trinomial"
      #steps = 10
    return [val_meth, steps]


"""-----------------------------------------------------------------------------
ResultVal()
    The function checks the result. If the result is erronous, an exception is 
    thrown.
-----------------------------------------------------------------------------"""
def ResultVal(res):
    if res < 0.0:         
        print "\n## !! EXCEPTION !! ##"
        if res == -1.0:
            raise F_CLIQUET_EXCEPT, 'The initial asset price is negative.'
        elif res == -2.0:
            raise F_CLIQUET_EXCEPT, 'The dividends size(s) are too large.'
        elif res == -3.0:
            raise F_CLIQUET_EXCEPT, 'The variable type is boolean.'
        elif res == -4.0:
            raise F_CLIQUET_EXCEPT, 'The number of trinomial steps < 3.'
        elif res == -5.0:
            raise F_CLIQUET_EXCEPT, 'Unknown pricing method.'
        elif res == -6.0:
            raise F_CLIQUET_EXCEPT, 'The reset day and the expiry day coincide.'
        elif res == -7.0:
            raise F_CLIQUET_EXCEPT, 'The last reset price is negative.'
        elif res == -8.0:
            raise F_CLIQUET_EXCEPT, 'The volatility is negative.'
        elif res == -9.0:
            raise F_CLIQUET_EXCEPT, 'The forward start alpha is negative.'
        elif res == -10.0:
            #the option has already expired#
            res = 0.0
        elif res == -11.0:
            raise F_CLIQUET_EXCEPT, 'The number of dividends is negative.'
        elif res == -12.0:
            raise F_CLIQUET_EXCEPT, 'The reset price is equal to zero.'
        else:
            raise F_CLIQUET_EXCEPT, 'Negative output?'
    return res

"""-----------------------------------------------------------------------------
get_fwdstart_pv()
    The function returns the present value for a forward start option.
-----------------------------------------------------------------------------"""
def get_fwdstart_pv(fp, val_meth_params):
    [val_meth, steps] = val_meth_params
    
    res = ael.eq_fwdstart(fp.price,
            fp.reset_times[1], fp.vol[0], fp.rate[0],
            fp.carry_cost[0], fp.put_call, fp.dividends, fp.performance,
            steps, val_meth, fp.reset_times[0], fp.last_reset_price,
            fp.alpha)

    res = ResultVal(res)
    if fp.performance and fp.reset_times[0] < 0:
        res = res * fp.price
    return res * fp.df[0]

"""-----------------------------------------------------------------------------
cliquet_pv()
    The function returns the present value for a cliquet option.
-----------------------------------------------------------------------------"""
def cliquet_pv(cp, val_meth_params):
    res = 0.0
    # The option is a cliquet pay in the end
    if cp.cliquet_type ==  F_CLIQUET_END:
        fi = -1+2*(cp.put_call==1)
        rate_exp = cp.rate[-1]
        discount_exp = math.exp(-cp.texp*rate_exp)
        df_exp = cp.df[-1]
        if cp.first_reset_occured:
            reset_price = cp.reset_prices[0]
            if reset_price <= 0.0:
                print "\n## !! EXCEPTION !! ##"
                raise F_CLIQUET_EXCEPT, 'The reset price is less than or equal to zero.'
            for maturity_price in cp.reset_prices[1:]:
                if maturity_price <= 0.0:
                    print "\n## !! EXCEPTION !! ##"
                    raise F_CLIQUET_EXCEPT, 'The reset price is less than or equal to zero.'
                payoff = fi*(maturity_price - cp.alpha*reset_price)
                if payoff > 0.0:
                    res = res + df_exp*discount_exp*payoff/reset_price 
                reset_price = maturity_price

        [val_meth, steps] = val_meth_params
        nr_of_resets = len(cp.reset_times)-1

        for i in range(nr_of_resets):
            part_res = ael.eq_fwdstart(cp.price,
                        cp.reset_times[i+1], cp.vol[i], cp.rate[i],
                        cp.carry_cost[i], cp.put_call, cp.dividends, cp.performance,
                        steps, val_meth, cp.reset_times[i], cp.last_reset_price,
                        cp.alpha)

            if part_res < 0.0:
                res = ResultVal(res)
            else:
                inv_discount_reset = math.exp(cp.rate[i]*cp.reset_times[i+1])
                # Compensate for the fact the payoff is at the expiry date and
                # not at the reset date.
                res = res + df_exp*inv_discount_reset*discount_exp*part_res
    # The option is a cliquet pay as you go
    elif cp.cliquet_type == F_CLIQUET_GO:
        res = 0.0
        [val_meth, steps] = val_meth_params

        nr_of_resets = len(cp.reset_times)-1
        for i in range(nr_of_resets):
            part_res = ael.eq_fwdstart(cp.price,
                        cp.reset_times[i+1], cp.vol[i], cp.rate[i],
                        cp.carry_cost[i], cp.put_call, cp.dividends, cp.performance,
                        steps, val_meth, cp.reset_times[i], cp.last_reset_price,
                        cp.alpha)

            part_res = ResultVal(part_res)
            res = res + cp.df[i]*part_res
    return res

















