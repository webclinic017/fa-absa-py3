import ael, string


def change_to_amort(ins, new_r, *rest):

    i = ael.Instrument[ins]
#    i_clone = i.clone()

    new_rate = (float)(new_r)
    
    trades = i.trades()
    for t in trades:
    	t_clone = t.clone()
	t_clone.price = new_rate
	try:
	    t_clone.commit()
	    print 'Trade ', t.trdnbr, 'price changed to ', new_rate
	except:
	    print 'Error committing trade'
	    return 'Error committing trade'


    legs = i.legs()    
    for l in legs:
    	l_clone = l.clone()
	l_clone.fixed_rate = new_rate
	l_clone.rolling_period = '1m'
	l_clone.annuity_rate = new_rate
    	l_clone.amort_period = '1m'
	l_clone.amort_start_day = i.start_day
	l_clone.amort_end_day = i.exp_day
	l_clone.amort_generation = 'Target End'
	l_clone.amort_end_nominal_factor = 0.0
	l_clone.amort_type = 'Annuity'
	
#   	only for long-stub trades
    	#l_clone.long_stub = 1
	try:
	    l_clone.regenerate()
	    print 'Cashflows successfully regenerated'	    
	    l_clone.commit()
	    print 'Leg ', l.legnbr, 'committed'
	except:
	    print 'Error committing leg 1'
	    return 'Error committing leg 1'
	    
    	ael.poll()
	
    return 'Success'

 
   

def instruments():
    instruments = ael.Instrument.select('instype = "Deposit"')
    ins = []
    for i in instruments:
    	ins.append(i.insid)
    return ins


#Upload file variable must be in this format "C:\\FDI.csv"

ael_variables = [('ins', 'Instrument ID', 'string', instruments(), None, 0),
    	    	 ('new_rate', 'New Rate', 'double', None, None, 0),
		 ('file', 'Upload File', 'string', None, None, 0)]


def ael_main(ael_dict):

    ins = ael_dict["ins"]
#   ZAR/050131-051031/7.475/#10        

    new_rate = ael_dict["new_rate"]
 
    filename = ael_dict["file"]
#    print filename

    count = 0
    fail_list = []
    if filename != None:
    	try:
    	    f = open(filename)
    	except:
            print 'Could not open file'
	    return
    	
	line = f.readline()
    	while line:
	    l = string.split(line, ',')
    	    ins = l[0]
	    new_rate = l[1]
#	    print ins, new_rate
	    if change_to_amort(ins, new_rate) == 'Success':
	    	count = count + 1
    	    else:
	    	fail_list.append(ins) 	   
	    line = f.readline()
    	f.close()
	
    else:
    	if change_to_amort(ins, new_rate) == 'Success':
	    count = count + 1
	else:
	    fail_list.append(ins) 	   
	
	
	
    print
    print 'Instruments committed : ', count
    print 'Instruments not committed : ', fail_list

	    
   
