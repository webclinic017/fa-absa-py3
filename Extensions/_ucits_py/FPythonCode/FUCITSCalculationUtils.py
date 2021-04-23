""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/UCITS/etc/FUCITSCalculationUtils.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FUCITSCalculationUtils

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
import acm
from collections import defaultdict
from FUCITSHooks import GeneralExposureMethods
from FUCITSInstrumentMethods import UCITSValuationIssuer

TOP = 'top'
TOP_NAV = 'topNAV'
AGGREGATED_NAV = 'aggregatedNav'
AMOUNT_OF_INSTRUMENTS = 'amountOfInstruments'
INSTRUMENT_NAVS = 'instrumentNavs'
SHOW = 'show'
FILTERED = 'filtered'
UNFILTERED = 'unfiltered'
THRESHOLD = 'threshold'
SEGREGATED_EXPOSURE = 'segregatedExposure'

def IncludeInCalc(nav, issuerFilter):
    inst = nav.First()
    if inst.UCITSInstrumentIsTSMM() == 'TSMM':
        issuer = UCITSValuationIssuer(inst)
        if issuer:
            return str(issuer.UCITSIssuerStatus()) == str(issuerFilter)
    return False

def ThresholdedSumOfIssuerNavs(instrumentNavs, accountingCurrencyZero, portfolioNav, threshold, issuerFilter):
    denomZero = lambda: accountingCurrencyZero
    d = defaultdict(denomZero)
    for nav in instrumentNavs:
        if IncludeInCalc(nav, issuerFilter):
            ultimateIssuer = UCITSValuationIssuer(nav.First()).UCITSUltimateIssuer()
            d[ultimateIssuer] += nav.Second()
    try:
        sumOfAllOver5Pct = sum([abs(d[k].Number()) for k in d if abs(d[k].Number())/abs(portfolioNav.Number()) >= threshold])
        return acm.DenominatedValue(sumOfAllOver5Pct, accountingCurrencyZero.Unit(), None)
    except Exception:
        return accountingCurrencyZero

def AggregatedNavFromSubResults(subResults):
    return ValueFromSubResultDict(AGGREGATED_NAV, subResults)

def IsTopValue(subResults):
    if len(subResults) == 0:
        return None
    values = [bool(result.At(TOP)) for result in subResults]
    if not False in values:
        return True
    elif not True in values:
        return False
    else:
        raise ValueError('Mix of Top/Non-Top Values')

def ShowFilteredNAVForFilteredRow(subResults):
    return all([str(result.At(SHOW)) in [FILTERED,] for result in subResults])

def ShowNAVForFilteredRow(subResults):
    return all([str(result.At(SHOW)) in [FILTERED, UNFILTERED] for result in subResults])

def MaxNavFromSubResults(subResults):
    return ValueFromSubResultDict(TOP_NAV, subResults)

def AmountOfInstrumentsFromSubResults(subResults):
    return ValueFromSubResultDict(AMOUNT_OF_INSTRUMENTS, subResults)

def InstrumentNavsFromSubResults(subResults):
    return ValueFromSubResultDict(INSTRUMENT_NAVS, subResults)
    
def SegregatedExposuresFromSubResults(subResults):
    return ValueFromSubResultDict(SEGREGATED_EXPOSURE, subResults)

def ValueFromSubResultDict(key, subResults):
    return [r.At(key) for r in subResults]

def ThresholdFromInput(subResults):
    thresholds = list(set(ValueFromSubResultDict(THRESHOLD, subResults)))
    if len(thresholds) == 1:
        return thresholds[0]
    else:
        raise ValueError('Could not find unique threshold')

def IsIncludeAllGrouping(grouping):
    return str(grouping.GroupingValue()) == "All Trades"

def GetExposureType(ins):
    funcList = [getattr(GeneralExposureMethods, f) for f in dir(GeneralExposureMethods) if f.startswith('If')]
    returnString = None
    for f in funcList:
        returnString = f(ins)
        if returnString:
            return returnString
    return 'currencyZero'