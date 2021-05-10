"""-----------------------------------------------------------------------------
PROJECT                 :  Security Borrowing and Lending (CFD Implementation)
PURPOSE                 :  Unit tests for sl_auto_return script
DEPATMENT AND DESK      :  Prime Services, Securities Lending
REQUESTER               :  Linda Breytenbach
DEVELOPER               :  Francois Truter
CR NUMBER               :  524194
-----------------------------------------------------------------------------

HISTORY
=============================================================================
Date       Change no Developer          Description
-----------------------------------------------------------------------------
2010-11-16 494829    Francois Truter    Initial implementation
2010-11-23 502781    Francois Truter    Updated tests
2010-12-14 524194    Francois Truter    Updated tests
2011-04-04 619099    Francois Truter    Added rates column parameter
"""
from test_helper_instruments import InstrumentHelper
from test_helper_trades import TradeHelper
from test_helper_general import PortfolioHelper
from test_helper_general import TradeFilterHelper
from test_sl_process_log import SlProcessLogHelper
from test_sl_rates import SblRatesHelper
from sl_process_log import ProcessLog
from sl_batch import SblAutoReturnBatch
import unittest
import acm
import sl_auto_return
import string
import test_sl_auto_return

TODAY = acm.Time().DateToday()
YESTERDAY = acm.Time().DateAddDelta(TODAY, 0, 0, -1)
TOMORROW = acm.Time().DateAddDelta(TODAY, 0, 0, 1)

EXTERNAL = 'External'
INTERNAL = 'Internal'

def _dateToOneYearExpiry(days):
    return  acm.Time().DateAddDelta(TODAY, 0, 0, days - 365)
    
class ReturnHelper:

    @staticmethod
    def AssertOrderFromLog(testCase, trades, log, expectPartialReturn):
        logStr = str(log)
        prevPos = 0
        prevTrade = None
        index = 0
        for trade in trades:
            index += 1
            searchStr = 'Trade [%i] returned'
            if index == len(trades) and expectPartialReturn:
                searchStr = 'Trade [%i] partially returned'
            try:
                pos = string.index(logStr, searchStr % trade.Oid())
            except  ValueError:
                testCase.fail('Did not find trade %i in log' % trade.Oid())
            if prevTrade:
                testCase.assertTrue(pos > prevPos, 'Expected trade %i to be returned before trade %i' % (prevTrade.Oid(), trade.Oid()))
            prevTrade = trade
            prevPos = pos
    
    @staticmethod
    def AssertReturnedTrade(testCase, trade, message):
        expectedInstrumentStatus = 'Terminated'
        expectedTtradeStatus = 'Terminated'
        instrument = trade.Instrument()
        testCase.assertEqual(expectedInstrumentStatus, instrument.OpenEnd(), '%s: Expected instrument to be termindated, got %s' % (message, instrument.OpenEnd()))
        testCase.assertEqual(expectedTtradeStatus, trade.Status(), '%s: Expected trade to be BO Confirmed, got %s' % (message, trade.Status()))
        
    @staticmethod
    def AssertPartiallyReturnedTrade(testCase, trade, quantityReturned, message):
        ReturnHelper.AssertReturnedTrade(testCase, trade, message)
        partialReturnChild = trade.SLPartialReturnNextTrade()
        testCase.assertTrue(partialReturnChild, '%s: Expected trade to be partially returned' % message)
        testCase.assertEqual('Open End', partialReturnChild.Instrument().OpenEnd(), '%s: Expected partially returned trade child to be open ended, got %s' % (message, partialReturnChild.Instrument().OpenEnd()))
        testCase.assertEqual('FO Confirmed', partialReturnChild.Status(), '%s: Expected partially returned trade to be FO Confirmed, got %s' % (message, partialReturnChild.Status()))
        quantityLeft = trade.QuantityInUnderlying() - quantityReturned
        testCase.assertEqual(quantityLeft, partialReturnChild.QuantityInUnderlying(), '%s: Quantity left not as expected. Expected %s, got %s' % (message, quantityLeft, partialReturnChild.QuantityInUnderlying()))
        
    @staticmethod
    def AssertNotReturnedTrade(testCase, trade, message):
        testCase.assertEqual('Open End', trade.Instrument().OpenEnd(), '%s: Expected trade to be open ended, got %s' % (message, trade.Instrument().OpenEnd()))
        testCase.assertEqual('BO Confirmed', trade.Status(), '%s: Expected trade to be BO Confirmed, got %s' % (message, trade.Status()))
        testCase.assertFalse(trade.SLPartialReturned(), '%s: Did not expect trade to be partially returned' % message)

