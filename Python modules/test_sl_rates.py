"""--------------------------------------------------------------------------
PROJECT                 :  Security Borrowing and Lending
PURPOSE                 :  Unit tests for sl_rates module
DEPATMENT AND DESK      :  Prime Services, Securities Lending
REQUESTER               :  Linda Breytenbach
DEVELOPER               :  Francois Truter
CR NUMBER               :  494829
-----------------------------------------------------------------------------

HISTORY
=============================================================================
Date       Change no Developer          Description
-----------------------------------------------------------------------------
2010-11-16 494829    Francois Truter    Initial Implementation
2011-04-04 619099    Francois Truter    Added multiple rates per file
"""

from test_helper_general import GeneralHelper
from test_helper_instruments import InstrumentHelper
import test_helper_general
import sl_rates
import unittest
import os
import csv
import tempfile
import test_sl_rates

class SblRatesHelper:
    filepath = os.path.join(tempfile.gettempdir(), 'tmpRateFile.csv')
    cfdFilepath = os.path.join(tempfile.gettempdir(), 'tmpCfdRateFile.csv')
    
    @staticmethod        
    def _writeRatesFile(filepath, rateRows):
        with open(filepath, "w") as rateFile:
            writer = csv.writer(rateFile)
            writer.writerow([1, 2, 3, 4, 5])
            writer.writerow(['Instrument', 'Do Not Auto Return', 'Rate 1', 'Rate 2', 'Rate N'])
            for row in rateRows:
                writer.writerow(row)
            
    @staticmethod        
    def WriteRatesFile(rateRows):
        SblRatesHelper._writeRatesFile(SblRatesHelper.filepath, rateRows)
                
    @staticmethod        
    def WriteCfdRatesFile(rateRows):
        SblRatesHelper._writeRatesFile(SblRatesHelper.cfdFilepath, rateRows)
        
