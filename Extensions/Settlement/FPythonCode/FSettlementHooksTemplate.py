""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementHooksTemplate.py"
"""----------------------------------------------------------------------------
MODULE: FSettlementHooksTemplate

DESCRIPTION: This module contains functions called by the core settlement
             scripts. It should NEVER be edited. All functions in
             FSettlementHooksTemplate can be overridden in a module of your
             own choice. To do so, simply create a module in the Python editor
             and copy the function declaration of the function you want to
             override into it. Then you implement the function as desired
             in this module. You might need to import acm when implementing
             your hook. See how the default implementation is done in this
             module to see what inputs and outputs are needed.

             Do not copy the declarations of the functions you do not want to
             override into your hook modules. Remember that the return types
             and the input parameters has to be the same in your hook as in
             FSettlementHooksTemplate.

             Save your module and register it in FSettlementParameters. To do
             so add a CustomHook-object into the list named hooks in
             FSettlementParameters. For example, if you have overridden
             the function GetNetAmount in a module called MyHooks, you would
             add a CustomHook-object like this:
             hooks = [CustomHook('MyHooks', 'GetNetAmount')]

             To add another hook for GetDaysForward you would add another
             CustomHook-object into the list hooks:
             hooks = [CustomHook('MyHooks', 'GetNetAmount'),
                      CustomHook('MyHooks', 'GetDaysForward')
                      ]

             The input parameters to a CustomHook-object has to be strings.
             The first string is the name of the module, the second the name
             of the hook.

             Once the hooks have been implemented and registered in
             FSettlementParameters, the affected Arena Task Servers have to be
             restarted in order to get the desired functionality.

             (c) Copyright 2008 SunGard FRONT ARENA . All rights reserved.
----------------------------------------------------------------------------"""
import acm

from FSettlementEnums import RelationType

def GetNetAmount(netChildrenList, netType):
    """
    DESCRIPTION: A function that calculates the net amount
    INPUT:       A list of FSettlements to be netted. Treat settlements as
                 read-only.
                 A string with the relation type describing the type of netting.
    OUTPUT:      A net amount
    """

    netAmount = 0.0
    for settlement in netChildrenList:
        if netType == RelationType.SECURITIES_DVP_NET:
            if settlement.IsSecurity():
                netAmount = netAmount + settlement.Amount()
        else:
            netAmount = netAmount + settlement.Amount()
    return netAmount

def GetDaysForward(settlement):
    """
    DESCRIPTION:   A function that determines the number of days forward
                   for settlement processing.
    INPUT:         An FSettlement. Treat entity as read-only.
    OUTPUT:        An integer
    OVERRIDE NOTE: When overriding GetDaysForward, remember to set parameter
                   maximumDaysForward in FSettlementParameters to the
                   maximum possible value that can be returned from the
                   overriding implementation.
    """
    import FSettlementParameters as SettlementParameters

    daysForward = SettlementParameters.maximumDaysForward
    return daysForward

def GetDaysBack(settlement):
    """
    DESCRIPTION:   A function that determines the number of days back
                   for settlement processing.
    INPUT:         An FSettlement. Treat entity as read-only.
    OUTPUT:        An integer
    OVERRIDE NOTE: When overriding GetDaysBack, remember to set parameter
                   maximumDaysBack in FSettlementParameters to the
                   maximum possible value that can be returned from the
                   overriding implementation.
    """
    import FSettlementParameters as SettlementParameters

    daysBack = SettlementParameters.maximumDaysBack
    return daysBack

def CompareSettlementAmounts(settlement1, settlement2):
    """
    DESCRIPTION: This function is used when comparing two settlement amounts.
                 The function should return true if the amounts of the two settlements
                 are considered as equal.
    INPUT:       Two FSettlements. Treat entities as read-only.
    OUTPUT:      A Boolean
    """

    return (abs(settlement1.Amount() - settlement2.Amount())) < 10e-6


def GetNotificationDay(settlement):
    """
    DESCRIPTION: This function should return the date value that NotificationDay
                 should be set to when creating or updating a settlement.
    INPUT:       An FSettlement. Treat entity as read-only.
    OUTPUT:      A  string representing a date.
    """
    return ''

