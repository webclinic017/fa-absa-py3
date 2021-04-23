""" SEQ_VERSION_NR = 2.3.1 """


"""--------------------------------------------------------------------------
DESCRIPTION
    Computes the value of a Cliquet pay at the end. 
    
    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

EXTERNAL DEPENDENCIES
    FCliquetParams       
    f_eq_fwdstart.dll

NOTE
    To print the valuation parameters of cliquet end options in the AEL console, 
    set LOG_PARAMETERS = 1. The information will be printed next time the 
    instrument is opened.
    
    This flag can be helpful when setting up the instrument. Thereafter, 
    LOG_PARAMETERS should once again be set to 0 to make sure that performance
    is not worsened.

-----------------------------------------------------------------------------"""
LOG_PARAMETERS = 0

import ael
import sys
import math
import FCliquetParams
import FEqCliquetUtils
import FTimeSeries

counter = 0

F_CLIQUET_EXCEPT        = 'f_eq_cliquet_xcp'    
F_CLIQUET_WARNING       = 'f_eq_cliquet_warning'

class FCliquetEndParams(FCliquetParams.FCliquetParams):
    def __init__(self, i):
        FCliquetParams.FCliquetParams.__init__(self, i)
        if (i.exercise_type == 'American') or (i.exercise_type == 'Bermudan') or not(i.exotic_type == 'None'): 
            raise F_CLIQUET_EXCEPT, 'Valuation only handles plain European options.'
        if i.digital: 
            raise F_CLIQUET_EXCEPT, 'FEqCliquetEnd does not handle digital options.'
        if not(i.und_instype == 'Stock' or i.und_instype == 'EquityIndex' or i.und_instype == 'Curr'):
            raise F_CLIQUET_EXCEPT, 'Valuation only handles Stock, EquityIndex and Currency as underlying instrument' 

    def pv(self):
        val_meth_params = FEqCliquetUtils.fwdstart_val_meth(self.dividends)
        res = FEqCliquetUtils.cliquet_end_pv(self, val_meth_params)
        return res*self.strike_theor_curr_fx


"""----------------------------------------------------------------------------
FUNCTION    
    pv() 

DESCRIPTION
    The function pv() calculates the price of a cliquet pay
    at the end option. 

ARGUMENTS
    i       Instrument  Cliquet Option
    calc    Integer     0=>No calculation 1=>Perform calculation
    ref                 Optimisation parameter

RETURNS
   [res     float       Value of instrument
    exp_day date        Maturity date
    curr    string      Currency in which it was valued
    Fixed   string      Constant = 'Fixed']                      
----------------------------------------------------------------------------"""
def pv(i, calc, ref):
    try:
        if calc:
            cep = FCliquetEndParams(i)
            try:print_info = i.add_info("FPrintInfo")
            except: print_info = ""
            if globals()['counter'] == 5: globals()['counter'] = 0
            if (LOG_PARAMETERS or print_info == "Yes") and globals()['counter'] == 0:
                if cep.texp > 0: print get_info(cep)
                else: print "\n## !! OPTION " + i.insid + " HAS EXPIRED !! ##"
            globals()['counter'] = globals()['counter'] + 1
            if i.exp_day < ael.date_valueday():  res = 0.0
            else:
                reset_dates_tot = FTimeSeries.get_TimeSeries(i, 'FCliquetResetDays', FCliquetParams.F_CLIQUET_TIMESERIESRUN)
                if len(reset_dates_tot) == 0:
                    print "\n## !! NO VALUE !! ##"
                    raise F_CLIQUET_EXCEPT, "No reset dates are given. Create them with the ASQL application .MaintCreateCliquetResets."
                res = cep.pv() 
        else: res = 0.0
    except F_CLIQUET_EXCEPT, msg: 
        print
        print 'Module:  FEqCliquetEnd'
        print 'Error : ', msg
        print 'Instr : ', i.insid
        res = 0.0

    return [[ res, i.exp_day.add_days(i.pay_day_offset), i.curr, 'Fixed' ]] 



"""----------------------------------------------------------------------------
get-info()                   
    The function returns a string with valuation parameters.
----------------------------------------------------------------------------"""
def get_info(CliquetEndParams):
    cp = CliquetEndParams
    s = cp.get_info()

    [val_meth, steps] = FEqCliquetUtils.fwdstart_val_meth(cp.dividends)
    s = s + "Valuation method:\t\t" + str(val_meth) + "\n"
    if str(val_meth) != "analytical":
        s = s + "Steps:\t\t\t\t" + str(steps) + "\n"
    s = s + "\t\n" 
    s = s + "Used valuation function: \tFEqCliquetEnd.pv \n"
    s = s + "Mapped in context:\t\t" + cp.used_context + "\n"
    s = s + "\t\n" + "\t\n"
    return s   









