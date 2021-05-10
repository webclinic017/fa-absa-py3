import ael
ins = ael.Instrument['ZAR/ALSI/DEC04']
opt = ael.Instrument.select('und_insaddr = %d' %(ins.insaddr))
for o in opt:
    if ins.exp_day != o.exp_day:
    	oclone = o.clone()
	oclone.exp_day = ins.exp_day
    	oclone.commit()
