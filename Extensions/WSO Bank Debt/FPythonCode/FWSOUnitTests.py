""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BankDebtWSO/test/cunit/test_FWSOUnitTests.py"

"""
#owner:Prime-OMS
#email:FrontArena.ProductSolutions.Dev@fisglobal.com
#AMF #WSOBankDebt
"""
import unittest

import acm
import sys


class MockImporter(object):
    ''' Utility function for unit tests.
        Attempts to import the Python library mock.
        The library mock is not available by default in PRIME.
    '''
    
    @classmethod
    def _AttemptImport(cls):
        try:
            import mock
        except ImportError as e:
            return False
        return True

    @classmethod
    def _AppendLibraryPath(cls):
        try:
            sys.path.append(r'C:\Python26\Lib\site-packages')
        except Exception as e:
            pass
        
    @classmethod
    def _AttemptAfterAppending(cls):
        cls._AppendLibraryPath()
        success = cls._AttemptImport()
        return success

    @classmethod
    def ImportMock(cls):
        success = cls._AttemptImport()
        if success:
            return True
        success = cls._AttemptAfterAppending()
        return success
    
    @classmethod
    def IsAvailable(cls):
        return cls.ImportMock()

if MockImporter.IsAvailable():
    import mock


def RunAllTests(eii=None):

    import FWSOTestCashflowFactory
    import FWSOTestExternalValuesContract
    import FWSOTestExternalValuesFacility
    import FWSOTestExternalValuesTrade
    import FWSOTestWSOFile
    import FWSOTestFileFormatHook
    import FWSOTestIPFCalculations
    import FWSOTestWSODictAccessor
    import FWSOTestWSODictToFrnDetailsDict
    import FWSOTestWSODictToTradeDict
    
    
    testClassesToRun = []
                        

    # Uses mock
    testClassesWithMock = [
                           FWSOTestCashflowFactory.TestCashflowFactory,
                           FWSOTestExternalValuesContract.TestFWSOExternalValuesContract,
                           FWSOTestExternalValuesFacility.TestFWSOExternalValuesFacility,
                           FWSOTestExternalValuesTrade.TestFWSOExternalValuesTrade,
                           FWSOTestWSOFile.TestWSOFile,
                           FWSOTestFileFormatHook.TestWSOFileFormatHook,
                           FWSOTestIPFCalculations.TestContractDetail,
                           FWSOTestIPFCalculations.TestIPFNominalCalculatorRealIPFs,
                           FWSOTestWSODictAccessor.TestWSODictAccessor,
                           FWSOTestWSODictToFrnDetailsDict.TestWSODictToFrnDetailsDict,
                           FWSOTestWSODictToFrnDetailsDict.TestContractIdContractDetailIPFDictsCreator,
                           FWSOTestWSODictToFrnDetailsDict.TestIPFPeriods,
                           FWSOTestWSODictToTradeDict.TestWSODictToTradeDict,
                          ]
    
    if MockImporter.IsAvailable():
        testClassesToRun.extend(testClassesWithMock)
    else:
        print('Test Info: The Python library mock is unavailable - tests using mock will not be run.')

    testSuite = unittest.TestSuite()
    for testClass in testClassesToRun:
        testSuite.addTest(unittest.TestLoader().loadTestsFromTestCase(testClass))

    runner = unittest.TextTestRunner()
    return runner.run(testSuite)


#RunAllTests()
