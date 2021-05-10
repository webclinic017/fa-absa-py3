"""-----------------------------------------------------------------------------
PROJECT                 :  Security Borrowing and Lending
PURPOSE                 :  Unit tests for SL extend open end process
DEPATMENT AND DESK      :  Prime Services, Securities Lending
REQUESTER               :  Linda Breytenbach
DEVELOPER               :  Paul Jacot-Guillarmod
CR NUMBER               :  494829
-----------------------------------------------------------------------------

HISTORY
=============================================================================
Date       Change no Developer              Description
-----------------------------------------------------------------------------
2010-11-16 494829    Paul Jacot-Guillarmod  Initial implementation
"""

import ael, acm
import unittest
from test_helper_trades import TradeHelper
from test_helper_instruments import InstrumentHelper
import SL_Extend_SecLoans
import test_extend_security_loans

calendar = acm.FCalendar['ZAR Johannesburg']
today = acm.Time().DateNow()
yesterday = calendar.AdjustBankingDays(today, -1)
tomorrow = calendar.AdjustBankingDays(today, 1)

class TestExtendOpenEndToday(unittest.TestCase):
    
    def setUp(self):
        self.startDate = acm.Time().DateFromYMD(2010, 6, 1)
        self.endDate = today
        self.quantity = 100
        self.instrument = InstrumentHelper.CreatePersistantOpenEndedSecurityLoan(self.startDate, self.endDate)
        self.trade = TradeHelper.BookSecurityLoan(self.instrument, 'BO Confirmed', self.startDate)
        SL_Extend_SecLoans.extend_security_loans([self.instrument])
        
    def testEndDate(self):
        self.assertEqual(self.instrument.EndDate(), tomorrow, 'Instrument end date should be tomorrow')

class TestExtendOpenEndTomorrow(unittest.TestCase):
    
    def setUp(self):
        self.startDate = acm.Time().DateFromYMD(2010, 6, 1)
        self.endDate = tomorrow
        self.quantity = 100
        self.instrument = InstrumentHelper.CreatePersistantOpenEndedSecurityLoan(self.startDate, self.endDate)
        self.trade = TradeHelper.BookSecurityLoan(self.instrument, 'BO Confirmed', self.startDate)
        SL_Extend_SecLoans.extend_security_loans([self.instrument])
        
    def testEndDate(self):
        self.assertEqual(self.instrument.EndDate(), tomorrow, 'Instrument end date should be tomorrow')

class TestExtendOpenEndYesterday(unittest.TestCase):
    
    def setUp(self):
        self.startDate = acm.Time().DateFromYMD(2010, 6, 1)
        self.endDate = yesterday
        self.quantity = 100
        self.instrument = InstrumentHelper.CreatePersistantOpenEndedSecurityLoan(self.startDate, self.endDate)
        self.trade = TradeHelper.BookSecurityLoan(self.instrument, 'BO Confirmed', self.startDate)
        SL_Extend_SecLoans.extend_security_loans([self.instrument])
        
    def testEndDate(self):
        self.assertEqual(self.instrument.EndDate(), tomorrow, 'Instrument end date should be tomorrow')

class TestExtendCFDOpenEndToday(unittest.TestCase):
    
    def setUp(self):
        self.startDate = yesterday
        self.endDate = today
        self.quantity = 100
        self.trade = TradeHelper.BookCFDSecurityLoanAndTrade(self.startDate, self.endDate, 'BO Confirmed', self.quantity)
        self.instrument = self.trade.Instrument()
        SL_Extend_SecLoans.extend_security_loans([self.instrument])
        
    def testEndDate(self):
        self.assertEqual(self.instrument.EndDate(), tomorrow, 'Instrument end date should be tomorrow')
        
    def testCashFlows(self):
        numOldCashflows = acm.Time().DateDifference(today, yesterday)
        numNewCashflows = acm.Time().DateDifference(tomorrow, today)
        numCashflows = numOldCashflows + numNewCashflows
        self.assertEqual(len(self.instrument.Legs().At(0).CashFlows()), numCashflows, 'Instrument should have ' + str(numCashflows) + ' two cashflows')

def _run_tests():
    suite = unittest.TestLoader().loadTestsFromModule(test_extend_security_loans)
    unittest.TextTestRunner(verbosity=2).run(suite)
