""" SEQ_VERSION_NR = PRIME 2.8.1 """




"""----------------------------------------------------------------------------
MODULE
    FEqBarrierPRIME - Barrier options are valued. PRIME calls the valuation.
    
    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
   Calculates the price of a barrier option. European options with discrete 
   dividends are handled.
----------------------------------------------------------------------------"""
import ael
import sys
import math
import FEqBarrierUtils
from FEqUtilsPRIME import *

# The timeseries where barrier monitor dates are stored.
F_BARRIER_EXCEPT        = 'f_eq_barrier_xcp' 
F_BARRIER_CROSSED       = 'FBarrier Crossed'

"""----------------------------------------------------------------------------
FBarrierParams 
    The class holds all necessary parameters for barrier valuation.
----------------------------------------------------------------------------"""    
class FBarrierParams:
    def __init__(self, vanilla_params, barrier_params, digital_params, quanto_params):
        # Standard Params
        self.price      = vanilla_params[0]
        self.texp       = vanilla_params[1]
        self.vol        = vanilla_params[2]
        self.rate       = vanilla_params[3]
        self.carry_cost = vanilla_params[4]
        self.strike     = vanilla_params[6]
        self.put_call   = vanilla_params[7]
        exc_type        = vanilla_params[8]
            
        # Barrier option params
        self.barrier_type_nbr      = barrier_params[0] + 1
        self.barrier               = barrier_params[1]
        self.rebate                = barrier_params[2]
        self.discrete_barr         = barrier_params[3]
        self.barr_dates            = AsList(barrier_params[4])
        self.barr_monitoring_times = barrier_params[5]
        try: float(self.barr_monitoring_times)
        except:
            print "\n## !! EXCEPTION !! ##"
            raise F_BARRIER_EXCEPT, barrier_params[5]

        self.dividends             = AsList(barrier_params[6])
        knocked                    = barrier_params[7]
        if knocked == 0: self.knocked = "Yes"
        elif knocked == 1: self.knocked = "Yes TEMP?"
        else: self.knocked = ""
        self.knocked_date          = barrier_params[8]
        barrier_man                = barrier_params[9] 
        self.pay_rebate            = barrier_params[10]
        if self.knocked != "":
            if self.knocked_date != '':
                # Check historical mode.
                try:
                    if ael.historical_mode() and self.knocked_date > ael.date_valueday():
                        self.knocked = ""
                        self.knocked_date = ""
                    elif self.knocked_date > ael.date_valueday(): 
                        print "\n## !! EXCEPTION !! ##"
                        raise F_BARRIER_EXCEPT, "The barrier cross date is in the future."
                    else: self.time_from_knocked = self.knocked_date.years_between(ael.date_valueday(), 'Act/365')
                except: 
                    self.time_from_knocked = self.knocked_date.years_between(ael.date_valueday(), 'Act/365')
            else: 
                if self.knocked != "Yes TEMP?":
                    print "\n## !! NO VALUE !! ##"
                    raise F_BARRIER_EXCEPT, "The barrier is crossed but no knock date is given. Please update the Additional Info field 'FBarrier Cross Date'." 
        if barrier_man != 0: 
            self.barrier_man = barrier_man
        else: self.barrier_man = self.barrier
        self.fix_fx = barrier_params[11]

        # Digital barrier params
        self.digital       = digital_params[0]
        self.settlement    = digital_params[1]
        
        if self.fix_fx:
            self.fx_rate = quanto_params[0]
            self.fx_vol  = quanto_params[1]
            self.foreign_rate  = quanto_params[2]
            self.corr_stock_fx = quanto_params[3]
            
        if exc_type == 'European' or exc_type == 0:self.eur_ame = 0
        else: self.eur_ame = 1
   
    def __str__(self):
        return str(self.__dict__)
   
    def __repr__(self):
        return self.__str__()

"""----------------------------------------------------------------------------
get_hit_probability 
    The function caclulates the probability that the underlying asset will hit 
    the barrier before expiry.
----------------------------------------------------------------------------"""    
def get_hit_probability(i,vanilla_params,barrier_params,digital_params,
                 quanto_params,val_meth_params,single,second_barrier=None):
    try:
        bp = FBarrierParams(vanilla_params, barrier_params, digital_params, quanto_params)
        try:
            if float(bp.price) == 0.0:
                return {"PV":'No underlying price!'}
        except: return {"PV":'No underlying price!'}
        bp.rebate = math.exp(bp.rate*bp.texp)
        bp.knock_in = 0
        if not single:
            bp.second_barrier = second_barrier
        res = FEqBarrierUtils.get_digital_expiry_pv(single, bp, val_meth_params)
        if bp.fix_fx: res['PV'] = res['PV'] / float(bp.fx_rate)
        return res
    except F_BARRIER_EXCEPT, msg:
        print 'Module: FEqBarrierPRIME'
        print 'Error : ', msg
        print 'Instr : ', i.insid
        return 0.0
    
