""" SEQ_VERSION_NR = PRIME 2.8.1 """




"""----------------------------------------------------------------------------
MODULE
    FEqBarrierUtils - Common code for Barrier options.
    
    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

----------------------------------------------------------------------------"""
import ael
import math
import sys
from FEqUtilsPRIME import *

# Constants
F_DAYS_PER_YEAR = 365.25
F_EPSILON = 1e-12

# The timeseries where barrier monitor dates are stored.
F_BARRIER_TIMESERIES    = 'FBarrierMonitorDays' 
F_BARRIER_EXCEPT        = 'f_eq_barrier_xcp' 

# Barrier types
F_BARRIER_ARBITRARY            = 'Arbitrary'           
F_BARRIER_CONTINUOUS           = 'Continuous'
F_BARRIER_DAILY                = 'Daily'
F_BARRIER_MONTHLY              = 'Monthly'
F_BARRIER_WEEKLY               = 'Weekly'
F_BARRIER_YEARLY               = 'Yearly'
F_BARRIER_DAILY_LAST_MONTH     = 'DailyLastMonth'
F_BARRIER_WEEKLY_LAST_MONTH    = 'WeeklyLastMonth'
F_BARRIER_DAILY_LAST_TWO_WEEKS = 'DailyLastTwoWeeks'

mon_freq_dict = {"Arbitrary":1, "Continuous":1, "Daily":1, "Monthly":1, "Weekly":1,
                 "Yearly":1, "DailyLastMonth":1, "WeeklyLastMonth":1, "DailyLastTwoWeeks":1}

exotic_type_dict = {"Down & Out":0,"Down & In":1, "Up & Out":2, "Up & In":3}

use_model_dict = {0:"Analytical",1:"Trinomial",2:"Smart",3:"Monte Carlo"}

"""----------------------------------------------------------------------------
get_exotic_number() 
    The function returns the a number corresponding to the barrier type chosen.
----------------------------------------------------------------------------"""    
def get_exotic_number(exotic_type):
    if exotic_type_dict.has_key(exotic_type):
        return exotic_type_dict[exotic_type]
    else:
        print "\n## !! EXCEPTION !! ##"
        raise  F_BARRIER_EXCEPT, 'No Barrier type given. Please specify one in the Exotic Type field.'
        
