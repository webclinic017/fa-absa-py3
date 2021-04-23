"""-----------------------------------------------------------------------------
PURPOSE                 :  Unit tests for copy_instrument_prices
DEPATMENT AND DESK      :  SM PCG - Securities Lending Desk
REQUESTER               :  Marko Milutinovic
DEVELOPER               :  Francois Truter
CR NUMBER               :  526074
-----------------------------------------------------------------------------

HISTORY
=============================================================================
Date       Change no Developer          Description
-----------------------------------------------------------------------------
2010-12-17 526074    Francois Truter    Initial Implementation
"""

import acm
import test_copy_instrument_prices
import unittest
import copy_instrument_prices
from sl_process_log import ProcessLog
from test_helper_general import PriceHelper
from test_helper_general import PartyHelper
from test_helper_instruments import InstrumentHelper
from test_sl_process_log import SlProcessLogHelper

TODAY = acm.Time().DateNow()
YESTERDAY = acm.Time().DateAddDelta(TODAY, 0, 0, -1)
LAST_MONTH = acm.Time().DateAddDelta(TODAY, 0, -1, 0)

class TestCopyInstrumentPrices(unittest.TestCase):

    def setUp(self):
        self.marketPlace1 = PartyHelper.GetPersistantMarketPlace()
        self.marketPlace2 = PartyHelper.GetPersistantMarketPlace()
        self.mtmMarket1 = PartyHelper.GetPersistantFMTMMarket()
        
    def tearDown(self):
        PartyHelper.DeleteParty(self.marketPlace1)
        PartyHelper.DeleteParty(self.marketPlace2)
        PartyHelper.DeleteParty(self.mtmMarket1)
        
    def testGetMarket(self):
        marketPlace = copy_instrument_prices.GetMarket(self.marketPlace1.Name())
        PartyHelper.AssertParty(self, marketPlace, self.marketPlace1, 'Market Place not as expected.')
        mtmMarket = copy_instrument_prices.GetMarket(self.mtmMarket1.Name())
        PartyHelper.AssertParty(self, mtmMarket, self.mtmMarket1, 'MTM Market not as expected.')
        
    def testGetMarketNotExists(self):
        name = PartyHelper.GetPartyNameNotExists()
        try:
            copy_instrument_prices.GetMarket(name)
        except Exception as ex:
            expected = 'Could not load market [%s].' % name
            self.assertEqual(expected, str(ex), 'Exception message not as expected. Expected [%(expected)s], got [%(actual)s]' % {'expected': expected, 'actual': str(ex)})
        else:
            self.fail('Expected an exception when trying to load a market that does not exist.')
            
    def testCopyHistoricalPrices(self):
        price1 = 10
        price2 = 12
        price3 = 15
        price4 = 18
        price5 = 19
        source = InstrumentHelper.CreatePersistantStock(None)
        PriceHelper.CreatePrice(source, price1, LAST_MONTH, self.marketPlace1)
        PriceHelper.CreatePrice(source, price2, YESTERDAY, self.marketPlace1)
        PriceHelper.CreatePrice(source, price3, TODAY, self.marketPlace1)
        PriceHelper.CreatePrice(source, price4, YESTERDAY, self.mtmMarket1)
        PriceHelper.CreatePrice(source, price5, TODAY, self.mtmMarket1)
        
        price6 = 100
        price7 = 101
        destination = InstrumentHelper.CreatePersistantStock(None)
        PriceHelper.CreatePrice(destination, price6, YESTERDAY, self.marketPlace1)
        PriceHelper.CreatePrice(destination, price7, TODAY, self.marketPlace1)
        PriceHelper.CreatePrice(destination, price6, YESTERDAY, self.marketPlace2)
        
        log = ProcessLog('testCopyPrices')
        copy_instrument_prices.CopyHistoricalPrices(source, destination, [self.marketPlace1, self.mtmMarket1], log)
        
        SlProcessLogHelper.AssertLogContains(self, 'Could not find copied message', log, 'Copied 3 price(s)')
        PriceHelper.AssertMarketPrices(self, destination, self.marketPlace1, [(LAST_MONTH, price1), (YESTERDAY, price2), (TODAY, price7)], 'Prices for destination instrument [%s] marketPlace1 not as expected.' % destination.Name())
        PriceHelper.AssertMarketPrices(self, destination, self.mtmMarket1, [(YESTERDAY, price4)], 'Prices for destination instrument [%s] mtmMarket1 not as expected.' % destination.Name())
        PriceHelper.AssertMarketPrices(self, destination, self.marketPlace2, [(YESTERDAY, price6)], 'Prices for destination instrument [%s] marketPlace2 not as expected.' % destination.Name())

def _run_tests():
    suite = unittest.TestLoader().loadTestsFromModule(test_copy_instrument_prices)
    unittest.TextTestRunner(verbosity=2).run(suite)
