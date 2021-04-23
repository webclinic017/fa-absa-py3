import ael
try:
    f = open('C:\\f.txt', 'w')
except:
    print 'could not open file'
p = ael.Portfolio['47274_CFD_ZERO']
for t in p.trades():
    tc = t.clone()
    v = t.fee
    f.write((str)(tc.trdnbr) + ',' + (str)(t.fee) + '\n')
    #print tc.fee
    tc.acquire_day = ael.date_from_time(tc.time)
    tc.value_day = ael.date_from_time(tc.time)
    tc.commit()
f.close()
