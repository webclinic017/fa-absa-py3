import ael, string
try:
    f = open('C:\\FenicsParty.csv')
except:
    print('Error opening file')

line = f.readline()
line = f.readline()
while line != '':
    l = []
    line = line.rstrip('\n')
    l = line.split(',')
    trade = ael.Trade[(int)(l[0])].clone()
    pty = ael.Party[l[2]]
    trade.counterparty_ptynbr = pty
    try:
    	trade.commit()
    except:
    	mes = 'Error ' + trd + ref
	ael.log(mes)
    print(trade.trdnbr, trade.optional_key)
    try:
    	line = f.readline()
    except:
    	print('End of file')
f.close()
