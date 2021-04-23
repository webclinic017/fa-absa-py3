""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementGetters.py"
import acm
import FOperationsUtils as OperationsUtils
import FSettlementUtils as SettlementUtils
from   FSettlementCorrectTradeHandler import CorrectTradeHandler
import FSettlementValidations as Validations
from FSettlementEnums import SettlementStatus, SettlementType, RelationType
import FSettlementStatusQueries as Queries
import FSettlementCreatorSingleton
import FSettlementModificationInspectorSingleton
import FSettlementUpdaterSingleton
import FSettlementRecallHandlerSingleton
from   FSettlementCommitter import SettlementCommitter, CommitAction
import FSettlementMatcher as Matcher

#-------------------------------------------------------------------------
# Settlement getter functions - used by FSettlementSecurityProcessEngine and FSettlementSecurityUpdateEngine
#-------------------------------------------------------------------------

#-------------------------------------------------------------------------
def GetSiblingPartialSettlement(cancellationSettlement):
    siblingPartialSettlement = None
    if cancellationSettlement and cancellationSettlement.Children():
        partialSettlement = cancellationSettlement.Children().First()
        if partialSettlement and partialSettlement.PartialParent():
            partialSiblingList = [x for x in partialSettlement.PartialParent().PartialChildren() if x.Oid() != partialSettlement.Oid()]
            if len(partialSiblingList):
                siblingPartialSettlement = partialSiblingList[0]
    return siblingPartialSettlement

#-------------------------------------------------------------------------
def GetSettlementsInPendingAmendment(trade):
    settlements = list()
    for settlement in trade.Settlements():
        settlement = settlement.GetTopNonCancellationSettlementInHierarchy()
        if not (settlement.PartialParent() or settlement.PairOffParent()):
            continue
        if settlement.PartialParent() and not Validations.AllPartialPartsApplicableForSettlmentProcess(settlement.PartialParent()):
            return list()
        if settlement.Status() == SettlementStatus.PENDING_AMENDMENT:
            settlements.append(settlement)
    return settlements

#-------------------------------------------------------------------------
def GetPartialParent(settlement):
    partialParent = None
    if settlement.PartialChildren():
        partialParent = settlement
    elif settlement.PartialParent():
        partialParent = settlement.PartialParent()
    elif settlement.GetTopNonCancellationSettlementInHierarchy().PartialChildren():
        partialParent = settlement.GetTopNonCancellationSettlementInHierarchy()
    elif settlement.GetTopNonCancellationSettlementInHierarchy().PartialParent():
        partialParent = settlement.GetTopNonCancellationSettlementInHierarchy().PartialParent()
    return partialParent

#-------------------------------------------------------------------------
def GetPairOffParent(settlement):
    pairOffParent = None
    if settlement.PairOffChildren():
        pairOffParent = settlement
    elif settlement.PairOffParent():
        pairOffParent = settlement.PairOffParent()
    elif settlement.GetTopNonCancellationSettlementInHierarchy().PairOffChildren():
        pairOffParent = settlement.GetTopNonCancellationSettlementInHierarchy()
    elif settlement.GetTopNonCancellationSettlementInHierarchy().PairOffParent():
        pairOffParent = settlement.GetTopNonCancellationSettlementInHierarchy().PairOffParent()
    return pairOffParent

#-------------------------------------------------------------------------
def GetSettlementTransferTypeFromSettlementType(settlementType):
    return {
        SettlementType.COUPON : SettlementType.COUPON_TRANSFER,
        SettlementType.DIVIDEND : SettlementType.DIVIDEND_TRANSFER,
        SettlementType.FIXED_AMOUNT : SettlementType.FIXED_AMOUNT_TRANSFER,
        SettlementType.CAPLET : SettlementType.CAPLET_TRANSFER,
        SettlementType.FLOORLET : SettlementType.FLOORLET_TRANSFER,
        SettlementType.DIGITAL_FLOORLET : SettlementType.FLOORLET_TRANSFER,
        SettlementType.DIGITAL_CAPLET : SettlementType.CAPLET_TRANSFER,
        SettlementType.REDEMPTION : SettlementType.FIXED_AMOUNT_TRANSFER
    }.get(settlementType, SettlementType.NONE)

#-------------------------------------------------------------------------
def GetBottomMostChildren(settlement, children):
    if settlement.RelationType() != RelationType.NONE and settlement.NumberOfChildren():
        for child in settlement.Children():
            GetBottomMostChildren(child, children)
    else:
        children.append(settlement)

#-------------------------------------------------------------------------
def GetSecurityTypes(settlement, trade):
    securityTypes = set()
    topMost = settlement.GetTopSettlementInHierarchy()
    children = list()
    GetBottomMostChildren(topMost, children)
    for child in children:
        if child.Trade() == trade and child.IsSecurity():
            securityTypes.add(child.Type())
    return securityTypes

