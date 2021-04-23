import ael, acm, string

def Trade_Ref_Upload(temp,*rest):
    
    print 'Loading..'
    file = 'Y:/JHB/PCG/Line/Credit Derivatives/Transref.csv'
    try:
        f = open(file)
    except:
        func=acm.GetFunction('msgBox', 3)
        func("Warning", "Could Not Open File", 0)
        return 'Upload Not Successful'
        
    line = f.readline()
    line = f.readline()
    line = f.readline()
        
    while line:
    
        lin = string.split(line, ',')
        trd = (int)(lin[8])
        trade = ael.Trade[trd]
        TransRef = (int)(lin[len(lin)-1])
        t = trade.clone()
        t.trx_trdnbr = TransRef
        t.commit()
        line = f.readline()
    
    f.close()
    
    func=acm.GetFunction('msgBox', 3)
    func("Warning", "Upload Complete", 0)
    
    print 'Done...'
    return 'Upload Success'
    
#Trade_Ref_Upload(1)
