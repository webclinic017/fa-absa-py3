import ael, acm, csv

def Not_Trading_Untick():
        
    PartyList = []
    Parties   = []
    
    errors = []

    for t in ael.Portfolio['JOB6'].trades():
    
        if t.counterparty_ptynbr not in Parties:
            Parties.append(t.counterparty_ptynbr)
    for t in Parties:
        if t.not_trading == 1:
                        
            if t.fullname not in PartyList:
                PartyList.append(t.fullname)
            t_c = t.clone()
            try:
                t_c.not_trading = 0
                t_c.commit()
            except:
                errors.append(t)
                
    if len(errors) != 0:
        func=acm.GetFunction('msgBox', 3)
        func("FAIL", "Commit Failed", 0)
           
    Party_list(PartyList)    
            
def Party_list(List):            

    FileName  = '/apps/frontnt/REPORTS/BackOffice/Atlas-End-Of-Day/Not_Trading_Counterparty.txt'
    for party in List:
        
        try:
            outfile = open(FileName, 'a')
            outfile.write(party + '\n')
            outfile.close()           
        except:
            func=acm.GetFunction('msgBox', 3)
            func("FAIL", "File could not open", 0)
            
Not_Trading_Untick()    
   
  
