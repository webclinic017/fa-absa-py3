
import ael
from ael import *
from math import *



def Theor(temp, i, *rest):

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

    rf = log(1+texp_carry*used_rate)/texp_carry

    carry_cost = rf * texp_carry / texp
			        
    und_dirty_price = und_dirty_frw_price * exp(- texp_carry * rf)
    
    d1 = (log(und_dirty_price/strike_dirty_price) + texp * (carry_cost + 0.5 * pow(vol, 2))) / (vol*sqrt(texp))
   	
    Der_Nd1 = exp(-pow(d1, 2)/2) / sqrt(2*pi)
	
    gamma = (Der_Nd1 * exp(-carry_cost * texp)) / (und_dirty_price * vol * sqrt(texp)) / 100

    return gamma	

#main
#i = ael.Instrument['ZAR/C/BD/060803/7.50/R157']
#print Theor(1, i, 1)
#print

