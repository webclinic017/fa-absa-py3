import acm

# Script to assist MidOffice in adding the Break days to Currency Swaps that runs longer than 3 years.
# It is called from the Instrument definition (Currency Swaps) under Special -> Add Breaks.
# ABITFA 1320
# Developer: Mighty Mkansi, Added logic to modify non banking days to banking days
 
def getCalendar(ins, cal):    
    for leg in ins.Legs():
        if cal == 'Calendar1' :            
            return leg.PayCalendar()
        elif cal == 'Calendar2':            
            return leg.Pay2Calendar()
        elif cal == 'Calendar3':            
            return leg.Pay3Calendar()  
        break        
    
def getDayCountMethod(ins):    
    for leg in ins.Legs():
        return leg.PayDayMethod()
        break
        
def getBusinessDate(ins, date):
    # This function assumes maximum of three calendar, I used the combination of the three calendars as the
    # IsNonBankingDay and ModifyDate only takes to calendars as arguments

    Calendar_1 = getCalendar(ins, 'Calendar1')
    Calendar_2 = getCalendar(ins, 'Calendar2')
    Calendar_3 = getCalendar(ins, 'Calendar3')
    dayMethod = getDayCountMethod(ins)    
    if Calendar_1.IsNonBankingDay(Calendar_1, Calendar_2, date):    
        return Calendar_1.ModifyDate(Calendar_1, Calendar_2, date, dayMethod)        
    elif  Calendar_1.IsNonBankingDay(Calendar_1, Calendar_3, date):    
        return Calendar_1.ModifyDate(Calendar_1, Calendar_3, date, dayMethod)        
    elif Calendar_2.IsNonBankingDay(Calendar_2, Calendar_3, date):    
        return Calendar_2.ModifyDate(Calendar_2, Calendar_3, date, dayMethod)        
    else:    
        return date      

def check_has_breaks(acm_ins):
    hasbreak = False
    bes = acm_ins.ExerciseEvents()
    for be in bes:
        if be.Type() == 'Break':
            hasbreak = True
            break
    return hasbreak

def get_dates(acm_ins):
    for leg in acm_ins.Legs():
        datediff  = acm.Time().DateDifference( leg.EndDate(), leg.StartDate())
        break
        
    used_trades = [t for t in acm_ins.Trades() if t.Status() not in ( 'Void', 'Simulated')]
    
    if len(used_trades) == 1 :
        trddate = used_trades[0].TradeTime()
    else:
        trddate = None

    return (leg.StartDate(), leg.EndDate(), datediff/365, trddate)
        

def addBreaksFromMenu(eii):
    acm_ins = eii.ExtensionObject().CurrentObject().Instrument()
    msg = addBreaksAfterXYears(acm_ins, 3, 10)
    try:
        func = acm.GetFunction('msgBox', 3)
        ret = func('Info', msg, 0)
    except:
        print acm_ins.Name(), '   :   ', msg
    
    
def addBreaksAfterXYears(acm_ins,years=3, skip_break_within_end_days = 10):
    hasbreak = check_has_breaks(acm_ins)
    if hasbreak:
        return '-This instrument already has breaks, not adding anything'
    
    start, end, yrdiff, trddate = get_dates(acm_ins)
    if yrdiff < years:
        return '-This instrument runs for %f years (< %f ), not adding anything' %(yrdiff, years)
    
    if trddate:
        breakdate = acm.Time().DateAddDelta(trddate, years, 0, 0)
        msg = "Break date based on the trade's date %s\n" %trddate
    else:
        breakdate = acm.Time().DateAddDelta(start, years, 0, 0)
        msg = "Break date based on the instrument start date %s\n" %start
    
    while breakdate < end:
        if breakdate > acm.Time().DateAddDelta(end, 0, 0, -1 * skip_break_within_end_days):
            msg += '-Not adding breakdate %s, it is too close to the end date %s\n' %(breakdate, end)
        else:
            ee = acm.FExerciseEvent()
            ee.Instrument = acm_ins
            ee.Date = getBusinessDate(acm_ins, breakdate)
            ee.SettlementDate = getBusinessDate(acm_ins, breakdate)
            ee.NoticeDate = getBusinessDate(acm_ins, breakdate)
            ee.Type = 'Break'
            ee.Commit()
            acm_ins.Commit()
            msg += '+Added break %s\n' % getBusinessDate(acm_ins, breakdate)
        breakdate = acm.Time().DateAddDelta(breakdate, 1, 0, 0)
    return msg