class TestSblRates(unittest.TestCase):

    def tearDown(self):
        if os.path.exists(SblRatesHelper.filepath):
            os.remove(SblRatesHelper.filepath)
            
        if os.path.exists(SblRatesHelper.cfdFilepath):
            os.remove(SblRatesHelper.cfdFilepath)
    
    def testGetRate(self):
        internalKey = '<<Internal>>'
        internalRate = 0.4
        spreadKey = '<<Spread>>'
        internalSpread = 0.015
        instrument1 = InstrumentHelper.CreateTemporaryStock()
        rate1 = 0.25
        instrument2 = InstrumentHelper.CreateTemporaryStock()
        rate2 = 0.1
        instrument3 = InstrumentHelper.CreateTemporaryStock()
        rateColumn = 3
        rates = sl_rates.SblRates(SblRatesHelper.filepath, rateColumn)
        
        SblRatesHelper.WriteRatesFile([[internalKey, '', internalRate], [spreadKey, '', internalSpread], [instrument1.Name(), '*', rate1], [instrument2.Name(), '', rate2]])
        
        GeneralHelper.AssertTypeAndValue(self, rates.GetRate(instrument1, True), rate1, float, 'Instrument 1 external rate not as expected')
        GeneralHelper.AssertTypeAndValue(self, rates.GetRate(instrument1, True, True), rate1, float, 'Instrument 1 external spread rate not as expected')
        GeneralHelper.AssertTypeAndValue(self, rates.GetRate(instrument1, False), internalRate, float, 'Instrument 1 internal rate not as expected')
        GeneralHelper.AssertTypeAndValue(self, rates.GetRate(instrument1, False, True), internalRate + internalSpread, float, 'Instrument 1 internal spread rate not as expected')
        
        GeneralHelper.AssertTypeAndValue(self, rates.GetRate(instrument2, True), rate2, float, 'Instrument 2 external rate not as expected')
        GeneralHelper.AssertTypeAndValue(self, rates.GetRate(instrument2, True, True), rate2, float, 'Instrument 2 external spread rate not as expected')
        GeneralHelper.AssertTypeAndValue(self, rates.GetRate(instrument2, False), internalRate, float, 'Instrument 2 internal rate not as expected')
        GeneralHelper.AssertTypeAndValue(self, rates.GetRate(instrument2, False, True), internalRate + internalSpread, float, 'Instrument 2 internal spread rate not as expected')
        
        expectedMessage = 'No external rate was found for [%(instrument)s] in column [3], please correct it in the file [%(filepath)s]' % \
                        {'instrument': instrument3.Name(), 'filepath': SblRatesHelper.filepath}
        try:
            rates.GetRate(instrument3, True)
        except Exception as ex:
           self.assert_(test_helper_general._startsWith(str(ex), expectedMessage), 'Exception message not as expected')
        else:
             self.fail('Expected an exception 1')
             
        try:
            rates.GetRate(instrument3, True, True)
        except Exception as ex:
           self.assert_(test_helper_general._startsWith(str(ex), expectedMessage), 'Exception message not as expected')
        else:
             self.fail('Expected an exception 2')

        GeneralHelper.AssertTypeAndValue(self, rates.GetRate(instrument3, False), internalRate, float, 'Instrument 3 internal rate not as expected')
        GeneralHelper.AssertTypeAndValue(self, rates.GetRate(instrument3, False, True), internalRate + internalSpread, float, 'Instrument 3 internal spread rate not as expected')        
        
    def testGetRateInvalidRate(self):
        invalidRateInstrument = 'Instrument2'
        invalidRate = 'Not a rate'
        rateColumn = 3
        rates = sl_rates.SblRates(SblRatesHelper.filepath, rateColumn)
        SblRatesHelper.WriteRatesFile([[invalidRateInstrument, '', invalidRate], ['Instrument3', '', '0.1']])
        try:
            rates.GetRate('Instrument1', True)
        except Exception as ex:
            expectedMessage = 'The rate [%(rate)s] for [%(instrument)s] in column [3] is invalid, please correct it in the file [%(filepath)s]:' % \
                        {'rate': invalidRate, 'instrument': invalidRateInstrument, 'filepath': SblRatesHelper.filepath}
            self.assert_(test_helper_general._startsWith(str(ex), expectedMessage), 'Exception message not as expected')
        else:
            self.fail('Expected an exception')
            
    def testInvalidColumn(self):
        rateColumn = 1
        rates = sl_rates.SblRates(SblRatesHelper.filepath, rateColumn)
        expectedMessage = 'Rates cannot be stored in column %i. Column 1 should contain the instrument code, even columns (2, 4, 6, etc) should contain the Auto Return marker and rates should be stored in uneven columns (3, 5, 7, etc).' % rateColumn
        GeneralHelper.AssertRaises(self, rates.GetRate, expectedMessage, 'Instrument1', True)
        
        rateColumn = 4
        rates = sl_rates.SblRates(SblRatesHelper.filepath, rateColumn)
        expectedMessage = 'Rates cannot be stored in column %i. Column 1 should contain the instrument code, even columns (2, 4, 6, etc) should contain the Auto Return marker and rates should be stored in uneven columns (3, 5, 7, etc).' % rateColumn
        GeneralHelper.AssertRaises(self, rates.GetRate, expectedMessage, 'Instrument1', True)
        
    def testMultipleRateColumns(self):
        DEFAULT_INTERNAL_RATE = 0.35
        DEFAULT_SPREAD = 0.01
        EXTERNAL = True
        INTERNAL = False
        SPREAD = True
        
        internalKey = '<<Internal>>'
        internalRate1 = 0.4
        internalRate2 = 0.5
        internalRate3 = ''
        
        spreadKey = '<<Spread>>'
        spread1 = 0.015
        spread2 = ''
        spread3 = 0.02
        
        instrument1 = InstrumentHelper.CreateTemporaryStock()
        held11 = '*'
        rate11 = 0.25
        held12 = ''
        rate12 = 0.3
        held13 = '*'
        
        instrument2 = InstrumentHelper.CreateTemporaryStock()
        held21 = '*'
        rate21 = 0.18
        held22 = '*'
        rate22 = ''
        held23 = ''
        rate23 = 0.19
        
        SblRatesHelper.WriteRatesFile([[internalKey, '', internalRate1, '', internalRate2, '', internalRate3], [spreadKey, '', spread1, '', spread2, '', spread3], [instrument1.Name(), held11, rate11, held12, rate12, held13], [instrument2.Name(), held21, rate21, held22, rate22, held23, rate23]])
        
        #RATE COLUMN 3
        rates = sl_rates.SblRates(SblRatesHelper.filepath, 3)
        
        self.failIf(rates.CanAutoReturn(instrument1), 'Expected False for instrument 1 column 3')
        GeneralHelper.AssertTypeAndValue(self, rates.GetRate(instrument1, EXTERNAL, not SPREAD), rate11, float, 'Instrument 1 external rate 1 not as expected')
        GeneralHelper.AssertTypeAndValue(self, rates.GetRate(instrument1, EXTERNAL, SPREAD), rate11, float, 'Instrument 1 external spread rate 1 not as expected')
        GeneralHelper.AssertTypeAndValue(self, rates.GetRate(instrument1, INTERNAL, not SPREAD), internalRate1, float, 'Instrument 1 internal rate 1 not as expected')
        GeneralHelper.AssertTypeAndValue(self, rates.GetRate(instrument1, INTERNAL, SPREAD), internalRate1 + spread1, float, 'Instrument 1 internal spread rate 1 not as expected')
        
        self.failIf(rates.CanAutoReturn(instrument2), 'Expected False for instrument 2 column 3')
        GeneralHelper.AssertTypeAndValue(self, rates.GetRate(instrument2, EXTERNAL, not SPREAD), rate21, float, 'Instrument 2 external rate 1 not as expected')
        GeneralHelper.AssertTypeAndValue(self, rates.GetRate(instrument2, EXTERNAL, SPREAD), rate21, float, 'Instrument 2 external spread rate 1 not as expected')
        GeneralHelper.AssertTypeAndValue(self, rates.GetRate(instrument2, INTERNAL, not SPREAD), internalRate1, float, 'Instrument 2 internal rate 1 not as expected')
        GeneralHelper.AssertTypeAndValue(self, rates.GetRate(instrument2, INTERNAL, SPREAD), internalRate1 + spread1, float, 'Instrument 2 internal spread rate 1 not as expected')
        
        #RATE COLUMN 5
        rates = sl_rates.SblRates(SblRatesHelper.filepath, 5)
        
        self.assert_(rates.CanAutoReturn(instrument1), 'Expected True for instrument 1 column 5')
        GeneralHelper.AssertTypeAndValue(self, rates.GetRate(instrument1, EXTERNAL, not SPREAD), rate12, float, 'Instrument 1 external rate 2 not as expected')
        GeneralHelper.AssertTypeAndValue(self, rates.GetRate(instrument1, EXTERNAL, SPREAD), rate12, float, 'Instrument 1 external spread rate 2 not as expected')
        GeneralHelper.AssertTypeAndValue(self, rates.GetRate(instrument1, INTERNAL, not SPREAD), internalRate2, float, 'Instrument 1 internal rate 2 not as expected')
        GeneralHelper.AssertTypeAndValue(self, rates.GetRate(instrument1, INTERNAL, SPREAD), internalRate2 + DEFAULT_SPREAD, float, 'Instrument 1 internal spread rate 2 not as expected')
        
        self.failIf(rates.CanAutoReturn(instrument2), 'Expected True for instrument 2 column 5')
        expectedMessage = 'No external rate was found for [%(instrument)s] in column [5], please correct it in the file [%(filepath)s]' % \
            {'instrument': instrument2.Name(), 'filepath': SblRatesHelper.filepath}
        GeneralHelper.AssertRaises(self, rates.GetRate, expectedMessage, instrument2, EXTERNAL)
        GeneralHelper.AssertTypeAndValue(self, rates.GetRate(instrument2, INTERNAL, not SPREAD), internalRate2, float, 'Instrument 2 internal rate 2 not as expected')
        GeneralHelper.AssertTypeAndValue(self, rates.GetRate(instrument2, INTERNAL, SPREAD), internalRate2 + DEFAULT_SPREAD, float, 'Instrument 2 internal spread rate 2 not as expected')
        
        #RATE COLUMN 7
        rates = sl_rates.SblRates(SblRatesHelper.filepath, 7)
        
        self.failIf(rates.CanAutoReturn(instrument1), 'Expected True for instrument 1 column 7')
        expectedMessage = 'No external rate was found for [%(instrument)s] in column [7], please correct it in the file [%(filepath)s]' % \
            {'instrument': instrument1.Name(), 'filepath': SblRatesHelper.filepath}
        GeneralHelper.AssertRaises(self, rates.GetRate, expectedMessage, instrument1, EXTERNAL)
        GeneralHelper.AssertTypeAndValue(self, rates.GetRate(instrument1, INTERNAL, not SPREAD), DEFAULT_INTERNAL_RATE, float, 'Instrument 1 internal rate 3 not as expected')
        GeneralHelper.AssertTypeAndValue(self, rates.GetRate(instrument1, INTERNAL, SPREAD), DEFAULT_INTERNAL_RATE + spread3, float, 'Instrument 1 internal spread rate 3 not as expected')
        
        self.assert_(rates.CanAutoReturn(instrument2), 'Expected True for instrument 2 column 7')
        GeneralHelper.AssertTypeAndValue(self, rates.GetRate(instrument2, EXTERNAL, not SPREAD), rate23, float, 'Instrument 2 external rate 3 not as expected')
        GeneralHelper.AssertTypeAndValue(self, rates.GetRate(instrument2, EXTERNAL, SPREAD), rate23, float, 'Instrument 2 external spread rate 3 not as expected')
        GeneralHelper.AssertTypeAndValue(self, rates.GetRate(instrument2, INTERNAL, not SPREAD), DEFAULT_INTERNAL_RATE, float, 'Instrument 2 internal rate 3 not as expected')
        GeneralHelper.AssertTypeAndValue(self, rates.GetRate(instrument2, INTERNAL, SPREAD), DEFAULT_INTERNAL_RATE + spread3, float, 'Instrument 2 internal spread rate 3 not as expected')
        
    def testSimultaneousUse(self):
        internalKey = '<<Internal>>'
        internalRate = 0.4
        cfdInternalRate = 0.5
        spreadKey = '<<Spread>>'
        internalSpread = 0.015
        cfdInternalSpread = 0.02
        instrument1 = InstrumentHelper.CreateTemporaryStock()
        rate1 = 0.25
        cfdRate1 = 0.3
        instrument2 = InstrumentHelper.CreateTemporaryStock()
        rate2 = 0.18
        
        rateColumn = 3
        rates = sl_rates.SblRates(SblRatesHelper.filepath, rateColumn)
        cfdRates = sl_rates.SblRates(SblRatesHelper.cfdFilepath, rateColumn)
        
        SblRatesHelper.WriteRatesFile([[internalKey, '', internalRate], [spreadKey, '', internalSpread], [instrument1.Name(), '*', rate1], [instrument2.Name(), '', rate2]])
        SblRatesHelper.WriteCfdRatesFile([[internalKey, '', cfdInternalRate], [spreadKey, '*', cfdInternalSpread], [instrument1.Name(), '', cfdRate1]])
        
        GeneralHelper.AssertTypeAndValue(self, rates.GetRate(instrument1, True), rate1, float, 'Instrument 1 external rate not as expected')
        GeneralHelper.AssertTypeAndValue(self, rates.GetRate(instrument1, True, True), rate1, float, 'Instrument 1 external spread rate not as expected')
        GeneralHelper.AssertTypeAndValue(self, rates.GetRate(instrument1, False), internalRate, float, 'Instrument 1 internal rate not as expected')
        GeneralHelper.AssertTypeAndValue(self, rates.GetRate(instrument1, False, True), internalRate + internalSpread, float, 'Instrument 1 internal spread rate not as expected')
        
        GeneralHelper.AssertTypeAndValue(self, cfdRates.GetRate(instrument1, True), cfdRate1, float, 'Instrument 1 external cfd rate not as expected')
        GeneralHelper.AssertTypeAndValue(self, cfdRates.GetRate(instrument1, True, True), cfdRate1, float, 'Instrument 1 external cfd spread rate not as expected')
        GeneralHelper.AssertTypeAndValue(self, cfdRates.GetRate(instrument1, False), cfdInternalRate, float, 'Instrument 1 internal cfd rate not as expected')
        GeneralHelper.AssertTypeAndValue(self, cfdRates.GetRate(instrument1, False, True), cfdInternalRate + cfdInternalSpread, float, 'Instrument 1 internal cfd spread rate not as expected')
        
        GeneralHelper.AssertTypeAndValue(self, rates.GetRate(instrument2, True), rate2, float, 'Instrument 2 external rate not as expected')
        
        expectedMessage = 'No external rate was found for [%(instrument)s] in column [3], please correct it in the file [%(filepath)s]' % \
                        {'instrument': instrument2.Name(), 'filepath': SblRatesHelper.cfdFilepath}
        try:
            cfdRates.GetRate(instrument2, True)
        except Exception as ex:
           self.assert_(test_helper_general._startsWith(str(ex), expectedMessage), 'Exception message not as expected')
        else:
             self.fail('Expected an exception when reading external rate for instrument 2 from cfd file')
             
    def testCanAutoReturn(self):
        instrument1 = InstrumentHelper.CreateTemporaryStock()
        instrument2 = InstrumentHelper.CreateTemporaryStock()
        instrument3 = InstrumentHelper.CreateTemporaryStock()
        instrument4 = InstrumentHelper.CreateTemporaryStock()
        
        rateColumn = 3
        rates = sl_rates.SblRates(SblRatesHelper.filepath, rateColumn)
        
        SblRatesHelper.WriteRatesFile([[instrument1.Name(), '', '0.1'], [instrument2.Name(), '*', '0.5'], [instrument3.Name(), '', '0.5']])
        
        self.assertTrue(rates.CanAutoReturn(instrument1), 'Expected True for instrument1')
        self.assertFalse(rates.CanAutoReturn(instrument2), 'Expected False for instrument2')
        self.assertTrue(rates.CanAutoReturn(instrument3), 'Expected True for instrument3')
        self.assertTrue(rates.CanAutoReturn(instrument4), 'Expected True for instrument4')
        
    def testGetValidRateColumns(self):
        values = sl_rates.SblRates.GetValidRateColumns(10)
        expected = 3
        for v in values:
            self.assertEqual(expected, v, 'Expected %i, got %s' % (expected, v))
            expected += 2
            
    def testHasExternalRate(self):
        instrument1 = InstrumentHelper.CreateTemporaryStock()
        instrument2 = InstrumentHelper.CreateTemporaryStock()
        rateColumn = 3
        rates = sl_rates.SblRates(SblRatesHelper.filepath, rateColumn)
        SblRatesHelper.WriteRatesFile([[instrument1.Name(), '', '0.1'], ['OtherInstrument_XXX', '*', '0.2']])
        self.assertTrue(rates.HasExternalRate(instrument1), 'Expected True for instrument1 - there is an external rate')
        self.assertFalse(rates.HasExternalRate(instrument2), 'Expected False for instrument2 - there is not an external rate')
        
    def testNoExternalRateMessage(self):
        instrument = InstrumentHelper.CreateTemporaryStock()
        column = 3
        rates = sl_rates.SblRates(SblRatesHelper.filepath, column)
        self.assertEqual(rates.NoExternalRateMessage(instrument), 'No external rate was found for [%(instrument)s] in column [%(column)i], please correct it in the file [%(filepath)s]' % 
            {'instrument': instrument.Name(), 'column': column, 'filepath': SblRatesHelper.filepath}, 'NoExternalRateMessage not as expected')

def _run_tests():
    suite = unittest.TestLoader().loadTestsFromModule(test_sl_rates)
    unittest.TextTestRunner(verbosity=2).run(suite)
