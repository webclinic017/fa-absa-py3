""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/swift/etc/FSwiftMT306.py"
"""----------------------------------------------------------------------------
MODULE
    FSwiftMT306 - Module that implements the MT 306 message functionality

    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

----------------------------------------------------------------------------"""

import acm
import ael
import FSwiftUtils
import FOperationsUtils as Utils
import FSwiftMTConfirmation

from FSwiftMTBase import GetOptionValue, GetPartyFullName, GetPartyAddress
from FSwiftMTConfirmation import sharedVariables
from FConfirmationEnums import EventType
from FOperationsEnums import BarrierOptionType, ExerciseType, SettleType, BarrierMonitoring, ExoticEventType

def Init(confirmation):
    assert confirmation.Trade(), "The confirmation has no trade reference"
    assert confirmation.Trade().Instrument(), "The trade referenced by the confirmation has no instrument"

def GetSIPPartyReceivingAgentOption(confirmation):
    moneyFlow = sharedVariables.get('moneyFlow')
    option = ''
    if moneyFlow:
        option = GetOptionValue('SIP_PARTY_RECEIVING_AGENT', confirmation)
    return option

def GetSIPPartyReceivingAgentBic(confirmation):
    moneyFlow = sharedVariables.get('moneyFlow')
    bic = ''
    if moneyFlow:
        if confirmation.Trade().Premium() < 0:
            if moneyFlow.AcquirerAccount():
                if moneyFlow.AcquirerAccount().Bic():
                    bic = moneyFlow.AcquirerAccount().Bic().Alias()
        else:
            if moneyFlow.CounterpartyAccount():
                if moneyFlow.CounterpartyAccount().Bic():
                    bic = moneyFlow.CounterpartyAccount().Bic().Alias()
    return bic

def GetSIPPartyReceivingAgentAccount(confirmation):
    moneyFlow = sharedVariables.get('moneyFlow')
    account = ''
    if moneyFlow:
        if confirmation.Trade().Premium() < 0:
            if moneyFlow.AcquirerAccount():
                account = moneyFlow.AcquirerAccount().Account()
        else:
            if moneyFlow.CounterpartyAccount():
                account = moneyFlow.CounterpartyAccount().Account()
    return account

def GetSIPPartyReceivingAgentName(confirmation):
    moneyFlow = sharedVariables.get('moneyFlow')
    name = ''
    if moneyFlow:
        if confirmation.Trade().Premium() < 0:
            if moneyFlow.AcquirerAccount():
                corrBank = moneyFlow.AcquirerAccount().CorrespondentBank()
                if corrBank:
                    name = GetPartyFullName(corrBank)

        else:
            if moneyFlow.CounterpartyAccount():
                corrBank = moneyFlow.CounterpartyAccount().CorrespondentBank()
                if corrBank:
                    name = GetPartyFullName(corrBank)
    return name

def GetSIPPartyReceivingAgentAddress(confirmation):
    moneyFlow = sharedVariables.get('moneyFlow')
    address = ''
    if moneyFlow:
        if confirmation.Trade().Premium() < 0:
            if moneyFlow.AcquirerAccount():
                corrBank = moneyFlow.AcquirerAccount().CorrespondentBank()
                if corrBank:
                    address = GetPartyAddress(corrBank)
        else:
            if moneyFlow.CounterpartyAccount():
                corrBank = moneyFlow.CounterpartyAccount().CorrespondentBank()
                if corrBank:
                    address = GetPartyAddress(corrBank)
    return address

def GetCalculationAgentOption(confirmation):
    option = GetOptionValue('CALCULATION_AGENT', confirmation)
    if option != 'J':
        calcAgent =  confirmation.Trade().Calcagent()
        if calcAgent == 'Both':
            option = 'D'
        elif calcAgent != 'CP' and calcAgent != 'We':
            option = 'J'
    return option

