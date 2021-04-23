import ael

trades = ael.TradeFilter['jpCall_All_Trades EQ'].trades()

for t in trades:

    ins = t.insaddr
    
    for l in ins.legs():
        maxdate = l.start_day
        for c in l.cash_flows():
            if c.pay_day > maxdate and c.type == 'Call Float Rate':
                maxdate = c.pay_day
    print maxdate
    while maxdate <= ael.date_today():
        
        ins.extend_open_end()
        maxdate = maxdate.add_banking_day(ael.Instrument['ZAR'], 1)
        ael.poll()
