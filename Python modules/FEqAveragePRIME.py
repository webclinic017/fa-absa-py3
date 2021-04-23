""" SEQ_VERSION_NR = PRIME 2.8.1 """





"""----------------------------------------------------------------------------
MODULE
    FEqAveragePRIME - Average options are valued. PRIME calls the valuation.
        
    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    Performs valuation of average options using routines in 
    FEqAverageUtils.
        
----------------------------------------------------------------------------"""
import ael
import FEqAverageUtils
import FTimeSeries
from FEqUtilsPRIME import *

F_AVERAGE_EXCEPT        = 'f_eq_average_xcp'  # This exception is thrown by all average routines
F_AVERAGE_FUTAVGVAL     = -1                  # Value stored in timeseries for unknown average points
F_STRIKE_TIMESERIES     = 'FAverageStrike'
F_AVERAGE_TIMESERIESRUN = 0
AVERAGE_ARITH = 0;AVERAGE_GEOM = 1;AVERAGE_HARM = 2
AvgOptionTypeDict = { 'ArithmeticFix':0, 'ArithmeticFloating':1,
                      'GeometricFix': 2, 'GeometricFloating': 3,
                      'HarmonicFix':  4, 'HarmonicFloating':  5 }

AvgOptionNumberDict = {}
for i in AvgOptionTypeDict.items():
    AvgOptionNumberDict[i[1]]=i[0]

AvgTypeDict = { 0:AVERAGE_ARITH, 1:AVERAGE_ARITH,
                2:AVERAGE_GEOM,  3:AVERAGE_GEOM,
                4:AVERAGE_HARM,  5:AVERAGE_HARM }

"""----------------------------------------------------------------------------
clear_old()
    The function checks if there are old timeseries defined for components not 
    longer in the underlying basket. The function also sorts the average prices.
----------------------------------------------------------------------------"""
def clear_old(ins, time_series_data, underlyings):
    # Remove old timeseries for components no longer in the basket
    #time_series_data = AsList(time_series_data)
    undInstrs = time_series_data[1]
    avg_price_list = time_series_data[2]
    
    new_undInstrs = []
    new_avg_price_list = []
    temp_dict = {}
    k = 0
    for undInstr in AsList(undInstrs):
        temp_dict[undInstr] = k    
        k = k + 1 
    for underlying in underlyings:
        if temp_dict.has_key(underlying.insid):
            new_undInstrs.append(underlying.insid)
            new_avg_price_list.append(avg_price_list[temp_dict[underlying.insid]])
    # ERROR CHECK
    if len(new_undInstrs) == 0:
        return [[], ['No Time Series exists for the instrument. Create one with the ASQL-application .MaintCreateAverageDates.']]
    else:
        for underlying in underlyings:
            if not temp_dict.has_key(underlying.insid):
                return [[], ['No TimeSerie is created for the stock ' + underlying.insid + '. Create one with the ASQL-application .MaintCreateAverageDates.']]
    return [new_undInstrs, new_avg_price_list]

"""----------------------------------------------------------------------------
get_avg_option_type_number()
    The function returns a corresponding number for the average option type.
----------------------------------------------------------------------------"""
def get_avg_option_type_number(avg_type_text):
    if AvgOptionTypeDict.has_key(avg_type_text):
        return AvgOptionTypeDict[avg_type_text]
    else: return 'No Average option Type set!'
    
"""----------------------------------------------------------------------------
get_avg_type_number()
    The function returns a corresponding number for the averaging method type.
----------------------------------------------------------------------------"""
def get_avg_type_number(average_option_type_number):
    return AvgTypeDict[average_option_type_number]