"""----------------------------------------------------------------------------
create_monitoring_dates() 
    The function returns a dictionary with the barrier monitoring dates and the 
    number of monitor dates.
----------------------------------------------------------------------------"""    
def create_monitoring_dates(discrete_barrier, monitor_freq, monitor_days, valuation_date, texp, exp_day):
    if monitor_freq == 0: 
        msg = "No Barrier Monitor Frequency is chosen. Choose frequency in the additional info field 'FBarrierMonitorFrq'."
        return {"barrier_mon_times":msg,"barrier_mon_dates":msg}
    monitor_days = AsList(monitor_days)
    barrier_dates = []
    if discrete_barrier:
        # The barrier is discrete.
        if monitor_freq == F_BARRIER_ARBITRARY and len(monitor_days) == 0:
            print "\n## !! NO VALUE !! ##"
            raise  F_BARRIER_EXCEPT, "No Monitor Days are given even though Arbitrary monitor frequency is chosen."
        if len(monitor_days) != 0: monitor_days.sort()
        else:
            # Periodic monitoring dates. Time series is not used, but valuation 
            # function expects a list of dates. Generate such a list.
            monitor_days = []
            if monitor_freq == F_BARRIER_DAILY:
                period = '1d';d = valuation_date
            elif monitor_freq == F_BARRIER_WEEKLY:
                period = '-1w'; d = exp_day
            elif monitor_freq == F_BARRIER_MONTHLY:
                period = '-1m';d = exp_day
            elif monitor_freq == F_BARRIER_YEARLY:
                period = '-1y';d = exp_day
            elif monitor_freq == F_BARRIER_DAILY_LAST_MONTH:
                period = '1d'
                if exp_day > valuation_date.add_period('1m'): 
                    d = exp_day.add_period('-1m')
                else: d = valuation_date
            elif monitor_freq == F_BARRIER_WEEKLY_LAST_MONTH:
                period = '1w'; d = exp_day.add_period('-1m')
            elif monitor_freq == F_BARRIER_DAILY_LAST_TWO_WEEKS:
                period = '1d'
                if (exp_day > valuation_date.add_period('2w')):
                    d = exp_day.add_period('-2w')
                else: d = valuation_date
            else:
                #Assuming a valid period
                try:        
                    tmp = valuation_date.add_period(monitor_freq)
                    period = monitor_freq; d = valuation_date
                except:
                    raise F_BARRIER_EXCEPT, "The period " + monitor_freq + " is invalid. Must be '1d', '1w', '1m', '1y' or another valid period."
            
            # Generate list of dates. 
            while valuation_date <= d <= exp_day:
                # A date should never be after expiry day or before today.
                date = d
                if valuation_date <= date <= exp_day:
                    # Do not insert doubles
                    if len(monitor_days) == 0 or monitor_days[0][0] <> date:                           
                        monitor_days.append((date, -1))
                d = d.add_period(period)
            
            # The list must be sorted:
            if d < valuation_date: monitor_days.reverse()
            
        # Transform the dates to be measured in years from today.. 
        barrier_dates_tmp = map(lambda x,start = valuation_date: \
                  (start.years_between(x[0], 'Act/365'), x[1]), monitor_days)

        for date_value in barrier_dates_tmp:
            # Build vector of future barrier dates
            if 0 <= date_value[0] <= texp: 
                barrier_dates.append(date_value[0])
            elif date_value[0] > texp:
                # Warning: A barrier date is after expiry in the time series
                # F_BARRIER_TIMESERIES, ignoring date.'
                pass
        barrier_monitoring_times = len(barrier_dates)
    else:
        barrier_monitoring_times = 0
    return {"barrier_mon_times":barrier_monitoring_times,"barrier_mon_dates":barrier_dates}

"""----------------------------------------------------------------------------
get_barrier_crossed() 
    The function returns the additional info value. Fetched in AEL to get real 
    time updates.
----------------------------------------------------------------------------"""    
def get_barrier_crossed_info(i,*rest):
    return i.add_info("FBarrier Crossed")
    
"""----------------------------------------------------------------------------
get_date() 
    The function returns an AEL date entity if the barrier has been crossed.
----------------------------------------------------------------------------"""    
def get_date(i,*rest):
    date_str = i.add_info("FBarrier Cross Date")
    if date_str != "":
        return ael.date_from_string(date_str)
    else: return date_str

"""----------------------------------------------------------------------------
is_valid_mon_freq() 
    The function checks the selected barrier monitor frequency.
----------------------------------------------------------------------------"""    
def is_valid_mon_freq(freq,insid=None):
    if mon_freq_dict.has_key(freq):
        return 1
    else:
        if insid != None: return 0
        print "\n## !! NO VALUE !! ##"
        raise F_BARRIER_EXCEPT, "No Barrier Monitor Frequency is chosen.Choose frequency in the additional info field 'FBarrierMonitorFrq'."


"""----------------------------------------------------------------------------
get_float_man_barrier() 
    The function converts the managment barrier (string) into a float.
----------------------------------------------------------------------------"""    
def get_float_man_barrier(man_barrier,trading=0,insid=None):
    if man_barrier == "": return 0
    try: man_barrier = float(man_barrier)
    except: 
        try:
            new_string = ''
            # Numbers > 10000 are represented as strings with ',', e.g. '10,000'.
            # This makes float throw a ValueError exception. Try to remedy the situation.
            if sys.exc_info()[0] == 'ValueError':
                try:
                    for char in second_barrier_str:
                        if not(char == ','):
                            new_string = new_string + char
                    man_barrier = float(new_string)
                except:
                    print "\n## !! EXCEPTION !! ##"
                    raise  F_BARRIER_EXCEPT, "The management barrier has not been set correctly. Choose a value in the AdditionalInfo field 'FBarrier RiskMan'."
            else:
                print "\n## !! EXCEPTION !! ##"
                raise  F_BARRIER_EXCEPT, "The management barrier has not been set correctly. Choose a value in the AdditionalInfo field 'FBarrier RiskMan'."
        except F_BARRIER_EXCEPT, msg:
            print '\nModule: FEqBarrierUtils'
            print 'Error : ', msg
            print 'Instr : ', insid
            return 0.0
    return man_barrier

