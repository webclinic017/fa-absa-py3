import ael


def third_day(temp, d, *rest):
#    print dir(d)
#    print d

    first_day_of_qtr = d.first_day_of_quarter()
#    print 'first day of qtr', first_day_of_qtr
    fdotm = first_day_of_qtr.add_period('2m')
#    print 'fdotm', fdotm
    flag = 0
    while flag != 1:
    	if fdotm.day_of_week() == 4:
	    flag = 1
	else:
	    fdotm = fdotm.add_days(1)
#	    print 'add 1 day'
    
    q2 = fdotm.add_weeks(2)
#    print fdotm, q2    
    thursday = q2.adjust_to_banking_day(ael.Instrument['ZAR'], 'Preceding')	
    return thursday
    	
	
	
def points(temp, day, buckets, number, *rest):
###   number MUST NOT BE > buckets    	    ###
    if number > buckets:
    	return ael.date_from_string('0001-01-01')
    count = 1
    list = []
    d = ael.date_from_string(day)    

    while count <= buckets:
    	list.append(third_day(1, d))
#    	print 'Third Thursday', list[count-1]	
	d = d.add_period('3m')
#	print
	count = count + 1
	
    return list[number-1].to_string()
    
    
    
    
def linear(temp, d1, mat, d2, value, number, *rest):
    date1 = ael.date_from_string(d1)
    doy1 = date1.day_of_year()
    doymat = mat.day_of_year()
    doytemp = doymat + 0
    date2 = ael.date_from_string(d2)
    doy2 = date2.day_of_year()
    print()
    print('Dates ', date1, mat, date2)
    print(doy1, doymat, doy2, doytemp)
    doymat = doytemp
    print()
    result = ((float)(doy2 - doymat) / (float)(doy2 - doy1)) * value  
    #255
    #result = (doymat - doy1) / (doy2 - doy1) * value  
    #255
    result2 = ((float)(doymat - doy1) / (float)(doy2 - doy1)) * value 
    #244
    print(result, result2)
    print()
    
    if number == 1:
    	return result
    elif number == 2:
    	return result2
    else:
    	return 3
    
    
    
#main
#d1 = '2005-09-15'
#mat = ael.date_from_string('2005-07-01')
#d2 = '2005-09-15'
#value = 500
#d = ael.date_today()

#print points(1, d, 2, 2)

#print linear(1, d1, mat, d2, value)

