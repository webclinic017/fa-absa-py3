""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/swift/etc/FSwiftMT305.py"
"""----------------------------------------------------------------------------
MODULE
    FSwiftMT305 - Implements confirmation message functionality

    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

----------------------------------------------------------------------------"""

import FOperationsUtils as Utils
import FSwiftUtils

try:
    import FSwiftParameters as Global
except ImportError:
    import FSwiftParametersTemplate as Global

from FSwiftMTBase import GetOptionValue, GetPartyFullName, GetPartyAddress, GetPartyBic
from FSwiftMTConfirmation import sharedVariables, GetPartyInfo
from FConfirmationEnums import EventType
from FOperationsEnums import SettleType

def Init(confirmation):
    assert confirmation.Trade(), "The confirmation has no trade reference"
    assert confirmation.Trade().Instrument(), "The trade referenced by the confirmation has no instrument"

def GetCode(confirmation):
    ''' Mandatory field 22 '''

    typeOfCode = {EventType.NEW_TRADE:'NEW', EventType.NEW_TRADE_AMENDMENT:'AMEND', \
                   EventType.NEW_TRADE_CANCELLATION:'CANCEL', EventType.NEW_TRADE_CLOSE:'CLOSEOUT'}
    confType = confirmation.EventType()
    return typeOfCode.get(confType, '')

def GetStrikePrice(confirmation):
    ''' Mandatory field 36 in SWIFT. '''

    strikePrice = confirmation.Trade().Instrument().StrikePrice()
    strikeCurr = confirmation.Trade().Instrument().StrikeCurrency()
    if strikeCurr:
        strikePrice = FSwiftUtils.ApplyCurrencyPrecision(strikeCurr.Name(), strikePrice)

    strikePrice = FSwiftUtils.SwiftNumericFormatter(strikePrice)
    return strikePrice

def GetCode1(confirmation):
    ''' This together with code2, code3 and underlying currency
        forms the optional field 23'''

    if confirmation.Trade().Quantity() >= 0:
        return 'BUY'
    else:
        return 'SELL'


def GetCode2(confirmation):
    ''' This together with code1, code3 and underlying currency
        forms the optional field 23. '''

    if confirmation.Trade().Instrument().IsCallOption():
        return 'CALL'
    else:
        return 'PUT'

def GetCode3(confirmation):
    ''' This together with code1, code2 and underlying currency
        forms the optional field 23.'''

    return confirmation.Trade().Instrument().ExerciseType()

def GetYourReference(confirmation):
    ''' Mandatory field 21.'''

    import FSwiftParameters as Global

    yourReference = ''

    confType = confirmation.EventType()
    if confType == EventType.NEW_TRADE:
        yourReference = 'NEW'
    elif confType in (EventType.NEW_TRADE_AMENDMENT, EventType.NEW_TRADE_CANCELLATION):
        confRef = confirmation.ConfirmationReference()
        if confRef and Global.FAC and Global.FAC.strip() != '':
            yourReference = Global.FAC + '-' + str(confRef.Oid())
    return yourReference

def GetUnderlyingCurrency(confirmation):
    ''' This together with code2, code3 and underlying currency
        forms the optional field 23. Also this together with
        underlying_amount forms the mandatory field 32B.'''

    underlyingCurrency = ''
    underlyingIns = confirmation.Trade().Instrument().Underlying()
    if underlyingIns:
        underlyingCurrency = underlyingIns.Name()
    return underlyingCurrency

def GetExerciseDate(confirmation):
    ''' Optional field 31C. '''

    return confirmation.Trade().AcquireDay()

def GetExpiryDetailsDate(confirmation):
    ''' This together with expiry_details_time and expiry_details_location
        forms the mandatory field 31G '''

    return confirmation.Trade().Instrument().ExpiryDateOnly()

def GetExpiryDetailsTime(confirmation):
    ''' This together with expiry_details_date and expiry_details_location
        forms the mandatory field 31G '''

    expiryTime = ''
    fixingSource = confirmation.Trade().Instrument().FixingSource()
    if fixingSource:
        expiryTime = fixingSource.ExternalCutOff()
        if not expiryTime:
            Utils.LogVerbose("Missing field: External Cut-off Time on Fixing source (%s)" % fixingSource.Name())
    else:
        Utils.LogVerbose("Missing Fixing source info")
    return str(expiryTime)

def GetExpiryDetailsLocation(confirmation):
    ''' This together with expiry_details_date and expiry_details_time
        forms the mandatory field 31G '''

    import FSwiftParameters as Global
    
    expiryLocation = ''
    fixingSource = confirmation.Trade().Instrument().FixingSource()
    if fixingSource and fixingSource.City():
        city = fixingSource.City().upper()
        if city in Global.city_dict:
            expiryLocation = Global.city_dict[city]
        if not expiryLocation:
            Utils.LogVerbose("Missing field: City on Fixing source (%s)" % fixingSource.Name())
    else:
        Utils.LogVerbose("Missing Fixing source info")
    return expiryLocation

