""" SEQ_VERSION_NR = 2.3.1 """


"""-----------------------------------------------------------------------------
MODULE
    FEqRainbowMin
        
    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    Computes the value of a European call / put on the maximum of two assets.
    
EXTERNAL DEPENDENCIES
    FRainbowParams        

REFERENCES
    Espen Gaarder Haug, (1997)
    "The Complete Guide To Option Pricing Formulas"
    McGraw-Hill, see page 56-58.

-----------------------------------------------------------------------------"""
import math
import ael 
import FRainbowParams 

F_RAINBOW_EXCEPT  = 'f_eq_rainbow_xcp'  
F_RAINBOW_WARNING = 'f_eq_rainbow_warning'  

EXPIRES_TODAY_WARNING = 'the option expires today.'
EXPIRED_WARNING = 'the option has already expired.'
"""----------------------------------------------------------------------------
CLASS                   
    FRainbowMinParams - Parameters for rainbow maximum of two options

INHERITS
    FRainbowParams
                
DESCRIPTION             
    The class extracts all parameters needed to value a rainbow maximum of two option.

CONSTRUCTION    
    i               Instrument  An instrument that is a rainbow maximum of two option

----------------------------------------------------------------------------"""
class FRainbowMinParams(FRainbowParams.FRainbowParams):
    def __init__(self, i):
        FRainbowParams.FRainbowParams.__init__(self, i)
            
    def call_on_the_min(self):
        res = self.price_vol_part[0]*math.exp((self.carry_cost[0] - self.rate)*self.texp)* \
              self.bivar_normal_dist(self.y1, -self.d, -self.rho1) + \
              self.price_vol_part[1]*math.exp((self.carry_cost[1] - self.rate)* \
              self.texp)*self.bivar_normal_dist(self.y2, self.d - self.sigma*math.sqrt(self.texp), -self.rho2) - \
              self.strike*math.exp(-self.rate*self.texp)*self.bivar_normal_dist(self.y1 - \
              self.vol[0]*math.sqrt(self.texp), self.y2 - self.vol[1]*math.sqrt(self.texp), self.rho) 
        return res

    def put_on_the_min(self):
        call_K0 = self.price_vol_part[0]*math.exp((self.carry_cost[0] - self.rate)*self.texp)* \
                  ael.normal_dist(-self.d) + self.price_vol_part[1]*math.exp((self.carry_cost[1] - \
                  self.rate)*self.texp)*ael.normal_dist(self.d - self.sigma*math.sqrt(self.texp))
        call_K = self.call_on_the_min()
        res = self.strike*math.exp(-self.rate*self.texp) - call_K0 + call_K 
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
            if self.put_call:
                # The option is a call
                res = self.call_on_the_min()      
            else:
                # The option is a put
                res = self.put_on_the_min()
            return res
            
        # Handling warnings
        except F_RAINBOW_WARNING, msg:
            if msg == EXPIRES_TODAY_WARNING:
                res = max(self.fi*(min(self.Sw0, self.Sw1) - self.strike), 0)
                return res
            elif msg == EXPIRED_WARNING:
                return 0.0
            else:
                print
                print 'Module: FEqRainbowMin'
                print 'Error : ', msg
                print 'Instr : ', self.insid
                return 0
         
        # Handling exceptions                
        except F_RAINBOW_EXCEPT, msg:
            print
            print 'Module: FEqRainbowMin'
            print 'Error : ', msg
            print 'Instr : ', self.insid
            return 0



"""----------------------------------------------------------------------------
FUNCTION        
    pv() 
    
DESCRIPTION
    Calculates the present value of a Rainbow Minimum of two option. 

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
        if not (i.category_chlnbr.entry == 'RainbowMin'):
            print 'WARNING: RainbowMin valuation, but category not set to RainbowMin valuation'
    except:
        print 'WARNING: No Category choosen for instrument', i.insid
    if calc:
        if i.exp_day < ael.date_valueday():
            res = 0
        else:
            rmp = FRainbowMinParams(i)                                                
            res = rmp.pv() 
    else: res = 0
    return [[ res, i.exp_day.add_days(i.pay_day_offset), i.curr, 'Fixed' ]] 























