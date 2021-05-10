"""
MODULE
        FInstrumentCACashflow - Find the cash balance for CallAccount cashflows
UPDATED
        2006-08-16
DESCRIPTION
        cash balance = redemption amount + accrured interest
"""

import ael
import acm


#Create Standard Calculation Space
calcSpace = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()           

 
def caCashBalance(ins):
    balance=0.0
    legs = ins.Legs()
    if not legs:
        return balance
    leg=legs.At(0) # only 1 leg for CallAccount
    if not leg:
        return balance
    cashflows=leg.CashFlows()
    if not cashflows:
        return balance
    trades = ins.Trades()
    if not trades:
        return balance
    sign = trades.At(0).Quantity()
        
    cf1=None
    cf2=None
    
    for cf in cashflows:
        if cf.CashFlowType() == 'Redemption Amount':
            cf1 = cf
            continue
        if cf.CashFlowType() == 'Call Fixed Rate Adjustable' or cf.CashFlowType() == 'Call Fixed Rate' or cf.CashFlowType() == 'Call Float Rate': 
            if not cf2:
                cf2=cf
            elif cf.EndDate() >= cf2.EndDate():
                cf2=cf

    if cf1:
        balance += cf1.Calculation().Projected(calcSpace, trades).Number()
    if cf2:
        balance += cf2.Calculation().Projected(calcSpace, trades).Number()
    
    return balance * (-1) * sign #opposite sign to redemption cashflow

def caRedemption(ins):
    dateToday=acm.Time.DateToday()
    #balance=acm.DenominatedValue(0.0, ins.Currency, dateToday)
    balance=0.0
    legs = ins.Legs()
    if not legs:
        return balance
    leg=legs.At(0) # only 1 leg for CallAccount
    if not leg:
        return balance
    cashflows=leg.CashFlows()
    if not cashflows:
        return balance
    trades = ins.Trades()
    if not trades:
        return balance
    trade = trades.At(0)
    sign = trade.Quantity()
        
    cf1=None
    
    for cf in cashflows:
        if cf.CashFlowType() == 'Redemption Amount':
            cf1 = cf
            break

    if cf1:
        balance = cf1.Calculation().Projected(calcSpace, trade).Number()
    totalBalance = balance * sign #opposite sign to redemption cashflow
    return totalBalance 

        
