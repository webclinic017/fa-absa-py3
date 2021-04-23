import acm

newtrades=acm.FSet()  
currencies=acm.FCurrency.Select('')
for currency in currencies:
    for trade in currency.Trades():
        if trade.HedgeTrade():
            hdgtrade=trade.HedgeTrade()
            if not newtrades.Includes(hdgtrade):
                newtrades.Add(hdgtrade)

#print newtrades

updated=acm.FArray()
missedtrades=acm.FArray()
notvoided=acm.FArray()
swaps=acm.FFxSwap.Select('')
ignored=acm.FArray()

for swap in swaps:
    #Excluding trades in generic instruments
    if swap.Generic():
        for trade in swap.Trades():
            ignored.Add(trade)
    else:
        for trade in swap.Trades():
            if trade.Status() not in ('Void', 'Confirmed Void'):
                notvoided.Add(trade)
            elif trade.Text1() == 'Converted to cash trade':
                updated.Add(trade)

#Check that all old trades has a corresponding new trade
for trade in updated:
    if not newtrades.Includes(trade):
        missedtrades.Add(trade)
        
print '---------------Missed Trades---------------'
for t in missedtrades:
    print 'Trade: %i, Instrument: %s' %(t.Oid(), t.Instrument().Name())
print '---------------Not voided---------------'
for t in notvoided:
    print 'Trade: %i, Instrument: %s' %(t.Oid(), t.Instrument().Name())
print '---------------Ignored---------------'
for t in ignored:
    print 'Trade: %i, Instrument: %s' %(t.Oid(), t.Instrument().Name())
