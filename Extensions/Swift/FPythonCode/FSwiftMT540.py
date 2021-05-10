""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/swift/etc/FSwiftMT540.py"
"""----------------------------------------------------------------------------
MODULE
    FSwiftMT540 - Module that implements the MT 540 message functionality

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

    SetInitiatingPartyDetails('SELL', counterPartyAccount, details)
    SetCustodianDetails('DECU', counterPartyAccount, details)
    SetIntermediate1Details('DEI1', counterPartyAccount, details)
    SetIntermediate2Details('DEI2', counterPartyAccount, details)
    SetAgentDetails('DEAG', counterPartyAccount, details)
    SetPSETDetails('PSET', counterPartyAccount, details)

    applicablePartyDetails = GetApplicablePartyDetails(option, details)
    AddElementsToPartyDetails(applicablePartyDetails, partyDetails)

def AddElementsToPartyDetails(elementList, partyDetails):
    for element in elementList:
        partyDetails.Add(element)

def GetAccountNumber(settlement):
    return settlement.AcquirerAccount()
