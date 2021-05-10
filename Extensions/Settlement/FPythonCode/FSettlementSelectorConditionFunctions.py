""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementSelectorConditionFunctions.py"
import acm
from FSettlementEnums import RelationType, SettlementStatus, SettlementType
import FOperationsUtils as Utils
import FSettlementStatusQueries as Queries
import FSettlementUtils as SettlementUtils
import FSettlementValidations as Validations
import FSettlementGetters as Getters

#-------------------------------------------------------------------------
def IsCorrectedTrade(settlement):
    isMet = False
    if Utils.IsCorrectedTrade(settlement.Trade()):
        topSettlement = SettlementUtils.FindRootInHierarchyTree(settlement)
        if topSettlement and (not topSettlement.IsSecurity() or topSettlement.Status() != SettlementStatus.ACKNOWLEDGED):
            isMet = Queries.GetPostReleasedStatusQuery().IsSatisfiedBy(topSettlement) or topSettlement.Status == SettlementStatus.CLOSED
        else:
            isMet = False
    return isMet

#-------------------------------------------------------------------------
def IsInactivePartial(settlement):
    isMet = False
    if Validations.IsPartOfPartial(settlement):
        trade = settlement.Trade()
        partialParent = Getters.GetPartialParent(settlement)
        if partialParent and trade:
            noActivePartialChildren = True
            for child in partialParent.PartialChildren():
                if child.Status() not in [SettlementStatus.CANCELLED, SettlementStatus.REPLACED] and not child.IsSettled():
                    noActivePartialChildren = False
            foundOtherActiveSettlement = False
            for settlement in trade.Settlements():
                if settlement.Children() or settlement.GetTopNonCancellationSettlementInHierarchy() == partialParent:
                    continue
                if not settlement.PartialParent():
                    settlement = settlement.GetTopNonCancellationSettlementInHierarchy()
                if Validations.IsActiveSecurity(settlement) and not settlement.IsSettled() and settlement not in partialParent.PartialChildren() and \
                   Getters.GetSecurityTypes(settlement, trade) == Getters.GetSecurityTypes(partialParent, trade):
                    if settlement.Type() == SettlementType.REDEMPTION_SECURITY:
                        if settlement.CashFlow() == settlement.CashFlow():
                            foundOtherActiveSettlement = True
                    else:
                        foundOtherActiveSettlement = True

            isMet = noActivePartialChildren and foundOtherActiveSettlement
    return isMet

#-------------------------------------------------------------------------
def IsInactivePairOff(settlement):
    isMet = False
    if not Validations.IsPartOfPartial(settlement) and Validations.IsPartOfPairOff(settlement):
        trade = settlement.Trade()
        pairOffParent = Getters.GetPairOffParent(settlement)
        if pairOffParent and trade:
            for settlement in trade.Settlements():
                if settlement.Children() or settlement.GetTopNonCancellationSettlementInHierarchy() == pairOffParent or \
                    (settlement.GetTopNonCancellationSettlementInHierarchy() and settlement.GetTopNonCancellationSettlementInHierarchy().PairOffChildren()):
                    continue
                if not settlement.PairOffParent():
                    settlement = settlement.GetTopNonCancellationSettlementInHierarchy()
                if Validations.IsActiveSecurity(settlement) and not settlement.IsSettled() and settlement not in pairOffParent.PairOffChildren() and \
                   Getters.GetSecurityTypes(settlement, trade) == Getters.GetSecurityTypes(pairOffParent, trade):
                    isMet = True
    return isMet

#-------------------------------------------------------------------------
def IsInactivePartOfPartial(settlement):
    isMet = False
    if Validations.IsPartOfPartial(settlement):
        partialParent = Getters.GetPartialParent(settlement)
        if partialParent and (settlement != partialParent or settlement.NumberOfChildren() == 0 or Validations.IsCorrectedSingleRecord(settlement)):
            atLeastOneSettled = False
            allSettled = True
            for partialChild in partialParent.PartialChildren():
                isSettled = partialChild.IsSettled()
                if isSettled:
                    atLeastOneSettled = True
                allSettled = allSettled and isSettled
            if settlement.Status() == SettlementStatus.REPLACED:
                isMet = atLeastOneSettled and not allSettled
            elif not settlement.PartialParent():
                isMet = settlement.GetTopNonCancellationSettlementInHierarchy().IsSettled() or not atLeastOneSettled
            else:
                isMet = settlement.IsSettled() or not atLeastOneSettled
        else:
            isMet = True
    return isMet

#-------------------------------------------------------------------------
def IsInactivePartOfPairOff(settlement):
    isMet = False
    if Validations.IsPartOfPairOff(settlement):
        pairOffParent = Getters.GetPairOffParent(settlement)
        trade = settlement.Trade()
        if pairOffParent and settlement != pairOffParent and settlement.GetTopNonCancellationSettlementInHierarchy() != pairOffParent and trade:
            useLeftOverPayment = False
            for pairOffChild in pairOffParent.PairOffChildren():
                if not pairOffChild.IsPairedOff() and pairOffChild.Trade() == trade:
                    if settlement.Type() == pairOffChild.Type() or pairOffChild.Type() == SettlementType.PAIR_OFF_PAYMENT:
                        useLeftOverPayment = True
            if pairOffParent.IsSettled() and useLeftOverPayment:
                if not settlement.PairOffParent():
                    isMet = settlement.GetTopNonCancellationSettlementInHierarchy().IsPairedOff() or Validations.IsFullyCancelled(settlement.GetTopSettlementInHierarchy())
                else:
                    isMet = settlement.IsPairedOff() or Validations.IsFullyCancelled(settlement.GetTopSettlementInHierarchy())
            else:
                if not settlement.PairOffParent():
                    isMet = not settlement.GetTopNonCancellationSettlementInHierarchy().IsPairedOff()
                else:
                    isMet = (not settlement.IsPairedOff() and settlement.NumberOfChildren() == 0)
        else:
            isMet = True
    return isMet

#-------------------------------------------------------------------------
def IsStoredForAccounting(settlement):
    isMet = False
    if settlement.RelationType() == RelationType.STORED_FOR_ACCOUNTING:
        isMet = True
    return isMet
