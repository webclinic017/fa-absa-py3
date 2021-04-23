import ael

def Filter():

    Filter=[]
    
    for t in ael.TradeFilter:
        Filter.append(t.fltid)
    Filter.sort()
    return Filter
    
def NewPortfolio():

    NewPortfolio=[]
    
    for p in ael.Portfolio:
        NewPortfolio.append(p.prfid)
    NewPortfolio.sort()
    return NewPortfolio
    
ael_variables = [('Filter', 'Filter', 'string', Filter(), '', 1),
                ('NewPortfolio', 'NewPortfolio', 'string', NewPortfolio(), '', 1)]

def ael_main(ael_dict):

    Filter = ael_dict["Filter"]
    NewPortfolio = ael_dict["NewPortfolio"] 
    
    jpCloseBookTrades(Filter, NewPortfolio)
    
def jpCloseBookTrades(Filter, NewPortfolio):

    newPortNumber = ael.Portfolio[NewPortfolio].prfnbr
    
    trds = ael.TradeFilter[Filter].trades()
    
    for t in trds.members():    
               
        if t.quantity != 0:
        
            newPos = ael.Trade[t.trdnbr].new()        
            newPos.prfnbr = newPortNumber
            newPos.optional_key = ''
            
            newOpposite = ael.Trade[t.trdnbr].new()
            newOpposite.quantity = t.quantity * -1
            newOpposite.premium = t.premium * -1
            newOpposite.optional_key = ''
            
            try:
                newOpposite.commit()
                try:
                    newPos.commit()
                except:
                    print '%i failed to create the trade in the new portfolio %s' %(t.trdnbr, NewPortfolio)
            except:
                print '%i failed to create the opposite trade in the portfolio %s' %(t.trdnbr, t.prfnbr.prfid)

            
            




