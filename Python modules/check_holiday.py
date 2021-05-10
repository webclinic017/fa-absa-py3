import ael

def findday(temp, pay_day, curr, *rest):
    day = pay_day.to_string('%a')
    pd = pay_day.to_string()
    i = ael.Instrument[curr]
    if day in ('Sun', 'Sat'):
    	return day
    else:
    	bankingd = pay_day.adjust_to_banking_day(i)
	if pd != bankingd.to_string():
	    return i.insid + ' Holiday'
        else:
	    return '1'
    
#main
#pay_day = ael.date_today().add_days(292)
#print pay_day
#print findday('temp', pay_day, 1)


