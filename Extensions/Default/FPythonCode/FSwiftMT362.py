""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/swift/etc/FSwiftMT362.py"
"""----------------------------------------------------------------------------
MODULE
    FSwiftMT362 - Implements confirmation message functionality

    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

----------------------------------------------------------------------------"""

import acm
import FSwiftUtils
import FSwiftMTConfirmation
from FSwiftMTBase import GetOptionValue, GetPartyFullName, GetPartyAddress
from FSwiftMTConfirmation import sharedVariables
from FOperationsEnums import InsType

def Init(confirmation):
    assert confirmation.Trade(), "The confirmation has no trade reference"
    assert confirmation.Trade().Instrument(), "The trade referenced by the confirmation has no instrument"
    global sharedVariables
    calcSpace = sharedVariables.get('calcSpace')
    if not calcSpace:
        sharedVariables['calcSpace'] = acm.Calculations().CreateStandardCalculationsSpaceCollection()

#------------------Seq A---------------------------------
def GetYourReference(confirmation):
    ''' Mandatory field 21 in seq A'''
    
    return FSwiftMTConfirmation.GetYourReference(confirmation)

def GetScopeOfOperation():
    ''' Optional field 94A in seq A. '''

    return 'BILA'

def GetSwapType(confirmation):
    ''' This together with settlement_method forms the mandatory field 23A in seq A
        Type of Swap must contain one of the following codes (Error code(s): T47):
        CAPBUYER Party A bought the cap and paid the premium.
        CAPSELLER Party A sold the cap and received the premium.
        COLLARBYER Party A bought the collar and paid the premium.
        COLLARSLLR Party A sold the collar and received the premium.
        FIXEDFIXED IRS or CS where both parties pay fixed rates.
        FIXEDFLOAT IRS or CS where party A pays fixed and receives floating rates.
        FLOATFIXED IRS or CS where, party A pays floating and receives fixed rates.
        FLOATFLOAT IRS or CS where both Parties pay floating rates.
        FLOORBUYER Party A bought the floor and paid the premium.
        FLOORSLLER Party A sold the floor and received the premium.
    '''

    instrument = confirmation.Trade().Instrument()
    trade = confirmation.Trade()
    insType = instrument.InsType()
    swapType = ''
    if insType in (InsType.SWAP, InsType.CURR_SWAP):
        for leg in instrument.Legs():
            legType = leg.LegType().upper()
            if legType in ['COLLARED FLOAT', 'CAPPED FLOAT', 'FLOORED FLOAT']:
                legType = 'FLOAT'
            swapType += legType

    if insType == InsType.CAP:
        quantity = trade.Quantity()
        swapType = insType.upper()
        if quantity > 0:
            swapType += 'BUYER'
        else:
            swapType += 'SELLER'

    if insType == InsType.FLOOR:
        quantity = trade.Quantity()
        swapType = insType.upper()
        if quantity > 0:
            swapType += 'BUYER'
        else:
            swapType += 'SLLER'

    if instrument.ProductTypeChlItem() == 'Collar':
        swapType = instrument.ProductTypeChlItem().upper()
        quantity = trade.Quantity()
        if quantity > 0:
            swapType += 'BYER'
        else:
            swapType += 'SLLR'

    return swapType

def GetSettlementMethod(confirmation):
    '''This together with type_swap forms the mandatory field 23A in seq A.
       It is assumed that if a cashFlow on the other leg has the same pay date, 
       the payments will be netted'''

    resetCashFlow = GetResetCashFlow(confirmation)
    settlementMethod = 'GROSS'
    if GetCashFlowWithSamePayDateAndCurrency(confirmation, resetCashFlow):
        settlementMethod = 'NET'
    return settlementMethod

def GetContractNumPartyA(confirmation):
    '''Mandatory field 21N in seq A'''

    return confirmation.Trade().Oid()

def GetEffectiveDate(confirmation):
    '''Mandatory field 30V in seq A'''

    effectiveDate = ''
    leg = GetResetCashFlowLeg(confirmation)
    if leg:
        effectiveDate = leg.StartDate()
    return effectiveDate

def GetTermDate(confirmation):
    ''' Mandatory field 30P in seq A'''

    termDate = ''
    leg = GetResetCashFlowLeg(confirmation)
    if leg:
        termDate = leg.EndDate()
    return termDate

