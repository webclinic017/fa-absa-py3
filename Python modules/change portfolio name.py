import acm

changePort = acm.FPhysicalPortfolio['MIDAS_FLD']

trds = acm.FPhysicalPortfolio['FX YieldX'].Trades()

ml=[]

for t in trds:
    if t.Instrument().InsType()=='Curr' and t.Counterparty().Name()=='MIDAS DUAL KEY':
        
        ml.append(t.Oid())


mt = tuple(ml)

print len(mt)

for trd in mt:
    t = acm.FTrade[trd]
    print t.Oid(), t.Instrument().InsType(), 'existing portfolio = ',  t.Portfolio().Name(), 'CP = ', t.Counterparty().Name()
    
    
    t.Portfolio = changePort
    
    t.Commit()
    print t.Oid(), t.Instrument().InsType(), 'new portfolio = ',  t.Portfolio().Name(), 'CP = ', t.Counterparty().Name()
    
