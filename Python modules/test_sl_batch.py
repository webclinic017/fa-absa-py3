"""-----------------------------------------------------------------------------
PROJECT                 :  Security Borrowing and Lending (CFD Implementation)
PURPOSE                 :  Unit tests for sl_batch module
DEPATMENT AND DESK      :  Prime Services, Securities Lending
REQUESTER               :  Linda Breytenbach
DEVELOPER               :  Francois Truter
CR NUMBER               :  494829
-----------------------------------------------------------------------------

HISTORY
=============================================================================
Date       Change no Developer          Description
-----------------------------------------------------------------------------
2010-11-16 494829    Francois Truter    Initial implementation
"""

from test_helper_instruments import InstrumentHelper
from test_helper_instruments import SlBatchType
from test_helper_trades import TradeHelper
from test_helper_general import TimeSeriesHelper
from test_helper_general import PortfolioHelper
from test_sl_process_log import SlProcessLogHelper
from sl_process_log import ProcessLog
import acm
import sl_batch
import unittest
import test_sl_batch
import sl_partial_returns

TODAY = acm.Time().DateNow()
TOMORROW = acm.Time().DateAddDelta(TODAY, 0, 0, 1)

class SblBatchTestBase():

    TestClass = None
    TimeSeriesSpec = None
    AdditionalInfo = None
    SlBatchType = None

    def testCreateBatch(self):
        runNo = TimeSeriesHelper.GetLastRunNo(self.__class__.TimeSeriesSpec, TODAY) + 1
        dateparts = acm.Time().DateToYMD(TODAY)
        expectedBatchNo = float('%(year)04i%(month)02i%(day)02i%(run)i' % {'year': dateparts[0], 'month': dateparts[1], 'day': dateparts[2], 'run': runNo})
        
        batch = self.__class__.TestClass.CreateBatch(TODAY)
        timeSeries = TimeSeriesHelper.GetTimeSeries(self.__class__.TimeSeriesSpec, TODAY, runNo)
        self.assertTrue(isinstance(batch, self.__class__.TestClass), 'Expected CreateBatch to return a %s instance, got %s' % (self.__class__.TestClass, batch.__class__))
        self.assertTrue(timeSeries, 'Expected time series does not exist')
        self.assertEqual(TODAY, timeSeries.Day(), 'Date not as expected. Expected [%s], Got [%s]' % (TODAY, timeSeries.Day()))
        self.assertEqual(expectedBatchNo, timeSeries.Value(), 'Batch number not as expected. Expected [%s], Got [%s]' % (expectedBatchNo, timeSeries.Value()))
        self.assertEqual(batch.BatchNumber, timeSeries.Value(), 'BatchNumer property not as expected. Expected [%s], Got [%s]' % (batch.BatchNumber, timeSeries.Value()))
        self.assertEqual(runNo, timeSeries.RunNo(), 'Run number not as expected. Expected [%i], Got [%i]' % (runNo, timeSeries.RunNo()))
    
    def testLoadBatch(self):
        runNo = TimeSeriesHelper.GetLastRunNo(self.__class__.TimeSeriesSpec, TODAY) + 1
        createdBatch = self.__class__.TestClass.CreateBatch(TODAY)
        loadedBatch = self.__class__.TestClass.LoadBatch(TODAY, runNo)
        expectedOid = createdBatch._timeSeries.Oid()
        actualOid = loadedBatch._timeSeries.Oid()
        self.assertEqual(expectedOid, actualOid, 'Loaded Batch not as expected. Expected %i, Got %i' % (expectedOid, actualOid))
        
    def testLoadBatchNotExists(self):
        runNo = TimeSeriesHelper.GetLastRunNo(self.__class__.TimeSeriesSpec, TODAY) + 1
        try:
            loadedBatch = self.__class__.TestClass.LoadBatch(TODAY, runNo)
        except Exception, ex:
            expected = "No '%s' batch exist for %s run number %i." % (self.__class__.TimeSeriesSpec.FieldName(), TODAY, runNo)
            actual = str(ex)
            self.assertEqual(expected, actual, 'Exception message not as expected. Expected [%s], got [%s].' % (expected, actual))
        else:
            self.fail('Expected an exception')
        
    def testBatchNumber(self):
        runNo = TimeSeriesHelper.GetLastRunNo(self.__class__.TimeSeriesSpec, TODAY) + 1
        batch = self.__class__.TestClass.CreateBatch(TODAY)
        dateparts = acm.Time().DateToYMD(TODAY)
        expected = int('%(year)04i%(month)02i%(day)02i%(run)i' % {'year': dateparts[0], 'month': dateparts[1], 'day': dateparts[2], 'run': runNo})
        actual = batch.BatchNumber
        self.assertEqual(expected, actual, 'BatchNuber not as expected. Expected %i, got %i' % (expected, actual))
        
    def testNumberOfTrades(self):
        batch = self.__class__.TestClass.CreateBatch(TODAY)
        tradeStatus = 'FO Confirmed'
        
        inInstrument1 = InstrumentHelper.CreatePersistantSecurityLoan(self.__class__.SlBatchType, batch.BatchNumber)
        inTrade1 = TradeHelper.BookSecurityLoan(inInstrument1, tradeStatus)
        inTrade2 = TradeHelper.BookSecurityLoan(inInstrument1, tradeStatus)
        
        inInstrument2 = InstrumentHelper.CreatePersistantSecurityLoan(self.__class__.SlBatchType, batch.BatchNumber)
        inTrade3 = TradeHelper.BookSecurityLoan(inInstrument2, tradeStatus)
        
        outInstrument1 = InstrumentHelper.CreatePersistantSecurityLoan(self.__class__.SlBatchType, batch.BatchNumber + 1)
        outTrade1 = TradeHelper.BookSecurityLoan(outInstrument1, tradeStatus)
        
        outInstrument2 = InstrumentHelper.CreatePersistantSecurityLoan()
        
        expected = 3
        actual = batch.NumberOfTrades
        self.assertEqual(expected, actual, 'NumberOfTrades not as expected. Expected %i, got %i' % (expected, actual))
        
    def testStampBatchNumberTrade(self):
        batch = self.__class__.TestClass.CreateBatch(TODAY)
        
        instrument1 = InstrumentHelper.CreatePersistantSecurityLoan()
        trade1 = TradeHelper.BookSecurityLoan(instrument1, 'FO Confirmed')
        
        actual = eval('instrument1.AdditionalInfo().%s()' % self.__class__.AdditionalInfo)
        self.assert_(actual == None, 'Expected no batch number, got ' + str(actual))
        
        batch.StampBatchNumber(trade1)
        
        expected = batch.BatchNumber
        actual = eval('instrument1.AdditionalInfo().%s()' % self.__class__.AdditionalInfo)
        self.assertEqual(expected, actual, 'Batch number not as expected. Expected %i, got %i' % (expected, actual))
        
    def testStampBatchNumberInstrument(self):
        batch = self.__class__.TestClass.CreateBatch(TODAY)
        
        instrument1 = InstrumentHelper.CreatePersistantSecurityLoan()
        
        actual = eval('instrument1.AdditionalInfo().%s()' % self.__class__.AdditionalInfo)
        self.assert_(actual == None, 'Expected no batch number, got ' + str(actual))        
        batch.StampBatchNumber(instrument1)
        
        expected = batch.BatchNumber
        actual = eval('instrument1.AdditionalInfo().%s()' % self.__class__.AdditionalInfo)
        self.assertEqual(expected, actual, 'Batch number not as expected. Expected %i, got %i' % (expected, actual))
        
    def testStampBatchNumberOther(self):
        batch = self.__class__.TestClass.CreateBatch(TODAY)
        
        portfolio = PortfolioHelper.CreateTemporaryPortfolio()
        try:
            batch.StampBatchNumber(portfolio)
        except Exception, ex:
            expected = 'Batch number can only be stamped on Trades and Instruments.'
            actual = str(ex)
            self.assertEqual(expected, actual, 'Exception message not as expected. Expected [%s], got [%s].' % (expected, actual))
        else:
            self.fail('Expected an exception')
            
