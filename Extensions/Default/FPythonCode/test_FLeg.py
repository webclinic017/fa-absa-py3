

import unittest
import acm

class TestFLeg(unittest.TestCase):
    def test_CreateCashFlow(self):
        """Test CreateCashFlow - SPR 271570"""
        i = acm.FSwap()
        i.CreateLeg(True) 
        self.assertTrue( len(i.PayLeg().CashFlows()) == 0 )
        i.PayLeg().CreateCashFlow()
        self.assertTrue( len(i.PayLeg().CashFlows()) == 1)





