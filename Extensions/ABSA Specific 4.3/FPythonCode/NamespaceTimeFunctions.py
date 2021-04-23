import acm, ael, string
'''
Date                    : 2011-01-27, 2010-07-23
Purpose                 : Custom Methods on FNamespaceTime
Developer               : Rohan van der Walt
CR Number               : 391566,581108
HISTORY
================================================================================
Date        Change no   Developer               Description
--------------------------------------------------------------------------------
2011-01-27  391566      Rohan vd Walt           Initial Implementation
2014-02-18  1752210     Rohan vd Walt           Added params with default values on DateAddDeltaType for Cal and bDayMethod 

'''

def GetLastBusinessDayOfMonth(self, date):
    '''
    Given a date object, it calculates the last 
    business date in the month using ZAR Johannesburg Calendar
    '''
    cal = acm.FCalendar['ZAR Johannesburg']
    nst = acm.Time()
    first = nst.FirstDayOfMonth(nst.DateAddDelta(date, 0, 1, 0))
    first = cal.AdjustBankingDays(first, -1)
    return first
    
def DateAddDeltaType(self, date, delta, type, cal='ZAR Johannesburg', bDayMethod='Mod. Following'):
    '''
    Takes ACM date object, adds delta of type ( "Y" = Year, "M" = Month, "D" = Day )
    Returns delta adjusted date (ael), again adjusted to banking day with ZAR Johannesburg Calendar
    '''
    result = None
    if string.upper(type) == 'Y':
        result = acm.Time().DateAddDelta(date, delta, 0, 0)
    elif string.upper(type) == 'M':
        result = acm.Time().DateAddDelta(date, 0, delta, 0)
    elif string.upper(type) == 'D':
        result = acm.Time().DateAddDelta(date, 0, 0, delta)
    else:
        result = date
    # Used ael instead of acm's AdjustBankingDay because of performance reasons
    return ael.date(result).adjust_to_banking_day(ael.Calendar[cal], bDayMethod)
          
