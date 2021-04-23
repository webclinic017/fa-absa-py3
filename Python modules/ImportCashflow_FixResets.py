import ael

def fix_resets(i,*rest):

    legs = i.legs()
    for l in legs:
    	if l.type == 'Float':
    	    cfs = l.cash_flows()
    	    for cf in cfs:
	    	cfr = cf.resets()
    	    	if len(cfr) > 0:
    	    	    x = cfr[0]
    	    	    xc = x.clone()

    	    	    xc.day = cf.start_day
    	    	    xc.start_day = cf.start_day
    	    	    xc.end_day = cf.end_day

		    xc.commit()
    print(1)
    return 1

#fix_resets(ael.Instrument['ZAR/IRS/F-JI/031009-131009/9.86/#1'])

#'ZAR/IRS/F-JI/030912-210331/10.28'
#'ZAR/IRS/F-JI/031001-051201/8.88/#1'
#'ZAR/IRS/F-JI/031009-121009/9.66/#2'
#'Alco15y'
#ZAR/IRS/F-JI/031009-131009/9.86/#1



