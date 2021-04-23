import ael, string

try: infile = open('c:\\DealNumbers2.csv', 'r')
except:
    print 'Outfile c:\DealNumbers.csv not found'
    ael.log('The file does not exist in the specified directory')


line = infile.readline()
while line:
    trdnbr = (int)(line)
    try:
    	
	print trdnbr
	trade = ael.Trade[trdnbr]
	print trade
	t = trade.clone()
	t.text1 = 'RISK'
	print t.text1
	try:
	    t.commit()
	except:
	    print 'Problem Here'
	
	
    except:
    	print 'Does not Exist'
    
    
    line = infile.readline()
    
infile.close()
