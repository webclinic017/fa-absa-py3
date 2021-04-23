"""-----------------------------------------------------------------------------
PROJECT                 :  Security Borrowing and Lending
PURPOSE                 :  Unit tests for sl_sweeping script
DEPATMENT AND DESK      :  Prime Services, Securities Lending
REQUESTER               :  Linda Breytenbach
DEVELOPER               :  Francois Truter
CR NUMBER               :  524194
-----------------------------------------------------------------------------

HISTORY
=============================================================================
Date       Change no Developer          Description
-----------------------------------------------------------------------------
2010-03-11 243997    Francois Truter    Initial Implementation
2010-03-15 254192    Francois Truter    Allowed partial sweeping
2010-06-08 332128    Francois Truter    Allow Multiple Sweeping per day
2010-11-16 494829    Francois Truter    Extracted helpers into seperate 
                                        modules. Added CFD sweeping tests.
2010-12-14 524194    Francois Truter    Allocate held positions
2011-04-04 619099    Francois Truter    Allowed missing external rates -
                                        those instruments are skipped.
                                        Fixed bug: if SBL desk is short
                                        and no other desk is short, the
                                        SBL desk's position wasn't covered
                                        Added rate column parameter
"""

from test_helper_general import PartyHelper
from test_helper_general import PortfolioHelper
from test_helper_general import TradeFilterHelper
from test_helper_general import TimeSeriesHelper
from test_helper_general import GeneralHelper
from test_helper_instruments import InstrumentHelper
from test_helper_instruments import SlBatchType
from test_helper_trades import TradeHelper
from test_sl_rates import SblRatesHelper
from test_sl_process_log import SlProcessLogHelper
from sl_process_log import ProcessLog
import test_helper_general
import acm
import sl_sweeping
import unittest
import os
import decimal
import test_sl_sweeping

TODAY = acm.Time().DateToday()
        
class PositionHelper:

    @staticmethod
    def CreatePosition(portfolio, instrument, quantity):
        return sl_sweeping.Position(portfolio, instrument, quantity)
        
    @staticmethod
    def AssertPosition(testCase, actualPosition, expectedPosition):
        PositionHelper.AssertPositionProperties(testCase, actualPosition, expectedPosition.portfolio, expectedPosition.instrument, expectedPosition.quantity, expectedPosition.external)

    @staticmethod
    def AssertPositionProperties(testCase, actualPosition, expectedPortfolio, expectedInstrument, expectedQuantity, expectedExternal):
        testCase.assertEqual(expectedPortfolio, actualPosition.portfolio, 'Portfolio not equal')
        testCase.assertEqual(expectedInstrument, actualPosition.instrument, 'Instrument not equal')
        GeneralHelper.AssertTypeAndValue(testCase, actualPosition.quantity, expectedQuantity, decimal.Decimal, 'Position Quantity not as expected')
        testCase.assertEqual(expectedExternal, actualPosition.external, 'External not equal')
        
class PositionCollectionHelper:

    @staticmethod
    def CreatePositionCollection(positions):
        return sl_sweeping.PositionCollection(positions)
        
    @staticmethod
    def Contains(positionCollection, portfolio, instrument, quantity, external):
        quantity = test_helper_general._toDecimal(quantity)
        for position in positionCollection:
            if position.portfolio == portfolio \
            and position.instrument == instrument \
            and position.quantity == quantity \
            and position.external == external:
                return True
        
        return False
        
class TestSblPrices(unittest.TestCase):

    def testAddAndGetPrice(self):
        price1 = 10.2
        price1b = 15.6
        price1c = 12.68
        instrument1 = InstrumentHelper.CreatePersistantStock(price1)
        price2 = 22.5
        price2b = 31.4
        instrument2 = InstrumentHelper.CreatePersistantStock(price2)
        prices = sl_sweeping.SblPrices()
        
        GeneralHelper.AssertTypeAndValue(self, prices.GetPrice(instrument1), price1, float, 'Expected used_price for instrument 1')
        
        prices.Add(instrument1, price1b)
        GeneralHelper.AssertTypeAndValue(self, prices.GetPrice(instrument1), price1b, float, 'Expected price1b for instrument 1')
        GeneralHelper.AssertTypeAndValue(self, prices.GetPrice(instrument2), price2, float, 'Expected used_price for instrument 2')
        
        prices.Add(instrument2, price2b)
        GeneralHelper.AssertTypeAndValue(self, prices.GetPrice(instrument1), price1b, float, 'Expected price1b for instrument 1')
        GeneralHelper.AssertTypeAndValue(self, prices.GetPrice(instrument2), price2b, float, 'Expected price2b for instrument 2')
        
        prices.Add(instrument1, price1c)
        GeneralHelper.AssertTypeAndValue(self, prices.GetPrice(instrument1), price1c, float, 'Expected price1c for instrument 1')
        GeneralHelper.AssertTypeAndValue(self, prices.GetPrice(instrument2), price2b, float, 'Expected price2b for instrument 2')
        
    def testEtfPrice(self):
        underlyingPrice = 15
        etfPrice = 25
        underlying = InstrumentHelper.CreatePersistantStock(underlyingPrice)
        etf = InstrumentHelper.CreatePersistantEtf(underlying, etfPrice)
        
        prices = sl_sweeping.SblPrices()
        GeneralHelper.AssertTypeAndValue(self, prices.GetPrice(etf), etfPrice, float, "Expected etf's price - not underlying's price")

class TestPosition(unittest.TestCase):
    position = None
    quantityBefore = 0
    quantityAfter = 0

    def testAttributes(self):
        portfolio = PortfolioHelper.CreateTemporaryPortfolio()
        instrument = InstrumentHelper.CreateTemporaryStock()
        quantity = 18
        external = True
        position = sl_sweeping.Position(portfolio, instrument, quantity, external)
        PositionHelper.AssertPositionProperties(self, position, portfolio, instrument, quantity, external)
        
    def testStr(self):
        portfolio = PortfolioHelper.CreateTemporaryPortfolio()
        instrument = InstrumentHelper.CreateTemporaryStock()
        quantity = 10999
        external = False
        position = sl_sweeping.Position(portfolio, instrument, quantity, external)
        
        expected = 'Portfolio | %(portfolio)s | Instrument | %(instrument)s | Quantity | %(quantity)s | %(external)s' % \
        {'portfolio': portfolio.Name(), 'instrument': instrument.Name(), 'quantity': quantity, 'external': sl_sweeping.Position.InternalExternal[external]}
        
        self.assertEqual(expected, str(position), 'Position does not convert to a string as expected')
    
    @staticmethod
    def UpdateQuantityBeforeAndAfter(position, before, after):
        TestPosition.position = position
        TestPosition.quantityBefore = before
        TestPosition.quantityAfter = after
        
    def testNotifyQuantityChanged(self):
        portfolio = PortfolioHelper.CreateTemporaryPortfolio()
        instrument = InstrumentHelper.CreateTemporaryStock()
        quantity = 201
        changedQuantity = 123
        external = True
        position = sl_sweeping.Position(portfolio, instrument, quantity, external)
        position.notifyQuantityChanged = TestPosition.UpdateQuantityBeforeAndAfter
        
        TestPosition.position = None
        TestPosition.quantityBefore = 0
        TestPosition.quantityAfter = 0
        
        position.quantity = changedQuantity
        PositionHelper.AssertPositionProperties(self, TestPosition.position, portfolio, instrument, changedQuantity, external)
        GeneralHelper.AssertTypeAndValue(self, TestPosition.quantityBefore, quantity, decimal.Decimal, 'Quantity before not as expected')
        GeneralHelper.AssertTypeAndValue(self, TestPosition.quantityAfter, changedQuantity, decimal.Decimal, 'Quantity after not as expected')
        
