
import ael, string


def delete_asql(temp, *rest):

    filename = 'f:\\ToBeRemoved.csv'
    #filename = 'f:\\test.csv'
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
            q_del = ael.TextObject[seq]
            try:
                q_del.delete()
                count = count + 1
            except:
                fail_list.append(q_del.name)
            

    print 'Queries deleted : ', count
    print 'Queries not deleted : ', fail_list
    return 'Success'
    
    
    
    
# main
delete_asql(1)
