import ael, string

def file_upload(temp):

    #filename = 'c:\Cashflow_TakeOn_mon.csv'  
    filename = 'c:\Cashflow_Upload_FixedAmounts.csv'    
    print filename

    count = 0
    prev_trdnbr = 0
    fail_list = []
    ins_list = []
    not_com = []
    flag = 0

    try:
    	f = open(filename)
    except:
    	print 'Could not open file'
	return

    line = f.readline()    	
    line = f.readline()
    while line:
    	l = string.split(line, ',')
	base_nom = (float)(l[0])
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
	i = t.insaddr
	
	
	if (count == 0) or (prev_trdnbr != trdnbr):
	    #if first cashflow of new trade
	    prev_trdnbr = trdnbr	    
	
	    if ins_list.__contains__(i.insaddr):
	    	print 'YES'
	    	not_com.append(t.trdnbr)
    	    	flag = 1
    	    else:
	    	ins_list.append(i.insaddr)
		flag = 0

    	if flag == 0:
    	    		
	    legs = i.legs()
	    l_clone = legs[0].clone()
#	    print trdnbr, l_clone.legnbr, nom
	
	
            newcf = ael.CashFlow.new(l_clone)
	    newcf.type = type
#	    newcf.start_day = start_day
#	    newcf.end_day = end_day
	    newcf.pay_day = pay_day
	    newcf.nominal_factor = 1
    	    newcf.fixed_amount = (nom / base_nom)
	
    	    try:
	        newcf.commit()
    	        print 'Nominal factor', newcf.nominal_factor, newcf.nominal_amount()
	        print
	        print 'New cashflow committed'
    	    except:
	        print 'Unable to commit cashflow'
    	        fail_list.append(trdnbr)
	
	count = count + 1

    	line = f.readline()  
	
    f.close()
    
    print 'Cashflows committed : ', count
    print 'Cashflows not committed : ', fail_list
    print 'Same instrument : ', not_com



# main
print '\nStart Upload\n'
file_upload(1)
print '\nUpload Complete\n'
	    
   
