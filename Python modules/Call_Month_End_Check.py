import ael, Call_Last_End_Day

'''
Date            Who                     What                                    CR Number
2008-05-13      Heinrich Cronje         Created                                 2820 - 2821
2008-06-03      Heinrich Cronje         Added function zeroRate                 3108 
2008-06-04      Heinrich Cronje         Added function rollingPeriod            3130
2008-07-31      Heinrich Cronje         Added function CFEndDayRedemptionPayDay 3793
2009-08-06      Heinrich Cronje         Added Call Region BB section            70346   1757
Description:

This AEL get called form that ASQL Call_Month_End_Check. It checks all the vital information for
all Call Accounts before Month End.

rollingBaseDayCheck:            If the Rolling Base Day is before the start day of the leg or if the 
                                Rolling Base Day is not the same as the start day of the leg or if the 
                                Rolling Base Day is not the first of the next month from the start day 
                                then it should be on the report.
currentIntStartDay:             If the latest Call Fixed Rate Adjustable's start date is before the first day of 
                                the current month then it should be on the report.
forwardDatedCashFlows:          If there is a cash flow done "today" with a future pay day then it should be on the report.
callRegion:                     If the add info field called Call_Region is empty or doesn't start with the letters
                                "INST" or "CORPORATE" then it should be on the report. 
zeroRate:                       If there is any resets with zero rates on the latest Call Fixed Rate Adjustable then the trade
                                should be on the report.
rollingPeriod:                  Any money market call account with rolling period not 1m should be on the report.
CFEndDayRedemptionPayDay:       The last interest cash flow's end day should equal the Redemption Amount's pay day.
CFFactor:                       The current Call Fixed Rate Adjustable interest entry should have a float_rate_factor = 1
CFNoResets:                     The current Call Fixed Rate Adjustable interest entry should have resets.
RedemptionMoreWeek:             Redemption amount should not be forward dated more that a week.
InterestPast:                   Interest that is created today should not have a payday before today
'''

def rollingBaseDayCheck(temp,trdnbr,*rest):
    t = ael.Trade[trdnbr]
    i = t.insaddr
    l = i.legs()[0]
    if l.rolling_base_day < l.start_day:
         return 1
    elif (l.rolling_base_day != l.start_day.add_months(1).first_day_of_month()) and (l.start_day != l.rolling_base_day):
         return 1
    return 0

def currentIntStartDay(temp,trdnbr,*rest):
    t = ael.Trade[trdnbr]
    i = t.insaddr
    d = ael.date_today()
    end_date = ael.date('1970-01-01')
    cfwnbr = 0
    
    for cf in i.legs()[0].cash_flows():
        if cf.type == 'Call Fixed Rate Adjustable':
            if cf.end_day > end_date:
                end_date = cf.end_day
                cfwnbr = cf.cfwnbr
    
    for c in i.legs()[0].cash_flows():
        if c.cfwnbr == cfwnbr:
            if c.start_day < d.first_day_of_month():
                return c.start_day
            else:
                return d

def forwardDatedCashFlows(temp,trdnbr,*rest):
    t = ael.Trade[trdnbr]
    i = t.insaddr
    
    for cf in i.legs()[0].cash_flows():
        if cf.type == 'Fixed Amount':
            if ael.date_from_time(cf.creat_time) == ael.date_today() and cf.pay_day > ael.date_from_time(cf.creat_time):
                return cf.cfwnbr
    
    return 0

def callRegion(temp,trdnbr,*rest):
    t = ael.Trade[trdnbr]
    if t.add_info('Call_Region')[0:4] == 'INST' or t.add_info('Call_Region')[0:9] == 'CORPORATE' or t.add_info('Call_Region')[0:2] == 'BB':
        return 0
    else:
        return 1

def zeroRate(temp,trdnbr,*rest):
    t = ael.Trade[trdnbr]
    for cf in t.insaddr.legs()[0].cash_flows():
        if cf.type == 'Call Fixed Rate Adjustable' and ael.date_today() > cf.start_day and ael.date_today() <= cf.end_day:
            for r in cf.resets():
                if r.value == 0:
                    return cf.cfwnbr
    return 0

def rollingBasePeriod(temp,trdnbr,*rest):
    t = ael.Trade[trdnbr]
    if t.insaddr.legs()[0].rolling_period != '1m':
        return t.insaddr.legs()[0].rolling_period
    return ''

def CFEndDayRedemptionPayDay(temp,trdnbr,*rest):
    t = ael.Trade[trdnbr]
    lastCFDay = Call_Last_End_Day.lastCFEndDay(temp, trdnbr)
    
    for cf in t.insaddr.legs()[0].cash_flows():
        if cf.type == 'Redemption Amount' and cf.pay_day != lastCFDay:
            return 1
            
    return 0

def CFFactor(temp,insid,*rest):
    i = ael.Instrument[insid]
    for cf in i.legs()[0].cash_flows():
        #if cf.type == 'Call Fixed Rate Adjustable' and ael.date_today() > cf.start_day and ael.date_today() <= cf.end_day:
        if cf.type == 'Call Fixed Rate Adjustable':
            if cf.float_rate_factor != 1:
                return 1
    return 0

def CFNoResets(temp,insid,*rest):
    i = ael.Instrument[insid]
    for cf in i.legs()[0].cash_flows():
        if cf.type == 'Call Fixed Rate Adjustable' and ael.date_today() > cf.start_day and ael.date_today() <= cf.end_day:
            if cf.resets().members() == []:
                return 1
    return 0

def RedemptionMoreWeek(temp,insid,*rest):
    i = ael.Instrument[insid]
    for cf in i.legs()[0].cash_flows():
        if cf.type == 'Redemption Amount':
            if cf.pay_day > ael.date_today().add_weeks(1):
                return 1
    return 0

def InterestPast(temp,insid,*rest):
    i = ael.Instrument[insid]
    l = i.legs()[0]
    today = ael.date_today()
    for cf in l.cash_flows():
        if cf.type in ('Call Fixed Rate Adjustable', 'Fixed Rate Adjustable'):
            if ael.date_from_time(cf.creat_time) == today and cf.pay_day < today:
                return 1
    return 0
