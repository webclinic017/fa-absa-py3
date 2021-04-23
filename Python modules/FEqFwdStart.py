""" SEQ_VERSION_NR = PRIME 2.8.1 """




"""--------------------------------------------------------------------------
DESCRIPTION
    Computes the value of a Forward start.     
    
    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.
    
EXTERNAL DEPENDENCIES
    FCliquetParams        

-----------------------------------------------------------------------------"""
LOG_PARAMETERS = 0

import ael
import math
import FEqCliquet
import FEqCliquetUtils

F_CLIQUET_EXCEPT        = 'f_eq_cliquet_fwdstart_xcp'       
F_FWDSTART_WARNING      = 'f_eq_fwdstart_warning'

counter = 0

"""----------------------------------------------------------------------------
CLASS                   
    FFwdStartParams - Parameters for forward start and forward start performance 
                      options.

INHERITS
    FCliquetParams
                
DESCRIPTION             
    The class extracts all parameters needed to value a forward start or a 
    forward start performance option. The class also includes a present value
    valuation function.

CONSTRUCTION    
    i               Instrument  An instrument that is a forward start option.
----------------------------------------------------------------------------"""
class FFwdStartParams(FEqCliquet.FCliquetParams):
    def __init__(self, i):
        FEqCliquet.FCliquetParams.__init__(self, i)
        if (i.exercise_type == 'American') or (i.exercise_type == 'Bermudan') or not(i.exotic_type == 'None'): 
            print "\n## !! EXCEPTION !! ##"
            raise F_CLIQUET_EXCEPT, 'FEqFwdStart only handles plain European options.'
        if i.digital: 
            print "\n## !! EXCEPTION !! ##"
            raise F_CLIQUET_EXCEPT, 'FEqFwdStart does not handle digital options.'
        if not(i.und_instype == 'Stock' or i.und_instype == 'EquityIndex' or i.und_instype == 'Curr'):
            print "\n## !! EXCEPTION !! ##"
            raise F_CLIQUET_EXCEPT, 'FEqCliquetEnd only handles Stock, EquityIndex and Currency as underlying instrument' 
        
    def pv(self):
        val_meth_params = FEqCliquetUtils.fwdstart_val_meth(self.dividends)
        res = FEqCliquetUtils.get_fwdstart_pv(self, val_meth_params)
        res = res * self.strike_theor_curr_fx
        return res

            
"""----------------------------------------------------------------------------
FUNCTION    
    pv() 

DESCRIPTION
    The function pv() calculates the price of a forward start option. 

ARGUMENTS
    i       Instrument  Forward start Option
    calc    Integer     0=>No calculation 1=>Perform calculation
    ref                 Optimisation parameter

RETURNS
   [res     float       Value of instrument
    exp_day date        Maturity date
    curr    string      Currency in which it was valued
    Fixed   string      Constant = 'Fixed']                      
----------------------------------------------------------------------------"""
def pv(i, calc, ref):
    extra_days = 0
    if calc:
        try:
            if i.add_info('FFwdStartDay') == '': 
                print "\n## !! NO VALUE !! ##"
                raise F_CLIQUET_EXCEPT, "No forward start day is given for the instrument. Please enter a date in the AdditionalInfo field FFwdStartDay."
            if i.add_info('FFwdStart') == '': 
                print "\n## !! NO VALUE !! ##"
                raise F_CLIQUET_EXCEPT, "Select forward type; forward start or forward start performance, in the Additional Info field FFwdStart."
            if i.add_info('FFwdStartAlpha') == '': 
                print "\n## !! NO VALUE !! ##"
                raise F_CLIQUET_EXCEPT, "No forward start alpha is given for the instrument. Please enter an alpha in the AdditionalInfo field FFwdStartAlpha."
            if float(i.add_info('FFwdStartAlpha')) <= 0.0: 
                print "\n## !! EXCEPTION !! ##"
                raise F_CLIQUET_EXCEPT, "Forward start alpha must be strictly larger than 0.0. Please update the AdditionalInfo field FFwdStartAlpha."
            fp = FFwdStartParams(i)
            if globals()['counter'] == 5: globals()['counter'] = 0
            try: print_info = i.add_info("FPrintInfo")
            except: print_info = ""
            if (LOG_PARAMETERS or print_info == "Yes") and globals()['counter'] == 0:
                if fp.texp > 0: print get_info(fp)
                else: print "\n## !! OPTION " + i.insid + " HAS EXPIRED !! ##"
            globals()['counter'] = globals()['counter'] + 1
            if fp.reset_times[0] < 0 and fp.last_reset_price == 0:
                print "\n## !! NO VALUE !! ##"
                raise F_CLIQUET_EXCEPT, "Forward start day is in the past but no strike price is given."
            if i.exp_day < ael.date_valueday():  res = 0.0
            else: res = fp.pv()
            extra_days = fp.extra_days
        except F_CLIQUET_EXCEPT, msg:
            print '\nModule:  FEqFwdStart'
            print 'Error : ', msg
            print 'Instr : ', i.insid
            res = 0.0
    else: res = 0.0
    return [[ res, i.exp_day.add_days(extra_days), i.curr, 'Fixed' ]] 


