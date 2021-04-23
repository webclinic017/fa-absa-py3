import ael, string


#Upload file variable must be in this format "C:\\FDI.csv"

ael_variables = [('file', 'Upload File', 'string', None, None, 0)]


def ael_main(ael_dict):

    filename = ael_dict["file"]
#    print filename

    count = 0
    fail_list = []
    if filename != None:
    	try:
    	    f = open(filename)
    	except:
            print 'Could not open file'
	    return
	    
    	try:
	    outfile = open('c:\\cp_ref.txt', 'w')
    	except:
    	    print 'Cannot open output file'
    	
	line = f.readline()
    	while line != 'AAA':
	    l = string.split(line, ',')
    	    
	    nbr = l[0]
	    nbr2 = string.strip(nbr)
	    t = ael.Trade[(int)(nbr)]
	    t_clone = t.clone()
	    t_clone.your_ref = string.strip(l[1])
	    
	    try:
	    	t_clone.commit()
		out = '%s CP Ref changed from %s to %s\n' %(nbr2, t.your_ref, t_clone.your_ref )				
		print out
		count = count + 1
	    except:
	    	print 'Error commiting trade ', t.trdnbr
		fail_list.append(t.trdnbr)
   
	    outfile.write(out)
	    line = f.readline()
    	f.close()
	outfile.close()
	

    print
    print 'Trades committed : ', count
    print 'Trades not committed : ', fail_list

	    
   
