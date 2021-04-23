""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/AMUtils/./etc/FAMValuationUtils.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FAMValuationUtils

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
import acm

def FXRateIsValid(curr1, curr2):
    try:
        label = FXRateLabel(curr1, curr2)
        return bool(acm.FCurrencyPair.Select01('name=%s' % label, None))
    except AttributeError:
        return False

def FXRateLabel(curr1, curr2):
    try:
        return '/'.join((curr1, curr2))
    except StandardError:
        return ''

def FXRateLabelFromInstrument(ins):
    try:
        curr1 = ins.Currency().Name()
        curr2 = ins.Underlying().Currency().Name()
        return FXRateLabel(curr1, curr2)
    except StandardError:
        return ''

def FXRateFormattedLabel(curr1, curr2):
    if FXRateIsValid(curr1, curr2):
        return FXRateLabel(curr1, curr2)
    else:
        return FXRateLabel(curr2, curr1)

def FXRateFormattedLabelFromInstrument(ins):
    try:
        curr1 = ins.Currency().Name()
        curr2 = ins.Underlying().Currency().Name()
        return FXRateFormattedLabel(curr1, curr2)
    except StandardError:
        return ''

def FXRateValue(curr1, curr2, fxRate):
    if FXRateIsValid(curr1, curr2):
        try:
            return 1/fxRate
        except StandardError:
            return 0.0
    return fxRate

def FXRateValueFromInstrument(ins, fxRate):
    try:
        curr1 = ins.Currency().Name()
        curr2 = ins.Underlying().Currency().Name()
        return FXRateValue(curr1, curr2, fxRate)
    except StandardError:
        return 0.0

def GetFormattedSalesActivityFXRate(salesActivity):
    return FXRateValueFromInstrument(
            salesActivity.Instrument(),
            salesActivity.FXRate()
            )

def SetFormattedSalesActivityFXRate(salesActivity, fxRateValue):
    formattedFxRateValue = FXRateValueFromInstrument(salesActivity.Instrument(), fxRateValue)
    salesActivity.FXRate(formattedFxRateValue)