"""----------------------------------------------------------------------------
get_float_second_barrier() 
    The function converts the second barrier (string) into a float.
----------------------------------------------------------------------------"""    
def get_float_second_barrier(second_barrier_str,trading=0,insid=None):
    try: second_barrier = float(second_barrier_str)
    except: 
        try:
            new_string = ''
            # Numbers > 10000 are represented as strings with ',', e.g. '10,000'.
            # This makes float throw a ValueError exception. Try to remedy the situation.
            if sys.exc_info()[0] == 'ValueError':
                try:
                    for char in second_barrier_str:
                        if not(char == ','):
                            new_string = new_string + char
                    second_barrier = float(new_string)
                except:
                    # There does not seem to be any valid second_barrier field
                    print "\n## !! NO VALUE !! ##"
                    raise  F_BARRIER_EXCEPT, "The second barrier has not been set correctly. Choose a value in the AdditionalInfo field FBarrier2."
            else:
                # There does not seem to be any valid second_barrier field
                print "\n## !! NO VALUE !! ##"
                raise  F_BARRIER_EXCEPT, "The second barrier has not been set correctly. Choose a value in the AdditionalInfo field FBarrier2."
        except F_BARRIER_EXCEPT, msg:
            print '\nModule: FEqBarrierUtils'
            print 'Error : ', msg
            print 'Instr : ', insid
            return 0.0
    return second_barrier

"""----------------------------------------------------------------------------
get_corr_stock_fx() 
    The function returns the correlation between the underlying asset and the 
    currency pair "Instrument curr / Strike curr".
----------------------------------------------------------------------------"""    
def get_corr_stock_fx(i,trading=0):
    try: 
        [corr, corr_name] = fetch_corr_stock_fx(i)
        return [corr, corr_name]
    except Exception, msg:
        if trading:return [msg, msg]
        else:
            print "\n## !! EXCEPTION !! ##"
            raise F_BARRIER_EXCEPT, msg
    

"""----------------------------------------------------------------------------
single_val_meth()
    The method returns the valuation method to use when valuing barrier options.
    
    Available valuation methods:
    
     - analytical
     - trinomial
     - Monte_Carlo
----------------------------------------------------------------------------"""    
def single_val_meth(dividends,discrete_barrier,barrier,barr_monitoring_times,barr_freq,price,texp,vol,use_model_enum,barrier_risk_man=0):
    try: float(barr_monitoring_times)
    except: return [barr_monitoring_times, barr_monitoring_times]
    if float(barrier_risk_man) != 0: barrier = float(barrier_risk_man)
    use_model = use_model_dict[use_model_enum]    
    if price == None: return [None, 0]
    dividends = AsList(dividends)
    
    val_meth = "analytical"; steps = 0
    if vol == None: return [val_meth, steps] 
    
    # Select a Monte Carlo valuation
    #val_meth = "Monte_Carlo"; steps = 1000
    
    if use_model   == "Analytical": return [val_meth, steps]
    elif use_model == "Trinomial": val_meth = "trinomial"
    elif use_model == "Monte Carlo": 
        val_meth = "Monte_Carlo"
        steps = 10000
        return [val_meth, steps]
    else: 
        n_divs = len(dividends)
        if n_divs > 0: val_meth = "trinomial"
    
    # Approximation condition
    appr_cond = 2
    if discrete_barrier:
        if not(barrier <= 0.0 or price == 0.0 or texp == 0.0 or vol == 0.0): 
            d = abs(math.log(barrier/price)* \
                    math.sqrt(barr_monitoring_times / texp) / vol)
            if d < appr_cond or \
                not(barr_freq == F_BARRIER_DAILY or barr_freq == F_BARRIER_WEEKLY):
                val_meth = "trinomial"
    if val_meth == "trinomial":
        if not texp <= 0.0:
            steps = min(max(math.ceil(600*vol*math.sqrt(texp)), 30), 300)
        else: steps = min(max(math.ceil(600*vol), 30), 300)
        if barrier != 0.0:
            dist_to_barrier = abs(barrier-price)/(barrier*1.0)
            if dist_to_barrier != 0.0:
                steps = steps * max(1, min(3, math.ceil(0.1/dist_to_barrier)))
        
        # The following criteria makes certain that a price shift never makes 
        # the option price be less than zero. This means there will be no jumps when 
        # the underlying price approaches the barrier. However, there is no cap on 
        # this number of time steps. When the value is very large, performance will
        # be affected. 
        #if not discrete_barrier:
            #n = 1.5*texp*pow(vol/math.log(price/barrier),2)
    return [val_meth, steps]

