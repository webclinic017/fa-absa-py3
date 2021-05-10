"""
    FDateTime - provides convenience functions for generating dates.

"""
import datetime
import time as _time

class FLocalTimeZone(datetime.tzinfo):
    ZERO = datetime.timedelta(0)
    STDOFFSET = datetime.timedelta(seconds = -_time.timezone)
    if _time.daylight:
        DSTOFFSET = datetime.timedelta(seconds = -_time.altzone)
    else:
        DSTOFFSET = STDOFFSET

    DSTDIFF = DSTOFFSET - STDOFFSET
    
    def utcoffset(self, dt):
        if self._isdst(dt):
            return self.DSTOFFSET
        else:
            return self.STDOFFSET

    def dst(self, dt):
        if self._isdst(dt):
            return self.DSTDIFF
        else:
            return self.ZERO

    def tzname(self, dt):
        return _time.tzname[self._isdst(dt)]

    def _isdst(self, dt):
        tt = (dt.year, dt.month, dt.day,
              dt.hour, dt.minute, dt.second,
              dt.weekday(), 0, -1)
        stamp = _time.mktime(tt)
        tt = _time.localtime(stamp)
        return tt.tm_isdst > 0

def iso_utc_now_tz():
    """returns ISO-8601 utc now with time zone info: http://en.wikipedia.org/wiki/ISO_8601"""
    dt = datetime.datetime.now(FLocalTimeZone()).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return dt

def iso_utc_now():
    """returns ISO-8601 utc now without time zone info"""
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat(' ') 
