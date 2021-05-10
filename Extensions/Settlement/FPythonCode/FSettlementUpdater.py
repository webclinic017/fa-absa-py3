""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementUpdater.py"
import acm
import FOperationsRuleEngine as Engine
import FSettlementStatusQueries as Queries
import FOperationsUtils as Utils
import FSettlementSetters as Setters
from FSettlementCommitter import SettlementCommitter, CommitAction
from FSettlementHierarchy import HierarchyTree
from FSettlementHookAdministrator import SettlementHooks, GetHookAdministrator
from FSettlementEnums import SettlementStatus, RelationType

class SettlementUpdater(object):

    def __init__(self):
        self.rules = []

        for (query, function) in GetQueriesFunctionsList():
            condition = Engine.QueryCondition(query)
            self.rules.append(Engine.Rule(condition, function))
        self.ruleExecutor = Engine.RuleExecutor(self.rules, Engine.ActionFunction(FallBack))

    def UpdateSettlements(self, oldSettlement, newSettlement, isAmendmentProcess = False):
        return self.ruleExecutor.Execute(oldSettlement, Engine.ValueType.SINGLE_VALUE, oldSettlement, newSettlement, isAmendmentProcess)

def Apply(oldSettlement, newSettlement, isAmendmentProcess):

    if (isAmendmentProcess == True):
        if (oldSettlement.Status() != SettlementStatus.PENDING_AMENDMENT):
            oldSettlement.Status(SettlementStatus.PENDING_AMENDMENT)
        return

    newDiaryText = ""
    if newSettlement.HasDiary():
        newDiaryText = newSettlement.Diary().Text()

    # fields modified by users are preserved
    newSettlement.Diary(oldSettlement.Diary())
    newSettlement.RestrictNet(oldSettlement.RestrictNet())
    newSettlement.Text(oldSettlement.Text())
    newSettlement.PartialSettlementType(oldSettlement.PartialSettlementType())
    # fields set by dh_layer are preserved
    newSettlement.AccountingNotificationDay(oldSettlement.AccountingNotificationDay())
    newSettlement.ManualMatch(oldSettlement.ManualMatch())
    oldSettlement.Apply(newSettlement)
    oldSettlement.Owner(newSettlement.Owner())  #owner is not copied when performing Apply()

    if newDiaryText != "":
        oldSettlement.AddDiaryNoteWithoutTimeStamp(str("\n") + newDiaryText)

def SettleSettlementIsClosed(settlement):
    closed = False
    settlementList = settlement.Settlement()
    if len(settlementList):
        if settlementList[0].Status() == SettlementStatus.CLOSED:
            closed = True
    return closed

def HandleHierarchyUpdate(hierarchyTree, newSettlement, toBeCommittedList, isAmendmentProcess):

    if hierarchyTree.HasClosedNodeInTree():
        Utils.LogVerbose('Settlement %d will NOT be updated. Part of hierarchy with settlement record in status Closed.' % (hierarchyTree.GetRoot().GetSettlement().Oid()))
        return toBeCommittedList

    oldSettlement = hierarchyTree.GetRoot().GetSettlement()
    parent = oldSettlement.Parent()
    Apply(oldSettlement, newSettlement, isAmendmentProcess)
    Setters.SetPendingAmendmentStatusExplanation(oldSettlement, isAmendmentProcess)
    oldSettlement.IsChangeToSourceData(False)
    oldSettlement.IsRecalledData(False)
    processSet = set()

    if isAmendmentProcess == False:
        statusExplanation = oldSettlement.StatusExplanation()
        oldSettlement.Parent(parent)
        oldSettlement.StatusExplanation(statusExplanation)
        oldSettlement.IsRecalledData(False)
        oldSettlement.IsChangeToSourceData(True)
        oldSettlement.Status(SettlementStatus.UPDATED)
        processSet.add(oldSettlement)

    settlementSet = set()
    nodePaths = hierarchyTree.GetNodePaths()

    for nodePath in nodePaths:
        processPathSet = nodePath.UpdateNodePath()
        processSet = processSet.union(processPathSet)
        for settlement in nodePath.GetSettlements():
            settlementSet.add(settlement)
    updateProcess = oldSettlement in processSet
    toBeCommittedList.append(SettlementCommitter(oldSettlement, CommitAction.UPDATE, updateProcess))
    for settlement in settlementSet:
        updateProcess = settlement in processSet
        ReMapStateChart(settlement)
        toBeCommittedList.append(SettlementCommitter(settlement, CommitAction.UPDATE, updateProcess))


