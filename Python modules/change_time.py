import ael, string
def change_time(file):
    try:
    	f = open(file)
    except:
    	print 'File not opened'
    trades = []
    line = f.readline()
    line = f.readline()
    print line.rstrip('\n')
    count = 1
    while line:
    	line = line.rstrip('\n')
    	trades = string.split(line, ',')
	try:
	    trades[1]
	    trd = ael.Trade[(int)(trades[1])].clone()
	    trd.time = trd.value_day.to_time()
	    trd.commit()
	    count = count + 1
	except:
	    print 'Done'
	    break
	try:
	    line = f.readline()
	except:
	    print 'End of file' 
    print 'Total: ', count
change_time('C:\\tradetime.csv')	
