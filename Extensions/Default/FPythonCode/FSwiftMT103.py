""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/swift/etc/FSwiftMT103.py"
"""----------------------------------------------------------------------------
MODULE
    FSwiftMT103 - Module that implements the MT 103 message functionality

    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

----------------------------------------------------------------------------"""

import FSwiftUtils
import FSwiftMTSettlement

from FSwiftMTBase import GetOptionValue, GetPartyBic, GetPartyFullName, GetPartyAddress, GetPartyStreetAndNumber
from FSwiftMTSettlement import GetApplicableOption


def Init(settlement):
    assert settlement.CounterpartyAccountRef(), "The settlement has no counterparty account reference"
    assert settlement.AcquirerAccountRef(), "The settlement has no acquirer account reference"
    assert settlement.Counterparty(), "The settlement has no counterparty"
    assert settlement.Acquirer(), "The settlement has no acquirer"

def GetOrderingCustomerOption(settlement):
    return GetOptionValue('ORDERING_CUSTOMER', settlement)

def GetSubNetwork(settlement):
    return FSwiftMTSettlement.GetSubNetwork(settlement)

def GetSwiftServiceCode(settlement):
    return FSwiftMTSettlement.GetSwiftServiceCode(settlement)

def GetOrderingCustomerBic(settlement):
    return GetPartyBic(settlement.AcquirerAccountRef())

def GetOrderingCustomerAccount(settlement):
    return settlement.AcquirerAccount()

def GetOrderingCustomerName(settlement):
    return GetPartyFullName(settlement.Acquirer())

def GetOrderingCustomerAddress(settlement):
    address = ''
    if GetOrderingCustomerOption(settlement) in ['A', 'K']:
        address = GetPartyAddress(settlement.Acquirer())
    elif GetOrderingCustomerOption(settlement) in ['F']:
        address = GetPartyStreetAndNumber(settlement.Acquirer())
    return address

def GetIntermediaryInstitutionOption(settlement):
    option = GetOptionValue('INTERMEDIARY_INSTITUTION', settlement)
    return GetApplicableOption(option, GetIntermediaryInstitutionAccount(settlement), GetIntermediaryInstitutionBic(settlement))

def GetIntermediaryInstitutionBic(settlement):
    import FSwiftParameters as Global

    bic = ''
    cpAccount = settlement.CounterpartyAccountRef()
    if Global.SWIFT_LOOPBACK:
        bic = Global.RECEIVER_BIC_LOOPBACK
    elif cpAccount.Bic2():
        bic = cpAccount.Bic2().Alias()
    return bic

def GetIntermediaryInstitutionAccount(settlement):
    return settlement.CounterpartyAccountRef().Account3()

def GetIntermediaryInstitutionName(settlement):
    name = ''
    corrBank = settlement.CounterpartyAccountRef().CorrespondentBank2()
    if corrBank:
        name = GetPartyFullName(corrBank)
    return name

def GetIntermediaryInstitutionAddress(settlement):
    address = ''
    corrBank = settlement.CounterpartyAccountRef().CorrespondentBank2()
    if corrBank:
        address = GetPartyAddress(corrBank)
    return address

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

def GetOrderingCustomerCountryCode(settlement):
    return settlement.Acquirer().JurisdictionCountryCode()

def GetOrderingCustomerTown(settlement):
    return settlement.Acquirer().City()

def GetOrderingCustomerZipCode(settlement):
    return settlement.Acquirer().ZipCode()

def GetBeneficiaryCustomerOption(settlement):
    option = GetOptionValue('BENEFICIARY_CUSTOMER', settlement)
    optionValue = GetApplicableOption(option, None, GetBeneficiaryCustomerBic(settlement))
    if optionValue == '':
        optionValue = 'NO OPTION'
    return optionValue

def GetBeneficiaryCustomerBic(settlement):
    return GetPartyBic(settlement.CounterpartyAccountRef())

def GetBeneficiaryCustomerAccount(settlement):
    return settlement.CounterpartyAccountRef().Account()

def GetBeneficiaryCustomerName(settlement):
    return GetPartyFullName(settlement.Counterparty())

def GetBeneficiaryCustomerAddress(settlement):
    if GetBeneficiaryCustomerOption(settlement) in ['NO OPTION', 'A']:
        return GetPartyAddress(settlement.Counterparty())
    else:
        return GetPartyStreetAndNumber(settlement.Counterparty())

