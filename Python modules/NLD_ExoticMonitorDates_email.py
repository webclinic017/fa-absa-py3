import ael

#Email notification of NLD intruments with exotic monitoring dates today

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
	
   

    MySubject = "Instrument exotic monitoring date %s" %(sdate)
    MyOutput = ''
    
    for i in ins_list:
#    	print i.insid
    	MonitorDates = i.exotic_events()
    	
    	for e in MonitorDates:
            if e.date == sdate: 
   	    	
                MyOutput = MyOutput + 'Exotic monitoring ' + str(e.date) + ' for FRONT trade number ' + str(t.trdnbr) + ', category ' + '"' + (str)(i.category_chlnbr.entry) + '"' + '\n\n'
	
#	        print MySubject,MyOutput
		

    if MyOutput == '':
#    	    print 'There are no exotic monitoring dates today'
    	    return 'There are no exotic monitoring dates today'	
    else:
        try:
            ael.sendmail(user_email, MySubject, MyOutput)
            return 'Mail sent successfully'
        except:
            return 'Error sending mail'	


    	return ''


	 
#Specification of trade filters applicable to particular email address 
#print 'Starting Trade Check'
#CheckInstruments(1, 'Test2',  ael.date_today(), 'aaedaw@absa.co.za') 
	
     



    	

