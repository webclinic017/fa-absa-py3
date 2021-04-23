""" SEQ_VERSION_NR = PRIME 2.8.1 """




"""----------------------------------------------------------------------------
MODULE
    FEqAverageUtils - Help functions for average options.
        
    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    Help functions that can be used both by FEqAverage and FEqAveragePRIME
        
----------------------------------------------------------------------------"""
import ael
from FEqUtilsPRIME import *

F_AVERAGE_EXCEPT    = 'f_eq_average_xcp'
F_AVERAGE_FUTAVGVAL = -1                  # Value stored in timeseries for future average points
F_EPSILON           = 1e-16               # Machine accuracy
F_AVERAGE_MIN_NBR   = 15                  # The minimum number of monitoring dates for using 
                                          # continuous approximation.
 
AVERAGE_ARITH = 0;AVERAGE_GEOM = 1;AVERAGE_HARM = 2

##Support functions
def sumSeq(t) :return reduce(lambda x, y:x+y, t, 0) ## Adds all elements in a list
def mulSeq(t) :return reduce(lambda x, y:x*y, t, 1) ## Multiplies all elements in a list

"""----------------------------------------------------------------------------
get_asian_quanto_flag() 
    Returns 1 if the asian option is quanto. Otherwise, the function returns 0.
----------------------------------------------------------------------------"""
def get_asian_quanto_flag(fix_fx, strike_curr, option_curr):
    quanto_flag = 0
    if fix_fx and (strike_curr != option_curr):quanto_flag = 1
    return quanto_flag

"""----------------------------------------------------------------------------
get_corr_stock_fx()
    Returns the correlation between the stock and the FX rate (for singel 
    underlying). The FX rate is the rate strike curr / option curr.
----------------------------------------------------------------------------"""
def get_corr_stock_fx(i,trading = 0):
    try: 
        [corr, corr_name] = fetch_corr_stock_fx(i)
        return [corr, corr_name]
    except Exception, msg:
        if trading:return [msg, msg]
        else:
            print "\n## !! EXCEPTION !! ##"
            raise F_AVERAGE_EXCEPT, msg

"""----------------------------------------------------------------------------
get_fix_float() 
   Even average_type_number -> Fix   -> fix_float = 0 , 
   Odd average_type_number  -> Float -> fix_float = 1 
----------------------------------------------------------------------------"""
def get_fix_float(avg_option_type_number):    
    try:
        type_number = avg_option_type_number & 1
        return type_number
    except: return 'No Average option Type set!'

