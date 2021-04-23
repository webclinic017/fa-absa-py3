""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementSecurityUpdateEngine.py"
"""----------------------------------------------------------------------------
MODULE
    FSettlementSecurityUpdater - Handles updates for the settlement security
                                 workflow

    (c) Copyright 2016 FIS Global. All rights reserved.

DESCRIPTION

----------------------------------------------------------------------------"""

import acm
import FOperationsUtils as Utils
import FSettlementUpdater as Updater
from   FSettlementCommitter import SettlementCommitter, CommitAction
from   FSettlementCorrectTradeRecaller import FSettlementCorrectTradeRecaller
from   FSettlementTransactionCommitter import TransactionCommitter
from   FSettlementEnums import RelationType, SettlementStatus, SettlementType
from   FOperationsExceptions import CommitException  
import FSettlementValidations as Validations
import FSettlementGetters as Getters
import FSettlementActions as Actions
import FSettlementProcessFunctions as Process
import FSettlementCreationFunctions as Creators
import FSettlementSelectorConditionFunctions as SelectorConditionFunctions

#-------------------------------------------------------------------------
# Security settlement update engine  - used by FSettlementProcess
#-------------------------------------------------------------------------

class SecurityUpdateEngine(object):

    def __init__(self, nettingRuleQueryCache):
        self.__nettingRuleQueryCache = nettingRuleQueryCache
    
    #-------------------------------------------------------------------------
    def UpdateSettlementsAfterOperationsDocumentChange(self, settlement, msg):
        if not settlement:
            return

        if Validations.IsAcknowledgedCancelCorrectSettlement(settlement):
            self._ProcessAcknowledgedCancelCorrect(settlement)
        elif Validations.IsAcknowledgedCancellationSettlement(settlement):
            self._ProcessAcknowledgedCancellation(settlement, msg)

    #-------------------------------------------------------------------------
    def _ProcessAcknowledgedCancelCorrect(self, settlement):
        if Validations.HasChildrenInNetHierarchy(settlement) or Validations.HasValueDayAdjustedSetttlementInHierarchy(settlement):
            self._CreateAndReprocessNetHierarchy(settlement.Children().First())
        else:
            self._CreateAndReprocessSingleRecord(settlement)

    #-------------------------------------------------------------------------
    def _ProcessAcknowledgedCancellation(self, settlement, msg):
        self._CancelChildren(settlement)
        if Validations.CancelledSettlementHasPairOffParent(settlement):
            self._ProcessPairOffUpdate(settlement)
        elif Validations.CancelledSettlementHasPartialParent(settlement):
            self._ProcessPartialUpdate(settlement, msg)

    #-------------------------------------------------------------------------
    def _CreateAndReprocessSingleRecord(self, settlement):
        settlementPairs = Getters.GetMatchedSettlementPairs([settlement.Children().First()], settlement.Trade(), FSettlementCorrectTradeRecaller())
        newSettl = None
        oldSettl = None

        for (old, new) in settlementPairs:
            if old and new:
                newSettl = new
                oldSettl = old
                break
            if old and not new:
                oldSettl = old
                break

        if (oldSettl and newSettl) or Validations.IsCorrectedTradeSettlement(oldSettl) or oldSettl:
            oldSettl.Status(SettlementStatus.CANCELLED)

            if newSettl:
                newSettl.RegisterInStorage()
                newSettl.PostSettleAction(False)
                newSettl.Status(SettlementStatus.AUTHORISED)
                newSettl.RelationType(RelationType.NONE)
                newSettl.PartialSettlementType(settlement.PartialSettlementType())
                newSettl.PairOffParent(oldSettl.PairOffParent())
                newSettl.STP()

                settlement.Parent(newSettl)
                settlement.Status(SettlementStatus.CANCELLED)

            oldSettl.PairOffParent(None)
            commitList = self._ReprocessCorrectionTradeSettlements([settlement.Trade()])

            acm.BeginTransaction()

            for settlementCommit in commitList:
                settlementCommit.Commit()

            SettlementCommitter(oldSettl, CommitAction.UPDATE).Commit()
            if newSettl:
                SettlementCommitter(newSettl, CommitAction.INSERT).Commit()
            SettlementCommitter(settlement, CommitAction.UPDATE).Commit()

            try:
                acm.CommitTransaction()
            except Exception as error:
                acm.AbortTransaction()
                Utils.LogAlways('Error while committing security settlements hierarchy: %s' % (str(error)))

    #-------------------------------------------------------------------------
    def _CreateAndReprocessNetHierarchy(self, netParent):
        newNetParent = None
        child = None

        try:
            acm.BeginTransaction()
            self._CancelExistingHierarchy(netParent)
            acm.CommitTransaction()
        except Exception as error:
            acm.AbortTransaction()
            Utils.LogAlways('Error while committing settlements: %s' % str(error))
            return

        oldSettlements = list()
        
        Getters.GetBottomMostChildren(netParent, oldSettlements)
        trades = {settlementTemp.Trade() for settlementTemp in oldSettlements}
        newSettlements = Creators.RecreateSettlementsForTrades(trades, oldSettlements)
        if len(newSettlements) > 0:
            child = newSettlements[0]
        committerList = Getters.GetSettlementCommitterListInsertOnly(newSettlements, FSettlementCorrectTradeRecaller())
        committerListTemp = self._ReprocessCorrectionTradeSettlements(trades)
        committerList.extend(committerListTemp)
        tc  = TransactionCommitter(committerList, None, self.__nettingRuleQueryCache)
        try:
            tc.CommitSettlements()
        except CommitException as error:
            Utils.LogAlways('Error while committing new security settlements hierarchy: %s' % (str(error)))
            return

        acm.BeginTransaction()
        try:
            bottomMostChildren = list()
            Getters.GetBottomMostChildren(netParent, bottomMostChildren)
            for oldSettl in bottomMostChildren:
                if oldSettl.PairOffParent():
                    oldSettl.PairOffParent(None)
                    SettlementCommitter(oldSettl, CommitAction.UPDATE).Commit()
            acm.CommitTransaction()
        except CommitException as error:
            Utils.LogAlways('Error while removing pair off parent reference from settlement: %s' % (str(error)))
            acm.AbortTransaction()
            return

        if child and child.GetTopNonCancellationSettlementInHierarchy():
            newNetParent = child.GetTopNonCancellationSettlementInHierarchy()
        self._SetCorrectionSettlementReference(newNetParent, netParent)

    #-------------------------------------------------------------------------
    def _CancelChildren(self, cancellation):
        if Validations.HasChildrenInNetHierarchy(cancellation) or Validations.HasValueDayAdjustedSetttlementInHierarchy(cancellation):
            try:
                acm.BeginTransaction()
                self._CancelExistingHierarchy(cancellation.Children().First())
                acm.CommitTransaction()
            except Exception as error:
                acm.AbortTransaction()
                Utils.LogAlways('Error while committing cancelled settlements: %s' % (str(error)))
        else:
            settlementToCancel = cancellation.Children().First()
            settlementToCancel.Status(SettlementStatus.CANCELLED)
            try:
                settlementToCancel.Commit()
            except Exception as error:
                Utils.LogAlways('Error while committing cancelled settlement: %s' % (str(error)))

    #-------------------------------------------------------------------------
    def _ProcessPairOffUpdate(self, settlement):
        if Validations.AllPairOffCancellationsAcknowledged(settlement):
            if settlement.Children():
                cancelledSettlement = settlement.Children().First()
                pairOffParent = cancelledSettlement.PairOffParent()
                if pairOffParent:
                    pairOffChildren = pairOffParent.PairOffChildren()
                    committerList = self._ReprocessSettlementsInAwaitingCancellation(pairOffChildren)
                    # Committed separately due to forced net hierarchy
                    committerListPairOffHierarchy = self._ProcessPairOffParentUpdate(pairOffParent)
                    tc  = TransactionCommitter(committerList, None, self.__nettingRuleQueryCache)
                    try:
                        acm.BeginTransaction()
                        for committer in committerListPairOffHierarchy:
                            committer.Commit()
                        tc.CommitSettlementsWithoutTransaction()
                        acm.CommitTransaction()
                    except CommitException as error:
                        Utils.LogAlways('Error while committing pair off hierarchy settlements: %s' % (str(error)))
                        acm.AbortTransaction()

    #-------------------------------------------------------------------------
    def _ProcessPartialUpdate(self, settlement, msg):
        partialSettlementSibling = Getters.GetSiblingPartialSettlement(settlement)
        if not Validations.IsCancelOrCorrectSettlement(partialSettlementSibling.GetTopSettlementInHierarchy()) or partialSettlementSibling.IsPairedOff():
            if partialSettlementSibling.IsPreReleased() or partialSettlementSibling.Status() == SettlementStatus.VOID:
                self._CancelPartialChild(partialSettlementSibling)
                self._RecreateOriginalHierarchyOrUpdateExisting(settlement, msg)
            else:
                if partialSettlementSibling.IsSettled() or partialSettlementSibling.IsPairedOff():
                    self._RecreateOriginalHierarchyOrUpdateExisting(settlement, msg)
                else:
                    if partialSettlementSibling.Status() == SettlementStatus.REPLACED:
                        self._RecreateOriginalHierarchyOrUpdateExisting(settlement, msg)
                    else:
                        self._CancelPartialChild(partialSettlementSibling)
        elif Validations.AllPartialCancellationsAcknowledged(settlement):
            self._RecreateOriginalHierarchyOrUpdateExisting(settlement, msg)

    #-------------------------------------------------------------------------
    def _ReprocessCorrectionTradeSettlements(self, trades):
        committerList = list()
        for trade in trades:
            correctedTrade = trade.CorrectedTrade()
            if correctedTrade:
                shouldReprocessAwaitingCancellation = True
                for settlement in trade.Settlements():
                    if settlement.IsWaitingForCancellationAck():
                        shouldReprocessAwaitingCancellation = False
                        break
                if shouldReprocessAwaitingCancellation:
                    committerListTemp = self._ReprocessSettlementsInAwaitingCancellation(correctedTrade.Settlements())
                    committerList.extend(committerListTemp)
        return committerList

    #-------------------------------------------------------------------------
    def _CancelExistingHierarchy(self, netParent):
        #Cancel the existing hierarchy and net parent
        for childSettlement in netParent.Children():
            self._CancelExistingHierarchy(childSettlement)

        netParent.Status(SettlementStatus.CANCELLED)
        SettlementCommitter(netParent, CommitAction.UPDATE).Commit()

    #-------------------------------------------------------------------------
    def _SetCorrectionSettlementReference(self, newNetParent, originalNetParent):
        try:
            if newNetParent:
                newNetParent.CorrectionSettlement(originalNetParent.Parent())
                SettlementCommitter(newNetParent, CommitAction.UPDATE).Commit()
        except Exception as error:
            Utils.RaiseCommitException(error)
            Utils.LogAlways('Error while committing security settlements hierarchy: %s' % (str(error)))

    #-------------------------------------------------------------------------
    def _ReprocessSettlementsInAwaitingCancellation(self, settlements):
        committerList = list()
        for settlement in settlements:
            settlementToProcess = settlement.GetTopSettlementInHierarchy()
            if settlementToProcess.Status() == SettlementStatus.AWAITING_CANCELLATION:
                settlementToProcess.Status(SettlementStatus.NEW)
                if settlementToProcess.IsValidForSTP():
                    settlementToProcess.STP()
                stateChart = acm.Operations.GetMappedSettlementProcessStateChart(settlementToProcess)
                settlementToProcess.StateChart(stateChart)
                committerList.append(SettlementCommitter(settlementToProcess, CommitAction.UPDATE))
        return committerList

    #-------------------------------------------------------------------------
    def _ProcessPairOffParentUpdate(self, pairOffParent):
        committerList = list()
        pairOffParent.Status(SettlementStatus.PAIRED_OFF)
        pairOffParent.SettledDay(pairOffParent.ValueDay())
        pairOffParent.SettledAmount(pairOffParent.CashAmount())
        committerList.append(SettlementCommitter(pairOffParent, CommitAction.UPDATE))
        for child in pairOffParent.Children():
            child.SettledDay(pairOffParent.ValueDay())
            child.SettledAmount(child.Amount())
            committerList.append(SettlementCommitter(child, CommitAction.UPDATE))
        return committerList

    #-------------------------------------------------------------------------
    def _CancelPartialChild(self, settlement):
        if not settlement:
            return
        committerList = list()
        oldSettlementsTemp, newSettlementsTemp = Actions.InstructToCancel(settlement)
        cancelChildren = settlement.IsPreReleased()
        oldSettl = oldSettlementsTemp[0]
        newSettl = newSettlementsTemp[0]
        cancSettl = newSettlementsTemp[1]
        Updater.Apply(oldSettl, newSettl, False)
        committerList.append(SettlementCommitter(oldSettl, CommitAction.UPDATE))
        committerList.append(SettlementCommitter(cancSettl, CommitAction.INSERT))
        if cancelChildren:
            childrenInHiearchy = list()
            Getters.GetAllChildrenInHierarchy(settlement, childrenInHiearchy)
            for child in childrenInHiearchy:
                child.Status(SettlementStatus.CANCELLED)
                committerList.append(SettlementCommitter(child, CommitAction.UPDATE))

        tc  = TransactionCommitter(committerList, None, self.__nettingRuleQueryCache)
        try:
            tc.CommitSettlements()
        except CommitException as error:
            Utils.LogAlways('Error while committing new security settlements hierarchy: %s' % (str(error)))
            return

    #-------------------------------------------------------------------------
    def _RecreateOriginalHierarchyOrUpdateExisting(self, settlement, msg):
        #Regenerate settlements and recreate the hierarchy
        if settlement.Children():
            if settlement.Children().First() and settlement.Children().First().PartialParent():
                partialParent = settlement.Children().First().PartialParent()
                topPartialParent = Getters.GetTopPartialParentInPartialHierarchy(partialParent)

                trades = {settlementTemp.Trade() for settlementTemp in partialParent.Children()}
                if partialParent.Trade():
                    trades.add(partialParent.Trade())

                bottomMostChildren = list()

                Getters.GetBottomMostChildren(partialParent, bottomMostChildren)

                tradesToUpdate = set()
                tradesToRecreate = set()

                for child in bottomMostChildren:
                    if SelectorConditionFunctions.IsInactivePartial(child):
                        tradesToUpdate.add(child.Trade())
                    else:
                        tradesToRecreate.add(child.Trade())

                bottomMostChildrenOfTopPartialParent = list()

                Getters.GetBottomMostChildren(topPartialParent, bottomMostChildrenOfTopPartialParent)

                recreatedSettlements = Creators.RecreateSettlementsForTrades(list(tradesToRecreate), bottomMostChildrenOfTopPartialParent)
                committerList = Getters.GetSettlementCommitterListInsertOnly(recreatedSettlements, FSettlementCorrectTradeRecaller())

                settlementCorrectTradeRecaller = FSettlementCorrectTradeRecaller()

                for trade in list(tradesToUpdate):
                    Process.CreateSettlementsFromTrade(trade, msg, self.__nettingRuleQueryCache)

                bottomMostChild = list()
                Getters.GetBottomMostChildren(topPartialParent, bottomMostChild)
                for settlement in bottomMostChild:
                    if settlement.PairOffParent():
                        settlement.PairOffParent(None)
                        committerList.append(SettlementCommitter(settlement, CommitAction.UPDATE))

                committerListTemp = self._ReprocessCorrectionTradeSettlements(list(trades))
                committerList.extend(committerListTemp)
                tc  = TransactionCommitter(committerList, None, self.__nettingRuleQueryCache)
                try:
                    tc.CommitSettlements()
                except CommitException as error:
                    Utils.LogAlways('Error while committing new security settlements hierarchy: %s' % (str(error)))
