import ael, string
def change_time(file):
    try:
    	f = open(file)
    except:
    	print 'File not opened'
    trades = []
    line = f.readline()
    line = f.readline()
    
    count = 0
    while line:
    	line = line.rstrip('\n')
	print line
    	trades = string.split(line, '\t')
	try:
	    trades[1]
	    trd = ael.Trade[(int)(trades[1])].clone()
	    trd.time = trd.value_day.to_time()
	    trd.commit()
	    print 'Commit :', trades[1]
	    count = count + 1
	except:
	    print 'Done'
	    break
	try:
	    line = f.readline()
	except:
	    print 'End of file' 
    print 'Total: ', count
change_time('/services/front/scripts/temp/tradetime.csv')