"""----------------------------------------------------------------------------
get_avg_price_dict() 
   The function returns dictionaries with average dates,both in the future and 
   in the past. It checks both the time series FAveragePrices and FAverageStrike.
----------------------------------------------------------------------------"""
def get_avg_price_dict(i,und_instrs,average_price_list,avgStrike,average_basket,avg_fwdstart,fwdstart_params,today,trading = 0):
    old_avgs_dict  = {}
    avg_dates_dict = {}
    avg_start_dict = {}
    avg_end_dict   = {}
    avgs_tmp_dict  = {}
    avg_dates      = []
    und_instrs = AsList(und_instrs)
    average_price_list = AsMatrix(average_price_list)
    j = 0
    for und_ins in und_instrs:
        if und_ins == 0:
            und_j = i.und_insaddr
        else: und_j = ael.Instrument[und_ins].insid
        avgs = average_price_list[j]
        avgs.sort()
        if avgs[len(avgs)-1][0] > i.exp_day:
            if trading: return 'There are average dates after the expiry date!'
            print "\n## !! EXCEPTION !! ##"
            raise F_AVERAGE_EXCEPT, 'There are average dates after the expiry date. Check the time series.'
        avg_start_dict[und_j] = avgs[0][0]
        avg_end_dict[und_j] = avgs[len(avgs)-1][0]
        avgs_tmp_dict[und_j] = map(lambda x,decr=today :(decr.years_between(x[0], 'Act/365'), x[1]), avgs)
        j = j + 1

    # Collect the average dates for the TimeSeries 'FAveragePrices'
    for key_date_vals in avgs_tmp_dict.items():
        und_ins  = key_date_vals[0]
        if not old_avgs_dict.has_key(und_ins):
            old_avgs_dict[und_ins]  = []
            avg_dates_dict[und_ins] = []
        no_avgs = len(key_date_vals[1])
        for date_val in key_date_vals[1]:
            if date_val[1] == F_AVERAGE_FUTAVGVAL:
                if date_val[0] < 0:
                    if today > ael.date_today():
                        if i.fix_fx:
                            try:   und_price = und_ins.used_price(None, und_ins.curr.insid)
                            except:und_price = ael.Instrument[und_ins].used_price(None, und_ins.curr.insid)
                        else: 
                            try:   und_price = und_ins.used_price(None, i.strike_curr.insid)
                            except:und_price = ael.Instrument[und_ins].used_price(None, i.strike_curr.insid)
                        
                        date_val = [date_val[0], und_price]
                        old_avgs_dict[und_ins].append((und_price, 1.0/no_avgs))
                    else:
                        if trading: return 'Average date in the past has got negative value!'
                        print "\n## !! EXCEPTION !! ##"
                        raise F_AVERAGE_EXCEPT, 'Time series error for the instrument. Average date in the past has got a negative value. Update it with the ASQL-application .AppAveragePrices.'
            else:
                if date_val[0] > 0:
                    try:
                        if today < ael.date_today():
                            date_val = [date_val[0], F_AVERAGE_FUTAVGVAL]
                        elif ael.historical_mode(): date_val = [date_val[0], F_AVERAGE_FUTAVGVAL]
                        else:
                            if trading: return 'Average future value should be -1!'
                            print "\n## !! EXCEPTION !! ##"
                            raise F_AVERAGE_EXCEPT, 'Time series error for the instrument. Average date in the future should have the value -1, not ' + str(date_val[1]) + ' Update it with the ASQL-application .AppAveragePrices.'
                    except F_AVERAGE_EXCEPT, msg:
                        raise F_AVERAGE_EXCEPT, msg
                    except: pass
                if date_val[0] == 0.0:
                    try: 
                        if ael.historical_mode(): date_val = [date_val[0], F_AVERAGE_FUTAVGVAL]
                    except: pass
                # Build vector of past averages, they will be summed later
                if date_val[1] != F_AVERAGE_FUTAVGVAL and date_val[0] < 0.0:
                    old_avgs_dict[und_ins].append((date_val[1], 1.0/no_avgs))
            avg_dates_dict[und_ins].append((date_val[0], 1.0/no_avgs))
            if not average_basket:
                avg_dates.append(date_val[0])

    # Collect the average dates for the TimeSeries 'FAverageStrike'
    if avgStrike != [] and avgStrike != ():
        avg_strike_tmp = map(lambda x,decr=today :(decr.years_between(x[0], 'Act/365'), x[1]), avgStrike)
        und_ins = i.und_insaddr.insid
        no_avgs = len(avg_strike_tmp)

        if not old_avgs_dict.has_key(und_ins):
            old_avgs_dict[und_ins]  = []
            avg_dates_dict[und_ins] = []
        for date_val in avg_strike_tmp:
            if date_val[1] == F_AVERAGE_FUTAVGVAL:
                if date_val[0] < 0:
                    if today > ael.date_today():
                        if i.fix_fx:
                            try:   und_price = und_ins.used_price(None, und_ins.curr.insid)
                            except:und_price = ael.Instrument[und_ins].used_price(None, und_ins.curr.insid)
                        else: 
                            try:   und_price = und_ins.used_price(None, i.strike_curr.insid)
                            except:und_price = ael.Instrument[und_ins].used_price(None, i.strike_curr.insid)

                        date_val = [date_val[0], und_price]
                        old_avgs_dict[und_ins].append((und_price, -1.0/no_avgs))
                    else:
                        if trading: return 'Average date in the past has got negative value!'
                        print "\n## !! EXCEPTION !! ##"
                        raise F_AVERAGE_EXCEPT, 'Time series error for the instrument. Average date in the past has got a negative value. Update it with the ASQL-application .AppAveragePrices.'
            else:
                if date_val[0] > 0:
                    if today < ael.date_today():
                        date_val = [date_val[0], F_AVERAGE_FUTAVGVAL]
                    else:
                        if trading: return 'Average future value should be -1!'
                        print "\n## !! EXCEPTION !! ##"
                        raise F_AVERAGE_EXCEPT, 'Time series error. Average date in the future should have the value -1, not ' + str(date_val[1]) + ' Update it with the ASQL-application .AppAveragePrices.'
                # Build vector of past averages, they will be summed later
                if date_val[1] != F_AVERAGE_FUTAVGVAL:
                    old_avgs_dict[und_ins].append((date_val[1], -1.0/no_avgs))
            avg_dates_dict[und_ins].append((date_val[0], -1.0/no_avgs))    

    for vec in avg_dates_dict.values():vec.sort()
    if avg_fwdstart != "":
        [fwdstart_time, fwdstart_alpha, strike] = fwdstart_params
        if fwdstart_time > avg_dates_dict[i.und_insaddr.insid][0][0]:
            if trading: return 'There are average dates before forward start date.'
            print "\n## !! EXCEPTION !! ##"
            raise F_AVERAGE_EXCEPT, 'There are average dates strictly before the forward start date.'
        avg_dates_dict[i.und_insaddr.insid].insert(0, (fwdstart_time, -fwdstart_alpha))
        if fwdstart_time < 0:
            old_avgs_dict[i.und_insaddr.insid].append((strike, -1))   
    if i.add_info('FAverageType') == "ArithmeticFloating" and not average_basket: 
        texp = today.years_between(i.exp_day, 'Act/365')
        avg_dates_dict[i.und_insaddr.insid].insert(len(avg_dates_dict[i.und_insaddr.insid])-1, (texp, -1))
    return [old_avgs_dict, avg_dates_dict, avg_start_dict, avg_end_dict, avg_dates]
    

