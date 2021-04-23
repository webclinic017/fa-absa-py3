"""-----------------------------------------------------------------------------
PROJECT                 :  Security Borrowing and Lending (CFD Implementation)
PURPOSE                 :  Unit tests for sl_process_log module
DEPATMENT AND DESK      :  Prime Services, Securities Lending
REQUESTER               :  Linda Breytenbach
DEVELOPER               :  Francois Truter
CR NUMBER               :  502781
-----------------------------------------------------------------------------

HISTORY
=============================================================================
Date       Change no Developer          Description
-----------------------------------------------------------------------------
2010-11-16 494829    Francois Truter    Initial implementation
2010-11-23 502781    Francois Truter    Added AssertLogNotContains
2011-04-04 619099    Francois Truter    Added RegEx searching
"""

import unittest
import sl_process_log
import string
import re
import test_sl_process_log

class SlProcessLogHelper:

    @staticmethod
    def AssertLogContains(testCase, errorMessage, log, searchMessage, isRegex = False):
        logStr = str(log)
        if isRegex:
            if not re.search(searchMessage, logStr):
                testCase.fail('%s: Did not find "%s" in process log.' % (errorMessage, searchMessage))
        else:
            try:
                string.index(logStr, searchMessage)
            except ValueError:
                testCase.fail('%s: Did not find "%s" in process log.' % (errorMessage, searchMessage))
            
    @staticmethod
    def AssertLogNotContains(testCase, errorMessage, log, searchMessage, isRegex = False):
        logStr = str(log)
        if isRegex:
            if re.search(searchMessage, logStr):
                testCase.fail('%s: Did not expect to find "%s" in process log.' % (errorMessage, searchMessage))
        else:
            if string.find(logStr, searchMessage) != -1:
                testCase.fail('%s: Did not expect to find "%s" in process log.' % (errorMessage, searchMessage))

class TestProcessLog(unittest.TestCase):

    def testLog(self):
        expected = r'''--------------------------------------------------------------------------------
Test Log Name started at \d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d
Current time: \d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d
Time elapsed: \d:\d\d:\d\d\.\d*
--------------------------------------------------------------------------------
!!!A serious error has occurred and this process has been stopped. Please review the message log for the EXCEPTION that caused this!!!
4 ERRORS were logged. Please review the log messages and take corrective action.
2 warnings were logged. Please review the log messages.
--------------------------------------------------------------------------------
Log Messages:
--------------
\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d Information : Information message 1
\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d Information : Information message 2
\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d Warning     : Warning message 1
\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d Warning     : Warning message 2
\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d Error       : Error message 1
\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d Error       : Error message 2
\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d Error       : Error message 3
\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d Exception   : Exception message to be raised
                                    File "\[Standard\]/test_sl_process_log", line \d*, in testLog
                                  
\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d Exception   : Exception message
                                    File "\[Standard\]/test_sl_process_log", line \d*, in testLog
                                  
\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d Error       : Exception message not to be raised
--------------------------------------------------------------------------------'''
    
        logName = 'Test Log Name'
        info1 = 'Information message 1'
        info2 = 'Information message 2'
        warning1 = 'Warning message 1'
        warning2 = 'Warning message 2'
        error1 = 'Error message 1'
        error2 = 'Error message 2'
        error3 = 'Error message 3'
        exception = 'Exception message'
        raiseException = 'Exception message to be raised'
        raiseException2 = 'Exception message not to be raised'
        
        log = sl_process_log.ProcessLog(logName)
        log.Information(info1)
        log.Information(info2)
        log.Warning(warning1)
        log.Warning(warning2)
        log.Error(error1)
        log.Error(error2)
        log.Error(error3)
        
        try:
            log.RaiseException(raiseException)
        except sl_process_log.ProcessLogException, ex:
            pass
        except Exception, ex:
            import traceback
            for line in traceback.format_stack():
                print(line)
            self.fail('Expected a ProcessLogException exception')
        else:
            self.fail('Expected an exception')
            
        try:
            raise Exception(exception)
        except Exception, ex:
            log.Exception(exception)
            
        log.RaiseException(raiseException2, False)
        print(log)
        if not re.match(expected, str(log), re.MULTILINE):
            self.fail('Log string not as expected')
            
def _run_tests():
    suite = unittest.TestLoader().loadTestsFromModule(test_sl_process_log)
    unittest.TextTestRunner(verbosity=2).run(suite)
