""" SEQ_VERSION_NR = 2.3.1 """


"""-----------------------------------------------------------------------------
MODULE
    FEqRainbowBOT
        
    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    Computes the value of a European best of two or cash option.     

EXTERNAL DEPENDENCIES
    FRainbowParams        
    FEqRainbowMax

-----------------------------------------------------------------------------"""
import math
import ael 
import FEqRainbowMax

F_RAINBOW_EXCEPT  = 'f_eq_rainbow_xcp'  
F_RAINBOW_WARNING = 'f_eq_rainbow_warning' 

EXPIRES_TODAY_WARNING = 'the option expires today.'
EXPIRED_WARNING = 'the option has expired'
"""----------------------------------------------------------------------------
CLASS                   
    FRainbowBOTParams - Parameters for rainbow best of two options

INHERITS
    FRainbowParams
                
DESCRIPTION             
    The class extracts all parameters needed to value a rainbow best of two option.

CONSTRUCTION    
    i               Instrument  An instrument that is a rainbow best of two option.
----------------------------------------------------------------------------"""
class FRainbowBOTParams(FEqRainbowMax.FRainbowMaxParams):
    def __init__(self, i):
        FEqRainbowMax.FRainbowMaxParams.__init__(self, i)
        
    def best_of_two_or_cash(self):
        res = self.strike*math.exp(-self.rate*self.texp) + self.call_on_the_max()
        return res
    
    def pv(self):
        try:
            if self.texp == 0.0:
                raise F_RAINBOW_WARNING, EXPIRES_TODAY_WARNING   
            if self.texp < 0.0:
                raise F_RAINBOW_WARNING, EXPIRED_WARNING
                
            self.price_vol_part[0] = self.weights[0]*self.price_vol_part[0]
            self.price_vol_part[1] = self.weights[1]*self.price_vol_part[1]
            self.rainbow_val_params(self.price_vol_part)
            res = self.best_of_two_or_cash()   
            return res

        # Handling warnings      
        except F_RAINBOW_WARNING, msg:
            if msg == EXPIRES_TODAY_WARNING:
                res = self.df*max(max(self.Sw0, self.Sw1), self.strike)
                return res
            elif msg == EXPIRED_WARNING:
                print "The rainbow option is expired."
                return 0.0
            else:
                print
                print 'Module: FEqRainbowBOT'
                print 'Error : ', msg
                print 'Instr : ', self.insid
                return 0

        # Handling exceptions                
        except F_RAINBOW_EXCEPT, msg:
            print
            print 'Module: FEqRainbowBOT'
            print 'Error : ', msg
            print 'Instr : ', self.insid
            return 0
            
        
"""----------------------------------------------------------------------------
FUNCTION        
    pv() 
    
DESCRIPTION
    Calculates the present value of a Rainbow Best of two option. 

ARGUMENTS
    i           Instrument      Best of two Option
    calc        Integer(01)    0->No calculation 1->Perform calculation
    ref                         Optimisation parameter

RETURNS
   [res         Float           Value of instrument
    expday      Date            Maturity date
    curr        String          Currency in which it was valued
    fixed       String          Constant = 'Fixed']                                     
----------------------------------------------------------------------------"""
def pv(i, calc, ref):
    try:
        if not (i.category_chlnbr.entry == 'RainbowBOT'):
            print 'WARNING: RainbowBOT valuation, but category not set to RainbowBOT valuation'
    except:
            print 'WARNING: No Category choosen for instrument', i.insid
    if calc:
        if i.exp_day < ael.date_valueday():
            res = 0
        else:
            try:
                rbp = FRainbowBOTParams(i)                                                
                res = rbp.pv() 
            except F_RAINBOW_EXCEPT, msg:
                print
                print 'Module: FEqRainbowBOT'
                print 'Error : ', msg
                print 'Instr : ', i.insid
                res = 0.0
    else: res = 0
    return [[ res, i.exp_day.add_days(i.pay_day_offset), i.curr, 'Fixed' ]] 
