class TestPositionCollection(unittest.TestCase):

    def setUp(self):
        self.portfolio1 = PortfolioHelper.CreateTemporaryPortfolio()
        self.portfolio2 = PortfolioHelper.CreateTemporaryPortfolio()
        self.instrument1 = InstrumentHelper.CreateTemporaryStock()
        self.instrument2 = InstrumentHelper.CreateTemporaryStock()
        self.instrument3 = InstrumentHelper.CreateTemporaryStock()
        self.instrument4 = InstrumentHelper.CreateTemporaryStock()
        self.quantityP1I1 = 1
        self.quantityP1I2 = 2
        self.quantityP1I2E = 3
        self.quantityP1I3 = 4
        self.quantityP2I1 = 5
        self.quantityP2I2 = 6
        self.positionCollection = sl_sweeping.PositionCollection()
        self.positionCollection.Add(self.portfolio1, self.instrument1, self.quantityP1I1, False)
        self.positionCollection.Add(self.portfolio1, self.instrument2, self.quantityP1I2, False)
        self.positionCollection.Add(self.portfolio1, self.instrument2, self.quantityP1I2E, True)
        self.positionCollection.Add(self.portfolio1, self.instrument3, self.quantityP1I3, False)
        self.positionCollection.Add(self.portfolio2, self.instrument1, self.quantityP2I1, False)
        self.positionCollection.Add(self.portfolio2, self.instrument2, self.quantityP2I2, False)
        self.rates = sl_sweeping.SblRates(SblRatesHelper.filepath, 3)
        self.prices = sl_sweeping.SblPrices()

    def tearDown(self):
        if os.path.exists(SblRatesHelper.filepath):
            os.remove(SblRatesHelper.filepath)
            
    def testIteration(self):
        counter = 0
        for position in self.positionCollection:
            PositionHelper.AssertPosition(self, position, self.positionCollection[counter])
            counter += 1
        self.assertEqual(6, counter, 'Expected six positions to have iterated first time')
        
        counter = 0
        for position in self.positionCollection:
            PositionHelper.AssertPosition(self, position, self.positionCollection[counter])
            counter += 1
        self.assertEqual(6, counter, 'Expected six positions to have iterated second time')
        
    def testIterationItemsRemoved(self):
        counter = 0
        for position in self.positionCollection:
            counter += 1
            if counter == 1:
                previousPosition = position
            elif counter == 2:
                self.positionCollection.RemovePosition(position)
            elif counter == 3:
                PositionHelper.AssertPosition(self, position, self.positionCollection[1])
                self.assertEqual(self.quantityP1I2E, position.quantity, 'Quantity not as expected (3). Expected %s, got %s' % (self.quantityP1I2E, position.quantity))
                self.positionCollection.RemovePosition(previousPosition)
            elif counter == 4:
                PositionHelper.AssertPosition(self, position, self.positionCollection[1])
                self.assertEqual(self.quantityP1I3, position.quantity, 'Quantity not as expected (4). Expected %s, got %s' % (self.quantityP1I3, position.quantity))
                self.positionCollection.RemovePosition(self.positionCollection[2])
            elif counter == 5:
                PositionHelper.AssertPosition(self, position, self.positionCollection[2])
                self.assertEqual(self.quantityP2I2, position.quantity, 'Quantity not as expected (5). Expected %s, got %s' % (self.quantityP2I2, position.quantity))
            else:
                self.fail('Only expected 5 iterations. Counter = %i' % counter)
                
    def testGetDistinctPortfolios(self):
        portfolios = self.positionCollection.GetDistinctPortfolios()
        self.assertEqual(2, len(portfolios), 'Expected 2 portfolios, got %i' % len(portfolios))
        self.assertTrue(self.portfolio1 in portfolios, 'Expected self.portfolio1')
        self.assertTrue(self.portfolio2 in portfolios, 'Expected self.portfolio2')
                
        
    def testLength(self):
        self.assertEqual(6, len(self.positionCollection), 'Expected 6 positions')

    def testAdd(self):
        positionCollection = sl_sweeping.PositionCollection()
        self.assertEqual(len(positionCollection), 0, 'Expected zero items in portfolioCollection')
        
        positionCollection.Add(self.portfolio1, self.instrument1, 10, True)
        self.assertEqual(len(positionCollection), 1, 'Expected 1 item in portfolioCollection')
        self.assert_(PositionCollectionHelper.Contains(positionCollection, self.portfolio1, self.instrument1, 10, True), 'Position 1 not found')
        
        positionCollection.Add(self.portfolio1, self.instrument1, 5.2, True)
        self.assertEqual(len(positionCollection), 1, 'Expected 1 item in portfolioCollection')
        self.assert_(PositionCollectionHelper.Contains(positionCollection, self.portfolio1, self.instrument1, 15.2, True), 'Position 1 not found with quantity = 15.2')
        
        positionCollection.Add(self.portfolio1, self.instrument1, 20, False)
        self.assertEqual(len(positionCollection), 2, 'Expected 2 items in portfolioCollection')
        self.assert_(PositionCollectionHelper.Contains(positionCollection, self.portfolio1, self.instrument1, 15.2, True), 'Position 1 not found with quantity = 15.2')
        self.assert_(PositionCollectionHelper.Contains(positionCollection, self.portfolio1, self.instrument1, 20, False), 'Position 2 not found')
        
        positionCollection.Add(self.portfolio1, self.instrument2, 30, True)
        self.assertEqual(len(positionCollection), 3, 'Expected 3 items in portfolioCollection')
        self.assert_(PositionCollectionHelper.Contains(positionCollection, self.portfolio1, self.instrument1, 15.2, True), 'Position 1 not found with quantity = 15.2')
        self.assert_(PositionCollectionHelper.Contains(positionCollection, self.portfolio1, self.instrument1, 20, False), 'Position 2 not found')
        self.assert_(PositionCollectionHelper.Contains(positionCollection, self.portfolio1, self.instrument2, 30, True), 'Position 3 not found')
        
        positionCollection.Add(self.portfolio2, self.instrument1, 40, True)
        self.assertEqual(len(positionCollection), 4, 'Expected 4 items in portfolioCollection')
        self.assert_(PositionCollectionHelper.Contains(positionCollection, self.portfolio1, self.instrument1, 15.2, True), 'Position 1 not found with quantity = 15.2')
        self.assert_(PositionCollectionHelper.Contains(positionCollection, self.portfolio1, self.instrument1, 20, False), 'Position 2 not found')
        self.assert_(PositionCollectionHelper.Contains(positionCollection, self.portfolio1, self.instrument2, 30, True), 'Position 3 not found')
        self.assert_(PositionCollectionHelper.Contains(positionCollection, self.portfolio2, self.instrument1, 40, True), 'Position 4 not found')
        
    def testInstruments(self):
        instruments = self.positionCollection.Instruments()
        self.assertEqual(len(instruments), 3, 'Expected 3 instruments')
        self.assert_(self.instrument1 in instruments, 'Expected instrument1')
        self.assert_(self.instrument2 in instruments, 'Expected instrument2')
        self.assert_(self.instrument3 in instruments, 'Expected instrument3')
        
    def testGetQuantity(self):
        expectedQuantity = self.quantityP1I1 + self.quantityP2I1
        GeneralHelper.AssertTypeAndValue(self, self.positionCollection.GetQuantity(self.instrument1), expectedQuantity, decimal.Decimal, "instrument1's quantity not as expected")
        
        expectedQuantity = self.quantityP1I2 + self.quantityP1I2E + self.quantityP2I2
        GeneralHelper.AssertTypeAndValue(self, self.positionCollection.GetQuantity(self.instrument2), expectedQuantity, decimal.Decimal, "instrument2's quantity not as expected")
        
        expectedQuantity = self.quantityP1I3
        GeneralHelper.AssertTypeAndValue(self, self.positionCollection.GetQuantity(self.instrument3), expectedQuantity, decimal.Decimal, "instrument3's quantity not as expected")
        
        GeneralHelper.AssertTypeAndValue(self, self.positionCollection.GetQuantity(self.instrument4), 0, decimal.Decimal, "instrument4's quantity not as expected")

    def testGetPositionsForInstrument(self):
        instrumentPositions = self.positionCollection.GetPositionsForInstrument(self.instrument1)
        self.assertEqual(len(instrumentPositions), 2, 'Expected 2 positions')
        self.assert_(PositionCollectionHelper.Contains(instrumentPositions, self.portfolio1, self.instrument1, self.quantityP1I1, False), 'Internal position for portfolio 1 instrument 1 not found')
        self.assert_(PositionCollectionHelper.Contains(instrumentPositions, self.portfolio2, self.instrument1, self.quantityP2I1, False), 'Internal position for portfolio 2 instrument 1 not found')
        
        instrumentPositions = self.positionCollection.GetPositionsForInstrument(self.instrument2)
        self.assertEqual(len(instrumentPositions), 3, 'Expected 3 positions')
        self.assert_(PositionCollectionHelper.Contains(instrumentPositions, self.portfolio1, self.instrument2, self.quantityP1I2, False), 'Internal position for portfolio 1 instrument 2 not found')
        self.assert_(PositionCollectionHelper.Contains(instrumentPositions, self.portfolio1, self.instrument2, self.quantityP1I2E, True), 'External position for portfolio 1 instrument 2 not found')
        self.assert_(PositionCollectionHelper.Contains(instrumentPositions, self.portfolio2, self.instrument2, self.quantityP2I2, False), 'Internal position for portfolio 2 instrument 2 not found')
        
        instrumentPositions = self.positionCollection.GetPositionsForInstrument(self.instrument3)
        self.assertEqual(len(instrumentPositions), 1, 'Expected 1 positions')
        self.assert_(PositionCollectionHelper.Contains(instrumentPositions, self.portfolio1, self.instrument3, self.quantityP1I3, False), 'Internal position for portfolio 1 instrument 3 not found')
        
        instrumentPositions = self.positionCollection.GetPositionsForInstrument(self.instrument4)
        self.assertEqual(len(instrumentPositions), 0, 'Expected 0 positions')
        
    def testExists(self):
        self.assert_(self.positionCollection.Exists(self.portfolio1, self.instrument1, False), 'Expected internal position for portfolio 1 instrument 1 to exist')
        self.assert_(self.positionCollection.Exists(self.portfolio1, self.instrument2, False), 'Expected internal position for portfolio 1 instrument 2 to exist')
        self.assert_(self.positionCollection.Exists(self.portfolio1, self.instrument2, True), 'Internal internal position for portfolio 1 instrument 2 to exist')
        self.assert_(self.positionCollection.Exists(self.portfolio1, self.instrument3, False), 'Expected internal position for portfolio 1 instrument 3 to exist')
        self.assert_(self.positionCollection.Exists(self.portfolio2, self.instrument1, False), 'Expected internal position for portfolio 2 instrument 1 to exist')
        self.assert_(self.positionCollection.Exists(self.portfolio2, self.instrument2, False), 'Expected internal position for portfolio 2 instrument 2 to exist')
        self.failIf(self.positionCollection.Exists(self.portfolio1, self.instrument1, True), 'Did not expect external position for portfolio 1 instrument 1 to exist')
        self.failIf(self.positionCollection.Exists(self.portfolio2, self.instrument3, False), 'Did not expect internal position for portfolio 2 instrument 3 to exist')
        self.failIf(self.positionCollection.Exists(self.portfolio1, self.instrument4, False), 'Did not expect internal position for portfolio 1 instrument 4 to exist')
        
    def testGetPosition(self):
        positionReturned = self.positionCollection.GetPosition(self.portfolio1, self.instrument2, False)
        PositionHelper.AssertPositionProperties(self, positionReturned, self.portfolio1, self.instrument2, self.quantityP1I2, False)
        
        positionReturned = self.positionCollection.GetPosition(self.portfolio1, self.instrument2, True)
        PositionHelper.AssertPositionProperties(self, positionReturned, self.portfolio1, self.instrument2, self.quantityP1I2E, True)
        
        positionReturned = self.positionCollection.GetPosition(self.portfolio1, self.instrument3, False)
        PositionHelper.AssertPositionProperties(self, positionReturned, self.portfolio1, self.instrument3, self.quantityP1I3, False)
        
        
    def testGetPositionNotExists(self):
        self.failIf(self.positionCollection.Exists(self.portfolio1, self.instrument4, False), 'Did not expect internal position for portfolio 1 instrument 4 to exist')
        positionReturned = self.positionCollection.GetPosition(self.portfolio1, self.instrument4, False)
        PositionHelper.AssertPositionProperties(self, positionReturned, self.portfolio1, self.instrument4, 0, False)
        self.assert_(self.positionCollection.Exists(self.portfolio1, self.instrument4, False), 'Expected internal position for portfolio 1 instrument 4 to exist')
        
        self.failIf(self.positionCollection.Exists(self.portfolio2, self.instrument1, True), 'Did not expect external position for portfolio 2 instrument 1 to exist')
        positionReturned = self.positionCollection.GetPosition(self.portfolio2, self.instrument1, True)
        PositionHelper.AssertPositionProperties(self, positionReturned, self.portfolio2, self.instrument1, 0, True)
        self.assert_(self.positionCollection.Exists(self.portfolio2, self.instrument1, True), 'Expected internal position for portfolio 2 instrument 1 to exist')

    def testCover(self):
        internalDepartment1 = PartyHelper.CreatePersistantInternalDepartment()
        internalDepartment2 = PartyHelper.CreatePersistantInternalDepartment()
        
        portfolio1 = PortfolioHelper.CreatePersistantPortfolio(internalDepartment1)
        portfolio2 = PortfolioHelper.CreatePersistantPortfolio(internalDepartment2)
        portfolio3 = PortfolioHelper.CreatePersistantPortfolio(internalDepartment1)
        portfolio4 = PortfolioHelper.CreatePersistantPortfolio(internalDepartment1)
        
        instrument1 = InstrumentHelper.CreatePersistantStock()
        instrument2 = InstrumentHelper.CreatePersistantStock()
        instrument3 = InstrumentHelper.CreatePersistantStock()
        instrument4 = InstrumentHelper.CreatePersistantStock()
        
        internalRate = 0.2
        spreadRate = 0.05
        rate1 = 0.3
        rate2 = 0.4
        rate3 = 0.5
        rate4 = 0.6
        SblRatesHelper.WriteRatesFile([[sl_sweeping.SblRates._INTERNAL_KEY, '', internalRate], [sl_sweeping.SblRates._SPREAD_KEY, '', spreadRate], [instrument1.Name(), '', rate1], [instrument2.Name(), '', rate2], [instrument3.Name(), '', rate3], [instrument4.Name(), '', rate4]])
        
        internal = False
        external = True
        
        shortPositions = sl_sweeping.PositionCollection()
        shortPositions.Add(portfolio2, instrument1, -250, internal)
        shortPositions.Add(portfolio2, instrument1, -100, external)
        shortPositions.Add(portfolio2, instrument2, -150, internal)
        shortPositions.Add(portfolio2, instrument3, -100, internal)
        shortPositions.Add(portfolio2, instrument4, -50, internal)
        shortPositions.Add(portfolio2, instrument4, -150, external)
        
        longPositions = sl_sweeping.PositionCollection()
        longPositions.Add(portfolio1, instrument1, 100, internal)
        longPositions.Add(portfolio1, instrument2, 100, external)
        longPositions.Add(portfolio1, instrument3, 50, internal)
        longPositions.Add(portfolio1, instrument4, 50, internal)
        longPositions.Add(portfolio3, instrument1, 400, internal)
        longPositions.Add(portfolio3, instrument2, 50, internal)
        longPositions.Add(portfolio3, instrument4, 300, internal)
        longPositions.Add(portfolio4, instrument4, 150, internal)
        
        log = ProcessLog('TestPositionCollection.testCover')
        batchNumber = '123'
        coverDate = acm.Time().DateNow()
        validationMode = True
        applySpread = True
        partialSweeping = True
        cfdSweep = True
        instrumentCountBefore = InstrumentHelper.GetInstrumentCount()
        tradeCountBefore = TradeHelper.GetSecurityLoanCount()
        longPositions.Cover(log, batchNumber, shortPositions, coverDate, None, not validationMode, self.rates, self.prices, not applySpread, not partialSweeping, not cfdSweep)
        instrumentCountAfter = InstrumentHelper.GetInstrumentCount()
        tradeCountAfter = TradeHelper.GetSecurityLoanCount()
        
        self.assertEqual(instrumentCountAfter - instrumentCountBefore, 12, 'Expected 12 new instruments')
        self.assertEqual(tradeCountAfter - tradeCountBefore, 24, 'Expected 24 new trades')
        
        position11 = longPositions.GetPosition(portfolio1, instrument1, internal)
        position12 = longPositions.GetPosition(portfolio1, instrument2, external)
        position13 = longPositions.GetPosition(portfolio1, instrument3, internal)
        position14 = longPositions.GetPosition(portfolio1, instrument4, internal)
        
        position21 = shortPositions.GetPosition(portfolio2, instrument1, internal)
        position22 = shortPositions.GetPosition(portfolio2, instrument2, internal)
        position23 = shortPositions.GetPosition(portfolio2, instrument3, internal)
        position24 = shortPositions.GetPosition(portfolio2, instrument4, internal)
        
        position2E1 = shortPositions.GetPosition(portfolio2, instrument1, external)
        position2E2 = shortPositions.GetPosition(portfolio2, instrument2, external)
        position2E3 = shortPositions.GetPosition(portfolio2, instrument3, external)
        position2E4 = shortPositions.GetPosition(portfolio2, instrument4, external)
        
        position31 = longPositions.GetPosition(portfolio3, instrument1, internal)
        position32 = longPositions.GetPosition(portfolio3, instrument2, internal)
        position33 = longPositions.GetPosition(portfolio3, instrument3, internal)
        position34 = longPositions.GetPosition(portfolio3, instrument4, internal)
        
        position41 = longPositions.GetPosition(portfolio4, instrument1, internal)
        position42 = longPositions.GetPosition(portfolio4, instrument2, internal)
        position43 = longPositions.GetPosition(portfolio4, instrument3, internal)
        position44 = longPositions.GetPosition(portfolio4, instrument4, internal)
        
        self.assertEqual(position11.quantity, 30, 'Quantity for Internal Portfolio1, Instrument1 not as expected')
        self.assertEqual(position21.quantity, 0, 'Quantity for Internal Portfolio2, Instrument1 not as expected')
        self.assertEqual(position2E1.quantity, 0, 'Quantity for External Portfolio2, Instrument1 not as expected')
        self.assertEqual(position31.quantity, 120, 'Quantity for Internal Portfolio3, Instrument1 not as expected')
        self.assertEqual(position41.quantity, 0, 'Quantity for Internal Portfolio4, Instrument1 not as expected')
        
        self.assertEqual(position12.quantity, 0, 'Quantity for Internal Portfolio1, Instrument2 not as expected')
        self.assertEqual(position22.quantity, 0, 'Quantity for Internal Portfolio2, Instrument2 not as expected')
        self.assertEqual(position2E2.quantity, 0, 'Quantity for External Portfolio2, Instrument2 not as expected')
        self.assertEqual(position32.quantity, 0, 'Quantity for Internal Portfolio3, Instrument2 not as expected')
        self.assertEqual(position42.quantity, 0, 'Quantity for Internal Portfolio4, Instrument2 not as expected')
        
        self.assertEqual(position13.quantity, 50, 'Quantity for Internal Portfolio1, Instrument3 not as expected')
        self.assertEqual(position23.quantity, -100, 'Quantity for Internal Portfolio2, Instrument3 not as expected')
        self.assertEqual(position2E3.quantity, 0, 'Quantity for External Portfolio2, Instrument3 not as expected')
        self.assertEqual(position33.quantity, 0, 'Quantity for Internal Portfolio3, Instrument3 not as expected')
        self.assertEqual(position43.quantity, 0, 'Quantity for Internal Portfolio4, Instrument3 not as expected')
        
        self.assertEqual(position14.quantity, 30, 'Quantity for Internal Portfolio1, Instrument4 not as expected')
        self.assertEqual(position24.quantity, 0, 'Quantity for Internal Portfolio2, Instrument4 not as expected')
        self.assertEqual(position2E4.quantity, 0, 'Quantity for External Portfolio2, Instrument4 not as expected')
        self.assertEqual(position34.quantity, 180, 'Quantity for Internal Portfolio3, Instrument4 not as expected')
        self.assertEqual(position44.quantity, 90, 'Quantity for Internal Portfolio4, Instrument4 not as expected')
        
        startDate = acm.Time().DateNow()
        endDate = acm.FCalendar['ZAR Johannesburg'].AdjustBankingDays(startDate, 1)
        
        expectedTradeStatus = 'FO Confirmed'
        expectedVat = bool(acm.FAdditionalInfoSpec['SL_VAT'].DefaultValue())
        expectedSlCfd = False
        trades11 = TradeHelper.GetTrades(portfolio1, instrument1)
        self.assertEqual(len(trades11), 2, 'Expected 2 trades for Portfolio1, Instrument1')
        self.assert_(TradeHelper.Contains(trades11, startDate, endDate, instrument1, -50, 0, 1, 'Principal', \
        'Internal', expectedVat, portfolio1, portfolio2, portfolio2.PortfolioOwner(), portfolio1.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate), 'Trade 1 not found in trades11')
        self.assert_(TradeHelper.Contains(trades11, startDate, endDate, instrument1, -20, 0, 1, 'Principal', \
        'Internal', expectedVat, portfolio1, portfolio2, portfolio2.PortfolioOwner(), portfolio1.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate), 'Trade 2 not found in trades11')
        
        trades21 = TradeHelper.GetTrades(portfolio2, instrument1)
        self.assertEqual(len(trades21), 4, 'Expected 4 trades for Portfolio2, Instrument1')
        self.assert_(TradeHelper.Contains(trades21, startDate, endDate, instrument1, 200, 0, 1, 'Principal', 'Internal', \
        expectedVat, portfolio2, portfolio3, portfolio3.PortfolioOwner(), portfolio2.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate), 'Trade 1 not found in trades21')
        self.assert_(TradeHelper.Contains(trades21, startDate, endDate, instrument1, 50, 0, 1, 'Principal', 'Internal', \
        expectedVat, portfolio2, portfolio1, portfolio1.PortfolioOwner(), portfolio2.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate), 'Trade 2 not found in trades21')
        self.assert_(TradeHelper.Contains(trades21, startDate, endDate, instrument1, 20, 0, 1, 'Principal', 'Internal', \
        expectedVat, portfolio2, portfolio1, portfolio1.PortfolioOwner(), portfolio2.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate), 'Trade 3 not found in trades21')
        self.assert_(TradeHelper.Contains(trades21, startDate, endDate, instrument1, 80, 0, 1, 'Principal', 'Internal', \
        expectedVat, portfolio2, portfolio3, portfolio3.PortfolioOwner(), portfolio2.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate), 'Trade 4 not found in trades21')
        
        trades31 = TradeHelper.GetTrades(portfolio3, instrument1)
        self.assertEqual(len(trades31), 2, 'Expected 2 trades for Portfolio3, Instrument1')
        self.assert_(TradeHelper.Contains(trades31, startDate, endDate, instrument1, -200, 0, 1, 'Principal', \
        'Internal', expectedVat, portfolio3, portfolio2, portfolio2.PortfolioOwner(), portfolio3.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate), 'Trade 1 not found in trades31')
        self.assert_(TradeHelper.Contains(trades31, startDate, endDate, instrument1, -80, 0, 1, 'Principal', \
        'Internal', expectedVat, portfolio3, portfolio2, portfolio2.PortfolioOwner(), portfolio3.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate), 'Trade 2 not found in trades31')

        trades22 = TradeHelper.GetTrades(portfolio2, instrument2)
        self.assertEqual(len(trades22), 2, 'Expected 2 trades for Portfolio2, Instrument2')
        self.assert_(TradeHelper.Contains(trades22, startDate, endDate, instrument2, 100, 0, 1, 'Principal', 'External', \
        expectedVat, portfolio2, portfolio1, portfolio1.PortfolioOwner(), portfolio2.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, rate2), 'Trade 1 not found in trades22')
        self.assert_(TradeHelper.Contains(trades22, startDate, endDate, instrument2, 50, 0, 1, 'Principal', 'Internal', \
        expectedVat, portfolio2, portfolio3, portfolio3.PortfolioOwner(), portfolio2.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate), 'Trade 2 not found in trades22')
        
        trades12 = TradeHelper.GetTrades(portfolio1, instrument2)
        self.assertEqual(len(trades12), 1, 'Expected 1 trade for Portfolio1, Instrument2')
        self.assert_(TradeHelper.Contains(trades12, startDate, endDate, instrument2, -100, 0, 1, 'Principal', \
        'External', expectedVat, portfolio1, portfolio2, portfolio2.PortfolioOwner(), portfolio1.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, rate2), 'Trade 1 not found in trades12')
        
        trades32 = TradeHelper.GetTrades(portfolio3, instrument2)
        self.assertEqual(len(trades32), 1, 'Expected 1 trade for Portfolio3, Instrument2')
        self.assert_(TradeHelper.Contains(trades32, startDate, endDate, instrument2, -50, 0, 1, 'Principal', \
        'Internal', expectedVat, portfolio3, portfolio2, portfolio2.PortfolioOwner(), portfolio3.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate), 'Trade 1 not found in trades32')
        
        trades03 = TradeHelper.GetTrades(None, instrument3)
        self.assertEqual(len(trades03), 0, 'Expected zero trades for Instrument3')
        
        trades14 = TradeHelper.GetTrades(portfolio1, instrument4)
        self.assertEqual(len(trades14), 2, 'Expected 2 trades for Portfolio1, Instrument4')
        self.assert_(TradeHelper.Contains(trades14, startDate, endDate, instrument4, -5, 0, 1, 'Principal', \
        'Internal', expectedVat, portfolio1, portfolio2, portfolio2.PortfolioOwner(), portfolio1.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate), 'Trade 1 not found in trades14')
        self.assert_(TradeHelper.Contains(trades14, startDate, endDate, instrument4, -15, 0, 1, 'Principal', \
        'Internal', expectedVat, portfolio1, portfolio2, portfolio2.PortfolioOwner(), portfolio1.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate), 'Trade 2 not found in trades14')
        
        trades24 = TradeHelper.GetTrades(portfolio2, instrument4)
        self.assertEqual(len(trades24), 6, 'Expected 6 trades for Portfolio2, Instrument4')
        self.assert_(TradeHelper.Contains(trades24, startDate, endDate, instrument4, 15, 0, 1, 'Principal', \
        'Internal', expectedVat, portfolio2, portfolio1, portfolio1.PortfolioOwner(), portfolio2.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate), 'Trade 1 not found in trades24')
        self.assert_(TradeHelper.Contains(trades24, startDate, endDate, instrument4, 5, 0, 1, 'Principal', 
        'Internal', expectedVat, portfolio2, portfolio1, portfolio1.PortfolioOwner(), portfolio2.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate), 'Trade 2 not found in trades24')
        self.assert_(TradeHelper.Contains(trades24, startDate, endDate, instrument4, 15, 0, 1, 'Principal', 'Internal', \
        expectedVat, portfolio2, portfolio4, portfolio4.PortfolioOwner(), portfolio2.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate), 'Trade 3 not found in trades24')
        self.assert_(TradeHelper.Contains(trades24, startDate, endDate, instrument4, 90, 0, 1, 'Principal', 'Internal', \
        expectedVat, portfolio2, portfolio3, portfolio3.PortfolioOwner(), portfolio2.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate), 'Trade 4 not found in trades24')
        self.assert_(TradeHelper.Contains(trades24, startDate, endDate, instrument4, 30, 0, 1, 'Principal', \
        'Internal', expectedVat, portfolio2, portfolio3, portfolio3.PortfolioOwner(), portfolio2.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate), 'Trade 5 not found in trades24')
        self.assert_(TradeHelper.Contains(trades24, startDate, endDate, instrument4, 45, 0, 1, 'Principal', 'Internal', \
        expectedVat, portfolio2, portfolio4, portfolio4.PortfolioOwner(), portfolio2.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate), 'Trade 6 not found in trades24')
        
        trades34 = TradeHelper.GetTrades(portfolio3, instrument4)
        self.assertEqual(len(trades34), 2, 'Expected 2 trades for Portfolio3, Instrument4')
        self.assert_(TradeHelper.Contains(trades34, startDate, endDate, instrument4, -30, 0, 1, 'Principal', \
        'Internal', expectedVat, portfolio3, portfolio2, portfolio2.PortfolioOwner(), portfolio3.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate), 'Trade 2 not found in trades34')
        self.assert_(TradeHelper.Contains(trades34, startDate, endDate, instrument4, -90, 0, 1, 'Principal', \
        'Internal', expectedVat, portfolio3, portfolio2, portfolio2.PortfolioOwner(), portfolio3.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate), 'Trade 3 not found in trades34')
        
        trades44 = TradeHelper.GetTrades(portfolio4, instrument4)
        self.assertEqual(len(trades44), 2, 'Expected 2 trades for Portfolio4, Instrument4')
        self.assert_(TradeHelper.Contains(trades44, startDate, endDate, instrument4, -15, 0, 1, 'Principal', \
        'Internal', expectedVat, portfolio4, portfolio2, portfolio2.PortfolioOwner(), portfolio4.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate), 'Trade1 not found in trades44')
        self.assert_(TradeHelper.Contains(trades44, startDate, endDate, instrument4, -45, 0, 1, 'Principal', \
        'Internal', expectedVat, portfolio4, portfolio2, portfolio2.PortfolioOwner(), portfolio4.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate), 'Trade2 not found in trades44')

    def testCoverWithPartialSweeping(self):
        internalDepartment1 = PartyHelper.CreatePersistantInternalDepartment()
        internalDepartment2 = PartyHelper.CreatePersistantInternalDepartment()
        
        portfolio1 = PortfolioHelper.CreatePersistantPortfolio(internalDepartment1)
        portfolio2 = PortfolioHelper.CreatePersistantPortfolio(internalDepartment2)
        portfolio3 = PortfolioHelper.CreatePersistantPortfolio(internalDepartment1)
        portfolio4 = PortfolioHelper.CreatePersistantPortfolio(internalDepartment1)
        
        instrument1 = InstrumentHelper.CreatePersistantStock()
        instrument2 = InstrumentHelper.CreatePersistantStock()
        instrument3 = InstrumentHelper.CreatePersistantStock()
        instrument4 = InstrumentHelper.CreatePersistantStock()
        
        internalRate = 0.2
        spreadRate = 0.05
        rate1 = 0.3
        rate2 = 0.4
        rate3 = 0.5
        rate4 = 0.6
        SblRatesHelper.WriteRatesFile([[sl_sweeping.SblRates._INTERNAL_KEY, '', internalRate], [sl_sweeping.SblRates._SPREAD_KEY, '', spreadRate], [instrument1.Name(), '', rate1], [instrument2.Name(), '', rate2], [instrument3.Name(), '', rate3], [instrument4.Name(), '', rate4]])
        
        internal = False
        external = True
        
        shortPositions = sl_sweeping.PositionCollection()
        shortPositions.Add(portfolio2, instrument1, -250, internal)
        shortPositions.Add(portfolio2, instrument1, -100, external)
        shortPositions.Add(portfolio2, instrument2, -150, internal)
        shortPositions.Add(portfolio2, instrument3, -75, internal)
        shortPositions.Add(portfolio2, instrument3, -25, external)
        shortPositions.Add(portfolio2, instrument4, -50, internal)
        shortPositions.Add(portfolio2, instrument4, -150, external)
        
        longPositions = sl_sweeping.PositionCollection()
        longPositions.Add(portfolio1, instrument1, 100, internal)
        longPositions.Add(portfolio1, instrument2, 100, internal)
        longPositions.Add(portfolio1, instrument3, 60, internal)
        longPositions.Add(portfolio1, instrument4, 50, internal)
        longPositions.Add(portfolio3, instrument1, 400, internal)
        longPositions.Add(portfolio3, instrument2, 50, internal)
        longPositions.Add(portfolio3, instrument3, 20, internal)
        longPositions.Add(portfolio3, instrument4, 300, internal)
        longPositions.Add(portfolio4, instrument4, 150, external)
        
        log = ProcessLog('TestPositionCollection.testCoverWithPartialSweeping')
        batchNumber = '1234'
        coverDate = acm.Time().DateNow()
        validationMode = True
        applySpread = True
        partialSweeping = True
        cfdSweep = True
        instrumentCountBefore = InstrumentHelper.GetInstrumentCount()
        tradeCountBefore = TradeHelper.GetSecurityLoanCount()
        longPositions.Cover(log, batchNumber, shortPositions, coverDate, None, not validationMode, self.rates, self.prices, applySpread, partialSweeping, not cfdSweep)
        instrumentCountAfter = InstrumentHelper.GetInstrumentCount()
        tradeCountAfter = TradeHelper.GetSecurityLoanCount()
        
        self.assertEqual(instrumentCountAfter - instrumentCountBefore, 16, 'Expected 16 new instruments')
        self.assertEqual(tradeCountAfter - tradeCountBefore, 32, 'Expected 32 new trades')
        
        position11 = longPositions.GetPosition(portfolio1, instrument1, internal)
        position12 = longPositions.GetPosition(portfolio1, instrument2, internal)
        position13 = longPositions.GetPosition(portfolio1, instrument3, internal)
        position14 = longPositions.GetPosition(portfolio1, instrument4, internal)
        
        position21 = shortPositions.GetPosition(portfolio2, instrument1, internal)
        position22 = shortPositions.GetPosition(portfolio2, instrument2, internal)
        position23 = shortPositions.GetPosition(portfolio2, instrument3, internal)
        position24 = shortPositions.GetPosition(portfolio2, instrument4, internal)
        
        position2E1 = shortPositions.GetPosition(portfolio2, instrument1, external)
        position2E2 = shortPositions.GetPosition(portfolio2, instrument2, external)
        position2E3 = shortPositions.GetPosition(portfolio2, instrument3, external)
        position2E4 = shortPositions.GetPosition(portfolio2, instrument4, external)
        
        position31 = longPositions.GetPosition(portfolio3, instrument1, internal)
        position32 = longPositions.GetPosition(portfolio3, instrument2, internal)
        position33 = longPositions.GetPosition(portfolio3, instrument3, internal)
        position34 = longPositions.GetPosition(portfolio3, instrument4, internal)
        
        position41 = longPositions.GetPosition(portfolio4, instrument1, internal)
        position42 = longPositions.GetPosition(portfolio4, instrument2, internal)
        position43 = longPositions.GetPosition(portfolio4, instrument3, internal)
        position44 = longPositions.GetPosition(portfolio4, instrument4, external)
        
        self.assertEqual(position11.quantity, 30, 'Quantity for Internal Portfolio1, Instrument1 not as expected')
        self.assertEqual(position21.quantity, 0, 'Quantity for Internal Portfolio2, Instrument1 not as expected')
        self.assertEqual(position2E1.quantity, 0, 'Quantity for External Portfolio2, Instrument1 not as expected')
        self.assertEqual(position31.quantity, 120, 'Quantity for Internal Portfolio3, Instrument1 not as expected')
        self.assertEqual(position41.quantity, 0, 'Quantity for Internal Portfolio4, Instrument1 not as expected')
        
        self.assertEqual(position12.quantity, 0, 'Quantity for Internal Portfolio1, Instrument2 not as expected')
        self.assertEqual(position22.quantity, 0, 'Quantity for Internal Portfolio2, Instrument2 not as expected')
        self.assertEqual(position2E2.quantity, 0, 'Quantity for External Portfolio2, Instrument2 not as expected')
        self.assertEqual(position32.quantity, 0, 'Quantity for Internal Portfolio3, Instrument2 not as expected')
        self.assertEqual(position42.quantity, 0, 'Quantity for Internal Portfolio4, Instrument2 not as expected')
        
        self.assertEqual(position13.quantity, 0, 'Quantity for Internal Portfolio1, Instrument3 not as expected')
        self.assertEqual(position23.quantity, -15, 'Quantity for Internal Portfolio2, Instrument3 not as expected')
        self.assertEqual(position2E3.quantity, -5, 'Quantity for External Portfolio2, Instrument3 not as expected')
        self.assertEqual(position33.quantity, 0, 'Quantity for Internal Portfolio3, Instrument3 not as expected')
        self.assertEqual(position43.quantity, 0, 'Quantity for Internal Portfolio4, Instrument3 not as expected')
        
        self.assertEqual(position14.quantity, 30, 'Quantity for Internal Portfolio1, Instrument4 not as expected')
        self.assertEqual(position24.quantity, 0, 'Quantity for Internal Portfolio2, Instrument4 not as expected')
        self.assertEqual(position2E4.quantity, 0, 'Quantity for External Portfolio2, Instrument4 not as expected')
        self.assertEqual(position34.quantity, 180, 'Quantity for Internal Portfolio3, Instrument4 not as expected')
        self.assertEqual(position44.quantity, 90, 'Quantity for Internal Portfolio4, Instrument4 not as expected')
        
        startDate = acm.Time().DateNow()
        endDate = acm.FCalendar['ZAR Johannesburg'].AdjustBankingDays(startDate, 1)
        
        expectedTradeStatus = 'FO Confirmed'
        expectedVat = bool(acm.FAdditionalInfoSpec['SL_VAT'].DefaultValue())
        expectedSlCfd = False
        trades11 = TradeHelper.GetTrades(portfolio1, instrument1)
        self.assertEqual(len(trades11), 2, 'Expected 2 trades for Portfolio1, Instrument1')
        self.assert_(TradeHelper.Contains(trades11, startDate, endDate, instrument1, -50, 0, 1, 'Principal', \
        'Internal', expectedVat, portfolio1, portfolio2, portfolio2.PortfolioOwner(), portfolio1.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate + spreadRate), 'Trade 1 not found in trades11')
        self.assert_(TradeHelper.Contains(trades11, startDate, endDate, instrument1, -20, 0, 1, 'Principal', \
        'Internal', expectedVat, portfolio1, portfolio2, portfolio2.PortfolioOwner(), portfolio1.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate + spreadRate), 'Trade 2 not found in trades11')
        
        trades21 = TradeHelper.GetTrades(portfolio2, instrument1)
        self.assertEqual(len(trades21), 4, 'Expected 4 trades for Portfolio2, Instrument1')
        self.assert_(TradeHelper.Contains(trades21, startDate, endDate, instrument1, 200, 0, 1, 'Principal', 'Internal', \
        expectedVat, portfolio2, portfolio3, portfolio3.PortfolioOwner(), portfolio2.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate + spreadRate), 'Trade 1 not found in trades21')
        self.assert_(TradeHelper.Contains(trades21, startDate, endDate, instrument1, 50, 0, 1, 'Principal', 'Internal', \
        expectedVat, portfolio2, portfolio1, portfolio1.PortfolioOwner(), portfolio2.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate + spreadRate), 'Trade 2 not found in trades21')
        self.assert_(TradeHelper.Contains(trades21, startDate, endDate, instrument1, 20, 0, 1, 'Principal', 'Internal', \
        expectedVat, portfolio2, portfolio1, portfolio1.PortfolioOwner(), portfolio2.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate + spreadRate), 'Trade 3 not found in trades21')
        self.assert_(TradeHelper.Contains(trades21, startDate, endDate, instrument1, 80, 0, 1, 'Principal', 'Internal', \
        expectedVat, portfolio2, portfolio3, portfolio3.PortfolioOwner(), portfolio2.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate + spreadRate), 'Trade 4 not found in trades21')
        
        trades31 = TradeHelper.GetTrades(portfolio3, instrument1)
        self.assertEqual(len(trades31), 2, 'Expected 2 trades for Portfolio3, Instrument1')
        self.assert_(TradeHelper.Contains(trades31, startDate, endDate, instrument1, -200, 0, 1, 'Principal', \
        'Internal', expectedVat, portfolio3, portfolio2, portfolio2.PortfolioOwner(), portfolio3.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate + spreadRate), 'Trade 1 not found in trades31')
        self.assert_(TradeHelper.Contains(trades31, startDate, endDate, instrument1, -80, 0, 1, 'Principal', \
        'Internal', expectedVat, portfolio3, portfolio2, portfolio2.PortfolioOwner(), portfolio3.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate + spreadRate), 'Trade 2 not found in trades31')

        trades22 = TradeHelper.GetTrades(portfolio2, instrument2)
        self.assertEqual(len(trades22), 2, 'Expected 2 trades for Portfolio2, Instrument2')
        self.assert_(TradeHelper.Contains(trades22, startDate, endDate, instrument2, 100, 0, 1, 'Principal', 'Internal', \
        expectedVat, portfolio2, portfolio1, portfolio1.PortfolioOwner(), portfolio2.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate + spreadRate), 'Trade 1 not found in trades22')
        self.assert_(TradeHelper.Contains(trades22, startDate, endDate, instrument2, 50, 0, 1, 'Principal', 'Internal', \
        expectedVat, portfolio2, portfolio3, portfolio3.PortfolioOwner(), portfolio2.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate + spreadRate), 'Trade 2 not found in trades22')
        
        trades12 = TradeHelper.GetTrades(portfolio1, instrument2)
        self.assertEqual(len(trades12), 1, 'Expected 1 trade for Portfolio1, Instrument2')
        self.assert_(TradeHelper.Contains(trades12, startDate, endDate, instrument2, -100, 0, 1, 'Principal', \
        'Internal', expectedVat, portfolio1, portfolio2, portfolio2.PortfolioOwner(), portfolio1.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate + spreadRate), 'Trade 1 not found in trades22')
        
        trades32 = TradeHelper.GetTrades(portfolio3, instrument2)
        self.assertEqual(len(trades32), 1, 'Expected 1 trade for Portfolio3, Instrument2')
        self.assert_(TradeHelper.Contains(trades32, startDate, endDate, instrument2, -50, 0, 1, 'Principal', \
        'Internal', expectedVat, portfolio3, portfolio2, portfolio2.PortfolioOwner(), portfolio3.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate + spreadRate), 'Trade 1 not found in trades32')
        
        trades13 = TradeHelper.GetTrades(portfolio1, instrument3)
        self.assertEqual(len(trades13), 2, 'Expected 2 trades for Portfolio1, Instrument3')
        self.assert_(TradeHelper.Contains(trades13, startDate, endDate, instrument3, -45, 0, 1, 'Principal', \
        'Internal', expectedVat, portfolio1, portfolio2, portfolio2.PortfolioOwner(), portfolio1.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate + spreadRate), 'Trade 1 not found in trades13')
        self.assert_(TradeHelper.Contains(trades13, startDate, endDate, instrument3, -15, 0, 1, 'Principal', \
        'Internal', expectedVat, portfolio1, portfolio2, portfolio2.PortfolioOwner(), portfolio1.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate + spreadRate), 'Trade 2 not found in trades13')
        
        trades23 = TradeHelper.GetTrades(portfolio2, instrument3)
        self.assertEqual(len(trades23), 4, 'Expected 4 trades for Portfolio2, Instrument3')
        self.assert_(TradeHelper.Contains(trades23, startDate, endDate, instrument3, 45, 0, 1, 'Principal', \
        'Internal', expectedVat, portfolio2, portfolio1, portfolio1.PortfolioOwner(), portfolio2.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate + spreadRate), 'Trade 1 not found in trades23')
        self.assert_(TradeHelper.Contains(trades23, startDate, endDate, instrument3, 15, 0, 1, 'Principal', \
        'Internal', expectedVat, portfolio2, portfolio1, portfolio1.PortfolioOwner(), portfolio2.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate + spreadRate), 'Trade 2 not found in trades23')
        self.assert_(TradeHelper.Contains(trades23, startDate, endDate, instrument3, 15, 0, 1, 'Principal', \
        'Internal', expectedVat, portfolio2, portfolio3, portfolio3.PortfolioOwner(), portfolio2.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate + spreadRate), 'Trade 3 not found in trades23')
        self.assert_(TradeHelper.Contains(trades23, startDate, endDate, instrument3, 5, 0, 1, 'Principal', \
        'Internal', expectedVat, portfolio2, portfolio3, portfolio3.PortfolioOwner(), portfolio2.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate + spreadRate), 'Trade 4 not found in trades23')
        
        trades33 = TradeHelper.GetTrades(portfolio3, instrument3)
        self.assertEqual(len(trades33), 2, 'Expected 2 trades for Portfolio3, Instrument3')
        self.assert_(TradeHelper.Contains(trades33, startDate, endDate, instrument3, -15, 0, 1, 'Principal', \
        'Internal', expectedVat, portfolio3, portfolio2, portfolio2.PortfolioOwner(), portfolio3.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate + spreadRate), 'Trade 1 not found in trades33')
        self.assert_(TradeHelper.Contains(trades33, startDate, endDate, instrument3, -5, 0, 1, 'Principal', \
        'Internal', expectedVat, portfolio3, portfolio2, portfolio2.PortfolioOwner(), portfolio3.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate + spreadRate), 'Trade 2 not found in trades33')
        
        trades14 = TradeHelper.GetTrades(portfolio1, instrument4)
        self.assertEqual(len(trades14), 2, 'Expected 2 trades for Portfolio1, Instrument4')
        self.assert_(TradeHelper.Contains(trades14, startDate, endDate, instrument4, -5, 0, 1, 'Principal', \
        'Internal', expectedVat, portfolio1, portfolio2, portfolio2.PortfolioOwner(), portfolio1.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate + spreadRate), 'Trade 1 not found in trades14')
        self.assert_(TradeHelper.Contains(trades14, startDate, endDate, instrument4, -15, 0, 1, 'Principal', \
        'Internal', expectedVat, portfolio1, portfolio2, portfolio2.PortfolioOwner(), portfolio1.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate + spreadRate), 'Trade 2 not found in trades14')
        
        trades24 = TradeHelper.GetTrades(portfolio2, instrument4)            
        self.assertEqual(len(trades24), 6, 'Expected 6 trades for Portfolio2, Instrument4')
        self.assert_(TradeHelper.Contains(trades24, startDate, endDate, instrument4, 15, 0, 1, 'Principal', \
        'Internal', expectedVat, portfolio2, portfolio1, portfolio1.PortfolioOwner(), portfolio2.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate + spreadRate), 'Trade 1 not found in trades24')
        self.assert_(TradeHelper.Contains(trades24, startDate, endDate, instrument4, 5, 0, 1, 'Principal', 
        'Internal', expectedVat, portfolio2, portfolio1, portfolio1.PortfolioOwner(), portfolio2.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate + spreadRate), 'Trade 2 not found in trades24')
        self.assert_(TradeHelper.Contains(trades24, startDate, endDate, instrument4, 15, 0, 1, 'Principal', 'External', \
        expectedVat, portfolio2, portfolio4, portfolio4.PortfolioOwner(), portfolio2.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, rate4), 'Trade 3 not found in trades24')
        self.assert_(TradeHelper.Contains(trades24, startDate, endDate, instrument4, 90, 0, 1, 'Principal', 'Internal', \
        expectedVat, portfolio2, portfolio3, portfolio3.PortfolioOwner(), portfolio2.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate + spreadRate), 'Trade 4 not found in trades24')
        self.assert_(TradeHelper.Contains(trades24, startDate, endDate, instrument4, 30, 0, 1, 'Principal', \
        'Internal', expectedVat, portfolio2, portfolio3, portfolio3.PortfolioOwner(), portfolio2.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate + spreadRate), 'Trade 5 not found in trades24')
        self.assert_(TradeHelper.Contains(trades24, startDate, endDate, instrument4, 45, 0, 1, 'Principal', 'External', \
        expectedVat, portfolio2, portfolio4, portfolio4.PortfolioOwner(), portfolio2.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, rate4), 'Trade 6 not found in trades24')
        
        trades34 = TradeHelper.GetTrades(portfolio3, instrument4)
        self.assertEqual(len(trades34), 2, 'Expected 2 trades for Portfolio3, Instrument4')
        self.assert_(TradeHelper.Contains(trades34, startDate, endDate, instrument4, -30, 0, 1, 'Principal', \
        'Internal', expectedVat, portfolio3, portfolio2, portfolio2.PortfolioOwner(), portfolio3.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate + spreadRate), 'Trade 2 not found in trades34')
        self.assert_(TradeHelper.Contains(trades34, startDate, endDate, instrument4, -90, 0, 1, 'Principal', \
        'Internal', expectedVat, portfolio3, portfolio2, portfolio2.PortfolioOwner(), portfolio3.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, internalRate + spreadRate), 'Trade 3 not found in trades34')
        
        trades44 = TradeHelper.GetTrades(portfolio4, instrument4)
        self.assertEqual(len(trades44), 2, 'Expected 2 trades for Portfolio4, Instrument4')
        self.assert_(TradeHelper.Contains(trades44, startDate, endDate, instrument4, -15, 0, 1, 'Principal', \
        'External', expectedVat, portfolio4, portfolio2, portfolio2.PortfolioOwner(), portfolio4.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, rate4), 'Trade1 not found in trades44')
        self.assert_(TradeHelper.Contains(trades44, startDate, endDate, instrument4, -45, 0, 1, 'Principal', \
        'External', expectedVat, portfolio4, portfolio2, portfolio2.PortfolioOwner(), portfolio4.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, rate4), 'Trade2 not found in trades44')
        
    def testCoverCfdPositions(self):
        internalDepartment = PartyHelper.CreatePersistantInternalDepartment()
        
        portfolio1 = PortfolioHelper.CreatePersistantPortfolio(internalDepartment)
        portfolio2 = PortfolioHelper.CreatePersistantPortfolio(internalDepartment)
        portfolio3 = PortfolioHelper.CreatePersistantPortfolio(internalDepartment)
        
        instrument1 = InstrumentHelper.CreatePersistantStock()
        instrument2 = InstrumentHelper.CreatePersistantStock()
        
        internalRate = 0.2
        spreadRate = 0.05
        rate1 = 0.3
        rate2 = 0.4
        SblRatesHelper.WriteRatesFile([[sl_sweeping.SblRates._INTERNAL_KEY, '', internalRate], [sl_sweeping.SblRates._SPREAD_KEY, '', spreadRate], [instrument1.Name(), '', rate1], [instrument2.Name(), '', rate2]])
        
        cfdInternalRate = internalRate + 0.02
        cfdSpreadRate = spreadRate + 0.04
        cfdRate1 = rate1 + 0.05
        cfdRate2 = rate2 + 0.05
        SblRatesHelper.WriteCfdRatesFile([[sl_sweeping.SblRates._INTERNAL_KEY, '', cfdInternalRate], [sl_sweeping.SblRates._SPREAD_KEY, '', cfdSpreadRate], [instrument1.Name(), '', cfdRate1], [instrument2.Name(), '', cfdRate2]])
        
        internal = False
        external = True
        
        shortPositions = sl_sweeping.PositionCollection()
        shortPositions.Add(portfolio1, instrument1, -100, internal)
        shortPositions.Add(portfolio2, instrument2, -75, internal)
        
        longPositions = sl_sweeping.PositionCollection()
        longPositions.Add(portfolio1, instrument2, 100, external)
        longPositions.Add(portfolio2, instrument1, 50, internal)
        longPositions.Add(portfolio3, instrument1, 150, external)
        longPositions.Add(portfolio3, instrument2, 200, external)
        
        log = ProcessLog('TestPositionCollection.testCoverCfdPositions')
        batchNumber = '456789'
        coverDate = acm.Time().DateNow()
        validationMode = True
        applySpread = True
        partialSweeping = True
        cfdSweep = True
        cfdRates = sl_sweeping.SblRates(SblRatesHelper.cfdFilepath, 3)
        instrumentCountBefore = InstrumentHelper.GetInstrumentCount()
        tradeCountBefore = TradeHelper.GetSecurityLoanCount()
        longPositions.Cover(log, batchNumber, shortPositions, coverDate, None, not validationMode, cfdRates, self.prices, not applySpread, not partialSweeping, cfdSweep)
        instrumentCountAfter = InstrumentHelper.GetInstrumentCount()
        tradeCountAfter = TradeHelper.GetSecurityLoanCount()
        
        self.assertEqual(instrumentCountAfter - instrumentCountBefore, 4, 'Expected 4 new instruments')
        self.assertEqual(tradeCountAfter - tradeCountBefore, 8, 'Expected 8 new trades')
        
        position11 = shortPositions.GetPosition(portfolio1, instrument1, internal)
        position12 = longPositions.GetPosition(portfolio1, instrument2, external)
        
        position21 = longPositions.GetPosition(portfolio2, instrument1, internal)
        position22 = shortPositions.GetPosition(portfolio2, instrument2, internal)
        
        position31 = longPositions.GetPosition(portfolio3, instrument1, external)
        position32 = longPositions.GetPosition(portfolio3, instrument2, external)
        
        self.assertEqual(position11.quantity, 0, 'Quantity for Portfolio1, Instrument1 not as expected')
        self.assertEqual(position21.quantity, 25, 'Quantity for Portfolio2, Instrument1 not as expected')
        self.assertEqual(position31.quantity, 75, 'Quantity for Portfolio3, Instrument1 not as expected')
        
        self.assertEqual(position12.quantity, 75, 'Quantity for Portfolio1, Instrument2 not as expected')
        self.assertEqual(position22.quantity, 0, 'Quantity for Portfolio2, Instrument2 not as expected')
        self.assertEqual(position32.quantity, 150, 'Quantity for Portfolio3, Instrument2 not as expected')
        
        startDate = acm.Time().DateNow()
        endDate = acm.FCalendar['ZAR Johannesburg'].AdjustBankingDays(startDate, 1)
        
        expectedTradeStatus = 'FO Confirmed'
        expectedVat = bool(acm.FAdditionalInfoSpec['SL_VAT'].DefaultValue())
        expectedSlCfd = True

        trades11 = TradeHelper.GetTrades(portfolio1, instrument1)
        self.assertEqual(len(trades11), 2, 'Expected 2 trades for Portfolio1, Instrument1')
        self.assert_(TradeHelper.Contains(trades11, startDate, endDate, instrument1, 25, 0, 1, 'Principal', \
        'Internal', expectedVat, portfolio1, portfolio2, portfolio2.PortfolioOwner(), portfolio1.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, cfdInternalRate), 'Trade 1 not found in trades11')
        self.assert_(TradeHelper.Contains(trades11, startDate, endDate, instrument1, 75, 0, 1, 'Principal', \
        'External', expectedVat, portfolio1, portfolio3, portfolio3.PortfolioOwner(), portfolio1.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, cfdRate1), 'Trade 2 not found in trades11')
        
        trades21 = TradeHelper.GetTrades(portfolio2, instrument1)
        self.assertEqual(len(trades21), 1, 'Expected 1 trade for Portfolio2, Instrument1')
        self.assert_(TradeHelper.Contains(trades21, startDate, endDate, instrument1, -25, 0, 1, 'Principal', 'Internal', \
        expectedVat, portfolio2, portfolio1, portfolio1.PortfolioOwner(), portfolio2.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, cfdInternalRate), 'Trade 1 not found in trades21')
        
        trades31 = TradeHelper.GetTrades(portfolio3, instrument1)
        self.assertEqual(len(trades31), 1, 'Expected 1 trade1 for Portfolio3, Instrument1')
        self.assert_(TradeHelper.Contains(trades31, startDate, endDate, instrument1, -75, 0, 1, 'Principal', \
        'External', expectedVat, portfolio3, portfolio1, portfolio1.PortfolioOwner(), portfolio3.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, cfdRate1), 'Trade 1 not found in trades31')

        trades12 = TradeHelper.GetTrades(portfolio1, instrument2)
        self.assertEqual(len(trades12), 1, 'Expected 1 trade for Portfolio1, Instrument2')
        self.assert_(TradeHelper.Contains(trades12, startDate, endDate, instrument2, -25, 0, 1, 'Principal', \
        'External', expectedVat, portfolio1, portfolio2, portfolio2.PortfolioOwner(), portfolio1.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, cfdRate2), 'Trade 1 not found in trades12')
        
        trades22 = TradeHelper.GetTrades(portfolio2, instrument2)
        self.assertEqual(len(trades22), 2, 'Expected 2 trade for Portfolio2, Instrument2')
        self.assert_(TradeHelper.Contains(trades22, startDate, endDate, instrument2, 25, 0, 1, 'Principal', \
        'External', expectedVat, portfolio2, portfolio1, portfolio1.PortfolioOwner(), portfolio2.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, cfdRate2), 'Trade 1 not found in trades22')
        self.assert_(TradeHelper.Contains(trades22, startDate, endDate, instrument2, 50, 0, 1, 'Principal', \
        'External', expectedVat, portfolio2, portfolio3, portfolio3.PortfolioOwner(), portfolio2.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, cfdRate2), 'Trade 2 not found in trades22')
        
        trades32 = TradeHelper.GetTrades(portfolio3, instrument2)
        self.assertEqual(len(trades32), 1, 'Expected 1 trade for Portfolio3, Instrument2')
        self.assert_(TradeHelper.Contains(trades32, startDate, endDate, instrument2, -50, 0, 1, 'Principal', \
        'External', expectedVat, portfolio3, portfolio2, portfolio2.PortfolioOwner(), portfolio3.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, cfdRate2), 'Trade 1 not found in trades32')
        
    def testCoverWithHeldPositions(self):
        internalDepartment1 = PartyHelper.CreatePersistantInternalDepartment()
        internalDepartment2 = PartyHelper.CreatePersistantInternalDepartment()
        
        portfolio1 = PortfolioHelper.CreatePersistantPortfolio(internalDepartment1)
        portfolio2 = PortfolioHelper.CreatePersistantPortfolio(internalDepartment2)
        portfolio3 = PortfolioHelper.CreatePersistantPortfolio(internalDepartment1)
        portfolio4 = PortfolioHelper.CreatePersistantPortfolio(internalDepartment1)
        
        instrument1 = InstrumentHelper.CreatePersistantStock()
        instrument2 = InstrumentHelper.CreatePersistantStock()
        instrument3 = InstrumentHelper.CreatePersistantStock()
        instrument4 = InstrumentHelper.CreatePersistantStock()
        
        internalRate = 0.2
        spreadRate = 0.05
        rate1 = 0.3
        rate2 = 0.4
        rate3 = 0.5
        rate4 = 0.6
        SblRatesHelper.WriteRatesFile([[sl_sweeping.SblRates._INTERNAL_KEY, '', internalRate], [sl_sweeping.SblRates._SPREAD_KEY, '', spreadRate], [instrument1.Name(), '', rate1], [instrument2.Name(), '*', rate2], [instrument3.Name(), '', rate3], [instrument4.Name(), '*', rate4]])
        
        internal = False
        external = True
        
        longPositions = sl_sweeping.PositionCollection()
        longPositions.Add(portfolio2, instrument1, 600, internal)
        longPositions.Add(portfolio2, instrument1, 400, external)
        longPositions.Add(portfolio2, instrument2, 600, internal)
        longPositions.Add(portfolio2, instrument2, 400, external)
        longPositions.Add(portfolio2, instrument3, 100, internal)
        longPositions.Add(portfolio2, instrument3, 100, external)
        longPositions.Add(portfolio2, instrument4, 100, internal)
        longPositions.Add(portfolio2, instrument4, 100, external)
        
        shortPositions = sl_sweeping.PositionCollection()
        shortPositions.Add(portfolio1, instrument1, -100, internal)
        shortPositions.Add(portfolio3, instrument1, -200, internal)
        shortPositions.Add(portfolio4, instrument1, -100, internal)
        
        shortPositions.Add(portfolio1, instrument2, -100, internal)
        shortPositions.Add(portfolio3, instrument2, -200, internal)
        shortPositions.Add(portfolio4, instrument2, -100, internal)
 
        shortPositions.Add(portfolio1, instrument3, -100, internal)
        shortPositions.Add(portfolio3, instrument3, -200, internal)
        shortPositions.Add(portfolio4, instrument3, -100, internal)
        
        shortPositions.Add(portfolio1, instrument4, -100, internal)
        shortPositions.Add(portfolio3, instrument4, -200, internal)
        shortPositions.Add(portfolio4, instrument4, -100, external)
        
        log = ProcessLog('TestPositionCollection.testCoverWithHeldPositions')
        batchNumber = '1235'
        coverDate = acm.Time().DateNow()
        validationMode = True
        applySpread = True
        partialSweeping = True
        cfdSweep = True
        allocateHeldPositions = True
        instrumentCountBefore = InstrumentHelper.GetInstrumentCount()
        tradeCountBefore = TradeHelper.GetSecurityLoanCount()
        longPositions.Cover(log, batchNumber, shortPositions, coverDate, None, not validationMode, self.rates, self.prices, applySpread, partialSweeping, not cfdSweep, allocateHeldPositions)
        instrumentCountAfter = InstrumentHelper.GetInstrumentCount()
        tradeCountAfter = TradeHelper.GetSecurityLoanCount()
        
        newInstruments = instrumentCountAfter - instrumentCountBefore
        self.assertEqual(newInstruments, 24, 'Expected 24 new instruments, got %i' % newInstruments)
        newTrades = tradeCountAfter - tradeCountBefore
        self.assertEqual(newTrades, 48, 'Expected 48 new trades, got %i' % newTrades)
        
        position11 = shortPositions.GetPosition(portfolio1, instrument1, internal)
        position12 = shortPositions.GetPosition(portfolio1, instrument2, internal)
        position13 = shortPositions.GetPosition(portfolio1, instrument3, internal)
        position14 = shortPositions.GetPosition(portfolio1, instrument4, internal)
        
        position21 = longPositions.GetPosition(portfolio2, instrument1, internal)
        position22 = longPositions.GetPosition(portfolio2, instrument2, internal)
        position23 = longPositions.GetPosition(portfolio2, instrument3, internal)
        position24 = longPositions.GetPosition(portfolio2, instrument4, internal)
        
        position2E1 = longPositions.GetPosition(portfolio2, instrument1, external)
        position2E2 = longPositions.GetPosition(portfolio2, instrument2, external)
        position2E3 = longPositions.GetPosition(portfolio2, instrument3, external)
        position2E4 = longPositions.GetPosition(portfolio2, instrument4, external)
        
        position31 = shortPositions.GetPosition(portfolio3, instrument1, internal)
        position32 = shortPositions.GetPosition(portfolio3, instrument2, internal)
        position33 = shortPositions.GetPosition(portfolio3, instrument3, internal)
        position34 = shortPositions.GetPosition(portfolio3, instrument4, internal)
        
        position41 = shortPositions.GetPosition(portfolio4, instrument1, internal)
        position42 = shortPositions.GetPosition(portfolio4, instrument2, internal)
        position43 = shortPositions.GetPosition(portfolio4, instrument3, internal)
        position44 = shortPositions.GetPosition(portfolio4, instrument4, external)
        
        self.assertEqual(position11.quantity, 0, 'Quantity for Internal Portfolio1, Instrument1 not as expected. Expected 0, got %s' % position11.quantity)
        self.assertEqual(position21.quantity, 360, 'Quantity for Internal Portfolio2, Instrument1 not as expected. Expected 360, got %s' % position21.quantity)
        self.assertEqual(position2E1.quantity, 240, 'Quantity for External Portfolio2, Instrument1 not as expected. Expected 240, got %s' % position2E1.quantity)
        self.assertEqual(position31.quantity, 0, 'Quantity for Internal Portfolio3, Instrument1 not as expected. Expected 0, got %s' % position31.quantity)
        self.assertEqual(position41.quantity, 0, 'Quantity for Internal Portfolio4, Instrument1 not as expected. Expected 0, got %s' % position41.quantity)
        
        self.assertEqual(position12.quantity, 150, 'Quantity for Internal Portfolio1, Instrument2 not as expected. Expected 150, got %s' % position12.quantity)
        self.assertEqual(position22.quantity, 0, 'Quantity for Internal Portfolio2, Instrument2 not as expected. Expected 0, got %s' % position22.quantity)
        self.assertEqual(position2E2.quantity, 0, 'Quantity for External Portfolio2, Instrument2 not as expected. Expected 0, got %s' % position2E2.quantity)
        self.assertEqual(position32.quantity, 300, 'Quantity for Internal Portfolio3, Instrument2 not as expected. Expected 300, got %s' % position32.quantity)
        self.assertEqual(position42.quantity, 150, 'Quantity for Internal Portfolio4, Instrument2 not as expected. Expected 150, got %s' % position42.quantity)
        
        self.assertEqual(position13.quantity, -50, 'Quantity for Internal Portfolio1, Instrument3 not as expected. Expected -50, got %s' % position13.quantity)
        self.assertEqual(position23.quantity, 0, 'Quantity for Internal Portfolio2, Instrument3 not as expected. Expected 0, got %s' % position23.quantity)
        self.assertEqual(position2E3.quantity, 0, 'Quantity for External Portfolio2, Instrument3 not as expected. Expected 0, got %s' % position2E3.quantity)
        self.assertEqual(position33.quantity, -100, 'Quantity for Internal Portfolio3, Instrument3 not as expected. Expected -100, got %s' % position33.quantity)
        self.assertEqual(position43.quantity, -50, 'Quantity for Internal Portfolio4, Instrument3 not as expected. Expected -50, got %s' % position43.quantity)
        
        self.assertEqual(position14.quantity, -50, 'Quantity for Internal Portfolio1, Instrument4 not as expected. Expected -50, got %s' % position14.quantity)
        self.assertEqual(position24.quantity, 0, 'Quantity for Internal Portfolio2, Instrument4 not as expected. Expected 0, got %s' % position24.quantity)
        self.assertEqual(position2E4.quantity, 0, 'Quantity for External Portfolio2, Instrument4 not as expected. Expected 0, got %s' % position2E4.quantity)
        self.assertEqual(position34.quantity, -100, 'Quantity for Internal Portfolio3, Instrument4 not as expected. Expected -100, got %s' % position34.quantity)
        self.assertEqual(position44.quantity, -50, 'Quantity for Internal Portfolio4, Instrument4 not as expected. Expected -50, got %s' % position44.quantity)
     