"""----------------------------------------------------------------------------
double_val_meth()
    The method returns the valuation method to use when valuing double barrier 
    options.
    
    Available valuation methods:
        
     - analytical
     - trinomial
     - Monte_Carlo
----------------------------------------------------------------------------"""    
def double_val_meth(dividends, discrete_barrier, barrier, barr_monitoring_times, barr_freq, second_barrier, price, texp, vol, use_model_enum):
    use_model = use_model_dict[use_model_enum]    
    if price == None: return {"val_meth":None ,"steps":0}
    dividends = AsList(dividends)
    
    val_meth = "analytical";steps = 0
    if vol == None: return [val_meth, steps] 
    # Select a Monte Carlo valuation
    #val_meth = "Monte_Carlo"; steps = 1000
    
    if use_model == "Analytical": return [val_meth, steps]
    elif use_model == "Trinomial": val_meth = "trinomial"
    elif use_model == "Monte Carlo": 
        val_meth = "Monte_Carlo"
        steps = 10000
        return [val_meth, steps]
    else: 
        n_div = len(dividends)
        if n_div > 0: val_meth = "trinomial"
    
    #Approximation condition:
    appr_cond = 3 
    if discrete_barrier:
        if not(price == 0.0 or texp == 0.0 or vol == 0.0): 
            if not(barrier <= 0.0): 
                d1 = abs(math.log(barrier/price)* \
                         math.sqrt(barr_monitoring_times / texp)/vol)
            else: d1 = appr_cond + 1
            if second_barrier != 0.0:
                d2 = abs(math.log(second_barrier/price)* \
                         math.sqrt(barr_monitoring_times / texp)/vol)
            else: d2 = appr_cond + 1
            if d1 < appr_cond or d2 < appr_cond or \
               not(barr_freq == F_BARRIER_DAILY or barr_freq == F_BARRIER_WEEKLY):
                val_meth = "trinomial"
    if val_meth == "trinomial":
        steps = min(max( math.ceil(800*vol*math.sqrt(texp)), 30), 300)
        if barrier != 0:
            dist_to_barrier = abs(barrier-price)/(barrier*1.0)
            if dist_to_barrier != 0.0:
                steps = steps * max(1, min(3, math.ceil(0.1/dist_to_barrier)))
    return [val_meth, steps]


