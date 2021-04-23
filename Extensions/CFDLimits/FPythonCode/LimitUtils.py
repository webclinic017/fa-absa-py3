"""-----------------------------------------------------------------------
MODULE
    LimitUtils

DESCRIPTION
    Institutional CFD Project
    
    Date                : 2010-10-23, 2010-11-16
    Purpose             : Utility functions used by the LimitSetting and LimitMonitoring modules.
    Department and Desk : Prime Services
    Requester           : Francois Henrion
    Developer           : Marco Cerutti, Herman Hoon
    CR Number           : 455227, 494772

ENDDESCRIPTION
-----------------------------------------------------------------------"""
import acm
import ael

EXTENSION_MODULE = "CFDLimits"
EXTENSION_CONTEXT = "Standard"
DEFAULT_LIMIT_COLUMN_ID = 'CFD Limit Status'

YDRIVE = "Y:\Jhb\FAReports\AtlasEndOfDay\\"

# A dictionary of columns and associated Breach values
BREACH_COLUMNS = {"CFD Limit Status":
                    {"value":"Breached","context":"Standard"},
                  "Trading Capacity Availability Status":
                    {"value":"Breached","context":"Standard"}}

SMTP_MAILSERVER = acm.GetCalculatedValue(0, acm.GetDefaultContext().Name(), 'mailServerAddress').Value()
SMTP_ME = "Front Arena"
SMTP_YOU = ["janet.loots@absacapital.com", "nicholasjames.watson@absacapital.com", "francois.henrion@absacapital.com"]

THREE_MONTH_MARKET = "3m Average Volume"
""" Market holding rolling average volumes over last 3 months. """

DAILY_MARKET = "Volume"
""" Uploaded daily, via a feed. Contains volume traded today"""

BUSINESS_DAY_METHOD = 2
""" Preceding:  Use the previous valid business day before the non-business day. """

def unique_sorted_sequence(seq): 
    seen = set() 
    seen_add = seen.add 
    result = [ x for x in seq if x not in seen and not seen_add(x)] 
    result.sort
    return result


acmCalendar = acm.FCurrency[str(acm.UsedAccountingCurrency())].Calendar()
calendar = ael.Calendar[acmCalendar.Name()]

TODAY           = ael.date_today()
PREVBUSDAY      = TODAY.add_banking_day(calendar, -1) 
TWODAYSAGO      = TODAY.add_days(-2)
YESTERDAY       = TODAY.add_days(-1)

EndDateList     = { 'Now':TODAY.to_string(ael.DATE_ISO),\
                    'TwoDaysAgo':TWODAYSAGO.to_string(ael.DATE_ISO),\
                    'PrevBusDay':PREVBUSDAY.to_string(ael.DATE_ISO),\
                    'Yesterday':YESTERDAY.to_string(ael.DATE_ISO),\
                    'Custom Date':TODAY.to_string(ael.DATE_ISO)}

EndDateListSortedKeys = EndDateList.keys()
EndDateListSortedKeys.sort()

SMTPYouSortedKeys = SMTP_YOU
SMTPYouSortedKeys.sort()

BreachColumnsSortedKeys = BREACH_COLUMNS.keys()
BreachColumnsSortedKeys.sort()

