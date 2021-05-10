""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementActions.py"
import acm
from FSettlementEnums import SettlementStatus

#-------------------------------------------------------------------------
# Settlement action functions - used by FSettlementSecurityProcessEngine and FSettlementSecurityUpdateEngine
#-------------------------------------------------------------------------

#-------------------------------------------------------------------------
def InstructToCorrect(settlement):
    settlementClone = settlement.Clone()
    results = acm.Operations.Actions().InstructToCorrect(settlementClone)
    return _PreCommit(results.First(), settlement, results.Second())

#-------------------------------------------------------------------------
def InstructToCancel(settlement):
    settlementClone = settlement.Clone()
    results = acm.Operations.Actions().InstructToCancel(settlementClone)
    return _PreCommit(results.First(), settlement, results.Second())

#-------------------------------------------------------------------------
def InstructedToCancel(settlement):
    settlementClone = settlement.Clone()
    results = acm.Operations.Actions().InstructedToCancel(settlementClone)
    return _PreCommit(results.First(), settlement, results.Second())
    

#-------------------------------------------------------------------------
def _PreCommit(cancellationSettlement, originalSettlement, cancelledSettlement):
    newSettlements = list()
    oldSettlements = list()
    cancellationSettlement.ProcessStatusChlItem(None)

    originalSettlement.IsDirty(True)
    cancelledSettlement.Parent(cancellationSettlement)

    if originalSettlement.IsPreReleased() or originalSettlement.Status() == SettlementStatus.REPLACED:
        cancellationSettlement.Status(SettlementStatus.PENDING_CLOSURE)
        cancelledSettlement.Status(SettlementStatus.CANCELLED)

    oldSettlements.append(originalSettlement)
    newSettlements.append(cancelledSettlement)
    newSettlements.append(cancellationSettlement)

    return oldSettlements, newSettlements