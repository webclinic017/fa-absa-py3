""" SEQ_VERSION_NR = PRIME 2.8.1 """




"""-----------------------------------------------------------------------------
MODULE
    FEqRainbowUtils
        
    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    Computes the value of a European rainbow.     

-----------------------------------------------------------------------------"""
import math
import ael 
import FRainbowParams

F_RAINBOW_EXCEPT  = 'f_eq_rainbow_xcp'  
F_RAINBOW_WARNING = 'f_eq_rainbow_warning' 
F_BASKET_EXCEPT   = 'f_eq_basket_xcp'  

EXPIRES_TODAY_WARNING = 'The option expires today.'
EXPIRED_WARNING = 'The option has expired'
NUMBEROFUND_EXCEPT = 'There are more than or less than two assets in the combination instrument.'

RAINBOW_MAX = "Max of Two"
RAINBOW_MIN = "Min of Two"
RAINBOW_BOT = "Best of Two"
RAINBOW_WOT = "Worst of Two"

# INFINITY is considered to be 'infinity' in the sense that the normal distribution N(x)
# is approximately equal to 1 for all x greater than INFINITY.
INFINITY = 6.0
PI = 3.14159265358979

rainbow_type_dict = {RAINBOW_MAX:0,RAINBOW_MIN:1,RAINBOW_BOT:2,RAINBOW_WOT:3}

"""----------------------------------------------------------------------------
get_type_number() 
    The function returns the rainbow type number.
----------------------------------------------------------------------------"""
def get_type_number(rainbow_type, insid):
    if rainbow_type_dict.has_key(rainbow_type):
        return rainbow_type_dict[rainbow_type]
    else:
        print "\n## !! EXCEPTION !! ##"
        print '\nModule: FEqRainbowUtils'
        print 'Error : Unknown Rainbow type'
        print 'Instr : ', insid
        return 'Unknown Rainbow type'

"""----------------------------------------------------------------------------
get_price_vol_part()
    The function calculates the volatility part of the underlying assets, 
    i.e. the initial value of the underlying assets minus the discounted
    sum of all future dividends paid out prior expiration.
----------------------------------------------------------------------------"""    
def get_price_vol_part(dividends, price, texp, rate_stocks):        
    divsum = 0.0
    price_vol_part = []
    for j in range(len(price)): 
        for div in dividends[j]:
            if (div[1] <= texp) and (div[1] >= 0): 
                divsum = divsum + div[0]*math.exp(-rate_stocks[j]*div[1])
        price_vol_part.append(price[j]-divsum)
        if ( price_vol_part[j] < 0.0 ):
            if (price[j] < 0.0):
                print "\n## !! EXCEPTION !! ##"
                raise F_BASKET_EXCEPT, 'The initial asset price(s) are less than or equal to zero.'
            else:
                print "\n## !! EXCEPTION !! ##"
                raise F_BASKET_EXCEPT, "The sum of the discounted dividends' amount is greater than the initial asset price."
        divsum = 0.0
    return price_vol_part

    
"""----------------------------------------------------------------------------
call_on_the_max() 
    The function returns the value for a call max of two rainbow option.
----------------------------------------------------------------------------"""
def call_on_the_max(price_vol_part, carry_cost, rate, texp, y1, y2, d, sigma, strike, vol, rho, rho1, rho2):
    res = price_vol_part[0] * math.exp((carry_cost[0] - rate) * texp) * bivar_normal_dist(y1, d, rho1) + \
          price_vol_part[1] * math.exp((carry_cost[1] - rate) * texp) * bivar_normal_dist(y2, -d + \
          sigma*math.sqrt(texp), rho2) - \
          strike * math.exp(-rate * texp) * (1 - bivar_normal_dist(-y1 + vol[0] * \
          math.sqrt(texp), -y2 + vol[1]*math.sqrt(texp), rho))
    return res

"""----------------------------------------------------------------------------
put_on_the_max() 
    The function returns the value for a put max of two rainbow option.
----------------------------------------------------------------------------"""
def put_on_the_max(price_vol_part, carry_cost, rate, texp, y1, y2, d, sigma, strike, vol, rho, rho1, rho2):
    call_K0 = price_vol_part[1]*math.exp((carry_cost[1] - rate)*texp)* \
              ael.normal_dist(-d + sigma*math.sqrt(texp)) + \
              price_vol_part[0]*math.exp((carry_cost[0] - rate)*texp)*ael.normal_dist(d)
    call_K = call_on_the_max(price_vol_part, carry_cost, rate, texp, y1, y2, d, sigma, strike, vol, rho, rho1, rho2)
    res = strike*math.exp(-rate*texp) - call_K0 + call_K 
    return res

