""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementNetting.py"
"""----------------------------------------------------------------------------
MODULE
    FOperationsNetting - Module for performing settlement netting.

    (c) Copyright 2008 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

----------------------------------------------------------------------------"""
import acm
import FOperationsUtils as Utils
import FSettlementUtils as SettlementUtils
import FSettlementSetters as Setters
import FSettlementStatusQueries as Queries
from FSettlementCommitter import CommitAction, SettlementCommitter
import FSettlementNetCandidatesFinderSingleton as Singleton
from FSettlementHookAdministrator import SettlementHooks, GetHookAdministrator
from FSettlementHierarchy import HierarchyTree
from FSettlementCreator import SettlementCreator
from FSettlementEnums import RelationType, NettingRuleType, SettlementStatus, PartialSettlementType, SettlementType, SettlementDeliveryType

CHANGE_TO_SOURCE_DATA = 0
RECALLED_DATA = 1

def GetDefaultPartialSettlementType():
    import FSettlementParameters as Params
    return Params.defaultPartialSettlementType

def GetNetAmount(netChildrenList, netType):

    hookAdmin = GetHookAdministrator()
    return hookAdmin.HA_CallHook(SettlementHooks.GET_NET_AMOUNT, netChildrenList, netType)


def GetNotificationDay(netParent):

    hookAdmin = GetHookAdministrator()
    return hookAdmin.HA_CallHook(SettlementHooks.GET_NOTIFICATION_DATE, netParent)

def NetParentModification(netParent, netChildrenList):

    SettlementCreator.ApplyClientModification(netParent, netChildrenList)

def SetNetParentPortfolio(netParent, netChildrenList):

    netChild = netChildrenList[0]
    portfolio = None
    if netChild.ToPortfolio():
        portfolio = netChild.ToPortfolio()
    elif netChild.FromPortfolio():
        portfolio = netChild.FromPortfolio()
    if portfolio:
        for netChild in netChildrenList:
            if netChild.ToPortfolio() and netChild.ToPortfolio().Oid() != portfolio.Oid():
                portfolio = None
                break
            elif netChild.FromPortfolio() and netChild.FromPortfolio().Oid() != portfolio.Oid():
                portfolio = None
                break
    netParent.ToPortfolio(portfolio)
    netParent.FromPortfolio(portfolio)

def IsSameTradeAmongNetChildren(netChildrenList):

    isSameTradeAmongNetChildren = True
    oid = netChildrenList[0].Trade().Oid()
    for netChild in netChildrenList:
        if oid != netChild.Trade().Oid():
            isSameTradeAmongNetChildren = False
            break
    return isSameTradeAmongNetChildren

def SetNetParentTypes(netParent, netChildrenList):
    SetNetParentType(netParent, netChildrenList)
    SetNetParentSplitType(netParent, netChildrenList)
    SetNetParentDeliveryType(netParent, netChildrenList)

def SetNetParentType(netParent, netChildrenList):
    netParentType = SettlementType.NONE
    if netParent.RelationType() == RelationType.SECURITIES_DVP_NET:
        netParentType = SettlementType.SECURITY_DVP
    else:
        firstChildType = netChildrenList[0].Type()
        allChildrenHaveSameType = True
        for netChild in netChildrenList[1:]:
            if firstChildType != netChild.Type():
                allChildrenHaveSameType = False
                break
        if allChildrenHaveSameType:
            netParentType = firstChildType
    netParent.Type(netParentType)

def SetNetParentSplitType(netParent, netChildrenList):
    netParentSplitType = None
    firstChildSplitType = netChildrenList[0].SplitTypeChlItem()
    allChildrenHaveSameSplitType = True
    for netChild in netChildrenList[1:]:
        if firstChildSplitType != netChild.SplitTypeChlItem():
            allChildrenHaveSameSplitType = False
            break
    if allChildrenHaveSameSplitType:
        netParentSplitType = firstChildSplitType
    netParent.SplitTypeChlItem(netParentSplitType)

