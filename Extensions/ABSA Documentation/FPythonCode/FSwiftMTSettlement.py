""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/swift/etc/FSwiftMTSettlement.py"
"""---------------------------------------------------------------------------------------------------------------------
MODULE
    FSwiftMTSettlement

DESCRIPTION
    FSwiftMTSettlement - Implements settlement message functionality

    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

------------------------------------------------------------------------------------------------------------------------
HISTORY
========================================================================================================================
Date            Change no       Developer               Requester               Description
------------------------------------------------------------------------------------------------------------------------
2021-03-24      FAOPS-855       Tawanda Mukhalela       Wandile Sithole         Fix Value date for Good Value 
                                                                                Payments
------------------------------------------------------------------------------------------------------------------------
"""
import FOperationsUtils as Utils
import FSwiftUtils

from FSwiftSettlementWrapper import FSwiftSettlement
from FSettlementEnums import RelationType


def GetSeqNbr(settlement):
    return settlement.Oid()


def GetSettlementCurrency(settlement):
    return settlement.Currency().Name()


def GetSubNetwork(settlement):
    ''' Returns the swift sub network. Extra validation is performed for
    TARGET2 and EBA '''

    import FSwiftParameters as Global

    swiftSettlement = FSwiftSettlement(settlement)
    retVal = ""
    if Global.SWIFT_SUB_NETWORKS:
        counterPartyAccountSubNetwork = settlement.CounterpartyAccountSubNetworkName()
        if counterPartyAccountSubNetwork in Global.SWIFT_SUB_NETWORKS:
            if counterPartyAccountSubNetwork == "TARGET2":
                if swiftSettlement.IsTargetTwo():
                    retVal = counterPartyAccountSubNetwork
            elif counterPartyAccountSubNetwork == "EBA":
                if swiftSettlement.IsEba():
                    retVal = counterPartyAccountSubNetwork
            else:
                retVal = counterPartyAccountSubNetwork
    return retVal


def GetSwiftServiceCode(settlement):
    import FSwiftParameters as Global

    retVal = ''
    subNetwork = GetSubNetwork(settlement)
    if Global.SWIFT_SERVICE_CODE and subNetwork in Global.SWIFT_SERVICE_CODE:
        retVal = Global.SWIFT_SERVICE_CODE[subNetwork]
    return retVal


def GetBankingPriority(settlement):
    import FSwiftParameters as Global

    retVal = ''
    subNetwork = GetSubNetwork(settlement)
    if Global.BANKING_PRIORITY and subNetwork in Global.BANKING_PRIORITY:
        retVal = Global.BANKING_PRIORITY[subNetwork]
    return retVal


def GetDirection(settlement):
    '''Returns the direction for KMASTER.'''

    direction = 'PAY'
    if settlement.Amount() >= 0:
        direction = 'REC'

    return direction


def GetPartyType(settlement):
    '''Returns the value for party type.'''

    partyType = ''
    counterparty  = settlement.Counterparty()
    if counterparty:
        partyType = str(counterparty.Type())
    else:
        Utils.LogVerbose('No Counterparty Found')

    return partyType


def GetNetwork(settlement):
    return settlement.AcquirerAccountNetworkName()


def GetReceiverBic(settlement):
    '''Returns SWIFT bic code of settlement receiver.
    This field goes into {2:Application Header Block} -- Receiver Information.'''

    import FSwiftParameters as Global

    receiverBic = ''
    if Global.SWIFT_LOOPBACK:
        return Global.RECEIVER_BIC_LOOPBACK
    else:
        acquireAccount = settlement.AcquirerAccountRef()
        counterPartyAccount = settlement.CounterpartyAccountRef()
        if counterPartyAccount:
            if settlement.CounterpartyAccountSubNetworkName() in ('TARGET2', 'EBA'):
                if counterPartyAccount.Bic2():
                    receiverBic = counterPartyAccount.Bic2().Alias()
                elif counterPartyAccount.Bic():
                    receiverBic = counterPartyAccount.Bic().Alias()
        if receiverBic == '':
            if acquireAccount:
                if acquireAccount.Bic():
                    receiverBic = acquireAccount.Bic().Alias()

    return receiverBic


def GetSenderBic(settlement):
    '''Returns SWIFT bic code of the Acquirer of the settlement.
    This field goes into {1: Basic Header Block} -- Address of the Sender'''

    import FSwiftParameters as Global

    if Global.SWIFT_LOOPBACK:
        return Global.SENDER_BIC_LOOPBACK

    account = settlement.AcquirerAccountRef()
    if account:
        if account.NetworkAlias():
            return account.NetworkAlias().Alias()
    assert settlement.AcquirerAccountRef(), "The settlement has no acquirer account reference"
    assert settlement.AcquirerAccountRef().Party(), "The acquirer account referenced by the settlement has no party"
    return account.Party().Swift()


