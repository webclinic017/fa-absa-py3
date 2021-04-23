import ael
chl = ael.ChoiceList[979]
q = '''select
    	    insaddr
    from 
    	instrument
    where
/*    	instype = "Option"
    and*/ insid like "%FUT/ALSI%"'''
for a in ael.dbsql(q)[0]:
    ins = ael.Instrument[a[0]]
    if (ins.product_chlnbr).display_id() == 'Government' and ins.instype == 'Option' and ins.exp_day >= ael.date_today():
    	print chl.display_id(), '----', (ins.product_chlnbr).display_id()
    	ic = ins.clone()
	ic.product_chlnbr = chl
	ic.otc = 0
	ic.quote_type = 'Per Contract'
	ic.spot_banking_days_offset = 0
	ic.pay_day_offset = 0
	ic.commit()
