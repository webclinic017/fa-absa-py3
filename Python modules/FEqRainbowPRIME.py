""" SEQ_VERSION_NR = PRIME 2.8.1 """




"""-----------------------------------------------------------------------------
MODULE
    FEqRainbowPRIME - Rainbow options are valued. PRIME calls the valuation.
        
    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
   Calculates the price of a rainbow option. 
   
-----------------------------------------------------------------------------"""
import ael
import math
import FEqRainbowUtils
from FEqUtilsPRIME import *


F_RAINBOW_EXCEPT  = 'f_eq_rainbow_xcp'  

rainbow_type_dict = {0:FEqRainbowUtils.RAINBOW_MAX,1:FEqRainbowUtils.RAINBOW_MIN,\
                     2:FEqRainbowUtils.RAINBOW_BOT,3:FEqRainbowUtils.RAINBOW_WOT}

"""----------------------------------------------------------------------------
FRainbowParams
    The class contains all valuation parameters necessary for rainbow option val.
----------------------------------------------------------------------------"""    
class FRainbowParams:
    def __init__(self, vanilla_params, rainbow_params):
        # Plain vanilla parameters
        self.texp           = vanilla_params[1]
        self.rate           = vanilla_params[3]
        self.strike         = vanilla_params[6]
        self.put_call       = vanilla_params[7]
        exc_type            = vanilla_params[8]
        if exc_type == 'European':self.eur_ame = 0
        else: self.eur_ame = 1
        
        # Rainbow parameters
        self.price          = AsList(rainbow_params[0])
        self.vol            = AsList(rainbow_params[1])
        self.rho            = rainbow_params[2]
        self.carry_cost     = AsList(rainbow_params[3])
        self.weights        = AsList(rainbow_params[4])
        self.dividends      = AsMatrix(rainbow_params[5])
        und_instrs          = AsList(rainbow_params[6])
        rainbow_type_number = rainbow_params[7]
        self.rainbow_type   = rainbow_type_dict[rainbow_type_number]
        if self.rainbow_type == "":
            print "\n## !! EXCEPTION !! ##"
            raise F_RAINBOW_EXCEPT, "No Rainbow type is chosen in the Additional Info field 'FRainbowType'."
        self.rate_stocks    = AsList(rainbow_params[8])
        self.dim            = len(self.price)   
        
        if self.texp == 0.0:
            self.Sw0 = und_instrs[0].weight*und_instrs[0].member_insaddr.used_price()
            self.Sw1 = und_instrs[1].weight*und_instrs[1].member_insaddr.used_price()
            self.fi = -1 + 2*(self.put_call == 1) 
        
        
"""----------------------------------------------------------------------------
FUNCTION    
    TheorRainbowOption() 

DESCRIPTION
    The function, which is called from PRIME, calculates the price of a rainbow option. 
    
ARGUMENTS
    vanilla_params[]      A list with all standard vanilla parameters, like price.
    rainbow_params[]      A list with rainbow specific parameters. 

RETURNS
    res       float     Value of instrument
----------------------------------------------------------------------------"""   
def TheorRainbowOption(i, vanilla_params, rainbow_params):
    try:
        rp = FRainbowParams(vanilla_params, rainbow_params)
        rp.df = get_discount_factor(i) 
        for p in rp.price:
            try: float(p)
            except: return {"PV":"No underlying price!"}   
        try:
            if abs(rp.rho) > 1:
                return {"PV":"The correlation's absolute value is greater than one!"}
        except: 
            print "## !! EXCEPTION !! ##"
            raise F_RAINBOW_EXCEPT, rp.rho
        res = FEqRainbowUtils.get_rainbow_pv(rp)
        return {"PV":res, "Delta":"theorGlobalBasketDelta", "DeltaPct":"theorGlobalBasketDeltaPct",\
                "Gamma":"theorGlobalBasketGamma","GammaPct":"theorGlobalBasketGammaPct",\
                "Vega":"theorGlobalVega"}
    except F_RAINBOW_EXCEPT, msg: 
        print '\nModule:  FEqRainbowPRIME'
        print 'Error : ', msg
        print 'Instr : ', i.insid
        return {"PV":'Valuation error!'}
    
    


