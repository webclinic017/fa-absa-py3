""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingDates.py"
import acm

# operations
from FOperationsDateUtils import GetAccountingCurrencyCalendar

# accounting
from FAccountingGetters import GetBookAndTreatmentLink

#-------------------------------------------------------------------------
def AdjustDateToModFollowing(date):
    calendar = GetAccountingCurrencyCalendar()
    return AdjustDateToModFollowingUsingCalendar(calendar, date)

#-------------------------------------------------------------------------
def AdjustDateToModFollowingUsingCalendar(calendar, date):
    if IsDateNonBankingDay(date, calendar):
        adjustedDate = calendar.AdjustBankingDays(date, 1)
        if not AreDatesInTheSameMonth(date, adjustedDate):
            adjustedDate = calendar.AdjustBankingDays(date, -1)
    else:
        adjustedDate = date

    return adjustedDate

#-------------------------------------------------------------------------
def AdjustDateToModPreceding(date):
    calendar = GetAccountingCurrencyCalendar()
    if IsDateNonBankingDay(date, calendar):
        adjustedDate = calendar.AdjustBankingDays(date, -1)
        if not AreDatesInTheSameMonth(date, adjustedDate):
            adjustedDate = calendar.AdjustBankingDays(date, 1)
    else:
        adjustedDate = date

    return adjustedDate

#-------------------------------------------------------------------------
def AreDatesInTheSameMonth(date1, date2):
    ymd1 = acm.Time.DateToYMD(date1)
    ymd2 = acm.Time.DateToYMD(date2)
    month1 = ymd1.At(1)
    month2 = ymd2.At(1)
    return month1 == month2

#-------------------------------------------------------------------------
def IsDateNonBankingDay(date, calendar):
    calInfo = calendar.CalendarInformation()
    return calInfo.IsNonBankingDay(date)

#-------------------------------------------------------------------------
def GetStartDate(info, compareDate, startDate, endDate, endOfDayDate):

    bookLink, treatmentLink = GetBookAndTreatmentLink(info)

    assert bookLink and treatmentLink, \
        "Expected bookLink and treatmentLink to be found, got {}, {}".format(bookLink, treatmentLink)

    return acm.Accounting.CalculateAmendStartDate( \
        bookLink, treatmentLink, compareDate, startDate, endDate, endOfDayDate)

#-------------------------------------------------------------------------
def GetEndDate(info, compareDate, startDate, endDate, endOfDayDate):

    bookLink, treatmentLink = GetBookAndTreatmentLink(info)

    assert bookLink and treatmentLink, \
        "Expected bookLink and treatmentLink to be found, got {}, {}".format(bookLink, treatmentLink)

    return acm.Accounting.CalculateAmendEndDate(\
        bookLink, treatmentLink, compareDate, startDate, endDate, endOfDayDate)

#-------------------------------------------------------------------------
class TimeScope:
    TIME_SCOPE_YEAR  = 0
    TIME_SCOPE_MONTH = 1

#-------------------------------------------------------------------------
def IsLastBankingDayInTimeScope(date, calendar, timeScope):
    if IsDateNonBankingDay(date, calendar):
        return False
    else:
        ymd1 = acm.Time.DateToYMD(date)
        ymd2 = acm.Time.DateToYMD(calendar.AdjustBankingDays(date, 1))
        return ymd1[timeScope] != ymd2[timeScope]

#-------------------------------------------------------------------------
def IsLastBankingDayOfMonth(date, calendar):
    return IsLastBankingDayInTimeScope(date, calendar, TimeScope.TIME_SCOPE_MONTH)

#-------------------------------------------------------------------------
def IsLastBankingDayOfYear(date, calendar):
    return IsLastBankingDayInTimeScope(date, calendar, TimeScope.TIME_SCOPE_YEAR)
