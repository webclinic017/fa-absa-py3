""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/swift/etc/FSwiftMT202.py"
"""----------------------------------------------------------------------------
MODULE
    FSwiftMT202 - Module that implements the MT 202 message functionality

    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

----------------------------------------------------------------------------"""

import FSwiftMTSettlement

from FSwiftMTBase import GetOptionValue, GetPartyBic, GetPartyFullName, GetPartyAddress
from FSwiftMTSettlement import GetApplicableOption

def Init(settlement):
    assert settlement.CounterpartyAccountRef(), "The settlement has no counterparty account reference"
    assert settlement.AcquirerAccountRef(), "The settlement has no acquirer account reference"

def GetYourReference(settlement):
    return FSwiftMTSettlement.GetYourRef(settlement)

def GetSubNetwork(settlement):
    return FSwiftMTSettlement.GetSubNetwork(settlement)

def GetSwiftServiceCode(settlement):
    return FSwiftMTSettlement.GetSwiftServiceCode(settlement)

def GetIntermediaryOption(settlement):
    option = GetOptionValue('INTERMEDIARY', settlement)
    return GetApplicableOption(option, GetIntermediaryAccount(settlement), GetIntermediaryBic(settlement))

def GetIntermediaryBic(settlement):
    import FSwiftParameters as Global

    cpAccount = settlement.CounterpartyAccountRef()
    intermediaryBic = ''
    if Global.SWIFT_LOOPBACK:
        intermediaryBic = Global.RECEIVER_BIC_LOOPBACK
    else:
        if cpAccount.Bic2():
            intermediaryBic = cpAccount.Bic2().Alias()
    return intermediaryBic

def GetIntermediaryAccount(settlement):
    return settlement.CounterpartyAccountRef().Account3()

def GetIntermediaryName(settlement):
    corrBank = settlement.CounterpartyAccountRef().CorrespondentBank2()
    intermediaryName = ''
    if corrBank:
        intermediaryName = GetPartyFullName(corrBank)
    return intermediaryName

def GetIntermediaryAddress(settlement):
    corrBank = settlement.CounterpartyAccountRef().CorrespondentBank2()
    intermediaryAddress = ''
    if corrBank:
        intermediaryAddress = GetPartyAddress(corrBank)
    return intermediaryAddress

def GetOrderingInstitutionOption(settlement):
    option = GetOptionValue('ORDERING_INSTITUTION', settlement)
    return GetApplicableOption(option, GetOrderingInstitutionAccount(settlement), GetOrderingInstitutionBic(settlement))

def GetOrderingInstitutionBic(settlement):
    return GetPartyBic(settlement.AcquirerAccountRef())

def GetOrderingInstitutionAccount(settlement):
    return settlement.AcquirerAccount()

def GetOrderingInstitutionName(settlement):
    return GetPartyFullName(settlement.Acquirer())

def GetOrderingInstitutionAddress(settlement):
    return GetPartyAddress(settlement.Acquirer())

def GetSendersCorrespondentOption(settlement):
    option = GetOptionValue('SENDERS_CORRESPONDENT', settlement)
    return GetApplicableOption(option, GetSendersCorrespondentAccount(settlement), GetSendersCorrespondentBic(settlement))

def GetSendersCorrespondentBic(settlement):
    acqAccount = settlement.AcquirerAccountRef()
    sendersCorrespondentBic = None
    if acqAccount.Bic():
        sendersCorrespondentBic = acqAccount.Bic().Alias()
    return sendersCorrespondentBic

def GetSendersCorrespondentAccount(settlement):
    return settlement.AcquirerAccountRef().Account()

def GetSendersCorrespondentName(settlement):
    corrBank = settlement.AcquirerAccountRef().CorrespondentBank()
    sendersCorrespondentName = ''
    if corrBank:
        sendersCorrespondentName = GetPartyFullName(corrBank)
    return sendersCorrespondentName

def GetSendersCorrespondentAddress(settlement):
    corrBank = settlement.AcquirerAccountRef().CorrespondentBank()
    sendersCorrespondentAddress = ''
    if corrBank:
        sendersCorrespondentAddress = GetPartyAddress(corrBank)
    return sendersCorrespondentAddress

def GetAccountWithInstitutionOption(settlement):
    option = GetOptionValue('ACCOUNT_WITH_INSTITUTION', settlement)
    return GetApplicableOption(option, GetAccountWithInstitutionAccount(settlement), GetAccountWithInstitutionBic(settlement))

def GetAccountWithInstitutionBic(settlement):
    import FSwiftParameters as Global

    cpAccount = settlement.CounterpartyAccountRef()
    accountWithInstitutionBic = ''
    if Global.SWIFT_LOOPBACK:
        accountWithInstitutionBic = Global.RECEIVER_BIC_LOOPBACK
    elif cpAccount.Bic():
        accountWithInstitutionBic = cpAccount.Bic().Alias()
    return accountWithInstitutionBic

def GetAccountWithInstitutionAccount(settlement):
    cpAccount = settlement.CounterpartyAccountRef()
    return cpAccount.Account2()

def GetAccountWithInstitutionName(settlement):
    corrBank = settlement.CounterpartyAccountRef().CorrespondentBank()
    accountWithInstitutionName = ''
    if corrBank:
        accountWithInstitutionName = GetPartyFullName(corrBank)
    return accountWithInstitutionName

def GetAccountWithInstitutionAddress(settlement):
    corrBank = settlement.CounterpartyAccountRef().CorrespondentBank()
    accountWithInstitutionAddress = ''
    if corrBank:
        accountWithInstitutionAddress = GetPartyAddress(corrBank)
    return accountWithInstitutionAddress

def GetBankingPriority(settlement):
    return FSwiftMTSettlement.GetBankingPriority(settlement)

def GetBeneficiaryInstitutionOption(settlement):
    return GetOptionValue('BENEFICIARY_INSTITUTION', settlement)

def GetBeneficiaryInstitutionBic(settlement):
    return GetPartyBic(settlement.CounterpartyAccountRef())

def GetBeneficiaryInstitutionAccount(settlement):
    return settlement.CounterpartyAccountRef().Account()

def GetBeneficiaryInstitutionName(settlement):
    return GetPartyFullName(settlement.Counterparty())

def GetBeneficiaryInstitutionAddress(settlement):
    return GetPartyAddress(settlement.Counterparty())

def GetInterbankSettledAmount(settlement):
    return FSwiftMTSettlement.GetInterbankSettledAmount(settlement)

def GetNationalClearingSystem(settlement):
    return FSwiftMTSettlement.GetNationalClearingSystem(settlement)

def GetNationalClearingCode(settlement):
    return FSwiftMTSettlement.GetNationalClearingCode(settlement)
