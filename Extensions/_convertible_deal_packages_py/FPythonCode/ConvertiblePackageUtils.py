""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/ConvertibleDealPackages/etc/ConvertiblePackageUtils.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    ConvertiblePackageUtils

    (c) Copyright 2016 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import acm
from FAssetManagementUtils import logger
from FAscotValuationFunctions import GetRecallSwap
import math

CB_MAT = 'Maturity'
CB_MAT_2BD = 'Maturity + 2BD'
CB_PUT = 'Next Put'
CB_PUT_2BD = 'Next Put + 2BD'
NEXT_PUT_DATE_CACHE = dict()

OPTION_CALL = 'Call'
OPTION_PUT = 'Put'

INSTYPE_CB = 'Convertible'
INSTYPE_ASCOT = 'ASCOT'

BUY_SELL_MAP = {'B':  1, (1): 'B', 
                'S': -1,(-1): 'S',
                '-':  0, (0): '-'}

def InsTypeFromGUI(GUIValue):
    if GUIValue == INSTYPE_CB:
        return 'Convertible'
    elif GUIValue == INSTYPE_ASCOT:
        return 'Option'

def InsTypeToGUI(insType):
    if insType == 'Convertible':
        return INSTYPE_CB
    elif insType == 'Option':
        return INSTYPE_ASCOT

def GetMarketPrice(instrument):
    def checkDenominatedValue(value):
        try:
            if not value:
                return False
            if value.Type() and value.Type().Text() == 'InvalidPrice':
                return False
            if not value.Number() >= 0.0 and not value.Number() < 0.0:
                return False
        except Exception:
            return False
        return True

    calcSpace = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()
    marketPrice = instrument.Calculation().MarketPrice(calcSpace)
    if checkDenominatedValue(marketPrice):
        return marketPrice.Value().Number()
    else:
        return 0.0

def GetUnderlyingStock(instrument):
    underlying = instrument.Underlying()
    if underlying:
        return GetUnderlyingStock(underlying)
    return instrument

def GetCBNextPutDate(instrument):
    if instrument.Putable():
        constraint = 'instrument="' + instrument.Name() + '" and type="Put"'
        ees = acm.FExerciseEvent.Select(constraint).SortByProperty('expiryDate')
        for ee in ees:
            today = acm.Time.DateToday()
            if today < ee.ExpiryDate():
                return ee.ExpiryDate()
    return acm.Time.SmallDate()

def GetCBMaturityDate2BD(convertible):
    calendar = convertible.Legs().First().PayCalendar()
    return AdjustBankingDays(calendar, convertible.EndDate(), 2)

def GetCBNextPutDate2BD(convertible):
    calendar = convertible.Legs().First().PayCalendar()
    nextPutDate = GetCBNextPutDate(convertible)
    return AdjustBankingDays(calendar, nextPutDate, 2)

def AdjustBankingDays(calendar, initialDate, numberOfDays):
    return calendar.AdjustBankingDays(initialDate, numberOfDays)

def GetTradeableAmount(originalQuantity, instrument):
    quantity = math.fabs(originalQuantity)
    minPiece = instrument.MinimumPiece()
    minIncremental = instrument.MinimumIncremental()
    if minPiece > 0.0 and quantity - minPiece < 0.0:
        quantity = minPiece
    elif minIncremental > 0.0:
        if minPiece > 0.000001:
            quantity = quantity - minPiece
        quantity = minPiece + round(quantity/minIncremental)*minIncremental
    return math.copysign(quantity, originalQuantity)

def AllCBChoices():
    # Retrieves all non-expired convertibles that are Monis valued
    today = acm.Time.DateToday()
    constraint = 'valuationGrpChlItem="Monis" and expiryDate>"' + today + '"'
    return acm.FConvertible.Select(constraint).SortByProperty('Name')

def CBChoicesExist():
    return AllCBChoices().Size() > 0

def StartDealPackage(dealPackage):
    ''' Starts a deal package application. Aborts if there are no Monis valued convertibles
        in the ADS.
    '''
    if not CBChoicesExist():
        logger.error('The application could not be opened: No Monis valued convertibles exist in the ADS.')
        return
    acm.UX().SessionManager().StartApplication('Deal Package', dealPackage)
    return

def InstrumentPackageGenerator(ins, defName):
    links = ins.DealPackageInstrumentLinks()
    for link in links:
        insPkg = link.InstrumentPackage()
        if insPkg.DefinitionName() == defName:
            yield insPkg
    
def InstrumentPackageIfUnique(inst, defName):
    insPkgGenerator = InstrumentPackageGenerator(inst, defName)
    try:
        insPkg = next(insPkgGenerator)
    except StopIteration:
        return None
    try:
        next(insPkgGenerator)
    except StopIteration:
        return insPkg
    else:
        return None
    
def MaturityType(ascot):
    cb = ascot.Underlying()
    irs = GetRecallSwap(ascot)
    if not irs:
        return ' '
    maturityDate = irs.Legs()[0].EndDate()
    if maturityDate == GetCBNextPutDate(cb):
        maturityType = CB_PUT
    elif maturityDate == GetCBNextPutDate2BD(cb):
        maturityType = CB_PUT_2BD
    elif maturityDate == cb.EndDate():
        maturityType = CB_MAT
    elif maturityDate == GetCBMaturityDate2BD(cb):
        maturityType = CB_MAT_2BD
    else:
        maturityType = ' '
    return maturityType

def GetRollingPeriodFromFloatRateReference(floatRateRef):
    periodCount = floatRateRef.Legs().First().EndPeriodCount()
    periodUnit = floatRateRef.Legs().First().EndPeriodUnit()
    rollingPeriod = str(periodCount) + str(periodUnit)
    return rollingPeriod

def _IsAscot(obj):
    return obj.Class() == acm.FOption and obj.Underlying().Class() == acm.FConvertible