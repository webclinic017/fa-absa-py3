""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/swift/etc/FSwiftMT320.py"
"""----------------------------------------------------------------------------
MODULE
    FSwiftMT320 - Implements the MT 320 message functionality

    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

----------------------------------------------------------------------------"""

import acm
import FSwiftUtils
import FSwiftMTConfirmation

from FSwiftMTBase import GetOptionValue, GetPartyFullName, GetPartyAddress
from FSwiftMTConfirmation import sharedVariables, GetPartyInfo 
from FSwiftMTLoanDeposit import GetFixedRateCashFlow, GetFloatRateCashFlow
from FOperationsEnums import TradeStatus, LegType
from FConfirmationEnums import EventType
from FSettlementEnums import SettlementType

def Init(confirmation):
    assert confirmation.Trade(), "The confirmation has no trade reference"
    assert confirmation.Trade().Instrument(), "The trade referenced by the confirmation has no instrument"

def IsEventRoll(confirmation):
    assert confirmation.Trade().Contract(), "The trade referenced by the confirmation has no contract"
    assert confirmation.Trade().Contract().Instrument(), "The contract referenced by the trade referenced by the confirmation has no instrument"
    isEventRoll = False
    if confirmation.Trade().Contract().Status() != TradeStatus.VOID and \
        confirmation.Trade().ContractTrdnbr() != confirmation.Trade().Oid() and \
        confirmation.Trade().Instrument().StartDate() == confirmation.Trade().Contract().Instrument().EndDate():
        isEventRoll = True
    return isEventRoll

def GetSIAPartyAIntermediaryPartyInfo(confirmation):
    moneyFlow = sharedVariables.get('moneyFlow')

    option = account = bic = name = address = ''

    if moneyFlow:
        option = GetOptionValue('SIA_PARTY_A_INTERMEDIARY', confirmation)
        if moneyFlow.CounterpartyAccount():
            account = moneyFlow.CounterpartyAccount().Account2()
            if moneyFlow.CounterpartyAccount().Bic2():
                bic = moneyFlow.CounterpartyAccount().Bic2().Name()
            corrBank = moneyFlow.CounterpartyAccount().CorrespondentBank2()
            if corrBank:
                name = GetPartyFullName(corrBank)
                address = GetPartyAddress(corrBank)

    return GetPartyInfo(option, account, bic, name, address)

def GetSIAPartyAIntermediaryOption(confirmation):
    return GetSIAPartyAIntermediaryPartyInfo(confirmation)[0]

def GetSIAPartyAIntermediaryAccount(confirmation):
    return GetSIAPartyAIntermediaryPartyInfo(confirmation)[1]

def GetSIAPartyAIntermediaryBic(confirmation):
    return GetSIAPartyAIntermediaryPartyInfo(confirmation)[2]

def GetSIAPartyAIntermediaryName(confirmation):
    return GetSIAPartyAIntermediaryPartyInfo(confirmation)[3]

def GetSIAPartyAIntermediaryAddress(confirmation):
    return GetSIAPartyAIntermediaryPartyInfo(confirmation)[4]

def GetSIAPartyBIntermediaryPartyInfo(confirmation):
    moneyFlow = sharedVariables.get('moneyFlow')

    option = account = bic = name = address = ''

    if moneyFlow:
        option = GetOptionValue('SIA_PARTY_B_INTERMEDIARY', confirmation)
        if moneyFlow.AcquirerAccount():
            account = moneyFlow.AcquirerAccount().Account2()
            if moneyFlow.AcquirerAccount().Bic2():
                bic = moneyFlow.AcquirerAccount().Bic2().Name()
            corrBank = moneyFlow.AcquirerAccount().CorrespondentBank2()
            if corrBank:
                name = GetPartyFullName(corrBank)
                address = GetPartyAddress(corrBank)

    return GetPartyInfo(option, account, bic, name, address)

def GetSIAPartyBIntermediaryOption(confirmation):
    return GetSIAPartyBIntermediaryPartyInfo(confirmation)[0]

def GetSIAPartyBIntermediaryAccount(confirmation):
    return GetSIAPartyBIntermediaryPartyInfo(confirmation)[1]

def GetSIAPartyBIntermediaryBic(confirmation):
    return GetSIAPartyBIntermediaryPartyInfo(confirmation)[2]

def GetSIAPartyBIntermediaryName(confirmation):
    return GetSIAPartyBIntermediaryPartyInfo(confirmation)[3]

def GetSIAPartyBIntermediaryAddress(confirmation):
    return GetSIAPartyBIntermediaryPartyInfo(confirmation)[4]

