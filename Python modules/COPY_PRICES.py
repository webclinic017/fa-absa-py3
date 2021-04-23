import ael
def copy_mtm_to_spot(ins):
    ael.poll()
    for i in ins:
    	hp = 0
	spot = 0
    	instr = ael.Instrument[i]
	current = instr.prices()
	for c in current:

	    np = c.clone()
	    np.day = ael.date_today()
	    print(np.pp())
#	    np.commit()
    ael.poll()
    print('**************************************')
    print('**************************************')
    print('**************************************')    
    print('******Copied the spot prices End *****')	
    print('**************************************')
    print('**************************************')
    print('**************************************')	
copy_mtm_to_spot(['ZAR/R194'])
    	
