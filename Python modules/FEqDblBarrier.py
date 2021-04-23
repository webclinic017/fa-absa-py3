""" SEQ_VERSION_NR = PRIME 2.8.1 """




"""----------------------------------------------------------------------------
MODULE
    FEqDblBarrier - Valuation of double barrier options
    
    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
   Calculates the theoretical price of a double barrier option. 
   European options with discrete / continuous dividends and discrete 
   / continuous barrier are handled.
 
NOTE        

REFERENCES  
 
----------------------------------------------------------------------------"""
LOG_PARAMETERS = 0

import ael
import math
import sys
import FEqBarrier
import FEqBarrierUtils

# This exception is thrown by all barrier and double barrier routines. 
F_BARRIER_EXCEPT        = 'f_eq_barrier_xcp'  

# Second barrier level
F_SECOND_BARRIER = 'FBarrier2'                                           
F_BARRIER_TIMESERIES    = 'FBarrierMonitorDays' 
F_BARRIER_TIMESERIESRUN = 0 
F_BARRIER_CROSSED       = 'FBarrier Crossed'
F_BARRIER_CROSSED_DATE  = 'FBarrier Cross Date'
F_BARRIER_MONITOR_FRQ   = 'FBarrierMonitorFrq'
F_BARRIER_CONTINUOUS    = 'Continuous'

counter = 0
"""----------------------------------------------------------------------------
CLASS           
    FDblBarrierParams - Parameters for barrier options

INHERITS
    FBarrierParams
            
DESCRIPTION     
    The class extracts all parameters needed to value a double barrier option.

CONSTRUCTION    
    i                       Instrument  An instrument that is a barrier option

MEMBERS         
    second_barrier                float       The second barrier. Only used for 
                                        double barrier options.                         
--------------------------------------------------------------------------------""" 
class FDblBarrierParams(FEqBarrier.FBarrierParams):
    def __init__(self, i):
        FEqBarrier.FBarrierParams.__init__(self, i)
        second_barrier_str = i.add_info(F_SECOND_BARRIER)
        self.second_barrier = FEqBarrierUtils.get_float_second_barrier(second_barrier_str)
                
    def pv(self):
        val_meth_params = FEqBarrierUtils.double_val_meth(self.dividends, self.discrete_barr,\
            self.barrier, self.barr_monitoring_times, self.barr_freq, self.second_barrier, \
            self.price, self.texp, self.vol, self.use_model)
        res = FEqBarrierUtils.get_double_pv(self, val_meth_params)
        if not self.fix_fx:
            if str(type(res)) == "<type 'dict'>" or str(type(res)) == "<type 'dictionary'>":
                pv = res['PV'] * self.strike_theor_curr_fx
                res['PV'] = pv
            else: res = res * self.strike_theor_curr_fx
        return res


"""----------------------------------------------------------------------------
FUNCTION    
    pv() 

DESCRIPTION
    The function pv() calculates the theoretical price of a double barrier option. 

ARGUMENTS
    i       Instrument  Double barrier option
    calc    Integer     0=>No calculation 1=>Perform calculation
    ref                 Optimisation parameter

RETURNS
   [res     float       Value of instrument
    exp_day date        Maturity date
    curr    string      Currency in which the option was valued
    Fixed   string      Constant = 'Fixed']                     
----------------------------------------------------------------------------"""
def pv(i, calc, ref):
    try:
        extra_days = 0
        if calc:
            dbl_barrier_params = FDblBarrierParams(i)
            try: print_info = i.add_info("FPrintInfo")
            except: print_info = ""
            if globals()['counter'] == 5: globals()['counter'] = 0
            if (LOG_PARAMETERS or (print_info == "Yes" and ael.userid() == i.updat_usrnbr.userid)) and globals()['counter'] == 0:
                if dbl_barrier_params.texp > 0: print get_info(dbl_barrier_params)
                else: print "\n## !! OPTION " + i.insid + " HAS EXPIRED !! ##"
            globals()['counter'] = globals()['counter'] + 1
            try: 
                if i.exp_day < ael.date_valueday(): res = 0.0
                else:
                    result = dbl_barrier_params.pv()  
                    if str(type(result)) == "<type 'dict'>" or str(type(result)) == "<type 'dictionary'>":
                        has_greeks = 0; greeks = []
                        greeks.append(result["Delta"])
                        greeks.append(result["Gamma"])
                        greeks.append(result["Theta"])

                        for greek in greeks:
                            if greek != -1: 
                                has_greeks = 1
                                break       
                        if has_greeks: 
                            res = [result["PV"]]
                            res.extend(greeks)
                        else: res = result["PV"]
                    else: res = result
                    extra_days = dbl_barrier_params.extra_days
            except Exception, msg: 
                print "\n## !! EXCEPTION !! ##"
                raise F_BARRIER_EXCEPT, msg                     
        else: res = 0.0
    except F_BARRIER_EXCEPT, msg:
        print
        print 'Module:  FEqDblBarrier'
        print 'Error : ', msg
        print 'Instr : ', i.insid
        res = 0.0 
    return [ [ res, i.exp_day.add_days(extra_days), i.curr, 'Fixed' ] ]


