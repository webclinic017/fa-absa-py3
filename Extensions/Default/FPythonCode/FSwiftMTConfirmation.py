""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/swift/etc/FSwiftMTConfirmation.py"
"""----------------------------------------------------------------------------
MODULE
    FSwiftMTConfirmation - Implements confirmation message functionality

    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

----------------------------------------------------------------------------"""

import acm
import xml.dom.minidom as dom
import FSwiftMTBase

from FSwiftMTBase import GetOptionValue, GetPartyFullName, GetPartyAddress, GetPartyBic
from FSettlementEnums import SettlementType
from FConfirmationEnums import ConfirmationType

sharedVariables = dict()

def Init(confirmation):
    #Note - Do not change order
    SetMoneyFlows(confirmation)

def SetMoneyFlows(confirmation):
    global sharedVariables
    sharedVariables.clear()
    calcSpace = None
    trade = confirmation.Trade()
    mt = GetSwiftMessageType(confirmation)
    resetCashFlow = ''
    if confirmation.Reset():
        resetCashFlow = confirmation.Reset().CashFlow()
    moneyflows = trade.MoneyFlows(None, None)
    for aMoneyFlow in moneyflows:
        if aMoneyFlow.Type() == SettlementType.REDEMPTION_AMOUNT and mt == 330:
            sharedVariables['moneyFlow'] = aMoneyFlow
        if resetCashFlow == aMoneyFlow.SourceObject() and mt == 362:
            sharedVariables['moneyFlow'] = aMoneyFlow
        elif aMoneyFlow.Type() in [SettlementType.PREMIUM, SettlementType.PREMIUM_2]:
            if not calcSpace:
                calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
                sharedVariables['calcSpace'] = calcSpace
            calcValue = aMoneyFlow.Calculation().Projected(calcSpace)
            if calcValue:
                amount = calcValue.Number()
                if acm.Operations.IsValueInfNanOrQNan(amount):
                    amount = 0
                if amount > 0:
                    sharedVariables['buyMoneyFlow'] = aMoneyFlow
                    sharedVariables['buyAmount'] = amount
                else:
                    sharedVariables['sellMoneyFlow'] = aMoneyFlow
                    sharedVariables['sellAmount'] = amount
                    
            if aMoneyFlow.Type() == SettlementType.PREMIUM:
                sharedVariables['moneyFlow'] = aMoneyFlow

def GetPartyAOption(confirmation):
    partyAOption = ''
    moneyFlow = sharedVariables.get('moneyFlow')
    if moneyFlow:
        partyAOption = GetOptionValue('PARTY_A', confirmation)
    return partyAOption

def GetPartyAAccount():
    partyAAccount = ''
    moneyFlow = sharedVariables.get('moneyFlow')
    if moneyFlow:
        acqaccount = moneyFlow.AcquirerAccount()
        if acqaccount:
            partyAAccount = acqaccount.Account()
    return partyAAccount

def GetPartyABic():
    partyABic = ''
    moneyFlow = sharedVariables.get('moneyFlow')
    if moneyFlow:            
        acqaccount = moneyFlow.AcquirerAccount()
        if acqaccount:
            partyABic = GetPartyBic(acqaccount)
    return partyABic

def GetPartyAName():
    partyAName = ''
    moneyFlow = sharedVariables.get('moneyFlow')
    if moneyFlow:
        partyAName = GetPartyFullName(moneyFlow.Acquirer())
    return partyAName

def GetPartyAAddress():
    partyAAddress = ''
    moneyFlow = sharedVariables.get('moneyFlow')
    if moneyFlow:
        partyAAddress = GetPartyAddress(moneyFlow.Acquirer())
    return partyAAddress

def GetPartyBOption(confirmation):
    partyBOption = ''
    moneyFlow = sharedVariables.get('moneyFlow')
    if moneyFlow:
        partyBOption = GetOptionValue('PARTY_B', confirmation)
    return partyBOption

def GetPartyBAccount():
    partyBAccount = ''
    moneyFlow = sharedVariables.get('moneyFlow')
    if moneyFlow:
        cpaccount = moneyFlow.CounterpartyAccount()
        if cpaccount:
            partyBAccount = cpaccount.Account()
    return partyBAccount

def GetPartyBBic():
    partyBBic = ''
    moneyFlow = sharedVariables.get('moneyFlow')
    if moneyFlow:
        cp = moneyFlow.Counterparty()
        if cp:
            partyBBic = cp.Swift()
        cpaccount = moneyFlow.CounterpartyAccount()
        if cpaccount:
            partyBBic = GetPartyBic(cpaccount)
    return partyBBic

def GetPartyBName():
    partyBName = ''
    moneyFlow = sharedVariables.get('moneyFlow')
    if moneyFlow:
        cp = moneyFlow.Counterparty()
        if cp:
            partyBName = GetPartyFullName(cp)
    return partyBName