def GetCalculationAgentBic(confirmation):
    bic = ''
    if GetOptionValue('CALCULATION_AGENT', confirmation) == 'J':
        bic = 'UKWN'
    else:
        calcAgent = confirmation.Trade().Calcagent()
        if calcAgent == 'CP':
            cp = confirmation.Counterparty()
            if cp:
                bic = confirmation.CounterpartyAddress()
        elif calcAgent == 'We':
            acq = confirmation.Acquirer()
            if acq:
                bic = confirmation.AcquirerAddress()
        elif calcAgent != 'Both':
            bic = 'UKWN'
    return bic

def GetCalculationAgentAccount():
    return ''

def GetCalculationAgentName(confirmation):
    name = ''
    if GetOptionValue('CALCULATION_AGENT', confirmation) != 'J':
        calcAgent = confirmation.Trade().Calcagent()
        if calcAgent == 'CP':
            cp = confirmation.Counterparty()
            if cp:
                name = cp.Name()
        elif calcAgent == 'We':
            acq = confirmation.Acquirer()
            if acq:
                name = acq.Name()
        elif calcAgent == 'Both':
            name = 'JOINT'
    return name

def GetCalculationAgentAddress(confirmation):
    address = ''
    option = GetOptionValue('CALCULATION_AGENT', confirmation)
    if option != 'J':
        calcAgent = confirmation.Trade().Calcagent()
        if calcAgent == 'CP':
            cp = confirmation.Counterparty()
            if cp:
                address = GetPartyAddress(cp)
        elif calcAgent == 'We':
            acq = confirmation.Acquirer()
            if acq:
                address = GetPartyAddress(acq)
    return address

def GetScopeOfOperation():
    '''Optional field 94A in seq A.
       If field 94 is changed to other code, then seq J is mandatory. '''

    return 'BILA'

def GetStrikePrice(confirmation):
    ''' Mandatory field 22C in seq A '''

    return confirmation.Trade().Instrument().StrikePrice()

def GetContractNoOfPartyA(confirmation):
    ''' Mandatory field 21N in seqA '''

    contractNo = ''
    eventType = confirmation.EventType()
    if eventType in [EventType.NEW_TRADE, EventType.NEW_TRADE_CANCELLATION]:
        contractNo = confirmation.Trade().Oid()
    elif eventType in [EventType.NEW_TRADE_AMENDMENT, EventType.NEW_TRADE_DUPLICATE]:
        contractNo = confirmation.Trade().ContractTrdnbr()

    return contractNo

def GetOptionStyle(confirmation):
    ''' Mandatory field 12F in seqA '''

    optionStyle = ''
    instrument = confirmation.Trade().Instrument()

    if instrument.Digital():
        optionStyle = 'DIGI'
    elif instrument.Exotic():
        excotic = instrument.Exotic()
        if excotic.BarrierOptionType() in (BarrierOptionType.DOUBLE_OUT, BarrierOptionType.DOWN_AND_OUT, BarrierOptionType.UP_AND_OUT):
            optionStyle = 'NOTO'
        elif all([excotic.BarrierOptionType(), excotic.DigitalBarrierType()]):
            optionStyle = 'BINA'
    else:
        optionStyle = 'VANI'

    return optionStyle

def GetExpirationStyle(confirmation):
    ''' Mandatory field 12E in seq A '''

    expirationCodes = {ExerciseType.AMERICAN:'AMER' , ExerciseType.EUROPEAN:'EURO'}
    exerciseType = confirmation.Trade().Instrument().ExerciseType()
    return expirationCodes.get(exerciseType, '')

def GetBarrierIndicator(confirmation):
    ''' Mandatory field 17A in seq A '''

    if confirmation.Trade().Instrument().Barrier() > 0:
        return 'Y'
    else:
        return 'N'

def GetNonDeliverableIndicator(confirmation):
    ''' Mandatory field 17F in seq A '''

    if confirmation.Trade().Instrument().SettlementType() == SettleType.PHYSICAL_DELIVERY:
        return 'N'
    else:
        return 'Y'

def GetEventType(confirmation):
    ''' This together with EventTypeNarrative forms the mandatory field 22K in seq A '''
    eventType = confirmation.EventType()
    if eventType == EventType.NEW_TRADE:
        return 'CONF'
    else:
        return 'OTHR'

