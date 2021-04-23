""" Compiled: 2017-11-06 12:31:15 """

#__src_file__ = "extensions/ConvertiblePricingAndRisk/etc/FExerciseEventFunctions.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FExerciseEventFunctions -

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import acm

def IsValidPutEvent(ee, valuationDate, expiryDate):
    if ee.Date() < valuationDate or ee.Date() > expiryDate:
        return False
    return _IsPut(ee)
    
def IsValidCallEvent(ee, valuationDate, expiryDate):
    if ee.Date() < valuationDate or ee.Date() > expiryDate:
        return False
    return _IsCall(ee)

def IsValidMandatoryConversionEvent(ee, valuationDate, expiryDate):
    if ee.Date() < valuationDate or ee.Date() > expiryDate:
        return False
    return _IsMandatoryConversion(ee)

def ValidPutEventsSorted(exerciseEvents, valuationDate, expiryDate):
    validPutEvents = acm.FArray()
    for ee in exerciseEvents:
        if IsValidPutEvent(ee, valuationDate, expiryDate):
            validPutEvents.Add(ee)
    return validPutEvents.SortByProperty('Date', True)

def ValidCallEventsSorted(exerciseEvents, valuationDate, expiryDate):
    validCallEvents = acm.FArray()
    for ee in exerciseEvents:
        if IsValidCallEvent(ee, valuationDate, expiryDate):
            validCallEvents.Add(ee)
    return validCallEvents.SortByProperty('Date', True)
    
def ValidMandatoryConversionEventsSorted(exerciseEvents, valuationDate, expiryDate):
    validEvents = acm.FArray()
    for ee in exerciseEvents:
        if IsValidMandatoryConversionEvent(ee, valuationDate, expiryDate):
            validEvents.Add(ee)
    return validEvents.SortByProperty('Date', True)

def _IsPut(ee):
    return ee.Type() == 'Put' or ee.Type() == 'PutPeriod'

def _IsCall(ee):
    return ee.Type() == 'Call' or ee.Type() == 'CallPeriod'
    
def _IsMandatoryConversion(ee):
    return ee.Type() == 'MandatoryConversion' or ee.Type() == 'MandatoryConversionPeriod'

def PutDate(exerciseEvent, valuationDate):
    if _IsPut(exerciseEvent):
        if exerciseEvent.IsPeriod():
            return min(max(exerciseEvent.StartDate(), valuationDate), exerciseEvent.ExpiryDate())
        else:
            return exerciseEvent.ExpiryDate()
    else:
        return None
        
def CallDate(exerciseEvent, valuationDate):
    if _IsCall(exerciseEvent):
        if exerciseEvent.IsPeriod():
            return min(max(exerciseEvent.StartDate(), valuationDate), exerciseEvent.ExpiryDate())
        else:
            return exerciseEvent.ExpiryDate()
    else:
        return None

def MaxOfPricingToPutResults(callDicts):
    # pylint: disable-msg=E1101
    returnDict = {}
    for callDict in callDicts:
        if returnDict == {}:
            returnDict = callDict
            continue
        if callDict.At('result')>returnDict.At('result'):
            returnDict = callDict
    return returnDict
