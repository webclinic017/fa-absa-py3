""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/swift/etc/FSwiftMT300.py"
"""----------------------------------------------------------------------------
MODULE
    FSwiftMT300 - Implements confirmation message functionality

    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

----------------------------------------------------------------------------"""

import FSwiftUtils
import FSwiftMTConfirmation

from FSwiftMTBase import GetOptionValue, GetPartyFullName, GetPartyAddress, GetPartyBic
from FSwiftMTConfirmation import sharedVariables, GetPartyInfo


def Init():
    pass

def GetBlockTrade():
    '''Optional field 17T.
    This field specifies whether the confirmed deal is a block trade
    and whether an MT 303 Forex/Currency Option Allocation Instruction,
    will be sent by the fund manager. Default value is N. '''

    return 'N'

def GetBuyAmount():
    ''' This together with buy_currency is a mandatory field 32B. '''

    buyAmount = sharedVariables.get('buyAmount', '')
    buyCurrency = GetBuyCurrency()
    return __GetRoundedAmount(buyAmount, buyCurrency)

def GetBuyCurrency():
    ''' This together with buy_amount is a mandatory field 32B '''

    buyMoneyFlow = sharedVariables.get('buyMoneyFlow')
    buyCurrency = ''
    if buyMoneyFlow:
        assert buyMoneyFlow.Currency(), "The buy moneyflow has no currency"
        buyCurrency = buyMoneyFlow.Currency().Name()
    return buyCurrency

def GetBuyDeliveryAgentPartyInfo(confirmation):
    buyMoneyFlow = sharedVariables.get('buyMoneyFlow')
    option = account = bic = name = address = ''

    if buyMoneyFlow:
        option = GetOptionValue('BUY_DELIVERY_AGENT', confirmation)
        if buyMoneyFlow.CounterpartyAccount():
            account = buyMoneyFlow.CounterpartyAccount().Account()

            if buyMoneyFlow.CounterpartyAccount().Bic():
                bic = buyMoneyFlow.CounterpartyAccount().Bic().Alias()

            corrBank = buyMoneyFlow.CounterpartyAccount().CorrespondentBank()
            if corrBank:
                name = GetPartyFullName(corrBank)
                address = GetPartyAddress(corrBank)

    return GetPartyInfo(option, account, bic, name, address)

def GetBuyDeliveryAgentOption(confirmation):
    return GetBuyDeliveryAgentPartyInfo(confirmation)[0]

def GetBuyDeliveryAgentAccount(confirmation):
    return GetBuyDeliveryAgentPartyInfo(confirmation)[1]

def GetBuyDeliveryAgentBic(confirmation):
    return GetBuyDeliveryAgentPartyInfo(confirmation)[2]

def GetBuyDeliveryAgentName(confirmation):
    return GetBuyDeliveryAgentPartyInfo(confirmation)[3]

def GetBuyDeliveryAgentAddress(confirmation):
    return GetBuyDeliveryAgentPartyInfo(confirmation)[4]

def GetBuyIntermediaryPartyInfo(confirmation):
    buyMoneyFlow = sharedVariables.get('buyMoneyFlow')
    option = account = bic = name = address = ''

    if buyMoneyFlow:
        option = GetOptionValue('BUY_INTERMEDIARY', confirmation)
        if buyMoneyFlow.AcquirerAccount():
            account = buyMoneyFlow.AcquirerAccount().Account2()

            if buyMoneyFlow.AcquirerAccount().Bic2():
                bic = buyMoneyFlow.AcquirerAccount().Bic2().Name()

            corrBank = buyMoneyFlow.AcquirerAccount().CorrespondentBank2()
            if corrBank:
                name = GetPartyFullName(corrBank)
                address = GetPartyAddress(corrBank)

    return GetPartyInfo(option, account, bic, name, address)

def GetBuyIntermediaryOption(confirmation):
    return GetBuyIntermediaryPartyInfo(confirmation)[0]

def GetBuyIntermediaryAccount(confirmation):
    return GetBuyIntermediaryPartyInfo(confirmation)[1]

def GetBuyIntermediaryBic(confirmation):
    return GetBuyIntermediaryPartyInfo(confirmation)[2]

def GetBuyIntermediaryName(confirmation):
    return GetBuyIntermediaryPartyInfo(confirmation)[3]

def GetBuyIntermediaryAddress(confirmation):
    return GetBuyIntermediaryPartyInfo(confirmation)[4]

def GetBuyReceivingAgentOption(confirmation):
    return GetOptionValue('BUY_RECEIVING_AGENT', confirmation)

def GetBuyReceivingAgentAccount():
    buyMoneyFlow = sharedVariables.get('buyMoneyFlow')
    account = ''
    if buyMoneyFlow and buyMoneyFlow.AcquirerAccount():
        account = buyMoneyFlow.AcquirerAccount().Account()
    return account