class TestReturnPosition(unittest.TestCase):

    def setUp(self):
        self.portfolio = PortfolioHelper.CreatePersistantPortfolio()
        self.underlying = InstrumentHelper.CreatePersistantStock()
        self.date = TODAY
        self.returnPosition = sl_auto_return.ReturnPosition(self.underlying, self.date, 10000, 90, 50)
    
    def testProperties(self):
        quantity = 10000
        daysBarrier = 90
        costBarrier = 500
        
        returnPosition = sl_auto_return.ReturnPosition(self.underlying, TODAY, quantity, daysBarrier, costBarrier)
        
        self.assertEqual(self.underlying, returnPosition.Instrument, 'Instrument not as expected. Expected %s, got %s' % (self.underlying.Name(), returnPosition.Instrument.Name()))
        self.assertEqual(quantity, returnPosition.QuantityToReturn, 'Quantity not as expected. Expected %s, got %s' % (quantity, returnPosition.QuantityToReturn))
        
    def testAddTradesInvalidInstrument(self):
        trade = TradeHelper.BookTrade(self.portfolio, self.underlying, TODAY, 100000, 'BO Confirmed')
        expectedMessage = 'Trade [%(trade)i] cannot be considered for auto return, it is a [%(type)s]. Only Security Loan instruments can be returned.' % \
            {'trade': trade.Oid(), 'type': self.underlying.InsType()}
        log = ProcessLog('TestReturnPosition.testAddTradesInvalidInstrument')
        self.returnPosition.AddTrades([trade], log)
        SlProcessLogHelper.AssertLogContains(self, 'Invalid instrument', log, expectedMessage)
        
    def testAddTradesInvalidStatus(self):
        trades = []
        for status in ['Simulated', 'Void', 'FO Confirmed', 'Terminated']:
            trades.append(TradeHelper.BookSecurityLoanFromUnderlying(self.portfolio, self.underlying, 100000, 10, 0.05, EXTERNAL, TODAY, status))
            
        log = ProcessLog('TestReturnPosition.testAddTradesInvalidStatus')
        self.returnPosition.AddTrades(trades, log)
         
        for trade in trades:
            expectedMessage = 'Trade [%(trade)i] cannot be considered for auto return, it has a status of [%(status)s]. Trade status must be BO Confirmed at a minimum in order to return.' % \
                {'trade': trade.Oid(), 'status': trade.Status()}
            SlProcessLogHelper.AssertLogContains(self, 'Invalid Status', log, expectedMessage)
            
    def testAddTradesInvalidOpenEnd(self):
        trades = []
        for status in ['None', 'Terminated']:
            trade = TradeHelper.BookSecurityLoanFromUnderlying(self.portfolio, self.underlying, 100000, 10, 0.05, EXTERNAL, TODAY, 'BO Confirmed')
            instrument = trade.Instrument()
            instrument.OpenEnd(status)
            instrument.Commit()
            trades.append(trade)
            
        log = ProcessLog('TestReturnPosition.testAddTradesInvalidOpenEnd')
        self.returnPosition.AddTrades(trades, log)
         
        for trade in trades:
            expectedMessage = 'Trade [%(trade)i] cannot be considered for auto return, it has an open end status of [%(status)s]. Only open ended trades can be returned.' % \
                {'trade': trade.Oid(), 'status': trade.Instrument().OpenEnd()}
            SlProcessLogHelper.AssertLogContains(self, 'Invalid Open End Status', log, expectedMessage)
            
    def testAddTradesInvalidStartDate(self):
        trade1 = TradeHelper.BookSecurityLoanFromUnderlying(self.portfolio, self.underlying, 100000, 10, 0.05, EXTERNAL, YESTERDAY, 'BO Confirmed')
        trade2 = TradeHelper.BookSecurityLoanFromUnderlying(self.portfolio, self.underlying, 100000, 10, 0.05, EXTERNAL, TODAY, 'BO Confirmed')
        trade3 = TradeHelper.BookSecurityLoanFromUnderlying(self.portfolio, self.underlying, 100000, 10, 0.05, EXTERNAL, TOMORROW, 'BO Confirmed')
        trades = [trade1, trade2, trade3]
            
        log = ProcessLog('TestReturnPosition.testAddTradesInvalidStartDate')
        self.returnPosition.AddTrades(trades, log)
        
        expectedMessageTrade2 = 'Trade [%(trade)i] cannot be returned today [%(today)s], it only starts on %(startDate)s.' % \
                {'trade': trade2.Oid(), 'today': TODAY, 'startDate': TODAY}
        
        expectedMessageTrade3 = 'Trade [%(trade)i] cannot be returned on %(returnDate)s, it only starts on %(startDate)s.' % \
                {'trade': trade3.Oid(), 'returnDate': self.date, 'startDate': TOMORROW}
        
        SlProcessLogHelper.AssertLogNotContains(self, 'trade1', log, str(trade1.Oid()))
        SlProcessLogHelper.AssertLogContains(self, 'trade2', log, expectedMessageTrade2)
        SlProcessLogHelper.AssertLogContains(self, 'trade3', log, expectedMessageTrade3)
         
    def testReturnTradesCostBarrier(self):
        quantity1 = 200000
        quantity2 = 60000
        quantity3 = 90000
        rate1 = 0.15
        rate2 = 0.1
        rate3 = 0.1
        price = 15
    
        tradeStatus = 'BO Confirmed'
        trade1 = TradeHelper.BookSecurityLoanFromUnderlying(self.portfolio, self.underlying, quantity1, price, rate1, EXTERNAL, _dateToOneYearExpiry(5), tradeStatus)
        trade2 = TradeHelper.BookSecurityLoanFromUnderlying(self.portfolio, self.underlying, quantity2, price, rate2, EXTERNAL, _dateToOneYearExpiry(5), tradeStatus)
        trade3 = TradeHelper.BookSecurityLoanFromUnderlying(self.portfolio, self.underlying, quantity3, price, rate3, EXTERNAL, _dateToOneYearExpiry(5), tradeStatus)
        
        totalQuantity = quantity1 + quantity2 + quantity3
        quantityLeft = round(quantity3 / 2)
        quantityToReturn = totalQuantity - quantityLeft
        costBarier = (quantity3 - quantityLeft) * price * trade3.Instrument().Underlying().Quotation().QuotationFactor() * rate3 / 365.00
        
        batch = SblAutoReturnBatch.CreateBatch(TODAY)
        log = ProcessLog('TestReturnPosition.testReturnTradesCostBarrier')
        returnPosition = sl_auto_return.ReturnPosition(self.underlying, TOMORROW, quantityToReturn, 90, costBarier)
        returnPosition.AddTrades([trade2, trade3, trade1], log)
        returnPosition.ReturnTrades(batch, log)
        
        ReturnHelper.AssertReturnedTrade(self, trade1, 'trade1')
        ReturnHelper.AssertReturnedTrade(self, trade2, 'trade2')
        ReturnHelper.AssertNotReturnedTrade(self, trade3, 'trade3')
        ReturnHelper.AssertOrderFromLog(self, [trade1, trade2], log, False)
        expectedMessage = 'Trade [%i] will not be partially returned as the cost does not exceed the cost barrier' %  trade3.Oid()
        SlProcessLogHelper.AssertLogContains(self, 'Cost Barrier', log, expectedMessage)
        
    def testReturnTrades(self):
        portfolio1 = PortfolioHelper.CreatePersistantPortfolio()
        portfolio2 = PortfolioHelper.CreatePersistantPortfolio()
        underlying = InstrumentHelper.CreatePersistantStock()
        
        quantity1 = 50000
        quantity2 = 100000
        quantity3 = 400000
        quantity4 = 200000
        quantity5 = 500000
        quantity6 = 90000
        quantity7 = 100000

        tradeStatus = 'BO Confirmed'
        trade1 = TradeHelper.BookSecurityLoanFromUnderlying(portfolio2, underlying, quantity1, 80, 0.08, EXTERNAL, _dateToOneYearExpiry(3), tradeStatus)
        trade2 = TradeHelper.BookSecurityLoanFromUnderlying(portfolio2, underlying, quantity2, 90, 0.095, INTERNAL, _dateToOneYearExpiry(25), tradeStatus)
        trade3 = TradeHelper.BookSecurityLoanFromUnderlying(portfolio1, underlying, quantity3, 70, 0.1, INTERNAL, _dateToOneYearExpiry(25), tradeStatus)
        trade4 = TradeHelper.BookSecurityLoanFromUnderlying(portfolio2, underlying, quantity4, 100, 0.15, EXTERNAL, _dateToOneYearExpiry(95), tradeStatus)
        trade5 = TradeHelper.BookSecurityLoanFromUnderlying(portfolio1, underlying, quantity5, 100, 0.1, EXTERNAL, _dateToOneYearExpiry(101), tradeStatus)
        trade6 = TradeHelper.BookSecurityLoanFromUnderlying(portfolio2, underlying, quantity6, 60, 0.15, INTERNAL, _dateToOneYearExpiry(95), tradeStatus)
        trade7 = TradeHelper.BookSecurityLoanFromUnderlying(portfolio1, underlying, quantity7, 100, 0.09, INTERNAL, _dateToOneYearExpiry(91), tradeStatus)
        
        totalQuantity = quantity1 + quantity2 + quantity3 + quantity4 + quantity5 + quantity6 + quantity7
        quantityLeft = 40
        quantityToReturn = totalQuantity - quantityLeft
        returnDate = TOMORROW
        
        batch = SblAutoReturnBatch.CreateBatch(returnDate)
        log = ProcessLog('TestReturnPosition.testReturnTrades')
        returnPosition = sl_auto_return.ReturnPosition(underlying, returnDate, quantityToReturn, 25, 1)
        returnPosition.AddTrades([trade6, trade2, trade1, trade4, trade3, trade7, trade5], log)
        returnPosition.ReturnTrades(batch, log)
        
        ReturnHelper.AssertReturnedTrade(self, trade1, 'trade1')
        ReturnHelper.AssertReturnedTrade(self, trade2, 'trade2')
        ReturnHelper.AssertReturnedTrade(self, trade3, 'trade3')
        ReturnHelper.AssertReturnedTrade(self, trade4, 'trade4')
        ReturnHelper.AssertReturnedTrade(self, trade5, 'trade5')
        ReturnHelper.AssertReturnedTrade(self, trade6, 'trade6')
        ReturnHelper.AssertPartiallyReturnedTrade(self, trade7, trade7.QuantityInUnderlying() - quantityLeft, 'trade7')
        ReturnHelper.AssertOrderFromLog(self, [trade1, trade2, trade3, trade4, trade5, trade6, trade7], log, True)
        
    def testReturnTradesNothingToReturn(self):
        returnPosition = sl_auto_return.ReturnPosition(self.underlying, TODAY, 0, 90, 50)
        batch = SblAutoReturnBatch.CreateBatch(TODAY)
        log = ProcessLog('TestReturnPosition.testReturnTradesNothingToReturn')
        returnPosition.ReturnTrades(batch, log)
        expectedMessage = 'Nothing needs be returned for %s.' % self.underlying.Name()
        SlProcessLogHelper.AssertLogContains(self, 'Noting To Return', log, expectedMessage)
        
    def testReturnTradesNoTradesToReturn(self):
        returnPosition = sl_auto_return.ReturnPosition(self.underlying, TODAY, 5000, 90, 50)
        batch = SblAutoReturnBatch.CreateBatch(TODAY)
        log = ProcessLog('TestReturnPosition.testReturnTradesNoTradesToReturn')
        returnPosition.ReturnTrades(batch, log)
        expectedMessage = 'No trades to return for %s.' % self.underlying.Name()
        SlProcessLogHelper.AssertLogContains(self, 'No Trades To Return', log, expectedMessage)

