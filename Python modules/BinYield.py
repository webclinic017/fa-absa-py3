import math
import ael
from BondOptParams import *

global OldP
global OldPv, OldDelta, OldGamma
global first_time
global EPS

EPS = 0.003

first_time = 1

#   Converts bond yields into a clean price.
#   The date is found from valday plus t plus settlement days
#   The clean price is discounted over the settlement period.

def y2p(i, y, t, r, valday):
    days = t * 365 + 0.5
    expday = valday 
    expday = expday.add_days(days) 
    expday_offset = expday.add_banking_day(i.curr, i.pay_day_offset)
    price = i.und_insaddr.clean_from_yield(expday_offset,'','',y)
    price = price * math.exp(-r * expday.years_between(expday_offset, 'Act/365'))
    return price

    
def similar_parameters(P, OldP):
    if P.vol == OldP.vol and P.t == OldP.t and P.strike == OldP.strike and P.american == OldP.american and P.call == OldP.call and math.fabs(P.spot_price - OldP.spot_price) < EPS:
#   Some more criterias should be added    
    	return 1
    else:
    	return 0
    
    
#   Yield Binominal tree pricing for bond options 

def binominal_yield(ins, steps):
    # Contract parameters
    valday = ael.date_today()
    t = valday.years_between(ins.exp_day,'Act/365')
    if ins.exercise_type == 'American':
    	american = 1
    else:
    	american = 0
    call = ins.call_option
    strike = ins.strike_price
    valday_offset = valday.add_banking_day(ins.curr, ins.pay_day_offset)
    expday_offset = ins.exp_day.add_banking_day(ins.curr, ins.pay_day_offset)

    # Valuation parameters 
    spot_yield = ins.used_und_price()    
    frw_yield = ins.used_und_frw_price()
    spot_price = ins.und_insaddr.clean_from_yield(valday_offset,'RSA','',spot_yield)
    frw_price = ins.und_insaddr.clean_from_yield(expday_offset,'RSA','',frw_yield)

    vol = ins.used_vol()/100
    cc = math.log(frw_price/spot_price) / t    
    yc = ins.used_yield_curve(ins.curr) 
    r = yc.yc_rate(valday,ins.exp_day,'Continuous','Act/365','Spot Rate')
    ycc = math.log(frw_yield / spot_yield) / t


    # Binominal Pricing, 
    # move back in time two steps, to handle greeks
    dt = t/(steps-2)
    df = math.exp(-r*dt)
    u = math.exp(math.sqrt(dt)*vol)
    u2 = u*u

    z = list(range(steps+1))
    und_price = list(range(steps+1))
    z[0] = spot_yield*math.exp(ycc*t)*math.pow(u,-steps)
    for j in range(steps):
        z[j+1] = u2*z[j]

    x = y2p(ins, strike, t, r, valday)
    for j in range(steps+1):
	und_price[j] = y2p(ins, z[j], t, r, valday) 
        if call:
	    if und_price[j] - x > 0.0:
    	    	z[j] = und_price[j] - x
	    else:
	    	z[j] = 0.0
        else:
	    if x - und_price[j] > 0.0:
            	z[j] = x - und_price[j]
	    else:
	    	z[j] = 0.0


    for i in range(steps):
    	t = t - dt
	zj = spot_yield * math.exp(ycc*t) * math.pow(u,-steps+i+1)
        for j in range (steps-i):
	    und_price0 = y2p(ins, zj, t, r, valday) 
	    if und_price[j] - und_price[j+1] > 0:
                p = (und_price0*math.exp(cc*dt) - und_price[j+1])/(und_price[j] - und_price[j+1])
    	    else:
	    	p = 0.5	
	    q = 1 - p
            z[j] = df*(p*z[j]+q*z[j+1])
	    und_price[j] = und_price0
            if american:
    		x = y2p(ins, strike, t, r, valday)
	    	if call:
	    	    if und_price[j] - x > z[j]:
	    	    	z[j] = und_price[j] - x
            	else:
	    	    if x - und_price[j] > z[j]:
            	    	z[j] = x - und_price[j]
	    if i == (steps - 3):
	    	if j == 0:
		    z0 = z[j]
		    p0 = und_price[j]
	    	if j == 1:
	    	    z1 = z[j]
		    p1 = und_price[j]
		if j == 2:
		    z2 = z[j]
		    p2 = und_price[j]
		
		
	    zj = u2 * zj

    pv = z1 / 100
    alfa = (z1 - z0) / (p1 - p0)
    beta = ((z2 - z1)/(p2 - p1) - (z1 - z0)/(p1 - p0))/(p2 - p0)
    delta = (alfa + beta * (p1 - p0)) 
    gamma = 2 * beta 
    return [pv, delta, gamma]
     

def Theor(i,calc,date):
    global first_time
    global OldP
    global OldPv, OldDelta, OldGamma
    steps = 36
    if calc:
    	P = BondOptParams(i)
	if first_time == 0 and similar_parameters(P, OldP):
	    dp = (P.spot_price - OldP.spot_price)/100
	    print "Estimation"
	    res = OldPv + OldDelta * dp + OldGamma * dp * dp * 0.5
	else:
	    print "Revaluation"
	    [OldPv, OldDelta, OldGamma]  = binominal_yield(i, steps)
	    OldP = P
	    res = OldPv
	    first_time = 0
	    
	    
    else:
    	res = 0
	
    return [ [ res, i.exp_day, i.curr, 'Fixed' ] ]
  
   
    
    
#   Test Code

#i = ael.Instrument['HN2']
#P = BondOptParams(i)
#steps = 36
#[pv , delta, gamma] = binominal_yield(i, steps)#

#print pv, delta, gamma

