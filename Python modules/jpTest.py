import ael

def jpChangeCloseOutStockPort(t,MappingDir,*rest):
    
    MappingDic={}
    
    MappingDirectory = MappingDir
    
    try:
    
        Md = open(MappingDirectory)
        
        line = Md.readline()
        
        while line:
        
            line = Md.readline()
            l = line.split(',')
            if l[0] == '\n' or l[0] == "":break
            
            list=[]
            
            for i in l: 
                reg = i.lstrip()
                reg = reg.rstrip()
                list.append(reg)
            
            MappingDic[list[0]] = list[1]
            
        if MappingDic.has_key(t.prfnbr.prfid):
    
            newPortNumber = ael.Portfolio[MappingDic[t.prfnbr.prfid]]
            
            new = t.clone()
            new.prfnbr = newPortNumber
            
            try:
                new.commit()
                return 'Success'
            except:
                print 'Can not commit trade', t.trdnbr
        
        else:
        
            print 'Mapping file does not contain a mapping for:', t.prfnbr.prfid            
    except:
    
        print 'Problem opening the Mapping File:%s.Remember that the file must be a csv file.'%(MappingDirectory)
    
    return 'Success'
    
    
