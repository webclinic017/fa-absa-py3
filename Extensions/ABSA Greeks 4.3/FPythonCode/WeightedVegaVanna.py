"""-----------------------------------------------------------------------------
MODULE
    WeightedVegaVanna

DESCRIPTION
    Date                : 2012-02-16
    Purpose             : Calculates the weights that is used in the weighted Term Vega and Term Vanna Cash columns
    Department and Desk : Equity Derivatives
    Requester           : Andre Checin
    Developer           : Eben Mare
    CR Number           : 891053
ENDDESCRIPTION

HISTORY
================================================================================
Date       Change no    Developer          Description
--------------------------------------------------------------------------------
2012-02-16 891053       Eben Mare          Initial implementation
-----------------------------------------------------------------------------"""
import math
import unittest

class ExponentialInterp:
    RateConstFactor = 1.0 / 10000.0

    def __init__(self, p0, pInf, rate):
        self._p0 = p0
        self._pInf = pInf
        self._rate = rate
        
    def Calculate(self, numDaysToExpiry):
        rateFactor = self._rate * self.RateConstFactor * numDaysToExpiry
        interp = self._pInf + ( (self._p0 - self._pInf) * (1 - math.exp(-rateFactor))) / rateFactor
        return interp

def CalculateWeight(weightedVegaT0, weightedVegaTInf, weightedVegaRate, numDaysToExpiry):
    decayCalc = ExponentialInterp(weightedVegaT0, weightedVegaTInf, weightedVegaRate)
    if not numDaysToExpiry:
        return 0
    else:
        return decayCalc.Calculate(numDaysToExpiry)


class TestExponentialInterp(unittest.TestCase):
    def testInterp(self):
        decayCalc = ExponentialInterp(1.6, 0, 83.33)
        self.assertAlmostEqual(decayCalc.Calculate(99), 1.089499183442110, 12, "numDaysToExpiry=99")
        self.assertAlmostEqual(decayCalc.Calculate(316), 0.5639641273222810, 12, "numDaysToExpiry=316")
        
    def runTest(self):
        suite = unittest.TestLoader().loadTestsFromTestCase(TestExponentialInterp)
        unittest.TextTestRunner(verbosity=2).run(suite)