def SettlementModification(settlement, netChildrenList):
    """
    DESCRIPTION: This function enables modification of a settlement record.
                 It is only allowed to change the input settlement record, NOT any
                 records referencing it or being referenced by it. Commits are
                 NOT allowed in function SettlementModification.
                 This function should be used on own risk!

    INPUT:       A FSettlement that is eligible for modification.
                 A list containing the net children. This list and its data is read only.
                 If the first argument is not a net the netChildrenList will be None i.e.
                 the implementation of the hook must support a None value for netChildrenList.

    OUTPUT:      A string. The string will be entered as a diary note on the settlement.
    """
    return ""

def ExcludeTrade(trade):
    """
    DESCRIPTION: This function is used for the purposes of preventing trades from
                 being processed for settlement creation.

    INPUT:       An FTrade. Treat entity as read-only.
    OUTPUT:      A Boolean.
    """
    return False


def GetMTMessage(settlement, MTMessage):
    """
    DESCRIPTION: This function return the number the SWIFT message that should
                 be created for a settlement.
    INPUT:       An FSettlement. Treat input as read-only.
                 The MT message (as string) that the core think should be created.
    OUTPUT:      A MT Message type represented as a string.
    """
    return MTMessage

def SplitSettlement(settlement):
    """
    DESCRIPTION: This function returns a list of Python tuples. The tuple values
                 are used for automatic split of settlement records.
    INPUT:       An FSettlement. Treat input as read-only.
    OUTPUT:      A list containing the split configurations. See FCA 2105, section
                 FSettlementHooksTemplate, for data preparation and hook implementation.
    """
    return list()

def ConfirmationEvent(confirmation):
    """
    DESCRIPTION: This function is called when a confirmation is updated.
    INPUT:       A FConfirmation that has been updated or created.
    OUTPUT:      None.
    """
    pass

def UpdateSettlementBusinessProcess(oldSettlement, newSettlement):
    """
    DESCRIPTION: This function is used for deciding if a change between an old
                 and a new settlement should trigger an update on the settlement
                 business process.
    INPUT:       The old settlement and the new settlement that has been updated.
    OUTPUT:      A Boolean.
    """
    return True

def DecideSettlementsToPairOff(settlementsEligibleForPairOffTomorrow):
    """
    DESCRIPTION: This function is used for deciding which settlements to 
                 automatically pair off among all eligible settlements found in 
                 FSettlementAutomaticRepoProcessing script.
    INPUT:       A set of all settlements eligible for pair off.
    OUTPUT:      A list of all settlements that should be pair off:ed.
    """
    shouldBePairedOff = list()
    sellSettlements = list()
    buySettlements = list()
    totalSellAmount = 0
    totalBuyAmount = 0
    for settlement in settlementsEligibleForPairOffTomorrow:
        if settlement.Amount() < 0:
            sellSettlements.append(settlement)
            totalSellAmount += settlement.Amount()
        else:            
            buySettlements.append(settlement)
            totalBuyAmount += settlement.Amount()
    if totalSellAmount == 0 or totalBuyAmount == 0:
        return shouldBePairedOff
    if totalSellAmount + totalBuyAmount == 0:
        shouldBePairedOff.extend(sellSettlements)
        shouldBePairedOff.extend(buySettlements)
    elif totalSellAmount + totalBuyAmount < 0:
        shouldBePairedOff.extend(buySettlements)
        shouldBePairedOff.extend(__AddSettlements(sorted(sellSettlements, key=lambda s: s.Amount(), reverse=True), totalBuyAmount))
    else:
        shouldBePairedOff.extend(sellSettlements)
        shouldBePairedOff.extend(__AddSettlements(sorted(buySettlements, key=lambda s: s.Amount()), totalSellAmount))
    return shouldBePairedOff

def __AddSettlements(sortedSettlements, totalAmount):
    shouldBePairedOff = list()
    currentTotalAmount = 0
    for settlement in sortedSettlements:
        shouldBePairedOff.append(settlement)
        currentTotalAmount += settlement.Amount()
        if abs(currentTotalAmount) >= abs(totalAmount):
            break

    realShouldBePairedOff = list()
    for settlement in reversed(shouldBePairedOff):
        if abs(settlement.Amount()) <= abs(abs(currentTotalAmount) - abs(totalAmount)):
            currentTotalAmount -= settlement.Amount()
        else:
            realShouldBePairedOff.append(settlement)
    return realShouldBePairedOff