class TestAutoReturn(unittest.TestCase):

    def testReturnTrades(self):
        sblPortfolio = PortfolioHelper.CreatePersistantPortfolio()
        portfolio1 = PortfolioHelper.CreatePersistantPortfolio()
        portfolio2 = PortfolioHelper.CreatePersistantPortfolio()

        loanTradeStatus = 'BO Confirmed'
        instrument1 = InstrumentHelper.CreatePersistantStock()
        stockTrade11 = TradeHelper.BookTrade(portfolio1, instrument1, YESTERDAY, -100000, 'FO Confirmed')
        stockTrade12 = TradeHelper.BookSecurityLoanFromUnderlying(portfolio1, instrument1, -50000, 8, 0.08, EXTERNAL, YESTERDAY, 'BO Confirmed')
        stockTrade13 = TradeHelper.BookTrade(portfolio2, instrument1, TODAY, -50000, 'FO Confirmed')
        trade11 = TradeHelper.BookSecurityLoanFromUnderlying(sblPortfolio, instrument1, 100000, 1200, 0.09, EXTERNAL, _dateToOneYearExpiry(2), loanTradeStatus)
        trade12 = TradeHelper.BookSecurityLoanFromUnderlying(sblPortfolio, instrument1, 100000, 1000, 0.1, EXTERNAL, _dateToOneYearExpiry(4), loanTradeStatus)
        trade13 = TradeHelper.BookSecurityLoanFromUnderlying(sblPortfolio, instrument1, 200000, 1000, 0.05, EXTERNAL, _dateToOneYearExpiry(4), loanTradeStatus)
        trade14 = TradeHelper.BookSecurityLoanFromUnderlying(sblPortfolio, instrument1, 200000, 1000, 0.1, EXTERNAL, _dateToOneYearExpiry(90), loanTradeStatus)
        trade15 = TradeHelper.BookSecurityLoanFromUnderlying(sblPortfolio, instrument1, 50000, 1000, 0.05, EXTERNAL, _dateToOneYearExpiry(156), loanTradeStatus)
        trade16 = TradeHelper.BookSecurityLoanFromUnderlying(sblPortfolio, instrument1, 350000, 1000, 0.05, EXTERNAL, _dateToOneYearExpiry(156), loanTradeStatus)

        instrument2 = InstrumentHelper.CreatePersistantStock()
        stockTrade21 = TradeHelper.BookTrade(portfolio1, instrument2, YESTERDAY, -50000, 'FO Confirmed')
        stockTrade21 = TradeHelper.BookTrade(portfolio1, instrument2, YESTERDAY, -50000, 'BO Confirmed')
        trade21 = TradeHelper.BookSecurityLoanFromUnderlying(sblPortfolio, instrument2, 100000, 2000, 0.05, EXTERNAL, _dateToOneYearExpiry(3), loanTradeStatus)
        trade22 = TradeHelper.BookSecurityLoanFromUnderlying(sblPortfolio, instrument2, 100000, 2000, 0.04, EXTERNAL, _dateToOneYearExpiry(3), loanTradeStatus)
        trade23 = TradeHelper.BookSecurityLoanFromUnderlying(sblPortfolio, instrument2, 205000, 2000, 0.04, EXTERNAL, _dateToOneYearExpiry(3), loanTradeStatus)

        instrument3 = InstrumentHelper.CreatePersistantStock()
        stockTrade31 = TradeHelper.BookTrade(portfolio2, instrument3, TODAY, -100000, 'FO Confirmed')
        trade31 = TradeHelper.BookSecurityLoanFromUnderlying(sblPortfolio, instrument3, 100000, 2000, 0.1, EXTERNAL, _dateToOneYearExpiry(3), loanTradeStatus)
        trade32 = TradeHelper.BookSecurityLoanFromUnderlying(sblPortfolio, instrument3, 100000, 1000, 0.1, EXTERNAL, _dateToOneYearExpiry(3), loanTradeStatus)
        trade33 = TradeHelper.BookSecurityLoanFromUnderlying(sblPortfolio, instrument3, 205000, 1000, 0.1, EXTERNAL, _dateToOneYearExpiry(3), loanTradeStatus)

        instrument4 = InstrumentHelper.CreatePersistantStock()
        stockTrade41 = TradeHelper.BookTrade(portfolio1, instrument4, YESTERDAY, -500000, 'BO Confirmed')
        stockTrade42 = TradeHelper.BookTrade(portfolio1, instrument4, TODAY, -2500000, 'FO Confirmed')
        trade41 = TradeHelper.BookSecurityLoanFromUnderlying(sblPortfolio, instrument4, 1000000, 5000, 0.1, EXTERNAL, _dateToOneYearExpiry(5), loanTradeStatus)
        trade42 = TradeHelper.BookSecurityLoanFromUnderlying(sblPortfolio, instrument4, 1800000, 6800, 0.09, EXTERNAL, _dateToOneYearExpiry(10), loanTradeStatus)
        
        instrument5 = InstrumentHelper.CreatePersistantStock()
        stockTrade51 = TradeHelper.BookTrade(portfolio1, instrument5, TODAY, -200000, 'BO Confirmed')
        trade51 = TradeHelper.BookSecurityLoanFromUnderlying(sblPortfolio, instrument5, 400000, 1000, 0.1, EXTERNAL, _dateToOneYearExpiry(100), loanTradeStatus)
        
        instrument6 = InstrumentHelper.CreatePersistantStock()
        stockTrade61 = TradeHelper.BookTrade(portfolio2, instrument6, YESTERDAY, 500000, 'BO Confirmed')
        trade61 = TradeHelper.BookSecurityLoanFromUnderlying(sblPortfolio, instrument6, 200000, 15000, 0.05, EXTERNAL, _dateToOneYearExpiry(2), loanTradeStatus)
        trade62 = TradeHelper.BookSecurityLoanFromUnderlying(sblPortfolio, instrument6, 100000, 21000, 0.3, EXTERNAL, _dateToOneYearExpiry(120), loanTradeStatus)
        
        instrument7 = InstrumentHelper.CreatePersistantStock()
        stockTrade71 = TradeHelper.BookTrade(portfolio1, instrument7, TODAY, -300000, 'FO Confirmed')
        trade71 = TradeHelper.BookSecurityLoanFromUnderlying(sblPortfolio, instrument7, 105000, 500, 0.1, EXTERNAL, _dateToOneYearExpiry(158), loanTradeStatus)
        trade72 = TradeHelper.BookSecurityLoanFromUnderlying(sblPortfolio, instrument7, 200000, 500, 0.1, EXTERNAL, _dateToOneYearExpiry(164), loanTradeStatus)
        
        positionsFilter = TradeFilterHelper.CreateTradeFilter([portfolio1, portfolio2])
        SblRatesHelper.WriteRatesFile([[instrument1.Name(), '*', '0.13', '', '0.12'], [instrument2.Name(), '', '0.1', '', '0.06'], [instrument5.Name(), '', '0.12', '*', '0.11']])
        
        returnDate = TOMORROW
        barierValue = 10
        log = ProcessLog('TestAutoReturn.testReturnTrades')
        autoReturn = sl_auto_return.AutoReturn(positionsFilter, sblPortfolio, returnDate, 90, barierValue)
        autoReturn.ReturnTrades(SblRatesHelper.filepath, 5, log)
        
        ReturnHelper.AssertReturnedTrade(self, trade11, 'trade11')
        ReturnHelper.AssertReturnedTrade(self, trade12, 'trade12')
        ReturnHelper.AssertReturnedTrade(self, trade13, 'trade13')
        ReturnHelper.AssertReturnedTrade(self, trade14, 'trade14')
        ReturnHelper.AssertReturnedTrade(self, trade15, 'trade15')
        ReturnHelper.AssertPartiallyReturnedTrade(self, trade16, 150000, 'trade16')
        ReturnHelper.AssertOrderFromLog(self, [trade11, trade12, trade13, trade14, trade15, trade16], log, True)
        
        ReturnHelper.AssertReturnedTrade(self, trade21, 'trade21')
        ReturnHelper.AssertReturnedTrade(self, trade22, 'trade22')
        ReturnHelper.AssertPartiallyReturnedTrade(self, trade23, 105000, 'trade23')
        ReturnHelper.AssertOrderFromLog(self, [trade21, trade22, trade23], log, True)
        
        ReturnHelper.AssertReturnedTrade(self, trade31, 'trade31')
        ReturnHelper.AssertReturnedTrade(self, trade32, 'trade32')
        ReturnHelper.AssertPartiallyReturnedTrade(self, trade33, 105000, 'trade33')
        ReturnHelper.AssertOrderFromLog(self, [trade31, trade32, trade33], log, True)
        
        ReturnHelper.AssertNotReturnedTrade(self, trade41, 'trade41')
        ReturnHelper.AssertNotReturnedTrade(self, trade42, 'trade42')
        
        ReturnHelper.AssertNotReturnedTrade(self, trade51, 'trade51')
        expectedMessage = 'Instrument [%s] is set to not auto return in the rates file.' % instrument5.Name()
        SlProcessLogHelper.AssertLogContains(self, 'trade51', log, expectedMessage)
        
        ReturnHelper.AssertReturnedTrade(self, trade61, 'trade61')
        ReturnHelper.AssertReturnedTrade(self, trade62, 'trade62')
        ReturnHelper.AssertOrderFromLog(self, [trade61, trade62], log, False)
        
        quatationFactor = trade71.Instrument().Underlying().Quotation().QuotationFactor()
        returnValue = 5000.0 * 500.0 * quatationFactor * 0.1 / 100 / 365.0
        ReturnHelper.AssertNotReturnedTrade(self, trade71, 'trade71')
        ReturnHelper.AssertNotReturnedTrade(self, trade72, 'trade72')
        expectedMessage = 'Trade [%(trade)i] will not be partially returned as the cost does not exceed the cost barrier: %(value).2f <= %(barrier).2f' % \
            {'trade': trade71.Oid(), 'value': returnValue, 'barrier': barierValue}
        SlProcessLogHelper.AssertLogContains(self, 'trade71', log, expectedMessage)


def _run_tests():
    suite = unittest.TestLoader().loadTestsFromModule(test_sl_auto_return)
    #suite = unittest.TestLoader().loadTestsFromTestCase(TestReturnPosition)
    unittest.TextTestRunner(verbosity=2).run(suite)
