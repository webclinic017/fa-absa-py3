import acm, ael, pprint

'''
Date                    : 2010-06-02
Purpose                 : Calculates Average Balance over custom period, using existing "Balance" column and simulating PLPeriodEnd value.
                          Calculates Average Rate over custom period, using resets  
Department and Desk     : Money Market
Requester               : Marilize Knoetze
Developer               : Rohan van der Walt
CR Number               : 333324
'''

def AvgBalance(temp, ins, start, end, *rest):
    '''
    Calculates the average balance of call account over a custom period. Uses Balance trading manager column to calculate the balance of a column.
    Simulates the PLPeriodEnd value for each day, and gets the dailyBalance, and then calculates the average.
    '''
    try:
        ins = acm.FInstrument[ins]    
        nsTime = acm.Time()
        start = nsTime.AsDate(start)
        end = nsTime.AsDate(end)
        if not ins.IsExpired() and start < end:
            dailyBalance = {}
            context = acm.GetDefaultContext()
            sheet_type = 'FPortfolioSheet'
            calc_space = acm.Calculations().CreateCalculationSpace(context, sheet_type)
            endValue = calc_space.CalculateValue(ins, 'PLPeriodEnd')
            while start < end:
                calc_space.SimulateValue(ins, 'PLPeriodEnd', start)
                try:
                    dailyBalance[str(start)] = calc_space.CalculateValue(ins, 'Deposit balance').Number()
                except:
                    print ins
                start = nsTime.DateAddDelta(start, 0, 0, 1)
            return sum([dailyBalance[i] for i in dailyBalance.keys()])/float(len(dailyBalance.keys()))
        else:
            return 0
    except:
        return 0

def interestRateOnDate(ins, date):
    '''
    InterestRateOnDate is calculated as the SUM of all Call Fixed Rate Adjustable reset value's where "date >= cf.StartDate AND date < cd.EndDate"
    '''
    result = 0
    for i in ins.Legs()[0].CashFlows():
        if i.CashFlowType() == "Call Fixed Rate Adjustable" and date >= i.StartDate() and date < i.EndDate():
            for r in i.Resets():
                if date >= r.StartDate() and date < r.EndDate():
                    result = result + r.FixingValue()
    if result == 0:
        print 'Interest Rate on', date, '= 0, Instrument', ins.Name(), ' has no rate defined for this date'
    return result
    
def AvgInterestRate(temp, ins, start, end, *rest):
    '''
    Calculates the Interest rate for each day in the period, then returns average rate per day
    '''
    try:
        ins = acm.FInstrument[ins]
        nsTime = acm.Time()
        date = nsTime.AsDate(start)
        end = nsTime.AsDate(end)
        if not ins.IsExpired() and date < end:
            dailyRate = {}
            while date < end:
                dailyRate[str(date)] = interestRateOnDate(ins, date)
                if dailyRate[str(date)] == 0:           #If one day's rate is not found, do not continue, return 0
                    return 0
                date = nsTime.DateAddDelta(date, 0, 0, 1)
            return sum([dailyRate[i] for i in dailyRate.keys()])/float(len(dailyRate.keys()))
        else:
            return 0
    except:
        return 0