def get_info(ForwardStartParams):
    fp = ForwardStartParams
    s = ''
    s = s + "Instrument: \t" + fp.insid + "\t is using parameter(s): \n"  
    s = s + "\t\n"
    for curve in fp.yield_curves:
        if curve[0] == 'Repo': insid = fp.insid
        elif curve[0] == 'Discount': insid = fp.underlying
        else: insid = fp.underlying
        s = s + "Yield curve:\t" + str(curve[1]) + " for " + str(curve[0]) + " (" + insid + ", " + fp.currency + ")\n" 
    s = s + "\t\n"
    s= s + "Volatility:\t" + str(fp.vol_surface) + "\t(" + fp.insid + ")\n"
    s = s + "\t\n"  
    s = s + "Used repo rate:\t\t%*.*f" % (6, 4, fp.repo*100) + "\n"
    s = s + "Used volatility:\t%*.*f" % (6, 4, fp.vol[0]*100)  + "\n"
    s = s + "Used discount rate:\t%*.*f" % (6, 4, fp.rate[0]*100) + "\n"
    s = s + "\t\n" 
    s = s + "Forward start day:\t" + str(fp.start_day) + "\n"
    s = s + "Forward start alpha:\t" + str(fp.alpha) + "\n"
    s = s + "Forward strike:\t\t" + str(fp.fwd_strike) + "\n"
    if fp.performance: flag = "Yes"
    else: flag = "No"
    s = s + "Forward start perf.:\t" + flag + "\n"
    
    [val_meth, steps] = FEqCliquetUtils.fwdstart_val_meth(fp.dividends)
    s = s + "\t\n"
    s = s + "Valuation method:\t" + str(val_meth) + "\n"
    if val_meth != "analytical":
        s = s + "Steps:\t\t\t" + str(steps) + "\n"
    s = s + "\t\n" 
    s = s + "Underlying:\t\t" + fp.underlying + "\n"
    s = s + "Underlying price:\t" + str(fp.price) + "\n"

    if fp.dividends != []:
        s = s + "\t\n"
        s = s + "Underlying Dividends (in " + fp.currency + ") :\n"
        s = s + "\t\tEx Div Day \tRecord Day \tAmount \tTax Factor\n"
        for d in fp.div_entity:
            s = s + "\t\t" + str(d.ex_div_day) + "\t" + str(d.day) + "\t" + str(d.dividend) + "\t" + str(d.tax_factor) + "\n"
    s = s + "\t\n"
    s = s + "Used valuation function:FEqFwdStart.pv \n"
    s = s + "Mapped in context:\t" + fp.used_context + "\n"
    s = s + "\t\n" + "\t\n"
    return s   










