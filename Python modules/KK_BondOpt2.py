import ael, time, math
from ael import *
from math import *





    


def Price(temp, i, *rest):

    und_frw_yield = i.used_und_frw_price()    
    vol = i.used_vol()/100.0
    today = date_today()
    expday = i.exp_day
    texp = today.years_between(expday, 'Act/365')
    if texp==0:
    	  texp = 0.000001  
       
    exp_offset = expday.add_banking_day(i.curr, i.pay_day_offset)
    today_offset = today.add_banking_day(i.und_insaddr.curr, i.und_insaddr.spot_banking_days_offset)

    und_dirty_frw_price = i.und_insaddr.dirty_from_yield(exp_offset, 'RSA', '', und_frw_yield)
    und_dirty_spot_price = i.und_insaddr.dirty_from_yield(today_offset, 'RSA', '', i.used_und_price())
    
    strike_dirty_price = i.und_insaddr.dirty_from_yield(exp_offset, 'RSA', '', i.strike_price)
    strike_dirty_spot_price = i.und_insaddr.dirty_from_yield(today_offset, 'RSA', '', i.strike_price)

    
    texp_carry = today_offset.years_between(exp_offset, 'Act/365')
    if texp_carry==0:
          texp_carry = 0.000001
	  
    used_rate = i.used_rate() * 0.01
    #print 'to,eo',today_offset,exp_offset
    rf = log(1+texp_carry*used_rate)/texp_carry

    carry_cost = rf * texp_carry / texp
         
			        
    und_dirty_price = und_dirty_frw_price * exp(- texp_carry * rf)
    
    #und_dirty_price = und_dirty_price + i.und_price_shift()
    
    
    test_exp = (und_dirty_price*exp(texp*carry_cost) - strike_dirty_price)*exp(-texp*rf)
    #print "test_exp",test_exp
    time = expday.years_between(exp_offset, 'Act/365')
    bs = ael.eq_option(und_dirty_price, texp, vol, rf, carry_cost, strike_dirty_price, i.call_option)*exp(-time*rf)
	
    return bs
#i = ael.Trade[1197386].insaddr
#print Theor(1, i)

def Price01(temp, trad, *rest):
    ii = ael.Trade[trad.trdnbr]
    i2 = ii.insaddr
    i3 = i2.und_insaddr
    pv0 = ii.present_value()
   # print i3.used_price()

    prc = i3.prices()
    for p in prc:
            pc = p.clone()
            pc.settle = p.settle + 0.01
            pc.last = p.last + 0.01
            pc.bid = p.bid + 0.01
            pc.ask = p.ask + 0.01
            pc.apply() 
   # print i3.used_price()
    pv1 = ii.present_value()
    
    pv01 = (pv1 - pv0)
    
    pc.revert_apply()
    pv2 = ii.present_value()
   # print pv01
   # print i3.used_price()
	
    return pv01

