""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementValidations.py"
from   FSettlementEnums import RelationType, SettlementStatus, SettlementType
from   FOperationsEnums import CashFlowType, InsType
import FSettlementTradeAmendmentFilterHandlerSingleton as Singleton
import FOperationsUtils as Utils
import acm

#-------------------------------------------------------------------------
# Settlement validation functions - used by FSettlementCreator, FSettlementModificationInspector, 
# FSettlementSecurityCommon, FSettlementSecurityProcessEngine, FSettlementSecurityUpdateEngine and FSettlementSelector
#-------------------------------------------------------------------------

#-------------------------------------------------------------------------
def IsPostReleasedSettlement(settlement):
    if settlement.Status() in [SettlementStatus.ACKNOWLEDGED, SettlementStatus.PENDING_CLOSURE]:
        return True
    return False

#-------------------------------------------------------------------------
def IsAcknowledgedSecuritySettlement(settlement):
    if settlement.Status() == SettlementStatus.ACKNOWLEDGED and settlement.IsSecurity():
        return True
    return False

#-------------------------------------------------------------------------
def IsPreReleasedSecuritySettlement(settlement):
    if settlement.IsPreReleased() and settlement.IsSecurity():
        return True
    return False

#-------------------------------------------------------------------------
def IsActiveSecurity(settlement):
    if settlement.IsSecurity():
        topSettlement = settlement.GetTopSettlementInHierarchy()
        return topSettlement.Status() not in [SettlementStatus.CANCELLED, SettlementStatus.REPLACED, SettlementStatus.CLOSED, SettlementStatus.PENDING_CLOSURE, SettlementStatus.VOID]
    else:
        return False

#-------------------------------------------------------------------------
def ProcessAsPreReleased(settlement):
    if len(settlement.PartialChildren()) == 0:
        return settlement.IsPreReleased()
    else:
        for child in settlement.PartialChildren():
            if not child.IsPreReleased():
                return False
    return True

#-------------------------------------------------------------------------
def IsCancelOrCorrectSettlement(settlement):
    if settlement and settlement.RelationType() in [RelationType.CANCEL_CORRECT, RelationType.CANCELLATION]:
        return True
    return False

#-------------------------------------------------------------------------
def IsAcknowledgedCancelCorrectSettlement(settlement):
    if settlement.Parent() == None and settlement.RelationType() == RelationType.CANCEL_CORRECT and settlement.Status() == SettlementStatus.PENDING_CLOSURE:
        return True
    return False

#-------------------------------------------------------------------------
def IsAcknowledgedCancellationSettlement(settlement):
    if settlement.Parent() == None and settlement.RelationType() == RelationType.CANCELLATION and settlement.Status() == SettlementStatus.PENDING_CLOSURE:
        return True
    return False

#-------------------------------------------------------------------------
def CancellationSettlementHasNotBeenAcknowledged(settlement):
    if settlement.GetTopSettlementInHierarchy().RelationType() == RelationType.CANCELLATION:
        if settlement.GetTopSettlementInHierarchy().Status() not in [SettlementStatus.PENDING_CLOSURE, SettlementStatus.VOID]:
            return True
        return False
    else:
        return True

#-------------------------------------------------------------------------
def HasChildrenInNetHierarchy(settlement):
    if len(settlement.Children()) > 0 and settlement.Children().First().RelationType() in [RelationType.SECURITIES_DVP_NET, RelationType.NET]:
        return True
    return False

#-------------------------------------------------------------------------
def CancelledSettlementHasPartialParent(settlement):
    if settlement.Children() and settlement.Children().First():
        netParent = settlement.Children().First()
        if netParent.PartialParent() and netParent.PartialParent().Status() == SettlementStatus.REPLACED:
            return True
    return False

#-------------------------------------------------------------------------
def AllPartialPartsApplicableForSettlmentProcess(partialParent):
    for child in partialParent.PartialChildren():
        trades = {settlementTemp.Trade() for settlementTemp in child.Children()}
        for t in trades:
            filterHandler = Singleton.GetTradeAmendmentFilterHandler()
            if filterHandler.IsAmendmentProcessTrade(t):
                return False
    return True

#-------------------------------------------------------------------------
def IsApplicableForSettlmentProcess(trade):
    if trade:
        filterHandler = Singleton.GetTradeAmendmentFilterHandler()
        if filterHandler.IsAmendmentProcessTrade(trade):
            return False
    return True

