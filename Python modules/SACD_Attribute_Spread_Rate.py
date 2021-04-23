import ael, amb
def get_yield_rate_attr(i,*rest):
    list = [0, 1, 2, 3, 4, 5]
    yc=ael.YieldCurve['CDIssuerCurveFO']
    mbf= yc.get_data_message()
    date = ael.date_today()
    att=mbf.mbf_find_object('ATTRIBUTE_SPREAD')
    obj=att
    i=0
    #filename = 'C:\\ACMBAttribute_spread.csv'
    #UNIX Automation Method
    #filename = '/frontnt/dart/ERM/SACD_Attribute_Spread.csv'
    filename = '/services/frontnt/dart/ERM/sacd_attribute_spread.csv'
    try:
    	f = open(filename, 'w')
    except:
	print 'error with opening filename'
    f.write('Party,Days in Period,End Date,Rate,DATADATE\n')
    while obj and obj.mbf_is_list():
    	i=i+1
        print '------------'
        obj.mbf_find_object('ATTRIBUTE')
	ob = obj.mbf_find_object('ATTRIBUTE')
	att_val = ob.mbf_get_value()
	print ael.Party[(int)(att_val)].ptyid
    	rating=obj.mbf_next_object()
	count = 0
        while rating:
    	    if (count) == 0:
	    	rate = get_und_rate(yc, date, date)
		num = date
	    else:
	    	rate = get_und_rate(yc.underlying_yield_curve_seqnbr, date.add_delta(0, 0, 0), date.add_delta(0, 0, count))
		num = date.add_delta(0, 0, count)
    	    rate = rate * 1
	    spr = (float)(rating.mbf_get_value())
	    #print 'Rating',rating.mbf_get_value()
	    #print 'ZAR_SWAP:' , rate
            rating=obj.mbf_next_object()
	    #print 'days:',   count
	    newr = spr * 100
	    newr = round(newr, 6)
	    daysbetween = date.days_between(num, 'Act/365')
	    #print date.days_between(num, 'Act/365')
#	    print date.add_years
	    print 'New rate: %d : %f ' %(daysbetween, ((spr + rate)*100)) 
	    f.write(ael.Party[(int)(att_val)].ptyid + ',' + str(daysbetween) + ',' + str(num) + ',' + str(newr)+ ',' + ael.date_today().to_string())
	    f.write('\n')	
	    count = count + 1
    	obj=mbf.mbf_next_object()
    f.close()
    return 'file created'
    
def get_und_rate(yc, d1, d2):
    return yc.yc_rate(d1, d2)
