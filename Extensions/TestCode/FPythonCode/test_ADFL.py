

import unittest
import acm

class TestADFL(unittest.TestCase):
    
    def eval_adfl(self, adflexpr):
        return acm.GetCalculatedValueFromString("", acm.GetDefaultContext(), adflexpr, acm.CreateEBTag()).Value()

    def test_subscripts(self):        
        """Test ADFL subscript operator [] SPR 268123"""
        self.assertEqual( self.eval_adfl(""" [1,2,3][0] """), 1)
        self.assertEqual( self.eval_adfl(""" [1,2,3][1] """), 2)
        self.assertEqual( self.eval_adfl(""" [1,2,3][2] """), 3)
        self.assertRaises( RuntimeError, self.eval_adfl, """ [1,2,3][-1] """)
        self.assertRaises( RuntimeError, self.eval_adfl, """ [1,2,3][4] """)
        self.assertRaises( RuntimeError, self.eval_adfl, """ [1,2,3][] """)
        self.assertEqual( self.eval_adfl(""" [[1,2]][0,0] """), 1)
        self.assertEqual( self.eval_adfl(""" [[1,2]][0,1] """), 2)
        





