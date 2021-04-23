import ael
    
def MoveTradePortfolio(temp,Stat,NewPortfolio,TrdFilter,MoveDate,*rest):
    
    GlobalStat=[]
    GlobalFail=[]
    counts = 0
    
    
    Newportnumber = ael.Portfolio[(str)(NewPortfolio)].prfnbr

    try:
    	sdate = ael.date_from_string(MoveDate)
    except:
	sdate = MoveDate
    
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
            
            trades_updated.append(t.trdnbr)
            trades_updated.append(t.status)
            trades_updated.append(t.prfnbr.prfid)
            
            try:
                new.commit()
                
            except:
                fail=[]
                print t.trdnbr
                fail.append(t.trdnbr)
                counts = counts + 1
                GlobalFail.append(fail)
            ael.poll()
            
            trades_updated.append(t.prfnbr.prfid)
            GlobalStat.append(trades_updated)
            
      
    GlobalFail.sort()    
    GlobalStat.sort()
    outfile1 = 'C:\\PortfolioMove' + Stat + '.csv'
    
    report = open(outfile1, 'w')
    Headers=[]
    
    Headers = ['Trdnbr', 'Status', 'OldPortfolio', 'NewPortfolio']
    #print 'Counts', counts
    
    for i in Headers:
        
        report.write((str)(i))
        report.write(',')
    report.write('\n')
        
    
    for lsts in GlobalStat:
        
        for ls in lsts:
            
            report.write((str)(ls))
            report.write(',')
        report.write('\n')
    
    report.close()
    
    
            
    print 'The file has been saved at' + 'C:\\PortfolioMove' + Stat + '.csv'
#
    outfile2 = 'C:\\PortfolioFailed' + Stat + '.csv'
    
    report2 = open(outfile2, 'w')
    Headers=[]
    
    Headers = ['Trdnbr', 'Status', 'OldPortfolio', 'NewPortfolio']
    print 'Counts', counts
    
    for i in Headers:
        
        report2.write((str)(i))
        report2.write(',')
    report2.write('\n')
        
    
    for lsts in GlobalFail:
        
        for ls in lsts:
            
            report2.write((str)(ls))
            report2.write(',')
        report2.write('\n')
    
    report2.close()
    
    
            
    print 'The file has been saved at' + 'C:\\PortfolioFailed' + Stat + '.csv'
    print GlobalFail
#    
def NewPortfolio():

    NewPortfolio=[]
    
    for p in ael.Portfolio:
        NewPortfolio.append(p.prfid)
    NewPortfolio.sort()
    return NewPortfolio
    
def TrdFilter():

    TrdFilter=[]
    
    for t in ael.TradeFilter:
        TrdFilter.append(t.fltid)
    TrdFilter.sort()
    return TrdFilter

ael_variables = [('Stat', 'Status', 'string', None, 'Simulated', 1),
                 ('NewPortfolio', 'NewPortfolio', 'string', NewPortfolio(), '', 1),
                 ('TrdFilter', 'TrdFilter', 'string', TrdFilter(), '', 1),  
                 ('MoveDate', 'MoveDate', 'date', None, ael.date_today(), 1)]   

def ael_main(ael_dict):

    Stat = ael_dict["Stat"]
    NewPortfolio = ael_dict["NewPortfolio"]
    TrdFilter = ael_dict["TrdFilter"] 
    MoveDate = ael_dict["MoveDate"]
    
    print MoveTradePortfolio(1, Stat, NewPortfolio, TrdFilter, MoveDate)
