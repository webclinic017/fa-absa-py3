'''
Purpose                       :  Called by the SANLD_AEL_Exercise_Trade ASQL query 
                                 to exercise FX Option trades intraday.
Department and Desk           :  NLD Desk
Requester                     :  Emlind Assur
Developer                     :  Herman Hoon
CR Number                     :  489649 
Date                          :  2010-11-09
'''

import ael

def exercise(temp, filtid, trdnbr, *rest):

    if filtid != '':
        trd_filter = ael.TradeFilter[filtid]
        trades = trd_filter.trades()
    elif trdnbr != '':
        trade = ael.Trade[int(trdnbr)]
        trades = [trade]
    else:
        trades = []
        print('No trade filter or trade selected')
    
    for t in trades:
    	flag = 0
    	contr = ael.Trade.select('contract_trdnbr = %d' %(t.trdnbr))
    	
    	if t.type == 'Exercise':
            flag = 1
            
    	for c in contr:
	    if c.type == 'Exercise' and c.status != 'Void':
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
	    new_trd.status = 'FO Confirmed'

	    try:
                new_trd.commit()
                print('New trade has been successfully booked', new_trd.trdnbr)
            except Exception, err:
                print('Error committing trade', t.trdnbr, err)
	    
	else:
	    print('This trade has already been exercised', t.trdnbr)
    return "Success"
	    
#exercise('NLD_All_Trades_MaturedOptions')