def GetEventTypeNarrative(confirmation):
    ''' This together with EventType forms the mandatory field 22K in seq A '''
    eventTypeNarrative = confirmation.EventType()
    if (len(eventTypeNarrative) > 35):
        eventTypeNarrative = eventTypeNarrative[0:35]
    return eventTypeNarrative

def GetTypeOfAgreement(confirmation):
    ''' Mandatory field 77H in seq A.
    Imp Note :  Codes specified in SWIFT stds should be configured in ChoiceList '''

    documentType = ''
    documentCodes = ['AFB', 'DERV', 'FBF', 'FEOMA', 'ICOM', 'IFEMA', 'ISDA']
    trade = confirmation.Trade()

    if trade.DocumentType():
        if trade.DocumentType().Name() in documentCodes:
            documentType = trade.DocumentType().Name()

    return documentType

def GetDateOfAgreement(confirmation):
    ''' Optional field in 77H in seq A.
    Imp Note :  Codes specified in SWIFT stds should be configured in ChoiceList '''

    date = ''
    trade = confirmation.Trade()

    if trade.DocumentType():
        tradeDocumentType = trade.DocumentType().Name()
        cp = confirmation.Counterparty()
        agreements = cp.Agreements()
        agreementStartDates = []

        for agreement in agreements:
            if agreement.DocumentTypeChlItem().Name() == tradeDocumentType:
                agreementStartDates.append(agreement.Dated())

        if agreementStartDates:
            date = max(agreementStartDates)

    return date

def GetVersionOfAgreement(confirmation):
    ''' Optional field in 77H in seq A '''
    date = GetDateOfAgreement(confirmation)
    year = date.split('-')[0]
    return year

def GetBuySellIndicator(confirmation):
    ''' Mandatory field 17V in seq B '''

    if confirmation.Trade().Quantity() >= 0:
        return 'B'
    else:
        return 'S'

def GetExpirationDate(confirmation):
    ''' Mandatory field 30X in seq B '''

    return confirmation.Trade().Instrument().ExpiryDateOnly()

def GetExpirationLocation(confirmation):
    '''  This together with ExpirationTime forms the mandatory field 29E in seq B '''

    import FSwiftParameters as Global

    location = ''
    fixingSource = confirmation.Trade().Instrument().FixingSource()
    if fixingSource:
        city = fixingSource.City()
        if city:
            city = city.upper()
            if city in Global.city_dict:
                location = Global.city_dict[city]
        else:
            Utils.LogVerbose("Missing field: City on Fixing source (%s)" % fixingSource.Oid())
    else:
        Utils.LogVerbose("Missing Fixing source information")

    return location

def GetExpirationTime(confirmation):
    '''  This together with expiration_location forms the mandatory field 29E in seq B '''

    expirationTime = ''
    fixingSource = confirmation.Trade().Instrument().FixingSource()
    if fixingSource:
        expirationTime = fixingSource.ExternalCutOff()
        if not expirationTime:
            Utils.LogVerbose("Missing field: External Cut-off Time on Fixing source (%s)" % fixingSource.Oid())
    else:
        Utils.LogVerbose("Missing Fixing source information")

    return expirationTime

def GetFinalSettlementDate(confirmation):
    ''' Mandatory field 30A in seq B '''

    settlementDate = ''
    expiryDate = confirmation.Trade().Instrument().ExpiryDateOnly()
    if expiryDate:
        offset = confirmation.Trade().Instrument().PayDayOffset()
        settlementDate = ael.date(expiryDate).add_days(offset).to_string("%Y-%m-%d")

    return settlementDate

def GetPremiumPaymentDate(confirmation):
    ''' Mandatory field 30V in seq B1 '''

    return confirmation.Trade().ValueDay()

def GetPremiumCurrency(confirmation):
    ''' This together with premium_amount forms the mandatory field 34B in seq B1 '''

    assert confirmation.Trade().Currency(), "The trade referenced by the confirmation has no currency"
    return confirmation.Trade().Currency().Name()

def GetPremiumAmount(confirmation):
    ''' This together with premium_currency forms the mandatory field 34B in seq B1 '''

    return abs(confirmation.Trade().Premium())

