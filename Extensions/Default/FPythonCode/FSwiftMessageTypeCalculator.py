""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/swift/etc/FSwiftMessageTypeCalculator.py"
"""----------------------------------------------------------------------------
MODULE
    FSwiftMessageTypeCalculator - Module that calculates SWIFT message type of given entity

    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

----------------------------------------------------------------------------"""

import acm, traceback
from collections import defaultdict
from FSwiftConfirmationWrapper import FSwiftConfirmation
from FSwiftSettlementWrapper import FSwiftSettlement
from FSettlementEnums import RelationType, SettlementDeliveryType, SettlementType
from FSwiftServiceSelector import UseSwiftWriterForMT
from FSwiftExceptions import SwiftWriterAPIException

moduleConfirmationHookAdmin = None
moduleSettlementHookAdmin = None

#-------------------------------------------------------------------------
class SwiftMessageTypeDict(dict):

    #-------------------------------------------------------------------------
    def __init__(self, inputDict):
        super(SwiftMessageTypeDict, self).__init__(inputDict)
        self.__msgList = [0]

    #-------------------------------------------------------------------------
    def __getitem__(self, inputKey):

        for key in self.iterkeys():
            matched = True
            for keyItem, inputKeyItem in zip(key, inputKey):

                if keyItem.startswith('*'):
                    continue

                elif keyItem.startswith('<>'):
                    if not (keyItem.strip('<>') != inputKeyItem):
                        matched = False
                        break

                elif keyItem.startswith('<'):
                    if not(inputKeyItem < int(keyItem.strip('<')) ):
                        matched = False
                        break

                elif keyItem.startswith('>'):
                    if not(inputKeyItem > int(keyItem.strip('>')) ):
                        matched = False
                        break

                elif keyItem.startswith('('):
                    if inputKeyItem not in keyItem:
                        matched = False
                        break

                elif keyItem.startswith('<>('):
                    if inputKeyItem in keyItem:
                        matched = False
                        break

                elif keyItem != inputKeyItem:
                    matched = False
                    break

            if matched:
                self.__msgList.append(self.get(key))

        self.__msgList.sort(reverse = True)
        return self.__msgList[0]


# Add conditions required for a particular message type in respective dict and that message type will be implemented.
# <> -> Not Equal to
# <  -> Less than
# >  -> Greater than
# *  -> Any Value


settlementMessageDict = \
{  # Amount,        CPType,    BIC,       'Relation',                  'Status',      'TARGET2',    'EBA', 'NotifyReceipt', 'DeliveryType' , Trade Type

    ('<0',      'Client',      '*',              '*',                       '*',            '*',      '*',    '*', '<>Delivery versus Payment', '*'  ): 103,
    ('<0',      'Broker',  'False',              '*',                       '*',            '*',      '*',    '*', '<>Delivery versus Payment', '*'  ): 103,

    ('<0',      'Client',      '*',     'Good Value',  '<>Pending Cancellation',        'False',  'False',    '*', '<>Delivery versus Payment', '*'  ): 199,
    ('<0',      'Broker',  'False',     'Good Value',  '<>Pending Cancellation',        'False',  'False',    '*', '<>Delivery versus Payment', '*'  ): 199,

    ('<0',      'Client',      '*',   'Cancellation',                       '*',            '*',      '*',    '*', '<>Delivery versus Payment', '*'  ): 192,
    ('<0',      'Broker',  'False',   'Cancellation',                       '*',            '*',      '*',    '*', '<>Delivery versus Payment', '*'  ): 192,
    ('<0',      'Client',      '*',     'Good Value',    'Pending Cancellation',        'False',  'False',    '*', '<>Delivery versus Payment', '*'  ): 192,
    ('<0',      'Broker',  'False',     'Good Value',    'Pending Cancellation',        'False',  'False',    '*', '<>Delivery versus Payment', '*'  ): 192,

    ('<0',           '*',      '*',              '*',                       '*',            '*',      '*',    '*', '<>Delivery versus Payment', 'Account Transfer'  ): 200,
    ('<0', 'Counterparty',      '*',              '*',                       '*',            '*',      '*',    '*', '<>Delivery versus Payment', '*'  ): 202,
    ('<0',      'Broker',   'True',              '*',                       '*',            '*',      '*',    '*', '<>Delivery versus Payment', '*'  ): 202,


    ('>0',           '*',      '*', '<>Cancellation',                       '*',            '*',      '*', 'True',                         '*', '<>Account Adjustment'  ): 210,


    ('<0', 'Counterparty',      '*',   'Cancellation',                       '*',            '*',      '*',    '*', '<>Delivery versus Payment', '*'  ): 292,
    ('<0',      'Broker',   'True',   'Cancellation',                       '*',            '*',      '*',    '*', '<>Delivery versus Payment', '*'  ): 292,
    ('<0', 'Counterparty',      '*',     'Good Value',    'Pending Cancellation',        'False',  'False',    '*', '<>Delivery versus Payment', '*'  ): 292,
    ('<0',      'Broker',   'True',     'Good Value',    'Pending Cancellation',        'False',  'False',    '*', '<>Delivery versus Payment', '*'  ): 292,
    ('>0',           '*',      '*',   'Cancellation',                       '*',            '*',      '*', 'True',                         '*', '*'  ): 292,

    ('<0', 'Counterparty',      '*',     'Good Value',  '<>Pending Cancellation',        'False',  'False',    '*', '<>Delivery versus Payment', '*'  ): 299,
    ('<0',      'Broker',   'True',     'Good Value',  '<>Pending Cancellation',        'False',  'False',    '*', '<>Delivery versus Payment', '*'  ): 299,

}


