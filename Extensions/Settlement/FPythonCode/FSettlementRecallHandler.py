""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementRecallHandler.py"
import acm

import FOperationsRuleEngine as Engine
import FOperationsUtils as Utils

import FSettlementSetters as Setters
import FSettlementStatusQueries as Queries
from FSettlementCommitter import SettlementCommitter, CommitAction
from FSettlementHierarchy import HierarchyTree
from FSettlementEnums import SettlementStatus

class SettlementRecallHandler(object):

    def __init__(self):
        import FSettlementParameters as SettlementParams
        self.rules = []
        for query in SettlementParams.preventSettlementDeletionQueries:
            preventQuery = Utils.GetStoredQuery(query, acm.FSettlement)
            if preventQuery:
                self.rules.append(Engine.Rule(Engine.QueryCondition(preventQuery.Query()), Engine.ActionFunction(SettlementRecallHandler.PreventSettlementDeletion)))
        for (query, function) in SettlementRecallHandler.GetQueriesFunctionsList():
            condition = Engine.QueryCondition(query)
            self.rules.append(Engine.Rule(condition, function))
        self.ruleExecutor = Engine.RuleExecutor(self.rules, Engine.ActionFunction(SettlementRecallHandler.FallBack))


    def ProcessRecall(self, oldSettlement):
        return self.ruleExecutor.Execute(oldSettlement, Engine.ValueType.SINGLE_VALUE, oldSettlement)

    @staticmethod
    def GetHierarchyMembers(oldSettlement):
        returnList = []
        settlements = oldSettlement.SplitChildren()
        for settlement in settlements:
            if not settlement.Status() == SettlementStatus.CLOSED:
                returnList.append(settlement)
        children = oldSettlement.Children()
        for child in children:
            if not child.Status() == SettlementStatus.CLOSED:
                returnList.append(child)
        return returnList

    @staticmethod
    def RecallUpdatedVoid(oldSettlement):
        toBeCommittedList = list()
        hierarchyTree = HierarchyTree(oldSettlement)
        if hierarchyTree.HasClosedNodeInTree():
            Utils.LogVerbose('Settlement %d will NOT be recalled. Part of hierarchy with settlement record in status Closed.' % (hierarchyTree.GetRoot().GetSettlement().Oid()))
            return toBeCommittedList

        partOfHierarchy = hierarchyTree.HasNodes()
        oldSettlement.IsRecalledData(True)
        oldSettlement.IsAmendmentProcess(False)
        oldSettlement.IsChangeToSourceData(False)

        if partOfHierarchy == True:
            oldSettlement.Status(SettlementStatus.RECALLED)
            settlementSet = set()
            nodePaths = hierarchyTree.GetNodePaths()
            for nodePath in nodePaths:
                nodePath.RecallNodePath()
                for settlement in nodePath.GetSettlements():
                    settlementSet.add(settlement)
            for settlement in settlementSet:
                toBeCommittedList.append(SettlementCommitter(settlement, CommitAction.UPDATE))
            toBeCommittedList.append(SettlementCommitter(oldSettlement, CommitAction.RECALL))
        else:
            if oldSettlement.Status() == SettlementStatus.UPDATED or \
               ((oldSettlement.IsCancelledByTheCounterparty() or \
               oldSettlement.IsCancelledByUs()) and \
               oldSettlement.ManualMatch() == False):
                toBeCommittedList.append(SettlementCommitter(oldSettlement, CommitAction.DELETE))
            else:
                toBeCommittedList = SettlementRecallHandler.RecallPostReleased(oldSettlement)
                oldSettlement.PostSettleAction(True)
                newSettlement = toBeCommittedList[1].GetSettlement()
                newSettlement.ManualMatch(False)
                newSettlement.IsNoStatusExplanation(True)
                newSettlement.IsRecalledData(True)
        return toBeCommittedList

    @staticmethod
    def RecallClosedRecalled(dummyOldSettlement):
        return []

    @staticmethod
    def RecallPreReleased(oldSettlement):
        returnList = []
        returnList.append(SettlementCommitter(oldSettlement, CommitAction.DELETE))
        return returnList

    @staticmethod
    def RecallPostReleased(oldSettlement):
        returnList = []
        newSettlement = acm.FSettlement()
        newSettlement.RegisterInStorage()
        newSettlement.Apply(oldSettlement)
        newSettlement.Owner(oldSettlement.Owner())  #owner is not copied when performing Apply()
        if oldSettlement.Diary():
            newSettlement.CopyDiary(oldSettlement)
        Setters.SetPostSettleActionIfNotStatusVoid(oldSettlement)
        newSettlement.Status(SettlementStatus.RECALLED)
        newSettlement.IsRecalledData(True)
        newSettlement.Parent(oldSettlement)
        oldSettlement.IsRecalledData(True)
        returnList.append(SettlementCommitter(oldSettlement, CommitAction.RECALL))
        returnList.append(SettlementCommitter(newSettlement, CommitAction.INSERT))
        return returnList

    @staticmethod
    def RecallNetPart(oldSettlement):
        returnList = None
        hierarchyTree = HierarchyTree(oldSettlement)
        if hierarchyTree.IsNetHierarchyPartOfHierarchy() == True:
            returnList = SettlementRecallHandler.RecallUpdatedVoid(oldSettlement)
        else:
            netParent = oldSettlement.Parent()
            returnList = list()
            if netParent.Status() == SettlementStatus.CLOSED:
                Utils.LogVerbose('%s settlement %d is in status Closed and %s settlement %d will therefore NOT be Recalled.' %
                  (netParent.RelationType(), netParent.Oid(), oldSettlement.RelationType(), oldSettlement.Oid()))
            elif Queries.GetPreReleasedStatusQuery().IsSatisfiedBy(netParent):
                sc = SettlementCommitter(oldSettlement, CommitAction.DELETE)
                sc.SetNetParent(oldSettlement.Parent())
                oldSettlement.Parent(None)
                sc.GetNetParent().Children() #Do not remove!
                returnList.append(sc)
            else:
                oldSettlement.IsRecalledData(True)
                oldSettlement.IsAmendmentProcess(False)
                oldSettlement.IsChangeToSourceData(False)
                oldSettlement.Status(SettlementStatus.RECALLED)
                returnList.append(SettlementCommitter(oldSettlement, CommitAction.RECALL))
        return returnList

    @staticmethod
    def RecallValueDayAdjusted(oldSettlement):
        returnList = list()
        if oldSettlement.GetTopNonCancellationSettlementInHierarchy().IsPreReleased():
            adjustedParent = oldSettlement.Parent()
            sc = SettlementCommitter(adjustedParent, CommitAction.DELETE)
            if adjustedParent.Parent():
                sc.SetNetParent(adjustedParent.Parent())
                adjustedParent.Parent(None)
                sc.GetNetParent().Children()
            returnList.append(sc)
            oldSettlement.Parent(None)
            returnList.append(SettlementCommitter(oldSettlement, CommitAction.DELETE))
        else:
            Utils.LogVerbose('Settlement %d will NOT be deleted/recalled\nsince it is handled by security settlement workflow.' % oldSettlement.Oid())

        return returnList

    @staticmethod
    def PreventSettlementDeletion(oldSettlement):
        Utils.LogVerbose('Settlement %d will NOT be deleted/recalled\ndue to query in preventSettlementDeletionQueries.' % oldSettlement.Oid())
        return []

    @staticmethod
    def PreventRecallingCancelledSecurities(oldSettlement):
        Utils.LogVerbose('Settlement %d will NOT be deleted/recalled\nsince it is handled by instruct to cancel.' % oldSettlement.Oid())
        return []

    @staticmethod
    def PreventRecallingSettledSecuritySettlement(oldSettlement):
        Utils.LogVerbose('Settlement %d will NOT be deleted/recalled\nsince it is settled.' % oldSettlement.Oid())
        return []

    @staticmethod
    def FallBack(oldSettlement):
        Utils.LogVerbose('No query was satisfied for settlement %d!' % oldSettlement.Oid())
        Utils.LogVerbose('Returning empty settlement list as fallback.')
        return []

    @staticmethod
    def DoNotAdd(oldSettlement):
        Utils.LogVerbose('Settlement %d will NOT be deleted/recalled\nsince it is handled by security settlement workflow.' % oldSettlement.Oid())
        return []

    @staticmethod
    def GetQueriesFunctionsList():
        qfl = []
        qfl.append((Queries.GetSettledSecuritySettlementQuery(), Engine.ActionFunction(SettlementRecallHandler.PreventRecallingSettledSecuritySettlement)))
        qfl.append((Queries.GetCancelledSecuritiesQuery(), Engine.ActionFunction(SettlementRecallHandler.PreventRecallingCancelledSecurities)))
        qfl.append((Queries.IsVoidCancelCorrectChild(), Engine.ActionFunction(SettlementRecallHandler.DoNotAdd)))
        qfl.append((Queries.IsCancelledSettlement(), Engine.ActionFunction(SettlementRecallHandler.DoNotAdd)))
        qfl.append((Queries.GetPartialSettled(), Engine.ActionFunction(SettlementRecallHandler.DoNotAdd)))
        qfl.append((Queries.GetPairOffHierarchyChildren(), Engine.ActionFunction(SettlementRecallHandler.DoNotAdd)))
        qfl.append((Queries.IsSecuritySettlementWithStatusReplaced(), Engine.ActionFunction(SettlementRecallHandler.DoNotAdd)))
        qfl.append((Queries.GetPairOffPaymentsQuery(), Engine.ActionFunction(SettlementRecallHandler.DoNotAdd)))        
        qfl.append((Queries.GetPairOffChildrenQuery(), Engine.ActionFunction(SettlementRecallHandler.DoNotAdd)))        
        qfl.append((Queries.GetValueDayAdjustedQuery(), Engine.ActionFunction(SettlementRecallHandler.RecallValueDayAdjusted)))
        qfl.append((Queries.GetCompensationPaymentQuery(), Engine.ActionFunction(SettlementRecallHandler.RecallClosedRecalled)))
        qfl.append((Queries.GetNetPartQuery(), Engine.ActionFunction(SettlementRecallHandler.RecallNetPart)))
        qfl.append((Queries.GetUpdatedVoidStatusQuery(), Engine.ActionFunction(SettlementRecallHandler.RecallUpdatedVoid)))
        qfl.append((Queries.GetPreReleasedStatusQuery(), Engine.ActionFunction(SettlementRecallHandler.RecallPreReleased)))
        qfl.append((Queries.GetClosedRecalledStatusQuery(), Engine.ActionFunction(SettlementRecallHandler.RecallClosedRecalled)))
        qfl.append((Queries.GetPostReleasedStatusQuery(), Engine.ActionFunction(SettlementRecallHandler.RecallPostReleased)))
        return qfl
