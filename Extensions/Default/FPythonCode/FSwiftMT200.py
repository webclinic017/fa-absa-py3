""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/swift/etc/FSwiftMT200.py"
"""----------------------------------------------------------------------------
MODULE
    FSwiftMT200 - Module that implements the MT 200 message functionality

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

----------------------------------------------------------------------------"""

import FSwiftMTSettlement
import FSwiftMTBase

def __GetIntermediaryAccount(settlement):
    account = settlement.CounterpartyAccountRef()
    if account:
        return account.Account3()
    return ''

def __GetAccountWithInstitutionAccount(settlement):
    account = settlement.CounterpartyAccountRef()
    if account:
        return account.Account2()
    return ''

def __GetIntermediaryBic(settlement):
    import FSwiftParameters as swiftParameters

    if swiftParameters.SWIFT_LOOPBACK:
        return swiftParameters.SENDER_BIC_LOOPBACK
    account = settlement.CounterpartyAccountRef()
    assert settlement.CounterpartyAccountRef(), "The settlement has no counterparty account reference"
    if account.Bic2():
        return account.Bic2().Alias()
    return ''

def __GetAccountWithInstitutionBic(settlement):
    import FSwiftParameters as swiftParameters

    if swiftParameters.SWIFT_LOOPBACK:
        return swiftParameters.SENDER_BIC_LOOPBACK
    account = settlement.CounterpartyAccountRef()
    assert settlement.CounterpartyAccountRef(), "The settlement has no counterparty account reference"
    if account.Bic():
        return account.Bic().Alias()
    return ''

def __GetCounterpartyCorrespondentBank2(settlement):
    account = settlement.CounterpartyAccountRef()
    if account:
        return account.CorrespondentBank2()
    return None

def __GetCounterpartyCorrespondentBank(settlement):
    account = settlement.CounterpartyAccountRef()
    if account:
        return account.CorrespondentBank()
    return None

def __GetIntermediaryName(settlement):
    counterpartyCorrespondentBank2 = __GetCounterpartyCorrespondentBank2(settlement)
    if counterpartyCorrespondentBank2:
        return FSwiftMTBase.GetPartyFullName(counterpartyCorrespondentBank2)
    return ''

def __GetIntermediaryAddress(settlement):
    counterpartyCorrespondentBank2 = __GetCounterpartyCorrespondentBank2(settlement)
    if counterpartyCorrespondentBank2:
        return FSwiftMTBase.GetPartyAddress(counterpartyCorrespondentBank2)
    return ''

def __GetAccountWithInstitutionName(settlement):
    counterpartyCorrespondentBank = __GetCounterpartyCorrespondentBank(settlement)
    if counterpartyCorrespondentBank:
        return FSwiftMTBase.GetPartyFullName(counterpartyCorrespondentBank)
    return ''

def __GetAccountWithInstitutionAddress(settlement):
    counterpartyCorrespondentBank = __GetCounterpartyCorrespondentBank(settlement)
    if counterpartyCorrespondentBank:
        return FSwiftMTBase.GetPartyAddress(counterpartyCorrespondentBank)
    return ''

#----- Field 20 -----

def GetSeqNbr(settlement):
    return settlement.Oid()

#----- Field 32A-----

def GetSettlementCurrency(settlement):
    return FSwiftMTSettlement.GetSettlementCurrency(settlement)

def GetInterbankSettledAmount(settlement):
    return FSwiftMTSettlement.GetInterbankSettledAmount(settlement)

#----- Field 53B -----

def GetSendersCorrespondentAccount(settlement):
    account = settlement.AcquirerAccountRef()
    if account:
        return account.Account()
    return ''

#----- Field 56A -----

def GetIntermediaryOption(settlement):
    return FSwiftMTSettlement.GetApplicableOption(FSwiftMTBase.GetOptionValue('INTERMEDIARY', settlement),
                                                  __GetIntermediaryAccount(settlement),
                                                  __GetIntermediaryBic(settlement))

def GetIntermediaryAccount(settlement):
    return __GetIntermediaryAccount(settlement)

def GetIntermediaryBic(settlement):
    return __GetIntermediaryBic(settlement)

def GetIntermediaryName(settlement):
    return __GetIntermediaryName(settlement)

def GetIntermediaryAddress(settlement):
    return __GetIntermediaryAddress(settlement)

#----- Field 57A -----

def GetAccountWithInstitutionOption(settlement):
    return FSwiftMTSettlement.GetApplicableOption(FSwiftMTBase.GetOptionValue('ACCOUNT_WITH_INSTITUTION', settlement),
                                                  __GetAccountWithInstitutionAccount(settlement),
                                                  __GetAccountWithInstitutionBic(settlement))

def GetAccountWithInstitutionAccount(settlement):
    return __GetAccountWithInstitutionAccount(settlement)

def GetAccountWithInstitutionBic(settlement):
    return __GetAccountWithInstitutionBic(settlement)

def GetAccountWithInstitutionName(settlement):
    return __GetAccountWithInstitutionName(settlement)

def GetAccountWithInstitutionAddress(settlement):
    return __GetAccountWithInstitutionAddress(settlement)

def GetNationalClearingSystem(settlement):
    return FSwiftMTSettlement.GetNationalClearingSystem(settlement)

def GetNationalClearingCode(settlement):
    return FSwiftMTSettlement.GetNationalClearingCode(settlement)