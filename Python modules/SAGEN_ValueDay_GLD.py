import ael, time
trade = ael.TradeFilter['GLD_valuedate'].trades()
for t in trade:
    if (ael.date_from_time(t.time)) == (ael.date('2004-11-03')):
    	print t.trdnbr, ael.date_from_time(t.time), time.gmtime(t.time)[3]
	tc = t.clone()
	if time.gmtime(t.time)[3] > 10:
	    print 'plus 3'
	    tc.value_day = t.value_day.add_banking_day(ael.Instrument['ZAR'], 3)
	    tc.commit()
	elif time.gmtime(t.time)[3] < 10:
    	    print 'plus 2'		    
	    tc.value_day = t.value_day.add_banking_day(ael.Instrument['ZAR'], 2)
    	    tc.commit()
