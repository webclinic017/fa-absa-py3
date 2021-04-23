import ael

trds = ael.TradeFilter['NLD_All_Trades'].trades()
count = 0
Notcount = 0
for t in trds:
    if t.status == 'BO Confirmed':
    	if (t.your_ref != '0') and (t.your_ref != ''):
	    tclone = t.clone()
	    tclone.status = 'BO-BO Confirmed'
	    try:
	    	tclone.commit()
		print(t.trdnbr, ' changed to BO-BO Confirmed')
    	    	count = count + 1   
	    except:
	    	print('Unable to commit trade ', t.trdnbr)
		Notcount = Notcount + 1   

print('Trades commited ', count)
print('Uncomitted trades ', Notcount)



