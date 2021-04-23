import ael

trades = ael.Portfolio['Agri ABL3 Options OTC'].trades()
for t in trades:
    ins = t.insaddr.insid
    insadd = t.insaddr.insaddr
    i = ael.Instrument[insadd]
    i_clone = i.clone()
    if i_clone.exp_day >= ael.date_today():
    	if i_clone.product_chlnbr.seqnbr == 1207:
    	    print(i_clone.insid)
    	    i_clone.product_chlnbr = 632
    	    i_clone.commit()
    ael.poll()
    		
