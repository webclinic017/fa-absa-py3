""" SEQ_VERSION_NR = PRIME 2.8.1 """




"""-----------------------------------------------------------------------------
MODULE
    FEqFwdStartPRIME - Forward Start options are valued. PRIME calls the valuation.
        
    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
   Calculates the price of a forward start option. 
   
NOTE
   At the forward start day, the strike price must be manually set in the 
   Instrument definition window. 

-----------------------------------------------------------------------------"""
import ael
import FEqCliquetUtils
import FTimeSeries
import sys
import math
from FEqUtilsPRIME import *

F_CLIQUET_EXCEPT = 'f_eq_cliquet_fwdstart_xcp'   
F_CLIQUET_END = "Cliquet End"
F_CLIQUET_GO = "Cliquet Go"

"""----------------------------------------------------------------------------
get_discount_factors
    The function returns a vector with all discount factors
----------------------------------------------------------------------------"""    
def get_discount_factors(i, reset_dates):
    if str(type(reset_dates)) == "<type 'str'>":
        return []
    df = []
    yc = i.used_yield_curve(i.curr)
    for date in reset_dates[1:]:
        exp_offset = date.add_banking_day(i.curr, i.pay_day_offset)
        rf_exp = yc.yc_rate(date, exp_offset, 'Annual Comp', 'Act/365', 'Spot Rate')
        toffset = date.years_between(exp_offset, 'Act/365')
        df.append(math.pow(1+rf_exp, -toffset))
    return df

def get_carry_factor(i, reset_date):
    valuation_date_offset = ael.date_valueday().add_banking_day(i.und_insaddr.curr, i.und_insaddr.spot_banking_days_offset)
    exp_offset = reset_date.add_banking_day(i.curr, i.pay_day_offset)
    texp_carry = valuation_date_offset.years_between(exp_offset, 'Act/365')
    temp       = ael.date_valueday().years_between(reset_date, 'ACT/365')
    if temp != 0.0:
        carry_factor = texp_carry/temp
    else:
        carry_factor = 0.0
    return carry_factor
                    
"""----------------------------------------------------------------------------
FFwdStartParams
    The class contains all valuation parameters necessary for fwdstart option val.
----------------------------------------------------------------------------"""    
class FFwdStartParams:
    def __init__(self, vanilla_params, fwd_start_params):
        self.reset_times = []
        
        # Fwd Start params
        self.dividends        = AsList(fwd_start_params[0])
        self.reset_times.append(fwd_start_params[3])   # Time to forward start day
        self.last_reset_price = fwd_start_params[4]    # Forward strike
        self.alpha            = fwd_start_params[5]
        self.vol              = [fwd_start_params[6]]
        self.performance      = fwd_start_params[7]

        # Plain vanilla parameters
        self.price          = vanilla_params[0]
        self.reset_times.append(vanilla_params[1])     # Time to expiry
        self.rate           = [vanilla_params[3]]
        self.carry_cost     = [vanilla_params[4]]
        self.put_call       = vanilla_params[7]
        exc_type            = vanilla_params[8]
        if exc_type == 'European':self.eur_ame = 0
        else: self.eur_ame = 1

        
        if self.performance == "Fwd Start Perf":self.performance = 1
        elif self.performance == "Fwd Start": self.performance = 0
    
"""----------------------------------------------------------------------------
FCliquetParams
    The class contains all valuation parameters necessary for cliquet option val.
----------------------------------------------------------------------------"""    
class FCliquetParams:
    def __init__(self, vanilla_params, cliquet_params):
        # Plain vanilla parameters
        self.price          = vanilla_params[0]
        self.texp           = vanilla_params[1]
        self.put_call       = vanilla_params[7]
        exc_type            = vanilla_params[8]
        if exc_type == 'European':self.eur_ame = 0
        else: self.eur_ame = 1
        
        # Cliquet params
        self.dividends        = AsList(cliquet_params[0])
        self.alpha            = cliquet_params[1]
        self.performance       = cliquet_params[2]
        self.rate             = AsList(cliquet_params[3][1:])
        self.df               = AsList(cliquet_params[4])
        self.first_reset_occured = cliquet_params[5]
        try: 
            if cliquet_params[6] != (): float(cliquet_params[6][0])
        except:
            print "\n## !! EXCEPTION !! ##"
            raise F_CLIQUET_EXCEPT, cliquet_params[6]
        self.reset_prices     = AsList(cliquet_params[6])
        self.reset_times      = AsList(cliquet_params[7])
        self.vol              = AsList(cliquet_params[8])
        self.carry_cost       = AsList(cliquet_params[9][1:])
        self.last_reset_price = cliquet_params[10]
        self.cliquet_type     = cliquet_params[11]
        
        if self.cliquet_type == 0: self.cliquet_type = F_CLIQUET_GO
        elif self.cliquet_type == 1:self.cliquet_type = F_CLIQUET_END
        else: self.cliquet_type = -1
        
        if self.performance == "Fwd Start Perf":self.performance = 1
        elif self.performance == "Fwd Start": self.performance = 0

        