def SetNetParentDeliveryType(netParent, netChildrenList):
    netParentDeliveryType = netChildrenList[0].DeliveryType()
    for netChild in netChildrenList[1:]:
        if netChild.DeliveryType() != netParentDeliveryType:
            netParentDeliveryType = SettlementDeliveryType.NONE
            break
    netParent.DeliveryType(netParentDeliveryType)

def SetNetParentData(netParent, netChildrenList, nettingRule):

    oldNetParent = netParent.Clone()
    oldNetParent.RegisterInStorage()
    netParent.Amount(GetNetAmount(netChildrenList, netParent.RelationType()))
    netChild = __GetBestMatchingChild(netParent, netChildrenList)
    SetNetParentPortfolio(netParent, netChildrenList)
    netParent.Currency(netChild.Currency())

    netParent.Acquirer(netChild.Acquirer())
    netParent.AcquirerName(netChild.AcquirerName())
    netParent.Counterparty(netChild.Counterparty())
    netParent.CounterpartyName(netChild.CounterpartyName())

    if netParent.RelationType() != RelationType.AD_HOC_NET and not __ManuallyNettedSecurity(netParent, nettingRule):
        netParent.RelationType(__GetRelationTypeString(netChild, nettingRule))
    if netParent.RelationType() in [RelationType.NET, RelationType.CLOSE_TRADE_NET, RelationType.SECURITIES_DVP_NET]:
        netParent.NettingRule(nettingRule)
    elif netParent.RelationType() == RelationType.COUPON_NET:
        netParent.CashFlow(netChild.CashFlow())
    else:
        netParent.NettingRule(None)
    netParent.ValueDay(netChild.ValueDay())
    if IsSameTradeAmongNetChildren(netChildrenList):
        netParent.Trade(netChild.Trade())
    else:
        netParent.Trade(None)

    netParent.SecurityInstrument(None)
    
    if netParent.RelationType() in [RelationType.DIVIDEND_NET, RelationType.COUPON_NET, RelationType.REDEMPTION_NET]\
        or (__AllChildrenShareInstrument(netChildrenList)):
        if netChild.Instrument().Underlying():
            netParent.SecurityInstrument(netChild.Instrument().Underlying())
        else:
            netParent.SecurityInstrument(netChild.Instrument())
    else:
        if netParent.IsSecurity() and __AllChildrenShareUnderlyingInstrument(netChildrenList):
            netParent.SecurityInstrument(netChild.Instrument().Underlying())
    
    if not netParent.SecurityInstrument() and __AllChildrenShareSecurityInstrument(netChildrenList):
        netParent.SecurityInstrument(netChild.SecurityInstrument())

    netParent.AcquirerAccountRef(netChild.AcquirerAccountRef())
    netParent.CounterpartyAccountRef(netChild.CounterpartyAccountRef())

    netParent.Protection(netChild.Protection())

    netParent.Owner(netChild.Owner())
    if netParent.IsValidForSTP():   #this stp makes the mapping for the net parent correct
        netParent.STP()             #stp will be run again in the transaction committer
    NetParentModification(netParent, netChildrenList)
    stateChart = acm.Operations.GetMappedSettlementProcessStateChart(netParent)
    netParent.StateChart(stateChart)
    netParent.NotificationDay(GetNotificationDay(netParent))

    netParent.PartialSettlementType(__GetPartialSettlementType(netParent, netChildrenList))

    hookAdmin = GetHookAdministrator()
    updateProcess = hookAdmin.HA_CallHook(SettlementHooks.UPDATE_SETTLEMENT_BUSINESS_PROCESS, oldNetParent, netParent)

    return updateProcess

def  __ManuallyNettedSecurity(netParent, nettingRule):
    return netParent.IsSecurity() and not nettingRule

def __GetBestMatchingChild(netParent, netChildrenList):
    bestMatch = None
    positiveNetParentAmount = netParent.Amount() >= 0.0
    for netChild in netChildrenList:
        if (netParent.IsSecurity() and netChild.IsSecurity()) or \
           (not netParent.IsSecurity() and not netChild.IsSecurity()):
            if netChild.Amount() >= 0.0 and positiveNetParentAmount or\
            netChild.Amount() < 0.0 and not positiveNetParentAmount:
                bestMatch = netChild
                break

    if not bestMatch:
        bestMatch = netChildrenList[-1] #fall back on last child
    return bestMatch

