import ael

#Instruments with exercise or break events

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
	
   

    MySubject = "Hybrid instrument exercise/break event %s"% (date)
    MyOutput = ''
    
    for i in ins_list:
#    	print i.insid
    	Events = i.exercise_events()
    	
    	for e in Events:
    	    if e.day == sdate: 
   	    	
    	    	MyOutput = MyOutput + 'Exercise/Break event ' + str(e.day) + ' for instrument ' + i.insid + '\n\n'
	
#	    	print MySubject,MyOutput
		

    if MyOutput == '':
#    	print 'There are no termination events today'
    	return 'There are no exercise/break events today'	
    else:
    	try:
    	    ael.sendmail(user_email, MySubject, MyOutput)
            return 'Mail sent successfully'
    	except:
	    return 'Error sending mail'	


    return ''


	 
#Specification of trade filters applicable to particular email address 
#print 'Starting Trade Check'
#CheckInstruments(1, 'ZAR/IRS/F-JI/060601-070601/7.625/#4', 'sjanevds@absa.co.za')
#CheckInstruments(1, 'IR_Opts_OPEN',  ael.date_today(), 'sjanevds@absa.co.za') 

     



    	