"""----------------------------------------------------------------------------
best_of_two_or_cash() 
    The function returns the value for a best of two or cash rainbow option.
----------------------------------------------------------------------------"""
def best_of_two_or_cash(price_vol_part, carry_cost, rate, texp, y1, y2, d, sigma, strike, vol, rho, rho1, rho2):
    res = strike*math.exp(-rate*texp) + \
    call_on_the_max(price_vol_part, carry_cost, rate, texp, y1, y2, d, sigma, strike, vol, rho, rho1, rho2)
    return res

"""----------------------------------------------------------------------------
best_of_two_or_cash() 
    The function returns the value for a best of two or cash rainbow option.
----------------------------------------------------------------------------"""
def call_on_the_min(price_vol_part, carry_cost, rate, texp, y1, y2, d, sigma, strike, vol, rho, rho1, rho2):
    res = price_vol_part[0]*math.exp((carry_cost[0] - rate)*texp)* \
          bivar_normal_dist(y1, -d, -rho1) + \
          price_vol_part[1]*math.exp((carry_cost[1] - rate)* \
          texp)*bivar_normal_dist(y2, d - sigma*math.sqrt(texp), -rho2) - \
          strike*math.exp(-rate*texp)*bivar_normal_dist(y1 - \
          vol[0]*math.sqrt(texp), y2 - vol[1]*math.sqrt(texp), rho) 
    return res

"""----------------------------------------------------------------------------
put_on_the_min() 
    The function returns the value for a put min of two assets rainbow option.
----------------------------------------------------------------------------"""
def put_on_the_min(price_vol_part, carry_cost, rate, texp, y1, y2, d, sigma, strike, vol, rho, rho1, rho2):
    call_K0 = price_vol_part[0]*math.exp((carry_cost[0] - rate)*texp)* \
              ael.normal_dist(-d) + price_vol_part[1]*math.exp((carry_cost[1] - \
              rate)*texp)*ael.normal_dist(d - sigma*math.sqrt(texp))
    call_K = call_on_the_min(price_vol_part, carry_cost, rate, texp, y1, y2, d, sigma, strike, vol, rho, rho1, rho2)
    res = strike*math.exp(-rate*texp) - call_K0 + call_K 
    return res
    
"""----------------------------------------------------------------------------
worst_of_two_or_cash() 
    The function returns the value for a worst of two or cash rainbow option.
----------------------------------------------------------------------------"""
def worst_of_two_or_cash(price_vol_part, carry_cost, rate, texp, y1, y2, d, sigma, strike, vol, rho, rho1, rho2):
    res = strike*math.exp(-rate*texp) - \
    put_on_the_min(price_vol_part, carry_cost, rate, texp, y1, y2, d, sigma, strike, vol, rho, rho1, rho2)
    return res
    
