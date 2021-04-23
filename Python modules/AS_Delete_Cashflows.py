import ael, time

count = 0
ex = 0
print(ael.date_today())

cfs = ael.CashFlow.select()
for c in cfs:
    if (c.creat_usrnbr.userid == 'ABAW339') and (time.strftime("%Y-%m-%d", time.gmtime(c.creat_time)) == ael.date_today): 
    	t = time.strftime("%Y-%m-%d", time.gmtime(c.creat_time))
#	print t[0] + '-' + t[1] + '-' + t[3]
	print(t)
	count = count + 1
    else:
    	ex = ex + 1
	
print('count', count, ex)