#-------------------------------------------------------------------------
def AllPartialCancellationsAcknowledged(settlement):
    if settlement.Children():
        partialSettlement = settlement.Children().First()
        if partialSettlement and partialSettlement.PartialParent():
            partialChildren = partialSettlement.PartialParent().PartialChildren()
            for partialChild in partialChildren:
                if CancellationSettlementHasNotBeenAcknowledged(partialChild):
                    return False
            return True
    return False

#-------------------------------------------------------------------------
def CancelledSettlementHasPairOffParent(settlement):
    if settlement.Children():
        firstChild = settlement.Children().First()
        if firstChild.PairOffParent():
            return True
    return False

#-------------------------------------------------------------------------
def AllPairOffCancellationsAcknowledged(settlement):
    if settlement.Children():
        pairOffSettlement = settlement.Children().First()
        if pairOffSettlement and pairOffSettlement.PairOffParent():
            pairOffChildren = pairOffSettlement.PairOffParent().PairOffChildren()
            for pairOffChild in pairOffChildren:
                if pairOffChild.IsWaitingForCancellationAck():
                    return False
            return True
    return False

#-------------------------------------------------------------------------
def TradeFullySettledOnDate(trade, date):
    assert(trade != None)
    
    tradeSettlements = trade.Settlements()
    allSettled = True
    for settlement in tradeSettlements:
        topSettlement = settlement.GetTopSettlementInHierarchy()
        if IsActiveSecurity(topSettlement) and not topSettlement.Type() == SettlementType.REDEMPTION_SECURITY:
            if not topSettlement.IsSettled() or topSettlement.SettledDay() > date:
                allSettled = False
                break
    return (allSettled and len(tradeSettlements) > 0)

#-------------------------------------------------------------------------
def SettlementTypeFullySettledOnTrade(trade, settlementType):
    assert(trade != None)
    assert(settlementType != None)
    
    tradeSettlements = trade.Settlements()
    allSettled = True
    for settlement in tradeSettlements:
        topSettlement = settlement.GetTopSettlementInHierarchy()
        if IsActiveSecurity(topSettlement) and settlement.Type() == settlementType:
            if not topSettlement.IsSettled():
                allSettled = False
                break
    return (allSettled and len(tradeSettlements) > 0)

#-------------------------------------------------------------------------
def PartiallySettledTrade(trade):
    assert(trade != None)
    
    tradeSettlements = trade.Settlements()
    for settlement in tradeSettlements:
        topSettlement = settlement.GetTopSettlementInHierarchy()
        if IsActiveSecurity(topSettlement) and not topSettlement.Type() == SettlementType.REDEMPTION_SECURITY:
            if topSettlement.IsSettled():
                return True
    return False

#-------------------------------------------------------------------------
def IsCorrectedTradeSettlement(oldSettlement):
    if oldSettlement == None:
        return False
    if not Utils.IsCorrectingTrade(oldSettlement.Trade()) and Utils.IsCorrectedTrade(oldSettlement.Trade()):
        return True
    return False

#-------------------------------------------------------------------------
def IsCorrectedSingleRecord(settlement):
    if settlement.Children() and settlement.Children()[0].RelationType() == RelationType.CANCEL_CORRECT:
        return True
    return False

#-------------------------------------------------------------------------
def IsPartOfPairOff(settlement):
    partOfPairOff = False
    if settlement.PairOffParent():
        partOfPairOff = True
    elif settlement.PairOffChildren():
        partOfPairOff = True
    elif settlement.Children():
        for child in settlement.Children():
            if child.PairOffParent():
                partOfPairOff = True
                break
    elif settlement.GetTopNonCancellationSettlementInHierarchy().PairOffParent():
        partOfPairOff = True
    elif settlement.GetTopNonCancellationSettlementInHierarchy().PairOffChildren():
        partOfPairOff = True
    return partOfPairOff

#-------------------------------------------------------------------------
def IsPartOfPartial(settlement):
    partOfPartial = False
    if settlement.PartialParent():
        partOfPartial = True
    elif settlement.PartialChildren():
        partOfPartial = True
    elif settlement.GetTopNonCancellationSettlementInHierarchy().PartialParent():
        partOfPartial = True
    elif settlement.GetTopNonCancellationSettlementInHierarchy().PartialChildren():
        partOfPartial = True
    return partOfPartial

#-------------------------------------------------------------------------
def IsDateInInterval(date, startDate, endDate):
    return date > startDate and date <= endDate

#-------------------------------------------------------------------------
def IsTransferType(settlmentType):
    return settlmentType in [
        SettlementType.COUPON_TRANSFER,
        SettlementType.DIVIDEND_TRANSFER,
        SettlementType.FIXED_AMOUNT_TRANSFER,
        SettlementType.ACCOUNT_TRANSFER,
        SettlementType.CAPLET_TRANSFER,
        SettlementType.FLOORLET_TRANSFER
    ]