"""----------------------------------------------------------------------------
rainbow_val_params() 
    The following parameters are needed in the 'Rainbow formulas', see p 56-58 
    in 'The complete guide to option pricing formulas' by Espen Gaarder Haug 
    for further details.
----------------------------------------------------------------------------"""
def rainbow_val_params(price_vol_part, strike, vol, carry_cost, texp, rho):
    # Taking care of the special cases:
    if strike == 0.0 or vol[0] == 0.0 or vol[1] == 0.0:
        if strike == 0.0:
            y1 = INFINITY; y2 = INFINITY
        elif (vol[0] == 0.0 and vol[1] == 0.0):
            y1 = sign(math.log(price_vol_part[0]/strike) + carry_cost[0]*texp)*INFINITY
            y2 = sign(math.log(price_vol_part[1]/strike) + carry_cost[1]*texp)*INFINITY
        elif vol[0] == 0.0:
            y1 = sign(math.log(price_vol_part[0]/strike) + carry_cost[0]*texp)*INFINITY
            y2 = (math.log(price_vol_part[1]/strike) + (carry_cost[1] + 0.5*vol[1]**2)*texp)/ \
                 (vol[1]*math.sqrt(texp))
        else:
            y1 = (math.log(price_vol_part[0]/strike) + (carry_cost[0] + 0.5*vol[0]**2)*texp)/ \
                 (vol[0]*math.sqrt(texp))
            y2 = sign(math.log(price_vol_part[1]/strike) + carry_cost[1]*texp)*INFINITY
    else:
        y1 = (math.log(price_vol_part[0]/strike) + (carry_cost[0] + 0.5*vol[0]**2)*texp)/ \
             (vol[0]*math.sqrt(texp))
        y2 = (math.log(price_vol_part[1]/strike) + (carry_cost[1] + 0.5*vol[1]**2)*texp)/ \
             (vol[1]*math.sqrt(texp))

    sigma = math.sqrt(vol[0]**2 + vol[1]**2 - 2*rho*vol[0]*vol[1]) 

    # The assets are not completly correlated.
    if sigma > 0:
        try:
            d = (math.log(price_vol_part[0]/price_vol_part[1]) + (carry_cost[0] - \
            carry_cost[1] + 0.5*sigma**2)*texp)/ (sigma*math.sqrt(texp))
        except ZeroDivisionError:
            ##### CHECK WHAT TO DO: pass?
            d = 0
        rho1 = (vol[0] - rho*vol[1])/sigma
        rho2 = (vol[1] - rho*vol[0])/sigma                                                                                          

    else:
        if price_vol_part[0] == price_vol_part[1]: d = INFINITY
        else:    
            d = INFINITY*sign(math.log(price_vol_part[0]/price_vol_part[1]))  
        rho1 = 0.0; rho2 = 0.0
    return [y1, y2, d, sigma, rho1, rho2]

"""----------------------------------------------------------------------------
sign() 
    The function returns the sign of a number.
----------------------------------------------------------------------------"""
def sign(a):
    if a < 0.0: return -1.0
    return 1.0

"""----------------------------------------------------------------------------
bivar_hlp1() 
    A help function to the bivariate normal distribution, see below.
----------------------------------------------------------------------------"""
def bivar_hlp1(x, y, aprime, bprime, rho):
    p = aprime * (2*x - aprime) + bprime * (2*y - bprime) + 2*rho * (x - aprime)*(y - bprime)
    return math.exp(p)
    
"""----------------------------------------------------------------------------
bivar_hlp2() 
    A help function to the bivariate normal distribution, see below.
----------------------------------------------------------------------------"""
def bivar_hlp2(a, b, rho):
    A = [0.24840615, 0.39233107, 0.21141819, 0.033246660, 0.00082485334]
    B = [0.10024215, 0.48281397, 1.0609498, 1.7797294, 2.6697604 ]

    if rho <= -1.0: return 0.0

    rhotilde = math.sqrt(1 - rho*rho)
    c = 1/math.sqrt(2)
    aprime = a*c/rhotilde
    bprime = b*c/rhotilde

    p=0
    for i in range(len(A)):
        for j in range(len(A)):
            p = p + A[i]*A[j]*bivar_hlp1(B[i], B[j], aprime, bprime, rho)
    p = p*rhotilde/PI
    return p
    
"""----------------------------------------------------------------------------
bivar_normal_dist() 
    The function computes the bivariate normal distribution. The approximation 
    produces values of the mentioned distribution within sex decimal places 
    accuracy, see 'The complete guide to option pricing formulas' by Espen Gaarder 
    Haug for further details.
----------------------------------------------------------------------------"""
def bivar_normal_dist(a, b, rho):
    if a <= 0.0 and  b <= 0.0 and rho <= 0.0:
        return bivar_hlp2(a, b, rho)

    elif a <= 0.0 and b >= 0.0 and rho >= 0.0:
        return ael.normal_dist(a) - bivar_hlp2(a, -b, -rho)

    elif a >= 0.0 and b <= 0.0 and rho >= 0.0:
        return ael.normal_dist(b) - bivar_hlp2(-a, b, -rho)

    elif a >= 0.0 and b >= 0.0 and rho <= 0.0:
        return ael.normal_dist(a) + ael.normal_dist(b) - 1 + bivar_hlp2(-a, -b, rho)

    else:
        if a == b:
            rho1 = -sign(a)*math.sqrt((1-rho)/2)
            rho2 = rho1
        else:
            c = 1/math.sqrt(a*a - 2*rho*a*b + b*b)
            rho1 = (rho*a - b)*sign(a)*c
            rho2 = (rho*b - a)*sign(b)*c
        delta = (1 - sign(a)*sign(b))/4
        p = bivar_normal_dist(a, 0.0, rho1) + bivar_normal_dist(b, 0.0, rho2) - delta
        return p
        
