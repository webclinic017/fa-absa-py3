import ael, AveReset
def get_RevisedNot(t,date,retvalue,*rest):
    trd = ael.Trade[t.trdnbr]
    #print trd
    orgnom = trd.nominal_amount(trd.value_day)
    nom = trd.nominal_amount(trd.value_day)
    revisedNom = nom
    for l in (trd.insaddr).legs():
    	if l.type == 'Float':
	    firstDay = (l.start_day).first_day_of_month()
    	    monthdays = (l.start_day).days_in_month()
	    monthEnd = firstDay.add_days(monthdays - 1)
	    prevMe = l.start_day
	    count = 0
	    while monthEnd <= date:
	    	print '********************'
	    	ave_rate = AveReset.AveResetAmount(1, t.trdnbr, monthEnd.to_string())
		#print 'AVERAGE Rate', ave_rate 
		if count == 0:
		    #print 'Days: ', (l.start_day).days_between(monthEnd,'Act/365')
		    revisedNom = orgnom * (1.0+(ave_rate/100.00 * (((l.start_day).days_between(monthEnd, 'Act/365')+1)/365.00)))
		else: 
		    if monthEnd == l.end_day:
		    	revisedNom = nom * (1.0+((ave_rate/100.00) * ((prevMe.days_between(monthEnd, 'Act/365')-1)/365.00)))	    
		    else:
		    	revisedNom = nom * (1.0+((ave_rate/100.00) * ((monthEnd.days_in_month())/365.00)))
		print 'DaysinMonth', monthEnd.days_in_month(), (prevMe.days_between(monthEnd, 'Act/365') -1)
		print monthEnd
		print 'RevisedNom: ', round(revisedNom, 2)
		print 'Nom: ', nom
		oldnom = nom
		nom = round(revisedNom, 2)
		print '--------------------'
		#print dir(monthEnd)
		prevMe = monthEnd
		monthEnd = monthEnd.add_months(1)
		prevMe = monthEnd.first_day_of_month().add_days(-1)
		if (monthEnd > l.end_day) and (monthEnd < (l.end_day).add_months(1)):
		    monthEnd = l.end_day
		print monthEnd, prevMe
		count = count + 1
    if retvalue == 'orgnom':
        print oldnom
	return oldnom
    if retvalue == 'revised':
    	print round(revisedNom, 2)
	return round(revisedNom, 2)
get_RevisedNot(ael.Trade[215016], ael.date_from_string('2004-09-09'), 'revised')
