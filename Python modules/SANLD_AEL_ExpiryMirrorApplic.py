import ael

def trdflt():
    list = []
    for tf in ael.TradeFilter.select():
        list.append(tf.fltid)
    return list
    
    
    
# included rebate amount    
def exercise(temp, filtid, *rest):

    trd_filter = ael.TradeFilter[filtid]
    #print trd_filter
    #print ael.date_today()
    #print trd_filter.trades()
    for t in trd_filter.trades():

        flag = 0
        contr = ael.Trade.select('contract_trdnbr = %d' %(t.trdnbr))
        #print contr[0].trdnbr
        for c in contr:
            if c.type == 'Exercise':
                flag = 1
    
        i = t.insaddr
        pflag = 1
        if i.instype == 'Option' and i.exotic_type != 'None':
            if i.exotic() != None:
                if i.exotic().barrier_option_type != None:
                    if i.rebate != 0:
                        if i.exotic().barrier_rebate_on_expiry == 1:
                            #if i.exotic().barrier_crossed_status == 'Crossed':          
                              if ((i.digital == 'NO' and i.exotic().barrier_option_type in ('Up & In', 'Down & In') and i.exotic().barrier_crossed_status == 'None')
                                or i.digital == 'YES'):
                                trds = ael.Trade.select('insaddr = ' + str(i.insaddr))
                                for t in trds:
                                    #print t.trdnbr
                                    for p in t.payments():
                                        #print p.pp()
                                        if p.text in ('Rebate', 'REBATE', 'rebate'):
                                            pflag = 0
                                            
                                '''
                                if i.digital == 'YES':
                                    trds = ael.Trade.select('insaddr = ' + str(i.insaddr))
                                    for t in trds:
                                        #print t.trdnbr
                                        for p in t.payments():
                                            #print p.pp()
                                            if p.text in ('Rebate', 'REBATE', 'rebate'):
                                                pflag = 0
                                '''
                            
                
                '''
                if i.exotic().barrier_option_type != None and i.exotic().barrier_rebate_on_expiry == 1:
                    trds = ael.Trade.select('insaddr = ' + str(i.insaddr))
                    for t in trds:
                        #print t.trdnbr
                        for p in t.payments():
                            #print p.pp()
                            if p.text in ('Rebate', 'REBATE', 'rebate'):
                                pflag = 0
                '''
        else:
            pflag = 0
            
                            
        if (flag == 0) and (pflag == 0):
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
            new_trd.curr = t.curr
            new_trd.status = t.status
            new_trd.commit()
            print 'New trade has been successfully booked'
        elif pflag != 0:
            print 'Please book additional payment with Text = Rebate AEL'
        elif flag != 0:
            print 'This trade has already been exercised', t.trdnbr
        else:
            print 'Trade not mirrored'
        
    return "Success"
    
    
    
def exercise_old(temp, filtid, *rest):
    trd_filter = ael.TradeFilter[filtid]
    print trd_filter
    print ael.date_today()
    print trd_filter.trades()
    for t in trd_filter.trades():
    	flag = 0
    	contr = ael.Trade.select('contract_trdnbr = %d' %(t.trdnbr))
	print contr[0].trdnbr
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
	    new_trd.curr = t.curr
	    new_trd.status = t.status
	    new_trd.commit()
	    print 'New trade has been successfully booked'
	else:
	    print 'This trade has already been exercised', t.trdnbr
    return "Success"



ael_variables = [('trd_filter', 'Trade Filter', 'string', trdflt(), None, 1, 0)]

def ael_main(ael_dict):
    #tradefilter = 'NLD_All_Trades_MaturedOptions'
    tmpfile = ael_dict["trd_filter"]
	    
    exercise(1, tmpfile, 1)
