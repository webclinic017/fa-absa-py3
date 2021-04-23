""" SEQ_VERSION_NR = PRIME 2.8.1 """




"""-----------------------------------------------------------------------------
MODULE
    FEqRainbow - Values a rainbow option
        
    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    Extracts and computes parameters for an instrument of rainbow
    type, that is, Call (or Put) on the minimum (or maximum)
    of two assets, minimum (or maximum) for two assets or cash 
    and Basket options.
-----------------------------------------------------------------------------"""
LOG_PARAMETERS = 0

import ael 
import math
import sys
import FEqBasket
import FEqBasketUtils
import FEqRainbowUtils

F_RAINBOW_EXCEPT  = 'f_eq_rainbow_xcp'  
F_RAINBOW_WARNING = 'f_eq_rainbow_warning'  
F_BASKET_EXCEPT = 'f_eq_basket_xcp' 

# INFINITY is considered to be 'infinity' in the sense that the normal distribution N(x)
# is approximately equal to 1 for all x greater than INFINITY.
INFINITY = 6.0
PI = 3.14159265358979

counter = 0

"""----------------------------------------------------------------------------
CLASS                   
    RainbowParams - Parameters for rainbow type options

INHERITS
    FOptionParams
                
DESCRIPTION             
    The class extracts all parameters needed to value a basket option.

INCLUDES 
    FRainbowParams          Extracts the necessery parameters to value rainbow options.
    volpart                 computes the sum of all future dividends 
                            (paid out before maturity).
    sign                    gives the sign of a number.
    bivar_normal_dist       computes the bivariate normal distribution.
    RainbowValParams        computes certain parameters which are needed to price 
                            two colour rainbow options.
    vol_corr_rainbow        extracts volatilities and correlations for the underlying
                            assets of (two colour) rainbow options.

CONSTRUCTION    
    i              Instrument   An instrument that is of rainbow type.

MEMBERS                 
    vol[]          Float        A vector with the volatilities of the two rainbow 
                                instruments.    
    rho            Float        The correlation between the two instruments.
    y1             Float        Rainbow formula calculation parameter.
    y2             Float        Rainbow formula calculation parameter.
    sigma          Float        Rainbow formula calculation parameter.
    d              Float        Rainbow formula calculation parameter.
    rho1           Float        Rainbow formula calculation parameter.
    rho2           Float        Rainbow formula calculation parameter.
----------------------------------------------------------------------------"""
class FRainbowParams(FEqBasket.BasketParams):
    def __init__(self, i):
        FEqBasket.BasketParams.__init__(self, i)
        if self.eur_ame: 
            print "\n## !! EXCEPTION !! ##"
            raise F_RAINBOW_EXCEPT, 'FEqRainbowMax/BOT/WOT only handles plain European options.'
        if self.digital: 
            print "\n## !! EXCEPTION !! ##"
            raise F_RAINBOW_EXCEPT, 'FEqRainbowMax/BOT/WOT does not handle digital options.'
        if not (i.und_instype == 'Combination' or i.und_instype == 'EquityIndex'):
            print "\n## !! EXCEPTION !! ##"
            raise F_RAINBOW_EXCEPT, 'Underlying instrument type is not an equity index instrument.'
        if self.dim != 2:  
            print "\n## !! EXCEPTION !! ##"
            raise F_RAINBOW_EXCEPT, NUMBEROFUND_EXCEPT
        if self.strike < 0.0:
            print "\n## !! EXCEPTION !! ##"
            raise F_RAINBOW_EXCEPT, 'The strike is negative.'
        
        und = ael.CombinationLink.select('owner_insaddr='+str(i.und_insaddr.insaddr))
        if self.texp == 0.0:
            self.Sw0 = und[0].weight*und[0].member_insaddr.used_price()
            self.Sw1 = und[1].weight*und[1].member_insaddr.used_price()
            self.fi = -1 + 2*(i.call_option == 1)    
        
        
        # Volatilities       
        self.vol = []
        check = 0
        self.vol_surfaces = []
        for j in range(2):
            # Find the right volatility surface
            vol_surf = und[j].member_insaddr.used_volatility(und[j].member_insaddr.curr)
            try:    
               self.vol_surfaces.append(vol_surf.vol_name)
            except: self.vol_surfaces = 'vol_name'
            self.vol.append(vol_surf.volatility(self.strike/self.weights[j], self.exp_day, self.valuation_date, self.put_call))
            if und[j].member_insaddr.insid != self.basket_stocks[j]: check = 1
            if self.vol[j] < 0.0:  
                print "\n## !! EXCEPTION !! ##"
                raise F_RAINBOW_EXCEPT, 'The volatility is negative.'
        if check: self.vol.reverse()
        
        # Correlations
        stocks = []
        for stock_link in und:
            stocks.append(stock_link.member_insaddr)
        self.rho = FEqBasketUtils.Corr(stocks, i)[0][1][0]
        if abs(self.rho) > 1:
            print "\n## !! EXCEPTION !! ##"
            raise F_RAINBOW_EXCEPT, "The correlation's absolute value is greater than one."
        
        self.rainbow_type = i.add_info("FRainbowType")
        if self.rainbow_type == "":
            print "\n## !! EXCEPTION !! ##"
            raise F_RAINBOW_EXCEPT, "No Rainbow type is chosen in the Additional Info field 'FRainbowType'."
    
    def pv(self):
        res = FEqRainbowUtils.get_rainbow_pv(self) * self.strike_theor_curr_fx 
        return res


