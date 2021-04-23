""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/swift/etc/FSwiftMTLoanDeposit.py"
"""----------------------------------------------------------------------------
MODULE
    FSwiftMTLoanDeposit - Module that implements the MT 320 and 330 message
    functionality

    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

----------------------------------------------------------------------------"""

import acm
import FSwiftUtils

from FSwiftMTBase import GetOptionValue, GetPartyFullName, GetPartyAddress
from FSwiftMTConfirmation import sharedVariables
from FOperationsEnums import CashFlowType, LegType

def Init(confirmation):
    assert confirmation.Trade(), "Confirmation has no trade reference"
    assert confirmation.Trade().Instrument(), "The trade referenced by the confirmation has no instrument"
    global sharedVariables
    calcSpace = sharedVariables.get('calcSpace')
    if not calcSpace:
        sharedVariables['calcSpace'] = acm.Calculations().CreateStandardCalculationsSpaceCollection()

def GetSIAPartyAReceivingAgentOption(confirmation):
    moneyFlow = sharedVariables.get('moneyFlow')
    option = ''
    if moneyFlow:
        option = GetOptionValue('SIA_PARTY_A_RECEIVING_AGENT', confirmation)
    return option

def GetSIAPartyAReceivingAgentBic(confirmation):
    moneyFlow = sharedVariables.get('moneyFlow')
    bic = ''
    if moneyFlow:
        if GetOptionValue('SIA_PARTY_A_RECEIVING_AGENT', confirmation) == 'J':
            bic = 'UKWN'
        else:
            if moneyFlow.CounterpartyAccount():
                if moneyFlow.CounterpartyAccount().Bic():
                    bic = moneyFlow.CounterpartyAccount().Bic().Alias()
    return bic

def GetSIAPartyAReceivingAgentAccount(confirmation):
    moneyFlow = sharedVariables.get('moneyFlow')
    account = ''
    if moneyFlow:
        if GetOptionValue('SIA_PARTY_A_RECEIVING_AGENT', confirmation) != 'J':
            if moneyFlow.CounterpartyAccount():
                account = moneyFlow.CounterpartyAccount().Account()
    return account

def GetSIAPartyAReceivingAgentName(confirmation):
    moneyFlow = sharedVariables.get('moneyFlow')
    name = ''
    if moneyFlow:
        if GetOptionValue('SIA_PARTY_A_RECEIVING_AGENT', confirmation) != 'J':
            if moneyFlow.CounterpartyAccount():
                corrBank = moneyFlow.CounterpartyAccount().CorrespondentBank()
                if corrBank:
                    name = GetPartyFullName(corrBank)
    return name

def GetSIAPartyAReceivingAgentAddress(confirmation):
    moneyFlow = sharedVariables.get('moneyFlow')
    address = ''
    if moneyFlow:
        if GetOptionValue('SIA_PARTY_A_RECEIVING_AGENT', confirmation) != 'J':
            if moneyFlow.CounterpartyAccount():
                corrBank = moneyFlow.CounterpartyAccount().CorrespondentBank()
                if corrBank:
                    address = GetPartyAddress(corrBank)
    return address

def GetSIAPartyBReceivingAgentOption(confirmation):
    moneyFlow = sharedVariables.get('moneyFlow')
    option = ''
    if moneyFlow:
        option = GetOptionValue('SIA_PARTY_B_RECEIVING_AGENT', confirmation)
    return option

def GetSIAPartyBReceivingAgentBic(confirmation):
    moneyFlow = sharedVariables.get('moneyFlow')
    bic = ''
    if moneyFlow:
        if GetOptionValue('SIA_PARTY_B_RECEIVING_AGENT', confirmation) == 'J':
            bic = 'UKWN'
        else:
            if moneyFlow.AcquirerAccount():
                if moneyFlow.AcquirerAccount().Bic():
                    bic = moneyFlow.AcquirerAccount().Bic().Alias()
    return bic

