import acm, ael

t1 = acm.FTrade[14721502]
t2 = acm.FTrade[14721503]

query = r'''
select t.trdnbr from trade t where
aggregate_trdnbr in (14721502, 14721503)
'''

res = ael.dbsql(query)[0]

for trdnbr, in res:
    trade = acm.FTrade[trdnbr]
    trade.AggregateTrade(None)
    trade.Status('Void')
    trade.Commit()
    

t1.Aggregate(0)
t1.Type('Normal')
t1.Commit()

t2.Aggregate(0)
t2.Type('Normal')
t2.Commit()

for p in t1.Payments():
    p.Delete()

for p in t2.Payments():
    p.Delete()
