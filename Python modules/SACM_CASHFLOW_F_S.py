import ael
def firstcf(t,*rest):
    list = []
    l = t.legs()
    cf = l[0].cash_flows()
    for d in cf:
    	if d.end_day:
    	    list.append(d.end_day)
    list.sort()	
    return list[0].to_string()	

def secondcf(t,*rest):
    list = []
    l = t.legs()
    cf= l[0].cash_flows()
    for d in cf:
    	if d.end_day:
    	    list.append(d.end_day)
    list.sort()
    print(t.insid)
    return list[1].to_string()

def nominal_firstcf(t,*rest):
 
    i = t.insaddr
    firstcfday = firstcf(i)
    l = i.legs()
    for cf in l[0].cash_flows():
    	if cf.pay_day.to_string() == firstcfday:
	    #print cf.nominal_amount(ael.date_from_time(t.time))
	    return cf.nominal_factor * cf.legnbr.nominal_factor * cf.legnbr.insaddr.contr_size * t.quantity
	    
def firstcf_start_day(t,*rest):
    list = []
    l = t.legs()
    cf = l[0].cash_flows()
    for d in cf:
    	list.append(d.start_day)
    list.sort()	
    return list[0].to_string()		    


#main
#t = ael.Instrument['ZAR/GFC1']
#print secondcf(t)