"""----------------------------------------------------------------------------
ResultVal()
    The function checks the pricing result. If the result is erronous, a statement 
    is displayed in the AEL console.
----------------------------------------------------------------------------"""    
def ResultVal(pv, price):
    if pv >= -F_EPSILON: return max(pv, 0.0)
    print "\n## !! EXCEPTION !! ##"
    if pv == -1.0:
        if price <= 0.0: 
            raise F_BARRIER_EXCEPT, 'The initial asset price is less than or equal to zero.'
        else: 
            raise F_BARRIER_EXCEPT, 'The dividends size(s) are too large'
    elif pv == -2.0: 
        raise F_BARRIER_EXCEPT, "The number of timesteps are less than 3. The number must be raised."
    elif pv == -3.0: 
        raise F_BARRIER_EXCEPT, 'One or more of the following parameters are negative or equal to zero: the initial asset price, the barrier(s),the volatility or the strike price.'
    elif pv == -4.0: 
        raise F_BARRIER_EXCEPT, 'The barrier option valuation does not handle American barrier options.'
    elif pv == -5.0: 
        raise F_BARRIER_EXCEPT, 'The optionparameter call/put must be defined.'
    elif pv == -6.0: 
        raise F_BARRIER_EXCEPT, 'The optionparameter up-and-out/ up-and-in/ down-and-out/ down-and-in must be defined.'
    elif pv == -7.0: 
        raise F_BARRIER_EXCEPT, 'The upper barrier is equal to the lower barrier.'
    elif pv == -8.0: 
        raise F_BARRIER_EXCEPT, 'The barrier option valuation does not handle the valuation method in question.'
    elif pv == -9.0:
        raise F_BARRIER_EXCEPT, 'The fixed exchange rate is negative.'
    elif pv == -10.0:
        raise F_BARRIER_EXCEPT, 'The absolute value of the correlation is strictly greater than 1.'
    elif pv == -11.0:
        raise F_BARRIER_EXCEPT, 'The volatility of the foreign exchange rate is negative.'
    elif pv == -12.0:
        raise F_BARRIER_EXCEPT, 'Unknown quanto barrier type ("Barrier","DigitalBarrier","DoubleBarrier" or "DigitalDoubleBarrier").'
    else: 
        raise F_BARRIER_EXCEPT, 'Negative result. Unknown valuation exception.'

"""----------------------------------------------------------------------------
mult_with_df()
    The function multiplies the result with a settlement discount factor.
----------------------------------------------------------------------------"""    
def mult_with_df(res, df):
    if str(type(res)) == "<type 'dict'>" or str(type(res)) == "<type 'dictionary'>":
        if has_greeks(res):
            for key in res.keys():
                res[key] = res[key] * df
        else: res['PV'] = res['PV'] * df
    else: res = res * df
    return res
    
"""----------------------------------------------------------------------------
get_expiry_greeks()
    The function calculates the greeks when the barrier rebate should be paid
    on expiry..
----------------------------------------------------------------------------"""    
def get_expiry_greeks(pv, rebate, rate, texp, res_rebate, res_barrier):
    return_greeks = has_greeks(res_rebate)
    t_fact = 1.0/F_DAYS_PER_YEAR*rebate*rate*math.exp(-rate*texp)

    if return_greeks:
        delta = res_barrier['Delta'] - res_rebate['Delta'] 
        gamma = res_barrier['Gamma'] - res_rebate['Gamma'] 
        theta = res_barrier['Theta'] - res_rebate['Theta'] + t_fact
    else:
        delta = -1; gamma = -1; theta = -1
    return {'PV':pv, 'Delta':delta, 'Gamma':gamma, 'Theta':theta}