def HandleNewHierarchyUpdate(oldSettlement, \
                             newSettlement, \
                             toBeCommittedList \
                             ):

    import FSettlementParameters as Params
    if Params.updateVoidedSettlement == True:
        newSettlement.Status(SettlementStatus.UPDATED)
        newSettlement.Parent(oldSettlement)
        newSettlement.IsChangeToSourceData(True)
        newSettlement.IsRecalledData(False)
        oldSettlement.RelationType(SettlementStatus.UPDATED)
        oldSettlement.IsChangeToSourceData(True)
        oldSettlement.IsRecalledData(False)
        Setters.SetPostSettleActionIfNotStatusVoid(oldSettlement)
        toBeCommittedList.append(SettlementCommitter(newSettlement, CommitAction.INSERT))
        toBeCommittedList.append(SettlementCommitter(oldSettlement, CommitAction.UPDATE))

    else:
        Utils.LogVerbose("Settlement %d will NOT be updated.\n" % oldSettlement.Oid()+ \
                  "See parameter updateVoidedSettlement in FSettlementParameters.")

def ProcessUpdatedVoidRecalledUpdate(oldSettlement, newSettlement, isAmendmentProcess):

    returnList = list()
    hierarchyTree = HierarchyTree(oldSettlement, isAmendmentProcess)
    if hierarchyTree.HasNodes():
        HandleHierarchyUpdate(hierarchyTree, newSettlement, returnList, isAmendmentProcess)
    else:
        if isAmendmentProcess == False:
            HandleNewHierarchyUpdate(oldSettlement, newSettlement, returnList)
    return returnList

def UpdateSettlementAndCreateUpdatedRow(oldSettlement, newSettlement, updateProcess = False):
    returnList = []

    newSettlement.Status(SettlementStatus.UPDATED)
    ReMapStateChart(newSettlement)
    newSettlement.Parent(oldSettlement)
    if oldSettlement.Diary():
        newSettlement.CopyDiary(oldSettlement)
    newSettlement.Text(oldSettlement.Text())
    newSettlement.IsChangeToSourceData(True)
    oldSettlement.IsChangeToSourceData(True)
    oldSettlement.RelationType(RelationType.UPDATED)
    Setters.SetPostSettleActionIfNotStatusVoid(oldSettlement)
    returnList.append(SettlementCommitter(newSettlement, CommitAction.INSERT))
    returnList.append(SettlementCommitter(oldSettlement, CommitAction.UPDATE, updateProcess))

    return returnList

def ReMapStateChart(settlement):
    clone = settlement.Clone()
    clone.RegisterInStorage()
    clone.Owner(settlement.Owner())
    stateChart = acm.Operations.GetMappedSettlementProcessStateChart(clone)
    settlement.StateChart(stateChart)

def ProcessPreReleasedUpdate(oldSettlement, newSettlement, isAmendmentProcess):
    if not oldSettlement.ManualMatch():
        returnList = list()
        updateProcess = False
        if not isAmendmentProcess:
            hookAdmin = GetHookAdministrator()
            updateProcess = hookAdmin.HA_CallHook(SettlementHooks.UPDATE_SETTLEMENT_BUSINESS_PROCESS, oldSettlement, newSettlement)
        oldProcessStatusChlItem = oldSettlement.ProcessStatusChlItem()
        if oldSettlement.Status() == SettlementStatus.AWAITING_CANCELLATION and newSettlement:
            newSettlement.Status(SettlementStatus.AWAITING_CANCELLATION)
        Apply(oldSettlement, newSettlement, isAmendmentProcess)
        if not updateProcess and not isAmendmentProcess:
            oldSettlement.ProcessStatusChlItem(oldProcessStatusChlItem)
        returnList.append(SettlementCommitter(oldSettlement, CommitAction.UPDATE, updateProcess))
        return returnList
    else:
        if isAmendmentProcess == True:
            return list()
        oldSettlement.Status(SettlementStatus.EXCEPTION)
        ReMapStateChart(oldSettlement)
        hookAdmin = GetHookAdministrator()
        updateProcess = hookAdmin.HA_CallHook(SettlementHooks.UPDATE_SETTLEMENT_BUSINESS_PROCESS, oldSettlement, newSettlement)
        return UpdateSettlementAndCreateUpdatedRow(oldSettlement, newSettlement, updateProcess)


def ProcessClosedUpdate(oldSettlement, dummyNewSettlement, dummyIsAmendmentProcess):
    Utils.LogVerbose('Settlement %d is in status %s and will therefore NOT be updated.' % \
             (oldSettlement.Oid(), oldSettlement.Status()))
    return []

def ProcessPostReleasedUpdate(oldSettlement, newSettlement, isAmendmentProcess):
    returnList = list()
    if newSettlement and newSettlement.Parent() and newSettlement.Parent().RelationType() in [RelationType.CANCEL_CORRECT, RelationType.CANCELLATION]:
        Apply(oldSettlement, newSettlement, False)
        returnList.append(SettlementCommitter(oldSettlement, CommitAction.UPDATE))
        return returnList

    if isAmendmentProcess == True:
        return returnList
    return UpdateSettlementAndCreateUpdatedRow(oldSettlement, newSettlement)


def ProcessCompensationPayment(oldSettlement, dummyNewSettlement, dummyIsAmendmentProcess):

    Utils.LogVerbose('Settlement %d is of category Compensation Payment and will therefore ' + \
              'NOT be considered for update.' % oldSettlement.Oid())
    return []

