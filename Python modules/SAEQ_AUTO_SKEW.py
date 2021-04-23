import ael, FC_Calibrate_Skew
def read_CSV(filename, heading, ending):
    list = []
    try:
    	f = open(filename)
    except:
    	print 'File not open'
    ld = []	
    line = f.readline()
    ld = line.split(',')
    tod = ael.date_today()
    dte = ael.date_from_string(ld[6], '%d-%b-%Y')
    #print 'dte',dte
    if dte == ael.date_today().add_days(0):
        while line:
	    l = []
	    line = line.rstrip()
	    l = line.split(',')
	    if l[0] == heading:
	    	l = []
	    	line = f.readline()	
		line = line.rstrip()
		l = line.split(',')
		while l[0] != ending: 
	    	    #print l
		    list.append(l)
		    l = []
	    	    line = f.readline()	
		    line = line.rstrip()
		    l = line.split(',')
	    line = f.readline()
    else:
    	ael.log('Incorrect data for today. The date on the file is not the same as today todays date')
	print 'Incorrect data for today. The date on the file is not the same as todays date'
    f.close()
    return list	
def update_safexskew(filename, begin, end):
    list = read_CSV(filename, begin, end)
    for l in list:
    	dte = ael.date_from_string(l[0], '%d-%b-%Y')
	mtm = (int)(l[5])
	if l[6] == '':
	    vol = (float)(l[7]) 
	else:
	    vol = (float)(l[6]) 
	print 'Date= ', dte, vol
	#print dir(dte)
	ins = ael.Instrument.select('instype = "Future/Forward"')
	for i in ins:
	    if i.exp_day == dte and i.otc != 1 and i.insid.startswith('ZAR/ALSI'):
	       	print 'INS= ', i.insid, ' ####STEP 4####'
		try:
		    FC_Calibrate_Skew.SkewCalibrate(None, '4_Config Daily Vol Surface', i.insid, 0.0, mtm, 0.0, vol, 0.0, 0.0)
		except:
		    print 'step 4 did not run'
		vs = ael.Volatility['Safex ATM Options'].clone()
		for vp in vs.points():
		    if vp.insaddr.exp_day == i.exp_day:
		    	print 'In VP'
		    	vpc = vp.clone()
			vpc.volatility = vol/100.0
			vpc.commit()
		vs.commit()
    ael.poll()
    for l1 in list:
    	dte = ael.date_from_string(l1[0], '%d-%b-%Y')
	mtm = (int)(l1[5])
	if l1[6] == '':
	    vol = (float)(l1[7])  
	else:
	    vol = (float)(l1[6])	
	print 'Date= ', dte, vol
	ins1 = ael.Instrument.select('instype = "Future/Forward"')
	for i in ins1:
	    if i.exp_day == dte and i.otc != 1 and i.insid.startswith('ZAR/ALSI'):
	       	print 'INS= ', i.insid, ' ####STEP 5####'
		try:
		    FC_Calibrate_Skew.SkewCalibrate(None, '5_Calibrate Daily Shift', i.insid, 0.0, mtm, 0.0, vol, 0.0, 0.0)
		except:
		    print 'Step 5 did not run'
	print 'MTM_Price= ', mtm
	print 'Volatility= ', vol 


update_safexskew('\\\\atlasprd\\BackOffice\\Safex_MTM\\Safex_MTM_Mini.csv', 'FTSE/JSE TOP 40 INDEX (ALSI)', 'FTSE/JSE INDI 25 INDEX (INDI) ')
