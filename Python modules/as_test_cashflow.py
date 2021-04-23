import ael, string

def file_upload(temp):

#    filename = 'c:\Cashflow_TakeOn.csv'
    filename = 'c:\Cashflow_TakeOn_One_Trade_temp.csv'    
    print filename

    count = 0
    prev_trdnbr = 0
    fail_list = []

    try:
    	f = open(filename)
    except:
    	print 'Could not open file'
	return

    line = f.readline()    	
    line = f.readline()
    while line:
    	l = string.split(line, ',')
	swapnbr = l[0]
	trdnbr = (int)(l[1])
	p_r = l[2]
	type = l[3]
	nom = (float)(l[4])
	start_day = ael.date_from_string(l[5])
	end_day = ael.date_from_string(l[6])
	pay_day = ael.date_from_string(l[7])
	rate = (float)(l[8])
	proj_cf = (float)(l[9])
	
    	t = ael.Trade[trdnbr]
	if t.prfnbr.prfid == 'IRP 2304':
	    print 'HELLO'
    	    line = f.readline()  
    	    break
	else:
	    print t.prfnbr.prfid
	    line = f.readline()  
	    break
	t_clone = t.clone()
	i = t.insaddr
 	legs = i.legs()
	l_clone = legs[0].clone()
#	print trdnbr, l_clone.legnbr, nom
	
	if (count == 0) or (prev_trdnbr != trdnbr):
	    #if first cashflow of new trade
	    base_nom = nom
	    t_clone.quantity = base_nom / i.contr_size
	    prev_trdnbr = trdnbr
    	    t_clone.text1 = 'swapnbr ' + swapnbr
	    if p_r == 'Receive':
	    	l_clone.payleg = 0
	    else:
	    	l_clone.payleg = 0
		

		
	    cfs = l_clone.cash_flows()
    	    for c in cfs:
#    	        c.delete()
	        try:
   	    	    c.delete()
    	    	    pass
	    	except:
	    	    print 'Unable to delete cashflow ', c.cfwnbr, ' for trade ', t.trdnbr

    	    try:
	    	print 'Nominal', t.nominal_amount(t.value_day)
	    	t_clone.commit()
	    	l_clone.commit()	
	    except:
	    	print 'Error committing trade or leg\n'

   	newcf = ael.CashFlow.new(l_clone)
	newcf.type = type
	newcf.start_day = start_day
	newcf.end_day = end_day
	newcf.pay_day = pay_day
	newcf.rate = rate
	if (count == 0) or (prev_trdnbr != trdnbr):
	    newcf.nominal_factor = 1
	else:    
	    newcf.nominal_factor = (nom / base_nom) 
	    #* -1
	
#	print
#	print newcf.pp()
	
	try:
	    newcf.commit()
#    	    print 'Nominal factor', newcf.nominal_factor, newcf.nominal_amount()
	    print
	    print 'New cashflow committed'
	except:
	    print 'Unable to commit cashflow'
    	    fail_list.append(trdnbr)
	
	count = count + 1
	line = f.readline()  
	
	
    f.close()
	
#    print
    print 'Cashflows committed : ', count
    print 'Trades not committed : ', fail_list





# main
print '\nStart Upload\n'
file_upload(1)
print '\nUpload Complete\n'
	    
   