"""----------------------------------------------------------------------------
get_avg_price_dict()
    The function calls a function with the same name in the FEqAverageUtils 
    module. The result is then sorted and arrays are returned instead of 
    disctionaries since PRIME can not handle all dictionary methods.
----------------------------------------------------------------------------"""
def get_avg_price_dict(i, und_instrs, average_price_list, avg_strike_prices, average_basket_flag, avg_fwdstart, fwdstart_params, undins_PRIME, today):
    if len(average_price_list[0][0])!= 2:
        a = average_price_list[0]
        return [[a, a], [a, a], [a], [a], [a]]
    if avg_fwdstart == 0: avg_fwdstart = "Fwd Start"
    elif avg_fwdstart == 1: avg_fwdstart = "Fwd Start Perf"
    else: avg_fwdstart = ""
    res = FEqAverageUtils.get_avg_price_dict(i, und_instrs, average_price_list, \
        avg_strike_prices, average_basket_flag, avg_fwdstart, fwdstart_params, today, 1)
    if str(type(res)) != "<type 'str'>":
        [old_avgs_dict, avg_dates_dict, avg_start_dict, avg_end_dict, avg_dates] = res
    else: return [[res, res], [res, res], [res], [res], [res]]
    old_avgs_keys    = []
    old_avgs_values  = []
    avg_dates_keys   = []
    avg_dates_values = []
    if len(undins_PRIME) != 1:
        for undins in undins_PRIME:
            if old_avgs_dict.has_key(undins.insid):
                old_avgs_keys.append(undins.insid)
                old_avgs_values.append(old_avgs_dict[undins.insid])
            if avg_dates_dict.has_key(undins.insid):
                avg_dates_keys.append(undins.insid)
                avg_dates_values.append(avg_dates_dict[undins.insid])
    else:
        old_avgs_keys = old_avgs_dict.keys()
        old_avgs_values = old_avgs_dict.values()
        avg_dates_keys = avg_dates_dict.keys()
        avg_dates_values = avg_dates_dict.values()
    return [[old_avgs_keys, old_avgs_values],\
            [avg_dates_keys, avg_dates_values],\
            avg_dates, avg_start_dict.values()[0], avg_end_dict.values()[0]]    

"""----------------------------------------------------------------------------
BasketParams()
    The class holds all necessary valuation parameters for basket options
----------------------------------------------------------------------------"""
class BasketParams:
    def __init__(self, basket_params):
        self.dim           = basket_params[0]
        self.quanto_flag   = basket_params[1]
        self.price         = AsList(basket_params[2])
        self.vol           = AsList(basket_params[3])
        try:
            if str(type(basket_params[4])) == "<type 'str'>":
                print "\n## !! EXCEPTION !! ##"
                raise F_AVERAGE_EXCEPT, basket_params[4]
            self.corr_stocks= AsMatrix(basket_params[4])
        except Exception, msg:
            print "\n## !! EXCEPTION !! ##"
            raise F_AVERAGE_EXCEPT, "No correlations are defined."
        self.rate_stocks   = AsList(basket_params[5])
        self.carry_cost    = AsList(basket_params[6])
        self.dividends     = AsMatrix(basket_params[7])
        self.weights       = AsList(basket_params[8])
        self.fx_error      = basket_params[10]
        self.no_fx_ins     = basket_params[11]
        
        if self.quanto_flag:
            [self.fx, self.fxvol, self.corr_fx, self.corr_stock_fx] = basket_params[9]
            self.fx            = AsList(self.fx)
            try: float(self.fx[0])
            except: 
                print "\n## !! EXCEPTION !! ##"
                raise F_AVERAGE_EXCEPT, self.fx[0]
            self.fxvol         = AsList(self.fxvol)
            try:
                if str(type(self.corr_fx)) == "<type 'str'>":
                    print "\n## !! EXCEPTION !! ##"
                    raise F_AVERAGE_EXCEPT, self.corr_fx
                self.corr_fx = AsMatrix(self.corr_fx)
            except Exception, msg:
                print "\n## !! EXCEPTION !! ##"
                raise F_AVERAGE_EXCEPT, "No FX correlations are defined."
            try:
                if str(type(self.corr_stock_fx)) == "<type 'str'>":
                    print "\n## !! EXCEPTION !! ##"
                    raise F_AVERAGE_EXCEPT, self.corr_stock_fx
                self.corr_stock_fx = AsMatrix(self.corr_stock_fx)
            except Exception, msg:
                print "\n## !! EXCEPTION !! ##"
                raise F_AVERAGE_EXCEPT, "No FX/Stock correlations are defined."
            self.fixfx_flag = 1
        else: self.fixfx_flag = 0
        
        