def ProcessNetPart(oldSettlement, newSettlement, isAmendmentProcess):

    returnList = list()
    hierarchyTree = HierarchyTree(oldSettlement, isAmendmentProcess)
    if hierarchyTree.IsNetHierarchyPartOfHierarchy() == True:
        HandleHierarchyUpdate(hierarchyTree, newSettlement, returnList, isAmendmentProcess)
    else:
        netParent = oldSettlement.Parent()
        if netParent:
            if netParent.Status() != SettlementStatus.CLOSED:
                statusExplanation = oldSettlement.StatusExplanation()
                if Queries.GetPreReleasedStatusQuery().IsSatisfiedBy(netParent):
                    Apply(oldSettlement, newSettlement, isAmendmentProcess)
                    Setters.SetPendingAmendmentStatusExplanation(oldSettlement, isAmendmentProcess)
                    if isAmendmentProcess == False:
                        if oldSettlement.Status() != SettlementStatus.EXCEPTION:
                            oldSettlement.Status(SettlementStatus.VOID)
                            oldSettlement.IsChangeToSourceData(False)
                        oldSettlement.StatusExplanation(statusExplanation)
                        oldSettlement.IsRecalledData(False)
                        oldSettlement.Parent(netParent)
                        netParent.IsChangeToSourceData(False)
                    returnList.append(SettlementCommitter(oldSettlement, CommitAction.UPDATE))
                elif Queries.GetPostReleasedStatusQuery().IsSatisfiedBy(netParent) or \
                     Queries.GetUpdatedVoidStatusQuery().IsSatisfiedBy(netParent):
                    if isAmendmentProcess == False:
                        Apply(oldSettlement, newSettlement, isAmendmentProcess)
                        oldSettlement.Status(SettlementStatus.UPDATED)
                        oldSettlement.StatusExplanation(statusExplanation)
                        oldSettlement.IsChangeToSourceData(True)
                        oldSettlement.IsRecalledData(False)
                        oldSettlement.Parent(netParent)
                        returnList.append(SettlementCommitter(oldSettlement, CommitAction.UPDATE))
            else:
                Utils.LogVerbose('%s settlement %d is in status Closed and %s settlement %d will therefore NOT be updated.' % \
                         (netParent.RelationType(), netParent.Oid(), oldSettlement.RelationType(), oldSettlement.Oid()))
        else:
            Utils.LogVerbose('Net settlement not found for Net Part settlement %d' % oldSettlement.Oid())
    return returnList

def ProcessSettledSecurityUpdate(oldSettlement, dummyNewSettlement, dummyIsAmendmentProcess):
    Utils.LogVerbose('Settlement %d will not be updated as it is fully settled' % oldSettlement.Oid())
    return []

def ProcessValueDayAdjusted(oldSettlement, newSettlement, isAmendmentProcess):
    returnList = list()
    returnListTemp = list()
    valueDayAdjustedParent = oldSettlement.Parent()
    returnListTemp = ProcessPreReleasedUpdate(oldSettlement, newSettlement, isAmendmentProcess)
    if returnListTemp:
        oldSettlement.Parent(None)
        sc = SettlementCommitter(valueDayAdjustedParent, CommitAction.DELETE)
        sc.SetNetParent(valueDayAdjustedParent.Parent())
        valueDayAdjustedParent.Parent(None)
        returnList.append(sc)
        returnList.extend(returnListTemp)
    return returnList

def FallBack(oldSettlement, dummyNewSettlement, dummyIsAmendmentProcess):
    Utils.LogVerbose('No query was satisfied for settlement %d!' % oldSettlement.Oid())
    Utils.LogVerbose('Returning empty settlement list as fallback.')
    return []


def GetQueriesFunctionsList():
    qfl = []
    qfl.append((Queries.GetValueDayAdjustedQuery(), Engine.ActionFunction(ProcessValueDayAdjusted)))
    qfl.append((Queries.GetSettledSecuritySettlementQuery(), Engine.ActionFunction(ProcessSettledSecurityUpdate)))
    qfl.append((Queries.GetCompensationPaymentQuery(), Engine.ActionFunction(ProcessCompensationPayment)))
    qfl.append((Queries.GetNetPartQuery(), Engine.ActionFunction(ProcessNetPart)))
    qfl.append((Queries.GetUpdatedVoidRecalledStatusQuery(), Engine.ActionFunction(ProcessUpdatedVoidRecalledUpdate)))
    qfl.append((Queries.GetPreReleasedStatusQuery(), Engine.ActionFunction(ProcessPreReleasedUpdate)))
    qfl.append((Queries.GetClosedStatusQuery(), Engine.ActionFunction(ProcessClosedUpdate)))
    qfl.append((Queries.GetPostReleasedStatusQuery(), Engine.ActionFunction(ProcessPostReleasedUpdate)))
    return qfl

