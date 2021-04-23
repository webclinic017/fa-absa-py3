import ael, AccruedInterest2, ResetDates



def accrued_int(t,d,*rest):
   
    legs = t.insaddr.legs()
    for l in legs:
        if l.type == 'Float':
            for cf in l.cash_flows():
                if cf.years_remaining() > 0:
                    for r in cf.resets():
                        if r.value != 0:
                            days = cf.start_day.days_between(cf.end_day)
                            AccrDays = ael.date(d).days_between(cf.pay_day)
                            fd = cf.pay_day
                   #         print cf.pay_day,l.type,cf.projected_cf()*t.quantity * AccrDays/days
                            fl  = cf.projected_cf()*t.quantity * AccrDays/days
    for l in legs:
        if l.type == 'Fixed': 
            for cf in l.cash_flows():
                if cf.years_remaining() > 0  and fd == cf.pay_day :
                        days = cf.start_day.days_between(cf.end_day)
                        AccrDays = ael.date(d).days_between(cf.pay_day)
                  #      print cf.pay_day,l.type,cf.projected_cf()*t.quantity * AccrDays/days
                        fx = cf.projected_cf()*t.quantity * AccrDays/days
    return  fx + fl


#def ael_main():

#t = ael.Trade[948410]
#d = ael.date('2007-09-28')
#print Accrued_int(t , d)

