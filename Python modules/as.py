import ael, AccruedInterest2, ResetDates

t = ael.Trade[630591]
d = ael.date('2007-09-28')
det = 'Accrued'
r = 'Fixed'
fx1 =  AccruedInterest2.accrued_interest(t, d, 'Fixed', det) 
fl1 = AccruedInterest2.accrued_interest(t, d, 'Float', det)
d2 = ael.date('2007-10-31')
fx2 =  AccruedInterest2.accrued_interest(t, d1, 'Fixed', det) 
fl2 =  AccruedInterest2.accrued_interest(t, d1, 'Float', det)
int = t.interest_accrued(d, d1)
#print fx1-fx2 + fl1-fl2 ,int 

legs = t.insaddr.legs()
for l in legs:
    if l.type == 'Float':
        for cf in l.cash_flows():
            if cf.years_remaining() > 0:
                for r in cf.resets():
                    if r.value != 0:
                        days = cf.start_day.days_between(cf.end_day)
                        AccrDays = d.days_between(cf.pay_day)
                        fd = cf.pay_day
                        print cf.pay_day, l.type, cf.projected_cf()*t.quantity * AccrDays/days
                        #print cf.type , cf.rate , cf.years_remaining() , cf.pay_day , r.value
for l in legs:
    if l.type == 'Fixed': 
        for cf in l.cash_flows():
            if cf.years_remaining() > 0  and fd == cf.pay_day :
            
                    days = cf.start_day.days_between(cf.end_day)
                    AccrDays = d.days_between(cf.pay_day)
                    print cf.pay_day, l.type, cf.projected_cf()*t.quantity * AccrDays/days
        

