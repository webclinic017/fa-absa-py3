import ael
trds = ael.TradeFilter['SAEQ_0d_Stocks'].trades()
for t in trds:
    if t.status == 'FO Confirmed':
        print(t.trdnbr, t.status)
        tc = t.clone()
        tc.status = 'BO Confirmed'
        print(tc.status)
        tc.commit()
