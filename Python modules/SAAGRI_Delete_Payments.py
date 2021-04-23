import ael

ins = ael.Instrument.select('instype = "Future/Forward"')
    
for i in ins:
#    if i.exp_day >= ael.date_today():
    count = 0
    trds = i.trades()
    for t in trds:
    	if t.add_info('AgriTransportDiff') != '':
	    count = count + 1
	    
	    if count == 1:
	    	i_clone = i.clone()
    	    	i_clone.paytype = 'Future'
		
	    try:
	    	i_clone.commit()
	    	print('Instrument ', i_clone.insid, ' committed')
   	    except:
    	       	print('Error committing instrument ', i_clone.insid)
				
    	    ael.poll()
	    t_clone = t.clone()
    	    pay = t_clone.payments()
	    
	    for p in pay:
	    	p.delete()
#		try:
#		    p.delete()
#		except:
#		    print t.trdnbr

    	    t_clone.commit()
		    
	    ael.poll()
    


'''

	    if count == 1:
	    	i_clone = i.clone()
		i_clone.extern_id1 = 'Transport Fee'
		    
    	    print t.trdnbr
    	    pay = t.payments()
    	    t_clone = t.clone()

    	    for p in pay:
	    	p_clone = p.clone()
		p_clone.type = 'Broker Fee'

	    try:
	    	p_clone.commit()
	    	print 'Payment committed'
   	    except:
    	       	print 'Error committing payment '


    	    ael.poll()		
	    try:
	    	i_clone.commit()
	    	print 'Instrument committed'
   	    except:
    	       	print 'Error committing instrument'


'''
