import ael
trades = ael.Portfolio['Agri ABL3 Options OTC'].trades()
list = []
for t in trades:
    ins = t.insaddr
    if ins.insaddr not in list:
    	list.append(ins.insaddr)
	if ins.instype == 'Option' and ins.exp_day >= ael.date_today():
	    print(ins.insid, ins.exercise_type)
	    insclone = ins.clone()
	    insclone.exercise_type = 'European'
    	    insclone.commit()
