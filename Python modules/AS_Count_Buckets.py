import ael


def CountTrades(temp, acq, status, flag, *rest):
    
    trades = ael.Trade.select('acquirer_ptynbr = %d' % acq)
    inslist = ['Stock', 'Future/Forward', 'Warrant', 'EquityIndex', 'Repo/Reverse', 'BuySellback', 'PriceIndex', 'IndexLinkedBond']
    tdy = ael.date_today()
    buck1 = 0
    buck2 = 0
    buck3 = 0
    buck4 = 0
    buck5 = 0	    
    buck6 = 0
    list1 = []
    
#    print d1.days_between(tdy, 'Act/365')
    
    for t in trades:
    	tdate = ael.date_from_time(t.time)
    	i = ael.Instrument[t.insaddr.insaddr]
	if (i.exp_day > tdy):
    	    if tdate > ael.date_from_string('2004-04-01'):
	    	if status == 'BO-BO Confirmed': 
	    	    if t.status == 'BO Confirmed' and i.instype in inslist:
		    	list1.append([t.trdnbr, tdate])
		    elif t.your_ref != '':
		    	list1.append([t.trdnbr, tdate])
		    elif t.status == 'BO-BO Confirmed':
		    	list1.append([t.trdnbr, tdate])
		elif status == 'BO Confirmed':
		    if (i.instype not in inslist) and t.your_ref == '':
		    	list1.append([t.trdnbr, tdate])    
    	    	elif t.status == status and t.status != 'BO-BO Confirmed' and t.status != 'BO Confirmed':
    	    	    list1.append([t.trdnbr, tdate])
	    
	    
    for l in list1:
    	diff = l[1].days_between(tdy, 'Act/365')
	
	if diff <= 2:
	    buck1 = buck1 + 1
	elif (diff >= 3 and diff <= 5):
	    buck2 = buck2 + 1
	elif (diff >= 6 and diff <= 10):
	    buck3 = buck3 + 1
	elif (diff >= 11 and diff <= 30):
	    buck4 = buck4 + 1
	elif (diff > 30):
	    buck5 = buck5 + 1
	else:
	    buck6 = buck6 + 1
	    

#    print buck1, buck2, buck3, buck4, buck5, buck6
  
    
    if flag == 1:
    	return buck1

    elif flag == 2:
    	return buck2
	
    elif flag == 3:
    	return buck3
	
    elif flag == 4:
    	return buck4
	
    elif flag == 5:
    	return buck5	
    

	
	
#main
#acq = ael.Party['Non Linear Deriv']
#CountTrades('', acq.ptynbr, 'FO Confirmed', 1)