def GetInterestAmount(confirmation):
    ''' This together with interest_currency forms the mandatory field 34E in seq B.
    If the interest amount has to be paid by Party A, sign must not be present;
    if the interest amount has to be received by Party A and amount is negative and Sign must be present.'''

    cashFlow = None
    if IsFloatLeg(confirmation):
        cashFlow = GetFloatRateCashFlow(confirmation)
    else:
        cashFlow = GetFixedRateCashFlow(confirmation)
    if (None != cashFlow):
        calcValue = cashFlow.Calculation().Projected(sharedVariables.get('calcSpace'), confirmation.Trade())
        assert confirmation.Trade().Currency(), "The trade referenced by the confirmation has no currency"
        if calcValue:
            value = calcValue.Value().Number()
            if acm.Operations.IsValueInfNanOrQNan(value):
                value = 0
            value = value * -1
            return FSwiftUtils.ApplyCurrencyPrecision(confirmation.Trade().Currency().Name(), value)
    return 0.0

def GetMaturityDate(confirmation):
    ''' Mandatory field 30P in seq B '''

    return confirmation.Trade().Instrument().ExpiryDateOnly()

def GetInterestRate(confirmation):
    ''' Mandatory field 37G in seq B '''
    cashFlow = GetFixedRateCashFlow(confirmation)
    if cashFlow:
        return FSwiftUtils.SwiftNumericFormatter(cashFlow.FixedRate())
    return 0

def GetEventType(confirmation):
    ''' Mandatory field 22B in seq A '''

    eventType = 'CONF'
    if IsEventRoll(confirmation):
        eventType = 'ROLL'
    elif confirmation.EventType() == EventType.DEPOSIT_MATURITY:
        eventType = 'MATU'
    return eventType

def GetNextInterestDueDate(confirmation):
    ''' Optional field 30X in seq B.
    Date is taken after today date and also by adding business days mentioned in Rolling Period. '''

    retVal = ''
    legs = confirmation.Trade().Instrument().Legs()
    dates = []
    for aLeg in legs:
        for aCashFlow in aLeg.CashFlows():
            endDate = aCashFlow.EndDate()
            if endDate and endDate >= acm.Time.DateToday():
                dates.append(endDate)

    if len(dates) > 0:
        dates.sort()

        if dates[0] == acm.Time.DateToday():
            if len(dates) > 1:
                retVal = dates[1]
            else:
                retVal = dates[0]
        else:
            retVal = dates[0]
    else:
        retVal = confirmation.Trade().Instrument().ExpiryDateOnly()

    return retVal

def IsFloatLeg(confirmation):
    assert confirmation.Trade().Instrument().Legs(), "The instrument referenced by the trade referenced by the confirmation has no legs"
    leg = confirmation.Trade().Instrument().Legs().First()
    return (leg.LegType() == LegType.FLOAT)

def GetTermsAndConditions(confirmation):
    ''' Optional field 77D in seq A '''

    import FSwiftParameters as Global

    assert confirmation.Trade().Instrument().Legs(), "The instrument referenced by the trade referenced by the confirmation has no legs"
    leg = confirmation.Trade().Instrument().Legs()[0]
    if leg.LegType() == LegType.FLOAT:
        return '/FLTR/'
    elif Global.TERMS_CONDITIONS :
        return Global.TERMS_CONDITIONS
    else:
        return ''

def GetSettleAmount(confirmation):
    calcSpace = sharedVariables.get('calcSpace')
    if GetEventType(confirmation) == 'ROLL':
        originalTrade = acm.FTrade[confirmation.Trade().ContractTrdnbr()]
        if originalTrade:
            totalAmount = 0
            prolongingAmount = 0
            for moneyFlow in originalTrade.MoneyFlows():
                if moneyFlow.Type() == SettlementType.FIXED_AMOUNT:
                    number = moneyFlow.Calculation().Projected(calcSpace).Value().Number()
                    if acm.Operations.IsValueInfNanOrQNan(number):
                        number = 0
                    totalAmount += number
            for moneyFlow in confirmation.Trade().MoneyFlows():
                if moneyFlow.Type() == SettlementType.FIXED_AMOUNT:
                    number = moneyFlow.Calculation().Projected(calcSpace).Value().Number()
                    if acm.Operations.IsValueInfNanOrQNan(number):
                        number = 0
                    prolongingAmount += number

            curr = confirmation.Trade().Currency()
            amountDiff = prolongingAmount - totalAmount
            return FSwiftUtils.ApplyCurrencyPrecision(curr, amountDiff)

    return ''

def GetSettleCurrency(confirmation):
    if GetEventType(confirmation) == 'ROLL':
        assert confirmation.Trade().Currency(), "The trade referenced by the confirmation has no currency"
        return confirmation.Trade().Currency().Name()
    return ''

def GetYourReference(confirmation):
    return FSwiftMTConfirmation.GetYourReference(confirmation)

def GetPartyARole(confirmation):
    if confirmation.Trade().Premium() < 0:
        return 'L'
    else:
        return 'B'