confirmationMessageDict = \
{  # (Entitytype,           InstType,                        UnderInst,         ExoticType,     Digital,  ExerciseType,                  OpenEndStrip,  Reset,  ProdEntry )

     (  'Chaser',                '*',                              '*',                '*',         '*',           '*',                           '*',    '*',        '*' ): 395,

     ('<>Chaser',             'Curr',                              '*',                '*',         '*',           '*',                           '*',    '*',        '*' ): 300,

     ('<>Chaser',           'Option',                           'Curr', "(None,'','None')",     'False',  '<>Bermudan',                           '*',    '*',        '*' ): 305,

     ('<>Chaser',           'Option',                           'Curr',            'Other',         '*',           '*',                           '*',    '*',        '*' ): 306,
     ('<>Chaser',           'Option',                           'Curr',                '*',      'True',           '*',                           '*',    '*',        '*' ): 306,
     ('<>Chaser',           'Option',                           'Curr',                '*',         '*',    'Bermudan',                           '*',    '*',        '*' ): 306,


     ('<>Chaser',           'Deposit',                             '*',                '*',         '*',           '*',   "('Open End','Terminated')",    '*',        '*' ): 330,

     ('<>Chaser',           'Deposit',                             '*',                '*',         '*',           '*', "<>('Open End','Terminated')",    '*',        '*' ): 320,


     ('<>Chaser', "('Swap','CurrSwap','Cap','Floor')",             '*',                '*',         '*',           '*',                           '*', 'True',         '*'): 362,
     ('<>Chaser',                 '*',                             '*',                '*',         '*',           '*',                           '*', 'True',   'Collar' ): 362,
}

#-------------------------------------------------------------------------
def _HandleAdjustedSettlement(boEntity, messageType, TARGET2, EBA):

    if boEntity.RelationType() == RelationType.ADJUSTED:
        for eachSettlement in boEntity.Children():
            if eachSettlement.RelationType() == RelationType.GOOD_VALUE and not (TARGET2 or EBA):
                if messageType == 103:
                    return 199
                else:
                    return 299
    return messageType

#-------------------------------------------------------------------------
def _CalculateSettlementMessageType(boEntity):

    messageType = 0
    acquirerNetwork = boEntity.AcquirerAccountNetworkName()
    counterpartyNetwork = boEntity.CounterpartyAccountNetworkName()

    messageDict = defaultdict(lambda: 0, settlementMessageDict)
    messageDict = SwiftMessageTypeDict(messageDict)
    settlementIsSecurity = boEntity.IsSecurity()
    settlementDeliveryType = boEntity.DeliveryType()
    amount = boEntity.Amount()

    if settlementIsSecurity:
        if not boEntity.Type() == SettlementType.REDEMPTION_SECURITY:
            if settlementDeliveryType == SettlementDeliveryType.DELIVERY_FREE_OF_PAYMENT:
                if amount > 0:
                    messageType = 540
                else:
                    messageType = 542

            elif settlementDeliveryType == SettlementDeliveryType.DELIVERY_VERSUS_PAYMENT:
                if amount > 0:
                    messageType = 541
                else:
                    messageType = 543
            if not HaveValidAccountNetworks(acquirerNetwork, counterpartyNetwork, amount):
                messageType = 0
        return messageType

    counterPartyType = boEntity.GetCounterpartyType()
    accountBIC = bool(boEntity.GetAccountBic())
    notifyReceipt = boEntity.GetNotifyReceipt()
    relationType = boEntity.RelationType()
    status = boEntity.Status()
    settlementIsTARGET2 = boEntity.IsTargetTwo()
    settlementIsEBA = boEntity.IsEba()

    tradeType = ''
    trade = boEntity.Trade()
    if trade:
        tradeType = trade.Type()
    messageType = messageDict[(amount, counterPartyType, str(accountBIC), relationType, status, str(settlementIsTARGET2), str(settlementIsEBA), str(notifyReceipt), settlementDeliveryType, tradeType)]

    if messageType in (103, 202):
        messageType = _HandleAdjustedSettlement(boEntity, messageType, settlementIsTARGET2, settlementIsEBA)

    if not HaveValidAccountNetworks(acquirerNetwork, counterpartyNetwork, amount):
        messageType = 0

    return messageType

