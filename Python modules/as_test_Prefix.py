import ael, string


def add_prefix(temp, file, *rest):

    try:
        f = open(file)
    except:
        print 'Could not open file'
        return
        
    c_list = []
    v_list = []
    c_count = 0
    v_count = 0
    line = f.readline()
    line = f.readline()
    
    while line:
        l = string.split(line, ',')
        try:
            Vola = ael.Volatility[l[2]]
        except:
            print 'NO VOL'
            return 'NO VOL'
        v = Vola.clone()
        try:
            v.vol_name = l[0]
        except:
            print 'NO'
        
        try:
            v.commit()
            print v.vol_name
            v_count = v_count + 1
        except:
            v_list.append(l[2].rstrip())
            
            #print Curve, Vola
    
    
        line = f.readline()
        
    f.close()
    
    print c_count, ' curves commited.   Curves not committed : ', c_list
    print v_count, ' vols commited.    Vols not committed : ', v_list
    
    
    return 'S'


ael_variables = [('filename', 'File Location', 'string',)]

def ael_main(dict):
    filenm = dict["filename"] 
    print add_prefix(1, filenm)