"""----------------------------------------------------------------------------
FAverageParams()
    The class holds all necessary valuation parameters for average options
----------------------------------------------------------------------------"""
class FAverageParams:
    def __init__(self, vanilla_params, average_params, quanto_params, basket_params):
        # Standard vanilla params
        self.price      = vanilla_params[0]
        self.texp       = vanilla_params[1]
        self.rate       = vanilla_params[3]
        self.carry_cost = vanilla_params[4]
        self.strike     = vanilla_params[6]
        self.put_call   = vanilla_params[7]
        
        # Average params
        self.avg_type_text    = average_params[0]
        self.avg_dates        = AsList(average_params[1])
        try: 
            if self.avg_dates != []:
                float(self.avg_dates[0])
        except: 
            print "\n## !! EXCEPTION !! ##"
            raise F_AVERAGE_EXCEPT, self.avg_dates[0]
        self.cont_div         = average_params[2]
        self.avg_so_far       = average_params[3]
        self.avg_type         = average_params[4]
        self.fix_float        = average_params[5]
        self.dividends        = AsList(average_params[6])
        self.average_basket   = average_params[7]
        avg_fwd_start         = average_params[8]
        self.fwd_start_time   = average_params[9]
        self.mod_strike       = average_params[10]
        self.fut_avg_dates    = AsMatrix(average_params[11])
        self.fut_avg_weights  = AsMatrix(average_params[12])
        self.quanto_flag      = average_params[13]
        self.vol              = average_params[14]
        self.avg_in           = average_params[15]
        
        if avg_fwd_start == 0: self.avg_fwd_start = "Fwd Start"
        elif avg_fwd_start == 1: self.avg_fwd_start = "Fwd Start Perf"
        else: self.avg_fwd_start = ""
        
        # Quanto params 
        if quanto_params != ():
            self.fx_rate       = quanto_params[1]
            self.foreign_rate  = quanto_params[2]
            self.fx_vol        = quanto_params[3]
            self.corr_stock_fx = quanto_params[4]

        # Basket params
        if basket_params != ():
            self.bp = BasketParams(basket_params)
            
        
"""----------------------------------------------------------------------------
FUNCTION    
    TheorAverageOption() 

DESCRIPTION
    The function calculates the price of an average option. 
    
ARGUMENTS
    vanilla_params[]    A list with all standard vanilla parameters, like strike.
    average_params[]    A list with average specific parameters. 
                          - valuation_date:       Valuation date
                          - exp_day:              Expiry
                          - avg_type_text:        See AvgOptionTypeDict above
                          - avg_dates:            List of all average monitor 
                                                  times
                          - cont_div:             Continuous dividend 
                          - avg_so_far:           Calculated average uptil today
                          - avg_type:             Arithmetic or geometric
                          - fix_float:            Is the strike fix or floating
                          - dividends:            Vector with future dividends
    quanto_params[]
    basket_params[]
    val_meth_params[]  

RETURNS
    res       float     Value of instrument
----------------------------------------------------------------------------"""   
def TheorAverageOption(i, vanilla_params, average_params, quanto_params, basket_params, val_meth_params):
    try:
        if i.und_insaddr.instype != "Stock" and i.und_insaddr.instype != "EquityIndex" and \
           i.und_insaddr.instype != "Combination" and i.und_insaddr.instype != "Curr":
            return {"PV":"The underlying instrument type " + str(i.und_insaddr.instype) + " of the instrument " + i.insid + ", is not handled."}
        if i.exotic_type != "None":
            return {"PV":"No support for barrier average options!"}
        if i.digital: 
            return {"PV":"No support for digital average options!"}
        if i.exercise_type != 'European': 
            return {"PV":"No support for American average options!"} 
        if average_params[14] < 0.0: return {"PV": 'Negative volatility!'}
        ap = FAverageParams(vanilla_params, average_params, quanto_params, basket_params)
        ap.df = get_discount_factor(i)            
        try: 
            if ap.average_basket:
                for price in ap.bp.price:
                    if float(price) == 0.0: return {"PV":'No underlying price!'}
            else:
                if float(ap.price) == 0.0: return {"PV":'No underlying price!'}
        except: return {"PV":'No underlying price!'}
        if ap.avg_in != "":        
            series2 = FTimeSeries.get_TimeSeries(i, F_STRIKE_TIMESERIES, F_AVERAGE_TIMESERIESRUN)
            if series2 == []:
                return {"PV":"The Average in styled option has no Strike timeseries!"}
        val_meth_params = AsList(val_meth_params)
        res = FEqAverageUtils.get_pv(ap, val_meth_params)
        theta = "theorAverageTheta"
        if ap.average_basket: 
            delta     = "theorGlobalBasketDelta"
            delta_pct = "theorGlobalBasketDeltaPct"
            gamma     = "theorGlobalBasketGamma" 
            gamma_pct = "theorGlobalBasketGammaPct"
            vega      = "theorGlobalVega"
            return {"PV":res, "Delta":delta, "DeltaPct":delta_pct, "Gamma":gamma, "GammaPct":gamma_pct, \
                   "Theta":theta, "Vega":vega}
        else: 
            if ap.avg_fwd_start != "":
                return {"PV":res, "Theta":theta, "Vega":"fwdstartNumericalVega"} 
            return {"PV":res, "Theta":theta}
    except F_AVERAGE_EXCEPT, msg:
        print '\nModule: FEqAveragePRIME'
        print 'Error :', msg
        print 'Instr :', i.insid
        return {"PV":'Valuation error!'}