#------------------Seq B---------------------------------
def GetIRPPartyBNotAmount(confirmation):
    ''' This together with irp_party_b_curr forms the mandatory field 33F in seq B.'''

    notAmount = ''
    cashFlow = GetIRPPartyBCashFlow(confirmation)
    if cashFlow:
        notAmount = abs(GetIRPNotAmount(confirmation, cashFlow))
    return notAmount

def GetIRPPartyBCurr(confirmation):
    '''This together with irp_party_a_amt forms the mandatory field 33F in seq B.'''

    currency = ''
    cashFlow = GetIRPPartyBCashFlow(confirmation)
    if cashFlow:
        currency = cashFlow.Leg().Currency().Name()
    return currency

def GetIRPPartyBPeriodStartDate(confirmation):
    ''' Mandatory field 30X in seq B'''

    startDate = ''
    cashFlow = GetIRPPartyBCashFlow(confirmation)
    if cashFlow:
        startDate = cashFlow.StartDate()
    return startDate

def GetIRPPartyBPeriodEndDate(confirmation):
    '''Optional field 30Q in seq B'''

    endDate = ''
    cashFlow = GetIRPPartyBCashFlow(confirmation)
    if cashFlow:
        endDate = cashFlow.EndDate()
    return endDate

def GetIRPPartyBResetRate(confirmation):
    assert confirmation.Reset(), "The confirmation has no reset"
    fixingValue = 0.0
    cashFlow = GetIRPPartyBCashFlow(confirmation)
    if cashFlow:
        if cashFlow == GetResetCashFlow(confirmation):
            fixingValue = confirmation.Reset().FixingValue()
        if not fixingValue:
            if cashFlow.Leg().LegType() == 'Fixed':
                fixingValue = cashFlow.Leg().FixedRate()
            else:
                for reset in cashFlow.Resets():
                    if reset.FixingValue():
                        fixingValue = reset.FixingValue()
                        break
    return fixingValue

def GetIRPPartyBResetRateFormatted(confirmation):
    ''' Mandatory field 37G in seq B'''

    return str(GetIRPPartyBResetRate(confirmation))[:13]

def GetIRPPartyBSpread(confirmation):
    '''Mandatory field 37R in seq B'''

    spread = 0.0
    cashFlow = GetIRPPartyBCashFlow(confirmation)
    if cashFlow and (cashFlow == GetResetCashFlow(confirmation) or cashFlow.Leg().LegType() == 'Float'):
        spread = str(cashFlow.Spread())[:13]
    return spread

def GetIRPPartyBTotalRate(confirmation):
    ''' Mandatory field 37M in seq B and seq D'''

    totalRate = 0.0
    cashFlow = GetIRPPartyBCashFlow(confirmation)
    if cashFlow == GetResetCashFlow(confirmation):
        totalRate = cashFlow.Spread()
    totalRate = str(totalRate + GetIRPPartyBResetRate(confirmation))[:13]
    return totalRate

def GetIRPPartyBPaymentDate(confirmation):
    ''' Mandatory field 30F in seq B'''

    paymentDate = ''
    cashFlow = GetIRPPartyBCashFlow(confirmation)
    if cashFlow:
        paymentDate = cashFlow.PayDate()
    return paymentDate

#------------------Seq C---------------------------------
def GetPartyBNumberRepetitions():
    '''Mandatory field 18A in seq C'''

    return 1

def GetNapPartyBPayAmount(confirmation):
    ''' This together with nap_party_b_currency forms the mandatory field 32M in seq C
    If counterparty is not paying '' is returned. '''

    amount = GetNapAmount(confirmation)
    if amount > 0:
        return abs(amount)
    return ''

def GetNapPartyBReceivingAgentOption(confirmation):
    '''Used to populate mandatory field 57A in seq C'''

    moneyFlow = sharedVariables.get('moneyFlow')
    option = ''
    if moneyFlow:
        option = GetOptionValue('NAP_PARTY_B_RECEIVING_AGENT', confirmation)
    return option

def GetNapPartyBReceivingAgentAccount():
    '''Used to populate mandatory field 57A in seq C'''

    moneyFlow = sharedVariables.get('moneyFlow')
    account = ''
    if moneyFlow:
        acquirerAccount = moneyFlow.AcquirerAccount()
        if acquirerAccount:
            account = acquirerAccount.Account()
    return account