"""----------------------------------------------------------------------------
FUNCTION    
    TheorFwdStartOption() 

DESCRIPTION
    The function, which is called from PRIME, calculates the price of a forward 
    start option. 
    
ARGUMENTS
    vanilla_params[]      A list with all standard vanilla parameters, like price.
    fwd_start_params[]    A list with fwd start specific parameters. 
                            - dividends:        Vector with future dividends
                            - steps:            The number of steps to use if 
                                                a numerical valuation method 
                                                is chosen.
                            - val_meth          The name of the chosen 
                                                valuation method.
                            - fwd_day_texp:     Time to expiry based on the 
                                                forward start day.
                            - fwd_strike:       If fwd_start_day > today => -1
                                                Else: strike / fwd_alpha
                            - fwd_alpha:        The strike multiplier.
                            - fwd_vol:          The forward volatlity.
                          

RETURNS
    res       float     Value of instrument
----------------------------------------------------------------------------"""   
def TheorFwdStartOption(i, vanilla_params, fwd_start_params):
    steps        = fwd_start_params[1]
    val_meth     = fwd_start_params[2]
    try:
        try: 
            if float(vanilla_params[0]) == 0.0:{"PV":'No underlying price!'}
        except: return {"PV":'No underlying price!'}
        fp = FFwdStartParams(vanilla_params, fwd_start_params)
        fp.df = [get_discount_factor(i)] 
        if fp.reset_times[0] < 0 and fp.last_reset_price == 0:
            return {"PV":"Forward start day is in the past but no strike price is given."}
        if float(i.add_info('FFwdStartAlpha')) <= 0.0: 
            return {"PV":"Forward start alpha must be strictly larger than 0.0!"}
        val_meth_params = [val_meth, steps]
        res = FEqCliquetUtils.get_fwdstart_pv(fp, val_meth_params)
        return {"PV":res, "Vega":"fwdstartNumericalVega"}
    except F_CLIQUET_EXCEPT, msg: 
        print '\nModule: FEqFwdStartPRIME'
        print 'Error :', msg
        print 'Instr :', i.insid
        return {"PV":'Valuation error!'}
    
    
"""----------------------------------------------------------------------------
FUNCTION    
    TheorCliquet() 

DESCRIPTION
    The function, which is called from PRIME, calculates the price of a cliquet 
    option. 
    
ARGUMENTS
    vanilla_params[]      A list with all standard vanilla parameters, like price.

RETURNS
    res       float     Value of instrument
----------------------------------------------------------------------------"""   
def TheorCliquetOption(i, vanilla_params, cliquet_params, val_meth_params):
    try:
        try: 
            if float(vanilla_params[0]) == 0.0: return {"PV":'No underlying price!'}
        except: return {"PV":'No underlying price!'}
        reset_dates_tot = FTimeSeries.get_TimeSeries(i, 'FCliquetResetDays', 0)
        if reset_dates_tot == []: return {"PV":'No Time Series is created for the instrument!'}
        cp = FCliquetParams(vanilla_params, cliquet_params)
        if cp.cliquet_type == -1: return {"PV":'Cliquet type is not selected!'}
        reset_dates_tot = FTimeSeries.get_TimeSeries(i, 'FCliquetResetDays', 0)
        res = FEqCliquetUtils.cliquet_pv(cp, val_meth_params)
        return {"PV":res, "Vega":"cliquetVega"} 
    except F_CLIQUET_EXCEPT, msg: 
        print '\nModule: FEqFwdStartPRIME'
        print 'Error :', msg
        print 'Instr :', i.insid
        return {"PV":'Valuation error!'}