"""----------------------------------------------------------------------------
get_avg_so_far() 
   The function returns a dictionary with averages for each underlying.
----------------------------------------------------------------------------"""
def get_avg_so_far(avg_option_type_number, old_avgs_keys, old_avgs_values, underlying):
    if str(type(old_avgs_values)) == "<type 'str'>":
        r = old_avgs_values
        return [r, r, r]
    avg_so_far_dict = {}
    if avg_option_type_number == 0 or avg_option_type_number == 1:
        # Arithmetic
        avg_type = AVERAGE_ARITH
        j = 0
        for key in old_avgs_keys:
            und_ins  = key
            old_avgs = old_avgs_values[j]
            if len(old_avgs) > 0 :
                avg_so_far_dict[und_ins] = average(old_avgs, AVERAGE_ARITH)
            else: avg_so_far_dict[und_ins] = 0
            j = j+1 

    elif avg_option_type_number == 2 or avg_option_type_number == 3:
        # Geometric
        avg_type = AVERAGE_GEOM
        j = 0
        for key in old_avgs_keys:
            und_ins  = key
            old_avgs = old_avgs_values[j]
            if len(old_avgs) > 0 :
                avg_so_far_dict[und_ins] = average(old_avgs, AVERAGE_GEOM)
            else: avg_so_far_dict[und_ins] = 0
            j = j+1
    elif avg_option_type_number == 4 or avg_option_type_number == 5:
        # Harmonic
        self.avg_type = AVERAGE_HARM
        print "\n## !! EXCEPTION !! ##"
        raise F_AVERAGE_EXCEPT, 'FAverageParams: HARMONIC not implemented'
    else:
        if str(type(avg_option_type_number)) == "<type 'str'>":
            a = avg_option_type_number
            return [a, a, a]
        print "\n## !! EXCEPTION !! ##"
        raise F_AVERAGE_EXCEPT, 'FAverageParams: Parameter error, FAverageType '
    if len(avg_so_far_dict) > 1:
        avg_so_far = 0
        stock_links = ael.CombinationLink.select('owner_insaddr='+str(underlying.insaddr))
        for stock_link in stock_links:
            stock  = stock_link.member_insaddr.insid
            weight = stock_link.weight
            if avg_so_far_dict.has_key(stock):
                avg_so_far = avg_so_far + weight*avg_so_far_dict[stock]
    else: avg_so_far = avg_so_far_dict.values()[0]
    return [avg_type, avg_so_far_dict, avg_so_far]