#-------------------------------------------------------------------------
def GetAllCashChildrenWithTrade(parent, trade):
    childrenWithTrade = list()
    allChildren = list()
    GetBottomMostChildren(parent, allChildren)
    for child in allChildren:
        if not child.IsSecurity() and child.Trade() == trade:
            childrenWithTrade.append(child)
    return childrenWithTrade

#-------------------------------------------------------------------------
def GetSettlementWithAmount(settlements, amount):
    for settlement in settlements:
        if abs(settlement.Amount() - amount) < 10e-6:
            return settlement
    return None

#-------------------------------------------------------------------------
def AllPartialChildren(partialParent):
    allChildren = list()
    for partialChild in partialParent.PartialChildren():
        if partialChild.PartialChildren():
            allChildren.extend(AllPartialChildren(partialChild))
        else:
            allChildren.append(partialChild)
    return allChildren

#-------------------------------------------------------------------------
def FindTopmostPartialParent(settlement):
    if settlement.PartialParent():
        return FindTopmostPartialParent(settlement.PartialParent())
    else:
        return settlement

#-------------------------------------------------------------------------
def TotalSettledAmount(settlements):
    totalSettledAmount = 0
    for settlement in settlements:
        if settlement.IsSettled():
            totalSettledAmount += settlement.Amount()
    return totalSettledAmount

#-------------------------------------------------------------------------
def GetAllChildrenInHierarchy(parent, childrenInHierarchy):
    for child in parent.Children():
        GetAllChildrenInHierarchy(child, childrenInHierarchy)
        childrenInHierarchy.append(child)
#-------------------------------------------------------------------------
def GetSettlementCommitterList(settlemenProcessData, trade, settlementCorrectTradeRecaller):

    modInspector = FSettlementModificationInspectorSingleton.GetModInspector()
    updater = FSettlementUpdaterSingleton.GetSettlementUpdater()
    settlementCommitterList = []
    tradesWaitingForCancellationAck = set()

    for (old, new) in settlemenProcessData.GetSettlementList():
        if new:
            if new.Trade() in tradesWaitingForCancellationAck or Validations.WaitingForCancellationAck(new, settlemenProcessData.GetSettlementList()):
                new.Status(SettlementStatus.AWAITING_CANCELLATION)
                tradesWaitingForCancellationAck.add(new.Trade())
            if new.IsValidForSTP():
                new.STP()
            stateChart = acm.Operations.GetMappedSettlementProcessStateChart(new)
            new.StateChart(stateChart)
        for sc in GetSettlementCommitters(old, new, modInspector, updater):
            if sc.GetSettlement().IsValidForSTP():
                sc.GetSettlement().STP()
            settlementCommitterList.append(sc)
    if OperationsUtils.IsCorrectingTrade(trade):
        settlementCommitterList = settlementCommitterList + settlementCorrectTradeRecaller.RecallSettlementIfApplicable(trade)
    return settlementCommitterList

#-------------------------------------------------------------------------
def GetSettlementCommitters(oldSettlement, newSettlement, modInspector, settlementUpdater):
    returnList = []
    if oldSettlement and newSettlement:
        if modInspector.IsModified(oldSettlement, newSettlement):
            returnList = settlementUpdater.UpdateSettlements(oldSettlement, newSettlement)
    elif (not oldSettlement) and (newSettlement):
        returnList.append(SettlementCommitter(newSettlement, CommitAction.INSERT))
    elif (oldSettlement) and (not newSettlement):
        settlementRecallHandler = FSettlementRecallHandlerSingleton.GetSettlementRecallHandler()
        returnList = settlementRecallHandler.ProcessRecall(oldSettlement)
    else:
        OperationsUtils.LogVerbose('Unknown event in GetSettlementCommitters')
    return returnList

#-------------------------------------------------------------------------
def GetMatchedSettlementPairs(oldSettlements, trade, settlementCorrectTradeRecaller):
    newSettlements = FSettlementCreatorSingleton.GetSettlementCreator().CreateSettlements(trade, settlementCorrectTradeRecaller)
    newSettlements = SettlementUtils.MergeSameSourceSettlements(trade, newSettlements)
    matcher = Matcher.SettlementMatcher(oldSettlements, newSettlements)
    return matcher.GetMatchedSettlementsList()

#-------------------------------------------------------------------------
def GetSettlementCommitterListInsertOnly(newSettlements, dummySettlementCorrectTradeRecaller):
    settlementCommitterList = []

    for settlement in newSettlements:
        if settlement:
            if settlement.IsValidForSTP():
                settlement.STP()
            stateChart = acm.Operations.GetMappedSettlementProcessStateChart(settlement)
            settlement.StateChart(stateChart)
            if settlement.IsValidForSTP():
                settlement.STP()
            settlementCommitterList.append(SettlementCommitter(settlement, CommitAction.INSERT))
    return settlementCommitterList

#-------------------------------------------------------------------------
def GetTopPartialParentInPartialHierarchy(partialParent):
    if partialParent.PartialParent():
        return GetTopPartialParentInPartialHierarchy(partialParent.PartialParent())
    else:
        return partialParent