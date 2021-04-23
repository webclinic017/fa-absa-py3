import ael, SAGEN_Functions
print 'Start SAEQ_Notional_amount'
print ael.date_today()
trades = ael.Trade.select()
count = 0
for t in trades:
    if t.insaddr.instype in ['Option', 'Future/Forward', 'Warrant'] and t.insaddr.exp_day > ael.date_from_string('2004-12-31') and t.counterparty_ptynbr and t.prfnbr and (ael.date_from_time(t.creat_time) >= ael.date_today() or ael.date_from_time(t.insaddr.updat_time) >= ael.date_today() or ael.date_from_time(t.updat_time) >= ael.date_today()):
#    if t.insaddr.instype in ['Option','Future/Forward','Warrant'] and t.insaddr.exp_day > ael.date_from_string('2005-02-22') and t.counterparty_ptynbr and t.prfnbr and (ael.date_from_time(t.creat_time) >= ael.date_from_string('2005-04-22') or ael.date_from_time(t.insaddr.updat_time) >= ael.date_from_string('2005-02-22') or ael.date_from_time(t.updat_time) >= ael.date_from_string('2005-02-22')):
    	print 'TT', t.trdnbr
	if  (t.prfnbr.prfid in ['VOE', 'AVOE', 'GDOP', 'G7OE']) or(t.counterparty_ptynbr.ptyid2 == 'SAFEX') or (t.insaddr.instype == 'Warrant'):
#	    print 'SS', t.trdnbr
    	    ins = t.insaddr
    	    und = t.insaddr.und_insaddr
	    date = ael.date_from_time(t.time)
#    	    print t.trdnbr,' ',t.insaddr.insid,' ',und.insid,' ',ael.date_from_time(t.time),' ',und.used_price(date,ins.curr.insid,None,None,'SPOT')
	    if und.insid == 'ZAR/ALSI':
	        notional = t.nominal_amount() * und.used_price(date, 'ZAR', None, None, 'SPOT') * 10
	    else:
    	        notional = t.nominal_amount() * und.used_price(date, 'ZAR', None, None, 'SPOT')
    	    #ai = t.additional_infos()
	    notional = notional
	    if t.insaddr.instype == 'Warrant':
	        notional = notional / 100
	    SAGEN_Functions.set_trade_addinf(t, 'Notional Amount', notional)
print 'Finished with SAEQ_Notional_amount.'
