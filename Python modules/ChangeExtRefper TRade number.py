import ael
try:
    f = open('C:\\MetalsDevNo.csv')
except:
    print 'Error opening file'

line = f.readline()
line = f.readline()
while line != '':
    line = line.rstrip('\n')
    trd, ref = line.split(',')
    ref = 'DEVON' + ref 
    print 'Trade: ', trd, 'REF: ', ref  
    trade = ael.Trade[(int)(trd)].clone()
    print trade.trdnbr, trade.optional_key
    trade.optional_key = ref
    try:
    	trade.commit()
    except:
    	mes = 'Error ' + trd + ref
	ael.log(mes)
    print trade.trdnbr, trade.optional_key
    try:
    	line = f.readline()
    except:
    	print 'End of file'
f.close()