"""----------------------------------------------------------------------------
get_future_avgs() 
   The function returns lists with future dates and weights.
----------------------------------------------------------------------------"""
def get_future_avgs(avg_dates_weights_list, texp, avg_type_text, average_basket_flag):
    # Sorting out the asian dates/weights that are in the future
    
    fut_avg_dates = []
    fut_avg_weights = []
    for avg_dates_weights in avg_dates_weights_list:
        tmp1 = []; tmp2 = []
        for date_weights in avg_dates_weights:
            if 0 <= date_weights[0] <= texp + 0.0027:
                tmp1.append(date_weights[0])
                tmp2.append(date_weights[1])
        fut_avg_dates.append(tmp1)
        fut_avg_weights.append(tmp2)
    return [fut_avg_dates, fut_avg_weights]


"""----------------------------------------------------------------------------
get_mod_strike() 
   The function calculates the modified strike price, which is the strike price 
   minus the sum of the average prices obtained so far times the weights.
----------------------------------------------------------------------------"""
def get_mod_strike(average_basket, avg_fwd_start, avg_dates_values, strike, old_avgs_values, basket_weights, avg_type_text, avg_in):
    if str(type(old_avgs_values)) == "<type 'str'>": return old_avgs_values
    mod_strike = strike
    if average_basket:
        # Average baskets
        i = 0
        for weight_price_list in old_avgs_values:
            for weight_price_tuple in weight_price_list:
                mod_strike = mod_strike - \
                    basket_weights[i]*weight_price_tuple[0]*weight_price_tuple[1]
            i = i + 1
    elif avg_type_text == "ArithmeticFix" or avg_type_text == "ArithmeticFloating":
        if avg_type_text == "ArithmeticFloating" or avg_fwd_start != "" or avg_in != "":
            mod_strike = 0.0
        for weight_price_tuple in old_avgs_values[0]:
            mod_strike = mod_strike - weight_price_tuple[0]*weight_price_tuple[1]
    return mod_strike
  
  
"""----------------------------------------------------------------------------
val_meth() 
    The function determines the best valuation method for a specific asian option.

    Available valuation methods:
    
     ASIAN BASKET
     - MomentMatching
     - MomentMatchingContAppr
     - GentleVorst
     - MonteCarlo                   (minimum number of simulations = 100)

     ASIAN WITH SINGLE UNDERLYING
     - RogersShi                    
     - MomentMatching               (only for fixed strike)
     - MomentMatchingContAppr       (only for fixed strike)
     - Vorst                        (only for fixed strike)
     - MonteCarlo
     - MomentMatching2              (also for geometric average)

     FORWARD START AND AVERAGE IN ASIANS
     - RogersShi
     - MonteCarlo
----------------------------------------------------------------------------"""
def val_meth(average_basket,avg_dates_weights_list,avg_type_text,avg_fwd_start,avg_in,texp=None):
    nbr_of_sim = 0
    # ASIAN BASKET OPTION
    if average_basket: 
        frequently_monitoring = 1    
        for avg_dates_weights in avg_dates_weights_list:
            nbr_of_asian_dates = len(avg_dates_weights)
            if nbr_of_asian_dates < F_AVERAGE_MIN_NBR: 
                frequently_monitoring = 0
            else:    
                time_diff = avg_dates_weights[nbr_of_asian_dates-1][0]- avg_dates_weights[0][0]
                if (time_diff/(1.0*nbr_of_asian_dates)) > 1.0/40.0:
                    frequently_monitoring = 0
                    break
        # Frequently monitoring means that the asian dates are at least weakly
        if frequently_monitoring: val_meth = "MomentMatchingContAppr" 
        else: val_meth = "MomentMatching"
    # SINGLE UNDERLYING ASIAN OPTION
    else: 
        if avg_type_text == "GeometricFloating" or avg_type_text == "GeometricFix":
            	    val_meth = "MomentMatching2"
        else:
            if avg_in == "Yes" or avg_fwd_start != "":
                val_meth = "RogersShi" 
            elif avg_type_text == "ArithmeticFloating":
                val_meth = "RogersShi"
                #val_meth = "MomentMatching2"
            else:
                val_meth = "Vorst"
		#val_meth = "MomentMatching"
                #val_meth = "MomentMatching2"
    
    # For Monte Carlo, uncomment the following line.
    # [val_meth, nbr_of_sim] = ["MonteCarlo", 1000]
    return [val_meth, nbr_of_sim]


