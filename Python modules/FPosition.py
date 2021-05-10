import acm, ael
    
def Position(i, p, d, *rest):
    ins = acm.FInstrument[i.insaddr]
    port = acm.FPhysicalPortfolio[p.prfnbr]
    forDate = acm.Time().AsDate(d)
    
    criteria = "instrument = '%s' and portfolio = '%s' and acquireDay <= '%s' and status = 'Simulated'" %(ins.Name(), port.Name(), forDate)
    #print criteria
    trades = acm.FTrade.Select(criteria)
    sum = 0
    for trade in trades:
        sum += trade.Quantity()
    return sum
    

'''
i = ael.Instrument['ZAR/CFR']
p = ael.Portfolio['47332']
d = '2009-12-08'

print Position(i, p, d)
'''
