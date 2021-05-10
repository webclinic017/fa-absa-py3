""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingAmendmentEvaluator.py"

# accounting
from FAccountingEnums import ReversalMethod
import FAccountingCompare as Compare
import FAccountingValidation as Validation

#-------------------------------------------------------------------------
def SkipAmendment(newPair, oldPair, previousPair, _):
    return newPair.ComparePairsAll(previousPair, Compare.IsSupressed) and \
        not newPair.CompareAny(Compare.IsPreventHistoricalAmendments) and \
        not newPair.IsEmpty()

#-------------------------------------------------------------------------
def IsCreateNew(newPair, oldPair, previousPair, _):
    return not newPair.ComparePairsAll(previousPair, Compare.IsSupressed) and \
           not newPair.CompareAny(Compare.IsPreventHistoricalAmendments)  and \
           not newPair.IsEmpty()

#-------------------------------------------------------------------------
def IsAmendment(newPair, oldPair, previousPair, args):
    if newPair.ComparePairsAny(oldPair, Compare.IsAmendmentPreventLive):
        return True

    if IsRemoveOld(newPair, oldPair, previousPair, args) and \
       not newPair.CompareAny(Compare.IsPreventHistoricalAmendments) and \
       (newPair.ComparePairsAny(oldPair, Compare.IsAmendment, args) or \
       not newPair.ComparePairsSameSize(oldPair)):
        return True

    return False

#-------------------------------------------------------------------------
def IsRemoveOld(newPair, oldPair, previousPair, _):
    return not oldPair.CompareAny(Compare.IsManual) and \
           not oldPair.CompareAny(Compare.IsPreventHistoricalAmendments)

#-------------------------------------------------------------------------
def IsProcessPrevious(newPair, oldPair, previousPair, _):
    if  previousPair and newPair and \
        not previousPair.CompareAny(Compare.IsManual) and \
        (not previousPair.ComparePairsAll(newPair, Compare.IsSupressed) or \
         not previousPair.ComparePairsSameSize(newPair)) and \
        not previousPair.CompareAny(Compare.IsReversalExclusion) and \
        (previousPair.CompareAny(Validation.IsValidReallocationReversal, newPair, oldPair) or \
         previousPair.CompareAny(Validation.IsValidPeriodicReversal)):
        return True

    return False

#-------------------------------------------------------------------------
def IsIncrementalBaseAmount(newPair, previousPair, args):
    if newPair and previousPair and \
       args['book'].IncrementalBaseAmount() and \
       not args['ai'].ExcludeFXConversion() and \
       args['ai'].IsPeriodic() and \
       (args['ai'].ReversalMethod() == ReversalMethod.REVERSE_AND_REPLACE) and \
       newPair.ComparePairsAll(previousPair, Validation.IsValidForIncrementalBaseAmount):
        return True

    return False
