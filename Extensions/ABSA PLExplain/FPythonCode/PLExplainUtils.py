""" 
MODULE
    PLExplainUtils - Gino Bellato March 2020

DESCRIPTION
    This module contains custom functions used in the FArtiQMarketRiskExport and PLExplainUtils_PL
---------------------------------------------------------------------------"""

import acm
from ArenaFunctionBridge import instrument_used_price
today = acm.Time().DateNow()

def check_measures_PLcolumn(measures):
    if measures:
        for i in measures:
            if 'PL' in i:
                return True
            else:
                return False
    else:
        return False

def getBenchmarkCurves():
    benchmarkCurves = []    
    for curve in acm.FYieldCurve.Select(''):
        if curve.Type() == 'Benchmark':
            benchmarkCurves.append(curve)
    return benchmarkCurves
    

def getFXDeltaShiftRate(riskFactors):
    if len(list(riskFactors)) == 1: #check contains 1 element
        if acm.FCurrencyPair[str(riskFactors[0])]:    
            ccy1 =  str(riskFactors[0])[0:3]
            ccy2 =  str(riskFactors[0])[4:7]
            spotRate = instrument_used_price(ccy1, today, "ZAR")
            shiftedSpotRate = instrument_used_price(ccy1, today, "ZAR") + 0.01
            return (shiftedSpotRate/spotRate) -1 
        else:
            return 0.01
    else:
        return 0.01
    
    

