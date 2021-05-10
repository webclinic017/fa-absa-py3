
import acm, ael

def FeesSettled(object, date):
    feesSettled = 0
    totalfees = 0
    for p in object.Trade().Payments():
        if p.Type() == 'Broker Fee':
            if p.ValidFrom() <= date and p.PayDay() <= date: #acm.DateToday()
                feesSettled = p.Amount()
            else:
                feesSettled = 0.00
            totalfees = totalfees + feesSettled
    return totalfees

def FeesUnSettled(object, date):
    feesUnSettled = 0
    totalfees = 0
    for p in object.Trade().Payments():
        if p.Type() == 'Broker Fee':
            if p.ValidFrom() <= date and p.PayDay() > date: #acm.DateToday()
                feesUnSettled = p.Amount()
            else:
                feesUnSettled = 0.00
            totalfees = totalfees + feesUnSettled
    return totalfees

