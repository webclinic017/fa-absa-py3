import ael

def change(temp,trdnbr,*rest):
    t = ael.Trade[trdnbr]
    i = t.insaddr
    l = i.legs()[0]
    cashflow = []
    
    for c in l.cash_flows():
        if c.type == 'Call Fixed Rate Adjustable' and c.pay_day == ael.date('2008-07-01'):
            cashflow.append(c.cfwnbr)
            cf = c.clone()
            cf.pay_day = ael.date('2008-06-30')
            cf.commit()
            
    ael.poll()
    
    
    for c in cashflow:
        cf = ael.CashFlow[c].clone()
        cf.pay_day = ael.date('2008-07-01')
        cf.commit()
    
    return 'Done'