def GetNapPartyBReceivingAgentAccountBic():
    '''Used to populate mandatory field 57A in seq C'''

    moneyFlow = sharedVariables.get('moneyFlow')
    bic = ''
    if moneyFlow:
        acquirerAccount = moneyFlow.AcquirerAccount()
        if acquirerAccount:
            if acquirerAccount.Bic():
                bic = acquirerAccount.Bic().Alias()
    return bic

def GetNapPartyBReceivingAgentName():
    '''Used to populate mandatory field 57A in seq C'''

    moneyFlow = sharedVariables.get('moneyFlow')
    name = ''
    if moneyFlow:
        acquirerAccount = moneyFlow.AcquirerAccount()
        if acquirerAccount:
            corrBank = acquirerAccount.CorrespondentBank()
            if corrBank:
                name = GetPartyFullName(corrBank)
    return name

def GetNapPartyBReceivingAgentAddress():
    '''Used to populate mandatory field 57A in seq C'''

    moneyFlow = sharedVariables.get('moneyFlow')
    address = ''
    if moneyFlow:
        acquirerAccount = moneyFlow.AcquirerAccount()
        if acquirerAccount:
            corrBank = acquirerAccount.CorrespondentBank()
            if corrBank:
                address = GetPartyAddress(corrBank)
    return address

#------------------Seq D---------------------------------
def GetIRPPartyANotAmount(confirmation):
    ''' This together with irp_party_a_curr forms the mandatory field 33F in seq D.'''

    notAmount = ''
    cashFlow = GetIRPPartyACashFlow(confirmation)
    if cashFlow:
        notAmount = abs(GetIRPNotAmount(confirmation, cashFlow))
    return notAmount

def GetIRPPartyACurr(confirmation):
    '''This together with irp_party_a_amt forms the mandatory field 33F in seq D.'''

    currency = ''
    cashFlow = GetIRPPartyACashFlow(confirmation)
    if cashFlow:
        currency = cashFlow.Leg().Currency().Name()
    return currency

def GetIRPPartyAPeriodStartDate(confirmation):
    ''' Mandatory field 30X in seq D'''

    startDate = ''
    cashFlow = GetIRPPartyACashFlow(confirmation)
    if cashFlow:
        startDate = cashFlow.StartDate()
    return startDate

def GetIRPPartyAPeriodEndDate(confirmation):
    '''Optional field 30Q in seq D'''

    endDate = ''
    cashFlow = GetIRPPartyACashFlow(confirmation)
    if cashFlow:
        endDate = cashFlow.EndDate()
    return endDate

def GetIRPPartyAResetRate(confirmation):
    assert confirmation.Reset(), "The confirmation has no reset"
    fixingValue = 0.0
    cashFlow = GetIRPPartyACashFlow(confirmation)
    if cashFlow:
        if cashFlow == GetResetCashFlow(confirmation):
            fixingValue = confirmation.Reset().FixingValue()
        if not fixingValue:
            if cashFlow.Leg().LegType() == 'Fixed':
                fixingValue = cashFlow.Leg().FixedRate()
            else:
                for reset in cashFlow.Resets():
                    if reset.FixingValue():
                        fixingValue = reset.FixingValue()
                        break
    return fixingValue

def GetIRPPartyAResetRateFormatted(confirmation):
    ''' Mandatory field 37G in seq D'''

    return str(GetIRPPartyAResetRate(confirmation))[:13]

def GetIRPPartyASpread(confirmation):
    '''Mandatory field 37R in seq D'''

    spread = 0.0
    cashFlow = GetIRPPartyACashFlow(confirmation)
    if cashFlow and (cashFlow == GetResetCashFlow(confirmation) or cashFlow.Leg().LegType() == 'Float'):
        spread = str(cashFlow.Spread())[:13]
    return spread

def GetIRPPartyATotalRate(confirmation):
    ''' Mandatory field 37M in seq D'''

    totalRate = 0.0
    cashFlow = GetIRPPartyACashFlow(confirmation)
    if cashFlow == GetResetCashFlow(confirmation):
        totalRate = cashFlow.Spread()
    totalRate = str(totalRate + GetIRPPartyAResetRate(confirmation))[:13]
    return totalRate

def GetIRPPartyAPaymentDate(confirmation):
    ''' Mandatory field 30F in seq D'''

    paymentDate = ''
    cashFlow = GetIRPPartyACashFlow(confirmation)
    if cashFlow:
        paymentDate = cashFlow.PayDate()
    return paymentDate

#------------------Seq E---------------------------------
def GetPartyANumberRepetitions():
    '''Mandatory field 18A in seq E'''

    return 1

