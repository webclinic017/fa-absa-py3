import ael

ins = ael.Instrument.select('instype = "Option"')
for i in ins:
    if (i.exp_day >= ael.date_today()) and (i.insid.startswith('ZAR/FUT/ALSI', 0) == 1):
    	if i.exercise_type != 'European':
#	    print i.insid, i.exercise_type
    	    ins_clone = i.clone()
	    ins_clone.exercise_type = 'European'
	    try:
	    	ins_clone.commit()
    	    	print(ins_clone.insid, 'exercise type changed to ', ins_clone.exercise_type)
	    except:
	    	print('Error committing instrument ', i.insid)
		
		
	    

