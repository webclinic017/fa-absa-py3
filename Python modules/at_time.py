# -*- coding: latin-1; -*-
'''
:Author: Andreas Bayer <Andreas.Bayer@absacapital.com; Andreas.Bayer@d-fine.de>
:Version: 0.1, 2014/02/15
:Summary: General acm, ael, python date and datetime aware functions for Front Arena Python programming

History
=======
2014-02-15  Andreas Bayer, created (in an attempt to beat the time)

Summary:
========

Time related functions extending Pythons time and datetime modules

The at_time module works even without ael and acm in sys.modules. If the acm or ael modules are available
then the default TODAY value is taken from acm.Time.DateToday() or ael.date_today(), otherwise
datetime.datetime.today() is used. Moreover, with ael available, the functions
to_date(), to_datetime() and to_timestamp() know about ael.ael_date objects.

The high-level "convert to date" functions (i.e., to_date(), ael_date() and
acm_date()) support the following input formats for conversion to their
respective output types:

* ael.ael_date objects (if the ael module is in use)
* strings (str, unicode), parsed using date_from_string()
* numbers (int, long, float), interpreted as a timestamp
* lists or tuples converted to time.struct_time using to_struct_time()
* datetime.datetime objects
* datetime.date objects

In the case of datetime input format, the time part is ignored in the
conversion.

The "convert to datetime" functions (i.e., to_datetime(), to_timestamp(),
acm_datetime(), ...) support the same input formats. In the case of a
date-only input format the time of the day is considered to be 00:00:00.


Date and Datetime String Parsing
================================
Parsing a string for a date is done in date_from_string(). The function parses
absolute dates in ISO Format 'YYYY-MM-DD' and in DIN5008-conform Format 'DD.MM.YYYY' and
symbolic names. In the DIN5008-conform Format the day and month part can also be
single-digit and the year can have two or four digits. If the year has two
digit strp2dyear() is used to get the actual year. Years with number less than
1000 can be inputted with leading zeros, i.e., '1.1.70' and '1.1.0070' are
parsed to different dates. Additional handling for date formats used in South
Africa will be implemented soon.

    >>> to_date('1.1.1970')
    datetime.date(1970, 1, 1)
    >>> to_date('01.01.1970')
    datetime.date(1970, 1, 1)
    >>> to_date('1970-01-01')
    datetime.date(1970, 1, 1)
    >>> to_date('01.01.70')
    datetime.date(1970, 1, 1)
    >>> to_date('01.01.0070')
    datetime.date(70, 1, 1)

Symbolic names are strings like 'TODAY'. See date_from_symbolic_date() for a
list of all supported names. Matching of the names is case in-sensitive.

    >>> to_date('FIRSTDAYOFMONTH', today = datetime.date(1963, 4, 6))
    datetime.date(1963, 4, 1)
    >>> to_date('LASTDAYOFMONTH', today = datetime.date(1963, 4, 6))
    datetime.date(1963, 4, 30)

The absolute or symbolic date can be followed by an offset, represented by a
date period string like '1d', '-2m' or '+2y'. The period shifts the date by
days (for 'd'), months (for 'm') or years (for 'y'). Several offsets can be
combined into a single string, e.g., '+1d1m' is an offset of one day and one
month. Note that the initial sign is mandatory if the period string follows
after a symbolic or absolute date, but can be skipped if only a period string
is given. It is good practice to always use the initial sign.

    >>> to_date('FIRSTDAYOFYEAR+1m+2d', today = datetime.date(1963, 4, 6))
    datetime.date(1963, 2, 3)
    >>> to_date('TWODAYSAGO-1m+2d', today = datetime.date(1963, 4, 6))
    datetime.date(1963, 3, 6)
    >>> to_date('1963-04-06-1m+2d')
    datetime.date(1963, 3, 8)
    >>> to_date('1963-04-06-1m2d')
    datetime.date(1963, 3, 4)
    >>> to_date('2d1m', today = datetime.date(1963, 4, 6))
    datetime.date(1963, 5, 8)
    >>> to_date('+2d1m', today = datetime.date(1963, 4, 6))
    datetime.date(1963, 5, 8)


Date Periods
============
The dateperiod class represents time periods of a given amount of days, months
and years. The objects support infix addition and subtraction:

    >>> dateperiod(days=2) + '2012-12-12'
    datetime.date(2012, 12, 14)
    >>> '2012-12-12' + dateperiod(days=2)
    datetime.date(2012, 12, 14)
    >>> dateperiod(days=2) + dateperiod(years=-1, days=-3)
    dateperiod(days=-1, years=-1)

The string representation of a dateperiod is the format parsed by the
dateperiod.fromstring() classmethod and in date_from_string():

    >>> str(dateperiod(weeks=1, days=3, years=1, months=2))
    '+10d+2m+1y'

Function Overview
=================

Calendar Calculations
=====================
`add_months(d, months, truncate=False)`_ 
    - add years to date returning a new
      datetime.date object. The date d can be any input suitable for to_date().
`add_days(d, days, truncate=False)`_
    - add days to date
`add_delta(d, days=0, months=0, years=0, truncate=False)`_ 
    - add days, months and years

`acm_calendar(cal)`_
    - return acm.FCalendar object for cal
`is_banking_day(cal, d)`_
    - True if date d is a banking day in calendar cal
`is_non_banking_day(cal, d)`_
    - True if d is a non-banking day in calendar cal
`bankingday_timediff(cal, t1, t2)`_
    - return timedelta between t1 and t2 counting only the time of banking days

Time and timedelta calculations
===============================
`diff_to_start_of_day(t)`_
    - return timedelta to start of day
`diff_to_end_of_day(t)`_
    - return timedelta to end of day

Converting
==========
`to_date(d, today=None)`_
    - convert d into datetime.date
`to_datetime(t, today=None)`_
    - convert t into datetime.datetime
`to_timestamp(t, today=None)`_
    - convert t into Python timestamp
`acm_date(d, today=None)`_
    - convert d into acm date string
`acm_datetime(t, today=None)`_
    - convert t into acm date-time string
`ael_date(d, today=None)`_
    - convert d into ael.ael_date object
`date_from_symbolic_date(symbol, today=None)`_
    - extract date relative to today from symbolic date string (e.g., 'TODAY')
`date_from_ael_date(d)`_
    - convert ael_date date into datetime.date
`date_from_string(string, today=None, **kwargs)`_
    - parse string for date, return datetime.date
`datetime_from_string(string, today=None, **kwargs)`_
    - parse string for datetime, return datetime.datetime
`strp2dyear(s, century=DEFAULT_CENTURY, century_switch=DEFAULT_CENTURY_SWITCH)`_
    - parse two-digit number string as year number
      ('00' -> 2000, ..., '68' -> 2068, '69' -> 1969, ... '99' -> 1999)
`to_struct_time(t)`_
    - convert list or tuple to time.struct_time

`parse_date_from_string(string, today=None, date_patterns=None)`_
    - parse (date, rest) pair from string
`parse_datetime_from_string(string, today=None, date_patterns=None, time_patterns=None)`_
    - parse (datetime, rest) pair from string
`parse_time_from_string(string, time_patterns=None)`_
    - parse (time, rest) pair from string

dbsql
=====
`dbsql_strftime(t, today=None, format=DBSQL_DATETIME_FORMAT)`_
    - convert t into timestamp and format for dbsql
`dbsql_to_timestamp(string, format=DBSQL_DATETIME_FORMAT)`_
    - convert dbsql time string to timestamp
`dbsql_to_datetime(string, format=DBSQL_DATETIME_FORMAT)`_
    - convert dbsql time string to datetime.datetime

Formatting
==========
`strftimedelta(format, delta = None)`_
    - format a datetime.timedelta object
'''

import calendar
import copy
import datetime
import re
import sys
import time

try:
    import ael
    import acm
    import at_type_helpers
except ImportError:
    pass

# ----------------------------------------------------------------------------
# Export
# ----------------------------------------------------------------------------

__all__ = [
    'dateperiod', 
    'date_today',
    'add_years', 
    'add_months', 
    'add_days', 
    'add_delta',
    'to_date', 
    'ael_date', 
    'acm_date',
    'to_datetime', 
    'to_timestamp', 
    'acm_datetime',
    'dbsql_strftime', 
    'dbsql_to_timestamp', 
    'dbsql_to_datetime',
    'strftimedelta', 
    'diff_to_start_of_day', 
    'diff_to_end_of_day',
    'acm_calendar',
    'is_banking_day', 
    'is_non_banking_day', 
    'bankingday_timediff',
    'date_from_symbolic_date',
    'date_from_ael_date',
    'date_from_string',
    'datetime_from_string',
    'to_struct_time',
    'parse_date_from_string',
    'parse_datetime_from_string',
    'parse_time_from_string',
    'strp2dyear'
]

# ----------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------

# Date output formats

DATE_ISO = '%Y-%m-%d'
DATETIME_ISO = '%Y-%m-%d %H:%M:%S'

DBSQL_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
ASQL_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
DEFAULT_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

# Date parse constants

DEFAULT_YEAR = 1900
DEFAULT_MONTH = 1
DEFAULT_DAY = 1

DEFAULT_CENTURY = 1900
DEFAULT_CENTURY_SWITCH = 69

