"""-----------------------------------------------------------------------
MODULE
    CashDaily

DESCRIPTION

    Date                : 2012-09-19
    Purpose             : Returns the daily cash movements of a trade
    Department and Desk : Prime Services
    Requester           : Danilo Mantoan
    Developer           : Nidheesh Sharma
    CR Number           : 556348

ENDDESCRIPTION
-----------------------------------------------------------------------"""

import acm

#Function to return the total cash movement of a trade for the portfolio end date
def ReturnTotalCashDaily(trade, pnlEndDate):
    totalCashDaily = 0.0
    if trade.Status() not in ('Void'):
        moneyFlows = trade.MoneyFlows(pnlEndDate, pnlEndDate)
        for flow in moneyFlows:
            cash = flow.Calculation().Projected(acm.FStandardCalculationsSpaceCollection()).Number()
            totalCashDaily += cash
    return totalCashDaily
