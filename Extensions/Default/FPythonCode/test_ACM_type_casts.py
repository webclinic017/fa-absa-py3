

import unittest
import acm

class TestCastOperators(unittest.TestCase):
    def _cast(self, funcname, indata, outdata):
        func = acm.GetFunction(funcname, 1)
        res = func(indata)
        self.assertEquals(res, outdata)
        self.assertEquals(type(res), type(outdata))
    def test_int(self):
        self._cast("int", 1, 1)
        self._cast("int", 10, 10)
        self._cast("int", 0, 0)
        self._cast("int", "876", 876)
        self._cast("int", "", 0)
    def test_bool(self):
         "int, int64, short"
         self._cast("bool", 1, True)
         self._cast("bool", 2, True)
         self._cast("bool", 0, False)
    def test_symbol(self):
        self._cast("symbol", 2, acm.FSymbol(2))
        self._cast("symbol", "", acm.FSymbol(""))
    def test_string(self):
        self._cast("string", 2, "2")
        self._cast("string", "", "")
        self._cast("string", None, "")
        self._cast("string", "e"*5000, "e"*5000)
        self._cast("string", 0, "0")
        self._cast("string", "\0\0a", "") # ?? ok         
    def test_denominatedvalue(self):
        self._cast("denominatedvalue", 1, acm.DenominatedValue(1.0, None, 0))     
        self._cast("denominatedvalue", "34", acm.DenominatedValue(34, None, 0))     
        self._cast("denominatedvalue", "34EUR", acm.DenominatedValue(34, "EUR", 0))     
    def test_float(self):
        self._cast("float", 0.0, 0.0)     
        self._cast("float", 99, 99.0)     
        self._cast("float", 1.0/3, 0.3333333432674408)     
        self._cast("float", "12.23", 12.229999542236328)     
        self._cast("float", "1e10", 1e10)         
    def test_time(self):        
        self._cast("time", 0, 0)     
        self._cast("time", 10, 10)     
    def test_double(self):
        self._cast("double", 0.0, 0.0)     
        self._cast("double", 99, 99.0)     
        self._cast("double", -99, -99.0)     
        self._cast("double", 1.0/3, 1.0/3)     
        self._cast("double", "12.23", 12.23)     
        self._cast("double", "1e10", 1e10)     
    def test_datetime(self):
        # looking at UTC / local time issue might cause failures when leaving DST...
        self._cast("datetime", 0.0, '1899-12-30 01:00:00')     
        self._cast("datetime", 180.0, '1900-06-28 01:00:00')     
        self._cast("datetime", '1900-06-08 01:00:00', '1900-06-08 01:00:00')     
    def test_dateperiod(self):                 
        self._cast("dateperiod", '4m', '4m')     
        self._cast("dateperiod", '3d', '3d')     
        self._cast("dateperiod", '3y', '3y')     
        self._cast("dateperiod", '-3d', '-3d')     
    def test_date(self):                 
        self._cast("date", 2, '0000-01-03')  
        self._cast("date", 2.0, '1900-01-01')
        self._cast("date", 0.0, '1899-12-30')        
        self._cast("date", 2.9, '1900-01-01')
        self._cast("date", '2005-01-01', '2005-01-01')
        self._cast("date", '2055-01-01', '2055-01-01')
    def test_byte(self):         
         self._cast("byte", 5, 5)
         self._cast("byte", 0, 0)
         self._cast("byte", 4096 + 137, 137)
    def test_char(self):
        self._cast("char", 32, ' ')
        self._cast("char", 4096 + 32, ' ')
        self._cast("char", 'a', 'a')
        self._cast("char", 'alban', 'a')
    def known_failures(self):
        # this two following conversion fail returning an emtpy string ''
        self._cast("date", 0, '0000-0-0')
        self._cast("date", 1, '0000-0-1')
        #gives really strange value
        self._cast("time", 0.0, 0)     
        # This silently truncates to 1930549383, should at leas trow an exception or something
        self._cast("int", "832409832094832908423", 0)

        # Do we really want the semantics below, ints and double give completly different dates
        self._cast("date", 2, '0000-01-03')  
        self._cast("date", 2.0, '1900-01-01')