"""----------------------------------------------------------------------------
calc_diff_spot_barrier_sim 
    The function calculates the difference between the barrier and the underlying 
    price. It is possible to simulate the underlying price.
----------------------------------------------------------------------------"""    
def calc_diff_spot_barrier_sim(i,price,barrier,double=0):
    barrier_status = i.add_info(F_BARRIER_CROSSED)
    if barrier_status !="Yes" and barrier_status !="Yes TEMP?" : 
        if price != 0.0:
            if double: 
                res = (price - barrier)/(1.0*abs(price))*100
            else:
                if i.exotic_type == "Down & Out" or i.exotic_type == "Down & In":
                    res = (price - barrier)/(1.0*price)*100
                elif i.exotic_type == "Up & Out" or i.exotic_type == "Up & In":
                    res = (barrier - price)/(1.0*price)*100
        else:
            return "No underlying price exist for " + str(i.und_insaddr.insid)
        res = int(res+1)
    elif barrier_status == "Yes" or barrier_status == "Yes TEMP?":res = 0.0
    else: return "Wrong Barrier status in addinfo field 'FBarrier Knocked' for ins " + i.insid + "s."
    return res

"""----------------------------------------------------------------------------
calc_diff_spot_lower_barrier_sim 
    The function calculates the difference (in percent) between the lower barrier
    and the spot price. It is possible to simulate the underlying price. 
----------------------------------------------------------------------------"""
def calc_diff_spot_lower_barrier_sim(i, price):
    import FEqDblBarrier
    lower_barrier = FEqDblBarrier.get_lower_barrier(i)
    return calc_diff_spot_barrier_sim(i, price, lower_barrier, 1)
    
"""----------------------------------------------------------------------------
calc_diff_spot_upper_barrier_sim
    The function calculates the difference (in percent) between the upper barrier
    and the spot price. It is possible to simualate the underlying price.
----------------------------------------------------------------------------"""
def calc_diff_spot_upper_barrier_sim(i, price):
    import FEqDblBarrier
    upper_barrier = FEqDblBarrier.get_upper_barrier(i)
    return calc_diff_spot_barrier_sim(i, -price, -upper_barrier, 1)


"""----------------------------------------------------------------------------
FUNCTION    
    TheorBarrierOption() / TheorDblBarrierOption()

DESCRIPTION
    The functions calculate the price of a barrier and a double barrier option, 
    respectively. If the valuation method is a tree-method, also the greeks delta, 
    gamma and theta are returned.
    
ARGUMENTS
    vanilla_params[]    A list with all standard vanilla parameters, like strike.
    barrier_params[]    A list with barrier specific parameters. 
                          - barrier_type_number:The exotic type string transformed
                                               into a number.(E.g "Down & Out"=>1).
                          - barrier:               The barrier.
                          - rebate:                The rebate.
                          - discrete_barr:         Boolean.
                          - barr_dates:            The barrier monitoring dates.
                          - barr_monitoring_times: The number of monitoring dates.
                          
                          - dividends:         The dividends to be distributed 
                                               during the option life time.
    digital_params[]    A list with digital parameters.
    val_meth_params[]   A list with valuation method (string) and the number of 
                        steps to use in the numerical valuation.

RETURNS
   {"PV"     float      Value of instrument
    "Delta"  float      The greek value, if not calculated = -1
    "Gamma"  float      The greek value, if not calculated = -1
    "Theta"  float      The greek value, if not calculated = -1}
----------------------------------------------------------------------------"""   
def TheorBarrierOption(i, vanilla_params, barrier_params, digital_params, quanto_params, val_meth_params):
    try:
        try: 
            if float(vanilla_params[2]) < 0.0:
                return {"PV":'Negative volatility!'}
        except: return {"PV":'No volatility!'}
        bp = FBarrierParams(vanilla_params, barrier_params, digital_params, quanto_params)
        bp.df = get_discount_factor(i) 
        try: 
            if float(bp.price) == 0.0:
                return {"PV":'No underlying price!'}
        except: return {"PV":'No underlying price!'}
        res = FEqBarrierUtils.get_pv(bp, val_meth_params)
        return check_has_greeks(res)
    except F_BARRIER_EXCEPT, msg:
        print '\nModule: FEqBarrierPRIME'
        print 'Error :', msg
        print 'Instr :', i.insid
        return {"PV":'Valuation error!'}
        
def TheorDblBarrierOption(i, vanilla_params, barrier_params, digital_params, second_barrier, quanto_params, val_meth_params):
    try:
        try: 
            if float(vanilla_params[2]) < 0.0:
                return {"PV":'Negative volatility!'}
        except: return {"PV":'No volatility!'}
        dbp = FBarrierParams(vanilla_params, barrier_params, digital_params, quanto_params)
        dbp.second_barrier = second_barrier
        dbp.df = get_discount_factor(i) 
        try: 
            if float(dbp.price)== 0.0:
                return {"PV":'No underlying price!'}
        except: return {"PV":'No underlying price!'}
        res = FEqBarrierUtils.get_double_pv(dbp, AsList(val_meth_params))
        return check_has_greeks(res)
    except F_BARRIER_EXCEPT, msg:
        print '\nModule: FEqBarrierPRIME'
        print 'Error :', msg
        print 'Instr :', i.insid
        return {"PV":'Valuation error!'}






