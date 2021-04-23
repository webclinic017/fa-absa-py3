import ael


def file_upload(temp):

    filename = '/apps/services/front/QUERIES/GEN/AEL/temp/SC1.txt'

    count = 0
    prev_trdnbr = 0
    fail_list = []

    try:
    	f = open(filename)
    except:
    	print('Could not open file')
	return

    line = f.readline()    	
    line = f.readline()
    while line:
        list = line.strip().split('\t')    
        #print list
        t = ael.Trade[int(list[0])].clone()
        new_ai = ael.AdditionalInfo.new(t)
        #print new_ai.recaddr
        if list[2] in (601, 602):
            new_ai.value = float(list[1])
        else:
            new_ai.value = list[1]
        new_ai.addinf_specnbr = int(list[2])
        try:
            new_ai.commit()
            count = count + 1
            #print new_ai.pp()
        except:
            print('error commiting')
            fail_list.append(list[3])
            
        #ael.poll()
        #print new_ai.pp()
        
        line = f.readline()
        
    f.close()

    print('AIs committed : ', count)
    print('AIs not committed : ', fail_list)





file_upload(1)