def __AllChildrenShareInstrument(netChildrenList):
    instrument = netChildrenList[0].Instrument()
    for child in netChildrenList:
        if child.Instrument() != instrument:
            return False
    return True

def __AllChildrenShareUnderlyingInstrument(netChildrenList):
    underlyingInstrument = netChildrenList[0].Instrument().Underlying()
    for child in netChildrenList:
        if child.Instrument().Underlying() != underlyingInstrument:
            return False
    return True

def __AllChildrenShareSecurityInstrument(netChildrenList):
    securityInstrument = netChildrenList[0].SecurityInstrument()
    for child in netChildrenList:
        if child.SecurityInstrument() != securityInstrument:
            return False
    return True

def __GetPartialSettlementType(netParent, netChildrenList):
    partialSettlementType = PartialSettlementType.NONE
    if netParent.IsSecurity():
        missmatch = False
        foundSecurity = False
        for child in netChildrenList:
            if child.IsSecurity():
                if child.PartialSettlementType() == PartialSettlementType.NPAR:
                    return PartialSettlementType.NPAR
                if not foundSecurity:
                    partialSettlementType = child.PartialSettlementType()
                    foundSecurity = True
                if child.PartialSettlementType() != partialSettlementType:
                    missmatch = True
        if missmatch:
            partialSettlementType = GetDefaultPartialSettlementType()

    return partialSettlementType

def IsCloseTradeNetPart(settlement):

    isCloseTradeNetPart = False
    trade = settlement.Trade()

    if trade == None:
        return isCloseTradeNetPart
    if SettlementUtils.IsClosingTrade(trade):
        closedTrade = acm.FTrade[trade.ContractTrdnbr()]
        query = Queries.GetRecallStatusesQuery()
        if not query.IsSatisfiedBy(closedTrade):
            isCloseTradeNetPart = True
        return isCloseTradeNetPart
    closingTrades = SettlementUtils.GetClosingTrades(trade)
    if len(closingTrades):
        query = Queries.GetRecallStatusesQuery()
        for closingTrade in closingTrades:
            if not query.IsSatisfiedBy(closingTrade):
                isCloseTradeNetPart = True
                break
        return isCloseTradeNetPart
    return isCloseTradeNetPart

def __GetRelationTypeString(settlement, nettingRule):
    import FSettlementParameters as Params

    settlementType = settlement.Type()
    reftypeString = RelationType.NET
    if  settlementType == SettlementType.COUPON and settlementType not in Params.preventAutomaticNetting:
        reftypeString = RelationType.COUPON_NET
    elif settlementType == SettlementType.REDEMPTION and settlementType not in Params.preventAutomaticNetting:
        reftypeString = RelationType.REDEMPTION_NET
    elif settlementType == SettlementType.DIVIDEND and settlementType not in Params.preventAutomaticNetting:
        reftypeString = RelationType.DIVIDEND_NET
    elif nettingRule.NettingRuleType() == NettingRuleType.CLOSE_TRADE_NET:
        reftypeString = RelationType.CLOSE_TRADE_NET
    elif nettingRule.NettingRuleType() == NettingRuleType.SECURITIES_DVP_NET:
        reftypeString = RelationType.SECURITIES_DVP_NET
    return reftypeString

def __CreateNetParent(netChildrenList, nettingRule):

    netChild = netChildrenList[len(netChildrenList)-1]
    netParent = acm.FSettlement()
    netParent.RegisterInStorage()
    netParent.Status(SettlementStatus.NEW)
    netParent.RelationType(__GetRelationTypeString(netChild, nettingRule))
    SetNetParentTypes(netParent, netChildrenList)
    SetNetParentData(netParent, netChildrenList, nettingRule)
    return netParent

