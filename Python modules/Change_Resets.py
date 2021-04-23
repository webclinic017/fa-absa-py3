   
import ael, string



def Update_Resets(temp, filename, *rest):
    
    #filename = 'c:\\Sifiso.csv'
    #   filename = 'c:\Cashflow_TakeOn_Correction.csv'  
    #print filename
    
    count = 0
    
    try:
        f = open(filename)
    except:
        return 'Could not open file'
    
    
    line = f.readline()    	
    line = f.readline()
    while line:
        l = string.split(line, ',')
        c = ael.CashFlow[(int)(l[0])]
        for r in c.resets():
            rc = r.clone()
            rc.start_day = ael.date_from_string(l[1])
            rc.end_day = ael.date_from_string(l[1])
            rc.day = ael.date_from_string(l[1])
            try:
                rc.commit()
            except:
                print 'Could not commit cf ', l[0]
            
        line = f.readline()
        
    return 'Success'
    
