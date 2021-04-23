import ael
port = ael.Portfolio['GOLD']
pr=ael.Trade.select('prfnbr = %d' %port.prfnbr)
for t in pr:
    #print t.trdnbr
    try:
    	t.delete()
    except:
    	ErrMsg = 'update trade set status = 7 where trdnbr = ' + str(t.trdnbr)
	print(ErrMsg)
	ael.log(ErrMsg)
