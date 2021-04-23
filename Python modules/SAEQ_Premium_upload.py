import ael, string
try:
    f = open('C:\\Premiums.csv')
except:
    print 'File not opened'
line = (f.readline()).strip()
line = (f.readline()).strip()
while line != '':
    print
    l = []
    l = string.split(line, ',')
    trdn = (int)(l[0])
    print trdn, l[1]
    tr = ael.Trade[trdn]
    trc = tr.clone()
    trc.premium = (float)(l[1])
#    print trc.trdnbr, tr.premium, trc.premium
    trc.commit()
    line = (f.readline()).strip()
f.close()
print 'done'
