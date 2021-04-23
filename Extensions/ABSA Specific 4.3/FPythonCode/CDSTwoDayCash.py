
import acm, ael

def getNextCashflow(trade, type, today, days):
    '''
Return the next cashflow for a specific type and where the next payday is equal to today + 2d
    '''
    ins = trade.Instrument()
    today = ael.date(today)

    for l in ins.Legs():
        if l.LegType() == type:
            for cf in l.CashFlows():
                cfDate = ael.date(cf.PayDate())
                diff = today.days_between(cfDate)
                
                if diff > 0 and diff <= days:
                    aelCF = ael.CashFlow[cf.Oid()]
                    return trade.Quantity() * aelCF.projected_cf()
    return 0
