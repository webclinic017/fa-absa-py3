""" SEQ_VERSION_NR = 2.3.1 """


"""-----------------------------------------------------------------------------
MODULE
    FRainbowParams - Parameters for Basket options
        
    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    Extracts and computes parameters for an instrument of rainbow
    type, that is, Call (or Put) on the minimum (or maximum)
    of two assets, minimum (or maximum) for two assets or cash 
    and Basket options. It also contains some functions that are shared
    by all rainbow valuation functions.
       
EXTERNAL DEPENDENCIES
    FEqRainbowBOT.py
    FEqRainbowWOT.py
    FEqRainbowMax.py
    FEqRainbowMin.py
    
-----------------------------------------------------------------------------"""
import ael 
import math
import sys
import FBasketParams

F_RAINBOW_EXCEPT  = 'f_eq_rainbow_xcp'  
F_RAINBOW_WARNING = 'f_eq_rainbow_warning'  

DIV_EXCEPTION = "the sum of the discounted dividends' amount are greater than the initial asset price."
UND_EXCEPTION = 'the initial asset price(s) are less than or equal to zero.'
NUMBEROFUND_EXCEPT = 'there are more than or less than two assets in the combination instrument.'
#This exception is used by all two coulour rainbow options


# INFINITY is considered to be 'infinity' in the sense that the normal distribution N(x)
# is approximately equal to 1 for all x greater than INFINITY.
INFINITY = 6.0
PI = 3.14159265358979

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
class FRainbowParams(FBasketParams.BasketParams):
    def __init__(self, i):
        FBasketParams.BasketParams.__init__(self, i)
        if self.eur_ame: 
            raise F_RAINBOW_EXCEPT, 'FEqRainbowMax/BOT/WOT only handles plain European options.'
        if self.digital: 
            raise F_RAINBOW_EXCEPT, 'FEqRainbowMax/BOT/WOT does not handle digital options.'
        if not (i.und_instype == 'Combination' or i.und_instype == 'EquityIndex'):
            raise F_RAINBOW_EXCEPT, 'underlying instrument type is not a combination instrument.'
        if self.dim != 2:  
            raise F_RAINBOW_EXCEPT, NUMBEROFUND_EXCEPT
        if self.strike < 0.0:
            raise F_RAINBOW_EXCEPT, 'The strike is negative.'
        
        if self.texp == 0.0:
            und = ael.CombinationLink.select('owner_insaddr='+str(i.und_insaddr.insaddr))
            self.Sw0 = und[0].weight*und[0].member_insaddr.used_price()
            self.Sw1 = und[1].weight*und[1].member_insaddr.used_price()
            self.fi = -1 + 2*(i.call_option == 1)    
                   
        # Volatilities       
        self.vol = []
        check = 0
        und = ael.CombinationLink.select('owner_insaddr='+str(i.und_insaddr.insaddr))
        for j in range(2):
            # Find the right volatility surface
            vol_surf = und[j].member_insaddr.used_volatility(und[j].member_insaddr.curr)
            self.vol.append(vol_surf.volatility(self.strike/self.weights[j], self.exp_day))
            if und[j].member_insaddr.insid != self.basket_stocks[j]:
                check = 1
            if self.vol[j] < 0.0:  
                raise F_RAINBOW_EXCEPT, 'The volatility is negative.'
        if check: 
            self.vol.reverse()
        # Correlations
        if sys.version[0] == '1':
            CORR = ael.Covariance[option.used_context_parameter('Correlation')]
            self.rho = CORR.corr_get_correlation(und[0].member_insaddr, und[1].member_insaddr, self.exp_day) 
        else: 
            CORR = ael.CorrelationMatrix[i.used_context_parameter('Correlation Matrix')]
            self.rho = CORR.used_correlation(und[0].member_insaddr, und[1].member_insaddr) 
        if abs(self.rho) > 1:
            raise F_RAINBOW_EXCEPT, "The correlation's absolute value is greater than one."
    
    def rainbow_val_params(self, price_vol_part):
        # The following parameters are needed in the 'Rainbow formulas', see p 56-58 
        # in 'The complete guide to option pricing formulas' by Espen Gaarder Haug 
        # for further details.
        
        # Taking care of the specialcases:
        if (self.strike == 0.0) or (self.vol[0] == 0.0) or (self.vol[1] == 0.0):
            if self.strike == 0.0:
                self.y1 = INFINITY
                self.y2 = INFINITY
            elif (self.vol[0] == 0.0 and self.vol[1] == 0.0):
                self.y1 = self.sign(math.log(self.price_vol_part[0]/self.strike) + \
                          self.carry_cost[0]*self.texp)*INFINITY
                self.y2 = self.sign(math.log(self.price_vol_part[1]/self.strike) + \
                          self.carry_cost[1]*self.texp)*INFINITY
            elif self.vol[0] == 0.0:
                self.y1 = self.sign(math.log(self.price_vol_part[0]/self.strike) + \
                          self.carry_cost[0]*self.texp)*INFINITY
                self.y2 = (math.log(self.price_vol_part[1]/self.strike) + \
                          (self.carry_cost[1] + 0.5*self.vol[1]**2)*self.texp)/ \
                          (self.vol[1]*math.sqrt(self.texp))
            else:
                self.y1 = (math.log(self.price_vol_part[0]/self.strike) + \
                          (self.carry_cost[0] + 0.5*self.vol[0]**2)*self.texp)/ \
                          (self.vol[0]*math.sqrt(self.texp))
                self.y2 = self.sign(math.log(self.price_vol_part[1]/self.strike) + \
                          self.carry_cost[1]*self.texp)*INFINITY
        else:
            self.y1 = (math.log(self.price_vol_part[0]/self.strike) + \
                      (self.carry_cost[0] + 0.5*self.vol[0]**2)*self.texp)/ \
                      (self.vol[0]*math.sqrt(self.texp))
            self.y2 = (math.log(self.price_vol_part[1]/self.strike) + \
                      (self.carry_cost[1] + 0.5*self.vol[1]**2)*self.texp)/ \
                      (self.vol[1]*math.sqrt(self.texp))

        self.sigma = math.sqrt(self.vol[0]**2 + self.vol[1]**2 - 2*self.rho*self.vol[0]*self.vol[1]) 

        # The assets are not completly correlated.
        if self.sigma > 0:
            try:
                self.d = (math.log(price_vol_part[0]/price_vol_part[1]) + \
                    (self.carry_cost[0] - self.carry_cost[1] + 0.5*self.sigma**2)*self.texp)/ \
                    (self.sigma*math.sqrt(self.texp))
            except ZeroDivisionError:
                pass
            self.rho1 = (self.vol[0] - self.rho*self.vol[1])/self.sigma
            self.rho2 = (self.vol[1] - self.rho*self.vol[0])/self.sigma                                                                                          

        else:
            if (price_vol_part[0] == price_vol_part[1]):
                self.d = INFINITY
            else:    
                self.d = INFINITY*self.sign(math.log(price_vol_part[0]/price_vol_part[1]))  
            self.rho1 = 0.0
            self.rho2 = 0.0
        
        
    # 'sign', method returning the sign of a number.
    def sign(self, a):
        if a < 0.0: return -1.0
        return 1.0

    # 'bivar_hlp1', a helpmethod to the bivariate normal distribution, see below.
    def bivar_hlp1(self, x, y, aprime, bprime, rho):
        p = aprime*(2*x - aprime) + bprime*(2*y - bprime) + 2*rho*(x - aprime)*(y - bprime)
        return math.exp(p)

    #'bivar_hlp2', a helpmethod to the bivariate normal distribution, see below.
    def bivar_hlp2(self, a, b, rho):
        A=[0.24840615, 0.39233107, 0.21141819, 0.033246660, 0.00082485334]
        B=[0.10024215, 0.48281397, 1.0609498, 1.7797294, 2.6697604 ]

        if rho <= -1.0:
            return 0.0

        rhotilde = math.sqrt(1 - rho*rho)
        c = 1/math.sqrt(2)
        aprime = a*c/rhotilde
        bprime = b*c/rhotilde

        p=0
        for i in range(len(A)):
            for j in range(len(A)):
                p = p + A[i]*A[j]*self.bivar_hlp1(B[i], B[j], aprime, bprime, rho)
        p = p*rhotilde/PI
        return p    

    # 'bivar_normal_dist' computes the bivariate normal distribution. The approximation produces
    # values of the mentioned distribution within sex decimal places accuracy, see 'The complete
    # guide to option pricing formulas' by Espen Gaarder Haug for further details.
    def bivar_normal_dist(self, a, b, rho):
        if (a <= 0.0 and  b <= 0.0 and rho <= 0.0):
            return self.bivar_hlp2(a, b, rho)

        elif (a <= 0.0 and b >= 0.0 and rho >= 0.0):
            return ael.normal_dist(a) - self.bivar_hlp2(a, -b, -rho)

        elif (a >= 0.0 and b <= 0.0 and rho >= 0.0):
            return ael.normal_dist(b) - self.bivar_hlp2(-a, b, -rho)

        elif (a >= 0.0 and b >= 0.0 and rho <= 0.0):
            return ael.normal_dist(a) + ael.normal_dist(b) - 1 + self.bivar_hlp2(-a, -b, rho)

        else:
            c = 1/math.sqrt(a*a - 2*rho*a*b + b*b)
            rho1 = (rho*a - b)*self.sign(a)*c
            rho2 = (rho*b - a)*self.sign(b)*c
            delta = (1 - self.sign(a)*self.sign(b))/4
            p = self.bivar_normal_dist(a, 0.0, rho1) + self.bivar_normal_dist(b, 0.0, rho2) - delta
            return p

       

        














