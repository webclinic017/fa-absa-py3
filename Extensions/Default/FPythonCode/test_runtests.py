


""" Run PRIME unit tests 

This module contains various helper functions for running the unittests built into PRIME

2007-01-07 Initial version  - Daniel R

Copyright 2007 SunGard FRONT ARENA

"""

import glob
import sys
import unittest

# This list is generated and set by the build_test_modules.py script located 
# in the MainApp directory when the python scripts are packaged into a PRIME
# extension module. DON'T CHANGE this line in any way as it is searched and 
# replaced:
LIST_OF_ALL_MODULES = ['BDPTestCommon', 'FAggregationTest', 'FExpirationTest', 'FMarkToMarketTest', 'ParseCsvFiles', 'test_ACM_type_casts', 'test_ADFL', 'test_AelToAcm', 'test_FIndexedCollection', 'test_FLeg', 'test_FMtMPerform', 'test_FMtMTask', 'test_FReportAPI', 'test_FSQL', 'test_UserDefinedMonteCarlo', 'test_nothing', 'test_runtests']

def get_all_modules_to_test():
    """Return list of all modules to test"""
    if LIST_OF_ALL_MODULES:
        return LIST_OF_ALL_MODULES
    # We are running externally and LIST_OF_ALL_MODULES has not been set
    # resort to returning a list of all .py files in current directory
    return [ fname[0:-3] for fname in glob.glob("*.py") ]

def test_modules(module_names):
    """Run all unittests in the named modules"""
    test_loader = unittest.defaultTestLoader 
    suite = unittest.TestSuite()
    for modname in module_names:
        suite.addTest( test_loader.loadTestsFromName(modname) )
    res = unittest.TextTestRunner(verbosity=2).run(suite)
    # note to capture oputput use keyword parameter stream
    sys.stderr.flush()
    if res.wasSuccessful():
        print ("All tests PASSED.")
    else:
        print ("Some tests FAILED.")
        
def run_tests_in_this_module():
    """Run all unit tests in the module which makes a call to this function
    
    Typical used during devlopment of tests in the following manner:
    
    import unittest
    
    ... code containing one or more unit tests ...
    
    import test_runtests
    test_runtests.run_tests_in_this_module()
    """
    frame = sys._getframe(1)
    module_name = frame.f_globals['__name__']
    test_modules( [module_name] )
    
def run_all_unit_tests():
    """Top level function to import and run all unit tests"""
    test_modules(get_all_modules_to_test())


if __name__ == '__main__':
    print (get_all_modules_to_test())
    run_all_unit_tests()





