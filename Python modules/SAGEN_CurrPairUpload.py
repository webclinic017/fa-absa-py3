import ael, string
def upload_curr(infile):
    try:
    	f = open(infile)
    except:
    	print 'Unable to open inputfile'
    line = f.readline()
    line = f.readline()
    while line:
    	l = []
	l = string.split(line, ',')
	currpair = ael.CurrencyPair.new()
	currpair.name = l[9]
	currpair.curr1 = (int)(l[10])
	currpair.curr2 = (int)(l[11])
	#currpair.point_value = (float)(l[12])
	#currpair.spot_banking_days_offset = (int)(l[17])
    	print currpair.pp()
    	try:
	    currpair.commit()
	except:
	    print 'error'
	line = f.readline()
upload_curr('C:\\currpair\\CurrPairP.csv')
