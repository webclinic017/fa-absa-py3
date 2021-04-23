#AS_InstrumentFix fixes a given instrument's quote type and all the prices
#of the associated trade prices

import ael, string


def Ins_Fix(temp, trdnbr, *rest):
    
    flag = 0
#    i = ael.Instrument['ZAR/STK/STXI/APR05/P/808/OTC']

    t = ael.Trade[trdnbr]
    
    i = t.insaddr
    
    if i.exp_day < ael.date_today():
    	return 'Expired'
    
    #quote type
    i_clone = i.clone()
    if i.quote_type != 'Per 100 Units':
    	i_clone.quote_type = 'Per 100 Units'
	
    	try:
    	    i_clone.commit()
#	    print i_clone.insid, 'committed'
    	except:
    	    flag = 1
    	    print('Error committing instrument ', i.insid)
   	ael.poll()	
	    
	

    	hp = i.historical_prices()
	for h in hp:
	    if h.curr == ael.Instrument['ZAR']:
#		and h.day != '2004/11/05' and h.ptynbr.ptyid != 'internal':
	    	price = ael.Price[h.prinbr]
		   
		p_clone = price.clone()
		p_clone.settle = p_clone.settle * 100
		    
		try:
		    p_clone.commit()
#		    print 'Price ', h.prinbr, ' changed from ', price.settle, ' to ', p_clone.settle
		except:
		    flag = 1
		    print('Error committing instrument ', h.prinbr)
		ael.poll()


    if flag == 1:
    	return 'Failed'
    else:
    	return 'Success'
		
	
#main ael
#i = ael.Instrument['Equity_OTC_AMPLATS']
#p = ael.Portfolio['SATRIX 40 CAPS OTC']
#Equity_OTC_AMPLATS
#print 'Starting Instrument Price Fix...'
#Ins_Fix('', 174873)    
#print 'Finished Instrument Price Fix'