def GetSettlementType(confirmation):
    ''' Mandatory field 26F in seq D
    This field should contain codes NETCASH or PRINCIPAL. '''

    if confirmation.Trade().Instrument().SettlementType() == SettleType.PHYSICAL_DELIVERY:
        return 'PRINCIPAL'
    else:
        return 'NETCASH'

def GetPutCurrency(confirmation):
    ''' This together with put_ammount forms the mandatory field 32B in seq D '''

    assert confirmation.Trade().Instrument().Underlying(), "The instrument referenced by the trade referenced by the confirmation has no underlying instrument"
    return confirmation.Trade().Instrument().Underlying().Name()

def GetPutAmount(confirmation):
    '''  This together with put_currency forms the mandatory field 32B in seq D '''

    return abs(confirmation.Trade().Quantity())

def GetCallCurrency(confirmation):
    '''  This together with call_currency forms the mandatory field 33B in seq D '''

    assert confirmation.Trade().Instrument().StrikeCurrency(), "The instrument referenced by the trade referenced by the confirmation has no strike currency"
    return confirmation.Trade().Instrument().StrikeCurrency().Name()

def GetCallAmount(confirmation):
    assert confirmation.Trade().Instrument().StrikeCurrency(), "The instrument referenced by the trade referenced by the confirmation has no strike currency"
    amount = confirmation.Trade().Quantity() * confirmation.Trade().Instrument().StrikePrice()
    return FSwiftUtils.ApplyCurrencyPrecision(confirmation.Trade().Instrument().StrikeCurrency().Name(), abs(amount))

def GetPayoutCurrency(confirmation):
    ''' This together with payout_ammount forms the mandatory field 32B in seq D '''

    assert confirmation.Trade().Instrument().Underlying(), "The instrument referenced by the trade referenced by the confirmation has no underlying instrument"
    return confirmation.Trade().Instrument().Underlying().Name()

def GetPayoutAmount(confirmation):
    ''' This together with payout_currency forms the mandatory field 32B in seq D '''

    return abs(confirmation.Trade().Quantity())

def GetPayoutReceivingAgentOption():
    '''Mandatory field 57A in seq E.
    This is field is not functionally supported by Front Arena.
    Because of network validation rule C8, this field becomes mandatory.'''
    return 'J'

def GetPayoutReceivingAgentBic():
    return 'UKWN'

def GetTypeOfBarrier(confirmation):
    ''' Mandatory field 22G in seq F'''

    typeCode = ''
    excotic = confirmation.Trade().Instrument().Exotic()
    if excotic:
        barrier_type = excotic.BarrierOptionType()
        if barrier_type == BarrierOptionType.DOUBLE_IN:
            typeCode = 'DKIN'
        elif barrier_type == BarrierOptionType.DOUBLE_OUT:
            typeCode = 'DKOT'
        elif barrier_type in (BarrierOptionType.DOWN_AND_IN, BarrierOptionType.UP_AND_IN):
            typeCode = 'SKIN'
        elif barrier_type in (BarrierOptionType.DOWN_AND_OUT, BarrierOptionType.UP_AND_OUT):
            typeCode = 'SKOT'

    return typeCode

def GetBarrierLevel(confirmation):
    ''' Mandatory field 37J in seq F'''

    excotic = confirmation.Trade().Instrument().Exotic()
    if excotic:
        return excotic.DoubleBarrier()
    else:
        return confirmation.Trade().Instrument().Barrier()

def GetBarrierWindowStartDate(event):
    ''' This together with barrier window end date forms the mandatory field 30G in seq F1 '''
    return event.Date()

def GetBarrierWindowEndDate(event, confirmation):
    ''' This together with barrier window start date forms the mandatory field 30G in seq F1 '''

    exotic = confirmation.Trade().Instrument().Exotic()
    if exotic and exotic.BarrierMonitoring() == BarrierMonitoring.DISCRETE:
        return confirmation.Trade().Instrument().ExpiryDateOnly()
    return event.EndDate()