#BIGDATE = datetime.date(*datetime.date.max.timetuple()[:3])
#SMALLDATE = datetime.date(*datetime.date.min.timetuple()[:3])

ACCEPT_DATE_ISO = 1
ACCEPT_DATE_DIN5008 = 2
ACCEPT_DATE_PACKED = 4
ACCEPT_DATE_QUICK = 8
ACCEPT_DATE_UK = 16
ACCEPT_DATE_USA = 32

DATE_ISO_RE = re.compile(r'(?P<year>\d{4})-(?P<month>\d\d)-(?P<day>\d\d)')
DATE_DIN5008_RE = re.compile(
    r'(?P<day>\d{1,2})\.(?P<month>\d{1,2})\.(?P<year>\d{1,4})')
DATE_PACKED_RE = re.compile(r'(?P<year>\d{4})(?P<month>\d\d)(?P<day>\d\d)')
DATE_QUICK_RE = re.compile(r'(?P<year>\d{2})(?P<month>\d\d)(?P<day>\d\d)')

DEFAULT_DATE_PATTERNS = (
    DATE_ISO_RE,
    DATE_DIN5008_RE,
    #DATE_PACKED_RE,
)

# ----------------------------------------------------------------------------
# date period pattern

DATE_PERIOD_RE = re.compile(r'(?P<num>[-+]?\d+)(?P<period>[dwmy])')



# ----------------------------------------------------------------------------
# time pattern

DATETIME_ISO_RE = re.compile(r'(?P<year>\d{4})-(?P<month>\d\d)-(?P<day>\d\d)'
                             r'T'
                             r'(?P<hour>\d\d):(?P<minute>\d\d)'
                             r':(?P<second>\d\d)'
                             r'(\.(?P<microsecond>\d+))?'
                             r'((?P<tz_hour>[+-]\d\d):(?P<tz_minute>\d\d))?')

TIME_ISO_RE = re.compile(r'(?P<hour>\d\d):(?P<minute>\d\d):(?P<second>\d\d)'
                         r'(\.(?P<microsecond>\d+))?'
                         r'((?P<tz_hour>[+-]\d\d):(?P<tz_minute>\d\d))?')
TIME_HHMMSS_RE = re.compile(r'(?P<hour>\d\d):(?P<minute>\d\d):(?P<second>\d\d)')
TIME_HHMM_RE = re.compile(r'(?P<hour>\d\d):(?P<minute>\d\d)')

DEFAULT_TIME_PATTERNS = (
    TIME_ISO_RE,
    TIME_HHMMSS_RE,
    TIME_HHMM_RE
)

# ----------------------------------------------------------------------------
# symbolic dates

SYMBOLIC_DATE_NAME_RE = re.compile(r'([A-Za-z]+)')

SYMBOLIC_DATE_NAMES = frozenset([
    'BIGDATE',
    'SMALLDATE',
    'TODAY',
    'TOMORROW',
    'YESTERDAY',
    'TWODAYSAGO',
    'FIRSTDAYOFYEAR',
    'LASTDAYOFYEAR',
    'FIRSTDAYOFQUARTER',
    'LASTDAYOFQUARTER',
    'FIRSTDAYOFMONTH',
    'LASTDAYOFMONTH',
    'FIRSTDAYOFWEEK',
    'LASTDAYOFWEEK',
    'INCEPTION',
    'PREVBUSDAY'
])

_offset_symbolic_dates = {
    'TODAY': datetime.timedelta(),
    'YESTERDAY': datetime.timedelta(days=-1),
    'TWODAYSAGO': datetime.timedelta(days=-2),
    'TOMORROW': datetime.timedelta(days=1),
}

# ----------------------------------------------------------------------------
# Local Constants
# ----------------------------------------------------------------------------
# Number of days per month (except for February in leap years)
_MDAYS = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# ----------------------------------------------------------------------------
# dateperiod class
# ----------------------------------------------------------------------------

class dateperiod(object):
    """
    A dateperiod object represents a period of days, months and years.

    The actual duration of the period in days is not fixed and depends on the
    date the period is applied to. Adding a period of one month to 2011-02-01
    results in 2011-03-01, i.e., a delta of 28 days. But adding the same
    duration to 2011-07-01 will result in a delta of 31 days. See total_days()
    for an approximated length of the period in days.

    >>> feb = datetime.date(2011, 2, 1)
    >>> jul = datetime.date(2011, 7, 1)
    >>> period = dateperiod(months=1)
    >>> ((feb + period) - feb).days
    28
    >>> ((jul + period) - jul).days
    31
    """

    # average length of a year in days in the proleptic gregorian calendar
    year_length = 365.2425

    # number of months in a year
    months_in_year = 12.0


    def __init__(self, days=0, months=0, years=0, weeks=0):
        """
        >>> dateperiod()
        dateperiod()
        >>> dateperiod(weeks=1)
        dateperiod(days=7)
        """
        self._days = days + weeks * 7
        self._months = months
        self._years = years

    @property
    def days(self):
        """
        Number of days in this dateperiod (read-only)

        >>> dateperiod(weeks=2, days=-4).days
        10
        """
        return self._days

    @property
    def months(self):
        """
        Number of months in this dateperiod (read-only)

        >>> dateperiod(weeks=2, days=-4).months
        0
        """
        return self._months

    @property
    def years(self):
        """
        Number of years in this dateperiod (read-only)

        >>> dateperiod(weeks=2, days=-4, years=-1).years
        -1
        """
        return self._years

    @classmethod
    def fromstring(cls, period_string, require_initial_sign=False):
        r"""
        Return date parsed from period_string.

        Initial or trailing spaces in period_string are ignored.

        >>> dateperiod.fromstring('1w')
        dateperiod(days=7)
        >>> dateperiod.fromstring('1w', require_initial_sign=True)
        Traceback (most recent call last):
            ...
        ValueError: Invalid date period period_string '1w'
        >>> dateperiod.fromstring('  1w \r\n')
        dateperiod(days=7)
        >>> dateperiod.fromstring('+1w', require_initial_sign=True)
        dateperiod(days=7)
        >>> dateperiod.fromstring('x')
        Traceback (most recent call last):
            ...
        ValueError: Invalid date period period_string 'x'
        >>> dateperiod.fromstring('-1m+2d')
        dateperiod(days=2, months=-1)
        >>> dateperiod.fromstring('-1m2d')
        dateperiod(days=-2, months=-1)
        """
        s = period_string.strip()
        (period, rest) = cls.parse_string(
            s, require_initial_sign=require_initial_sign)
        if period and not rest:
            return period
        else:
            raise ValueError('Invalid date period period_string %r' % period_string)

    @classmethod
    def parse_string(cls, period_string, require_initial_sign=False):
        """
        Parse date-period string

        >>> dateperiod.parse_string('1w ')
        (dateperiod(days=7), ' ')
        >>> dateperiod.parse_string('1m')
        (dateperiod(months=1), '')
        >>> dateperiod.parse_string('+1m')
        (dateperiod(months=1), '')
        >>> dateperiod.parse_string('1m', require_initial_sign=True)
        (None, '1m')
        >>> dateperiod.parse_string('+1m', require_initial_sign=True)
        (dateperiod(months=1), '')
        >>> dateperiod.parse_string('1y1m')[0]
        dateperiod(months=1, years=1)
        >>> dateperiod.parse_string('1y1m2y-1y 00:00')
        (dateperiod(months=1, years=2), ' 00:00')
        >>> dateperiod.parse_string('x')
        (None, 'x')
        """
        # initialize processing
        s = period_string
        days, months, years = (0, 0, 0)
        # initialize first match
        m = DATE_PERIOD_RE.match(s.lower())
        if not m:
            # no match at all in string
            return (None, period_string)
        elif require_initial_sign and period_string[:1] not in ('-', '+'):
            # match, but string does not start with sign character
            return (None, period_string)
        # loop as long as we match something
        last_sign = '+'
        while m:
            s = s[m.end():]
            num_s = m.group('num')
            if num_s[0] not in ('-', '+'):
                num_s = last_sign + num_s
            else:
                last_sign = num_s[0]
            num = int(num_s)
            period = m.group('period')
            if period == 'd':
                days += num
            elif period == 'w':
                days += 7 * num
            elif period == 'm':
                months += num
            elif period == 'y':
                years += num
            m = DATE_PERIOD_RE.match(s.lower())
        return (cls(days=days, months=months, years=years), s)

    def __eq__(self, other):
        """
        >>> dateperiod() == dateperiod()
        True
        >>> dateperiod(weeks=2, days=-4) == dateperiod(days=10)
        True
        >>> dateperiod(days=1, years=1) == dateperiod(days=1, months=2)
        False
        """
        if isinstance(other, dateperiod):
            return vars(self) == vars(other)
        else:
            return NotImplemented

    def __ne__(self, other):
        """
        >>> dateperiod() != dateperiod()
        False
        >>> dateperiod(weeks=2, days=-4) != dateperiod(days=10)
        False
        >>> dateperiod(days=1, years=1) != dateperiod(days=1, months=2)
        True
        """
        return not self.__eq__(other)

    def total_days(self):
        """
        Return approximate number of days covered by the dateperiod object

        (see http://bugs.python.org/issue1580, closed in Python 3.1 and
        http://docs.python.org/release/3.1.3/whatsnew/3.1.html#other-language-changes
        for some comments on why we have to be extra careful about the floating
        point numbers in the doctests)

        >>> '%.12g' % dateperiod(years=1).total_days()
        '365.2425'
        >>> '%.12g' % dateperiod(months=1).total_days()
        '30.436875'
        >>> '%.12g' % dateperiod(days=4, months=1, years=1).total_days()
        '399.679375'

        Note that the return value is not an accurate indicator of how many
        days a date is shifted by adding the delta:

        >>> delta = dateperiod(months=1)
        >>> '%.12g' % delta.total_days()
        '30.436875'
        >>> d1 = datetime.date(2011, 2, 1)
        >>> d2 = d1 + delta
        >>> d2
        datetime.date(2011, 3, 1)
        >>> td = d2 - d1
        >>> td.days
        28
        """
        y = self.years + self.months / self.months_in_year
        return (y * self.year_length) + self.days

    def __repr__(self):
        """
        >>> dateperiod()
        dateperiod()
        >>> dateperiod(days=34)
        dateperiod(days=34)
        >>> dateperiod(weeks=1, days=3)
        dateperiod(days=10)
        """
        type_name = type(self).__name__
        args = []
        for attr in ('days', 'months', 'years'):
            val = getattr(self, attr, None)
            if val:
                args.append('%s=%r' % (attr, val))
        return '%s(%s)' % (type_name, ', '.join(args))

    def __str__(self):
        """
        >>> str(dateperiod())
        '+0d'
        >>> str(dateperiod(days=34))
        '+34d'
        >>> str(dateperiod(weeks=1, days=3))
        '+10d'
        >>> str(dateperiod(weeks=1, days=3, years=-1, months=-2))
        '+10d-2m-1y'
        >>> str(dateperiod(weeks=1, days=3, years=1, months=2))
        '+10d+2m+1y'
        """
        args = []
        for attr in ('days', 'months', 'years'):
            val = getattr(self, attr, None)
            if val:
                args.append('%+d%s' % (val, attr[0]))
        if args:
            return ''.join(args)
        else:
            return '+0d'

    def __neg__(self):
        """
        Return new "negated" date delta

        Note: The negation works component-wise.

        >>> str(-dateperiod(3, 2, 1))
        '-3d-2m-1y'
        >>> str(-dateperiod(3, -2, 1))
        '-3d+2m-1y'
        """
        return self.__class__(days=-self.days, months=-self.months,
                              years=-self.years)

    def __abs__(self):
        """
        Return new absolute value version of given dateperiod object

        Note: The abs() function works component-wise.

        >>> str(abs(-dateperiod(-3, 2, 1)))
        '+3d+2m+1y'
        """
        return self.__class__(days=abs(self.days), months=abs(self.months),
                              years=abs(self.years))

    def __add__(self, other):
        """
        Return the sum of two periods or the sum of a period and a date 
        >>> dateperiod(days=2) + '2012-12-12'
        datetime.date(2012, 12, 14)
        >>> dateperiod(days=2) + dateperiod(years=-1, days=-3)
        dateperiod(days=-1, years=-1)
        """
        #if 'ael' in sys.modules:
        #    import ael
        #    if isinstance(other, ael.ael_date):
        #        return other.add_delta(self.days, self.months, self.years)
        if isinstance(other, dateperiod):
            return dateperiod(days = self.days + other.days,
                             months = self.months + other.months,
                             years = self.years + other.years,)
        try:
            d = to_date(other)
        except ValueError, e:
            return
        if not d:
            raise NotImplementedError()
        return add_delta(d, days=self.days, months=self.months,
                         years=self.years)

    def __radd__(self, other):
        """
        >>> '2012-12-12' + dateperiod(days=2)
        datetime.date(2012, 12, 14)
        """
        return self.__add__(other)

    def __sub__(self, other):
        """
        >>> dateperiod(days=10) - dateperiod(days=3, months=2)
        dateperiod(days=7, months=-2)
        """
        if isinstance(other, dateperiod):
            return self + (-other)
        else:
            raise NotImplementedError()

    def __rsub__(self, other):
        """
        >>> '2012-12-12' - dateperiod(days=2)
        datetime.date(2012, 12, 10)
        """
        return other + (-self)

