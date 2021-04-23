import ael


def copyMTM(temp, i, tdy, *rest):
    
    try:
    	sdate = ael.date_from_string(tdy)
    except:
#       	print '\n argument1 not in string format\n'
	sdate = tdy

    
    #ael.poll()
    #for i in ins:
    hp = 0
    spot = 0
    ins = ael.Instrument[i]
    hist = ins.historical_prices()
    current = ins.prices()
    for c in current:
        #print 'test1', c.pp()
        if c.ptynbr.ptynbr == 10:
            spot = c
    np = spot.clone()
    for h in hist:
        #print h.day, sdate
        if (h.day == sdate) and (h.ptynbr == ael.Party['internal']):
            hp = h
            #print 'test2', h.pp()
    if hp != 0:
        np.settle = hp.settle
        np.day = sdate
        np.ptynbr = 10
        np.curr = hp.curr
        #print 'test3', np.pp()
        np.commit()
        #ael.poll()
        #print '**************************************'
        #print '**************************************'
        print('**************************************')    
        print('******Copied the spot prices End *****')	
        print('**************************************')
        #print '**************************************'
        #print '**************************************'
        return 'Success'
    else:
        #print sdate.to_string()
        msg = 'No price commited for ' + i + ' for the ' + sdate.to_string()
        return msg

#print copyMTM(1, 'ZAR/BAW3_BASKET')
