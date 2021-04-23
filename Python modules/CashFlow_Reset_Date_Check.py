import ael

#Date           Who                     CR Number       What
#2008-07-09     Heinrich Cronje         3506            Created
#2008-08-14     Heinrich Cronje         3837            Added Functions to fix the reset dates.

#Description
#
#This ael gets called from the ASQL: SAMM_CashFlow_Reset_Date_Check.
#It checks the following information:
#       The reset date should equal the cash flow start day.
#       The reset start day should equal the cash flow start day.
#       The reset end day should equal the cash flow end day.
#       The reset date should equal the reset start day.
#       The end day of a float rate cashflow should be followed by
#               a cash flow with the same start date.

def checkReset(temp,cfwnbr,*rest):
    startDay = []
    endDay = []
    resetDate = []
    cf = ael.CashFlow[cfwnbr]
    returnValue = ''
    
    if len(cf.resets().members()) == 1:
        for r in cf.resets():
            startDay.append(r.start_day)
            endDay.append(r.end_day)
            resetDate.append(r.day)
    
            if r.day != r.start_day:
                returnValue = returnValue + '4'
                
        resetDate.sort()
        startDay.sort()
        endDay.sort()
        
        for d in resetDate:
            if d != cf.start_day:
                returnValue = returnValue + '1'
            
        if startDay[0] != cf.start_day:
            returnValue = returnValue + '2'
            
        if endDay[len(endDay)-1] != cf.end_day:
            returnValue = returnValue + '3'
    else:
        returnValue = ''
    
    return returnValue

def cashflowStartEndDayCheck(temp,trdnbr,*rest):
    cashEnd = ael.date('1970-01-01')
    t = ael.Trade[trdnbr]
    i = t.insaddr
    cashflowStart = []
    cashflowEnd = []
    
    if i.legs().members() != []:
        for l in i.legs():
            for cf in i.cash_flows():
                if cf.type == 'Float Rate':
                    cashflowStart.append(cf.start_day)
                    cashflowEnd.append(cf.end_day)
                    if cashEnd < cf.end_day:
                        cashEnd = cf.end_day

    cashflowStart.sort()
    cashflowEnd.sort()
    
    for i in cashflowEnd:
        if i != cashEnd:
            if not cashflowStart.__contains__(i):
                return 1
    return 0

def resetDateCFStartDate(temp,cfwnbr,*rest):
    ael.poll()
    cf = ael.CashFlow[cfwnbr]
    if len(cf.resets().members()) == 1:
        r = cf.resets()[0]
        if r.day != cf.start_day:
            re = r.clone()
            re.day = cf.start_day
            try:
                re.commit()
                print cf.cfwnbr, 'Done'
                return 'Done'
            except:
                print cf.cfwnbr, 'Error'
                return 'Error'            
        print cf.cfwnbr, 'No Change'
        return 'No Change'
    else:
        print cf.cfwnbr, 'Multiple Resets'
        return 'Multiple Resets'

def resetStartDayCFStartDay(temp,cfwnbr,*rest):
    ael.poll()
    cf = ael.CashFlow[cfwnbr]
    if len(cf.resets().members()) == 1:
        r = cf.resets()[0]
        if r.start_day != cf.start_day:
            re = r.clone()
            re.start_day = cf.start_day
            try:
                re.commit()
                print cf.cfwnbr, 'Done'
                return 'Done'
            except:
                print cf.cfwnbr, 'Error'
                return 'Error'            
        print cf.cfwnbr, 'No Change'
        return 'No Change'
    else:
        print cf.cfwnbr, 'Multiple Resets'
        return 'Multiple Resets'

def resetEndDayCFEndDay(temp,cfwnbr,*rest):
    ael.poll()
    cf = ael.CashFlow[cfwnbr]
    if len(cf.resets().members()) == 1:
        r = cf.resets()[0]
        if r.end_day != cf.end_day:
            re = r.clone()
            re.end_day = cf.end_day
            try:
                re.commit()
                print cf.cfwnbr, 'Done'
                return 'Done'
            except:
                print cf.cfwnbr, 'Error'
                return 'Error'            
        print cf.cfwnbr, 'No Change'
        return 'No Change'
    else:
        print cf.cfwnbr, 'Multiple Resets'
        return 'Multiple Resets'

def resetRate(temp,cfwnbr,*rest):
    cf = ael.CashFlow[cfwnbr]
    if len(cf.resets().members()) == 1:
        r = cf.resets()[0]
        if cf.legnbr.float_rate.used_price(cf.start_day, 'ZAR', None, 3, 'SPOT') != r.value:
            return r.value
    return -1

def resetRateFix(temp,cfwnbr,*rest):
    ael.poll()
    cf = ael.CashFlow[cfwnbr]
    if len(cf.resets().members()) == 1:
        r = cf.resets()[0]
        if cf.legnbr.float_rate.used_price(cf.start_day, 'ZAR', None, 3, 'SPOT') != r.value:
            re = r.clone()
            re.value = cf.legnbr.float_rate.used_price(cf.start_day, 'ZAR', None, 3, 'SPOT')
            try:
                re.commit()
                return str(cf.cfwnbr) + 'Done'
            except:
                return str(cf.cfwnbr) + 'Error on save'
    return str(cf.cfwnbr) + 'No Change'