"""----------------------------------------------------------------------------
get_und_stock() 
    The function is called from ASQL .AppAveragePrices. If the asian option only
    has one underlying, the function returns the name of that instrument. If the
    underlying instrument is basket option the function returns the name of 
    the instrument that corresponds to the given insaddr (run_no).
----------------------------------------------------------------------------"""    
def get_und_stock(i,run_no,*rest):
    if run_no == 0.0: return i.und_insaddr.insid
    else: return ael.Instrument[run_no].insid

"""----------------------------------------------------------------------------
get_pv() 
    The function returns present value given an asian class with parameters.
----------------------------------------------------------------------------"""    
def get_pv(ap, val_meth_params):
    [val_meth, nbr_of_sim] = val_meth_params
    
    if ap.fix_float and ap.avg_fwd_start != "":
        print "\n## !! EXCEPTION !! ##"
        raise F_AVERAGE_EXCEPT, "The forward start and the floating strike feature can not be combined. Either set the Add Info field 'FAverageType' to 'ArithmeticFix' or delete the Add Info field 'FFwdStart'."
    if ap.fix_float and ap.avg_in != "":
        print "\n## !! EXCEPTION !! ##"
        raise F_AVERAGE_EXCEPT, "The average in and the floating strike feature can not be combined. Either set the Add Info field 'FAverageType' to 'ArithmeticFix' or delete the Add Info field 'FAverageIn'."
    if ap.avg_type_text == "GeometricFix" and ap.avg_in != "":
        print "\n## !! EXCEPTION !! ##"
        raise F_AVERAGE_EXCEPT, "The average in and the geometric average feature can not be combined. Either set the Add Info field 'FAverageType' to 'ArithmeticFix' or delete the Add Info field 'FAverageIn'."
    if ap.avg_in != "" and ap.avg_fwd_start != "":
        print "\n## !! EXCEPTION !! ##"
        raise F_AVERAGE_EXCEPT, "The average in and the forward start feature can not be combined. Either delete the Add Info field 'FAverageIn' or 'FFwdStart'."
    if ap.quanto_flag and ap.avg_type_text == "GeometricFix":
        print "\n## !! EXCEPTION !! ##"
        raise F_AVERAGE_EXCEPT, "There is no support for quanto Asian options with a geometric averageing method."
        
    # AVERAGE BASKETS
    if ap.average_basket:
        if ap.avg_type_text != "ArithmeticFix" or ap.avg_fwd_start != "":
            print "\n## !! EXCEPTION !! ##"
            raise F_AVERAGE_EXCEPT, 'Only pricing of arithmetic average basket options with fixed strike implemented.'
        if ap.bp.dim != len(ap.fut_avg_dates):   
            print "\n## !! EXCEPTION !! ##"
            raise F_AVERAGE_EXCEPT, 'The average dates do not correspond to the number of assets in the basket.'
        if ap.bp.fx_error:
            print  "\n## !! NO VALUE !! ##"
            if len(ap.bp.no_fx_ins) == ap.bp.dim:
                raise F_AVERAGE_EXCEPT, "No FX rates are defined for the basket. Use the ASQL application .MaintCreateQuantoBasketFX."
            else: 
                for ins in ap.bp.no_fx_ins:
                    print "## !!" + str(ins) + " !! ##"
                    raise F_AVERAGE_EXCEPT, "No FX rates are defined for these basket components. Use the ASQL application .MaintCreateQuantoBasketFX."
        try: float(ap.bp.vol[0])
        except: return 0.0 
        
        # AVERAGE QUANTO BASKET
        if ap.bp.quanto_flag:
            res = ael.eq_quanto_asian_basket(ap.bp.price, ap.texp, ap.bp.vol,
                    ap.bp.fx, ap.bp.fxvol, ap.bp.corr_stocks, ap.bp.corr_fx,
                    ap.bp.corr_stock_fx, ap.rate, ap.bp.rate_stocks, ap.bp.carry_cost,
                    ap.mod_strike, ap.put_call, ap.bp.dividends,
                    ap.fut_avg_dates, ap.fut_avg_weights, ap.bp.fixfx_flag,
                    ap.bp.weights, val_meth, nbr_of_sim)
        else:            
            res = ael.eq_asian_basket(ap.bp.price, ap.texp,
                ap.bp.vol, ap.bp.corr_stocks, ap.rate, ap.bp.carry_cost,  
                ap.mod_strike, ap.put_call, ap.bp.dividends, ap.fut_avg_dates,
                ap.fut_avg_weights, ap.bp.weights, val_meth, nbr_of_sim)

    # FORWARD START PERF.AVERAGE OPTION if the forward start day
    # is in the future.               
    elif ap.avg_fwd_start == "Fwd Start Perf" and ap.fwd_start_time >= 0:
        if ap.average_basket:
            print "\n## !! EXCEPTION !! ##"
            raise F_AVERAGE_EXCEPT, 'Pricing of forward start basket option not implemented'
        if ap.avg_type_text == "GeometricFix" or ap.avg_type_text == "GeometricFloating":
            print "\n## !! EXCEPTION !! ##"
            raise F_AVERAGE_EXCEPT, 'Only pricing of arithmetic average forward start performance implemented, not ' + ap.avg_type_text
        if ap.price == 0.0:
            print "\n## !! EXCEPTION !! ##"
            raise F_AVERAGE_EXCEPT, 'Underlying asset price equal to zero => division with zero.'

        res = ael.eq_fwd_start_perf_asian(ap.price,
                ap.texp, ap.vol, ap.rate, ap.carry_cost, ap.put_call,
                ap.dividends, ap.fut_avg_dates[0], ap.fut_avg_weights[0],
                val_meth, nbr_of_sim)
        
    # QUANTO AVERAGE with one underlying
    elif ap.quanto_flag and val_meth != "MomentMatching2":
        res = ael.eq_quanto_asian(ap.price, ap.texp, ap.vol, 
                ap.fx_rate, ap.fx_vol, ap.corr_stock_fx, ap.rate, ap.foreign_rate, ap.carry_cost,
                ap.mod_strike*ap.fx_rate, ap.put_call, ap.dividends, ap.fut_avg_dates[0],
                ap.fut_avg_weights[0], ap.quanto_flag, val_meth, nbr_of_sim)
    else:
        # OLD FIX/FLOATING VANILLA AVERAGE OPTION
        if val_meth == "MomentMatching2":
            if ap.avg_fwd_start != "":
                print "\n## !! EXCEPTION !! ##"
                raise F_AVERAGE_EXCEPT, "The MomentMatching2 valuation method does not handle the option type Forward Start Asian."
            if ap.quanto_flag:
                print "\n## !! EXCEPTION !! ##"
                raise F_AVERAGE_EXCEPT, "The MomentMatching2 valuation method does not handle quanto Asian options."
            future_dividends = 0
            for div in ap.dividends:
                if div[1]>0:
                    future_dividends = 1
                    break
            if (future_dividends and ap.fix_float) or ap.avg_type_text=='GeometricFloating': 
                # Only works for Python 1.5
                if ap.avg_type_text=='GeometricFloating':
                    print "\n## !! EXCEPTION !! ##"
                    raise F_AVERAGE_EXCEPT, "The GeometricFloating average option type is no longer supported."
                else:
                    print "\n## !! EXCEPTION !! ##"
                    raise F_AVERAGE_EXCEPT, "The 'MomentMatching2' valuation method does not handle floating strike options with future dividends. Please use the 'RogerShi' method instead."
            else: 
                import FEqAverageAnalytic
                res = FEqAverageAnalytic.AverageAnalytic(ap).eq_average_analytic()

        # NEW FIX/FLOATING FORWARD START/VANILLA AVERAGE OPTION
        else:        
            res = ael.eq_asian(ap.price, ap.texp, ap.vol,
                ap.rate, ap.carry_cost, ap.mod_strike, ap.put_call,
                ap.dividends, ap.fut_avg_dates[0], ap.fut_avg_weights[0],
                val_meth, nbr_of_sim)
    try:float(res)
    except:
        print "\n## !! EXCEPTION !! ##"
        raise F_AVERAGE_EXCEPT, "No result is returned from the valuation."
    res = error_handling(res)
    res = res * ap.df
    return res

