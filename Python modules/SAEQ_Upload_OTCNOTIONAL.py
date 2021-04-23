import ael, string, SAGEN_Functions
def upload_addinfo(filename, addinfo):
    try:
    	f = open(filename)
    except:
    	print 'Could not open the file'
    line = f.readline()
    line = f.readline()
    while line:
    	l = []
	line = line.rstrip()
	print line
	l = string.split(line, ',')
	trad = ael.Trade[(int)(l[0])]
	notional = l[1]
    	print trad.trdnbr, '****NOT****', notional
	SAGEN_Functions.set_trade_addinf(trad, addinfo, notional)
	line = f.readline()
	
    f.close()		
upload_addinfo('C:\\OTC_Notvalues.csv', 'Notional Amount')