class TestSblSweepBatch(unittest.TestCase, SblBatchTestBase):

    TestClass = sl_batch.SblSweepBatch
    TimeSeriesSpec = acm.FTimeSeriesSpec['SBL Sweeping Batch']
    AdditionalInfo = 'SL_SweepingBatchNo'
    SlBatchType = SlBatchType.Sweeping
    
    def setUp(self):
         if TimeSeriesHelper.GetLastRunNo(self.__class__.TimeSeriesSpec, TODAY) > 75:
            TimeSeriesHelper.DeleteSeriesData(self.__class__.TimeSeriesSpec, TODAY, self.__class__.SlBatchType)
    
    def testVoidBatch(self):
        batch = sl_batch.SblSweepBatch.CreateBatch(TODAY)
        tradeStatus = 'FO Confirmed'
        
        inInstrument1 = InstrumentHelper.CreatePersistantSecurityLoan(self.__class__.SlBatchType, batch.BatchNumber)
        inTrade1 = TradeHelper.BookSecurityLoan(inInstrument1, tradeStatus)
        inTrade2 = TradeHelper.BookSecurityLoan(inInstrument1, tradeStatus)
        
        inInstrument2 = InstrumentHelper.CreatePersistantSecurityLoan(self.__class__.SlBatchType, batch.BatchNumber)
        inTrade3 = TradeHelper.BookSecurityLoan(inInstrument2, tradeStatus)
        
        outInstrument1 = InstrumentHelper.CreatePersistantSecurityLoan(self.__class__.SlBatchType, batch.BatchNumber + 1)
        outTrade1 = TradeHelper.BookSecurityLoan(outInstrument1, tradeStatus)
        
        outInstrument2 = InstrumentHelper.CreatePersistantSecurityLoan()
        
        batch.VoidBatch()
        
        self.assert_(inInstrument1.OpenEnd() == 'Terminated', 'Expected inInstrument1 to be terminated')
        self.assert_(inTrade1.Status() == 'Void', 'Expected inTrade1 [%(instrument)s: %(trade)i] to be voided' % \
            {'instrument': inInstrument1.Name(), 'trade': inTrade1.Oid()})
        self.assert_(inTrade2.Status() == 'Void', 'Expected inTrade2 [%(instrument)s: %(trade)i] to be voided' % \
            {'instrument': inInstrument2.Name(), 'trade': inTrade2.Oid()})
        
        self.assert_(inInstrument2.OpenEnd() == 'Terminated', 'Expected inInstrument2 to be terminated')
        self.assert_(inTrade3.Status() == 'Void', 'Expected inTrade3 [%(instrument)s: %(trade)i] to be voided' % \
            {'instrument': inInstrument2.Name(), 'trade': inTrade3.Oid()})
        
        self.assert_(outInstrument1.OpenEnd() != 'Terminated', 'Did not expect outInstrument1 to be terminated')
        self.assert_(outTrade1.Status() == tradeStatus, 'Expected outTrade1 [%(instrument)s: %(trade)i] to be FO confirmed' % \
            {'instrument': outInstrument1.Name(), 'trade': outTrade1.Oid()})
        
        self.assert_(outInstrument2.OpenEnd() != 'Terminated', 'Did not expect outInstrument2 to be terminated')
        
    def testVoidBatchExternalLog(self):
        batch = sl_batch.SblSweepBatch.CreateBatch(TODAY)
        
        instrument = InstrumentHelper.CreatePersistantSecurityLoan(self.__class__.SlBatchType, batch.BatchNumber)
        trade = TradeHelper.BookSecurityLoan(instrument, 'BO Confirmed')
        
        log = ProcessLog('TestSblSweepBatch.testVoidBatchExternalLog')
        batch.VoidBatch(log)
        
        expected = 'Trade %i voided.' % trade.Oid()
        SlProcessLogHelper.AssertLogContains(self, 'Log Message', log, expected)

