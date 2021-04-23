
import ael, string


def rename_asql(temp, *rest):

    filename = 'f:\unused.csv'
    print filename

    count = 0
    fail_list = []

    try:
    	f = open(filename)
    except:
    	print 'Could not open file'
	return

    q_list = []
    line = f.readline()
    while line:
    	l = string.split(line, ',')
    	q_list.append(l[0].strip())
	line = f.readline()  
    
    f.close()
    db_ASQL = {}
    
    for x in ael.TextObject.select('type = "SQL Query"'):
        db_ASQL[x.name] = x.seqnbr
           
     
    for q in q_list:
        if db_ASQL.has_key(q):
            seq = db_ASQL[q]
            q_clone = ael.TextObject[seq].clone()
            if len(q_clone.name) >= 28:
                temp = q_clone.name[0:-2]
                q_clone.name = 'X_' + temp
            else:
                q_clone.name = 'TBR_' + q_clone.name
            #print q, ';', q_clone.name
            
            try:
                q_clone.commit()
                count = count + 1
            except:
                fail_list.append(q_clone.name)
            
                
                

    print 'Queries committed : ', count
    print 'Queries not committed : ', fail_list
    return 'Success'
    
    
    
    
# main
rename_asql(1)
