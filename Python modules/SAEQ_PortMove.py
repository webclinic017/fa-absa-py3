import ael

def NewPortfolio():

    NewPortfolio=[]
    
    for p in ael.Portfolio:
        NewPortfolio.append(p.prfid)
    NewPortfolio.sort()
    return NewPortfolio
    
def Filter():

    Filter=[]
    
    for t in ael.TradeFilter:
        Filter.append(t.fltid)
    Filter.sort()
    return Filter
    
ael_variables = [('Filter', 'Filter', 'string', Filter(), '', 1), 
                 ('NewPortfolio', 'NewPortfolio', 'string', NewPortfolio(), '', 1),                  
                 ('Server', 'Server', 'string', None, 'C:\\', 1)]   

def ael_main(ael_dict):

    Filter = ael_dict["Filter"] 
    NewPortfolio = ael_dict["NewPortfolio"]    
    Server = ael_dict["Server"]
    
    jpPortfolioMove(Filter, NewPortfolio, Server)


def jpPortfolioMove(tf, Prf, Server):
    
    GlobalUpdated=[]
    GlobalFail=[]
    counter=0
    
    newPortNumber = ael.Portfolio[Prf].prfnbr
    
    trades = ael.TradeFilter[tf].trades()
    
    for t in trades.members():
        
        tradesUpdated=[]
        
        new = t.clone()
        new.prfnbr = newPortNumber
        
        try:
            new.commit()
            tradesUpdated.append(t.trdnbr)
            tradesUpdated.append(t.prfnbr.prfid)
            
            ael.poll()
            
            tradesUpdated.append(t.prfnbr.prfid)
            
        except:
            fail=[]
            fail.append(t.trdnbr)
            fail.append(t.prfnbr.prfid)
            counter += 1
            GlobalFail.append(fail)
            
        GlobalUpdated.append(tradesUpdated)
    
    GlobalFail.sort()
    GlobalUpdated.sort()
    
    outfileUpdated = Server + 'PortMoveUpdated' + ael.date_today().to_string('%Y%m%d') + '.csv'
    reportUpdated = open(outfileUpdated, 'w')  

    for list in GlobalUpdated:
        for element in list:
            
            reportUpdated.write((str)(element))
            reportUpdated.write(',')
        reportUpdated.write('\n')
        
    reportUpdated.close()
    
    print 'The file has been saved at' + Server + 'PortMoveUpdated' + ael.date_today().to_string('%Y%m%d') + '.csv'
    
    outfileFail = Server + 'PortMoveFailed' + ael.date_today().to_string('%Y%m%d') + '.csv'
    reportFail = open(outfileFail, 'w')
    
    for list in GlobalFail:
        for element in list:
            
            reportFail.write((str)(element))
            reportFail.write(',')
        reportFail.write('\n')
    
    print 'The file has been saved at' + Server + 'PortMoveFailed' + ael.date_today().to_string('%Y%m%d') + '.csv'
    reportFail.close()

    return counter



