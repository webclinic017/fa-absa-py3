"""-----------------------------------------------------------------------------
PROJECT                 :  N/A
PURPOSE                 :  Executes all the test modules
DEPATMENT AND DESK      :  N/A
REQUESTER               :  N/A
DEVELOPER               :  Francois Truter and Paul Jacot-Guillarmod
CR NUMBER               :  494829
-----------------------------------------------------------------------------

HISTORY
=============================================================================
Date       Change no Developer          Description
-----------------------------------------------------------------------------
2010-11-16 494829    FT & PJG           Initial implementation
"""

import acm
import unittest

def get_test_modules():
    test_modules = [
        'test_partial_returns', 
        'test_extend_security_loans',
        'test_sl_auto_return',
        'test_sl_batch',
        'test_sl_process_log',
        'test_sl_rates',
        'test_sl_sweeping'
    ]
    return test_modules
    
def run_test_modules():
    suite = unittest.TestSuite()
    for module_name in get_test_modules():
        module = __import__(module_name)
        suite.addTest(unittest.TestLoader().loadTestsFromModule(module))
        
    unittest.TextTestRunner(verbosity=2).run(suite)
        
#run_test_modules()
