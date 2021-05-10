""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FTradeStatusOnlyLegally.py"
"""------------------------------------------------------------------------------------------------
MODULE
    FTradeStatusOnlyLegally

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Trade Status Inclusion Mask Only Legally Confirmed trades helper 
    Only Legally Confirmed Trades Replace Shift Parameters Dialog 

------------------------------------------------------------------------------------------------"""
import acm

LEGALLY_STATUSES = ('Legally Confirmed')

def TradeStatusOnlyLegally():
    enum = acm.FEnumeration['enum(TradeStatus)']
    mask = 0
    for status in enum.Values():
        mask += (1 << enum.Enumeration(status)) if status in LEGALLY_STATUSES else 0
    return mask
    
def ael_custom_dialog_show( shell, params ):
    return acm.FDictionary()
    
def ael_custom_dialog_main( parameters, dictExtra ):
    shiftVector = acm.CreateReplaceShiftVector('trade status inclusion mask', None)
    shiftVector.AddReplaceShiftItem(TradeStatusOnlyLegally(), 'Only Legally Confirmed')
    return shiftVector