"""----------------------------------------------------------------------------
FUNCTION        
   pv() 

DESCRIPTION
   Calculates the present value of a Rainbow option. 

ARGUMENTS
   i           Instrument      Best of two Option
   calc        Integer         0->No calculation 1->Perform calculation
   ref                         Optimisation parameter

RETURNS
  [res         Float           Value of instrument
   expday      Date            Maturity date
   curr        String          Currency in which it was valued
   fixed       String          Constant = 'Fixed']                                     
----------------------------------------------------------------------------"""
def pv(i, calc, ref):
    extra_days = 0
    if calc:
        try:
            rainbow_type = i.add_info("FRainbowType")
            if rainbow_type == "":
                print "\n## !! EXCEPTION !! ##"
                raise F_RAINBOW_EXCEPT, "No Rainbow type is chosen in the Additional Info field 'FRainbowType'."
            try:
                print_info = i.add_info("FPrintInfo")
            except: print_info = ""
            rp = FRainbowParams(i)
            if globals()['counter'] == 5: globals()['counter'] = 0
            if (LOG_PARAMETERS or print_info == "Yes") and globals()['counter'] == 0:
                if rp.texp > 0: print get_info(rp)
                else: print "\n## !! OPTION " + i.insid + " HAS EXPIRED !! ##"
            globals()['counter'] = globals()['counter'] + 1
            if i.exp_day < ael.date_valueday():  res = 0.0
            else: 
                res = rp.pv()
                extra_days = rp.extra_days
        except F_RAINBOW_EXCEPT, msg:
            print '\nModule: FEqRainbow'
            print 'Error : ', msg
            print 'Instr : ', i.insid
            res = 0.0
        except F_BASKET_EXCEPT, msg:
            print '\nModule:  FEqRainbow'
            print 'Error : ', msg
            print 'Instr : ', i.insid
            res = 0.0
    else: res = 0.0
    return [ [ res, i.exp_day.add_days(extra_days), i.curr, 'Fixed' ] ]


"""----------------------------------------------------------------------------
print_info() 
    The function returns a string with valuation parameters.
----------------------------------------------------------------------------"""
def get_info(RainbowParams):
    rp = RainbowParams
    s = ''
    s = s + "Instrument: \t" + rp.insid + "\t is using parameter(s): \n"  
    s = s + "\t\n"
    s = s + "Underlying:\t\t" + rp.underlying + "\n"
    s = s + "Rainbow type:\t\t" + rp.rainbow_type + "\n"
    s = s + "Used discount rate:\t%*.*f" % (6, 4, rp.rate*100) + "\n"
    s = s + "Mapped to Correlation:\t" + rp.corr_name + "\n"
    s = s + "Correlation value:\t" + str(rp.rho) + "\n"
    s = s + "\t\n"
    s = s + "---------------------------------\n"
    for i in range(rp.dim):
        s = s + "Rainbow member:\t\t" + str(rp.basket_stocks[i]) + "\n"
        s = s + "Member price:\t\t" + str(rp.price[i]) + "\n"
        s = s + "Member weight:\t\t" + str(rp.weights[i]) + "\n"
        s = s + "Volatility surface:\t" + str(rp.vol_surfaces[i]) + "\n" 
        s = s + "Used volatility:\t%*.*f" % (6, 4, rp.vol[i]*100)  + "\n"
        if rp.dividends[i] != []:
            s = s + "Underlying Dividends (in " + rp.currency + ") :\n"
            s = s + "\t\tEx Div Day \tRecord Day \tAmount \tTax Factor\n"
            for d in rp.div_entities[i]:
                s = s + "\t\t" + str(d.ex_div_day) + "\t" + str(d.day) + "\t" + str(d.dividend) + "\t" + str(d.tax_factor) + "\n"
        s = s + "---------------------------------\n"
    s = s + "\t\n"
    s = s + "Used valuation function: \tFEqRainbow.pv \n"
    s = s + "Mapped in context:\t\t" + rp.used_context + "\n"
    s = s + "\t\n" + "\t\n"
    return s    

        














