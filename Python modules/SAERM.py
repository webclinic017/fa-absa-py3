import ael
def GetLastTrdDate(p,id,acq,*rest):
    port = ael.Portfolio[id]
    trds = port.trades()
    list = []
    #print id,acq,trds
    for t in trds:
    	if t.acquirer_ptynbr:
	    if t.acquirer_ptynbr.ptyid == acq:
	    	ins = t.insaddr
	    	if (ins.exp_day >= ael.date_today()) or (ins.exp_day == None):
		    #(ins.exp_day == '0000-01-01')
		    #print t.trdnbr, '***', ael.date_from_time(t.time)
	    	    list.append(ael.date_from_time(t.time))
    list.sort()
    #print list
    if len(list) != 0:
    	return list[len(list)-1]
    else:
    	return 0

    
#main
def GetLast(n,id,*rest):

    p = ael.Portfolio[id]
    t = p.trades()
    
    if t == None:
    	#print 'None'
	return 0
	
    else:
    	list = []
    
        for tr in t:
    	    tup = tr.trdnbr, tr.time
    	    list.append(tup)

    	list.sort()
    	return list[len(list)-1][0]