"""----------------------------------------------------------------------------
get_expiry_pv()
    The function calculates the pv for a barrier option where the rebate should
    be paid on expiry.
----------------------------------------------------------------------------"""    
def get_expiry_pv(single, bp, val_meth_params):
    [val_meth, steps] = val_meth_params
    if single:
        if bp.barrier_type_nbr == 1 or bp.barrier_type_nbr == 2: bp.upperb = 0 
        else: bp.upperb = 1
        
        if bp.fix_fx:
            res_barrier = ael.eq_quanto_barrier(bp, val_meth, steps, "Barrier")
            res_rebate = ael.eq_quanto_barrier(bp, val_meth, steps, "DigitalBarrier")
            bp.rebate = bp.rebate * bp.fx_rate
        else:
            res_barrier = ael.eq_barrier2(bp.price, bp.texp, bp.vol, bp.rate, bp.carry_cost, bp.strike,
                                 bp.put_call, bp.eur_ame, bp.dividends, bp.barrier_type_nbr, bp.barrier,
                                 0, steps, val_meth, bp.discrete_barr, bp.barr_monitoring_times, bp.barr_dates)
        
            res_rebate =  ael.eq_digital_barrier(bp.price, bp.texp, bp.vol, bp.rate, bp.carry_cost, bp.barrier,
                                  bp.upperb, bp.dividends, 0, bp.rebate, steps, val_meth, bp.discrete_barr,
                                  bp.barr_monitoring_times, bp.barr_dates)
    else:
        if bp.fix_fx:
            res_barrier = ael.eq_quanto_barrier(bp, val_meth, steps, "DoubleBarrier")
            res_rebate = ael.eq_quanto_barrier(bp, val_meth, steps, "DigitalDoubleBarrier")
            bp.rebate = bp.rebate * bp.fx_rate
        else:
            res_barrier = ael.eq_dblbarrier(bp.price, bp.texp, bp.vol, bp.rate, bp.carry_cost, bp.strike, bp.put_call,
                                 bp.eur_ame, bp.dividends, bp.barrier_type_nbr, bp.barrier, bp.second_barrier,
                                 0.0, steps, val_meth, bp.discrete_barr, bp.barr_monitoring_times, bp.barr_dates)
            res_rebate =  ael.eq_digital_dblbarrier(bp.price, bp.texp, bp.vol, bp.rate, bp.carry_cost, bp.barrier,
                                 bp.second_barrier, bp.dividends, 0, bp.rebate, steps, val_meth, bp.discrete_barr,
                                 bp.barr_monitoring_times, bp.barr_dates)
                                                
    pv = ResultVal(res_barrier['PV'], bp.price) + bp.rebate*math.exp(-bp.rate*bp.texp) - ResultVal(res_rebate['PV'], bp.price)
    
    return get_expiry_greeks(pv, bp.rebate, bp.rate, bp.texp, res_rebate, res_barrier)
        
"""----------------------------------------------------------------------------
get_digital_expiry_pv()
    The function calculates the pv for a digital barrier option where the 
    rebate should be paid on expiry.
----------------------------------------------------------------------------"""    
def get_digital_expiry_pv(single, bp, val_meth_params):
    [val_meth, steps] = val_meth_params
    if single:
        if bp.barrier_type_nbr == 1 or bp.barrier_type_nbr == 2:bp.upperb = 0
        else: bp.upperb = 1
        
        if bp.fix_fx:
            res_rebate = ael.eq_quanto_barrier(bp, val_meth, steps, "DigitalBarrier")
            bp.rebate = bp.rebate * bp.fx_rate
        else:
            res_rebate =  ael.eq_digital_barrier(bp.price, bp.texp, bp.vol, bp.rate, bp.carry_cost, bp.barrier,
                                 bp.upperb, bp.dividends, 0, bp.rebate, steps, val_meth, bp.discrete_barr,
                                 bp.barr_monitoring_times, bp.barr_dates)
    else:
        if bp.fix_fx:
            res_rebate = ael.eq_quanto_barrier(bp, val_meth, steps, "DigitalDoubleBarrier")        
            bp.rebate = bp.rebate * bp.fx_rate
        else:
            res_rebate = ael.eq_digital_dblbarrier(bp.price, bp.texp, bp.vol, bp.rate, bp.carry_cost, bp.barrier,
                                bp.second_barrier, bp.dividends, 0, bp.rebate, steps, val_meth, bp.discrete_barr,
                                bp.barr_monitoring_times, bp.barr_dates)
                                
    pv = bp.rebate*math.exp(-bp.rate*bp.texp) - ResultVal(res_rebate['PV'], bp.price) 
    res_barrier = {'Delta':0.0, 'Gamma':0.0, 'Theta':0.0}
    return get_expiry_greeks(pv, bp.rebate, bp.rate, bp.texp, res_rebate, res_barrier)

         