class TestSblSweeper(unittest.TestCase):

    def tearDown(self):
        if os.path.exists(SblRatesHelper.filepath):
            os.remove(SblRatesHelper.filepath)

    def setUp(self):
        self.internalDepartment1 = PartyHelper.CreatePersistantInternalDepartment()
        self.internalDepartment2 = PartyHelper.CreatePersistantInternalDepartment()
        self.sblPortfolio = PortfolioHelper.CreatePersistantPortfolio(self.internalDepartment1)
        
        self.desk1 = PortfolioHelper.GetTradingDesk()
        self.portfolio11 = PortfolioHelper.CreatePersistantSweepingPortfolio(self.internalDepartment1, self.desk1, 'Equity')
        self.portfolio12 = PortfolioHelper.CreatePersistantSweepingPortfolio(self.internalDepartment2, self.desk1, 'Equity')
        self.portfolio13 = PortfolioHelper.CreatePersistantSweepingPortfolio(self.internalDepartment1, self.desk1, 'Equity')
        self.loan1 = PortfolioHelper.CreatePersistantSweepingPortfolio(self.internalDepartment1, self.desk1, 'Fee')
        
        self.desk2 = PortfolioHelper.GetTradingDesk()
        self.portfolio21 = PortfolioHelper.CreatePersistantSweepingPortfolio(self.internalDepartment2, self.desk2, 'Equity')
        self.portfolio22 = PortfolioHelper.CreatePersistantSweepingPortfolio(self.internalDepartment1, self.desk2, 'Equity')
        self.portfolio23 = PortfolioHelper.CreatePersistantSweepingPortfolio(self.internalDepartment2, self.desk2, 'Equity')
        self.loan2 = PortfolioHelper.CreatePersistantSweepingPortfolio(self.internalDepartment1, self.desk2, 'Fee')

        self.desk3 = PortfolioHelper.GetTradingDesk()
        self.portfolio31 = PortfolioHelper.CreatePersistantSweepingPortfolio(self.internalDepartment1, self.desk3, 'Equity')
        self.portfolio32 = PortfolioHelper.CreatePersistantSweepingPortfolio(self.internalDepartment2, self.desk3, 'Equity')
        self.portfolio33 = PortfolioHelper.CreatePersistantSweepingPortfolio(self.internalDepartment1, self.desk3, 'Equity')
        self.loan3 = PortfolioHelper.CreatePersistantSweepingPortfolio(self.internalDepartment1, self.desk3, 'Fee')

        self.desk4 = PortfolioHelper.GetTradingDesk()
        self.portfolio41 = PortfolioHelper.CreatePersistantSweepingPortfolio(self.internalDepartment2, self.desk4, 'Equity')
        self.portfolio42 = PortfolioHelper.CreatePersistantSweepingPortfolio(self.internalDepartment1, self.desk4, 'Equity')
        self.portfolio43 = PortfolioHelper.CreatePersistantSweepingPortfolio(self.internalDepartment2, self.desk4, 'Equity')
        self.loan4 = PortfolioHelper.CreatePersistantSweepingPortfolio(self.internalDepartment1, self.desk4, 'Fee')

        self.desk5 = PortfolioHelper.GetTradingDesk()
        self.portfolio51 = PortfolioHelper.CreatePersistantSweepingPortfolio(self.internalDepartment1, self.desk5, 'Equity')
        self.portfolio52 = PortfolioHelper.CreatePersistantSweepingPortfolio(self.internalDepartment2, self.desk5, 'Equity')
        self.portfolio53 = PortfolioHelper.CreatePersistantSweepingPortfolio(self.internalDepartment1, self.desk5, 'Equity')
        self.loan5 = PortfolioHelper.CreatePersistantSweepingPortfolio(self.internalDepartment1, self.desk5, 'Fee')
        
        self.desk6 = PortfolioHelper.GetTradingDesk()
        self.portfolio61 = PortfolioHelper.CreatePersistantSweepingPortfolio(self.internalDepartment1, self.desk6, 'Equity')
        self.loan6 = PortfolioHelper.CreatePersistantSweepingPortfolio(self.internalDepartment1, self.desk6, 'Fee')
        
        self.desk7 = PortfolioHelper.GetTradingDesk()
        self.portfolio71 = PortfolioHelper.CreatePersistantSweepingPortfolio(self.internalDepartment1, self.desk7, 'Equity')
        self.loan7 = PortfolioHelper.CreatePersistantSweepingPortfolio(self.internalDepartment1, self.desk7, 'Fee')

        self.price1 = 10
        self.instrument1 = InstrumentHelper.CreatePersistantStock(self.price1)
        self.price2 = 200
        self.instrument2 = InstrumentHelper.CreatePersistantStock(self.price2)
        self.instrument3 = InstrumentHelper.CreatePersistantStock()
        self.instrument4 = InstrumentHelper.CreatePersistantStock()
        
        self.rates = sl_sweeping.SblRates(SblRatesHelper.filepath, 3)
        SblRatesHelper.WriteRatesFile([[self.instrument1.Name(), '', 0.2], [self.instrument2.Name(), '', 0.3], [self.instrument3.Name(), '', 0.4], [self.instrument4.Name(), '', 0.5]])
        
        self.portfolios = [self.portfolio11, self.portfolio12, self.portfolio13, self.loan1, self.portfolio21, self.portfolio22,
            self.portfolio23, self.loan2, self.portfolio31, self.portfolio32, self.portfolio33, self.loan3, self.portfolio41, self.portfolio42,
            self.portfolio43, self.loan4, self.portfolio51, self.portfolio52, self.portfolio53, self.loan5, self.portfolio61, self.loan6, 
            self.portfolio71, self.loan7]
            
        self.tradeFilter = TradeFilterHelper.CreateTradeFilter(self.portfolios)
        self.today = acm.Time().DateNow()
        self.log = ProcessLog('TestSblSweeper')
        
        timeSeriesSpec = acm.FTimeSeriesSpec['SBL Sweeping Batch']
        if TimeSeriesHelper.GetLastRunNo(timeSeriesSpec, self.today) > 75:
            TimeSeriesHelper.DeleteSeriesData(timeSeriesSpec, self.today, SlBatchType.Sweeping)
            
    def testSblPortfolioWithoutOwner(self):
        portfolioWithoutOwner = PortfolioHelper.CreatePersistantPortfolio()
        try:
            sl_sweeping.SblSweeper(acm.Time().DateNow(), self.tradeFilter, portfolioWithoutOwner, False, SblRatesHelper.filepath, 3, self.log, False, False)
        except Exception as ex:
            expectedMessage = "Portfolio [%s] is not valid, since it has no owner." % portfolioWithoutOwner.Name()
            self.assertEqual(expectedMessage, str(ex), 'Exception message not as expected')
        else:
            self.fail('Expected an exception')
        
    def testSblPortfolioNotInternal(self):
        counterparty = PartyHelper.CreatePersistantCounterparty()
        counterpartyPortfolio = PortfolioHelper.CreatePersistantPortfolio(counterparty)
        try:
            sl_sweeping.SblSweeper(acm.Time().DateNow(), self.tradeFilter, counterpartyPortfolio, False, SblRatesHelper.filepath, 3, self.log, False, False)
        except Exception as ex:
            expectedMessage = "Portfolio [%(portfolio)s], owned by [%(owner)s] of type [%(ownerType)s], is not valid. It is not owned by an internal department. The portfolio owner must be of type 'Intern Dept'" % \
                {'portfolio': counterpartyPortfolio.Name(), 'owner': counterparty.Name(), 'ownerType': counterparty.Type()}
            self.assertEqual(expectedMessage, str(ex), 'Exception message not as expected')
        else:
            self.fail('Expected an exception')
            
    def testPortfolioWithoutOwner(self):
        desk = PortfolioHelper.GetTradingDesk()
        portfolio = PortfolioHelper.CreatePersistantSweepingPortfolio(self.internalDepartment1, desk, 'Equity')
        portfolioWithoutOwner = PortfolioHelper.CreatePersistantSweepingPortfolio(None, desk, 'Fee')
        tradeFilter = TradeFilterHelper.CreateTradeFilter(self.portfolios + [portfolio])
        TradeHelper.BookTrade(portfolio, self.instrument1, acm.Time().DateNow(), 100)
        sweeper = sl_sweeping.SblSweeper(acm.Time().DateNow(), tradeFilter, self.sblPortfolio, False, SblRatesHelper.filepath, 3, self.log, False, False)
        expectedMessage = "Portfolio [%s] is not valid, since it has no owner." % portfolioWithoutOwner.Name()
        sweeper.Sweep()
        SlProcessLogHelper.AssertLogContains(self, 'Portfolio Without Owner', self.log, expectedMessage)
            
    def testPortfolioNotInternal(self):
        desk = PortfolioHelper.GetTradingDesk()
        portfolio = PortfolioHelper.CreatePersistantSweepingPortfolio(self.internalDepartment1, desk, 'Equity')
        counterparty = PartyHelper.CreatePersistantCounterparty()
        counterpartyPortfolio = PortfolioHelper.CreatePersistantSweepingPortfolio(counterparty, desk, 'Fee')
        tradeFilter = TradeFilterHelper.CreateTradeFilter(self.portfolios + [portfolio])
        TradeHelper.BookTrade(portfolio, self.instrument1, acm.Time().DateNow(), 100)
        sweeper = sl_sweeping.SblSweeper(acm.Time().DateNow(), tradeFilter, self.sblPortfolio, False, SblRatesHelper.filepath, 3, self.log, False, False)
        expectedMessage = "Portfolio [%(portfolio)s], owned by [%(owner)s] of type [%(ownerType)s], is not valid. It is not owned by an internal department. The portfolio owner must be of type 'Intern Dept'" % \
                {'portfolio': counterpartyPortfolio.Name(), 'owner': counterparty.Name(), 'ownerType': counterparty.Type()}
        sweeper.Sweep()
        SlProcessLogHelper.AssertLogContains(self, 'Portfolio Not Internal', self.log, expectedMessage)

    def testSweep(self):
        
        #------------------ Instrument 1 Positions ----------------------
        TradeHelper.BookTrade(self.portfolio11, self.instrument1, self.today, 50)
        TradeHelper.BookTrade(self.portfolio12, self.instrument1, self.today, 30)
        TradeHelper.BookTrade(self.portfolio13, self.instrument1, self.today, 20)
        
        TradeHelper.BookTrade(self.portfolio21, self.instrument1, self.today, 450)
        TradeHelper.BookTrade(self.portfolio22, self.instrument1, self.today, -50)
        TradeHelper.BookTrade(self.portfolio23, self.instrument1, self.today, -100)
        
        TradeHelper.BookTrade(self.portfolio31, self.instrument1, self.today, 100)
        TradeHelper.BookTrade(self.portfolio33, self.instrument1, self.today, -300)
        
        TradeHelper.BookTrade(self.portfolio41, self.instrument1, self.today, 100)
        TradeHelper.BookTrade(self.portfolio42, self.instrument1, self.today, -50)
        TradeHelper.BookTrade(self.portfolio43, self.instrument1, self.today, -50)
        
        TradeHelper.BookTrade(self.portfolio51, self.instrument1, self.today, 400)
        
        #------------------ Instrument 2 Positions ----------------------
        TradeHelper.BookTrade(self.portfolio11, self.instrument2, self.today, 200)
        TradeHelper.BookTrade(self.portfolio12, self.instrument2, self.today, -100)
        
        TradeHelper.BookTrade(self.portfolio21, self.instrument2, self.today, 150)
        TradeHelper.BookTrade(self.portfolio22, self.instrument2, self.today, 50)
        TradeHelper.BookTrade(self.portfolio23, self.instrument2, self.today, 100)
        
        TradeHelper.BookTrade(self.portfolio31, self.instrument2, self.today, -150)
        TradeHelper.BookTrade(self.portfolio32, self.instrument2, self.today, -50)
        
        TradeHelper.BookTrade(self.portfolio51, self.instrument2, self.today, 200)
        TradeHelper.BookTrade(self.portfolio53, self.instrument2, self.today, -400)
            
        #------------------ Instrument 3 Positions ----------------------
        TradeHelper.BookTrade(self.sblPortfolio, self.instrument3, self.today, 100)
        
        TradeHelper.BookTrade(self.portfolio11, self.instrument3, self.today, 60)
        TradeHelper.BookTrade(self.portfolio13, self.instrument3, self.today, 40)
        
        TradeHelper.BookTrade(self.portfolio21, self.instrument3, self.today, 500)
        TradeHelper.BookTrade(self.portfolio21, self.instrument3, self.today, 100)
        TradeHelper.BookTrade(self.portfolio22, self.instrument3, self.today, 300)
    
        TradeHelper.BookTrade(self.portfolio31, self.instrument3, self.today, 100)
        TradeHelper.BookTrade(self.portfolio32, self.instrument3, self.today, -400)
        
        TradeHelper.BookTrade(self.portfolio51, self.instrument3, self.today, -100)
        
        #------------------ Instrument 4 Positions ----------------------
        TradeHelper.BookTrade(self.sblPortfolio, self.instrument4, self.today, -200)
        
        TradeHelper.BookTrade(self.portfolio21, self.instrument4, self.today, 130)
        TradeHelper.BookTrade(self.portfolio22, self.instrument4, self.today, 70)
        
        TradeHelper.BookTrade(self.portfolio31, self.instrument4, self.today, 100)
        TradeHelper.BookTrade(self.portfolio32, self.instrument4, self.today, -100)
        
        TradeHelper.BookTrade(self.portfolio41, self.instrument4, self.today, 200)
        TradeHelper.BookTrade(self.portfolio42, self.instrument4, self.today, -100)
        TradeHelper.BookTrade(self.portfolio43, self.instrument4, self.today, -200)
        
        TradeHelper.BookTrade(self.portfolio51, self.instrument4, self.today, -100)
        TradeHelper.BookTrade(self.portfolio52, self.instrument4, self.today, 200)
        
        tradeFilter = TradeFilterHelper.CreateTradeFilter(self.portfolios)
        cfdSweep = True
        validationMode = False
        allowPartialSweeping = False
        sweeper = sl_sweeping.SblSweeper(self.today, tradeFilter, self.sblPortfolio, not cfdSweep, SblRatesHelper.filepath, 3, self.log, validationMode, allowPartialSweeping)
        sweeper.Sweep()
        
        self.assertEqual(0, InstrumentHelper.GetInventoryPosition(self.sblPortfolio, self.instrument1, self.today), 'Position of sblPortfolio, instrument1 not as expected')
        self.assertEqual(-25, InstrumentHelper.GetInventoryPosition(self.loan1, self.instrument1, self.today), 'Position of loan1, instrument1 not as expected')
        self.assertEqual(-75, InstrumentHelper.GetInventoryPosition(self.loan2, self.instrument1, self.today), 'Position of loan2, instrument1 not as expected')
        self.assertEqual(200, InstrumentHelper.GetInventoryPosition(self.loan3, self.instrument1, self.today), 'Position of loan3, instrument1 not as expected')
        self.assertEqual(0, InstrumentHelper.GetInventoryPosition(self.loan4, self.instrument1, self.today), 'Position of loan4, instrument1 not as expected')
        self.assertEqual(-100, InstrumentHelper.GetInventoryPosition(self.loan5, self.instrument1, self.today), 'Position of loan5, instrument1 not as expected')
        
        self.assertEqual(0, InstrumentHelper.GetInventoryPosition(self.sblPortfolio, self.instrument2, self.today), 'Position of sblPortfolio, instrument2 not as expected')
        self.assertEqual(-100, InstrumentHelper.GetInventoryPosition(self.loan1, self.instrument2, self.today), 'Position of loan1, instrument2 not as expected')
        self.assertEqual(-300, InstrumentHelper.GetInventoryPosition(self.loan2, self.instrument2, self.today), 'Position of loan2, instrument2 not as expected')
        self.assertEqual(200, InstrumentHelper.GetInventoryPosition(self.loan3, self.instrument2, self.today), 'Position of loan3, instrument2 not as expected')
        self.assertEqual(0, InstrumentHelper.GetInventoryPosition(self.loan4, self.instrument2, self.today), 'Position of loan4, instrument2 not as expected')
        self.assertEqual(200, InstrumentHelper.GetInventoryPosition(self.loan5, self.instrument2, self.today), 'Position of loan5, instrument2 not as expected')
        
        self.assertEqual(0, InstrumentHelper.GetInventoryPosition(self.sblPortfolio, self.instrument3, self.today), 'Position of sblPortfolio, instrument3 not as expected')
        self.assertEqual(-30, InstrumentHelper.GetInventoryPosition(self.loan1, self.instrument3, self.today), 'Position of loan1, instrument3 not as expected')
        self.assertEqual(-270, InstrumentHelper.GetInventoryPosition(self.loan2, self.instrument3, self.today), 'Position of loan2, instrument3 not as expected')
        self.assertEqual(300, InstrumentHelper.GetInventoryPosition(self.loan3, self.instrument3, self.today), 'Position of loan3, instrument3 not as expected')
        self.assertEqual(0, InstrumentHelper.GetInventoryPosition(self.loan4, self.instrument3, self.today), 'Position of loan4, instrument3 not as expected')
        self.assertEqual(100, InstrumentHelper.GetInventoryPosition(self.loan5, self.instrument3, self.today), 'Position of loan5, instrument3 not as expected')
        
        self.assertEqual(0, InstrumentHelper.GetInventoryPosition(self.sblPortfolio, self.instrument4, self.today), 'Position of sblPortfolio, instrument4 not as expected')
        self.assertEqual(0, InstrumentHelper.GetInventoryPosition(self.loan1, self.instrument4, self.today), 'Position of loan1, instrument4 not as expected')
        self.assertEqual(-200, InstrumentHelper.GetInventoryPosition(self.loan2, self.instrument4, self.today), 'Position of loan2, instrument4 not as expected')
        self.assertEqual(0, InstrumentHelper.GetInventoryPosition(self.loan3, self.instrument4, self.today), 'Position of loan3, instrument4 not as expected')
        self.assertEqual(100, InstrumentHelper.GetInventoryPosition(self.loan4, self.instrument4, self.today), 'Position of loan4, instrument4 not as expected')
        self.assertEqual(-100, InstrumentHelper.GetInventoryPosition(self.loan5, self.instrument4, self.today), 'Position of loan5, instrument4 not as expected')
        
    def testSweepTwice(self):
    
        TradeHelper.BookTrade(self.sblPortfolio, self.instrument1, self.today, 100)
        TradeHelper.BookTrade(self.portfolio11, self.instrument1, self.today, -100)
        TradeHelper.BookTrade(self.portfolio21, self.instrument1, self.today, -300)
        TradeHelper.BookTrade(self.portfolio31, self.instrument1, self.today, 100)
        
        TradeHelper.BookTrade(self.portfolio11, self.instrument2, self.today, 100.1)
        TradeHelper.BookTrade(self.portfolio21, self.instrument2, self.today, 199.9)
        TradeHelper.BookTrade(self.portfolio31, self.instrument2, self.today, -1000)
        
        tradeFilter = TradeFilterHelper.CreateTradeFilter([self.portfolio11, self.portfolio21, self.portfolio31])
        validationMode = False
        allowPartialSweeping = True
        sweeper = sl_sweeping.SblSweeper(self.today, tradeFilter, self.sblPortfolio, False, SblRatesHelper.filepath, 3, self.log, validationMode, allowPartialSweeping)
        sweeper.Sweep()
        
        self.assertEqual(0, InstrumentHelper.GetInventoryPosition(self.sblPortfolio, self.instrument1, self.today), 'Position of sblPortfolio, instrument1 not as expected on first sweep')
        self.assertEqual(50, InstrumentHelper.GetInventoryPosition(self.loan1, self.instrument1, self.today), 'Position of loan1, instrument1 not as expected on first sweep')
        self.assertEqual(150, InstrumentHelper.GetInventoryPosition(self.loan2, self.instrument1, self.today), 'Position of loan2, instrument1 not as expected on first sweep')
        self.assertEqual(-100, InstrumentHelper.GetInventoryPosition(self.loan3, self.instrument1, self.today), 'Position of loan3, instrument1 not as expected on first sweep')
        
        self.assertEqual(0, InstrumentHelper.GetInventoryPosition(self.sblPortfolio, self.instrument2, self.today), 'Position of sblPortfolio, instrument2 not as expected on first sweep')

        self.assertAlmostEqual(-100.1, InstrumentHelper.GetInventoryPosition(self.loan1, self.instrument2, self.today), 10, 'Position of loan1, instrument2 not as expected on first sweep')
        self.assertAlmostEqual(-199.9, InstrumentHelper.GetInventoryPosition(self.loan2, self.instrument2, self.today), 10, 'Position of loan2, instrument2 not as expected on first sweep')
        self.assertEqual(300, InstrumentHelper.GetInventoryPosition(self.loan3, self.instrument2, self.today), 'Position of loan3, instrument2 not as expected on first sweep')
        
        TradeHelper.BookTrade(self.sblPortfolio, self.instrument1, self.today, 300)
        TradeHelper.BookTrade(self.sblPortfolio, self.instrument2, self.today, 700)
        sweeper = sl_sweeping.SblSweeper(self.today, tradeFilter, self.sblPortfolio, False, SblRatesHelper.filepath, 3, self.log, validationMode, allowPartialSweeping)
        sweeper.Sweep()
        
        self.assertEqual(100, InstrumentHelper.GetInventoryPosition(self.sblPortfolio, self.instrument1, self.today), 'Position of sblPortfolio, instrument1 not as expected on second sweep')
        self.assertEqual(100, InstrumentHelper.GetInventoryPosition(self.loan1, self.instrument1, self.today), 'Position of loan1, instrument1 not as expected on second sweep')
        self.assertEqual(300, InstrumentHelper.GetInventoryPosition(self.loan2, self.instrument1, self.today), 'Position of loan2, instrument1 not as expected on second sweep')
        self.assertEqual(-100, InstrumentHelper.GetInventoryPosition(self.loan3, self.instrument1, self.today), 'Position of loan3, instrument1 not as expected on second sweep')
        
        self.assertEqual(0, InstrumentHelper.GetInventoryPosition(self.sblPortfolio, self.instrument2, self.today), 'Position of sblPortfolio, instrument2 not as expected on second sweep')
        self.assertAlmostEqual(-100.1, InstrumentHelper.GetInventoryPosition(self.loan1, self.instrument2, self.today), 10, 'Position of loan1, instrument2 not as expected on second sweep')
        self.assertAlmostEqual(-199.9, InstrumentHelper.GetInventoryPosition(self.loan2, self.instrument2, self.today), 10, 'Position of loan2, instrument2 not as expected on second sweep')
        self.assertEqual(1000, InstrumentHelper.GetInventoryPosition(self.loan3, self.instrument2, self.today), 'Position of loan3, instrument2 not as expected on second sweep')
        
    def testSweepNoZeroTradeCreated(self):
        TradeHelper.BookTrade(self.sblPortfolio, self.instrument1, self.today, 13967)       
        TradeHelper.BookTrade(self.portfolio11, self.instrument1, self.today, 2)
        TradeHelper.BookTrade(self.portfolio21, self.instrument1, self.today, -2)
        TradeHelper.BookTrade(self.portfolio31, self.instrument1, self.today, 6700)
        TradeHelper.BookTrade(self.portfolio41, self.instrument1, self.today, -20662)
        
        tradeFilter = TradeFilterHelper.CreateTradeFilter([self.portfolio11, self.portfolio21, self.portfolio31, self.portfolio41])
        validationMode = False
        allowPartialSweeping = False
        sweeper = sl_sweeping.SblSweeper(self.today, tradeFilter, self.sblPortfolio, False, SblRatesHelper.filepath, 3, self.log, validationMode, allowPartialSweeping)
        sweeper.Sweep()
        
        positionLoan1 = InstrumentHelper.GetInventoryPosition(self.loan1, self.instrument1, self.today)
        self.assertEqual(0, InstrumentHelper.GetInventoryPosition(self.sblPortfolio, self.instrument1, self.today), 'Position of sblPortfolio, instrument1 not as expected')
        self.assert_(positionLoan1 in (-1, -2),  'Position of loan1, instrument1 not as expected')
        self.assertEqual(2, InstrumentHelper.GetInventoryPosition(self.loan2, self.instrument1, self.today), 'Position of loan2, instrument1 not as expected')
        self.assertEqual(-6697 - positionLoan1, InstrumentHelper.GetInventoryPosition(self.loan3, self.instrument1, self.today), 'Position of loan3, instrument1 not as expected')
        self.assertEqual(20662, InstrumentHelper.GetInventoryPosition(self.loan4, self.instrument1, self.today), 'Position of loan4, instrument1 not as expected')
        
    def testSweepValidationMode(self):        
        TradeHelper.BookTrade(self.sblPortfolio, self.instrument1, self.today, 13967)       
        TradeHelper.BookTrade(self.portfolio11, self.instrument1, self.today, 2)
        TradeHelper.BookTrade(self.portfolio21, self.instrument1, self.today, -2)
        TradeHelper.BookTrade(self.portfolio31, self.instrument1, self.today, 6700)
        TradeHelper.BookTrade(self.portfolio41, self.instrument1, self.today, -20662)
        
        tradeFilter = TradeFilterHelper.CreateTradeFilter([self.portfolio11, self.portfolio21, self.portfolio31, self.portfolio41])
        validationMode = True
        allowPartialSweeping = False
        sweeper = sl_sweeping.SblSweeper(self.today, tradeFilter, self.sblPortfolio, False, SblRatesHelper.filepath, 3, self.log, validationMode, allowPartialSweeping)
        countBeforeSweep = TradeHelper.GetSecurityLoanCount()
        sweeper.Sweep()
        countAfterSweep = TradeHelper.GetSecurityLoanCount()
        self.assertEqual(countBeforeSweep, countAfterSweep, 'Did not expect any trades to be booked')
        
        self.assertEqual(13967, InstrumentHelper.GetInventoryPosition(self.sblPortfolio, self.instrument1, self.today), 'Position of sblPortfolio, instrument1 not as expected')
        self.assertEqual(0, InstrumentHelper.GetInventoryPosition(self.loan1, self.instrument1, self.today), 'Position of loan1, instrument1 not as expected')
        self.assertEqual(0, InstrumentHelper.GetInventoryPosition(self.loan2, self.instrument1, self.today), 'Position of loan2, instrument1 not as expected')
        self.assertEqual(0, InstrumentHelper.GetInventoryPosition(self.loan3, self.instrument1, self.today), 'Position of loan3, instrument1 not as expected')
        self.assertEqual(0, InstrumentHelper.GetInventoryPosition(self.loan4, self.instrument1, self.today), 'Position of loan4, instrument1 not as expected')
        self.assertEqual(2, InstrumentHelper.GetInventoryPosition(self.portfolio11, self.instrument1, self.today), 'Position of portfolio11, instrument1 not as expected')
        self.assertEqual(-2, InstrumentHelper.GetInventoryPosition(self.portfolio21, self.instrument1, self.today), 'Position of portfolio21, instrument1 not as expected')
        self.assertEqual(6700, InstrumentHelper.GetInventoryPosition(self.portfolio31, self.instrument1, self.today), 'Position of portfolio31, instrument1 not as expected')
        self.assertEqual(-20662, InstrumentHelper.GetInventoryPosition(self.portfolio41, self.instrument1, self.today), 'Position of portfolio41, instrument1 not as expected')

    def testSweepValidationModeMessages(self):
        noLoanDesk = PortfolioHelper.GetTradingDesk()
        portfolioNoLoanDesk = PortfolioHelper.CreatePersistantSweepingPortfolio(self.internalDepartment1, noLoanDesk, 'Equity')
        TradeHelper.BookTrade(self.sblPortfolio, self.instrument1, self.today, 100)
        TradeHelper.BookTrade(portfolioNoLoanDesk, self.instrument1, self.today, -100)
        
        noRateInstrument1 = InstrumentHelper.CreatePersistantStock()
        noRateInstrument2 = InstrumentHelper.CreatePersistantStock()
        TradeHelper.BookTrade(self.sblPortfolio, noRateInstrument1, self.today, 100)
        TradeHelper.BookTrade(self.portfolio11, noRateInstrument1, self.today, -100)
        TradeHelper.BookTrade(self.sblPortfolio, noRateInstrument2, self.today, 200)
        TradeHelper.BookTrade(self.portfolio11, noRateInstrument2, self.today, -200)
        
        TradeHelper.BookTrade(self.sblPortfolio, self.instrument2, self.today, 20)
        TradeHelper.BookTrade(self.portfolio12, self.instrument2, self.today, -150)
        TradeHelper.BookTrade(self.portfolio22, self.instrument2, self.today, 50)
        
        tradeFilter = TradeFilterHelper.CreateTradeFilter([portfolioNoLoanDesk, self.portfolio11, self.portfolio12, self.portfolio22])
        validationMode = True
        allowPartialSweeping = False
        sweeper = sl_sweeping.SblSweeper(self.today, tradeFilter, self.sblPortfolio, False, SblRatesHelper.filepath, 3, self.log, validationMode, allowPartialSweeping)
        countBeforeSweep = TradeHelper.GetSecurityLoanCount()
        sweeper.Sweep()
        countAfterSweep = TradeHelper.GetSecurityLoanCount()
        self.assertEqual(countBeforeSweep, countAfterSweep, 'Did not expect any trades to be booked')
        
        SlProcessLogHelper.AssertLogContains(self, 'No fee portfolio', self.log, 'No Fee portfolio found for trading desk [%(desk)s], please correct this and try again.' % {'desk': noLoanDesk})
        SlProcessLogHelper.AssertLogContains(self, 'No external rate for noRateInstrument1', self.log, r'No external rate was found for \[%(instrument)s\] in column \[3\], please correct it in the file \[%(filepath)s\]\: Short of 100.* will not be covered\.' % \
            {'instrument': noRateInstrument1.Name(), 'filepath': SblRatesHelper.filepath.replace('\\', '\\\\')}, True)
        SlProcessLogHelper.AssertLogContains(self, 'No external rate for noRateInstrument2', self.log, r'No external rate was found for \[%(instrument)s\] in column \[3\], please correct it in the file \[%(filepath)s\]\: Short of 200.* will not be covered\.' % \
            {'instrument': noRateInstrument2.Name(), 'filepath': SblRatesHelper.filepath.replace('\\', '\\\\')}, True)
        SlProcessLogHelper.AssertLogContains(self, 'Not enough to cover short', self.log, 'Long position of %(long)f is not enough to cover a short of %(short)f for instrument %(instrument)s. %(instrument)s will not be swept.' % \
            {'long': 50, 'short': 130, 'instrument': self.instrument2.Name()})
        
    def testSweepNotCfd(self):
        
        #------------------ Instrument 1 Positions ----------------------
        quantity11 = 20
        price11 = self.price1 + 10
        quantity12 = 70
        price12 = self.price1 + 5
        avgPrice1 = ((float(quantity11) * float(price11)) + (float(quantity12) * float(price12))) / float(quantity11 + quantity12)
        TradeHelper.BookSecurityLoanFromUnderlying(self.sblPortfolio, self.instrument1, quantity11, price11, 1, 'External', TODAY, 'FO Confirmed')
        TradeHelper.BookSecurityLoanFromUnderlying(self.sblPortfolio, self.instrument1, quantity12, price12, 1, 'External', TODAY, 'FO Confirmed')
        TradeHelper.BookSecurityLoanFromUnderlying(self.sblPortfolio, self.instrument1, 10, 10, 1, 'Internal', TODAY, 'FO Confirmed')
        
        TradeHelper.BookSecurityLoanFromUnderlying(self.portfolio11, self.instrument1, 1000, 9, 1, 'Internal', TODAY, 'FO Confirmed')

        TradeHelper.BookSecurityLoanFromUnderlying(self.portfolio21, self.instrument1, -600, 9, 1, 'External', TODAY, 'FO Confirmed')
        
        TradeHelper.BookTrade(self.portfolio31, self.instrument1, self.today, 4000)
        
        #------------------ Instrument 2 Positions ----------------------
        quantity21 = 200
        price21 = self.price2 - 50
        quantity22 = 800
        price22 = self.price2 + 20
        avgPrice2 = ((float(quantity21) * float(price21)) + (float(quantity22) * float(price22))) / float(quantity21 + quantity22)
        TradeHelper.BookSecurityLoanFromUnderlying(self.sblPortfolio, self.instrument2, quantity21, price21, 1, 'External', TODAY, 'FO Confirmed')
        TradeHelper.BookSecurityLoanFromUnderlying(self.sblPortfolio, self.instrument2, quantity22, price22, 1, 'External', TODAY, 'FO Confirmed')
        
        TradeHelper.BookTrade(self.portfolio11, self.instrument2, self.today, 800)
        
        TradeHelper.BookTrade(self.portfolio21, self.instrument2, self.today, 200)
        
        TradeHelper.BookSecurityLoanFromUnderlying(self.portfolio31, self.instrument2, -1200, 100, 1, 'Internal', TODAY, 'FO Confirmed')
        
        portfolios = [self.portfolio11, self.portfolio21, self.portfolio31, self.loan1, self.loan2]
        tradeFilter = TradeFilterHelper.CreateTradeFilter(self.portfolios)
        cfdSweep = True
        validationMode = True
        allowPartialSweeping = True
        sweeper = sl_sweeping.SblSweeper(self.today, tradeFilter, self.sblPortfolio, not cfdSweep, SblRatesHelper.filepath, 3, self.log, not validationMode, not allowPartialSweeping)
        sweeper.Sweep()
        
        self.assertEqual(0, InstrumentHelper.GetInventoryPosition(self.sblPortfolio, self.instrument1, self.today), 'Position of sblPortfolio, instrument1 not as expected')
        self.assertEqual(-100, InstrumentHelper.GetInventoryPosition(self.loan1, self.instrument1, self.today), 'Position of loan1, instrument1 not as expected')
        self.assertEqual(600, InstrumentHelper.GetInventoryPosition(self.loan2, self.instrument1, self.today), 'Position of loan2, instrument1 not as expected')
        self.assertEqual(-400, InstrumentHelper.GetInventoryPosition(self.loan3, self.instrument1, self.today), 'Position of loan3, instrument1 not as expected')
        
        self.assertEqual(0, InstrumentHelper.GetInventoryPosition(self.sblPortfolio, self.instrument2, self.today), 'Position of sblPortfolio, instrument2 not as expected')
        self.assertEqual(-160, InstrumentHelper.GetInventoryPosition(self.loan1, self.instrument2, self.today), 'Position of loan1, instrument2 not as expected')
        self.assertEqual(-40, InstrumentHelper.GetInventoryPosition(self.loan2, self.instrument2, self.today), 'Position of loan2, instrument2 not as expected')
        self.assertEqual(1200, InstrumentHelper.GetInventoryPosition(self.loan3, self.instrument2, self.today), 'Position of loan3, instrument2 not as expected')
        
        trades = TradeHelper.GetLatestSweepingBatchTrades(self.today)
        actual = len(trades)
        self.assertEqual(16, actual, 'Expected 16 trades, got %s' % actual)
        for trade in trades:
            instrument = trade.Instrument()
            self.assertFalse(instrument.AdditionalInfo().SL_CFD(), 'Expected trade [%i] to have SL_CFD set to False' % trade.Oid())
            underlying = instrument.Underlying()
            if underlying == self.instrument1:
                self.assertEqual(avgPrice1, instrument.RefPrice(), 'Reference price for trade %i not as expected. Expected %f, got %f.' % (trade.Oid(), avgPrice1, instrument.RefPrice()))
            elif underlying == self.instrument2:
                self.assertEqual(avgPrice2, instrument.RefPrice(), 'Reference price for trade %i not as expected. Expected %f, got %f.' % (trade.Oid(), avgPrice2, instrument.RefPrice()))
            else:
                self.fail('Unexpected underlyng instrument [%s] for trade [%i].' % (underlying.Name(), trade.Oid()))
            
    def testSweepCfd(self):
        
        #------------------ Instrument 1 Positions ----------------------
        quantity11 = 20
        price11 = self.price1 + 10
        quantity12 = 70
        price12 = self.price1 + 5
        TradeHelper.BookSecurityLoanFromUnderlying(self.sblPortfolio, self.instrument1, quantity11, price11, 1, 'External', TODAY, 'FO Confirmed')
        TradeHelper.BookSecurityLoanFromUnderlying(self.sblPortfolio, self.instrument1, quantity12, price12, 1, 'External', TODAY, 'FO Confirmed')
        TradeHelper.BookSecurityLoanFromUnderlying(self.sblPortfolio, self.instrument1, 10, 10, 1, 'Internal', TODAY, 'FO Confirmed')
        
        TradeHelper.BookSecurityLoanFromUnderlying(self.portfolio11, self.instrument1, 1000, 9, 1, 'Internal', TODAY, 'FO Confirmed')

        TradeHelper.BookSecurityLoanFromUnderlying(self.portfolio21, self.instrument1, -600, 9, 1, 'External', TODAY, 'FO Confirmed')
        
        TradeHelper.BookTrade(self.portfolio31, self.instrument1, self.today, 4000)
        
        #------------------ Instrument 2 Positions ----------------------
        quantity21 = 200
        price21 = self.price2 - 50
        quantity22 = 800
        price22 = self.price2 + 20
        TradeHelper.BookSecurityLoanFromUnderlying(self.sblPortfolio, self.instrument2, quantity21, price21, 1, 'External', TODAY, 'FO Confirmed')
        TradeHelper.BookSecurityLoanFromUnderlying(self.sblPortfolio, self.instrument2, quantity22, price22, 1, 'External', TODAY, 'FO Confirmed')
        
        TradeHelper.BookTrade(self.portfolio11, self.instrument2, self.today, 800)
        
        TradeHelper.BookTrade(self.portfolio21, self.instrument2, self.today, 200)
        
        TradeHelper.BookSecurityLoanFromUnderlying(self.portfolio31, self.instrument2, -1200, 100, 1, 'Internal', TODAY, 'FO Confirmed')
        
        portfolios = [self.portfolio11, self.portfolio21, self.portfolio31, self.loan1, self.loan2]
        tradeFilter = TradeFilterHelper.CreateTradeFilter(self.portfolios)
        cfdSweep = True
        validationMode = True
        allowPartialSweeping = True
        sweeper = sl_sweeping.SblSweeper(self.today, tradeFilter, self.sblPortfolio, cfdSweep, SblRatesHelper.filepath, 3, self.log, not validationMode, not allowPartialSweeping)
        sweeper.Sweep()
        
        self.assertEqual(0, InstrumentHelper.GetInventoryPosition(self.sblPortfolio, self.instrument1, self.today), 'Position of sblPortfolio, instrument1 not as expected')
        self.assertEqual(-100, InstrumentHelper.GetInventoryPosition(self.loan1, self.instrument1, self.today), 'Position of loan1, instrument1 not as expected')
        self.assertEqual(600, InstrumentHelper.GetInventoryPosition(self.loan2, self.instrument1, self.today), 'Position of loan2, instrument1 not as expected')
        self.assertEqual(-400, InstrumentHelper.GetInventoryPosition(self.loan3, self.instrument1, self.today), 'Position of loan3, instrument1 not as expected')
        
        self.assertEqual(0, InstrumentHelper.GetInventoryPosition(self.sblPortfolio, self.instrument2, self.today), 'Position of sblPortfolio, instrument2 not as expected')
        self.assertEqual(-160, InstrumentHelper.GetInventoryPosition(self.loan1, self.instrument2, self.today), 'Position of loan1, instrument2 not as expected')
        self.assertEqual(-40, InstrumentHelper.GetInventoryPosition(self.loan2, self.instrument2, self.today), 'Position of loan2, instrument2 not as expected')
        self.assertEqual(1200, InstrumentHelper.GetInventoryPosition(self.loan3, self.instrument2, self.today), 'Position of loan3, instrument2 not as expected')
        
        trades = TradeHelper.GetLatestSweepingBatchTrades(self.today)
        actual = len(trades)
        self.assertEqual(16, actual, 'Expected 16 trades, got %s' % actual)
        for trade in trades:
            instrument = trade.Instrument()
            self.assertTrue(instrument.AdditionalInfo().SL_CFD(), 'Expected trade [%i] to have SL_CFD set to True' % trade.Oid())
            underlying = instrument.Underlying()
            if underlying == self.instrument1:
                self.assertEqual(self.price1, instrument.RefPrice(), 'Reference price for trade %i not as expected. Expected %f, got %f.' % (trade.Oid(), self.price1, instrument.RefPrice()))
            elif underlying == self.instrument2:
                self.assertEqual(self.price2, instrument.RefPrice(), 'Reference price for trade %i not as expected. Expected %f, got %f.' % (trade.Oid(), self.price2, instrument.RefPrice()))
            else:
                self.fail('Unexpected underlyng instrument [%s] for trade [%i].' % (underlying.Name(), trade.Oid()))

    def testSweepAllocateHeld(self):
        
        #------------------ Instrument 1 Positions ----------------------
        TradeHelper.BookTrade(self.sblPortfolio, self.instrument1, self.today, 400)
        
        TradeHelper.BookTrade(self.portfolio11, self.instrument1, self.today, -100)
        TradeHelper.BookTrade(self.portfolio21, self.instrument1, self.today, -100)
        TradeHelper.BookTrade(self.portfolio31, self.instrument1, self.today, -50)
        TradeHelper.BookTrade(self.portfolio41, self.instrument1, self.today, 50)
        TradeHelper.BookTrade(self.portfolio51, self.instrument1, self.today, -200)
        
        #------------------ Instrument 2 Positions ----------------------
        TradeHelper.BookTrade(self.sblPortfolio, self.instrument2, self.today, 1000)
        
        TradeHelper.BookTrade(self.portfolio21, self.instrument2, self.today, 55)
        TradeHelper.BookTrade(self.portfolio31, self.instrument2, self.today, 100)
        TradeHelper.BookTrade(self.portfolio51, self.instrument2, self.today, 400)
        TradeHelper.BookTrade(self.portfolio71, self.instrument2, self.today, 100)
        
        #------------------ Instrument 3 Positions ----------------------
        TradeHelper.BookTrade(self.sblPortfolio, self.instrument3, self.today, 90)
        
        #------------------ Instrument 4 Positions ----------------------
        TradeHelper.BookTrade(self.sblPortfolio, self.instrument4, self.today, 6000)
        
        TradeHelper.BookTrade(self.portfolio11, self.instrument4, self.today, -1000)
        TradeHelper.BookTrade(self.portfolio21, self.instrument4, self.today, -2000)
        TradeHelper.BookTrade(self.portfolio41, self.instrument4, self.today, 800)
        
        #------------------ Instrument 5 Positions ----------------------
        instrument5 = InstrumentHelper.CreatePersistantStock()
        TradeHelper.BookTrade(self.sblPortfolio, instrument5, self.today, 500)
        
        TradeHelper.BookTrade(self.portfolio11, instrument5, self.today, -50)
        TradeHelper.BookTrade(self.portfolio31, instrument5, self.today, 100)
        TradeHelper.BookTrade(self.portfolio51, instrument5, self.today, -100)
        
        tradeFilter = TradeFilterHelper.CreateTradeFilter(self.portfolios)
        cfdSweep = True
        validationMode = False
        allowPartialSweeping = False
        allocateHeldPositions = True
        
        SblRatesHelper.WriteRatesFile([[self.instrument1.Name(), '', 0.2], [self.instrument2.Name(), '*', 0.3], [self.instrument3.Name(), '*', 0.35], [self.instrument4.Name(), '*', 0.5], [instrument5.Name(), '', 0.45]])
        
        sweeper = sl_sweeping.SblSweeper(self.today, tradeFilter, self.sblPortfolio, not cfdSweep, SblRatesHelper.filepath, 3, self.log, validationMode, allowPartialSweeping, allocateHeldPositions)
        sweeper.Sweep()
        
        #------------------ Instrument 1 Positions ----------------------
        InstrumentHelper.AssertInventoryPosition(self, self.sblPortfolio, self.instrument1, self.today, 0, 'Position of sblPortfolio, instrument1 not as expected. Expected: %(expected)s, Actual: %(actual)s')
        InstrumentHelper.AssertInventoryPosition(self, self.loan1, self.instrument1, self.today, 100, 'Position of loan1, instrument1 not as expected. Expected: %(expected)s, Actual: %(actual)s')
        InstrumentHelper.AssertInventoryPosition(self, self.loan2, self.instrument1, self.today, 100, 'Position of loan2, instrument1 not as expected. Expected: %(expected)s, Actual: %(actual)s')
        InstrumentHelper.AssertInventoryPosition(self, self.loan3, self.instrument1, self.today, 50, 'Position of loan3, instrument1 not as expected. Expected: %(expected)s, Actual: %(actual)s')
        InstrumentHelper.AssertInventoryPosition(self, self.loan4, self.instrument1, self.today, -50, 'Position of loan4, instrument1 not as expected. Expected: %(expected)s, Actual: %(actual)s')
        InstrumentHelper.AssertInventoryPosition(self, self.loan5, self.instrument1, self.today, 200, 'Position of loan5, instrument1 not as expected. Expected: %(expected)s, Actual: %(actual)s')
        InstrumentHelper.AssertInventoryPosition(self, self.loan6, self.instrument1, self.today, 0, 'Position of loan6, instrument1 not as expected. Expected: %(expected)s, Actual: %(actual)s')
        InstrumentHelper.AssertInventoryPosition(self, self.loan7, self.instrument1, self.today, 0, 'Position of loan7, instrument1 not as expected. Expected: %(expected)s, Actual: %(actual)s')
        
        #------------------ Instrument 2 Positions ----------------------
        InstrumentHelper.AssertInventoryPosition(self, self.sblPortfolio, self.instrument2, self.today, 0, 'Position of sblPortfolio, instrument2 not as expected. Expected: %(expected)s, Actual: %(actual)s')
        InstrumentHelper.AssertInventoryPosition(self, self.loan1, self.instrument2, self.today, 385, 'Position of loan1, instrument2 not as expected. Expected: %(expected)s, Actual: %(actual)s')
        InstrumentHelper.AssertInventoryPosition(self, self.loan2, self.instrument2, self.today, 330, 'Position of loan2, instrument2 not as expected. Expected: %(expected)s, Actual: %(actual)s')
        InstrumentHelper.AssertInventoryPosition(self, self.loan3, self.instrument2, self.today, 285, 'Position of loan3, instrument2 not as expected. Expected: %(expected)s, Actual: %(actual)s')
        dict = {self.loan4: 'loan4', self.loan5: 'loan5', self.loan6: 'loan6', self.loan7: 'loan7'}
        for portfolio in dict:
            InstrumentHelper.AssertInventoryPosition(self, portfolio, self.instrument2, self.today, 0, 'Position of %s, instrument2 not as expected.' % dict[portfolio] + 'Expected: %(expected)s, Actual: %(actual)s')
        
        #------------------ Instrument 3 Positions ----------------------
        InstrumentHelper.AssertInventoryPosition(self, self.sblPortfolio, self.instrument3, self.today, 0, 'Position of sblPortfolio, instrument3 not as expected. Expected: %(expected)s, Actual: %(actual)s')
        dict = {self.loan4: 'loan4', self.loan6: 'loan6', self.loan7: 'loan7'}
        for portfolio in dict:
            InstrumentHelper.AssertInventoryPosition(self, portfolio, self.instrument3, self.today, 0, 'Position of %s, instrument3 not as expected.' % dict[portfolio] + 'Expected: %(expected)s, Actual: %(actual)s')

        dict = {self.loan1: 'loan1', self.loan2: 'loan2', self.loan3: 'loan3', self.loan5: 'loan5'}
        expected = [23, 23, 23, 21]
        for portfolio in dict:
            actual = InstrumentHelper.GetInventoryPosition(portfolio, self.instrument3, self.today)
            if actual in expected:
                expected.remove(actual)
            else:
                self.fail('Position of %(portfolio)s, instrument3 not as expected. Expected one of %(expected)s, got: %(actual)s' % {'portfolio': dict[portfolio], 'expected': expected, 'actual': actual})
        
        #------------------ Instrument 4 Positions ----------------------        
        InstrumentHelper.AssertInventoryPosition(self, self.sblPortfolio, self.instrument4, self.today, 0, 'Position of sblPortfolio, instrument4 not as expected. Expected: %(expected)s, Actual: %(actual)s')
        InstrumentHelper.AssertInventoryPosition(self, self.loan1, self.instrument4, self.today, 2000, 'Position of loan1, instrument4 not as expected. Expected: %(expected)s, Actual: %(actual)s')
        InstrumentHelper.AssertInventoryPosition(self, self.loan2, self.instrument4, self.today, 4000, 'Position of loan2, instrument4 not as expected. Expected: %(expected)s, Actual: %(actual)s')
        dict = {self.loan3: 'loan3', self.loan4: 'loan4', self.loan5: 'loan5', self.loan6: 'loan6', self.loan7: 'loan7'}
        for portfolio in dict:
            InstrumentHelper.AssertInventoryPosition(self, portfolio, self.instrument4, self.today, 0, 'Position of %s, instrument4 not as expected.' % dict[portfolio] + 'Expected: %(expected)s, Actual: %(actual)s')
        
        #------------------ Instrument 5 Positions ----------------------        
        InstrumentHelper.AssertInventoryPosition(self, self.sblPortfolio, instrument5, self.today, 350, 'Position of sblPortfolio, instrument5 not as expected. Expected: %(expected)s, Actual: %(actual)s')
        InstrumentHelper.AssertInventoryPosition(self, self.loan1, instrument5, self.today, 50, 'Position of loan1, instrument5 not as expected. Expected: %(expected)s, Actual: %(actual)s')
        InstrumentHelper.AssertInventoryPosition(self, self.loan5, instrument5, self.today, 100, 'Position of loan5, instrument5 not as expected. Expected: %(expected)s, Actual: %(actual)s')
        dict = {self.loan2: 'loan2', self.loan3: 'loan3', self.loan4: 'loan4', self.loan6: 'loan6', self.loan7: 'loan7'}
        for portfolio in dict:
            InstrumentHelper.AssertInventoryPosition(self, portfolio, instrument5, self.today, 0, 'Position of %s, instrument5 not as expected.' % dict[portfolio] + 'Expected: %(expected)s, Actual: %(actual)s')
    
    def testSweepAllocateHeldNoShorts(self):
    
        #------------------ Instrument 1 Positions ----------------------
        TradeHelper.BookTrade(self.sblPortfolio, self.instrument1, self.today, 400)
        
        TradeHelper.BookTrade(self.portfolio11, self.instrument1, self.today, 100)
        TradeHelper.BookTrade(self.portfolio21, self.instrument1, self.today, 50)
        
        #------------------ Instrument 2 Positions ----------------------
        TradeHelper.BookTrade(self.sblPortfolio, self.instrument2, self.today, 1000)
        
        TradeHelper.BookTrade(self.portfolio21, self.instrument2, self.today, 55)
        TradeHelper.BookTrade(self.portfolio31, self.instrument2, self.today, 100)
        
        #------------------ Instrument 3 Positions ----------------------
        TradeHelper.BookTrade(self.sblPortfolio, self.instrument3, self.today, 90)
        
        tradeFilter = TradeFilterHelper.CreateTradeFilter(self.portfolios)
        cfdSweep = True
        validationMode = False
        allowPartialSweeping = False
        allocateHeldPositions = True
        
        SblRatesHelper.WriteRatesFile([[self.instrument1.Name(), '', 0.2], [self.instrument2.Name(), '*', 0.3], [self.instrument3.Name(), '*', 0.35]])
        
        instrumentCountBefore = InstrumentHelper.GetInstrumentCount()
        tradeCountBefore = TradeHelper.GetSecurityLoanCount()
        
        sweeper = sl_sweeping.SblSweeper(self.today, tradeFilter, self.sblPortfolio, not cfdSweep, SblRatesHelper.filepath, 3, self.log, validationMode, allowPartialSweeping, allocateHeldPositions)
        sweeper.Sweep()
        
        instrumentCountAfter = InstrumentHelper.GetInstrumentCount()
        tradeCountAfter = TradeHelper.GetSecurityLoanCount()
        
        newInstruments = instrumentCountAfter - instrumentCountBefore
        self.assertEqual(newInstruments, 0, 'Expected no new instruments, got %i' % newInstruments)
        newTrades = tradeCountAfter - tradeCountBefore
        self.assertEqual(newTrades, 0, 'Expected no new trades, got %i' % newTrades)
        SlProcessLogHelper.AssertLogContains(self, 'Held Positions Warning', self.log, 'No portfolios to allocate held postions to.')
        
    def testSweepRateColumns(self):
    
        TradeHelper.BookTrade(self.sblPortfolio, self.instrument1, self.today, 400)
        
        TradeHelper.BookTrade(self.portfolio11, self.instrument1, self.today, -100)
        TradeHelper.BookTrade(self.portfolio21, self.instrument1, self.today, -100)
        
        cfdSweep = True
        validationMode = False
        allowPartialSweeping = False
        allocateHeldPositions = True
        startDate = acm.Time().DateNow()
        endDate = acm.FCalendar['ZAR Johannesburg'].AdjustBankingDays(startDate, 1)
        expectedTradeStatus = 'FO Confirmed'
        expectedVat = bool(acm.FAdditionalInfoSpec['SL_VAT'].DefaultValue())
        expectedSlCfd = False
        
        rate1 = 0.2
        rate2 = 0.3
        SblRatesHelper.WriteRatesFile([[self.instrument1.Name(), '', rate1, '', rate2], [self.instrument2.Name(), '*', 0.3, '', 0.5], [self.instrument3.Name(), '*', 0.35]])
        
        rateColumn = 3
        tradeFilter = TradeFilterHelper.CreateTradeFilter([self.portfolio11])
        sweeper = sl_sweeping.SblSweeper(startDate, tradeFilter, self.sblPortfolio, not cfdSweep, SblRatesHelper.filepath, rateColumn, self.log, validationMode, allowPartialSweeping, allocateHeldPositions)
        sweeper.Sweep()
        
        trades = TradeHelper.GetTrades(self.loan1, self.instrument1)
        self.assertEqual(len(trades), 1, 'Expected 1 trade after first sweep, got %i' % len(trades))
        self.assert_(TradeHelper.Contains(trades, startDate, endDate, self.instrument1, 100, 0, 1, 'Principal', \
        'External', expectedVat, self.loan1, self.sblPortfolio, self.sblPortfolio.PortfolioOwner(), self.loan1.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, rate1), 'Trade not as expected after first sweep')
        
        rateColumn = 5
        tradeFilter = TradeFilterHelper.CreateTradeFilter([self.portfolio21])
        sweeper = sl_sweeping.SblSweeper(startDate, tradeFilter, self.sblPortfolio, not cfdSweep, SblRatesHelper.filepath, rateColumn, self.log, validationMode, allowPartialSweeping, allocateHeldPositions)
        sweeper.Sweep()
        
        trades = TradeHelper.GetTrades(self.loan2, self.instrument1)
        self.assertEqual(len(trades), 1, 'Expected 1 trade after second sweep, got %i' % len(trades))
        self.assert_(TradeHelper.Contains(trades, startDate, endDate, self.instrument1, 100, 0, 1, 'Principal', \
        'External', expectedVat, self.loan2, self.sblPortfolio, self.sblPortfolio.PortfolioOwner(), self.loan2.PortfolioOwner(), None, expectedTradeStatus, expectedSlCfd, rate2), 'Trade not as expected after second sweep')
        
    def testSweepCoverSblShorts(self):
        
        #------------------ Instrument 1 Positions ----------------------
        TradeHelper.BookTrade(self.sblPortfolio, self.instrument1, self.today, 150)
        
        TradeHelper.BookTrade(self.portfolio11, self.instrument1, self.today, -100)
        TradeHelper.BookTrade(self.portfolio21, self.instrument1, self.today, -50)
        
        #------------------ Instrument 2 Positions ----------------------
        TradeHelper.BookTrade(self.sblPortfolio, self.instrument2, self.today, -100)
        
        TradeHelper.BookTrade(self.portfolio11, self.instrument2, self.today, -50)
        TradeHelper.BookTrade(self.portfolio21, self.instrument2, self.today, 250)
        
        #------------------ Instrument 3 Positions ----------------------
        TradeHelper.BookTrade(self.sblPortfolio, self.instrument3, self.today, -100)
        
        TradeHelper.BookTrade(self.portfolio11, self.instrument3, self.today, 200)
        
        tradeFilter = TradeFilterHelper.CreateTradeFilter(self.portfolios)
        cfdSweep = True
        validationMode = True
        allowPartialSweeping = True
        allocateHeldPositions = True
        
        SblRatesHelper.WriteRatesFile([[self.instrument1.Name(), '', 0.2], [self.instrument2.Name(), '*', 0.3], [self.instrument3.Name(), '*', 0.35]])
        
        sweeper = sl_sweeping.SblSweeper(self.today, tradeFilter, self.sblPortfolio, not cfdSweep, SblRatesHelper.filepath, 3, self.log, not validationMode, not allowPartialSweeping, allocateHeldPositions)
        sweeper.Sweep()
        
        #------------------ Instrument 1 Positions ----------------------
        InstrumentHelper.AssertInventoryPosition(self, self.sblPortfolio, self.instrument1, self.today, 0, 'Position of sblPortfolio, instrument1 not as expected. Expected: %(expected)s, Actual: %(actual)s')
        InstrumentHelper.AssertInventoryPosition(self, self.loan1, self.instrument1, self.today, 100, 'Position of loan1, instrument1 not as expected. Expected: %(expected)s, Actual: %(actual)s')
        InstrumentHelper.AssertInventoryPosition(self, self.loan2, self.instrument1, self.today, 50, 'Position of loan2, instrument1 not as expected. Expected: %(expected)s, Actual: %(actual)s')
         
        #------------------ Instrument 2 Positions ----------------------
        InstrumentHelper.AssertInventoryPosition(self, self.sblPortfolio, self.instrument2, self.today, 0, 'Position of sblPortfolio, instrument2 not as expected. Expected: %(expected)s, Actual: %(actual)s')
        InstrumentHelper.AssertInventoryPosition(self, self.loan1, self.instrument2, self.today, 50, 'Position of loan1, instrument2 not as expected. Expected: %(expected)s, Actual: %(actual)s')
        InstrumentHelper.AssertInventoryPosition(self, self.loan2, self.instrument2, self.today, -150, 'Position of loan2, instrument2 not as expected. Expected: %(expected)s, Actual: %(actual)s')
           
        #------------------ Instrument 3 Positions ----------------------
        InstrumentHelper.AssertInventoryPosition(self, self.sblPortfolio, self.instrument3, self.today, 0, 'Position of sblPortfolio, instrument3 not as expected. Expected: %(expected)s, Actual: %(actual)s')
        InstrumentHelper.AssertInventoryPosition(self, self.loan1, self.instrument3, self.today, -100, 'Position of loan1, instrument3 not as expected. Expected: %(expected)s, Actual: %(actual)s')
        
    def testSweepMissingExternalRate(self):
        yesterday = acm.Time().DateAddDelta(self.today, 0, 0, -1)
        
        #------------------ Instrument 1 Positions ----------------------
        TradeHelper.BookSecurityLoanFromUnderlying(self.sblPortfolio, self.instrument1, 150, 1, 0.053, 'External', yesterday, 'BO Confirmed')
        #TradeHelper.BookTrade(self.sblPortfolio, self.instrument1, self.today, 150)
        
        TradeHelper.BookTrade(self.portfolio11, self.instrument1, self.today, -100)
        TradeHelper.BookTrade(self.portfolio21, self.instrument1, self.today, -50)
        
        #------------------ Instrument 2 Positions ----------------------
        TradeHelper.BookTrade(self.portfolio11, self.instrument2, self.today, -150)
        TradeHelper.BookTrade(self.portfolio21, self.instrument2, self.today, 250)
        
        #------------------ Instrument 3 Positions ----------------------
        TradeHelper.BookSecurityLoanFromUnderlying(self.sblPortfolio, self.instrument3, 50, 1, 0.053, 'External', yesterday, 'BO Confirmed')
        #TradeHelper.BookTrade(self.sblPortfolio, self.instrument3, self.today, 50)
        
        TradeHelper.BookTrade(self.portfolio11, self.instrument3, self.today, -100)
        
        tradeFilter = TradeFilterHelper.CreateTradeFilter(self.portfolios)
        cfdSweep = True
        validationMode = True
        allowPartialSweeping = True
        allocateHeldPositions = True
        
        SblRatesHelper.WriteRatesFile([[self.instrument1.Name(), '', 0.2]])
        
        sweeper = sl_sweeping.SblSweeper(self.today, tradeFilter, self.sblPortfolio, not cfdSweep, SblRatesHelper.filepath, 3, self.log, not validationMode, allowPartialSweeping, not allocateHeldPositions)
        sweeper.Sweep()
        
        #------------------ Instrument 1 Positions ----------------------
        InstrumentHelper.AssertInventoryPosition(self, self.sblPortfolio, self.instrument1, self.today, 0, 'Position of sblPortfolio, instrument1 not as expected. Expected: %(expected)s, Actual: %(actual)s')
        InstrumentHelper.AssertInventoryPosition(self, self.loan1, self.instrument1, self.today, 100, 'Position of loan1, instrument1 not as expected. Expected: %(expected)s, Actual: %(actual)s')
        InstrumentHelper.AssertInventoryPosition(self, self.loan2, self.instrument1, self.today, 50, 'Position of loan2, instrument1 not as expected. Expected: %(expected)s, Actual: %(actual)s')
         
        #------------------ Instrument 2 Positions ----------------------
        InstrumentHelper.AssertInventoryPosition(self, self.sblPortfolio, self.instrument2, self.today, 0, 'Position of sblPortfolio, instrument2 not as expected. Expected: %(expected)s, Actual: %(actual)s')
        InstrumentHelper.AssertInventoryPosition(self, self.loan1, self.instrument2, self.today, 150, 'Position of loan1, instrument2 not as expected. Expected: %(expected)s, Actual: %(actual)s')
        InstrumentHelper.AssertInventoryPosition(self, self.loan2, self.instrument2, self.today, -150, 'Position of loan2, instrument2 not as expected. Expected: %(expected)s, Actual: %(actual)s')
           
        #------------------ Instrument 3 Positions ----------------------
        InstrumentHelper.AssertInventoryPosition(self, self.sblPortfolio, self.instrument3, self.today, 50, 'Position of sblPortfolio, instrument3 not as expected. Expected: %(expected)s, Actual: %(actual)s')
        InstrumentHelper.AssertInventoryPosition(self, self.loan1, self.instrument3, self.today, 0, 'Position of loan1, instrument3 not as expected. Expected: %(expected)s, Actual: %(actual)s')
        
        expectedWarning = r'No external rate was found for \[%(instrument)s\] in column \[3\], please correct it in the file \[%(filepath)s\]\: Short of 100.* will not be covered\.' % \
            {'instrument': self.instrument3.Name(), 'filepath': SblRatesHelper.filepath.replace('\\', '\\\\')}
        expectedCompletion = r'Sweeping batch \[\d+\] completed successfully\.'
        
        SlProcessLogHelper.AssertLogContains(self, 'no external rate warning', self.log, expectedWarning, True)
        SlProcessLogHelper.AssertLogContains(self, 'batch completed successfully', self.log, expectedCompletion, True)
        
def _run_tests():
    suite = unittest.TestLoader().loadTestsFromModule(test_sl_sweeping)
    #suite = unittest.TestLoader().loadTestsFromTestCase(TestSblSweeper)
    unittest.TextTestRunner(verbosity=2).run(suite)
