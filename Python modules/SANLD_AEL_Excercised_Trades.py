'''
Purpose                       :  Change the trade currency to be equal to instrument
Department and Desk           :  PCG, NLD Desk
Requester                     :  Matt Berry
Developer                     :  Zaakirah kajee
CR Number                     :  423377 
Date                          :  2010-09-07
'''

import ael
def exercise(temp, filtid, *rest):
    trd_filter = ael.TradeFilter[filtid]
    print(trd_filter)
    print(ael.date_today())
    print(trd_filter.trades())
    for t in trd_filter.trades():
    	flag = 0
    	contr = ael.Trade.select('contract_trdnbr = %d' %(t.trdnbr))
	print(contr[0].trdnbr)
    	for c in contr:
	    if c.type == 'Exercise':
	    	flag = 1
	if (flag == 0):
	    new_trd = ael.Trade.new(t.insaddr)
    	    new_trd.type = 'Exercise'
	    new_trd.premium = 0
	    new_trd.quantity = t.quantity * -1
	    new_trd.value_day = ael.date_today()
	    new_trd.acquire_day = ael.date_today()
	    new_trd.contract_trdnbr = t.trdnbr
	    new_trd.prfnbr = t.prfnbr
	    new_trd.counterparty_ptynbr = t.counterparty_ptynbr
	    new_trd.acquirer_ptynbr = t.acquirer_ptynbr
	    new_trd.broker_ptynbr = t.broker_ptynbr
	    new_trd.optkey1_chlnbr = t.optkey1_chlnbr
	    new_trd.time =ael.date_today().to_time()
	    new_trd.curr = t.insaddr.curr
	    new_trd.status = t.status
            if t.optional_key != '':
                new_trd.optional_key = t.optional_key + '/EXEC'
	    try:
                new_trd.commit()
                print('New trade has been successfully booked')
            except:
                print('Error committing trade ', t.trdnbr)
	    
	else:
	    print('This trade has already been exercised', t.trdnbr)
    return "Success"
	    
#exercise('NLD_All_Trades_MaturedOptions')
