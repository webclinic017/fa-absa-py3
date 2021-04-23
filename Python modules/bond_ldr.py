import ael, time, acm

def next_bond_paydte(ins,*rest):
    
    #ins = ael.Instrument[ins]
    
    paydte = []
       
    for l in ins.legs():
        for cf in l.cash_flows():
            if cf.pay_day > ael.date_today():
                if cf.type <> 'Fixed Amount':
                    paydte.append(cf.end_day)
                else:
                    paydte.append(cf.pay_day)
    
    paydte.sort()
    
    next_paydte = paydte[0]
    
    return next_paydte
    

def bond_ldr_date(ins,dte,*rest):
    
    #ins = ael.Instrument[ins]
    paydte = []
    cashflows = []
    
    if ins.maturity_date() < ael.date_today():  
        return
    
    for l in ins.legs():
        for cf in l.cash_flows():
            if cf.pay_day >= ael.date_today():
                paydte.append(cf.pay_day)
                cashflows.append(cf)
    
    paydte.sort()
    
    next_paydte = paydte[0]
              
    enddte = []
    
    if next_paydte == dte:
        for cf in cashflows:
            if cf.type <> 'Fixed Amount' and cf.end_day >= ael.date_today().add_banking_day(ins.curr, -5):
                enddte.append(cf.end_day)

    else:
        enddte.append(ael.date('1970-01-01'))
    
    enddte.sort()
           
    ex_period = int(ins.ex_coup_period[:-1])
    
    exdte = enddte[0].add_days(-ex_period)
    
    ldr_date = exdte.add_banking_day(ins.curr, -1)

    return ldr_date
    
    
#bond_ldr_date(ael.Instrument['ZAR/R153'],ael.date_today())







