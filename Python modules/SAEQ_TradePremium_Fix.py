import ael
try:
    f = open('C:\\Equit\\Satrixtrade.csv')
except:
    print 'File not opened'
line = (f.readline()).strip()
while line != '':
    line = (f.readline()).strip()
    trdn = (int)(line)
    print trdn
    tr = ael.Trade[trdn]
    trc = tr.clone()
    try:
    	trc.premium = trc.premium_from_quote(ael.date_today(), trc.price)
    	trc.commit()
    except:
    	print 'Could not commit: ', trc.trdnbr 
print 'done'