def GetBarriers(confirmation):
    barriers = acm.FArray()
    exotic = confirmation.Trade().Instrument().Exotic()
    if exotic and exotic.BarrierMonitoring() in [BarrierMonitoring.WINDOW, BarrierMonitoring.DISCRETE]:
        exoticEvents = confirmation.Trade().Instrument().ExoticEvents().SortByProperty("Date")
        for exoticEvent in exoticEvents:
            if exoticEvent.Type() == ExoticEventType.BARRIER_DATE:
                barriers.Add(exoticEvent)
    else:
        #Create dummy barrier event for default values
        exoticEvent = acm.FExoticEvent()
        tradeDate = acm.Time.AsDate(confirmation.Trade().TradeTime())
        exoticEvent.Date(tradeDate)    #change to trade day
        exoticEvent.EndDate(confirmation.Trade().Instrument().ExpiryDateOnly())
        barriers.Add(exoticEvent)

    return barriers

def GetStartDateLocation(dummyEvent, confirmation):
    ''' This together with start_date_time forms the mandatory field 29J in seq F1 '''

    return GetExpirationLocation(confirmation)

def GetStartDateTime(dummyEvent):
    ''' This together with start_date_location forms the mandatory field 29J in seq F1 '''

    return '0000'

def GetEndDateLocation(dummyEvent, confirmation):
    ''' This together with end_date_time forms the mandatory field 29K in seq F1 '''

    return GetExpirationLocation(confirmation)

def GetEndDateTime(dummyEvent):
    ''' This together with end_date_location forms the mandatory field 29K in seq F1 '''

    return '0000'

def GetTypeOfTrigger(confirmation):
    ''' Mandatory field 22J in seq G '''

    if confirmation.Trade().Instrument().Barrier():
        return 'SITR'
    excotic = confirmation.Trade().Instrument().Exotic()
    if excotic:
        if excotic.DoubleBarrier():
            return 'DBTR'

    return ''

def GetTriggerLevel(confirmation):
    ''' Mandatory field 37U in seq G '''

    return GetBarrierLevel(confirmation)

def GetCurrencyPair(confirmation):
    ''' Mandatory field 32Q in seq G '''

    assert confirmation.Trade().Instrument().Underlying(), "The instrument referenced by the trade referenced by the confirmation has no underlying instrument"
    assert confirmation.Trade().Instrument().StrikeCurrency(), "The instrument referenced by the trade referenced by the confirmation has no strike currency"
    curr1 = confirmation.Trade().Instrument().Underlying().Name()
    curr2 = confirmation.Trade().Instrument().StrikeCurrency().Name()
    return "%s/%s" % (curr1, curr2)

def GetSettlementRateSource(confirmation):
    '''Mandatory field 14S in seq H '''

    source = ''
    if confirmation.Trade().Instrument().SettlementType() == SettleType.CASH:
        fixingSource = confirmation.Trade().Instrument().FixingSource()
        if fixingSource:
            source = fixingSource.Name()

    return source

def GetSettlementCurrency(confirmation):
    '''Mandatory field 32E in seq H '''

    assert confirmation.Trade().Currency(), "The trade referenced by the confirmation has no currency"
    return confirmation.Trade().Currency().Name()

def GetLowerBarrierLevel(confirmation):
    '''Optional field 37L in seq F '''

    barrier = 0
    doubleBarrier = 0

    barrier = confirmation.Trade().Instrument().Barrier()
    excotic = confirmation.Trade().Instrument().Exotic()
    if excotic:
        doubleBarrier = excotic.DoubleBarrier()

    return min(barrier, doubleBarrier)

def GetLowerTriggerLevel(confirmation):
    '''Optional field 37P in seq G '''

    return GetLowerBarrierLevel(confirmation)

def GetEarliestExerciseDate(confirmation):
    ''' Optional field 30P in seq D '''

    if confirmation.Trade().Instrument().ExerciseType() == ExerciseType.AMERICAN:
        return confirmation.Trade().ValueDay()
    else:
        return ''

def GetAdditionalInfoAgreement():
    return 'Additional info'

def GetYourReference(confirmation):
    ''' Mandatory field 21 '''

    return FSwiftMTConfirmation.GetYourReference(confirmation)
