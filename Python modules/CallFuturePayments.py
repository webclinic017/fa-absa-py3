import ael

def futPayment(temp,i,repDay,*rest):
    date = ael.date(repDay)
    subBal = 0
    i = ael.Instrument[i]
    quantity = i.trades()[0].quantity
    if i.legs().members() != []:
        l = i.legs()[0]
        if date < l.end_day:
            for c in l.cash_flows():
                if c.type in ('Fixed Amount', 'Interest Reinvestment'):
                    if c.pay_day > date and c.pay_day <= l.end_day:
                        if c.start_day and c.start_day < date:
                            subBal = subBal + 0
                        else:
                            subBal = subBal + c.projected_cf()
    return quantity * subBal

#print futPayment(1,'464502-ZAR-2203-01','2009-02-28')
