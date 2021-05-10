""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementCreationFunctions.py"
import acm
from   FSettlementCommitter import SettlementCommitter, CommitAction
from FSettlementEnums import SettlementStatus, SettlementType
from FSettlementCreatorSingleton import GetSettlementCreator
import FSettlementValidations as Validations
from FSettlementCorrectTradeRecaller import FSettlementCorrectTradeRecaller
import FSettlementGetters as Getters
import FSettlementUpdateFunctions as UpdateFunctions

#-------------------------------------------------------------------------
def CreateOffsettingSettlementAndTransfer(settlement, offsettingAmountFactor, offsettingTransferAmountFactor, cashFlow):
    committerList = list()
    if settlement and offsettingAmountFactor != 0:
        offsetSettlement = acm.FSettlement()
        offsetSettlement.Apply(settlement)
        offsetSettlement.Diary(None)
        offsetSettlement.CashFlow(None)
        offsetSettlement.Parent(None)
        offsetSettlement.Amount(settlement.Amount()*offsettingAmountFactor)
        offsetSettlement.Status(SettlementStatus.NEW)
        offsetSettlement.IsTradeWasPartiallySettled(True)
        offsetSettlement.STP()
        stateChart = acm.Operations.GetMappedSettlementProcessStateChart(offsetSettlement)
        offsetSettlement.StateChart(stateChart)        
        offsetSettlement.STP()
        committerList.append(SettlementCommitter(offsetSettlement, CommitAction.INSERT))

    if settlement and offsettingTransferAmountFactor != 0:
        offsetSettlementTransfer = acm.FSettlement()
        offsetSettlementTransfer.Apply(settlement)
        offsetSettlementTransfer.Diary(None)
        offsetSettlementTransfer.CashFlow(None)
        offsetSettlementTransfer.Parent(None)
        offsetSettlementTransfer.Type(Getters.GetSettlementTransferTypeFromSettlementType(settlement.Type()))
        offsetSettlementTransfer.Amount(settlement.Amount()*offsettingTransferAmountFactor)
        offsetSettlementTransfer.Counterparty(settlement.Trade().Counterparty())
        offsetSettlementTransfer.CounterpartyName(settlement.Trade().Counterparty().Name())
        acm.Operations.AccountAllocator().SetSettlementAccountInfo(offsetSettlementTransfer)
        offsetSettlementTransfer.Status(SettlementStatus.NEW)
        offsetSettlementTransfer.IsTradeWasPartiallySettled(True)
        offsetSettlementTransfer.STP()
        stateChart = acm.Operations.GetMappedSettlementProcessStateChart(offsetSettlementTransfer)
        offsetSettlementTransfer.StateChart(stateChart)
        offsetSettlementTransfer.STP()
        committerList.append(SettlementCommitter(offsetSettlementTransfer, CommitAction.INSERT))     

    return committerList

#-------------------------------------------------------------------------
def CreateSettlementsAfterMaturity(trade, cashFlow, logger):
    committerList = list()

    settlement = acm.Operations.CreateSettlement(cashFlow, trade, False)
    
    creator = GetSettlementCreator()
    createdSettlements = creator.CreateSettlementsFromSettlement(trade, settlement, FSettlementCorrectTradeRecaller())
    if len(createdSettlements) != 1:
        logger.LP_Log("Could not create settlement after maturity for trade {}".format(trade.Oid()))
        logger.LP_Flush()
        settlement = None
    else:
        createdSettlement = createdSettlements[0]
        createdSettlement.STP()
        stateChart = acm.Operations.GetMappedSettlementProcessStateChart(createdSettlement)
        createdSettlement.StateChart(stateChart)
        createdSettlement.STP()
        createdSettlement.IsTradeWasPartiallySettled(True)
        committerList.append(SettlementCommitter(createdSettlement, CommitAction.INSERT))
        settlement = createdSettlement

    if Validations.IsInstrumentTypeWithTransfer(trade.Instrument().InsType()):
        settlementTransfer = acm.Operations.CreateSettlement(cashFlow, trade, True)
        if settlementTransfer:
            createdSettlements = creator.CreateSettlementsFromSettlement(trade, settlementTransfer, FSettlementCorrectTradeRecaller())
            if len(createdSettlements) != 1:
                logger.LP_Log("Could not create settlement transfer after maturity for trade {}".format(trade.Oid()))
                logger.LP_Flush()
                settlement = None
            else:
                createdSettlement = createdSettlements[0]
                createdSettlement.STP()
                stateChart = acm.Operations.GetMappedSettlementProcessStateChart(createdSettlement)
                createdSettlement.StateChart(stateChart)
                createdSettlement.STP()
                createdSettlement.IsTradeWasPartiallySettled(True)
                committerList.append(SettlementCommitter(createdSettlement, CommitAction.INSERT))
    return committerList, settlement

