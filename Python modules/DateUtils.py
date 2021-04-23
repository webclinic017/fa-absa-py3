''' =====================================================================
    Date Utils

    This module exposes a date wrapper class which supports initializing
    dates with the following inputs: time.struct_time, datetime.datetime,
    float, int, str, ael.ael_date. It also overloads a few operators, nl.
    +, -, <, > as well as the method str().

    Eben Mare
    ===================================================================== '''

import ael
import time
from datetime import datetime, timedelta
from time import strptime

class PDate:
    def __init__(self, date, format = "%Y-%m-%d"):
        self._internalFormat = format
        self._date = self._reformatDate(date, self._internalFormat)

    def __cmp__(self, other):
        return self._date > other._date and 1 or (self._date < other._date and -1 or 0)

    def __add__(self, other):
        return PDate(self._date + timedelta(other))

    def __sub__(self, other):
        return PDate(self._date - timedelta(other))

    def __str__(self):
        return self._date.__str__()

    def _reformatDate(self, date, format = "%Y-%m-%d"):
        '''This function can be passed a time, ael_date or string object and the 
           date will be formatted as a string, the default format is yyyy-mm-dd.
        '''

        map = {time.struct_time: self._ReformatLocalTimeDate,
               datetime: self._ReformatDateTime, 
               float: self._ReformatTimeDate,
               int: self._ReformatTimeDate,
               str: self._ReformatStrDate,
               ael.ael_date: self._ReformatAELDate}

        # We will return a datetime object.
        date_type = type(date)
        if map.has_key(date_type):
            date_reformatted = map[date_type](date, format)
            if isinstance(date_reformatted, datetime): 
                return date_reformatted
            else:
                timestruct = strptime(date_reformatted, format)
                # now create a datetime from the first six arguments of our struct_time.
                return datetime(*timestruct[:6]) 
        else:
            raise "The type (%s) which you passed wasn't recognised as a valid date." % date_type

    def strftime(self, format = "%Y-%m-%d"):
        return self._date.strftime(format)

    def date():
        return ReformatDate(self._date, format)

    def _ReformatLocalTimeDate(self, date, format):
        return time.strftime(format, date)

    def _ReformatDateTime(self, date, format):
        return date.strftime(format)

    def _ReformatTimeDate(self, date, format):
        return self._ReformatLocalTimeDate(time.localtime(date), format)

    def _ReformatStrDate(self, date, format):
        timestruct = strptime(date, format)
        return datetime(timestruct[0], timestruct[1], timestruct[2])

    def _ReformatAELDate(self, date, format):
        return date.to_string(format)