def get_info(DblBarrierParams):
    dbp = DblBarrierParams
    s = ''
    s = s + "Instrument: \t" + dbp.insid + "\t is using parameter(s): \n"  
    s = s + "\t\n"
    for curve in dbp.yield_curves:
        if curve[0] == 'Repo': insid = dbp.insid
        elif curve[0] == 'Discount': insid = dbp.underlying
        else: insid = dbp.underlying
        s = s + "Yield curve:\t" + str(curve[1]) + " for " + str(curve[0]) + " (" + insid + ", " + dbp.currency + ")\n" 
    s = s + "\t\n"
    s= s + "Volatility:\t" + str(dbp.vol_surface) + "\t(" + dbp.insid + ")\n"
    s = s + "\t\n"  
    s = s + "Used repo rate:\t\t%*.*f" % (6, 4, dbp.repo*100) + "\n"
    s = s + "Used volatility:\t%*.*f" % (6, 4, dbp.vol*100)  + "\n"
    s = s + "Used discount rate:\t%*.*f" % (6, 4, dbp.rate*100) + "\n"
    s = s + "\t\n" 

    s = s + "Barrier type:\t\t" + dbp.exotic_type + "\n"
    s = s + "First Barrier level:\t" + str(dbp.barrier) + "\n"
    s = s + "Second Barrier level:\t" + str(dbp.second_barrier) + "\n"
    s = s + "\t\n" 
        
    s = s + "Rebate:\t\t\t" + str(dbp.rebate) + "\n"
    if dbp.pay_rebate == "Expiry": rebate_day = "Expiry"
    else: rebate_day = "Hit"
    s = s + "Rebate will be paid on\t" + str(rebate_day) + "\n"
    s = s + "\t\n"
    
    if dbp.discrete_barr: disc = 'Yes'
    else: disc = 'No'
    s = s + "Discrete barrier:\t" + disc + "\n"
    s = s + "Monitoring times:\t" + str(dbp.barr_monitoring_times) + "\n"
    
    if dbp.knocked != "Yes": 
        status = "Not yet knocked"
        date = ""
    else: 
        status = "Knocked"
        date = dbp.knocked_date

    s = s + "Barrier status:\t\t" + status + "\n"
    if date != "":
        s = s + "Barrier knock date:\t" + str(date) + "\n"
        
    [val_meth, steps] = FEqBarrierUtils.double_val_meth(dbp.dividends, dbp.discrete_barr,\
                dbp.barrier, dbp.barr_monitoring_times, dbp.barr_freq, dbp.second_barrier, \
            dbp.price, dbp.texp, dbp.vol, dbp.use_model)
    if status != "Knocked":
        s = s + "Valuation method:\t" + str(val_meth) + "\n"
        s = s + "Steps:\t\t\t" + str(steps) + "\n"
    s = s + "\t\n" 

    s = s + "Underlying:\t\t" + dbp.underlying + "\n"
    s = s + "Underlying price:\t" + str(dbp.price) + "\n"

    if dbp.dividends != []:
        s = s + "\t\n"
        s = s + "Underlying Dividends (in " + dbp.currency + ") :\n"
        s = s + "\t\tEx Div Day \tRecord Day \tAmount \tTax Factor\n"
        for d in dbp.div_entity:
            s = s + "\t\t" + str(d.ex_div_day) + "\t" + str(d.day) + "\t" + str(d.dividend) + "\t" + str(d.tax_factor) + "\n"
    s = s + "\t\n"
    s = s + "Used valuation function: \tFEqDblBarrier.pv \n"
    s = s + "Mapped in context:\t\t" + dbp.used_context + "\n"
    s = s + "\t\n" + "\t\n"
    return s


