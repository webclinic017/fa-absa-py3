import ael

#Email notification of NLD intruments with fixings today

def CheckInstruments(temp, trdfilter, date, user_email, *rest):


    try:
    	sdate = ael.date_from_string(date)
    except:
#       	print '\n argument1 not in string format\n'
	sdate = date


    TradeFilter = ael.TradeFilter[trdfilter]
    Trades = TradeFilter.trades()
     
    ins_list = []
    
    for t in Trades:
#    	print dir(ins_list)
#	if ins_list.__contains__(t.insaddr) == 1:
#	    print t.insaddr, 'Already in list'
#	    pass
#	else:
    	ins_list.append(t.insaddr)
	
   

    MySubject = "Instrument fixing %s" %(sdate)
    MyOutput = ''
    
    for i in ins_list:
#    	print i.insid
    	Fixings = i.exotic_events()
    	
    	for ev in Fixings:
            if ev.date == sdate: 
   	    	
                MyOutput = MyOutput + 'Fixing ' + str(ev.date) + ' for FRONT trade number ' + str(t.trdnbr) + ' (' + str(t.optional_key) + ')' + '\n\n'
	
#	    	print MySubject,MyOutput
		

    if MyOutput == '':
#       print 'There are no fixings today'
    	return 'There are no fixings today'	
    else:
    	try:
    	    ael.sendmail(user_email, MySubject, MyOutput)
            return 'Mail sent successfully'
    	except:
	    return 'Error sending mail'	


    return ''




	 
#Specification of trade filters applicable to particular email address 
#print 'Starting Trade Check'
#CheckInstruments(1, 'NLD_Fixings',  ael.date_today(), 'sjanevds@absa.co.za') 
	
     



    	

