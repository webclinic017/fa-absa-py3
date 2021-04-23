""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/AACalendarExport.py"

import acm

""" 
Same as printCalendarsInfo, but instead of printing, 
the details are written to file.
"""
def writeCalendarsInfoToFile(file_path, location=None, year=None):
    target = '%scalendar%s information to %s' % (
        str('%s ' % location) if location else '',
        str('[%d]' % year) if year is not None else '',
        file_path
    )
    print('%s - will write %s' % (__name__, target))
    infos = __getCalendarsInfo(location=location, year=year)
    with open(file_path, 'wb') as fout:
        fout.write(infos)

    print('%s - finished writing %s' % (__name__, target))
    return

""" 
Collect and print the calendar details in a format that AA can consume.
Keyword args:
    location - Filter by name (None corresponds to all calendars)
    year - Filter the calendar details by year (None corresponds to all years)
"""
def printCalendarsInfo(location=None, year=None):
    infos = __getCalendarsInfo(location=location, year=year)
    print(infos)
    return

""" 
Private attributes and functions.
Do not directly refer to any of the below functions or attributes as
they may be subject to change.
"""
def __getCalendarsInfo(location, year):
    print('%s - collecting calendar information' % __name__)
    # Collect info for all matching calendars
    cals = acm.FCalendar.Select('name = \'%s\'' % location if location else '')
    infos = tuple([__getCalendarInfo(cal, year) for cal in cals])
    infos = '<Calendars>%s%s\n</Calendars>' % (
        __INFO_PREFIX, __INFO_PREFIX.join(infos)
    )
    return infos

def __getCalendarInfo(calendar, year):
    # Collect info for specific calendar
    weekends = __getWeekendDayNamesFromCalendar(calendar)
    holidays = __getHolidaysFromCalendar(calendar, year)
    info = '<Calendar Location="%s" Weekends="%s" Holidays="%s"/>' % (
        calendar.Name(), weekends, holidays
    )
    return info

def __getWeekendDayNamesFromCalendar(calendar):
    # Convert from FCalendar.WeekendDays() bitmask to day name(s)
    weekend_days_int = int(calendar.WeekendDays())
    sum = 0
    days = []
    for bit, day in __WEEKEND_DAY_BITMASK.items():
        if (weekend_days_int & bit) == bit:
            days.append(day)
            sum += bit

        if sum == weekend_days_int:
            return ', '.join(days)
            
    msg = 'Failed to get all weekend days from FCalendar.WeekendDays = %d' % (
        weekend_day_int
    )
    raise Exception(msg)

def __getHolidaysFromCalendar(calendar, year):
    # Collect details about any holidays in the matching year
    holidays = {}
    if year:
        year = int(year)

    for date in calendar.Dates():
        date_str = date.Date()      
        if (year is None) or (int(date_str[:4]) == year):
            holidays[date_str] = date.Description()

    holidays = ', '.join(
        str(holiday + '|' + info) for holiday, info in holidays.items()
    )
    return holidays

__WEEKEND_DAY_BITMASK = {
    2: 'Monday',
    4: 'Tuesday',
    8: 'Wednesday',
    16: 'Thursday', 
    32: 'Friday',
    64: 'Saturday',
    128: 'Sunday',
}
__INFO_PREFIX = '\n  '