def GetSettlementDate(confirmation):
    ''' Optional field 31E '''

    return GetExpiryDetailsDate(confirmation)

def GetSettlementType(confirmation):
    ''' Mandatory field 26F '''

    type_dict = {SettleType.PHYSICAL_DELIVERY:'PRINCIPAL', SettleType.CASH:'NETCASH'}

    settlType = confirmation.Trade().Instrument().SettlementType()

    return type_dict.get(settlType, '')

def GetUnderlyingAmount(confirmation):
    ''' This together with underlying_currency forms the mandatory field 32B '''

    assert confirmation.Trade().Currency(), "The trade referenced by the confirmation has no currency"
    amount = confirmation.Trade().Quantity()
    currency = confirmation.Trade().Currency().Name()
    return FSwiftUtils.ApplyCurrencyPrecision(currency, abs(amount))

def GetCounterCurrency(confirmation):
    ''' This together with counter_amount forms the mandatory field 33B '''

    strikeCurr = confirmation.Trade().Instrument().StrikeCurrency()
    if strikeCurr:
        return strikeCurr.Name()
    else:
        return ''

def GetCounterAmount(confirmation):
    ''' This together with counter_currency forms the mandatory field 33B '''

    contractSize = confirmation.Trade().Instrument().ContractSize()
    strikePrice = confirmation.Trade().Instrument().StrikePrice()
    quantity = confirmation.Trade().Quantity()
    quantity = abs(quantity)
    return contractSize * quantity * strikePrice

def GetPremiumPrice(confirmation):
    ''' Mandatory field 37K '''

    assert confirmation.Trade().Currency(), "The trade referenced by the confirmation has no currency"
    price = confirmation.Trade().Price()
    currency = confirmation.Trade().Currency().Name()
    return FSwiftUtils.ApplyCurrencyPrecision(currency, price)

def GetPremiumPaymentOption(confirmation):
    ''' This together with PREMIUM_PAYMENT_DATE,PREMIUM_PAYMENT_CURRENCY
        and PREMIUM_PAYMENT_AMOUNT forms the mandatory field 34A in SWIFT.'''

    if GetCode1(confirmation) == 'SELL':
        return 'R'
    else:
        return 'P'

def GetPremiumPaymentDate(confirmation):
    ''' This together with PREMIUM_PAYMENT_OPTION,PREMIUM_PAYMENT_CURRENCY
        and PREMIUM_PAYMENT_AMOUNT forms the mandatory field 34A in SWIFT.'''

    return confirmation.Trade().ValueDay()

def GetPremiumPaymentCurrency(confirmation):
    ''' This together with PREMIUM_PAYMENT_OPTION,PREMIUM_PAYMENT_DATE
        and PREMIUM_PAYMENT_AMOUNT forms the mandatory field 34A in SWIFT.'''

    assert confirmation.Trade().Currency(), "The trade referenced by the confirmation has no currency"
    return confirmation.Trade().Currency().Name()

def GetPremiumPaymentAmount(confirmation):
    ''' This together with PREMIUM_PAYMENT_OPTION,PREMIUM_PAYMENT_DATE
        and PREMIUM_PAYMENT_CURRENCY forms the mandatory field 34A in SWIFT.'''

    return abs(confirmation.Trade().Premium())

def GetSenderCorrespondentOption(confirmation):
    moneyFlow = sharedVariables.get('moneyFlow')
    option = ''
    if moneyFlow:
        option = GetOptionValue('SENDER_CORRESPONDENT', confirmation)
    return option

def GetSenderCorrespondentAccount():
    moneyFlow = sharedVariables.get('moneyFlow')
    account = ''
    if moneyFlow and moneyFlow.AcquirerAccount():
        account = moneyFlow.AcquirerAccount().Account()
    return account

def GetSenderCorrespondentName():
    moneyFlow = sharedVariables.get('moneyFlow')
    name = ''
    if moneyFlow and moneyFlow.AcquirerAccount():
        corrBank = moneyFlow.AcquirerAccount().CorrespondentBank()
        if corrBank:
            name = GetPartyFullName(corrBank)
    return name

def GetSenderCorrespondentAddress():
    moneyFlow = sharedVariables.get('moneyFlow')
    adress = ''
    if moneyFlow and moneyFlow.AcquirerAccount():
        corrBank = moneyFlow.AcquirerAccount().CorrespondentBank()
        if corrBank:
            adress = GetPartyAddress(corrBank)
    return adress

def GetSenderCorrespondentBic():
    moneyFlow = sharedVariables.get('moneyFlow')
    bic = ''
    if moneyFlow and moneyFlow.AcquirerAccount():
        if moneyFlow.AcquirerAccount().Bic():
            bic = moneyFlow.AcquirerAccount().Bic().Alias()
    return bic

