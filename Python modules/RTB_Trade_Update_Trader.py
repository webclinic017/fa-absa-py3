import acm

tradeSet = [55700595, 55700935]


for t in tradeSet:
    trd = acm.FTrade[t]
    trd.Trader('STRAUSD')
    print 'Updating Trader on', trd.Oid(), 'from', trd.Trader().Name() 
    trd.Commit()
    print 'Trader on', trd.Oid(), 'Updated to', trd.Trader().Name() 