def __UpdateSettleSettlement(netParent, netHierarchyList, statusExplanation):
    settlement = netParent.Parent()
    if settlement: #We might have manually adjusted the net parent.
        if settlement.Status() == SettlementStatus.CLOSED:
            return
        if Queries.GetPreReleasedStatusQuery().IsSatisfiedBy(settlement):
            settlement.Status(SettlementStatus.EXCEPTION)
        if Queries.GetPostReleasedStatusQuery().IsSatisfiedBy(settlement) or Queries.GetIsCancelledSettlementQuery().IsSatisfiedBy(settlement):
            Setters.SetPostSettleActionIfNotStatusVoid(settlement)
        if statusExplanation == CHANGE_TO_SOURCE_DATA:
            settlement.IsChangeToSourceData(True)
        elif statusExplanation == RECALLED_DATA:
            settlement.IsRecalledData(True)
        netHierarchyList.append(SettlementCommitter(settlement, CommitAction.UPDATE))
        netParent.Status(SettlementStatus.UPDATED)

def __DoPostReleasedNetParentUpdate(netChild, netHierarchyList):

    hierarchyTree = HierarchyTree(netChild)


    if hierarchyTree.IsNetHierarchyPartOfHierarchy() == False:
        netParent = netChild.Parent()
        __UpdateSettleSettlement(netParent, netHierarchyList, CHANGE_TO_SOURCE_DATA)
        netParent.IsChangeToSourceData(True)
        if not netParent.Parent(): #We might have manually adjusted the net parent.
            Setters.SetPostSettleActionIfNotStatusVoid(netParent)
        netHierarchyList.append(SettlementCommitter(netParent, CommitAction.UPDATE))

def __RemoveSettlementCommitterFromList(settlement, settlementCommitterList):

    for sc in settlementCommitterList:
        if sc.GetSettlement().Oid() == settlement.Oid():
            settlementCommitterList.remove(sc)

def __GetCommitAction(settlement, settlementCommitterList):

    commitAction = CommitAction.NONE
    for sc in settlementCommitterList:
        if sc.GetSettlement().Oid() == settlement.Oid():
            commitAction = sc.GetCommitAction()
    return commitAction

def __IsSameNetChildrenInHierarchies(netParent, netChildrenList, settlement):

    isSameNetChildrenInHierarchies = True
    children = netParent.Children()
    netParentChildrenOidList = []
    netChildrenOidList = []
    if not len(children):
        return False
    for child in netChildrenList:
        netChildrenOidList.append(child.Oid())
    for child in netParent.Children():
        if child.Oid() != settlement.Oid():
            netParentChildrenOidList.append(child.Oid())
    for childOid in netParentChildrenOidList:
        if childOid not in netChildrenOidList:
            isSameNetChildrenInHierarchies = False
            break
    return isSameNetChildrenInHierarchies

def __GetNetParent(netChildrenList):

    netParent = None
    netParentList = []
    for child in netChildrenList:
        if child.Parent():
            netParentList.append(child.Parent())
    if len(netParentList):
        netPrnt = netParentList[0]
        oid = netPrnt.Oid()
        for np in netParentList:
            if np.Oid() != oid:
                break
        else:
            #Beacause of ACM we do this to get net parent with correct version ID
            query = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
            query.AddAttrNode('Oid', 'EQUAL', netPrnt.Oid())
            netParent = query.Select()[0]
    return netParent

