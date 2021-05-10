""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/swift/etc/FSwiftMT543.py"
"""----------------------------------------------------------------------------
MODULE
    FSwiftMT543 - Module that implements the MT 543 message functionality

    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

----------------------------------------------------------------------------"""

import FSwiftMT542
import FSwiftMTSecuritiesSettlement as MTSecurities

def Init(settlement):
    FSwiftMT542.Init(settlement)

def GetAccountNumber(settlement):
    return FSwiftMT542.GetAccountNumber(settlement)

def GetPartyDetails(settlement):
    return FSwiftMT542.GetPartyDetails(settlement)

def GetAmountQualifier():
    return MTSecurities.GetAmountQualifier()

def GetAmountSign(settlement):
    if MTSecurities.CalculateCashAmount(settlement) >= 0:
        return ''
    else:
        return 'N'

def GetCurrencyCode(settlement):
	return MTSecurities.GetCurrencyCode(settlement)

def GetAmount(settlement):
	return MTSecurities.GetAmount(settlement)