#-------------------------------------------------------------------------    
def IsAfterMaturity(instrument):
    return instrument.Underlying() and instrument.ExpiryDate() <= acm.Time.DateToday() 

#-------------------------------------------------------------------------
def IsThereAtLeastOnePostReleasedOffsettingSettlement(settlements):
    for settlement in settlements:
        if IsCreatedDueToPartiallySettledTrade(settlement):
            topMostSettlement = settlement.GetTopSettlementInHierarchy()
            if topMostSettlement == settlement:
                if not (settlement.IsPreReleased() or \
                    settlement.Status() == SettlementStatus.RECALLED):
                    return True
            elif not topMostSettlement.IsPreReleased():
                return True
    return False

#-------------------------------------------------------------------------   
def IsCreatedDueToPartiallySettledTrade(settlement):
    return settlement.IsTradeWasPartiallySettled()

#-------------------------------------------------------------------------  
def IsConsideredInSettlementAmountCalculation(settlement, instrument, date):
    topSettlement = settlement.GetTopSettlementInHierarchy()
    return settlement.RelationType() == RelationType.NONE and  settlement.ValueDay() <= date \
           and settlement.IsSecurity() and not settlement.Type() == SettlementType.REDEMPTION_SECURITY \
           and IsActiveSecurity(topSettlement) \
           and not (IsAfterMaturity(instrument) and settlement.Type() == SettlementType.SECURITY_NOMINAL)

#-------------------------------------------------------------------------  
def IsCashflowThatShouldBeOffsetted(cashFlow, instrument):
    return cashFlow.CashFlowType() not in [
        CashFlowType.TOTAL_RETURN,
        CashFlowType.CREDIT_DEFAULT,
        CashFlowType.CALL_FIXED_RATE,
        CashFlowType.CALL_FLOAT_RATE,
        CashFlowType.REDEMPTION_AMOUNT,
        CashFlowType.ZERO_COUPON_FIXED,
        CashFlowType.RETURN,
        CashFlowType.DIVIDEND,
        CashFlowType.FIXED_ADJUSTABLE,
        CashFlowType.INTEREST_REINVESTMENT,
        CashFlowType.CALL_FIXED_RATE_ADJUSTABLE,
        CashFlowType.POSITION_TOTAL_RETURN,
        CashFlowType.FIXED_PRICE,
        CashFlowType.FLOAT_PRICE,
        CashFlowType.AGGREGATED_FIXED_AMOUNT,
        CashFlowType.AGGREGATED_COUPON,
        CashFlowType.COLLARED_FLOAT
    ]

#-------------------------------------------------------------------------  
def IsInstrumentTypeWithTransfer(insType):
    return insType in [InsType.REPO_REVERSE, InsType.SECURITY_LOAN]

#-------------------------------------------------------------------------  
def HasValueDayAdjustedSetttlementInHierarchy(settlement):
    if settlement.RelationType() == RelationType.VALUE_DAY_ADJUSTED:
        return True
    for child in settlement.Children():
        if HasValueDayAdjustedSetttlementInHierarchy(child):
            return True
    return False

#-------------------------------------------------------------------------  
def IsFullyCancelled(topSettlement):
    return IsCancelOrCorrectSettlement(topSettlement) and topSettlement.Status() in [SettlementStatus.PENDING_CLOSURE, SettlementStatus.VOID]

#-------------------------------------------------------------------------  
def WaitingForCancellationAck(settlement, settlementPairs):
    if HasCorrectionTrade(settlement):
        correctionTradeSettlements = list(settlement.Trade().CorrectionTrade().Settlements().AsArray())
        for correctionSettlement in correctionTradeSettlements:
            clone = __FindCloneSettlement(correctionSettlement, settlementPairs)
            if clone:
                correctionSettlement = clone
            if correctionSettlement.IsWaitingForCancellationAck():
                return True
    return False

#-------------------------------------------------------------------------  
def HasCorrectionTrade(settlement):
    return settlement.Trade() and settlement.Trade().CorrectionTrade() and \
    settlement.Trade().CorrectionTrade() != settlement.Trade()

#-------------------------------------------------------------------------  
def __FindCloneSettlement(oldSettlement, settlementPairs):
    if oldSettlement.Parent():
        oldSettlement = oldSettlement.Parent()
    for (old, new) in settlementPairs:
        if old == oldSettlement:
            return new
    return None
