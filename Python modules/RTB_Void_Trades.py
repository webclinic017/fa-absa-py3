    import acm

#Replace the below trade numbers with the ones to be voided
TRADES = [
'9904169999',
'9904168988',
'9904168877',
'9904168766',
]


acm.BeginTransaction()
try:
    for t in TRADES:
        trd = acm.FTrade[t]
        trd.Status('Void')
        trd.Commit()
    acm.CommitTransaction()
except:
    acm.AbortTransaction()
