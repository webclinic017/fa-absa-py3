import ael
def del_pmm(filter):
    for trd in ael.TradeFilter[filter].trades():
        ins = trd.insaddr
    	try:
    	    trd.delete()
    	except:
    	    print(trd.trdnbr)
	try:
	    ins.delete()
    	except:
	    print('ins')
del_pmm('SAMM_Primary_Trades')
