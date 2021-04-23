#AS_InstrumentFix fixes a given instrument's quote type and all the prices
#of the associated trade prices

import ael, string


def Ins_Fix(temp, i, *rest):

    flag = 0

    trds = i.trades()
    for t in trds:
    	t_clone = t.clone()
	t_clone.price = t.price / 100
	print 'Trade ', t.trdnbr, ' price changed from ', t.price, ' to ', t_clone.price
    	t_clone.commit()
	ael.poll()		
		
    print
    	
    hp = i.historical_prices()
    for h in hp:
    	if h.curr == ael.Instrument['ZAR']:
#	    and h.day != '2004/11/05' and h.ptynbr.ptyid != 'internal':
	    price = ael.Price[h.prinbr]
		   
	    p_clone = price.clone()
	    p_clone.settle = p_clone.settle / 100
		    
	    try:
    	    	p_clone.commit()
		print 'Price ', h.prinbr, ' changed from ', price.settle, ' to ', p_clone.settle
	    except:
		flag = 1
		print 'Error committing instrument ', h.prinbr
	    ael.poll()


    if flag == 1:
    	return 'Failed'
    else:
    	return 'Success'
		
	
#main ael
i = ael.Instrument['ZAR/RUT']
#p = ael.Portfolio['SATRIX 40 CAPS OTC']
#Equity_OTC_AMPLATS
print 'Starting Instrument Price Fix...'
Ins_Fix('', i)    
print 'Finished Instrument Price Fix'
