# This is to capture the prices for all different equity instruments 
# Hardus Jacobs
 
import ael
def price_input(i,p,prt,date,*rest):
    cday = ael.date_from_string(date)    
    instrument =  ael.Instrument[i.insid]
    res = 'false'
    for pr in instrument.prices():
    	if pr.ptynbr:
            if pr.ptynbr.ptynbr == 10:
       	    	pi = pr.clone()
	    	pi.creat_time = cday.to_time()
    	    	#pr.insaddr = instrument
    	    	pi.day = cday
    	    	pi.settle = float(prt)
    	    	pi.curr = 2
    	    	result = pi.commit()
	    	res = 'true'
    if res == 'false':
        pi = ael.Price.new()
	pi.creat_time = cday.to_time()
    	pi.insaddr = instrument.insaddr
    	pi.day = cday
    	pi.settle = float(prt)
    	pi.curr = 2
	pi.ptynbr = 10
    	print(pi.pp())
    	result = pi.commit()    
    return 'Success'

    
