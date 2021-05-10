""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/swift/etc/FSwiftMT542.py"
"""----------------------------------------------------------------------------
MODULE
    FSwiftMT542 - Module that implements the MT 542 message functionality

    (c) Copyright 201 SunGard FRONT ARENA. All rights reserved.

----------------------------------------------------------------------------"""

import acm

from FSwiftMTBase import GetOptionValue
from FSwiftMTSecuritiesSettlement import GetApplicablePartyDetails, SetInitiatingPartyDetails, \
SetPSETDetails, SetAgentDetails, SetCustodianDetails, SetIntermediate1Details, SetIntermediate2Details

def Init(settlement):
    assert settlement.CounterpartyAccountRef(), "The settlement has no counterparty account reference"

def GetPartyDetails(settlement):
    partyDetails = acm.FList()
    SetPartyDetails(settlement, partyDetails)
    return partyDetails

def SetPartyDetails(settlement, partyDetails):
    details = list()
    option = GetOptionValue('PARTY', settlement)
    counterPartyAccount = settlement.CounterpartyAccountRef()

    SetInitiatingPartyDetails('BUYR', counterPartyAccount, details)
    SetCustodianDetails('RECU', counterPartyAccount, details)
    SetIntermediate1Details('REI1', counterPartyAccount, details)
    SetIntermediate2Details('REI2', counterPartyAccount, details)
    SetAgentDetails('REAG', counterPartyAccount, details)
    SetPSETDetails('PSET', counterPartyAccount, details)

    applicablePartyDetails = GetApplicablePartyDetails(option, details)
    AddElementsToPartyDetails(applicablePartyDetails, partyDetails)

def AddElementsToPartyDetails(elementList, partyDetails):
    for element in elementList:
        partyDetails.Add(element)

def GetAccountNumber(settlement):
    return settlement.AcquirerAccount()