"""----------------------------------------------------------------------------
pv() 
    The function returns the value for a rainbow option.
----------------------------------------------------------------------------"""
def get_rainbow_pv(rp):    
    try:
        if rp.texp == 0.0:
            raise F_RAINBOW_WARNING, EXPIRES_TODAY_WARNING   
        if rp.texp < 0.0:
            raise F_RAINBOW_WARNING, EXPIRED_WARNING

        rp.price_vol_part = get_price_vol_part(rp.dividends, rp.price, rp.texp, rp.rate_stocks)
        rp.price_vol_part[0] = rp.weights[0]*rp.price_vol_part[0]
        rp.price_vol_part[1] = rp.weights[1]*rp.price_vol_part[1]
        [y1, y2, d, sigma, rho1, rho2] = rainbow_val_params(rp.price_vol_part, rp.strike,\
                                        rp.vol, rp.carry_cost, rp.texp, rp.rho)

        if rp.rainbow_type == RAINBOW_MAX:
            if rp.put_call:
                # The option is a call
                res = call_on_the_max(rp.price_vol_part, rp.carry_cost, rp.rate, rp.texp,\
                y1, y2, d, sigma, rp.strike, rp.vol, rp.rho, rho1, rho2)   
            else:
                res = put_on_the_max(rp.price_vol_part, rp.carry_cost, rp.rate, rp.texp,\
                y1, y2, d, sigma, rp.strike, rp.vol, rp.rho, rho1, rho2)
        
        elif rp.rainbow_type == RAINBOW_MIN:
            if rp.put_call:
                # The option is a call
                res = call_on_the_min(rp.price_vol_part, rp.carry_cost, rp.rate, rp.texp,\
                y1, y2, d, sigma, rp.strike, rp.vol, rp.rho, rho1, rho2)      
            else:
                # The option is a put
                res = put_on_the_min(rp.price_vol_part, rp.carry_cost, rp.rate, rp.texp,\
                y1, y2, d, sigma, rp.strike, rp.vol, rp.rho, rho1, rho2)
        
        elif rp.rainbow_type == RAINBOW_BOT:
            res = best_of_two_or_cash(rp.price_vol_part, rp.carry_cost, rp.rate, rp.texp,\
            y1, y2, d, sigma, rp.strike, rp.vol, rp.rho, rho1, rho2)   
        elif rp.rainbow_type == RAINBOW_WOT:
            res = worst_of_two_or_cash(rp.price_vol_part, rp.carry_cost, rp.rate, rp.texp,\
            y1, y2, d, sigma, rp.strike, rp.vol, rp.rho, rho1, rho2)    
        
        else: 
            print "\n## !! EXCEPTION !! ##"
            raise F_RAINBOW_EXCEPT, 'Unknown rainbow type.'
        return res * rp.df

    # Handling warnings
    except F_RAINBOW_WARNING, msg:
        if msg == EXPIRES_TODAY_WARNING:
            if rp.rainbow_type == RAINBOW_MAX:
                res = max(rp.fi*(max(rp.Sw0, rp.Sw1) - rp.strike), 0)
            elif rp.rainbow_type == RAINBOW_MIN:
                res = max(rp.fi*(min(rp.Sw0, rp.Sw1) - rp.strike), 0)
            elif rp.rainbow_type == RAINBOW_BOT:
                res = rp.df*max(max(rp.Sw0, rp.Sw1), rp.strike)
            elif rp.rainbow_type == RAINBOW_WOT:
                res = min(min(rp.Sw0, rp.Sw1), rp.strike)
            else: raise F_RAINBOW_EXCEPT, 'Unknown rainbow type.'
            return res
        elif msg == EXPIRED_WARNING:
            return 0.0
        else:
            print '\nModule: FEqRainbowUtils'
            print 'Error : ', msg
            print 'Instr : ', rp.insid
            return 0.0

        



        
            
   
        
    
































































