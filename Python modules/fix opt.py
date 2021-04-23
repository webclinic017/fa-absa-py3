import ael
name = "und_insaddr.insid = 'ZAR/ALSI/SEP05'" 
print(name)
opt = ael.Instrument.select(name)
for t in opt:
    if t.exercise_type == 'American' and t.contr_size != 10:
    	print(t.insid)
    	print(t.contr_size)
