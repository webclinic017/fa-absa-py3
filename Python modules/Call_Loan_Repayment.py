import ael

def reinvest(temp,trade,insid,start,end,*rest):
    t = ael.Trade[trade]
    ins = ael.Instrument[insid]
    d1 = ael.date(start)
    d2 = ael.date(end)
    reinvest = 0
    for cf in ins.cash_flows():
        if cf.type == 'Interest Reinvestment' and cf.pay_day >= d1 and cf.pay_day <= d2:
            reinvest = reinvest + (cf.projected_cf()* t.quantity)
    return reinvest

def repayment(temp,trade,insid,start,end,*rest):
    t = ael.Trade[trade]
    ins = ael.Instrument[insid]
    d1 = ael.date(start)
    d2 = ael.date(end)
    repayment = 0
    for cf in ins.cash_flows():
        if cf.type == 'Fixed Amount' and cf.add_info('Settle_Type') == 'Interest Repayment' and cf.pay_day >= d1 and cf.pay_day <= d2:
            repayment = repayment + (cf.projected_cf()* t.quantity)
    return repayment
