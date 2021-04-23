import ael

def CPI_Reset_Fixing(temp, cfwnbr, sday, eday, *rest):

    try:
    	sdate = ael.date_from_string(sday)
    except:
#       print '\n argument1 not in string format\n'
	sdate = sday
	

    try:
    	edate = ael.date_from_string(eday)
    except:
#       print '\n argument2 not in string format\n'=
	edate = eday
	
	
    #legs = ael.Trade[trd].insaddr.legs()
    #for l in legs:
    #cashfs = l.cash_flows()
    #    for c in cashfs:
    c = ael.CashFlow[cfwnbr]
    print('CF', c.cfwnbr)
    res = c.resets()
    for r in res:
        #print 'RES', r.resnbr, r.start_day, r.end_day, r.day
        r_clone = r.clone()
        r_clone.start_day = sdate
        r_clone.end_day = sdate
        r_clone.day = sdate
        #print 'RES_NEW', r_clone.resnbr, r_clone.start_day, r_clone.end_day, r_clone.day
        try:
            r_clone.commit()
            pass
        except:
            print('Error commiting reset for cashflow number ', c.cfwnbr)
                
                
    return 'Success'
    
    
#main
#print CPI_Reset_Fixing(1, 938729, '2007-05-01', '2007-07-10')
        
    