class TestSblAutoReturnBatch(unittest.TestCase, SblBatchTestBase):

    TestClass = sl_batch.SblAutoReturnBatch
    TimeSeriesSpec = acm.FTimeSeriesSpec['SBL Return Batch']
    AdditionalInfo = 'SL_ReturnBatchNo'
    SlBatchType = SlBatchType.AutoReturn
    
    def _assertTradeReverted(self, trade, message):
        instrument = trade.Instrument()
        self.assertEqual('BO Confirmed', trade.Status(), '%s: Expected trade status to be BO Confirmed, got %s' % (message, trade.Status()))
        self.assertEqual('Open End', instrument.OpenEnd(), '%s: Expected instrument to be open ended, got %s' %  (message, instrument.OpenEnd()))
        self.assertEqual(TOMORROW, instrument.EndDate(), '%s: Expected end date to be tomorrow, got %s' % (message, instrument.EndDate()))
    
    def setUp(self):
        if TimeSeriesHelper.GetLastRunNo(self.__class__.TimeSeriesSpec, TODAY) > 75:
            TimeSeriesHelper.DeleteSeriesData(self.__class__.TimeSeriesSpec, TODAY, self.__class__.SlBatchType)
            
    def testVoidBatch(self):
        batch = sl_batch.SblAutoReturnBatch.CreateBatch(TODAY)
        startDate1 = acm.Time().DateFromYMD(2010, 8, 2)
        endDate1 = acm.Time().DateAddDelta(TODAY, 0, 1, 0)
        inInstrument1 = InstrumentHelper.CreatePersistantOpenEndedSecurityLoan(startDate1, endDate1)
        inTrade11 = TradeHelper.BookSecurityLoan(inInstrument1, 'BO Confirmed', startDate1, 1000000)
        outTrade12 = sl_partial_returns.partial_return(inTrade11, TODAY, 250000)
        self.assertTrue(inTrade11.SLPartialReturnNextTrade() == outTrade12, 'Expect inTrade11 to have next trade outTrade12.')
        self.assertTrue(outTrade12.SLPartialReturnPrevTrade() == inTrade11, 'Expect outTrade12 to have previous trade inTrade11.')
        batch.StampBatchNumber(inTrade11)
        
        startDate2 = acm.Time().DateFromYMD(2010, 9, 13)
        endDate2 = acm.Time().DateAddDelta(TODAY, 0, 1, 10)
        quantity2 = 50000
        inInstrument2 = InstrumentHelper.CreatePersistantOpenEndedSecurityLoan(startDate2, endDate2)
        inTrade21 = TradeHelper.BookSecurityLoan(inInstrument2, 'BO Confirmed', startDate2, quantity2)
        outTrade22 = sl_partial_returns.partial_return(inTrade21, TODAY, quantity2)
        self.assertFalse(outTrade22, 'Did not expect outTrade22')
        batch.StampBatchNumber(inTrade21)
        
        outInstrument1 = InstrumentHelper.CreatePersistantSecurityLoan(self.__class__.SlBatchType, batch.BatchNumber + 1)
        outInstrument1.OpenEnd('Terminated')
        outInstrument1.Commit()
        outTrade1 = TradeHelper.BookSecurityLoan(outInstrument1, 'BO Confirmed')
        outTrade1.Status('Terminated')
        outTrade1.Commit()
        
        startDate3 = acm.Time().DateFromYMD(2010, 8, 26)
        yesterday = acm.Time().DateAddDelta(TODAY, 0, 0, -1)
        outInstrument2 = InstrumentHelper.CreatePersistantOpenEndedSecurityLoan(startDate3, yesterday)
        outInstrument2.OpenEnd('None')
        outInstrument2.Commit()
        
        batch.VoidBatch()
        
        self._assertTradeReverted(inTrade11, 'inTrade11')
        self.assertEqual('Void', outTrade12.Status(), 'Expected outTrade12 status to be Void, got %s' % outTrade12.Status())
        self.assertTrue(inTrade11.SLPartialReturnNextTrade() == None, 'Did not expect inTrade11 to have a next trade.')
        self.assertTrue(outTrade12.SLPartialReturnPrevTrade() == None, 'Did not expect outTrade12 to have a previous trade.')
        
        self._assertTradeReverted(inTrade21, 'inTrade21')
        
        self.assertEqual('Terminated', outInstrument1.OpenEnd(), 'Expected outInstrument1 to be terminated, got %s' % outInstrument1.OpenEnd())
        self.assertEqual('Terminated', outTrade1.Status(), 'Expected outTrade1 status to be Terminated, got %s' % outTrade1.Status())

        self.assertEqual('None', outInstrument2.OpenEnd(), 'Expected outInstrument2 to be none, got %s' % outInstrument2.OpenEnd())
        
def _run_tests():
    suite = unittest.TestLoader().loadTestsFromModule(test_sl_batch)
    #suite = unittest.TestLoader().loadTestsFromTestCase(TestSblSweepBatch)
    unittest.TextTestRunner(verbosity=2).run(suite)