def GetNapPartyAPayAmount(confirmation):
    '''This together with nap_party_a_currency forms the mandatory field 32M in seq E.
    If acquirer is not paying '' is returned. '''

    amount = GetNapAmount(confirmation)
    if amount < 0:
        return abs(amount)
    return ''


def GetNapPartyAReceivingAgentOption(confirmation):
    '''Used to populate mandatory field 57A in seq E'''
    moneyFlow = sharedVariables.get('moneyFlow')
    option = ''
    if moneyFlow:
        option = GetOptionValue('NAP_PARTY_A_RECEIVING_AGENT', confirmation)
    return option

def GetNapPartyAReceivingAgentAccount():
    '''Used to populate mandatory field 57A in seq E'''

    moneyFlow = sharedVariables.get('moneyFlow')
    account = ''
    if moneyFlow:
        counterPartyAccount = moneyFlow.CounterpartyAccount()
        if counterPartyAccount:
            account = counterPartyAccount.Account()
    return account

def GetNapPartyAReceivingAgentAccountBic():
    '''Used to populate mandatory field 57A in seq E'''

    moneyFlow = sharedVariables.get('moneyFlow')
    bic = ''
    if moneyFlow:
        counterPartyAccount = moneyFlow.CounterpartyAccount()
        if counterPartyAccount:
            if counterPartyAccount.Bic():
                bic = counterPartyAccount.Bic().Alias()
    return bic

def GetNapPartyAReceivingAgentName():
    '''Used to populate mandatory field 57A in seq E'''

    moneyFlow = sharedVariables.get('moneyFlow')
    name = ''
    if moneyFlow:
        counterPartyAccount = moneyFlow.CounterpartyAccount()
        if counterPartyAccount:
            corrBank = counterPartyAccount.CorrespondentBank()
            if corrBank:
                name = GetPartyFullName(corrBank)
    return name

def GetNapPartyAReceivingAgentAddress():
    '''Used to populate mandatory field 57A in seq E'''

    moneyFlow = sharedVariables.get('moneyFlow')
    address = ''
    if moneyFlow:
        counterPartyAccount = moneyFlow.CounterpartyAccount()
        if counterPartyAccount:
            corrBank = counterPartyAccount.CorrespondentBank()
            if corrBank:
                address = GetPartyAddress(corrBank)
    return address

#------------------Common Methods------------------------
def GetReset(confirmation):
    return confirmation.Reset()

def GetResetCashFlow(confirmation):
    reset = GetReset(confirmation)
    cashFlow = ''
    if reset:
        cashFlow = reset.CashFlow()
    return cashFlow

def GetResetCashFlowLeg(confirmation):
    resetCashFlow = GetResetCashFlow(confirmation)
    resetCashFlowLeg = ''
    if resetCashFlow:
        resetCashFlowLeg = resetCashFlow.Leg()
    return resetCashFlowLeg

def GetOtherLegWithSameCurrency(confirmation):
    leg = GetResetCashFlowLeg(confirmation)
    otherLeg = ''
    if leg:
        for l in leg.Instrument().Legs():
            if l != leg and l.Currency() == leg.Currency():
                otherLeg = l
                break
    return otherLeg

def GetCashFlowWithSamePayDateAndCurrency(confirmation, cashFlow):
    otherLeg = GetOtherLegWithSameCurrency(confirmation)
    otherCashFlow = ''
    if otherLeg and cashFlow:
        for cf in otherLeg.CashFlows():
            if cf.PayDate() == cashFlow.PayDate():
                if cf.Leg().LegType() == 'Fixed':
                    otherCashFlow = cf
                else:
                    for reset in cf.Resets():
                        if reset.FixingValue():
                            otherCashFlow = cf
                            break
                break
    return otherCashFlow

def GetPayAndReceiveCashFlows(confirmation):
    payCashFlow = ''
    receiveCashFlow = ''
    resetCashFlow = GetResetCashFlow(confirmation)          
    otherCashFlow = GetCashFlowWithSamePayDateAndCurrency(confirmation, resetCashFlow)
    if resetCashFlow.Leg().PayLeg():
        payCashFlow = resetCashFlow
        receiveCashFlow = otherCashFlow
    else:
        payCashFlow = otherCashFlow
        receiveCashFlow = resetCashFlow
    return payCashFlow, receiveCashFlow