def GetIntermediaryPartyInfo(confirmation):
    ''' Optional field 56.
    Option A and D are supported. Option J is not supported. '''

    moneyFlow = sharedVariables.get('moneyFlow')
    option = account = bic = name = address = ''

    if moneyFlow:
        option = GetOptionValue('INTERMEDIARY', confirmation)
        if moneyFlow.CounterpartyAccount():
            account = moneyFlow.CounterpartyAccount().Account2()

            if moneyFlow.CounterpartyAccount().Bic2():
                bic = moneyFlow.CounterpartyAccount().Bic2().Alias()

            corrBank = moneyFlow.CounterpartyAccount().CorrespondentBank2()
            if corrBank:
                name = GetPartyFullName(corrBank)
                address = GetPartyAddress(corrBank)

    return GetPartyInfo(option, account, bic, name, address)


def GetIntermediaryOption(confirmation):
    return GetIntermediaryPartyInfo(confirmation)[0]

def GetIntermediaryAccount(confirmation):
    return GetIntermediaryPartyInfo(confirmation)[1]

def GetIntermediaryName(confirmation):
    return GetIntermediaryPartyInfo(confirmation)[3]

def GetIntermediaryAddress(confirmation):
    return GetIntermediaryPartyInfo(confirmation)[4]

def GetIntermediaryBic(confirmation):
    return GetIntermediaryPartyInfo(confirmation)[2]

def GetAccountWithInstitutionOption(confirmation):
    moneyFlow = sharedVariables.get('moneyFlow')
    option = ''
    if moneyFlow:
        option = GetOptionValue('ACCOUNT_WITH_INSTITUTION', confirmation)
    return option

def GetAccountWithInstitutionAccount():
    moneyFlow = sharedVariables.get('moneyFlow')
    account = ''
    if moneyFlow and moneyFlow.CounterpartyAccount():
        account = moneyFlow.CounterpartyAccount().Account()
    return account

def GetAccountWithInstitutionName():
    moneyFlow = sharedVariables.get('moneyFlow')
    name = ''
    if moneyFlow and moneyFlow.CounterpartyAccount():
        corrBank = moneyFlow.CounterpartyAccount().CorrespondentBank()
        if corrBank:
            name = GetPartyFullName(corrBank)
    return name

def GetAccountWithInstitutionAddress():
    moneyFlow = sharedVariables.get('moneyFlow')
    address = ''
    if moneyFlow and moneyFlow.CounterpartyAccount():
        corrBank = moneyFlow.CounterpartyAccount().CorrespondentBank()
        if corrBank:
            address = GetPartyAddress(corrBank)
    return address

def GetAccountWithInstitutionBic():
    moneyFlow = sharedVariables.get('moneyFlow')
    bic = ''
    if moneyFlow and moneyFlow.CounterpartyAccount():
        if moneyFlow.CounterpartyAccount().Bic():
            bic = moneyFlow.CounterpartyAccount().Bic().Alias()
    return bic

def GetSenderToRecieverInfo():
    ''' Optional field 72 '''

    return 'SENDER TO RECEIVER INFORMATION'

def GetReportingJurisdiction():
    return ''

def GetReportingPartyAddress():
    moneyFlow = sharedVariables.get('moneyFlow')
    address = ''
    if moneyFlow:
        address = GetPartyAddress(moneyFlow.Acquirer())
    return address

def GetReportingPartyBic():
    moneyFlow = sharedVariables.get('moneyFlow')
    bic = ''
    if moneyFlow:
        acqaccount = moneyFlow.AcquirerAccount()
        if acqaccount:
            bic = GetPartyBic(acqaccount)
    return bic

def GetReportingPartyAccount():
    moneyFlow = sharedVariables.get('moneyFlow')
    account = ''
    if moneyFlow:
        acqaccount = moneyFlow.AcquirerAccount()
        if acqaccount:
            account = acqaccount.Account()
    return account

def GetReportingPartyOption(confirmation):
    moneyFlow = sharedVariables.get('moneyFlow')
    option = ''
    if moneyFlow:
        option = GetOptionValue('REPORTING_PARTY', confirmation)
    return option

def GetReportingPartyName():
    moneyFlow = sharedVariables.get('moneyFlow')
    name = ''
    if moneyFlow:
        name = GetPartyFullName(moneyFlow.Acquirer())
    return name

def GetUTINamespace(confirmation):
    return FSwiftUtils.GetUTINamespace(confirmation.Trade())

def GetPriorUTINamespace(confirmation):
    return FSwiftUtils.GetPriorUTINamespace(confirmation.Trade())

def GetTransactionIdentifier(confirmation):
    return FSwiftUtils.GetTransactionIdentifier(confirmation.Trade())

def GetPriorTransactionIdentifier(confirmation):
    return FSwiftUtils.GetPriorTransactionIdentifier(confirmation.Trade())

def GetAdditionalReportingInformation():
    return ''