def __DoNetChildInsert(netChildrenList, nettingRule, settlement, netHierarchyList, settlementCommitterList, netParentCleanUpList):
    Utils.LogVerbose('Netting settlement %d with %s' % (settlement.Oid(), netChildrenList))

    oldNetParent = __GetNetParent(netChildrenList)
    updateChildProcess = True
    isSameNetChildrenInHierarchies = False
    if oldNetParent:
        isSameNetChildrenInHierarchies = __IsSameNetChildrenInHierarchies(oldNetParent, netChildrenList, settlement)

    if isSameNetChildrenInHierarchies:
        #Use oldNetParent and update that parent
        netChildrenList.Add(settlement)
        SetNetParentTypes(oldNetParent, netChildrenList)
        updateParentProcess = SetNetParentData(oldNetParent, netChildrenList, nettingRule)
        netChildrenList.RemoveAt(netChildrenList.Size() - 1)
        settlement.Status(SettlementStatus.VOID)
        settlement.StateChart(acm.Operations.GetMappedSettlementProcessStateChart(settlement))
        if settlement.Parent() and \
           settlement.Parent().Oid() != oldNetParent.Oid():
            if not __IsSettlementIncludedInList(settlement.Parent(), netParentCleanUpList):
                netParentCleanUpList.append(settlement.Parent())
        for netChild in netChildrenList:
            netChild.Status(SettlementStatus.VOID)
            if netChild.Parent() and \
               netChild.Parent().Oid() != oldNetParent.Oid():
                if not __IsSettlementIncludedInList(netChild.Parent(), netParentCleanUpList):
                    netParentCleanUpList.append(netChild.Parent())
            commitAction = __GetCommitAction(netChild, settlementCommitterList)
            __RemoveSettlementCommitterFromList(netChild, settlementCommitterList)
            if commitAction == CommitAction.NONE: #existing settlements that haven't actually been updated
                netHierarchyList.append(SettlementCommitter(netChild, CommitAction.UPDATE))
            else:
                netChild.StateChart(acm.Operations.GetMappedSettlementProcessStateChart(netChild))
                netHierarchyList.append(SettlementCommitter(netChild, commitAction, updateChildProcess))
        netHierarchyList.append(SettlementCommitter(oldNetParent, CommitAction.UPDATE, updateParentProcess))
    else:
        #create new netParent
        netChildrenList.Add(settlement)
        netParent = __CreateNetParent(netChildrenList, nettingRule)
        netChildrenList.RemoveAt(netChildrenList.Size() - 1)
        settlement.Status(SettlementStatus.VOID)
        settlement.StateChart(acm.Operations.GetMappedSettlementProcessStateChart(settlement))
        if not __IsSettlementIncludedInList(settlement.Parent(), netParentCleanUpList):
            netParentCleanUpList.append(settlement.Parent())
        for netChild in netChildrenList:
            netChild.Status(SettlementStatus.VOID)

            if not __IsSettlementIncludedInList(netChild.Parent(), netParentCleanUpList):
                netParentCleanUpList.append(netChild.Parent())
            commitAction = __GetCommitAction(netChild, settlementCommitterList)
            __RemoveSettlementCommitterFromList(netChild, settlementCommitterList)
            if commitAction == CommitAction.NONE:   #existing settlements that haven't actually been updated
                netHierarchyList.append(SettlementCommitter(netChild, CommitAction.UPDATE))
            else:
                netChild.StateChart(acm.Operations.GetMappedSettlementProcessStateChart(netChild))
                netHierarchyList.append(SettlementCommitter(netChild, commitAction, updateChildProcess))
        netHierarchyList.append(SettlementCommitter(netParent, CommitAction.INSERT))

def __DoNetChildRecall(netChild, netHierarchyList):

    hierarchyTree = HierarchyTree(netChild)
    if hierarchyTree.IsNetHierarchyPartOfHierarchy() == False:
        netParent = netChild.Parent()
        __UpdateSettleSettlement(netParent, netHierarchyList, RECALLED_DATA)
        netParent.IsRecalledData(True)
        if not netParent.Parent():
            Setters.SetPostSettleActionIfNotStatusVoid(netParent)
        netHierarchyList.append(SettlementCommitter(netParent, CommitAction.UPDATE))

def __IsSettlementIncludedInList(settlement, settlementList):

    if settlement == None:
        return True

    isSettlementIncludedInList = False
    for s in settlementList:
        if s.Oid() == settlement.Oid():
            isSettlementIncludedInList = True
            break
    return isSettlementIncludedInList

def __DoNetChildDelete(settlementCommitter, netParentCleanUpList):
    netParent = settlementCommitter.GetNetParent()
    if not __IsSettlementIncludedInList(netParent, netParentCleanUpList):
        netParentCleanUpList.append(netParent)

