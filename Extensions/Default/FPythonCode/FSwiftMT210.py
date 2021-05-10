""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/swift/etc/FSwiftMT210.py"
"""----------------------------------------------------------------------------
MODULE
    FSwiftMT210 - Module that implements the MT 210 message functionality

    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

----------------------------------------------------------------------------"""

import FSwiftMTBase
import FSwiftMTSettlement

from FOperationsEnums import PartyType

def Init():
    pass

def GetOrderingCustomerOption(settlement):
    orderingCustomerOption = FSwiftMTBase.GetOptionValue('ORDERING_CUSTOMER', settlement)
    if not orderingCustomerOption:
        orderingCustomerOption = 'NO OPTION'
    return orderingCustomerOption

def GetOrderingCustomerBic(settlement):
    counterpartyPartyAccount = settlement.CounterpartyAccountRef()
    orderingCustomerBic = None
    if counterpartyPartyAccount != None and settlement.Counterparty().Type() == PartyType.CLIENT:
        orderingCustomerBic = FSwiftMTBase.GetPartyBic(counterpartyPartyAccount)
    return orderingCustomerBic

def GetOrderingCustomerAccount(settlement):
    orderingCustomerAccount = None
    if settlement.Counterparty().Type() == PartyType.CLIENT:
        return settlement.CounterpartyAccount()
    return orderingCustomerAccount

def GetOrderingCustomerName(settlement):
    orderingCustomerName = None
    if settlement.Counterparty().Type() == PartyType.CLIENT:
        orderingCustomerName = FSwiftMTBase.GetPartyFullName(settlement.Counterparty())
    return orderingCustomerName

def GetOrderingCustomerAddress(settlement):
    orderingCustomerAddress = None
    if settlement.Counterparty().Type() == PartyType.CLIENT:
        orderingCustomerAddress = FSwiftMTBase.GetPartyAddress(settlement.Counterparty())
    return orderingCustomerAddress

def GetOrderingInstitutionOption(settlement):
    option = FSwiftMTBase.GetOptionValue('ORDERING_INSTITUTION', settlement)
    return FSwiftMTSettlement.GetApplicableOption(option, GetOrderingInstitutionAccount(settlement), GetOrderingInstitutionBic(settlement))

def GetOrderingInstitutionBic(settlement):
    counterpartyPartyAccount = settlement.CounterpartyAccountRef()
    orderingInstitutionBic = None
    if counterpartyPartyAccount and counterpartyPartyAccount.Bic() and settlement.Counterparty().Type() == PartyType.COUNTERPARTY:
        orderingInstitutionBic = counterpartyPartyAccount.Bic().Alias()
    return orderingInstitutionBic

def GetOrderingInstitutionAccount(settlement):
    counterpartyAccount = None
    if settlement.Counterparty().Type() == PartyType.COUNTERPARTY:
        counterpartyAccount = settlement.CounterpartyAccount()
    return counterpartyAccount

def GetOrderingInstitutionName(settlement):
    orderingInstitutionName = None
    if settlement.Counterparty().Type() == PartyType.COUNTERPARTY:
        orderingInstitutionName = FSwiftMTBase.GetPartyFullName(settlement.Counterparty())
    return orderingInstitutionName

def GetOrderingInstitutionAddress(settlement):
    orderingInstitutionAddress = None
    if settlement.Counterparty().Type() == PartyType.COUNTERPARTY:
        orderingInstitutionAddress = FSwiftMTBase.GetPartyAddress(settlement.Counterparty())
    return orderingInstitutionAddress

def GetIntermediaryOption(settlement):
    option = FSwiftMTBase.GetOptionValue('INTERMEDIARY', settlement)
    return FSwiftMTSettlement.GetApplicableOption(option, GetIntermediaryAccount(settlement), GetIntermediaryBic(settlement))

def GetIntermediaryBic(settlement):
    intermediaryBic = None
    cpAccount = settlement.CounterpartyAccountRef()
    if cpAccount and cpAccount.Bic2():
        intermediaryBic = cpAccount.Bic2().Alias()
    return intermediaryBic

def GetIntermediaryAccount(settlement):
    intermediaryAccount = None
    cpAccount = settlement.CounterpartyAccountRef()
    if cpAccount:
        intermediaryAccount = cpAccount.Account2()
    return intermediaryAccount

def GetIntermediaryName(settlement):
    corrBank = None
    intermediaryName = ''
    cpAccount = settlement.CounterpartyAccountRef()
    if cpAccount:
        corrBank = cpAccount.CorrespondentBank2()
    if corrBank:
        intermediaryName = FSwiftMTBase.GetPartyFullName(corrBank)
    return intermediaryName

def GetIntermediaryAddress(settlement):
    corrBank = None
    intermediaryAddress = ''
    cpAccount = settlement.CounterpartyAccountRef()
    if cpAccount:
        corrBank = cpAccount.CorrespondentBank2()
    if corrBank:
        intermediaryAddress = FSwiftMTBase.GetPartyAddress(corrBank)
    return intermediaryAddress

def GetAccountIdentification(settlement):
    ''' Optional field 25 '''

    return settlement.AcquirerAccount()

def GetRelatedReference():
    ''' Mandatory field 21 '''

    return 'NONREF'

def GetInterbankSettledAmount(settlement):
    return FSwiftMTSettlement.GetInterbankSettledAmount(settlement)

def GetNationalClearingSystem(settlement):
    return FSwiftMTSettlement.GetNationalClearingSystem(settlement)

def GetNationalClearingCode(settlement):
    return FSwiftMTSettlement.GetNationalClearingCode(settlement)
