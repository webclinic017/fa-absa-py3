import ael
def copy_mtm_to_spot(ins):
    ael.poll()
    for i in ins:
    	hp = 0
	spot = 0
    	instr = ael.Instrument[i]
	hist = instr.historical_prices()
	current = instr.prices()
	for c in current:
	    print(c.pp())
	    if c.ptynbr.ptynbr == 10:
	    	spot = c
	np = spot.clone()
	for h in hist:
	    if (h.day == ael.date_today()) and (h.ptynbr == ael.Party['internal']):
	    	hp = h
		print(h.pp())
	if hp != 0:
	    np.settle = hp.settle
	    np.day = ael.date_today()
	    np.ptynbr = 10
	    np.curr = hp.curr
	    print(np.pp())
	    np.commit()
    ael.poll()
    print('**************************************')
    print('**************************************')
    print('**************************************')    
    print('******Copied the spot prices End *****')	
    print('**************************************')
    print('**************************************')
    print('**************************************')	
#copy_mtm_to_spot(['ZAR/PIC_BASKET'])
    	