def GetSeqRef():
    '''SEQREF toghether with SEQNBR builds field 20, Senders reference '''

    import FSwiftParameters as Global

    ref = ''
    if Global.FAS:
        ref = Global.FAS
    return ref


def GetSwiftLoopback():
    import FSwiftParameters as Global

    return Global.SWIFT_LOOPBACK


def _is_valid_good_value_payment(settlement):
    """
    Check if the settlement meets the criteria for the
    backdated Good Value Payments
    """
    if settlement.RelationType() != RelationType.GOOD_VALUE:
        return False
    if settlement.MTMessages() != '103':
        return False
    if not settlement.Trade():
        return False
    if settlement.Trade().Instrument().InsType() != 'Deposit':
        return False
    if settlement.Type() != 'Fixed Amount':
        return False
    if settlement.Currency().Name() != 'ZAR':
        return False
    if settlement.Amount() < 0:
        return False
    if not settlement.CounterpartyAccountRef():
        return False
    if settlement.CounterpartyAccountRef().Bic().Name() not in ('ABSAZAJJ', 'ABSAZAJ0'):
        return False

    return True


def GetValueDate(settlement):
    """
    This together with interbank_settled_amount forms the
    mandatory field 32A in 103 and 202. Also it is a mandatory field 30 for 210.
    Returns the value day for settlement or Child Settlement for
    Pay Good Value Se
    """
    if _is_valid_good_value_payment(settlement):
        return settlement.CashFlow().PayDate()

    return settlement.ValueDay()


def IsNet(settlement):
    if settlement.RelationType() in (RelationType.AD_HOC_NET, RelationType.NET):
        return True
    return False


def GetLeastNetTrade(settlement):
    children = settlement.Children()
    children = [child for child in children if child.Trade() != None]

    if len(children) == 0:
        return None

    return min(children, key = lambda child: child.Trade().Oid())


def GetYourRef(setttlement):
    trade = setttlement.Trade()

    if IsNet(setttlement):
        trade = GetLeastNetTrade(setttlement)

    if trade != None:
        if trade.YourRef():
            return trade.YourRef()[:16]

    return 'NONREF'


def GetInterbankSettledAmount(settlement):
    ''' Mandatory field 32A '''

    assert settlement.Currency(), "Settlement has no currency"
    amount = settlement.Amount()
    curr = settlement.Currency().Name()
    amount = FSwiftUtils.ApplyCurrencyPrecision(curr, amount)
    return abs(amount)


def GetNarrative(settlement):
    ''' Mandatory field 79 '''
    
    narrative = 'Paying Good Value for settlement '

    if settlement.RelationType() == RelationType.ADJUSTED:
        if settlement.Children():
            settlement = settlement.Children()[0]

    if settlement.RelationType() == RelationType.GOOD_VALUE:
        if settlement.Children():
            settlement = settlement.Children()[0]

    oid = str(settlement.Oid())
    valueDay = str(settlement.ValueDay())
    curr = settlement.Currency().Name()
    amount = FSwiftUtils.ApplyCurrencyPrecision(curr, settlement.Amount())
    amount = str(amount)

    narrative += '%s dated %s and amount was %s %s' % (oid, valueDay, amount, curr)
    narrative = FSwiftUtils.SwiftNarrativeTextFormatter.Format(narrative)

    return narrative


def GetApplicableOption(option, account, bic):
    if option == 'A' and not account and not bic:
        return ''
    return option


def GetNationalClearingSystem(settlement):
    import FSwiftParameters as Global

    clearingSystem = ""
    account = settlement.CounterpartyAccountRef()
    if account:
        clearingSystemChlItem = account.NationalClearingSystemChlItem()
        if clearingSystemChlItem:
            clearingSystemFullName = clearingSystemChlItem.Name()
            if clearingSystemFullName in Global.NATIONAL_CLEARING_SYSTEM:
                clearingSystem = Global.NATIONAL_CLEARING_SYSTEM[clearingSystemFullName]
            else:
                Utils.LogVerbose("The value '%s' could not be found in parameter NATIONAL_CLEARING_SYSTEM." % clearingSystemFullName)
    return clearingSystem


def GetNationalClearingCode(settlement):
    clearingCode = ""
    account = settlement.CounterpartyAccountRef()
    if account:
        clearingCode = account.NationalClearingCode()
    return clearingCode
