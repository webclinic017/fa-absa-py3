import ael, string
 

def file_upload(temp, *rest):

    filename = '/apps/services/front/QUERIES/GEN/AEL/pk_upload_whole.csv'
    #print filename

    count = 0
    fail_list = []

    try:
    	f = open(filename)
    except:
    	print 'Could not open file'
	return

    line = f.readline()    	
    line = f.readline()
    while line:
        l = string.split(line, ',')
        p_clone = ael.Instrument[l[0]].historical_prices()[0].new()
        p_clone.ptynbr = ael.Party[int(l[2])]
        
        p_clone.bid = (float)(l[3])
        p_clone.ask = (float)(l[4])
        p_clone.settle = (float)(l[5])
        p_clone.last = (float)(l[6])
        p_clone.day = ael.date_today().add_days(-1)
        p_clone.curr = ael.Instrument[int(l[8])]
        try:
            p_clone.commit()
            count = count + 1
            #return 'Success'
        except:
            #print 'could not commit ', l[0]
            fail_list.append(l[0])
            #return 'Failed'
            

	line = f.readline()
	
	
    f.close()
    print 'Instruments committed : ', count
    print 'Ins not committed : ', fail_list
    return


    
    
print '\nStart Upload\n'
file_upload(1)
print '\nUpload Complete\n'
        
