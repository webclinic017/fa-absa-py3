import ael
try:
    f = open('C:\\t.txt', 'w')
except:
    print 'Could not open'
u = ael.Instrument['ZAR/ALSID']
new = ael.Instrument['ZAR/ALSID_TEST1']
print u, new
ins = ael.Instrument.select('und_insaddr = %d' %(u.insaddr))
for i in ins:
    if i.exp_day >= ael.date_today():
        f.write(i.insid)
        f.write('\n')
        ic = i.clone()
        ic.und_insaddr = new
        ic.commit()
f.close()
