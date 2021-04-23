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
        Curve = ael.YieldCurve[l[0]]
        Vola = ael.Volatility[l[1].rstrip()]
        '''
        if Curve != None:
            c = Curve.clone()
            c.yield_curve_name = 'TBR_' + c.yield_curve_name
            try:
                c.commit()      
                c_count = c_count + 1
            except:
                c_list.append(l[0])
        else:
            c_list.append(l[0])
            
        '''
        if Vola != None:
            v = Vola.clone()
            try:
                v.vol_name = 'TBR_' + v.vol_name
            except:
                print v.vol_name + ' NOT COMMITED, name too long?'
            try:
                v.commit()
                print v.vol_name
                v_count = v_count + 1
            except:
                v_list.append(l[1].rstrip())
        else:
            v_list.append(l[1].rstrip())
        
        #print Curve, Vola
        
        line = f.readline()
        
    f.close()
    
    print c_count, ' curves commited.   Curves not committed : ', c_list
    print v_count, ' vols commited.    Vols not committed : ', v_list
    
    
    return 'Success'




ael_variables = [('filename', 'File Location', 'string',)]

def ael_main(dict):
    filenm = dict["filename"] 
    print '....Start....'
    add_prefix(1, filenm)
    print '....End....'
