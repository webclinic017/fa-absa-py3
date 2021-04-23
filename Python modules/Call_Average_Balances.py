import ael, acm, FSQL_functions
import Call_Average_Balances_OvrPeriod

from collections import OrderedDict

context = acm.GetDefaultContext()
calc_space = acm.Calculations().CreateCalculationSpace(context, 'FPortfolioSheet')
money_calc = acm.Calculations().CreateCalculationSpace(context, 'FMoneyFlowSheet')

def averageBalance(temp, trdnbr, date, *rest):
    end = acm.Time.DateAddDelta(date, 0, 0, 1) 
    start = acm.Time.FirstDayOfMonth(date)  
    trade = acm.FTrade[trdnbr]
    return Call_Average_Balances_OvrPeriod.AvgBalance(temp, trade.Instrument().Name(), start, end, *rest)*trade.Quantity()

def balanceOnDate(date, trade):
    calc_space.SimulateValue(trade, 'PLPeriodEnd', date)
    try:
        return calc_space.CalculateValue(trade, 'Deposit balance').Number()
    except:
       return 0

def totalInterest(temp,trdnbr,date,*rest):
    start = acm.Time.FirstDayOfMonth(date)
    end =  acm.Time.AsDate(date)
    trade = acm.FTrade[trdnbr]
    ins = trade.Instrument()
    total  = 0.0
    while start <= end:
        if balanceOnDate(start, trade) != 0:
            total = total + ((balanceOnDate(start, trade)*Call_Average_Balances_OvrPeriod.interestRateOnDate(ins, start))/36500)
        start = acm.Time.DateAddDelta(start, 0, 0, 1)
    return total
        

'''
    This method reads the rates directly from the cash flow.
'''
def interestRate(temp, date, trdnbr, *rest):
    trade = acm.FTrade[trdnbr]
    start = acm.Time.FirstDayOfMonth(date)
    if trade and trade.MoneyFlows():
        for flow in trade.MoneyFlows():
            if (start <= flow.StartDate() <= date) and flow.Type() == 'Call Fixed Rate Adjustable':
                return money_calc.CalculateValue(flow, 'Cash Analysis Forward Rate')*100  
    return 0.0
