import ael
    
def MoveTradePortfolio(temp,Stat,NewPortfolio,TrdFilter,MoveDate,*rest):
    
    Newportnumber = ael.Portfolio[(str)(NewPortfolio)].prfnbr
    MoveDate = ael.date_today()
        
    trds = ael.TradeFilter[(str)(TrdFilter)].trades()
    
    for t in trds.members():
    
        trades_updated=[]
        
        #print t.status
        #print t.trdnbr
        if (str)(Stat) == 'Simulated':
            dat = ael.date_from_time(t.time)
        
        elif (str)(Stat) == 'Void':
            dat = ael.date_from_time(t.updat_time)
            
        else:
            dat = ael.date_from_time(t.updat_time)
            
        if t.status == (str)(Stat) and dat <= MoveDate:
            
            new = t.clone()
            new.prfnbr = Newportnumber
                            
            try:
                new.commit()
                
            except:
                t.trdnbr
                
                
    return 'Success'
            
