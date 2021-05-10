"""-----------------------------------------------------------------------------
PURPOSE                 :  Unit tests for sl_change_underlying
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
import test_sl_change_underlying
import unittest
import sl_change_underlying
from test_helper_instruments import InstrumentHelper
from sl_process_log import ProcessLog
from test_sl_process_log import SlProcessLogHelper

TODAY = acm.Time().DateNow()
TOMORROW = acm.Time().DateAddDelta(TODAY, 0, 0, 1)
YESTERDAY = acm.Time().DateAddDelta(TODAY, 0, 0, -1)
LAST_MONTH = acm.Time().DateAddDelta(TODAY, 0, -1, 0)

def _getSecurityLoans(underlying):
    query = acm.CreateFASQLQuery('FSecurityLoan', 'AND')
    
    op = query.AddOpNode('AND')
    op.AddAttrNode('Underlying.Oid', 'EQUAL', underlying.Oid())
            
    return query.Select()

class TestSlChangeUnderlying(unittest.TestCase):
    
    def setUp(self):
        #-------------------- Underlying 1 --------------------
        self.underlying1 = InstrumentHelper.CreatePersistantStock()
        self.loan11 = InstrumentHelper.CreateSecurityLoanFromUnderlying(self.underlying1, 10, 0.5, 'Internal', LAST_MONTH, None, None, YESTERDAY)
        
        self.loan12 = InstrumentHelper.CreateSecurityLoanFromUnderlying(self.underlying1, 10, 0.5, 'Internal', LAST_MONTH, None, None, YESTERDAY)
        self.loan12.OpenEnd('None')
        self.loan12.Commit()
        
        self.loan13 = InstrumentHelper.CreateSecurityLoanFromUnderlying(self.underlying1, 10, 0.5, 'External', LAST_MONTH, None, None, TOMORROW)
        self.loan13.OpenEnd('None')
        self.loan13.Commit()
        
        #-------------------- Underlying 2 --------------------
        self.underlying2 = InstrumentHelper.CreatePersistantStock()
        self.loan21 = InstrumentHelper.CreateSecurityLoanFromUnderlying(self.underlying2, 10, 0.5, 'Internal', LAST_MONTH, None, None, TOMORROW)
        
        #-------------------- Underlying 3 --------------------
        self.underlying3 = InstrumentHelper.CreatePersistantStock()
        self.loan31 = InstrumentHelper.CreateSecurityLoanFromUnderlying(self.underlying3, 10, 0.5, 'Internal', LAST_MONTH, None, None, TOMORROW)
        
    def testChangeUnderlyingInstrument(self):
        log = ProcessLog('testChangeUnderlyingInstrument')
        sl_change_underlying.ChangeUnderlyingInstrument(self.underlying1, self.underlying2, log)
        SlProcessLogHelper.AssertLogContains(self, 'Could not find message', log, '2 security loans updated')
        
        withUnderlying1 = _getSecurityLoans(self.underlying1)
        self.assertEqual(1, len(withUnderlying1), 'Expected 1 loan with underlying1, got %i' % len(withUnderlying1))
        self.assertEqual(self.loan12, withUnderlying1[0], 'Expected loan12')
        
        withUnderlying2 = _getSecurityLoans(self.underlying2)
        self.assertEqual(3, len(withUnderlying2), 'Expected 3 loans with underlying2, got %i' % len(withUnderlying2))
        expected = [self.loan11, self.loan13, self.loan21]
        for loan in withUnderlying2:
            if loan in expected:
                expected.remove(loan)
            else:
                self.fail('Could not find loan')

def _run_tests():
    suite = unittest.TestLoader().loadTestsFromModule(test_sl_change_underlying)
    unittest.TextTestRunner(verbosity=2).run(suite)
