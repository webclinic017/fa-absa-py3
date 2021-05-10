""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/FOperationsDateUtils.py"
import acm

#-------------------------------------------------------------------------
def GetCalendarFromCurrency(currency):
    accountingCurrency = currency
    assert(accountingCurrency)
    return accountingCurrency.Calendar()

#-------------------------------------------------------------------------
def GetAccountingCurrencyCalendar():
    accountingCurrency = acm.FCurrency[str(acm.UsedAccountingCurrency())]
    assert(accountingCurrency)
    return accountingCurrency.Calendar()

#-------------------------------------------------------------------------
def AdjustDateToday(calendar, daysDelta):
    assert(calendar)
    assert(daysDelta != None), "No daysDelta (number of days) to AdjustDateToday()"
    return calendar.AdjustBankingDays(acm.Time.DateToday(), str(daysDelta))