#-------------------------------------------------------------------------
def CreateNewAndAdjustLeftOverCash(oldLeftOverCash, cashSettlementsToMerge):
    newLeftOverCash = acm.FSettlement()
    newLeftOverCash.Apply(oldLeftOverCash)
    newLeftOverCash.Owner(oldLeftOverCash.Owner())
    newLeftOverCash.Protection(oldLeftOverCash.Protection())
    newLeftOverCash.Status(SettlementStatus.NEW)
    newLeftOverCash.Parent(None)
    newLeftOverCash.PartialParent(None)
    newLeftOverCash.PairOffParent(oldLeftOverCash.PairOffParent())

    return UpdateFunctions.AdjustLeftOverCash(newLeftOverCash, cashSettlementsToMerge)

#-------------------------------------------------------------------------
def RecreateSettlementsInHiearchies(settlements):
    
    allOldHierarchies = set()
    allTrades = set()
    for settlement in settlements:
        oldHierarchy = list()
        if not Validations.IsCorrectedSingleRecord(settlement):
            Getters.GetBottomMostChildren(settlement, oldHierarchy)
        if len(oldHierarchy) == 0:
            oldHierarchy.append(settlement)
        trades = [settlementTemp.Trade() for settlementTemp in oldHierarchy if settlementTemp.Trade()]
        if settlement.Trade() and settlement.Trade():
            trades.append(settlement.Trade())
        allOldHierarchies = allOldHierarchies.union(oldHierarchy)
        allTrades = allTrades.union(trades)

    recreatedSettlements = RecreateSettlementsForTrades(list(allTrades), list(allOldHierarchies))

    committerList = Getters.GetSettlementCommitterListInsertOnly(recreatedSettlements, FSettlementCorrectTradeRecaller())
    return committerList

#-------------------------------------------------------------------------
def RecreateSettlementsForTrades(trades, oldSettlements):
    settlementCorrectTradeRecaller = FSettlementCorrectTradeRecaller()
    settlementList = list()

    for trade in trades:
        oldSettlementsForTrade = [settlementTemp for settlementTemp in oldSettlements if settlementTemp.Trade()==trade]
        settlementPairs = Getters.GetMatchedSettlementPairs(oldSettlementsForTrade, trade, settlementCorrectTradeRecaller)
        setToPendingAmendment = not Validations.IsApplicableForSettlmentProcess(trade)
        leftOverCash = None
        pairOffSecurityCreated = False
        for (old, new) in settlementPairs:
            if old and new:
                createdLeftOverCash = False
                if setToPendingAmendment:
                    new.Status(SettlementStatus.PENDING_AMENDMENT)
                if old.PairOffParent():
                    pairOffSecurityCreated = pairOffSecurityCreated or new.IsSecurity()
                    new.PairOffParent(old.PairOffParent())
                    if not old.IsSecurity():
                        oldPairOffHiearchyCashChildren = Getters.GetAllCashChildrenWithTrade(old.PairOffParent(), old.Trade())
                        newCashSettlements = RecreateSettlementsForTrades([old.Trade()], oldPairOffHiearchyCashChildren)
                        UpdateFunctions.AdjustLeftOverCash(new, newCashSettlements)
                        leftOverCash = new
                        createdLeftOverCash = True
                if not createdLeftOverCash:
                    settlementList.append(new)
            if old and not new:
                if old.PairOffParent() and not old.IsSecurity():
                    oldPairOffHiearchyCashChildren = Getters.GetAllCashChildrenWithTrade(old.PairOffParent(), old.Trade())
                    newCashSettlements = RecreateSettlementsForTrades([old.Trade()], oldPairOffHiearchyCashChildren)
                    leftOverCash = CreateNewAndAdjustLeftOverCash(old, newCashSettlements)
        if leftOverCash and (leftOverCash.Amount() != 0 or pairOffSecurityCreated):
            if not pairOffSecurityCreated:
                leftOverCash.Type(SettlementType.PAIR_OFF_PAYMENT)
            settlementList.append(leftOverCash)
    return settlementList