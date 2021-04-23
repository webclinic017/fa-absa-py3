
import ael		
from ael import *				
from math import *
		
def rndppt(temp, ins, *rest):
	
    today = ael.date_today()
     			
    if (ins.instype == 'Bond'):
        i = ins
    
    elif (ins.und_instype == 'Bond'):
        i = ins.und_insaddr
    
    today_offset = today.add_banking_day(i.curr, i.spot_banking_days_offset)
    
    dirty_price = i.dirty_from_yield(today_offset, 'RSA', '', i.used_price())
    #print '\ndirty_price',dirty_price
    dirty_price_bpshift = i.dirty_from_yield(today_offset, 'RSA', '', (i.used_price()+0.01))
    #print '\ndirty_price_bpshift',dirty_price_bpshift
    rndppt=((dirty_price_bpshift - dirty_price) * (- 10000))
    #print '\nrndppt',rndppt   
     
    return rndppt