## Utility functions used by ASQL Query .AppPricingDblBarrier

def UsedValFun(i, *rest):
    B = FDblBarrierParams(i)
    b = B.dbl_barrier_val_meth()
    val_meth = b[0]
    return str(val_meth)
    
"""----------------------------------------------------------------------------
get_barriers() 
    The function retrieves the two double barrier option levels.
----------------------------------------------------------------------------"""
def get_barriers(i):
    barrier = i.barrier
    try: second_barrier = float(i.add_info(F_SECOND_BARRIER))
    except: 
        new_string = ''
        if sys.exc_info()[0] == 'ValueError':
            try:
                value = i.add_info(F_SECOND_BARRIER)
                for char in value:
                    if not(char == ','):
                        new_string = new_string + char
                second_barrier = float(new_string)
            except: second_barrier = 0.0
        else: second_barrier = 0.0
    return (barrier, second_barrier)

"""----------------------------------------------------------------------------
get_lower_barrier() 
    The function returns the smallest barrier level
----------------------------------------------------------------------------"""
def get_lower_barrier(i):
    return min(get_barriers(i))

"""----------------------------------------------------------------------------
get_upper_barrier() 
    The function returns the highest barrier level
----------------------------------------------------------------------------"""
def get_upper_barrier(i):
    return max(get_barriers(i))

"""----------------------------------------------------------------------------
FUNCTION    
    calc_diff_spot_lower_barrier() 

DESCRIPTION
    The function calculates the difference (in percent) between the lower barrier
    and the spot price. 

ARGUMENTS
    i       Instrument  Double Barrier Option

RETURNS
   diff     If the barrier is already crossed the value zero is returned.
----------------------------------------------------------------------------"""
def calc_diff_spot_lower_barrier(i,*rest):
    barrier_status = i.add_info(F_BARRIER_CROSSED)
    barr_freq = i.add_info(F_BARRIER_MONITOR_FRQ)
    
    if barrier_status !="Yes" and barrier_status !="Yes TEMP?" : 
        lower_barrier = get_lower_barrier(i)
        price = i.und_insaddr.used_price(None, i.strike_curr.insid) 
        if price != 0.0:
            res = (price-lower_barrier)/(1.0*price)*100
        else:
            print "No underlying price exist for ", i.und_insaddr.insid
            return 10000000 
        if res <= 0 and barr_freq == F_BARRIER_CONTINUOUS:
            FEqBarrier.update_addinfo(i, "Yes TEMP?", lower_barrier)
            res = 0.0
        else:
            res = int(res+1)
    elif barrier_status == "Yes" or barrier_status == "Yes TEMP?":res = 0.0
    else: raise F_BARRIER_EXCEPT, "Wrong Barrier status in addinfo field 'FBarrier Knocked'."
    return res

"""----------------------------------------------------------------------------
FUNCTION    
    calc_diff_spot_upper_barrier() 

DESCRIPTION
    The function calculates the difference (in percent) between the upper barrier
    and the spot price. 

ARGUMENTS
    i       Instrument  Double Barrier Option

RETURNS
   diff     If the barrier is already crossed the value zero is returned.
----------------------------------------------------------------------------"""
def calc_diff_spot_upper_barrier(i,*rest):
    barrier_status = i.add_info(F_BARRIER_CROSSED)
    barr_freq = i.add_info(F_BARRIER_MONITOR_FRQ)
    
    if barrier_status !="Yes" and barrier_status !="Yes TEMP?" : 
        upper_barrier = get_upper_barrier(i)
        price = i.und_insaddr.used_price(None, i.strike_curr.insid) 
        if price != 0.0:
            res = (upper_barrier - price)/(1.0*price)*100
        else:
            print "No underlying price exist for ", i.und_insaddr.insid
            return 10000000 
        if res <= 0 and barr_freq == F_BARRIER_CONTINUOUS:
            FEqBarrier.update_addinfo(i, "Yes TEMP?", upper_barrier)
            res = 0.0
        else:
            res = int(res+1)
    elif barrier_status == "Yes" or barrier_status == "Yes TEMP?":res = 0.0
    else: raise F_BARRIER_EXCEPT, "Wrong Barrier status in addinfo field 'FBarrier Knocked'."
    return res