def GetSIAPartyBReceivingAgentAccount(confirmation):
    moneyFlow = sharedVariables.get('moneyFlow')
    account = ''
    if moneyFlow:
        if GetOptionValue('SIA_PARTY_B_RECEIVING_AGENT', confirmation) != 'J':
            if moneyFlow.AcquirerAccount():
                account = moneyFlow.AcquirerAccount().Account()
    return account

def GetSIAPartyBReceivingAgentName(confirmation):
    moneyFlow = sharedVariables.get('moneyFlow')
    name = ''
    if moneyFlow:
        if GetOptionValue('SIA_PARTY_B_RECEIVING_AGENT', confirmation) != 'J':
            if moneyFlow.AcquirerAccount():
                corrBank = moneyFlow.AcquirerAccount().CorrespondentBank()
                if corrBank:
                    name = GetPartyFullName(corrBank)
    return name

def GetSIAPartyBReceivingAgentAddress(confirmation):
    moneyFlow = sharedVariables.get('moneyFlow')
    address = ''
    if moneyFlow:
        if GetOptionValue('SIA_PARTY_B_RECEIVING_AGENT', confirmation) != 'J':
            if moneyFlow.AcquirerAccount():
                corrBank = moneyFlow.AcquirerAccount().CorrespondentBank()
                if corrBank:
                    address = GetPartyAddress(corrBank)
    return address

def GetValueDate(confirmation):
    return confirmation.Trade().ValueDay()

def GetPrincipalCurrency(confirmation):
    assert confirmation.Trade().Currency(), "The trade referenced by the confirmation has no currency"
    return confirmation.Trade().Currency().Name()

def GetPrincipalAmount(confirmation):
    assert confirmation.Trade().Currency(), "The trade referenced by the confirmation has no currency"
    curr = confirmation.Trade().Currency().Name()
    amount = confirmation.Trade().Premium()
    return FSwiftUtils.ApplyCurrencyPrecision(curr, abs(amount))

def GetInterestCurrency(confirmation):
    return GetPrincipalCurrency(confirmation)

def GetDayCountFraction(confirmation):
    legs = confirmation.Trade().Instrument().Legs()
    if legs:
        leg = legs[0]
        return leg.DayCountMethod().upper()
    return ''

def GetFloatRateCashFlow(confirmation):
    return __GetRateCashFlow(CashFlowType.FLOAT_RATE, confirmation)

def GetFixedRateCashFlow(confirmation):
    return __GetRateCashFlow(CashFlowType.FIXED_RATE, confirmation)
    
def __GetRateCashFlow(cashFlowType, confirmation):
    assert confirmation.Trade().Instrument().Legs(), "The instrument referenced by the trade referenced by the confirmation has no legs"
    leg = confirmation.Trade().Instrument().Legs().First()
    selection = acm.FCashFlow.Select('leg = %d and cashFlowType = "%s"' % (leg.Oid(), cashFlowType))
    if (selection.Size() > 0):
        return selection.SortByProperty('StartDate').First()
    return None

def GetCashFlow(confirmation):
    legTocfTypeMappings = { LegType.CALL_FIXED : CashFlowType.CALL_FIXED_RATE,
                    LegType.CALL_FIXED_ADJUSTABLE : CashFlowType.CALL_FIXED_RATE_ADJUSTABLE,
                    LegType.CALL_FLOAT : CashFlowType.CALL_FLOAT_RATE
                     }

    cashflows = {}
    legs = confirmation.Trade().Instrument().Legs()
    for aLeg in legs:
        cfType = legTocfTypeMappings.get(aLeg.LegType(), '')
        if cfType:
            for aCashFlow in aLeg.CashFlows():
                if aCashFlow.CashFlowType() == cfType:
                    cashflows[aCashFlow.StartDate()] = aCashFlow

    cfStartdates = list(cashflows.keys())
    cfStartdates.sort()

    dateToday = acm.Time.DateToday()
    for startDate in cfStartdates:
        endDate = cashflows[startDate].EndDate()
        if startDate <= dateToday <= endDate or startDate > dateToday:
            return cashflows[startDate]

    return ''