def GetBeneficiaryCustomerCountryCode(settlement):
    return settlement.Counterparty().JurisdictionCountryCode()

def GetBeneficiaryCustomerTown(settlement):
    return settlement.Counterparty().City()

def GetBeneficiaryCustomerZipCode(settlement):
    return settlement.Counterparty().ZipCode()

def GetAccountWithInstitutionOption(settlement):
    option = GetOptionValue('ACCOUNT_WITH_INSTITUTION', settlement)
    return GetApplicableOption(option, GetAccountWithInstitutionAccount(settlement), GetAccountWithInstitutionBic(settlement))

def GetAccountWithInstitutionBic(settlement):
    import FSwiftParameters as Global

    bic = ''
    cpAccount = settlement.CounterpartyAccountRef()
    if Global.SWIFT_LOOPBACK:
        bic = Global.RECEIVER_BIC_LOOPBACK
    elif cpAccount.Bic():
        bic = cpAccount.Bic().Alias()
    return bic

def GetAccountWithInstitutionAccount(settlement):
    return settlement.CounterpartyAccountRef().Account2()

def GetAccountWithInstitutionName(settlement):
    name = ''
    corrBank = settlement.CounterpartyAccountRef().CorrespondentBank()
    if corrBank:
        name = GetPartyFullName(corrBank)
    return name

def GetAccountWithInstitutionAddress(settlement):
    address = ''
    corrBank = settlement.CounterpartyAccountRef().CorrespondentBank()
    if corrBank:
        address = GetPartyAddress(corrBank)
    return address

def GetSendersCorrespondentOption(settlement):
    option = GetOptionValue('SENDERS_CORRESPONDENT', settlement)
    return GetApplicableOption(option, GetSendersCorrespondentAccount(settlement), GetSendersCorrespondentBic(settlement))

def GetSendersCorrespondentBic(settlement):
    acqAccount = settlement.AcquirerAccountRef()
    bic = None
    if acqAccount.Bic():
        bic = acqAccount.Bic().Alias()
    return bic

def GetSendersCorrespondentAccount(settlement):
    return settlement.AcquirerAccountRef().Account()

def GetSendersCorrespondentName(settlement):
    name = ''
    corrBank = settlement.AcquirerAccountRef().CorrespondentBank()
    if corrBank:
        name = GetPartyFullName(corrBank)
    return name

def GetSendersCorrespondentAddress(settlement):
    address = ''
    corrBank = settlement.AcquirerAccountRef().CorrespondentBank()
    if corrBank:
        address = GetPartyAddress(corrBank)
    return address

def GetBankOperationCode():
    ''' Mandatory field 23B '''

    return 'CRED'

def GetBankingPriority(settlement):
    return FSwiftMTSettlement.GetBankingPriority(settlement)

def GetInterbankSettledAmount(settlement):
    return FSwiftMTSettlement.GetInterbankSettledAmount(settlement)

def GetInstructionCode():
    ''' Mandatory field 23E '''

    return 'PHOB'

def GetInstructedAmount(settlement):
    ''' Optional field 33B '''

    return GetInterbankSettledAmount(settlement)

def GetRemittanceInfo(settlement):
    ''' Optional field 70 '''

    import FSwiftParameters as Global

    trade = settlement.Trade()
    instrument = settlement.Instrument()
    YOUR_REF = 'Your reference:'
    OUR_REF = 'Our reference:'
    code = '/INV/'
    newline = Global.SEPARATOR
    info = []
    info.append(code)
    info.append(newline)
    if instrument:
        info.append('Instrument:')
        info.append(instrument.Name())
    info.append(newline)
    info.append(OUR_REF)
    if trade:
        info.append(str(trade.Oid()))
    info.append(newline)
    info.append(YOUR_REF)
    info.append(FSwiftMTSettlement.GetYourRef(settlement))

    info = ''.join(info)
    info = FSwiftUtils.SwiftNarrativeTextFormatter.Format(info)
    return info

def GetDetailsOfCharges(settlement):
    ''' Mandatory field 71A '''

    account = settlement.CounterpartyAccountRef()
    details = account.DetailsOfCharges()
    if details and details != 'None':
        return details
    return 'SHA'

def GetNationalClearingSystem(settlement):
    return FSwiftMTSettlement.GetNationalClearingSystem(settlement)

def GetNationalClearingCode(settlement):
    return FSwiftMTSettlement.GetNationalClearingCode(settlement)


