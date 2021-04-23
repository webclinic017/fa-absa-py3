""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/swift/etc/FSwiftMT330.py"
"""----------------------------------------------------------------------------
MODULE
    FSwiftMT330 - Implements confirmation message functionality

    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

----------------------------------------------------------------------------"""


import acm
import FSwiftUtils

from FSwiftMTLoanDeposit import sharedVariables, GetCashFlow
from FOperationsEnums import CashFlowType

def GetInterestAmount(confirmation):
    ''' Mandatory field 37G in seq B '''

    cashFlow = GetCashFlow(confirmation)
    if cashFlow:
        assert confirmation.Trade(), "The confirmation has no trade reference"
        assert confirmation.Trade().Currency(), "The trade referenced by the confirmation has no currency"
        calcValue = cashFlow.Calculation().Projected(sharedVariables.get('calcSpace'), confirmation.Trade())
        if calcValue:
            if isinstance(calcValue, int):
                value = float(calcValue)
            else:
                value = calcValue.Value().Number()
                if acm.Operations.IsValueInfNanOrQNan(value):
                    value = 0
            return FSwiftUtils.ApplyCurrencyPrecision(confirmation.Trade().Currency().Name(), value)
    return ''

def GetInterestRate(confirmation):
    ''' Mandatory field 37G in seq B '''

    if confirmation.Reset():
        return confirmation.Reset().FixingValue()

    interestRate = ''
    cashFlow = GetCashFlow(confirmation)
    if cashFlow:
        interestRate = cashFlow.FixedRate()
        if not interestRate:
            for aReset in cashFlow.Resets():
                if aReset.FixingValue():
                    interestRate = aReset.FixingValue()
                    break
    return interestRate

def GetProjectedCashFlow(cashFlow, trade):
    value = ''
    calcValue = cashFlow.Calculation().Projected(sharedVariables.get('calcSpace'), trade)
    if isinstance(calcValue, int):
        value = float(calcValue)
    else:
        value = calcValue.Value().Number()
        if acm.Operations.IsValueInfNanOrQNan(value):
            value = 0
    return value

def GetPeriodNotice(confirmation):
    assert confirmation.Trade(), "The confirmation has no trade reference"
    assert confirmation.Trade().Instrument(), "The trade referenced by the confirmation has no instrument"
    unit_map = dict(Days=1, Weeks=7, Months=30, Years=365)
    unit = confirmation.Trade().Instrument().NoticePeriodUnit()
    days = confirmation.Trade().Instrument().NoticePeriodCount() * unit_map[unit]
    if days > 999:
        days = 999
    return '%03d' % days

def GetEventType():
    ''' Mandatory field 22B in seq A '''
    # MATU (Close trade) and ROLL (Extend Open End) should be implemented

    return 'CONF'

def GetBalanceAmount(confirmation):
    ''' This together with balance_currency forms the mandatory field 32B in seq B '''

    assert confirmation.Trade(), "The confirmation has no trade reference"
    assert confirmation.Trade().Instrument(), "The trade referenced by the confirmation has no instrument"
    legs = confirmation.Trade().Instrument().Legs()
    for aLeg in legs:
        cashFlows = aLeg.CashFlows()
        for aCashFlow in cashFlows:
            if aCashFlow.CashFlowType() == CashFlowType.REDEMPTION_AMOUNT:
                value = GetProjectedCashFlow(aCashFlow, confirmation.Trade())
                return FSwiftUtils.ApplyCurrencyPrecision(aLeg.Currency().Name(), abs(value))
    return ''

def GetBalanceCurrency(confirmation):
    ''' This together with balance_amount forms the mandatory field 32B in seq B '''

    assert confirmation.Trade(), "The confirmation has no trade reference"
    assert confirmation.Trade().Instrument(), "The trade referenced by the confirmation has no instrument"
    curr = ''
    legs = confirmation.Trade().Instrument().Legs()
    if legs:
        assert legs[0].Currency(), "The first leg has no currency"
        curr = legs[0].Currency().Name()
    return curr

def GetTermsAndConditions():
    ''' Optional naarative field 77D in seq A '''

    import FSwiftParameters as Global

    if Global.TERMS_CONDITIONS :
        return Global.TERMS_CONDITIONS
    return ''

def GetPartyARole(confirmation):
    assert confirmation.Trade(), "The confirmation has no trade reference"
    if confirmation.Trade().Quantity() < 0:
        return 'L'
    else:
        return 'B'