#-------------------------------------------------------------------------
def _CalculateConfirmationMessageType(boEntity):

    messageDict = defaultdict(lambda: 0, confirmationMessageDict)
    messageDict = SwiftMessageTypeDict(messageDict)
    entityType = boEntity.Type()
    instrumentType = boEntity.GetInsType()
    underlyingInstrType = boEntity.GetUnderlyingInstrType()
    exoticType = boEntity.GetExoticType()
    digital = boEntity.GetDigital()
    exerciseType = boEntity.GetExerciseType()
    openEndStrip = boEntity.GetOpenEnd()
    resetResnbr = bool(boEntity.Reset())
    productTypeChlnbrEntry = boEntity.GetProductTypeChlItem()
    messageType = messageDict[(entityType, instrumentType, underlyingInstrType, str(exoticType), str(digital), exerciseType, openEndStrip, str(resetResnbr), str(productTypeChlnbrEntry))]

    return messageType

#-------------------------------------------------------------------------
def GetConfirmationHookAdministratorModule():
    global moduleConfirmationHookAdmin
    if (None == moduleConfirmationHookAdmin):
        moduleConfirmationHookAdmin = __import__('FConfirmationHookAdministrator')
    return moduleConfirmationHookAdmin

#-------------------------------------------------------------------------
def GetSettlementHookAdministratorModule():
    global moduleSettlementHookAdmin
    if (None == moduleSettlementHookAdmin):
        moduleSettlementHookAdmin = __import__('FSettlementHookAdministrator')
    return moduleSettlementHookAdmin

#-------------------------------------------------------------------------
def CalculateMTOperations(fObject, checkIfSupported):

    result = 0

    if fObject.IsKindOf(acm.FSettlement):
        boEntity = FSwiftSettlement(fObject)
        messageType = _CalculateSettlementMessageType(boEntity)
        settlementHookAdminModule = GetSettlementHookAdministratorModule()
        hookAdmin = settlementHookAdminModule.GetHookAdministrator()
        settlementHooks = settlementHookAdminModule.SettlementHooks
        messageTypeFromHook = hookAdmin.HA_CallHook(settlementHooks.GET_MT_MESSAGE, fObject, str(messageType))
        if messageTypeFromHook == str(messageType) and checkIfSupported and not isSupported(messageType):
            return result
        messageType = messageTypeFromHook
        result = int(messageType)

    elif fObject.IsKindOf(acm.FConfirmation):
        boEntity = FSwiftConfirmation(fObject)
        messageType = _CalculateConfirmationMessageType(boEntity)
        confirmationHookAdminModule = GetConfirmationHookAdministratorModule()
        hookAdmin = confirmationHookAdminModule.GetConfirmationHookAdministrator()
        confirmationHooks = confirmationHookAdminModule.ConfirmationHooks
        messageTypeFromHook = hookAdmin.HA_CallHook(confirmationHooks.GET_MT_MESSAGE, fObject, str(messageType))
        if messageTypeFromHook == str(messageType) and checkIfSupported and not isSupported(messageType):
            return result
        messageType = messageTypeFromHook
        result = int(messageType)

    return result

#-------------------------------------------------------------------------
def CalculateMTSwiftWriter(fObject, checkIfSupported):
    messageType = 0
    try:
        import FSwiftWriterAPIs

        swiftWriterMT = FSwiftWriterAPIs.get_swift_mt_type(fObject)

        if swiftWriterMT and checkIfSupported and not FSwiftWriterAPIs.is_outgoing_message_generation_on_for('MT{}'.format(swiftWriterMT)):
            swiftWriterMT = 0

        messageType = swiftWriterMT

    except Exception as exception:
        raise SwiftWriterAPIException("Exception when calculating SwiftWriter MT: {}. \n{}".format(exception, traceback.format_exc()))

    return messageType

#-------------------------------------------------------------------------
def Calculate(fObject, checkIfSupported = True):
    return CalculateMTSwiftWriter(fObject, checkIfSupported) if UseSwiftWriterForMT(fObject) else CalculateMTOperations(fObject, checkIfSupported)

#-------------------------------------------------------------------------
def HaveValidAccountNetworks(acquirerNetwork, counterpartyNetwork, amount):
    validNetworks = False
    if acquirerNetwork == "SWIFT":
        if amount < 0.0:
            if counterpartyNetwork == "SWIFT":
                validNetworks = True
        else:
            validNetworks = True
    return validNetworks

#-------------------------------------------------------------------------
def isSupported(mt):
    import FSwiftParameters as Global

    mt = int(mt)
    usedMessages = Global.USED_MT_MESSAGES_SETTLEMENT + Global.USED_MT_MESSAGES_CONFIRMATION
    usedMessages = dict(usedMessages)

    status = usedMessages.get(mt, '')

    if status == 'Yes':
        return True

    return False

