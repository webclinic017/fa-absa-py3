
import ael
from ael import *
from math import *


def Theor(i, calc, date):

    und_frw_yield = i.used_und_frw_price()    
    vol = i.used_vol()/100.0
    today = date_today()
    expday = i.exp_day
    texp = today.years_between(expday, 'Act/365')
       
    exp_offset = expday.add_banking_day(i.curr, i.pay_day_offset)
    today_offset = today.add_banking_day(i.und_insaddr.curr, i.und_insaddr.spot_banking_days_offset)

    
    und_dirty_frw_price = i.und_insaddr.dirty_from_yield(exp_offset, 'RSA', '', und_frw_yield)
    und_dirty_spot_price = i.und_insaddr.dirty_from_yield(today_offset, 'RSA', '', i.used_und_price())
    
    strike_dirty_price = i.und_insaddr.dirty_from_yield(exp_offset, 'RSA', '', i.strike_price)
    strike_dirty_spot_price = i.und_insaddr.dirty_from_yield(today_offset, 'RSA', '', i.strike_price)

    
    texp_carry = today_offset.years_between(exp_offset, 'Act/365')
    
    used_rate = i.used_rate() * 0.01
    #print 'to,eo',today_offset,exp_offset
    rf = log(1+texp_carry*used_rate)/texp_carry

    carry_cost = rf * texp_carry / texp
         
    
			        
    und_dirty_price = und_dirty_frw_price * exp(- texp_carry * rf)
    
    #und_dirty_price = und_dirty_price + i.und_price_shift()

   
    if calc:
    	test_exp = (und_dirty_price*exp(texp*carry_cost) - strike_dirty_price)*exp(-texp*rf)
	#print "test_exp",test_exp
	time = expday.years_between(exp_offset, 'Act/365')
	bs = ael.eq_option(und_dirty_price, texp, vol, rf, carry_cost, strike_dirty_price, i.call_option)*exp(-time*rf)
	
	
	if i.call_option:

	    time = ael.date_today().years_between(exp_offset, 'Act/365')
    	    intrinsic = (und_dirty_frw_price - strike_dirty_price)/(time * used_rate + 1.0)
	else:

	    time = ael.date_today().years_between(exp_offset, 'Act/365')
   
    	    intrinsic = (strike_dirty_price - und_dirty_frw_price)/(time * used_rate + 1.0)

	amount = (max(intrinsic, bs))/100
				       
    #print "amount", amount

	
    else:
    	amount = 0.0
		
    return [ [ amount, exp_offset, i.curr, 'Fixed' ] ]
