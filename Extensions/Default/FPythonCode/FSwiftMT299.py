""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/swift/etc/FSwiftMT299.py"
"""----------------------------------------------------------------------------
MODULE
    FSwiftMT299 - Module that implements the MT 299 message functionality

    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

----------------------------------------------------------------------------"""

import FSwiftMTSettlement

def GetSwiftRelationType():
    '''New field used in adaptiv rules when creating MTn99 '''
    
    return '299'

def GetNarrative(settlement):
    return FSwiftMTSettlement.GetNarrative(settlement)

def GetSwiftServiceCode(settlement):
    return FSwiftMTSettlement.GetSwiftServiceCode(settlement)


