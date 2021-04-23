import ael


def CopyTrade(temp, trd, *rest):
    i = ael.Instrument[trd.insaddr.insid]
    new_i = i.new()
    new_i.insid = trd.insaddr.insid + 'NEW11'
    new_i.commit()
    
    ael.poll()
    
    base_trade = trd
    ins = t.insaddr
    #ins = ael.Insturment[t.insaddr.insid]
    trade = ael.Trade.new(new_i)
    

    #base_trade = ael.Trade[tr.trdnbr]
    #ins = ael.Instrument[base_trade.insaddr.insid]
   
    trade = base_trade.clone()
    trade.time = base_trade.time
    #trade.execution_time = base_trade.execution_time
    #trade.protection = base_trade.protection
    trade.quantity = base_trade.quantity
    trade.price = base_trade.price
    trade.premium = base_trade.premium
    trade.curr = base_trade.curr
    trade.owner_usrnbr = base_trade.owner_usrnbr
    trade.trader_usrnbr = base_trade.trader_usrnbr
    #trade.prfnbr = portf.prfnbr
    trade.prfnbr = base_trade.prfnbr
    trade.acquire_day = base_trade.acquire_day
    trade.value_day = base_trade.acquire_day
    #trade.acquirer_ptynbr = party.ptynbr
    trade.acquirer_ptynbr = base_trade.acquirer_ptynbr
    trade.counterparty_ptynbr = base_trade.counterparty_ptynbr
    trade.optkey1_chlnbr = base_trade.optkey1_chlnbr
    trade.optkey2_chlnbr = base_trade.optkey2_chlnbr
    trade.status = base_trade.status
    print(trade.pp())
    trade.commit()


    '''
    new_t = trd
    new_t.counterparty_ptynbr = t.counterparty_ptynbr
    new_t.commit()
    '''
    
    
    
    '''
    #i_clone = t.insaddr.clone()
    t_clone = t.clone()
    print 'BEFORE', new_t.pp()
    #new_i = i
     
    new_t.quantity = t_clone.quantity + 1
    print new_t.pp()
    print '\n\n\n'
    print t_clone.pp()
    
    #new_i.commit()
    new_t.commit()
    t_clone.commit()
    #i_clone.commit()
    '''
    
    '''
    try:
        new_i.commit()
        new_t.commit()
        print new_t.pp()
        print 'Done'
        
    except:
        print 'Error committing Trade'
    '''
    
    return 'Success'


#main
t = ael.Trade[826093]
print(CopyTrade(1, t))






def add_cashflow(trd, type, value, factor, dat, subtype):
    legs = trd.insaddr.legs()
    l = legs[0].clone()
    
    if abs(value) > 0.000000001:
    	cf = ael.CashFlow.new(l)
    	cf.type = type 
    else:
    	return 'No Cashflow Booked'
    
    if type in ('Fixed Amount'):
    	cf.fixed_amount = value
     	cf.nominal_factor = 1
    	cf.pay_day = dat

    try:
    	cf.commit()
	#print 'Cashflow committed'
	return 'Success'
    except:
    	print('Error commiting cashflow')
    	return 'Error'
 
    

