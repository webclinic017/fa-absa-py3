import ael

def InstrumentType(t,*rest):
    #print t.trdnbr
    ins = t.insaddr
    if ins.instype == 'Swap':
    	legs = ins.legs()
	flag = 0
	for l in legs:
	    if l.type == 'Float':
	    	flag = flag + 1
	if flag == 2:
	    # Started
	    static = 0
	    for l in legs:
	    	for cf in l.cash_flows():
	    	    if static == 0:
		    	static = t.quantity*ins.contr_size*cf.nominal_factor
		    else:
		    	if t.quantity*ins.contr_size*cf.nominal_factor != static:
		    	    return 'AmortisingPrimeBS'
	    return 'PrimeBS'
	    
	    # Ended
	for l in legs:
	    if l.type == 'Float':
		reset = l.resets() #ael.Reset.read('legnbr=%d' % l.legnbr)
		if reset:
		    if reset[0].type == 'Weighted':
		    	return 'AveSwap'
		    elif reset[0].type == 'Weighted 1m Compound':
		    	return 'ROD'
	
	static = 0
	for l in legs:
	    for cf in l.cash_flows():
	    	if static == 0:
		    static = t.quantity*ins.contr_size*cf.nominal_factor
		else:
		    if t.quantity*ins.contr_size*cf.nominal_factor != static:
		    	return 'Amortising Swap'
	return 'Swap'
    elif ins.instype == 'CurrSwap':
    	legs = ins.legs()
	flag = 0
	for l in legs:
	    if l.payleg == 1:
	    	Pay = l.curr.insid
	    else:
	    	Rec = l.curr.insid
	    if l.type == 'Float':
	    	flag = flag + 1
	if Pay > Rec and flag == 2:
	    return Pay + '-' + Rec + '/BS'
	elif Rec > Pay and flag == 2:
	    return Rec + '-' + Pay + '/BS'
	elif Pay > Rec:
	    return Pay + '-' + Rec + '/CS'
	else:
	    return Rec + '-' + Pay + '/CS'
    elif ins.instype == 'Curr':
    	if t.trade_process  in (4096, 8192, 16384, 32768):
            return 'FxSwap'
        else:
            return ins.instype
    elif ins.instype == 'TotalReturnSwap':
        for l in ins.legs():
            if l.index_ref :
                if l.index_ref.instype in('Stock', 'EquityIndex'):
                    return 'EquitySwap'
        return ins.instype
    else:
    	return ins.instype

#trd = ael.Trade.read('trdnbr = %d' % 178384)	
#intr = InstrumentType(trd)
#print intr