#---------------Common Methods seq B and D------------------------
def GetIRPPartyACashFlow(confirmation):
    cashFlow = ''
    trade = confirmation.Trade()
    if trade:
        settlementMethod = GetSettlementMethod(confirmation)
        if settlementMethod == 'GROSS':
            resetCashFlow = GetResetCashFlow(confirmation) 
            if (trade.Nominal() > 0 and resetCashFlow.Leg().PayLeg()) or \
               (trade.Nominal() < 0 and not resetCashFlow.Leg().PayLeg()):
                cashFlow = resetCashFlow
        elif settlementMethod == 'NET': 
            payCashFlow, receiveCashFlow = GetPayAndReceiveCashFlows(confirmation)
            if trade.Nominal() > 0:
                cashFlow = payCashFlow
            else:
                cashFlow = receiveCashFlow
    return cashFlow

def GetIRPPartyBCashFlow(confirmation):
    cashFlow = ''
    trade = confirmation.Trade()
    if trade:
        settlementMethod = GetSettlementMethod(confirmation)
        if settlementMethod == 'GROSS': 
            resetCashFlow = GetResetCashFlow(confirmation) 
            if (trade.Nominal() > 0 and not resetCashFlow.Leg().PayLeg()) or \
               (trade.Nominal() < 0 and resetCashFlow.Leg().PayLeg()):
                cashFlow = resetCashFlow
        elif settlementMethod == 'NET': 
            payCashFlow, receiveCashFlow = GetPayAndReceiveCashFlows(confirmation)
            if trade.Nominal() > 0:
                cashFlow = receiveCashFlow
            else:
                cashFlow = payCashFlow
    return cashFlow

def GetIRPNotAmount(confirmation, cashFlow):
    nominal = ''
    trade = confirmation.Trade()
    if cashFlow:
        value = cashFlow.Calculation().Nominal(sharedVariables.get('calcSpace'), trade, cashFlow.Leg().Currency())
        if value:
            nominal = value.Number()
    return nominal

def GetIRPCapRate(confirmation):
    '''Optional field 37V in seq B and seq D'''

    instrument = confirmation.Trade().Instrument()
    rate = ''
    if instrument.InsType() == 'Cap':
        rate = str(instrument.Legs()[0].Strike())[:12]
    return rate

def GetIRPFloorRate(confirmation):
    '''Optional field 37G in seq B and seq D'''

    instrument = confirmation.Trade().Instrument()
    rate = ''
    if instrument.InsType() == 'Floor':
        rate = str(instrument.Legs()[0].Strike())[:12]
    return rate

#---------------Common Methods seq C and E------------------------
def GetNapPayDate(confirmation):
    ''' Mandatory field 30F in seq C and seq E'''

    payDate = ''
    cashFlow = GetResetCashFlow(confirmation)
    if cashFlow:
        payDate = cashFlow.PayDate()
    return payDate

def GetNapCurrency(confirmation):
    ''' This together with nap_party_a_amount forms the mandatory field 32M in seq C and seq E'''

    currency = ''
    leg = GetResetCashFlowLeg(confirmation)
    if leg:
        currency = leg.Currency().Name()
    return currency

def GetNapAmount(confirmation):
    amount = 0.0
    cashFlow = GetResetCashFlow(confirmation)
    if cashFlow:
        trade = confirmation.Trade()
        calcSpace = sharedVariables.get('calcSpace')
        projectedCalc = cashFlow.Calculation().Projected(calcSpace, trade)
        if projectedCalc:
            if isinstance(projectedCalc, int):
                amount = float(projectedCalc)
            else:
                amount = projectedCalc.Value().Number()
                if acm.Operations.IsValueInfNanOrQNan(amount):
                    amount = 0
        otherCashFlow = GetCashFlowWithSamePayDateAndCurrency(confirmation, cashFlow)
        if otherCashFlow:
            projectedCalc = otherCashFlow.Calculation().Projected(calcSpace, trade)
            if projectedCalc:
                if isinstance(projectedCalc, int):
                    amount = amount + float(projectedCalc)
                else:
                    number = projectedCalc.Value().Number()
                    if acm.Operations.IsValueInfNanOrQNan(amount):
                        number = 0
                    amount = amount + number
        leg = GetResetCashFlowLeg(confirmation)
        if leg:
            currency = leg.Currency()
            currencyName = ''
            if currency:
                currencyName = currency.Name()
            if currencyName:
                amount = FSwiftUtils.ApplyCurrencyPrecision(currencyName, amount)
    return amount
