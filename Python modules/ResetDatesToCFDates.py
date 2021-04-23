'''ResetDatesToCFDates: last updated on Fri May 07 15:07:27 2004. Extracted by Stowaway on 2004-05-07.'''
import ael


def ResetDatesToCFDates():

    file = open('c:\\oldvalues.csv', 'w')
    res = ael.Reset.select()
    for r in res:
    	if r.type == 'Single'  and r.cfwnbr.end_day >= ael.date_today():
	    if r.start_day != r.cfwnbr.start_day or r.end_day != r.cfwnbr.end_day:
		file.write(str(r.resnbr) + ',' + str(r.start_day) + ',' + str(r.end_day) + ',' + str(r.value) + '\n')
		rc = r.clone()
		if r.start_day != r.cfwnbr.start_day: rc.start_day = r.cfwnbr.start_day
		if r.end_day != r.cfwnbr.end_day: rc.end_day = r.cfwnbr.end_day
		rc.commit()
	
    file.close()
    print 'done'
	
ResetDatesToCFDates()
