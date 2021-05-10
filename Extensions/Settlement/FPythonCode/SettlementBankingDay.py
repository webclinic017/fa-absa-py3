""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/gui/SettlementBankingDay.py"
import acm

from FAccountingDates import IsDateNonBankingDay, AdjustDateToModFollowingUsingCalendar
from FOperationsDateUtils import GetCalendarFromCurrency

def HandleBankingDay(shell, settlementProxy, date):
    calendar = GetCalendarFromCurrency(settlementProxy.Currency())
    if IsDateNonBankingDay(date, calendar):
        adjustedDate = AdjustDateToModFollowingUsingCalendar(calendar, date)
        weekday = acm.Time.DayOfWeek(date)
        msg = "According to the calendar, " + date + \
        " is not a valid business day (" + weekday + ").\n\n" + \
        "Change date to the next following business day (" + adjustedDate + ")?"
        output = acm.UX().Dialogs().MessageBoxYesNo(shell, 'Question', msg)
        if output == "Button1":
            date = adjustedDate
    return date
