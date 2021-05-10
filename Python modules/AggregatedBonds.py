import ael

trds = ael.TradeFilter['AggregatedBonds'].trades()

for t in trds:
 new_t = t.clone()
 new_t.status = "BO Confirmed"
 new_t.commit()