def __DoUnNetNetChild(settlementCommitter, netParentCleanUpList):
    netChild = settlementCommitter.GetSettlement()
    settlementCommitter.SetNetParent(netChild.Parent())
    netChild.Parent(None)
    netChild.IsChangeToSourceData(False)
    netChild.IsAmendmentProcess(False)
    if netChild.Status() != SettlementStatus.PENDING_AMENDMENT:
        netChild.Status(SettlementStatus.EXCEPTION)
    if netChild.IsValidForSTP():
        netChild.STP()
    netChild.StateChart(acm.Operations.GetMappedSettlementProcessStateChart(netChild))
    settlementCommitter.SetUpdateProcess(True)
    __DoNetChildDelete(settlementCommitter, netParentCleanUpList)

def IsNotAdHocNetNetParent(settlement):
    if settlement.Parent():
        if settlement.Parent().RelationType() != RelationType.AD_HOC_NET:
            return True
    return False

def IsAdHocNetNetPart(settlement):
    parent = settlement.Parent()
    if parent:
        if parent.RelationType() == RelationType.AD_HOC_NET:
            if (parent.Parent() == None and
                len(parent.SplitChildren())== 0):
                for child in parent.Children():
                    if child.RelationType() != RelationType.NONE:
                        return False
                return True
    return False

def IsValidNetPart(settlement):
    return settlement.IsSystemNetPart() or IsAdHocNetNetPart(settlement)


def Net(settlementCommitter, netParentCleanUpList, settlementCommitterList, possibleNettingCandidates, nettingRule, settlementCommittermap):
    settlement = settlementCommitter.GetSettlement()
    netChildrenList = acm.FArray()
    netHierarchyList = list()

    netCandidatesFinder = Singleton.GetNetCandidatesFinder()

    netCandidatesFinder.GetNetCandidates(settlementCommitter, settlementCommitterList, netChildrenList, possibleNettingCandidates, nettingRule, settlementCommittermap)
    netParent = SettlementUtils.GetSettlementNetParent(settlement)
    if settlementCommitter.GetCommitAction() == CommitAction.UPDATE and \
       IsValidNetPart(settlement) and (Queries.GetPostReleasedStatusQuery().IsSatisfiedBy(netParent) or \
       Queries.GetUpdatedVoidRecalledStatusQuery().IsSatisfiedBy(netParent) or \
       Queries.IsCancelledSettlement().IsSatisfiedBy(netParent) or \
       Queries.IsSecuritySettlementWithStatusReplaced().IsSatisfiedBy(netParent)):
        __DoPostReleasedNetParentUpdate(settlement, netHierarchyList)
    elif settlementCommitter.GetCommitAction() == CommitAction.RECALL and \
         IsValidNetPart(settlement):
        __DoNetChildRecall(settlement, netHierarchyList)
    elif settlementCommitter.GetCommitAction() == CommitAction.DELETE and \
         settlementCommitter.GetNetParent():
        __DoNetChildDelete(settlementCommitter, netParentCleanUpList)
    elif netChildrenList.Size() > 0:
        if settlementCommitter.GetCommitAction() == CommitAction.UPDATE and \
           IsValidNetPart(settlement) and Queries.GetPreReleasedStatusQuery().IsSatisfiedBy(netParent):
            __DoNetChildInsert(netChildrenList, nettingRule, settlement, netHierarchyList, settlementCommitterList, netParentCleanUpList)
        elif settlementCommitter.GetCommitAction() == CommitAction.INSERT or \
             settlementCommitter.GetCommitAction() == CommitAction.UPDATE:
            __DoNetChildInsert(netChildrenList, nettingRule, settlement, netHierarchyList, settlementCommitterList, netParentCleanUpList)
    elif netChildrenList.Size() == 0:
        if settlementCommitter.GetCommitAction() == CommitAction.UPDATE and IsValidNetPart(settlement):
            __DoUnNetNetChild(settlementCommitter, netParentCleanUpList)
        elif settlementCommitter.GetCommitAction() == CommitAction.INSERT and IsValidNetPart(settlement) and settlement.RelationType() == RelationType.VALUE_DAY_ADJUSTED:
            __DoUnNetNetChild(settlementCommitter, netParentCleanUpList)
    return netHierarchyList