"""----------------------------------------------------------------------------
get_pv()
    The function returns either the present value or a dictionary with the present
    value and the greeks delta, gamma and theta for a barrier option. 
----------------------------------------------------------------------------"""    
def get_pv(bp, val_meth_params):
    [val_meth, steps] = val_meth_params
    if bp.texp < 0.0: return 0.0
    if bp.digital:
        if bp.eur_ame:
            print "\n## !! EXCEPTION !! ##"
            raise F_BARRIER_EXCEPT, 'American digital barrier options are not handled.'
        
        if bp.barrier_type_nbr == 1:
            bp.upperb = 0 ; bp.knock_in = 0
        elif bp.barrier_type_nbr == 2:
            bp.upperb = 0;bp.knock_in = 1
        elif bp.barrier_type_nbr == 3:
            bp.upperb = 1; bp.knock_in = 0
        else:
            bp.upperb = 1;bp.knock_in = 1
        
        if bp.knocked != "Yes":
            if bp.settlement == "Physical Delivery":
                # A digital knock in option => American asset or nothing digital
                if bp.barrier_type_nbr == 2:
                    bp.rebate = bp.barrier
                    if bp.price <= bp.barrier: return bp.price
                elif bp.barrier_type_nbr == 4:
                    bp.rebate = bp.barrier
                    if bp.price >= bp.barrier: return bp.price
            
            if bp.pay_rebate == "Expiry" and (bp.barrier_type_nbr == 2 or bp.barrier_type_nbr == 4): 
                res = get_digital_expiry_pv(1, bp, val_meth_params)
            else:
                if bp.fix_fx:
                    res = ael.eq_quanto_barrier(bp, val_meth, steps, "DigitalBarrier")
                else:
                    res = ael.eq_digital_barrier(bp.price, bp.texp, bp.vol, bp.rate, bp.carry_cost,
                                        bp.barrier_man, bp.upperb, bp.dividends, bp.knock_in, bp.rebate,
                                        steps, val_meth, bp.discrete_barr, bp.barr_monitoring_times,
                                        bp.barr_dates)
            pv = ResultVal(res['PV'], bp.price)
            res['PV'] = pv
        else: 
            # "Down & out" or "Up & out"
            if bp.barrier_type_nbr == 1 or bp.barrier_type_nbr == 3:res = 0
            else:
                if bp.settlement == "Physical Delivery": 
                    # A digital knock in option => American asset or nothing digital
                    res = bp.price
                else: 
                    res = bp.rebate * math.exp(bp.rate * bp.time_from_knocked)
    else:
        if bp.knocked != "Yes":
            if bp.pay_rebate == "Expiry" and (bp.barrier_type_nbr == 1 or bp.barrier_type_nbr == 3): 
                res = get_expiry_pv(1, bp, val_meth_params)
            else: 
                if bp.fix_fx:
                    res = ael.eq_quanto_barrier(bp, val_meth, steps, "Barrier")
                else:
                    res = ael.eq_barrier2(bp.price, bp.texp, bp.vol, bp.rate, bp.carry_cost,
                                   bp.strike, bp.put_call, bp.eur_ame, bp.dividends,
                                   bp.barrier_type_nbr, bp.barrier_man, bp.rebate, steps,
                                   val_meth, bp.discrete_barr, bp.barr_monitoring_times,
                                   bp.barr_dates)
                pv = ResultVal(res['PV'], bp.price)
                res['PV'] = pv
        else:
            if bp.barrier_type_nbr == 1 or bp.barrier_type_nbr == 3: 
                if bp.pay_rebate == "Expiry":
                    res = bp.rebate * math.exp(-bp.rate * bp.texp)
                else: res = bp.rebate * math.exp(bp.rate * bp.time_from_knocked)
            else: 
                res = ael.eq_option(bp.price, bp.texp, bp.vol, bp.rate, bp.carry_cost,
                            bp.strike, bp.put_call, bp.eur_ame, bp.dividends)
                if res == -1:
                    print "\n## !! EXCEPTION !! ##"
                    raise F_BARRIER_EXCEPT, 'Unknown valuation error.'
    return mult_with_df(res, bp.df)

