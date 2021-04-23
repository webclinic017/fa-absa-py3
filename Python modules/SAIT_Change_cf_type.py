import ael, string

def changecfs(temp, type, *rest):

    line = f.readline()    	
    line = f.readline()
    while line:
        l = string.split(line, ',')
        c = ael.CashFlow[(int)(l[0])]
        cc = c.clone()
        cc.type = type
        try:
            cc.commit()
        except:
            print 'cannot commit'
        line = f.readline()         
    
    return 'Success'
        


ael_variables = [('filename', 'File Location', 'string'),
                 ('newtype', 'New Cashflow Type', 'string')]
    
    
def ael_main(dict):

    infile = dict["filename"]
    type = dict["newtype"]
    #infile = 'c:\Sifiso1.csv'
    
    try:
        f = open(infile)
        print changecfs(1, type)        
    except:
        print 'Could not open file'


