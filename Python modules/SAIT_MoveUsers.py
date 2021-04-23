

import ael, string


def move_users(temp, *rest):

    filename = 'f:\\PCG_Users.csv'
    print filename

    count = 0
    fail_list = []

    try:
    	f = open(filename)
    except:
    	print 'Could not open file'
	return

    
    line = f.readline()
    while line:
    	l = string.split(line, ',')
    	try:
            u_clone = ael.User[l[1]].clone()
            u_clone.grpnbr = (int)(l[3])
            try:
                u_clone.commit()
                count = count + 1
            except:
                fail_list.append(u_clone.userid)
        except:
            pass
            
	line = f.readline()  
    
    f.close()
            
    print 'Users committed : ', count
    print 'Users not committed : ', fail_list
    return 'Success'
    
    
# main
move_users(1)