# ----------------------------------------------------------------------------
# Calendar functions / date calculation functions
# ----------------------------------------------------------------------------

def date_today():
    """
    .. _`date_today()`:
    
    Return current date as datetime.date object. Uses ael.date_today if
    the ael module is availabe. Otherwise datetime.date.today() is used.

    >>> _ael = ('ael' in sys.modules)
    >>> not _ael or (date_today() == to_date(ael.date_today()))
    True
    >>> _ael or (date_today() == datetime.date.today())
    True
    """
    if 'ael' in sys.modules:
        return datetime.date(*ael.date_today().to_ymd())
    else:
        return datetime.date.today()

def add_years(date_param, years, truncate=False):
    """
    .. _`add_years(date_param, years, truncate=False)`:
    
    add years to date d returning a new datetime.date object

    Raises ValueError if the year of the resulting date is out of range.
    If truncate is True no exception is raised and the resulting date is
    truncated to be between datetime.date.min and datetime.date.max
    (including).

    >>> add_years(datetime.date(1996, 2, 29), 1)
    datetime.date(1997, 2, 28)
    >>> add_years(datetime.date(1997, 2, 28), 1)
    datetime.date(1998, 2, 28)
    """
    date_param = to_date(date_param)
    year = date_param.year + years
    if truncate:
        if year < datetime.MINYEAR:
            return copy.copy(datetime.date.min)
        elif year > datetime.MAXYEAR:
            return copy.copy(datetime.date.max)
    day = min(date_param.day, calendar.monthrange(year, date_param.month)[1])
    return date_param.replace(year=year, day=day)

def add_months(date_param, months, truncate=False):
    """
    .. _`add_months(date_param, months, truncate=False)`:
    
    add months to date date_param returning a new datetime.date object

    Raises ValueError if the resulting date is out of range.
    If truncate is True no exception is raised and the resulting date is
    truncated to be between datetime.date.min and datetime.date.max
    (including).

    >>> add_months(datetime.date(1996, 1, 31), 1)
    datetime.date(1996, 2, 29)
    >>> add_months(datetime.date(1997, 1, 31), 1)
    datetime.date(1997, 2, 28)
    >>> add_months(datetime.date(1997, 1, 31), 130000)
    Traceback (most recent call last):
        ...
    ValueError: year is out of range
    """
    date_param = to_date(date_param)
    (q, r) = divmod(date_param.month + months - 1, 12)
    year = date_param.year + q
    month = r + 1
    if truncate:
        if year < datetime.MINYEAR:
            return copy.copy(datetime.date.min)
        elif year > datetime.MAXYEAR:
            return copy.copy(datetime.date.max)
    day = min(date_param.day, calendar.monthrange(year, month)[1])
    return datetime.date(year=year, month=month, day=day)

def add_days(date_param, days, truncate=False):
    """
    .. _`add_days(date_param, days, truncate=False)`:
    
    add days to date date_param returning a new datetime.date object

    Raises ValueError if the resulting date is out of range.
    If truncate is True no exception is raised and the resulting date is
    truncated to be between datetime.date.min and datetime.date.max
    (including).

    >>> add_days(datetime.date(1996, 1, 31), 1)
    datetime.date(1996, 2, 1)
    >>> add_days(datetime.date(1997, 1, 31), 365)
    datetime.date(1998, 1, 31)
    >>> add_days(datetime.date(1996, 1, 31), 365)
    datetime.date(1997, 1, 30)
    >>> add_days(datetime.date(1997, 1, 31), 1300000)
    datetime.date(5556, 5, 13)
    >>> add_days(datetime.date(1997, 1, 31), 35000000)
    Traceback (most recent call last):
        ...
    ValueError: year is out of range
    """

    date_param = to_date(date_param)
    try:
        date_param = date_param + datetime.timedelta(days=days)
        # in older Python versions (pre 2.6.6) the datetime.date object d from
        # the calculation above can be bogus and out of range
        # (see http://bugs.python.org/issue7150):
        #
        # To protect against this we make an additional manual check:
        if (date_param < datetime.date.min) or (date_param > datetime.date.max):
            raise OverflowError('')
        return date_param
    except OverflowError:
        if truncate:
            if days < 0:
                return copy.copy(datetime.date.min)
            else:
                return copy.copy(datetime.date.max)
        else:
            raise ValueError('year is out of range')

