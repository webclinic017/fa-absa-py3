import ael

def Safex_MTM_Rates(test,e, *rest):
    today = ael.date_today()
    near = ''
    if e.und_insaddr != 0:
    	futures = ael.Instrument.select('und_insaddr = %d' % (e.insaddr))

    	#get the first (non-expired) future in the list    
    	for f in futures:
    	    if f.exp_day >= today:
	    	near = f
	    
    	#get the closest future from today
    	for f in futures:
    	    if f.exp_day >= today and f.exp_day < near.exp_day:
	    	near = f

    	if near == '':
	    return 0.0
	else:
    	    return near.used_price()
    else: 
    	return 0.0
    
