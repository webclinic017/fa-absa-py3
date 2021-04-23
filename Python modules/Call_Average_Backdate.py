import ael

def average_rate(temp,ins, cfwnbr,*rest):
    i = ael.Instrument[ins]
    c = ael.CashFlow[cfwnbr]
    
    start = c.start_day
    fixedAmount = round(c.fixed_amount, 2)
    days = 0
    interest = 0
    foundCF = 0
    
    for l in i.legs():
        while not foundCF:
            flag = 0
            for cf in l.cash_flows():
                if cf.type == 'Fixed Rate Adjustable':
                    if (fixedAmount - (-1*round(cf.nominal_factor, 2))) == 0.00:
                        if start == cf.start_day:
                            days = days + cf.start_day.days_between(cf.end_day)
                            interest = interest + cf.projected_cf()
                            start = cf.end_day
                            flag = 1
            if not flag:
                foundCF = 1
    
    rate = (interest*36500)/(days*fixedAmount)
    return rate

#print average_rate(1,'332077-ZAR-2203-01',3221774)