def add_delta(date_param, days=0, months=0, years=0, truncate=False):
    """
    .. _`add_delta(date_param, days=0, months=0, years=0, truncate=False)`:
    
    add days, months, years to date date_param returning a new datetime.date object

    The result is computed by adding first years then months and finally days.

    Raises ValueError if the resulting date is out of range.
    If truncate is True no exception is raised and the resulting date is
    truncated to be between datetime.date.min and datetime.date.max
    (including).

    >>> add_delta(datetime.date(1996, 2, 29), 0, 1, 1)
    datetime.date(1997, 3, 28)
    >>> add_delta(datetime.date(1996, 2, 29), 0, 13, 0)
    datetime.date(1997, 3, 29)
    >>> add_delta(datetime.date(1996, 2, 29), 1, 1, 1)
    datetime.date(1997, 3, 29)
    >>> add_delta(datetime.date(1996, 2, 29), -1, 1, 1)
    datetime.date(1997, 3, 27)
    >>> add_delta(datetime.date(1996, 1, 31), -1, 1, 0)
    datetime.date(1996, 2, 28)
    >>> add_delta(datetime.date(1, 1, 1), -1, 1, 0)
    datetime.date(1, 1, 31)
    >>> add_delta(datetime.date(1, 1, 1), -32, 1, 0)
    Traceback (most recent call last):
        ...
    ValueError: year is out of range
    >>> add_delta(datetime.date(1, 1, 1), -32, 1, 0, truncate=True)
    datetime.date(1, 1, 1)
    >>> add_delta(datetime.date(2, 1, 1), 350000000, 0, -1)
    Traceback (most recent call last):
        ...
    ValueError: year is out of range
    >>> add_delta(datetime.date(2, 1, 1), 350000000, 0, -1, truncate=True)
    datetime.date(9999, 12, 31)
    >>> add_delta(datetime.date(2, 1, 1), 350000000, 0, -2, truncate=True)
    datetime.date(1, 1, 1)
    """
    date_param = to_date(date_param)
    try:
        num = years
        date_param = add_years(date_param, num)
        num = months
        date_param = add_months(date_param, num)
        num = days
        return add_days(date_param, num)
    except (ValueError, OverflowError):
        if truncate:
            if num < 0:
                return copy.copy(datetime.date.min)
            else:
                return copy.copy(datetime.date.max)
        else:
            raise

#----------------------------------------------------------------------------
# date conversion helper functions
#----------------------------------------------------------------------------

def date_from_ael_date(date_param):
    '''
    .. _`date_from_ael_date(date_param)`:
    
    Convert ael.ael_date object to a datetime.date object

    The special dates ael.SMALL_DATE and ael.BIG_DATE are converted to
    datetime.date.min and datetime.date.max, respectively.

    >>> _ael = 'ael' in sys.modules
    >>> dd1 = datetime.date(2001, 2, 3)
    >>> ad1 = ael.date_from_ymd(2001, 2, 3)
    >>> not _ael or date_from_ael_date(ael.SMALL_DATE) == datetime.date.min
    True
    >>> not _ael or date_from_ael_date(ael.BIG_DATE) == datetime.date.max
    True
    >>> not _ael or date_from_ael_date(ad1) == dd1
    True
    '''
    if date_param is None:
        return None
    (yr, _, _) = date_param.to_ymd()
    if (yr < datetime.MINYEAR) or (date_param == ael.SMALL_DATE):
        return datetime.date.min
    elif (yr > datetime.MAXYEAR) or (date_param == ael.BIG_DATE):
        return datetime.date.max
    else:
        return datetime.date(*date_param.to_ymd())

