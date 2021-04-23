""" SEQ_VERSION_NR = PRIME 2.8.1 """




"""----------------------------------------------------------------------------
MODULE
    FEqLadderPRIME - Ladder options are valued. PRIME calls the valuation.
    
    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
   Calculates the price of a ladder option. European options with discrete 
   dividends are handled.
 
----------------------------------------------------------------------------"""
import ael
import sys
import FEqBarrierUtils
import FEqLadderUtils
from FEqUtilsPRIME import *

# The timeseries where barrier monitor dates are stored.
F_BARRIER_EXCEPT        = 'f_eq_barrier_xcp' 
F_LADDER_EXCEPT         = 'f_eq_ladder_xcp'

"""----------------------------------------------------------------------------
FLadderParams 
    The class holds all necessary parameters for ladder valuation.
----------------------------------------------------------------------------"""    
class FLadderParams:
    def __init__(self, vanilla_params, ladder_params):
        # Standard Params
        self.price      = vanilla_params[0]
        self.texp       = vanilla_params[1]
        self.vol        = vanilla_params[2]
        self.rate       = vanilla_params[3]
        self.carry_cost = vanilla_params[4]
        self.strike     = vanilla_params[6]
        self.put_call   = vanilla_params[7]
        exc_type        = vanilla_params[8]
        if exc_type == 'European' or exc_type == 0:self.eur_ame = 0
        else: self.eur_ame = 1
        
        # Ladder option params
        self.discrete_barr         = ladder_params[0]
        self.barr_dates            = AsList(ladder_params[1])
        self.barr_monitoring_times = ladder_params[2]
        self.dividends             = AsList(ladder_params[3])
        self.barr_freq             = ladder_params[4]
        self.rungs                 = ladder_params[5]
        if self.rungs == (): 
            print "\n## !! EXCEPTION !! ##"
            raise F_LADDER_EXCEPT, "No rungs are given."
        elif str(type(self.rungs)) == "<type 'str'>":
            print "\n## !! EXCEPTION !! ##"
            raise F_LADDER_EXCEPT, self.rungs
            
        self.vanilla_res           = ladder_params[6]
        self.knocked               = ""
        self.knocked_date          = ""
        self.pay_rebate            = ""
        self.settlement            = ""
        self.fix_fx                = 0

"""----------------------------------------------------------------------------
FUNCTION    
    TheorLadderOption() 

DESCRIPTION
    The function calculate the price of a ladder option.
    
ARGUMENTS
    vanilla_params[]    A list with all standard vanilla parameters, like strike.
    barrier_params[]    A list with barrier specific parameters. 
    ladder_params[]     A list with digital parameters.
    val_meth_params[]   A list with valuation method (string) and the number of 
                        steps to use in the numerical valuation.

RETURNS
   PV     float      Value of instrument
----------------------------------------------------------------------------"""   
def TheorLadderOption(i, vanilla_params, ladder_params):
    try:
        try: 
            if float(vanilla_params[0]) == 0.0:
                return {'PV':'No underlying price!'}
        except: return {'PV':'No underlying price!'}
        lp = FLadderParams(vanilla_params, ladder_params)
        lp.df = get_discount_factor(i) 
        res = FEqLadderUtils.get_ladder_pv(lp, 1)
        return res
    except F_BARRIER_EXCEPT, msg:
        raise F_LADDER_EXCEPT, msg
    except F_LADDER_EXCEPT, msg:
        print '\nModule: FEqLadderPRIME'
        print 'Error :', msg
        print 'Instr :', i.insid
        return {'PV':'Valuation error!'}
        
















