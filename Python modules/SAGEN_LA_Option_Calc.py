import ael

def calc_HPayment(temp,t,date,baseCurr,*rest):
    hpayment = 0
    t = ael.Trade[t]
    if t.payments():
        for p in t.payments():
            if date < p.payday:
                hpayment = hpayment + p.amount*p.curr.used_price(ael.date(date), baseCurr)
    return hpayment

def calc_HPremium(temp, t, date, baseCurr, *rest):
    t = ael.Trade[t]
    hprem = t.premium * t.curr.used_price(ael.date(date), baseCurr)
    return hprem