def date_from_symbolic_date(symbol, today=None):
    '''.. _`date_from_symbolic_date(symbol, today=None)`:
    
    Convert symbolic date (TODAY, ...) into datetime.date object

    Returns the datetime.date value associated with the symbolic date string
    relative to today. Matching is case-insensitive. A KeyError is raised
    if the symbolic date symbol is not known.

    The date returned by date_today() is used if today is None.

    The following symbolic name are supported (case-insensitive):

    * BIGDATE  datetime.date.max ('9999-12-31')
    * SMALLDATE  datetime.date.min ('0001-01-01')
    * TODAY  date today
    * TOMORROW  date tomorrow
    * YESTERDAY  date yesterday
    * TWODAYSAGO  date two days ago
    * FIRSTDAYOFYEAR  first day of year
    * LASTDAYOFYEAR  last day of year
    * FIRSTDAYOFQUARTER  first day of quarter
    * LASTDAYOFQUARTER  last day of quarter
    * FIRSTDAYOFMONTH  first day of month
    * LASTDAYOFMONTH  last day of month
    * FIRSTDAYOFWEEK  the Monday coinciding with or immediatly preceding today
    * LASTDAYOFWEEK  the Sunday coinciding with or immediatly following today
    * INCEPTION 01.01.1970
    * PREVBUSDAY the previous business day according to the calendar of the base currency

    **Examples:**
    
    >>> TODAY = date_today()
    >>> one_day = datetime.timedelta(days=1)
    >>> date_from_symbolic_date('TODAY') == TODAY
    True
    >>> date_from_symbolic_date('Yesterday') == TODAY - one_day
    True
    >>> date_from_symbolic_date('TOMORROW') == TODAY + one_day
    True
    >>> date_from_symbolic_date('FIRSTDAYOFYEAR') == \
        TODAY.replace(month=1, day=1)
    True
    >>> date_from_symbolic_date('FIRSTDAYOFMONTH') == TODAY.replace(day=1)
    True
    >>> date_from_symbolic_date('FIRSTDAYOFWEEK') == \
        TODAY - datetime.timedelta(days=TODAY.weekday())
    True
    >>> d = datetime.date(1996, 2, 14)
    >>> date_from_symbolic_date('FIRSTDAYOFWEEK', today=d)
    datetime.date(1996, 2, 12)
    >>> date_from_symbolic_date('LASTDAYOFWEEK', today=d)
    datetime.date(1996, 2, 18)
    >>> date_from_symbolic_date('FIRSTDAYOFQUARTER', today=d)
    datetime.date(1996, 1, 1)
    >>> date_from_symbolic_date('LASTDAYOFQUARTER', today=d)
    datetime.date(1996, 3, 31)
    >>> date_from_symbolic_date('LASTDAYOFYEAR', today=d)
    datetime.date(1996, 12, 31)
    >>> date_from_symbolic_date('FIRSTDAYOFMONTH', today=d)
    datetime.date(1996, 2, 1)
    >>> date_from_symbolic_date('LASTDAYOFMONTH', today=d)
    datetime.date(1996, 2, 29)
    >>> d2 = datetime.date(1997, 2, 14)
    >>> date_from_symbolic_date('LASTDAYOFMONTH', today=d2)
    datetime.date(1997, 2, 28)
    >>> date_from_symbolic_date('INCEPTION')
    datetime.date(1970, 1, 1)
    '''
    
    today = _extract_today(today)
    s = symbol.upper()
    if s in _offset_symbolic_dates:
        d = today + _offset_symbolic_dates[s]
    elif s == 'BIGDATE':
        d = datetime.date.max
    elif s == 'SMALLDATE':
        d = datetime.date.min
    elif s == 'FIRSTDAYOFMONTH':
        d = today.replace(day = 1)
    elif s == 'LASTDAYOFMONTH':
        d = today.replace(day = calendar.monthrange(today.year, today.month)[1])
    elif s == 'FIRSTDAYOFQUARTER':
        m = ((today.month - 1) // 3) * 3 + 1 # first month in quarter
        d = today.replace(month=m, day=1)
    elif s == 'LASTDAYOFQUARTER':
        m = ((today.month - 1) // 3) * 3 + 3 # last month in quarter
        d = today.replace(month=m, day=calendar.monthrange(today.year, m)[1])
    elif s == 'FIRSTDAYOFWEEK':
        d = today - datetime.timedelta(days=today.weekday())
    elif s == 'LASTDAYOFWEEK':
        d = today - datetime.timedelta(days=today.weekday() - 6)
    elif s == 'FIRSTDAYOFYEAR':
        d = today.replace(day=1, month=1)
    elif s == 'LASTDAYOFYEAR':
        d = today.replace(day=31, month=12)
    elif s == 'INCEPTION':
        d = datetime.date(1970, 01, 01)
    elif s == 'PREVBUSDAY':
        mappedValuationParameters = acm.GetFunction('mappedValuationParameters', 0)
        d = mappedValuationParameters().Parameter().AccountingCurrency().Calendar().AdjustBankingDays(today.strftime(DATE_ISO), -1)
        d = to_date(d)
    else:
        raise KeyError(symbol)
    return d

def to_struct_time(time_param):
    """
    .. _`to_struct_time(time_param)`:
    
    Convert time.struct_time, list or tuple to time.struct_time.

    Returns a new time.struct_time record, even if time_param is already such a record.
    Returns None for time_param=None or time_param=() or time_param=[].

    >>> t1 = time.struct_time((2000, 1, 1, 0, 0, 0, 0, 1, -1))
    >>> t1s = ('time.struct_time(tm_year=2000, tm_mon=1, tm_mday=1, '
    ...        'tm_hour=0, tm_min=0, tm_sec=0, tm_wday=0, tm_yday=1, '
    ...        'tm_isdst=-1)')
    >>> to_struct_time((2000, 1, 1)) == t1
    True
    >>> str(to_struct_time((2000, 1, 1))) == str(t1)
    True
    >>> str(to_struct_time((2000, 1, 1))) == t1s
    True
    >>> lt = time.localtime()
    >>> id(to_struct_time(lt)) == id(lt)
    False
    """
    if not time_param:
        return None
    elif isinstance(time_param, time.struct_time):
        return time.struct_time(time_param)
    else:
        defaults = (1900, 1, 1, 0, 0, 0, 0, 1, -1)
        time_param = list(time_param[:9])
        time_param.extend(defaults[len(time_param):])
        return time.struct_time(time_param)

# ----------------------------------------------------------------------------
# date parsing helper functions
# ----------------------------------------------------------------------------

def strp2dyear(year_string, century=DEFAULT_CENTURY,
               century_switch=DEFAULT_CENTURY_SWITCH):
    """
    .. _`strp2dyear(s, century=DEFAULT_CENTURY, century_switch=DEFAULT_CENTURY_SWITCH)`:
    
    Return year number for two-digit year string.

    >>> strp2dyear('68')
    2068
    >>> strp2dyear('69')
    1969
    >>> strp2dyear('68', century=1700)
    1868
    >>> strp2dyear('69', century=1700)
    1769
    >>> strp2dyear('68', century=1700, century_switch=70)
    1868
    >>> strp2dyear('69', century=1700, century_switch=70)
    1869
    >>> strp2dyear('70', century=1700, century_switch=70)
    1770
    """
    year = int(year_string, 10)
    if year < century_switch:
        year += 100
    year += century
    return year

# ----------------------------------------------------------------------------
# Low level date/time parsing
# ----------------------------------------------------------------------------

def _extract_today(today):
    """
    .. _`_extract_today(today)`:
    
    Extract datetime.date from today

    Returns the result of date_today() if today is None.

    >>> _extract_today(None) == date_today()
    True
    >>> d1 = datetime.date(2001, 2, 3)
    >>> _ael = 'ael' in sys.modules
    >>> not _ael or _extract_today(ael.date_today()) == date_today()
    True
    >>> not _ael or _extract_today(ael.date_from_string('2001-02-03')) == d1
    True
    """
    if today:
        if 'ael' in sys.modules:
            if isinstance(today, ael.ael_date):
                return date_from_ael_date(today)
        return today
    else:
        return date_today()

def _parse_symbolic_date_from_string(date_symbol, today=None):
    """
    .. _`_parse_symbolic_date_from_string(date_symbol, today=None)`:
    
    Scan for a symbolic date (e.g., 'TODAY') at the beginning of date_symbol

    The input date_symbol must not be None and is not stripped of whitespace
    characters.

    Returns a pair (date, rest) with date being the value of the scanned
    date as a datetime.date object and rest the part of the string not
    consumed. Returns None as the date part if no known symbolic string
    was found. The returned date value is relative to today which must be a
    datetime.date object.

    >>> d = datetime.date(2012, 12, 12)
    >>> _parse_symbolic_date_from_string('TOday', today=d)
    (datetime.date(2012, 12, 12), '')
    >>> _parse_symbolic_date_from_string('TOdaz', today=d)
    (None, 'TOdaz')
    """
    m = SYMBOLIC_DATE_NAME_RE.match(date_symbol)
    if m:
        symb = m.group(1).upper()
        if symb not in SYMBOLIC_DATE_NAMES:
            return (None, date_symbol)
        else:
            return (date_from_symbolic_date(symb, today=today),
                    date_symbol[m.end():])
    else:
        return (None, date_symbol)

def _parse_absolute_date(date_string, two_digit_year_func=None,
                         date_patterns=None):
    """
    .. _`_parse_absolute_date(string, two_digit_year_func=None, date_patterns=None)`:
    
    Internal function parsing an absolute date. The date can be in any of the
    following formats:

      ISO Format 'YYYY-MM-DD'
      DIN 5008 conform Format 'DD.MM.YYYY' where day and month can be single-digit
          numbers and the year can be a two or four digit number
    """
    date_patterns = date_patterns or DEFAULT_DATE_PATTERNS
    for regex in date_patterns:
        m = regex.match(date_string)
        if m:
            year = m.group('year')
            if len(year) in (1, 2):
                if two_digit_year_func:
                    year = two_digit_year_func(year)
                else:
                    year = strp2dyear(year)
            else:
                year = int(year)
            month = int(m.group('month'))
            day = int(m.group('day'))
            return (datetime.date(year, month, day), date_string[m.end():])
    return (None, date_string)

def parse_date_from_string(date_string, today=None,
                           date_patterns=None):
    """
    .. _`parse_date_from_string(date_string, today=None, date_patterns=None)`:
    
    >>> parse_date_from_string(None)
    (None, None)
    >>> parse_date_from_string('')
    (None, '')
    >>> parse_date_from_string('foo')
    (None, 'foo')
    >>> parse_date_from_string('2012-12-12')
    (datetime.date(2012, 12, 12), '')
    >>> parse_date_from_string('2012-12-12foo')
    (datetime.date(2012, 12, 12), 'foo')
    >>> parse_date_from_string('2012-12-12+1d')
    (datetime.date(2012, 12, 13), '')
    >>> parse_date_from_string('2012-12-12 1d')
    (datetime.date(2012, 12, 12), ' 1d')
    >>> parse_date_from_string('2012-12-12 \t+1d  12:00')
    (datetime.date(2012, 12, 13), '  12:00')
    >>> d = datetime.date(2012, 12, 12)
    >>> parse_date_from_string('1y', d)
    (datetime.date(2013, 12, 12), '')
    """
    if not date_string:
        return (None, date_string)
    # (A) parse symbolic date or absolute date
    (d, rest) = _parse_symbolic_date_from_string(date_string, today=today)
    if not d:
        (d, rest) = _parse_absolute_date(date_string, date_patterns=date_patterns)
    # (B) parse optional date period
    s2 = rest.lstrip()
    if s2:
        (period, s2) = dateperiod.parse_string(s2,
                                               require_initial_sign=bool(d))
        if period:
            d = (d or today) + period
            rest = s2
    # (C) return
    return (d, rest)

def parse_time_from_string(time_string, time_patterns=None):
    """
    .. _`parse_time_from_string(time_string, time_patterns=None)`:
    
    >>> parse_time_from_string('13:14:09.678+02:30')
    (datetime.time(13, 14, 9, 678), '')
    """
    if not time_string:
        return (None, time_string)
    time_patterns = time_patterns or DEFAULT_TIME_PATTERNS
    for regex in time_patterns:
        m = regex.match(time_string)
        if m:
            d = m.groupdict()
            hour = int(d.get('hour', 0))
            minute = int(d.get('minute', 0))
            second = int(d.get('second', 0))
            microsecond = int(d.get('microsecond', None) or 0)
            try:
                t = datetime.time(hour=hour, minute=minute, second=second,
                                  microsecond=microsecond)
                return (t, time_string[m.end():])
            except ValueError:
                pass
    return (None, time_string)

def parse_datetime_from_string(datetime_string, today=None,
                               date_patterns=None,
                               time_patterns=None):
    """
    .. _`parse_datetime_from_string(datetime_string, today=None, date_patterns=None, time_patterns=None)`:
    
    Scan for a datetime at the beginning of string.

    Returns a pair (datetime, rest) with datetime being the scanned
    datetime as a datetime.datetime object and rest the part of the
    string not consumed. returns None as the datetime part if string
    is None or no datetime was detected at the beginning of the string.

    >>> parse_datetime_from_string('2012-12-12 12:12:12')
    (datetime.datetime(2012, 12, 12, 12, 12, 12), '')
    >>> parse_datetime_from_string('2013-12-11T14:15:16')
    (datetime.datetime(2013, 12, 11, 14, 15, 16), '')
    >>> parse_datetime_from_string('2012-12-12 12:12')
    (datetime.datetime(2012, 12, 12, 12, 12), '')
    >>> parse_datetime_from_string('2012-12-12 12:12 :12')
    (datetime.datetime(2012, 12, 12, 12, 12), ' :12')
    >>> parse_datetime_from_string(' 2012-12-12 12:12 :12')
    (None, ' 2012-12-12 12:12 :12')
    >>> parse_datetime_from_string('2012-12-12')
    (datetime.datetime(2012, 12, 12, 0, 0), '')
    >>> parse_datetime_from_string('12:12', datetime.date(1911, 11, 11))
    (datetime.datetime(1911, 11, 11, 12, 12), '')
    """
    if not datetime_string:
        return (None, datetime_string)
    # check for special string 'NOW'
    if datetime_string.upper().startswith('NOW'):
        return (datetime.datetime.now(), datetime_string[3:])
    # check for datetime in ISO format
    if DATETIME_ISO_RE.match(datetime_string):
        pos = datetime_string.find('T')
        datetime_string = '%s %s' % (datetime_string[:pos], datetime_string[pos+1:])
    # start regular datetime parsing
    today = _extract_today(today)
    d, rest = parse_date_from_string(datetime_string, today=today,
                                       date_patterns=date_patterns)
    if d:
        if rest and not rest[0].isspace():
            return (None, rest)
        rest = rest.lstrip()
    t, rest = parse_time_from_string(rest, time_patterns=time_patterns)
    if not d and not t:
        return (None, datetime_string)
    d = d or today
    t = t or datetime.time(0)
    return (datetime.datetime.combine(d, t), rest)

# ----------------------------------------------------------------------------
# Mid-level date/time parsing
# ----------------------------------------------------------------------------

def date_from_string(date_string, today=None, **kwargs):
    '''
    .. _`date_from_string(date_string, today=None, **kwargs)`:
    
    Extract and return date from date_string

    **Examples:**

    >>> today = date_today()
    >>> yesterday = today + datetime.timedelta(days = -1)
    >>> date_from_string(' Yesterday ') == yesterday
    True
    >>> date_from_string('1.3.1980')
    datetime.date(1980, 3, 1)
    >>> date_from_string('2.4.69')
    datetime.date(1969, 4, 2)
    >>> date_from_string('  2012-07-31 ')
    datetime.date(2012, 7, 31)
    >>> date_from_string(' -0d  ') == today
    True
    >>> date_from_string('-1d') == yesterday
    True
    >>> date_from_string('300d') == today + datetime.timedelta(days = 300)
    True
    >>> d = datetime.date(1981, 3, 4)
    >>> date_from_string('-2y+2m', today = d)
    datetime.date(1979, 5, 4)
    >>> date_from_string('-4000y') == datetime.date.min
    Traceback (most recent call last):
        ...
    ValueError: year is out of range
    >>> date_from_string('5000000d')
    Traceback (most recent call last):
        ...
    ValueError: year is out of range
    >>> date_from_string('-5000000d')
    Traceback (most recent call last):
        ...
    ValueError: year is out of range
    >>> date_from_string('-1m', today = datetime.date(1996, 3, 31))
    datetime.date(1996, 2, 29)
    >>> date_from_string('-1y', today = datetime.date(1996, 2, 29))
    datetime.date(1995, 2, 28)
    >>> date_from_string('+4y', today = datetime.date(1996, 2, 29))
    datetime.date(2000, 2, 29)
    >>> date_from_string('+1m+1y', today = datetime.date(1996, 2, 29))
    datetime.date(1997, 3, 28)
    >>> date_from_string('+13m', today = datetime.date(1996, 2, 29))
    datetime.date(1997, 3, 29)
    >>> date_from_string('+1d+1m+1y', today = datetime.date(1996, 2, 29))
    datetime.date(1997, 3, 29)
    >>> date_from_string('-1d+1m+1y', today = datetime.date(1996, 2, 29))
    datetime.date(1997, 3, 27)
    >>> date_from_string('-1d+1m', today = datetime.date(1996, 1, 31))
    datetime.date(1996, 2, 28)
    >>> date_from_string('FIRSTDAYOFYEAR+1y-1d', today = d)
    datetime.date(1981, 12, 31)
    >>> date_from_string('FIRSTDAYOFMONTH+1m-1d', today = d)
    datetime.date(1981, 3, 31)
    >>> date_from_string('FIRSTDAYOFMONTH+1M-1D', today = d)
    datetime.date(1981, 3, 31)
    >>> date_from_string(None) is None
    True
    >>> date_from_string('') is None
    True
    >>> date_from_string('1996-02-29+1d+1m+1y')
    datetime.date(1997, 3, 29)
    
    '''
    if date_string is None or not date_string.strip():
        return None

    (date, rest) = parse_date_from_string(date_string.strip(),
                                          today=_extract_today(today),
                                          **kwargs)
    if date and not rest:
        return date
    else:
        # no date found or some rest found => raise exception
        raise ValueError('invalid date string: %r' % date_string)

def datetime_from_string(datetime_string, today=None, **kwargs):
    """
    .. _`datetime_from_string(datetime_string, today=None, **kwargs)`:
    
    Parse datetime_string for a valid date and/or time and return corresponding
    datetime.datetime object. Returns None if string is None or contains only
    whitespace characters. The date part defaults to today (or date_today()
    if today is None) and the time part defaults to 00:00:00.

    Returns datetime.datetime.now() if the datetime_string is 'NOW' after stripping and
    conversion to uppercase.

    >>> datetime_from_string(None) is None
    True
    >>> datetime_from_string('   ') is None
    True
    >>> now_delta = abs(datetime_from_string('now') - datetime.datetime.now())
    >>> now_delta < datetime.timedelta(0, 0, 100)
    True
    >>> d = datetime.date(1996, 3, 14)
    >>> datetime_from_string('TODAY', today = d)
    datetime.datetime(1996, 3, 14, 0, 0)
    >>> datetime_from_string('today', today = d)
    datetime.datetime(1996, 3, 14, 0, 0)
    >>> datetime_from_string('TODAz', today = d)
    Traceback (most recent call last):
        ...
    ValueError: invalid datetime datetime_string: 'TODAz'
    >>> datetime_from_string('TODAY 12:20:40', today = datetime.date(1, 1, 1))
    datetime.datetime(1, 1, 1, 12, 20, 40)
    >>> datetime_from_string('12:20:40', today = datetime.date(1981, 1, 1))
    datetime.datetime(1981, 1, 1, 12, 20, 40)
    >>> datetime_from_string('12:20', today = d)
    datetime.datetime(1996, 3, 14, 12, 20)
    >>> datetime_from_string('12:70', today = d)
    Traceback (most recent call last):
        ...
    ValueError: invalid datetime datetime_string: '12:70'
    >>> datetime_from_string('-14d 12:20', today = d)
    datetime.datetime(1996, 2, 29, 12, 20)
    >>> datetime_from_string('FIRSTDAYOFMONTH-3d 12:20', today = d)
    datetime.datetime(1996, 2, 27, 12, 20)
    >>> datetime_from_string('FIRSTDAYOFMONTH -3d 12:20', today = d)
    datetime.datetime(1996, 2, 27, 12, 20)
    >>> one_sec = datetime.timedelta(seconds=1)
    >>> datetime_from_string('NOW') - datetime.datetime.now() < one_sec
    True
    """

    s = (datetime_string or '').strip()
    if not s:
        return None
    (dt, rest) = parse_datetime_from_string(s, today=_extract_today(today),
                                            **kwargs)
    if dt and not rest:
        return dt
    else:
        raise ValueError('invalid datetime datetime_string: %r' % datetime_string)


# ----------------------------------------------------------------------------
# High-level date/time parsing and conversion functions
# ----------------------------------------------------------------------------

def to_date(date_param, today=None):
    """
    .. _`to_date(date_param, today=None)`:
    
    Convert date_param to a datetime.date

    Returns datetime.date.min for ael.SMALL_DATE and datetime.date.max for
    ael.BIG_DATE.

    >>> to_date('1970-01-01')
    datetime.date(1970, 1, 1)
    >>> to_date('1.1.1970')
    datetime.date(1970, 1, 1)
    >>> to_date(datetime.datetime(1971, 2, 3, 4, 5, 6))
    datetime.date(1971, 2, 3)
    >>> to_date(350002800) == datetime.date.fromtimestamp(350002800)
    True
    >>> d1 = datetime.date(1984, 12, 30)
    >>> if 'ael' in sys.modules:
    ...     to_date(ael.date_from_ymd(1984, 12, 30)) == d1
    ... else:
    ...     True
    True
    >>> to_date('TODAY', today = d1) == d1
    True
    >>> to_date('TOMORROW', today = d1) == add_days(d1, 1)
    True
    >>> id(to_date(d1)) == id(d1)
    False
    >>> to_date((1921,))
    datetime.date(1921, 1, 1)
    >>> to_date([1921, 2, 5])
    datetime.date(1921, 2, 5)
    >>> to_date(time.struct_time((2000, 1, 3, 0, 0, 0, 0, 3, -1)))
    datetime.date(2000, 1, 3)
    >>> to_date('LASTDAYOFMONTH', datetime.date(2012, 1, 20))
    datetime.date(2012, 1, 31)
    >>> to_date('LASTDAYOFMONTH+1m', datetime.date(2012, 1, 20))
    datetime.date(2012, 2, 29)
    >>> to_date('TODAY', datetime.date(2012, 1, 20))
    datetime.date(2012, 1, 20)
    >>> to_date('TODAY+1m', datetime.date(2012, 1, 20))
    datetime.date(2012, 2, 20)
    >>> to_date('\t') is None
    True
    >>> to_date(None) is None
    True
    >>> if 'ael' in sys.modules:
    ...     import ael
    ...     to_date(ael.date_from_string('9999-12-31')) == datetime.date.max
    ... else: True
    True
    >>> _ael = 'ael' in sys.modules
    >>> not _ael or to_date(ael.SMALL_DATE) == datetime.date.min
    True
    >>> not _ael or to_date(ael.BIG_DATE) == datetime.date.max
    True
    """
    if 'ael' in sys.modules:
        if isinstance(date_param, ael.ael_date):
            return date_from_ael_date(date_param)
    if isinstance(date_param, basestring):
        return date_from_string(date_param, today=today)
    elif isinstance(date_param, (int, long, float)):
        return datetime.date.fromtimestamp(date_param)
    elif isinstance(date_param, datetime.datetime):
        return date_param.date()
    elif isinstance(date_param, datetime.date):
        return copy.copy(date_param)
    elif date_param is None:
        return None
    elif isinstance(date_param, (time.struct_time, list, tuple)):
        return datetime.date(*(to_struct_time(date_param)[:3]))
    else:
        raise ValueError('Parameter %r is of unknown type' % date_param)

def ael_date(date_param, today=None):
    """
    .. _`ael_date(date_param, today=None)`:
    
    Convert date_param to an AEL date object.

    The date parameter date_param can be in any format accepted by to_date().
    The return value is an ael.ael_date object. The funtion will raise an
    ImportError if the ael module can not be loaded.
    The dates datetime.date.min and datetime.date.max are converted to
    ael.SMALL_DATE and ael.BIG_DATE, respectively.

    >>> _ael = 'ael' in sys.modules
    >>> def _s(d):
    ...     return d.to_string(ael.DATE_ISO)
    >>> not _ael or _s(ael_date(datetime.date(1999, 9, 9))) == '1999-09-09'
    True
    >>> not _ael or _s(ael_date('1999-09-09')) == '1999-09-09'
    True
    >>> not _ael or _s(ael_date('9.9.1999')) == '1999-09-09'
    True
    >>> not _ael or ael_date('') is None
    True
    >>> not _ael or ael_date(None) is None
    True
    >>> not _ael or ael_date(datetime.date.min) == ael.SMALL_DATE
    True
    >>> not _ael or ael_date(datetime.date.max) == ael.BIG_DATE
    True
    >>> if _ael: type(ael_date('9.9.1999')) == ael.ael_date
    ... else: True
    True
    """

    if not date_param:
        return None
    else:
        date_param = to_date(date_param, today=today)
        if date_param == datetime.date.min:
            return ael.SMALL_DATE
        elif date_param == datetime.date.max:
            return ael.BIG_DATE
        else:
            return ael.date_from_ymd(date_param.year, date_param.month, date_param.day)

def acm_date(date_param, today=None):
    """
    .. _`acm_date(date_param, today=None)`:
    
    Convert date_param to an ACM usable date string

    The date parameter date_param can be in any format accepted by to_date().
    The return value is a string in format '%Y-%m-%d'.

    >>> acm_date(datetime.date(1999, 9, 9))
    '1999-09-09'
    >>> acm_date('1999-09-09')
    '1999-09-09'
    >>> acm_date('9.9.1999')
    '1999-09-09'
    >>> acm_date('') is None
    True
    >>> acm_date('  \t') is None
    True
    >>> acm_date(None) is None
    True
    >>> acm_date('TODAY', datetime.date(1984, 12, 30))
    '1984-12-30'
    >>> acm_date('TOMORROW', datetime.date(2000, 2, 28))
    '2000-02-29'
    >>> acm_date('TOMORROW', datetime.date(2001, 2, 28))
    '2001-03-01'
    """
    date_param = to_date(date_param, today=today)
    if not date_param:
        return None
    else:
        return date_param.strftime('%Y-%m-%d')

def to_datetime(datetime_param, today=None):
    """
    .. _`to_datetime(datetime_param, today=None)`:
    
    Return datetime.datetime object for date/time datetime_param

    >>> to_datetime(0) - datetime.datetime.fromtimestamp(0)
    datetime.timedelta(0)
    >>> to_datetime(datetime.datetime(1971, 2, 3, 4, 5, 6))
    datetime.datetime(1971, 2, 3, 4, 5, 6)
    >>> d1 = datetime.date(2003, 10, 1)
    >>> dt1 = datetime.datetime(2003, 9, 30, 12, 13)
    >>> id(to_datetime(dt1)) == id(dt1)
    False
    >>> to_datetime('YESTERDAY 12:13', today = d1) == dt1
    True
    >>> to_datetime('30.9.2003 12:13:00') == dt1
    True
    >>> to_datetime((2003, 9, 30, 12, 13)) == dt1
    True
    >>> to_datetime([2003, 9, 30, 12, 13]) == dt1
    True
    >>> to_datetime('2003-10-01 00:00:00') == to_datetime(d1)
    True
    >>> to_datetime('TOMORROW', datetime.date(2001, 2, 28))
    datetime.datetime(2001, 3, 1, 0, 0)
    >>> d2 = datetime.date(2012, 01, 20)
    >>> to_datetime('TODAY+2d+2m 12:00:00', today=d2)
    datetime.datetime(2012, 3, 22, 12, 0)
    >>> to_datetime(None) is None
    True
    >>> to_datetime('  ') is None
    True
    >>> to_datetime('InceptIon')
    datetime.datetime(1970, 1, 1, 0, 0)
    """
    if 'ael' in sys.modules:
        if isinstance(datetime_param, ael.ael_date):
            return datetime.datetime.combine(date_from_ael_date(datetime_param),
                                             datetime.time(0, 0))
    if isinstance(datetime_param, basestring):
        return datetime_from_string(datetime_param, today=today)
    elif isinstance(datetime_param, (int, long, float)):
        return datetime.datetime.fromtimestamp(datetime_param)
    elif isinstance(datetime_param, datetime.datetime):
        return copy.copy(datetime_param)
    elif isinstance(datetime_param, datetime.date):
        return datetime.datetime.combine(datetime_param, datetime.time(0, 0))
    elif isinstance(datetime_param, (time.struct_time, list, tuple)):
        return datetime.datetime.fromtimestamp(time.mktime(to_struct_time(datetime_param)))
    elif datetime_param is None:
        return None
    else:
        raise ValueError('Parameter datetime_param=%r is of unknown type' % datetime_param)

def acm_datetime(datetime_param, today=None):
    """
    .. _`acm_datetime(datetime_param, today=None)`:
    
    Convert datetime_param to an ACM date-and-time string

    The date-time parameter datetime_param can be in any format accepted by to_datetime().
    The return value is a string in format '%Y-%m-%d %H:%M:%S'.

    >>> acm_datetime(datetime.date(1999, 9, 9))
    '1999-09-09 00:00:00'
    >>> acm_datetime(datetime.datetime(1999, 9, 9, 1, 2, 3))
    '1999-09-09 01:02:03'
    >>> acm_datetime('TODAY', datetime.date(1984, 12, 30))
    '1984-12-30 00:00:00'
    >>> acm_datetime('TOMORROW', datetime.date(2001, 2, 28))
    '2001-03-01 00:00:00'
    >>> d2 = datetime.date(2012, 01, 20)
    >>> acm_datetime('TODAY+2d+2m 12:00:00', d2)
    '2012-03-22 12:00:00'
    >>> acm_datetime('') is None
    True
    >>> acm_datetime(' \t') is None
    True
    >>> acm_datetime(None) is None
    True
    """
    datetime_param = to_datetime(datetime_param, today=today)
    if not datetime_param:
        return None
    else:
        return datetime_param.strftime('%Y-%m-%d %H:%M:%S')

def to_timestamp(datetime_param, today=None):
    """
    .. _`to_timestamp(datetime_param, today=None)`:
    
    Convert datetime_param to a Python timestamp (seconds since the epoch, in UTC)

    If datetime_param is a number (int, long or float) it is considered to be a timestamp
    already. If datetime_param is a string it is parsed into a datetime first.
    For datetime.date, datetime.datetime, time.struct_time, tuple and list
    arguments time.mktime is used for the conversion

    >>> to_timestamp(0)
    0
    >>> to_timestamp(datetime.datetime.fromtimestamp(0))
    0.0
    >>> to_date(to_timestamp('TODAY')) - date_today()
    datetime.timedelta(0)
    >>> if 'ael' in sys.modules:
    ...     d1 = ael.date_from_string('2001-01-01')
    ...     d2 = to_date('2001-01-01')
    ...     to_timestamp(d1) - to_timestamp(d2)
    ... else:
    ...     0.0
    0.0
    >>> to_timestamp(None) is None
    True
    >>> to_timestamp('\t') is None
    True
    """

    if 'ael' in sys.modules:
        if isinstance(datetime_param, ael.ael_date):
            return datetime_param.to_time()
    if isinstance(datetime_param, basestring):
        dt = datetime_from_string(datetime_param, today=today)
        if dt is None:
            return None
        else:
            return time.mktime(dt.timetuple())
    elif isinstance(datetime_param, (int, long, float)):
        return datetime_param
    elif isinstance(datetime_param, (datetime.date, datetime.datetime)):
        return time.mktime(datetime_param.timetuple())
    elif isinstance(datetime_param, (time.struct_time, list, tuple)):
        return time.mktime(to_struct_time(datetime_param))
    elif datetime_param is None:
        return None
    else:
        raise ValueError('Parameter t=%r is of unknown type' % datetime_param)

# ----------------------------------------------------------------------------
# dbsql conversion functions
# ----------------------------------------------------------------------------

def dbsql_strftime(t, today=None, format_string=DBSQL_DATETIME_FORMAT):
    """
    .. _`dbsql_strftime(t, today=None, format=DBSQL_DATETIME_FORMAT)`:
    
    Format time t for dbsql statements

    Time t is converted to a Python timestamp using to_timestamp() and then
    formatted for dbsql.

    >>> dbsql_strftime(978307261)
    '2001-01-01 00:01:01'
    >>> local_time = to_datetime(978307261).strftime('%H:%M:%S')
    >>> # (would be '01:01:01' in GMT)
    >>> d1 = datetime.date(2012, 2, 28)
    >>> dbsql_strftime('TODAY+2d ' + local_time, today=d1)
    '2012-03-01 00:01:01'
    """
    return time.strftime(format_string, time.gmtime(to_timestamp(t, today=today)))

def dbsql_to_timestamp(datetime_string, format_string=DBSQL_DATETIME_FORMAT):
    """
    .. _`dbsql_to_timestamp(datetime_string, format_string=DBSQL_DATETIME_FORMAT)`:
    
    Parse dbsql time datetime_string and return Python timestamp
    (a float expressing seconds since the epoch, in UTC).

    >>> dbsql_to_timestamp('2001-01-01 00:01:01')
    978307261
    >>> time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(978307261))
    '2001-01-01 00:01:01'
    """
    return calendar.timegm(time.strptime(datetime_string, format_string))

def dbsql_to_datetime(datetime_string, format_string=DBSQL_DATETIME_FORMAT):
    """
    .. _`dbsql_to_datetime(datetime_string, format=DBSQL_DATETIME_FORMAT)`:
    
    Parse dbsql time datetime_string and return Python datetime.datetime object.

    >>> dt1 = dbsql_to_datetime('2001-01-01 00:01:01')
    >>> dbsql_strftime(dt1)
    '2001-01-01 00:01:01'
    >>> s1 = '2012-12-12 12:12:12'
    >>> dbsql_to_datetime(dbsql_strftime(s1)) == to_datetime(s1)
    True
    """
    return datetime.datetime.fromtimestamp(
        dbsql_to_timestamp(datetime_string, format_string=format_string))

# ----------------------------------------------------------------------------
# ASQL conversion functions
# ----------------------------------------------------------------------------

def asql_strftime(t):
    """
    .. _`asql_strftime(t)`:
    
    Format local time of t to ASQL suitable time string

    The input t is first converted to a timestamp and then to local time using
    time.localtime().

    >>> asql_strftime('10.11.1999 12:13')
    '1999-11-10 12:13:00'
    """
    return time.strftime(ASQL_DATETIME_FORMAT,
                         time.localtime(to_timestamp(t)))

# ----------------------------------------------------------------------------
# timedelta functions
# ----------------------------------------------------------------------------

def strftimedelta(format, delta = None):
    """
    .. _`strftimedelta(format, delta = None)`:
    
    Format datetime.timedelta object delta

    %d - days
    %H - full hours (includes hours for days), at least two digits
    %h - hours (does not include hours for days), formatted to two digits
    %M - minutes
    %S - seconds
    %% - percentage sign

    NOTE:
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    >>> strftimedelta('%d days %h hours', datetime.timedelta(days = 2))
    '2 days 00 hours'

    """
    if delta is None:
        delta = datetime.timedelta()
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if days < 0:
        full_hours = days * 24 - hours
    else:
        full_hours = days * 24 + hours
    map_ = {
        '%d': '%d' % days,
        '%H': '%02d' % full_hours,
        '%h': '%02d' % hours,
        '%M': '%02d' % minutes,
        '%S': '%02d' % seconds,
        '%%': '%',
    }
    return re.sub('%[dHhMS]', lambda m : map_[m.group(0)], format)

def diff_to_start_of_day(t):
    """
    .. _`diff_to_start_of_day(t)`:
    
    Return the timedelta between start of day and t

    >>> diff_to_start_of_day('17:00')
    datetime.timedelta(0, 61200)
    >>> diff_to_start_of_day('00:00:23')
    datetime.timedelta(0, 23)
    """
    t = to_datetime(t)
    start_of_day = datetime.datetime.combine(t.date(), datetime.time(0))
    return t - start_of_day

def diff_to_end_of_day(t):
    """
    .. _`diff_to_end_of_day(t)`:
    
    Return the timedelta between t and end of day.

    >>> diff_to_end_of_day('17:00')
    datetime.timedelta(0, 25200)
    >>> diff_to_end_of_day('00:00:23')
    datetime.timedelta(0, 86377)
    >>> datetime.timedelta(hours=23, minutes=59, seconds=60-23)
    datetime.timedelta(0, 86377)
    """
    t = to_datetime(t)
    t2 = t + datetime.timedelta(days=1)
    end_of_day = datetime.datetime.combine(t2.date(), datetime.time(0))
    return end_of_day - t

# ----------------------------------------------------------------------------
# ACM/AEL calendar related functions
# ----------------------------------------------------------------------------

def acm_calendar(cal):
    """
    .. _`acm_calendar(cal)`:
    
    Return acm.FCalendar object for cal.

    The function knows about extracting the calendar from currency objects.
    The calendar can also be identified by an integer or string identifier.
    In this case the function first checks if there is an acm.FCalender object
    for the identifier before checking for a currency object.

    >>> from at_type_helpers import xrepr
    >>> xrepr(acm_calendar('GBP London'))
    "acm.FCalendar['GBP London']"
    >>> xrepr(acm_calendar(ael.Calendar['GBP London']))
    "acm.FCalendar['GBP London']"
    >>> xrepr(acm_calendar(acm.FCalendar['GBP London']))
    "acm.FCalendar['GBP London']"
    >>> xrepr(acm_calendar('EUR'))
    "acm.FCalendar['EUR Euro']"
    >>> xrepr(acm_calendar(ael.Instrument['ZAR/MTN']))
    Traceback (most recent call last):
        ...
    ValueError: Can not convert ael.Instrument['ZAR/MTN'] to an acm.FCalendar object
    """
    if at_type_helpers.isinstance(cal, acm.FCalendar):
        return cal
    elif at_type_helpers.isinstance(cal, acm.FCurrency):
        # extra calendar from acm.FCurrency object
        return cal.Calendar()
    elif isinstance(cal, ael.ael_entity):
        if cal.record_type == 'Instrument' and cal.instype == 'Curr':
            # extract calendar from ael.Instrument (instype='Curr') object
            return at_type_helpers.to_acm(cal).Calendar()
        elif cal.record_type == 'Calendar':
            return at_type_helpers.to_acm(cal)
    elif isinstance(cal, (int, long, basestring)):
        # extract calendar from integer or string key. First try for
        # acm.FCalendar and then for acm.FCurrency
        acm_cal = acm.FCalendar[cal]
        if acm_cal is not None:
            return acm_cal
        curr = acm.FCurrency[cal]
        if curr is not None:
            return curr.Calendar()
    raise ValueError('Can not convert %s to an acm.FCalendar object' %
                     at_type_helpers.xrepr(cal))

def is_banking_day(cal, d):
    """
    .. _`is_banking_day(cal, d)`:
    
    Return True if date d is a banking day in calendar cal.

    >>> is_banking_day('GBP London', '2012-04-06')
    False
    >>> is_banking_day('GBP London', '2012-04-05')
    True
    >>> is_banking_day('EUR', '2012-04-05')
    True
    >>> is_banking_day('EUR', '2012-04-06')
    False
    >>> is_banking_day('EUR', '2012-04-07')
    False
    """
    cal = acm_calendar(cal)
    return not cal.IsNonBankingDay(None, None, acm_date(d))

def is_non_banking_day(cal, d):
    """
    .. _`is_non_banking_day(cal, d)`:
    
    Return True if date d is a non-banking day in calendar cal.

    >>> is_non_banking_day('GBP London', '2012-04-06')
    True
    >>> is_non_banking_day('GBP London', '2012-04-05')
    False
    """
    cal = acm_calendar(cal)
    return cal.IsNonBankingDay(None, None, acm_date(d))

def bankingday_timediff(cal, t1, t2):
    """
    .. _`bankingday_timediff(cal, t1, t2)`:
    
    Return timedelta between t1 and t2 counting only banking days

    Returns datetime.timedelta(0) if t1 >= t2.

    >>> cal = 'GBP London'
    >>> bankingday_timediff(cal, '2012-03-09 17:00', '2012-03-12 09:00')
    datetime.timedelta(0, 57600)
    >>> bankingday_timediff(cal, '2012-03-09 17:00', '2012-03-13 09:00')
    datetime.timedelta(1, 57600)
    >>> bankingday_timediff(cal, '2012-04-06 17:00', '2012-04-10 09:00')
    datetime.timedelta(0, 32400)
    >>> bankingday_timediff(cal, '2012-03-12 17:00', '2012-03-13 09:00')
    datetime.timedelta(0, 57600)
    >>> bankingday_timediff(cal, '2012-03-12 17:00', '2012-03-15 09:00')
    datetime.timedelta(2, 57600)
    >>> bankingday_timediff(cal, '2012-03-09 17:00', '2012-03-09 09:00')
    datetime.timedelta(0)
    >>> bankingday_timediff(cal, '2012-03-09 09:00', '2012-03-09 17:00')
    datetime.timedelta(0, 28800)
    >>> bankingday_timediff(cal, '2012-03-11 09:00', '2012-03-11 17:00')
    datetime.timedelta(0)
    """
    cal = acm_calendar(cal)
    t1 = to_datetime(t1)
    t2 = to_datetime(t2)
    delta = datetime.timedelta(0)
    if t1 >= t2:
        return delta
    if to_date(t1) == to_date(t2):
        if is_banking_day(cal, t1):
            return t2 - t1
        else:
            return delta
    one_day = datetime.timedelta(days=1)
    if is_banking_day(cal, t1):
        delta += diff_to_end_of_day(t1)
    if is_banking_day(cal, t2):
        delta += diff_to_start_of_day(t2)
    t1 = cal.AdjustBankingDays(acm_date(t1), 1)
    t2 = cal.AdjustBankingDays(acm_date(t2), 0)
    banking_days = cal.BankingDaysBetween(t1, t2)
    delta += banking_days * one_day
    return delta

# ----------------------------------------------------------------------------
# Main program
# ----------------------------------------------------------------------------

def time_now():
    return acm_datetime(acm.Time.TimeNow())

def testmain(argv=None):
    import doctest
    doctest.testmod(verbose=True)


if __name__ == '__main__':
    sys.exit(testmain(argv=sys.argv))
