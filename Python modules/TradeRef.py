import ael, string

def Trade_Ref(temp,*rest):
    
    file = 'C:/Documents and Settings/abhc164/My Documents/Dumi/Portfolio Reference/Book3.csv'
    filename = open(file)
    line = filename.readline()
    #line = filename.readline()
    #line = filename.readline()
    #line = filename.readline()
    
    while line:
        lin = string.split(line, ',')
        trd1 = (int)(lin[1])
        trade1 = ael.Trade[trd1]
        t1 = trade1.clone()
        t1.trx_trdnbr = (int)(lin[0])
        t1.commit()
        
        #trd2 = (int)(lin[4])
        #trade2 = ael.Trade[trd2]
        #t2 = trade2.clone()
        #t2.trx_trdnbr = (int)(lin[0])
        #t2.commit()

        #trd3 = (int)(lin[8])
        #trade3 = ael.Trade[trd3]
        #t3 = trade3.clone()
        #t3.trx_trdnbr = (int)(lin[0])
        #3.commit()

        #trd4 = (int)(lin[12])
        #trade4 = ael.Trade[trd4]
        #4 = trade4.clone()
        #4.trx_trdnbr = (int)(lin[0])
        #t4.commit()

        #trd5 = (int)(lin[16])
        #trade5 = ael.Trade[trd5]
        #t5 = trade5.clone()
        #t5.trx_trdnbr = (int)(lin[0])
        #t5.commit()

        line = filename.readline()
    
    filename.close()
    print 'Done'
    return 'Done'

