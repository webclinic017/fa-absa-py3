
########################################################
# this AEL is the same as SAGEN_Cashflow_Upload     	    	
# but it only uploads cashflows for portfolio IRP 2304'


import ael, string

def file_upload(temp):

    filename = 'c:\Cashflow_TakeOn_642546_WED.csv'
#    filename = 'c:\Cashflow_TakeOn_2304.csv'    
    print filename

    count = 0
    prev_trdnbr = 0
    fail_list = []
    prflist = []
    prfcount = 0

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
	legnbr = (float)(l[10])
	fwd = (float)(l[11])
	
    	t = ael.Trade[trdnbr]
	if t.prfnbr.prfid == 'IRP 2304':
	    t_clone = t.clone()
	    i = t.insaddr
 	    legs = i.legs()
	    
	    for l in legs:
    	    	print l.legnbr, legnbr
	    	if l.legnbr == legnbr:
	    	    		
		    l_clone = l.clone()

#	    print trdnbr, l_clone.legnbr, nom
	
   	    newcf = ael.CashFlow.new(l_clone)
	    newcf.type = type
	    newcf.start_day = start_day
	    newcf.end_day = end_day
	    newcf.pay_day = pay_day
	    newcf.rate = rate
    	    newcf.nominal_factor = 1	    
    	    if type == 'Float Rate':
    	    	newcf.float_rate_factor = 1
	    else:
    	    	newcf.float_rate_factor = 0

#	    if (count == 0) or (prev_trdnbr != trdnbr):
#	    	newcf.nominal_factor = 1
#	    else:    
#	    	newcf.nominal_factor = (nom / base_nom) 
	    	#* -1
	
#   	    print
#    	    print newcf.pp()
	
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
	

 	else:
	    print t.prfnbr.prfid
	    prflist.append(t.trdnbr)
	    prfcount = prfcount + 1
	    line = f.readline()  
	
    f.close()
	
#    print
    print 'Cashflows committed : ', count
    print 'Trades not committed : ', fail_list
    print 'Trade not in portfolio IRP 2304 : ', prflist





# main
print '\nStart Upload\n'
print 'Only uploading cashflows for portfolio IRP 2304\n'
file_upload(1)
print '\nUpload Complete\n'
	    
   
