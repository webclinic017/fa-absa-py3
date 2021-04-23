import ael, string

try: infile = open('c:\\OrderNum.csv', 'r')
except:
    print 'Outfile c:\OrderNum.csv not found'
    ael.log('The file does not exist in the specified directory')


line = infile.readline()
while line:
    devno, ordnum = string.split(line, ',')
    try:
    	t = ael.Trade.read('optional_key=%s'%devno)
	newtrd = t.clone()
    	#if newtrd.your_ref == '':
    	print newtrd.trdnbr, newtrd.your_ref
	newtrd.your_ref = ordnum
	#newtrd.commit()
	print newtrd.trdnbr, newtrd.your_ref
	#else:
	 #   print 'Has ', newtrd.trdnbr
    except:
    	print 'Does not Exist'
    
    
    line = infile.readline()
    
infile.close()