def GetBuyReceivingAgentBic():
    buyMoneyFlow = sharedVariables.get('buyMoneyFlow')
    bic = ''
    if buyMoneyFlow and buyMoneyFlow.AcquirerAccount():
        if buyMoneyFlow.AcquirerAccount().Bic():
            bic = buyMoneyFlow.AcquirerAccount().Bic().Alias()
    return bic

def GetBuyReceivingAgentName():
    buyMoneyFlow = sharedVariables.get('buyMoneyFlow')
    name = ''
    if buyMoneyFlow and buyMoneyFlow.AcquirerAccount():
        corrBank = buyMoneyFlow.AcquirerAccount().CorrespondentBank()
        if corrBank:
            name = GetPartyFullName(corrBank)
    return name

def GetBuyReceivingAgentAddress():
    buyMoneyFlow = sharedVariables.get('buyMoneyFlow')
    adress = ''
    if buyMoneyFlow and buyMoneyFlow.AcquirerAccount():
        corrBank = buyMoneyFlow.AcquirerAccount().CorrespondentBank()
        if corrBank:
            adress = GetPartyAddress(corrBank)
    return adress

def GetSellAmount():
    ''' This together with sell_currency is a mandatory field 33B '''

    sellAmount = sharedVariables.get('sellAmount', '')
    sellCurrency = GetSellCurrency()
    return __GetRoundedAmount(sellAmount, sellCurrency)

def __GetRoundedAmount(amount, currency):
    import FSwiftParameters as Global

    if ('' == amount): #Default value in cache
        return amount
    return round(abs(amount), Global.ROUND_PER_CURR.get(currency, 2))

def GetSellCurrency():
    ''' This together with sell_amount is a mandatory field 33B '''

    sellMoneyFlow = sharedVariables.get('sellMoneyFlow')
    sellCurrency = ''
    if sellMoneyFlow:
        assert sellMoneyFlow.Currency(), "The sell moneyflow has no currency"
        sellCurrency = sellMoneyFlow.Currency().Name()
    return sellCurrency

def GetSellBeneficiaryInstitutionOption(confirmation):
    sellMoneyFlow = sharedVariables.get('sellMoneyFlow')
    option = ''
    if sellMoneyFlow:
        option = GetOptionValue('SELL_BENEFICIARY_INSTITUTION', confirmation)
    return option

def GetSellBeneficiaryInstitutionAccount(confirmation):
    sellMoneyFlow = sharedVariables.get('sellMoneyFlow')
    account = ''
    if sellMoneyFlow and sellMoneyFlow.CounterpartyAccount() and GetSellBeneficiaryInstitutionOption(confirmation) != "J":
        account = sellMoneyFlow.CounterpartyAccount().Account()
    return account

def GetSellBeneficiaryInstitutionName(confirmation):
    sellMoneyFlow = sharedVariables.get('sellMoneyFlow')
    name = ''
    if sellMoneyFlow and sellMoneyFlow.CounterpartyAccount() and GetSellBeneficiaryInstitutionOption(confirmation) != "J":
        name = GetPartyFullName(sellMoneyFlow.Counterparty())
    return name

def GetSellBeneficiaryInstitutionAddress(confirmation):
    sellMoneyFlow = sharedVariables.get('sellMoneyFlow')
    adress = ''
    if sellMoneyFlow and sellMoneyFlow.CounterpartyAccount() and GetSellBeneficiaryInstitutionOption(confirmation) != "J":
        adress = GetPartyAddress(sellMoneyFlow.Counterparty())
    return adress

def GetSellBeneficiaryInstitutionBic(confirmation):
    sellMoneyFlow = sharedVariables.get('sellMoneyFlow')
    bic = ''
    if sellMoneyFlow:
        if GetOptionValue('SELL_BENEFICIARY_INSTITUTION', confirmation) == 'J':
            bic = 'UKWN'
        else:
            if sellMoneyFlow.CounterpartyAccount():
                bic = GetPartyBic(sellMoneyFlow.CounterpartyAccount())
    return bic

def GetSellDeliveryAgentPartyInfo(confirmation):
    sellMoneyFlow = sharedVariables.get('sellMoneyFlow')
    option = account = bic = name = address = ''

    if sellMoneyFlow:
        option = GetOptionValue('SELL_DELIVERY_AGENT', confirmation)
        if sellMoneyFlow.AcquirerAccount():
            account = sellMoneyFlow.AcquirerAccount().Account()

            if sellMoneyFlow.AcquirerAccount().Bic():
                bic = sellMoneyFlow.AcquirerAccount().Bic().Alias()

            corrBank = sellMoneyFlow.AcquirerAccount().CorrespondentBank()
            if corrBank:
                name = GetPartyFullName(corrBank)
                address = GetPartyAddress(corrBank)

    return GetPartyInfo(option, account, bic, name, address)

def GetSellDeliveryAgentOption(confirmation):
    return GetSellDeliveryAgentPartyInfo(confirmation)[0]

def GetSellDeliveryAgentAccount(confirmation):
    return GetSellDeliveryAgentPartyInfo(confirmation)[1]

def GetSellDeliveryAgentBic(confirmation):
    return GetSellDeliveryAgentPartyInfo(confirmation)[2]

