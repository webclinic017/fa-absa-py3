import ael

def lastCFEndDay(temp,trdnbr,*rest):
    endDay = ael.date('1970-01-01')
    t = ael.Trade[trdnbr]
    
    for cf in t.insaddr.legs()[0].cash_flows():
        if cf.type in ('Call Fixed Rate Adjustable', 'Fixed Rate Adjustable') and endDay < cf.end_day:
            endDay = cf.end_day
    
    return endDay

def updateLastInterest(temp,cfwnbr,date,*rest):
    cf = ael.CashFlow[cfwnbr]
    c = cf.clone()
    c.pay_day = ael.date(date).add_days(-1)
    try:
        c.commit()
        
        ael.poll()
        
        cf = ael.CashFlow[cfwnbr]
        c = cf.clone()
        c.pay_day = ael.date(date)
        c.commit()
        return 'Done'
    except:
        return 'Error'