"""----------------------------------------------------------------------------
error_handling() 
    The function checks a result to identify an eventual error message.
----------------------------------------------------------------------------"""        
def error_handling(res):
    if res > -F_EPSILON: return max(res, 0.0)
    # Error handling
    print "\n## !! EXCEPTION !! ##"
    if res == -1.0:
        raise F_AVERAGE_EXCEPT, 'The correlation matrix is not positive definite.'
    elif res == -3.0:
        raise F_AVERAGE_EXCEPT, 'There are too many assets in basket, maximum = 100.'
    elif res == -4.0:
        raise F_AVERAGE_EXCEPT, 'Negative input value: time to expiry, stock price or volatility.'
    elif res == -5.0:
        raise F_AVERAGE_EXCEPT, 'The number of simulations must be increased, minimum = 100.'
    elif res == -6.0:
        raise F_AVERAGE_EXCEPT, 'The valuation method is not implemented.'
    elif res == -8.0:
        raise F_AVERAGE_EXCEPT, 'The dividends are too large.'
    elif res == -9.0:
        raise F_AVERAGE_EXCEPT, 'Negative dividends.'
    elif res == -10.0:
        raise F_AVERAGE_EXCEPT, 'The forward start date is after or at the same time as the maturity of the option.'
    elif res == -12.0:
        raise F_AVERAGE_EXCEPT, 'The GentleVorst or the MomentMatching method do not handle negative asian weights.'
    else:
        raise F_AVERAGE_EXCEPT, 'Negative output. Unknown exception'

"""----------------------------------------------------------------------------
average() 
    Calculates the average of all elements in a list (either a geometric or 
    an arithmetic average).
----------------------------------------------------------------------------"""    
def average(t, avg_type):
    try:    l = len(t[0])
    except: l = 1
    if avg_type == AVERAGE_ARITH:
        if l == 2:return sumSeq(map(lambda x:(x[0]), t))/len(t)             
        else: return sumSeq(t)/len(t)             
    elif avg_type == AVERAGE_GEOM:
        if l == 2:
            return pow(mulSeq(map(lambda x:(x[0]), t)), 1/(1.0*len(t)))
        else: return pow(mulSeq(t), 1/(1.0*len(t)))
    else: 
        raise F_AVERAGE_EXCEPT, 'The average type ' + str(avg_type) + ' is not supported.'    