def GetSellDeliveryAgentName(confirmation):
    return GetSellDeliveryAgentPartyInfo(confirmation)[3]

def GetSellDeliveryAgentAddress(confirmation):
    return GetSellDeliveryAgentPartyInfo(confirmation)[4]

def GetSellIntermediaryParytInfo(confirmation):
    sellMoneyFlow = sharedVariables.get('sellMoneyFlow')
    option = account = bic = name = address = ''

    if sellMoneyFlow:
        option = GetOptionValue('SELL_INTERMEDIARY', confirmation)
        if sellMoneyFlow.CounterpartyAccount():
            account = sellMoneyFlow.CounterpartyAccount().Account2()

            if sellMoneyFlow.CounterpartyAccount().Bic2():
                bic = sellMoneyFlow.CounterpartyAccount().Bic2().Name()

            corrBank = sellMoneyFlow.CounterpartyAccount().CorrespondentBank2()
            if corrBank:
                name = GetPartyFullName(corrBank)
                address = GetPartyAddress(corrBank)

    return GetPartyInfo(option, account, bic, name, address)

def GetSellIntermediaryOption(confirmation):
    return GetSellIntermediaryParytInfo(confirmation)[0]

def GetSellIntermediaryAccount(confirmation):
    return GetSellIntermediaryParytInfo(confirmation)[1]

def GetSellIntermediaryBic(confirmation):
    return GetSellIntermediaryParytInfo(confirmation)[2]

def GetSellIntermediaryName(confirmation):
    return GetSellIntermediaryParytInfo(confirmation)[3]

def GetSellIntermediaryAddress(confirmation):
    return GetSellIntermediaryParytInfo(confirmation)[4]

def GetSellReceivingAgentOption(confirmation):
    sellMoneyFlow = sharedVariables.get('sellMoneyFlow')
    option = ''
    if sellMoneyFlow:
        option = GetOptionValue('SELL_RECEIVING_AGENT', confirmation)
    return option

def GetSellReceivingAgentAccount():
    sellMoneyFlow = sharedVariables.get('sellMoneyFlow')
    account = ''
    if sellMoneyFlow and sellMoneyFlow.CounterpartyAccount():
        account = sellMoneyFlow.CounterpartyAccount().Account()
    return account

def GetSellReceivingAgentBic():
    sellMoneyFlow = sharedVariables.get('sellMoneyFlow')
    bic = ''
    if sellMoneyFlow and sellMoneyFlow.CounterpartyAccount():
        if sellMoneyFlow.CounterpartyAccount().Bic():
            bic = sellMoneyFlow.CounterpartyAccount().Bic().Alias()
    return bic

def GetSellReceivingAgentName():
    sellMoneyFlow = sharedVariables.get('sellMoneyFlow')
    name = ''
    if sellMoneyFlow and sellMoneyFlow.CounterpartyAccount():
        corrBank = sellMoneyFlow.CounterpartyAccount().CorrespondentBank()
        if corrBank:
            name = GetPartyFullName(corrBank)
    return name

def GetSellReceivingAgentAddress():
    sellMoneyFlow = sharedVariables.get('sellMoneyFlow')
    address = ''
    if sellMoneyFlow and sellMoneyFlow.CounterpartyAccount():
        corrBank = sellMoneyFlow.CounterpartyAccount().CorrespondentBank()
        if corrBank:
            address = GetPartyAddress(corrBank)
    return address

def GetValueDate(confirmation):
    assert confirmation.Trade(), "The confirmation has no trade reference"
    return confirmation.Trade().ValueDay()

def GetCounterpartysReference(confirmation):
    ''' Optional field 26H in sequence c.
    In FX Spot GUI this field is called CP Ref.'''

    ref = ''
    trade = confirmation.Trade()
    if trade:
        ref = trade.YourRef()

    return ref

def GetExchangeRate(confirmation):
    ''' Mandatory field 36. '''

    rate = ''
    trade = confirmation.Trade()
    if trade:
        rate = trade.Price()
    rate = FSwiftUtils.SwiftNumericFormatter(rate)
    return rate

def GetSplitSettlementIndicator():
    ''' Optional field 17U. '''

    return "N" #"Y"

def GetScopeOfOperation():
    ''' Optional field 94A in sequence c. '''

    return 'BILA'

def GetTermsConditions(confirmation):
    '''Optional field 77D.
    It is a narrative field and specifies the legal agreement
    separated by newline characters. '''

    tc = ''
    assert confirmation.Trade(), "The confirmation has no trade reference"
    trade = confirmation.Trade()
    docType = trade.DocumentType()
    if docType:
        agreement = confirmation.AgreementFromDocument(docType)
        if agreement and agreement.Dated():
            tc = trade.DocumentType().Name() + ' AS PER ' + agreement.Dated()
    return tc

def GetYourReference(confirmation):
    ''' Mandatory field 21 '''
    return FSwiftMTConfirmation.GetYourReference(confirmation)

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