"""----------------------------------------------------------------------------
get_double_pv()
    The function returns either the present value or a dictionary with the present
    value and the greeks delta, gamma and theta for a double barrier option. 
----------------------------------------------------------------------------"""    
def get_double_pv(dbp, val_meth_params):
    [val_meth, steps] = val_meth_params
    if dbp.texp < 0.0: return 0.0
    if dbp.digital:
        if dbp.eur_ame:
            print "\n## !! EXCEPTION !! ##"
            raise F_BARRIER_EXCEPT, 'American digital barrier options are not handled.'
        if dbp.barrier_type_nbr == 1 or dbp.barrier_type_nbr == 3:
            dbp.knock_in = 0
        else: dbp.knock_in = 1  
        if dbp.knocked != "Yes":
            if dbp.settlement == "Physical Delivery":
                # Asset or nothing digital.
                if dbp.barrier_type_nbr == 2 or dbp.barrier_type_nbr == 4:
                    dbp.rebate = dbp.barrier
                    # A digital knock in option => American asset or nothing digital
                    lower_barrier = min(dbp.barrier, dbp.second_barrier)
                    upper_barrier = max(dbp.barrier, dbp.second_barrier)
                    if dbp.price <= lower_barrier or dbp.price >= upper_barrier : 
                        return dbp.price

            if dbp.pay_rebate == "Expiry" and (dbp.barrier_type_nbr == 2 or dbp.barrier_type_nbr == 4): 
                res = get_digital_expiry_pv(0, dbp, val_meth_params)
            else:
                if dbp.fix_fx:
                    res = ael.eq_quanto_barrier(dbp, val_meth, steps, "DigitalDoubleBarrier")
                else:
                    res = ael.eq_digital_dblbarrier(dbp.price, dbp.texp, dbp.vol, dbp.rate,
                                   dbp.carry_cost, dbp.barrier, dbp.second_barrier, dbp.dividends, dbp.knock_in,
                                   dbp.rebate, steps, val_meth, dbp.discrete_barr,
                                   dbp.barr_monitoring_times, dbp.barr_dates)
                pv = ResultVal(res['PV'], dbp.price)
                res['PV'] = pv 
        else: 
            # "Down & out" or "Up & out"
            if dbp.barrier_type_nbr == 1 or dbp.barrier_type_nbr == 3:
                res = 0
            else:
                if dbp.settlement == "Physical Delivery": 
                    # A digital knock in option => American asset or nothing digital
                    res = dbp.price
                else: res = dbp.rebate * math.exp(dbp.rate * dbp.time_from_knocked)
    else:
        if dbp.knocked != "Yes":
            if dbp.pay_rebate == "Expiry" and (dbp.barrier_type_nbr == 1 or dbp.barrier_type_nbr == 3):
                res = get_expiry_pv(0, dbp, val_meth_params)
            else:
                if dbp.fix_fx:
                    res = ael.eq_quanto_barrier(dbp, val_meth, steps, "DoubleBarrier")
                else:                                                     
                    res = ael.eq_dblbarrier(dbp.price, dbp.texp, dbp.vol, dbp.rate, dbp.carry_cost, dbp.strike,
                                 dbp.put_call, dbp.eur_ame, dbp.dividends, dbp.barrier_type_nbr, dbp.barrier,
                                 dbp.second_barrier, dbp.rebate, steps, val_meth, dbp.discrete_barr,
                                 dbp.barr_monitoring_times, dbp.barr_dates)
                pv = ResultVal(res['PV'], dbp.price)
                res['PV'] = pv 
        else:
            if dbp.barrier_type_nbr == 1 or dbp.barrier_type_nbr == 3: 
                if dbp.pay_rebate == "Expiry":
                    res = dbp.rebate * math.exp(-dbp.rate * dbp.texp)
                else:
                    res = dbp.rebate * math.exp(dbp.rate * dbp.time_from_knocked) 
            else: 
                res = ael.eq_option(dbp.price, dbp.texp, dbp.vol, dbp.rate, dbp.carry_cost,
                            dbp.strike, dbp.put_call, dbp.eur_ame, dbp.dividends)
                if res == -1:
                    print "\n## !! EXCEPTION !! ##"
                    raise F_BARRIER_EXCEPT, 'Unknown valuation error.'
    return mult_with_df(res, dbp.df)