def GetPartyBAddress():
    partyBAddress = ''
    moneyFlow = sharedVariables.get('moneyFlow')
    if moneyFlow:
        cp = moneyFlow.Counterparty()
        if cp:
            partyBAddress = GetPartyAddress(cp)
    return partyBAddress

def GetSwiftMessageType(confirmation):
    return FSwiftMTBase.GetSwiftMessageType(confirmation)

def GetNetwork(confirmation):
    network = ''
    if confirmation.ConfTemplateChlItem():
        if confirmation.ConfTemplateChlItem().Name() == 'SWIFT':
            network = confirmation.ConfTemplateChlItem().Name()
    return network

def GetReceiverBic(confirmation):
    '''Returns SWIFT bic code of settlement receiver.
    This field goes into {2:Application Header Block} -- Receiver Information.'''

    import FSwiftParameters as Global

    if Global.SWIFT_LOOPBACK:
        return Global.RECEIVER_BIC_LOOPBACK
    else:
        return confirmation.CounterpartyAddress()

def GetSenderBic(confirmation):
    '''Returns SWIFT bic code of the Acquirer of the settlement.
    This field goes into {1: Basic Header Block} -- Address of the Sender'''

    import FSwiftParameters as Global

    if Global.SWIFT_LOOPBACK:
        return Global.SENDER_BIC_LOOPBACK
    else:
        return confirmation.AcquirerAddress()

def GetSeqRef():
    '''SEQREF toghether with SEQNBR builds field 20, Senders reference '''

    import FSwiftParameters as Global
    
    ref = ''
    if Global.FAC:
        ref = Global.FAC
    return ref

def GetTradeDate(confirmation):
    assert confirmation.Trade(), "The confirmation has no trade reference"
    return confirmation.Trade().TradeTime()[:10]

def GetTypeOfOperation(confirmation):
    ''' Mandatory field 22A for all confirmations except MT 306. '''

    operation = 'NEWT'

    confTypes = {   ConfirmationType.RESEND:'NEWT',
                    ConfirmationType.AMENDMENT:'AMND',
                    ConfirmationType.CANCELLATION:'CANC',
                    ConfirmationType.CHASER:'DUPL'
                }

    if confirmation.Type() in confTypes:
        operation = confTypes[confirmation.Type()]

    return operation

def GetYourReference(confirmation):
    ''' Mandatory field 21 '''

    import FSwiftParameters as Global

    ref = ''
    refConf = None
    if confirmation.Type() in (ConfirmationType.AMENDMENT, ConfirmationType.CANCELLATION):
        refConf = confirmation.ConfirmationReference()
    elif confirmation.Type() in (ConfirmationType.CHASER):
        refConf = confirmation.ChasingConfirmation()

    if refConf and Global.FAC:
        ref = Global.FAC + '-' + str(refConf.Oid())

    return ref

def GetTagsFromOldSwiftBlock(confirmation):
    oldXml = ''
    oldSwiftTag = ''
    cancelledConf = confirmation.ConfirmationReference()
    opsDocuments = cancelledConf.Documents()
    if opsDocuments:
        oldXml = GetXmlFromOpsDocument(opsDocuments[0])
        if oldXml:
            oldSwiftTag = GetModifiedOldSwiftTag(oldXml)
    if not oldSwiftTag:
        oldSwiftTag = '<SWIFT>No applicable MT-message</SWIFT>'
    return oldSwiftTag

def GetXmlFromOpsDocument(opsDocument):
    xml = ''
    dataFromOpsDoc = opsDocument.Data()
    if dataFromOpsDoc:
        dataInZlibFormat = dataFromOpsDoc.decode('hex')
        xml = dataInZlibFormat.decode('zlib')
    return xml

def GetModifiedOldSwiftTag(oldXml):
    oldXml = dom.parseString(oldXml)
    oldSwiftTag = ''
    oldSwiftTags = oldXml.getElementsByTagName('SWIFT')
    if oldSwiftTags:
        oldSwiftTag = oldSwiftTags[0]
        tagsToBeDeleted = ['YOUR_REFERENCE', 'TYPE_OF_OPERATION']
        for aTag in tagsToBeDeleted:
            nodesToBeDeleted = oldSwiftTag.getElementsByTagName(aTag)
            if nodesToBeDeleted:
                nodeToBeDeleted = nodesToBeDeleted[0]
                nodeToBeDeleted.parentNode.removeChild(nodeToBeDeleted.previousSibling)
                nodeToBeDeleted.parentNode.removeChild(nodeToBeDeleted)
        oldSwiftTag = oldSwiftTag.toxml()
    return oldSwiftTag

def GetPartyInfo(option, account, bic, name, address):
    if option == 'J':
        return ('J', '', 'UKWN', '', '')

    conditionForOptionA = (option == 'A' and not bic)
    conditionForOptionD = (option == 'D' and (not name or not address))
    if conditionForOptionA or conditionForOptionD:
        return ('', '', '', '', '')

    return (option, account, bic, name, address)

