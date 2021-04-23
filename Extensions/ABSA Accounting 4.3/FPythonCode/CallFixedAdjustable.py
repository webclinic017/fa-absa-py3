'''
Date        CR Number   Who                      What
2011-05-27  666125      Paul Jacot-Guillarmod    Corrected an error that occurs when viewing the balance column backdated, the cashflow startdate
                                                 should be <= repday, not strictly <.                                            
'''

import acm

def getFixedAdjustableCashFlows(leg, comparedDate):
    res = []
    for c in leg.CashFlows():
        cashFlowType = c.CashFlowType()
        if (cashFlowType == "Call Fixed Rate Adjustable" or cashFlowType == "Fixed Rate Adjustable"):
            if c.PayDate() > comparedDate:
                if c.EndDate() <= comparedDate:
                    res.append(c)
    return res


def getRateFixedAdjustableCashFlows(leg, dateToday):
    res = []
    for c in leg.CashFlows():
        cashFlowType = c.CashFlowType()
        if (cashFlowType == "Call Fixed Rate Adjustable" or cashFlowType == "Fixed Rate Adjustable"):
            if c.PayDate() >= dateToday:
                res.append(c)
    return res

def getFutureAdjustableCashFlows(leg, repDay):
    res = []
    for c in leg.CashFlows():
        if c.CashFlowType() in ('Fixed Amount', 'Interest Reinvestment') and c.PayDate() > repDay and c.PayDate <= leg.EndDate():
            if not (c.StartDate() and c.StartDate() <= repDay):
                res.append(c)
    return res

