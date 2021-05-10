""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementSecurityProcessEngine.py"
"""----------------------------------------------------------------------------
MODULE
    FSettlementSecurityProcessEngine - Handles the workflow for security settlements

    (c) Copyright 2016 FIS Global. All rights reserved.

DESCRIPTION

----------------------------------------------------------------------------"""

import acm
import FOperationsUtils as Utils
from   FSettlementEnums import SettlementStatus, SettlementType, RelationType
from   FSettlementCommitter import SettlementCommitter, CommitAction
import FSettlementUpdater as Updater
import FSettlementValidations as Validations
import FSettlementGetters as Getters
import FSettlementActions as Actions
import FSettlementDeleters as Deleters
import FSettlementCreationFunctions as Creators

#-------------------------------------------------------------------------
# Security settlement processing engine  - used by FSettlementProcess
#-------------------------------------------------------------------------

class SecurityProcessEngine(object):

    #-------------------------------------------------------------------------
    @staticmethod
    def Process(settlements, trade):
        processedSettlementIDs = list()
        oldSettlements = list()
        newSettlements = list()
        committerList = list()

        if settlements:
            for settlement in settlements:
                settlementToProcess = SecurityProcessEngine._GetSettlementToProcess(settlement, trade, committerList)
                if settlementToProcess and settlementToProcess.Oid() not in processedSettlementIDs:
                    if settlementToProcess.PairOffChildren():
                        SecurityProcessEngine._ProcessPairOff(settlementToProcess, oldSettlements, newSettlements, committerList)
                    elif settlementToProcess.PartialChildren():
                        SecurityProcessEngine.ProcessPartial(settlementToProcess, committerList)
                    else:
                        SecurityProcessEngine._ProcessDefault(settlementToProcess, oldSettlements, newSettlements)

                    processedSettlementIDs.append(settlementToProcess.Oid())
        else:
            SecurityProcessEngine._ProcessAmendmentSettlements(trade, committerList)

        return oldSettlements, newSettlements, committerList

    #-------------------------------------------------------------------------
    @staticmethod
    def _ProcessPairOff(pairOffParent, oldSettlements, newSettlements, committerList):
        parents = list()
        shouldRecreate = True
        settlementsToRecreate = list()
        updatedSingleRecordSettlements = list()
        if not pairOffParent.IsSettled():
            pairOffParent.Status(SettlementStatus.EXCEPTION)
            pairOffParent.IsChangeToSourceData(True)
            committerList.append(SettlementCommitter(pairOffParent, CommitAction.UPDATE))
            for pairOffChild in pairOffParent.PairOffChildren():
                if pairOffChild.Status() == SettlementStatus.VOID and pairOffChild.GetTopSettlementInHierarchy().RelationType() == RelationType.CANCELLATION:
                    cancellationParent = pairOffChild.GetTopSettlementInHierarchy()
                    cancellationParent.Status(SettlementStatus.EXCEPTION)
                    cancellationParent.IsChangeToSourceData(True)
                    committerList.append(SettlementCommitter(cancellationParent, CommitAction.UPDATE))
        else:
            for pairOffChild in pairOffParent.PairOffChildren():
                if pairOffChild.Status() not in [SettlementStatus.REPLACED, SettlementStatus.CANCELLED]:
                    pairOffChild = pairOffChild.GetTopNonCancellationSettlementInHierarchy()
                    if pairOffChild.Oid() not in parents and not pairOffChild.Type() == SettlementType.PAIR_OFF_PAYMENT:
                        parents.append(pairOffChild.Oid())
                        if pairOffChild.IsPreReleased():
                            if pairOffChild.Status() == SettlementStatus.PENDING_AMENDMENT:
                                pairOffChild.Status(SettlementStatus.NEW)
                                pairOffChild.STP()
                            settlementsToRecreate.append(pairOffChild)
                        else:
                            shouldRecreate = False
                        if pairOffChild.IsSecurity():
                            oldSettlementsTemp, newSettlementsTemp = SecurityProcessEngine._PerformCancelOrCorrect(pairOffChild)
                            oldSettlements.extend(oldSettlementsTemp)
                            newSettlements.extend(newSettlementsTemp)
                            if (not pairOffChild.Children() or Validations.IsCorrectedSingleRecord(pairOffChild)) and newSettlementsTemp:
                                updatedSingleRecordSettlements.append(newSettlementsTemp[0])
                        else:
                            oldSettlementsTemp, newSettlementsTemp = Actions.InstructToCancel(pairOffChild)
                            oldSettlements.extend(oldSettlementsTemp)
                            newSettlements.extend(newSettlementsTemp)
                            if (not pairOffChild.Children() or Validations.IsCorrectedSingleRecord(pairOffChild)) and newSettlementsTemp:
                                updatedSingleRecordSettlements.append(newSettlementsTemp[0])
            if shouldRecreate:
                committerListTemp = Creators.RecreateSettlementsInHiearchies(settlementsToRecreate)
                committerList.extend(committerListTemp)
                for settlementToRecreate in settlementsToRecreate:
                    if settlementToRecreate.Children() and not Validations.IsCorrectedSingleRecord(settlementToRecreate):
                        childrenInHiearchy = list()
                        Getters.GetAllChildrenInHierarchy(settlementToRecreate, childrenInHiearchy)
                        for child in childrenInHiearchy:
                            child.Status(SettlementStatus.CANCELLED)
                            child.PairOffParent(None)
                            committerList.append(SettlementCommitter(child, CommitAction.UPDATE))
                    else:
                        for updatedSingleRecordSettlement in updatedSingleRecordSettlements:
                            updatedSingleRecordSettlement.Status(SettlementStatus.CANCELLED)
                            updatedSingleRecordSettlement.PairOffParent(None)

    #-------------------------------------------------------------------------
    @staticmethod
    def ProcessPartial(partialParent, committerList):
        if Validations.AllPartialPartsApplicableForSettlmentProcess(partialParent):
            reCreated = False
            topPartialParent = Getters.GetTopPartialParentInPartialHierarchy(partialParent)
            if Validations.ProcessAsPreReleased(partialParent):
                committerListTemp = Creators.RecreateSettlementsInHiearchies([topPartialParent])
                committerList.extend(committerListTemp)
                committerListTemp = SecurityProcessEngine._DeletePartialHierarchy(partialParent)
                committerList.extend(committerListTemp)
                reCreated = True
            else:
                allSettled = True
                shouldRecreate = True
                for partialChild in partialParent.PartialChildren():
                    if not partialChild.IsSettled():
                        allSettled = False
                    if not partialChild.IsPreReleased() and not partialChild.IsSettled() and not partialChild.Status() == SettlementStatus.REPLACED:
                        shouldRecreate = False
                    if Validations.IsPostReleasedSettlement(partialChild) or partialChild.IsPreReleased():
                        if partialChild.Status() == SettlementStatus.PENDING_AMENDMENT:
                            partialChild.Status(SettlementStatus.NEW)
                            partialChild.STP()
                        cancelChildren = partialChild.IsPreReleased()
                        oldSettlementsTemp, newSettlementsTemp = Actions.InstructToCancel(partialChild)
                        oldSettl = oldSettlementsTemp[0]
                        newSettl = newSettlementsTemp[0]
                        cancSettl = newSettlementsTemp[1]
                        Updater.Apply(oldSettl, newSettl, False)
                        committerList.append(SettlementCommitter(oldSettl, CommitAction.UPDATE))
                        committerList.append(SettlementCommitter(cancSettl, CommitAction.INSERT))
                        if cancelChildren:
                            childrenInHiearchy = list()
                            Getters.GetAllChildrenInHierarchy(partialChild, childrenInHiearchy)
                            for child in childrenInHiearchy:
                                child.Status(SettlementStatus.CANCELLED)
                                committerList.append(SettlementCommitter(child, CommitAction.UPDATE))
                if allSettled:
                    Utils.LogVerbose('Settlement {} will not be updated as the settlements for trade {} is fully settled'.format(partialParent.Oid(), partialParent.Trade().Oid()))
                if shouldRecreate:
                    committerListTemp = Creators.RecreateSettlementsInHiearchies([topPartialParent])
                    committerList.extend(committerListTemp)
                    reCreated = True

            if reCreated and (not Validations.ProcessAsPreReleased(partialParent) or topPartialParent != partialParent):
                bottomMostChild = list()
                Getters.GetBottomMostChildren(topPartialParent, bottomMostChild)
                for settlement in bottomMostChild:
                    if settlement.PairOffParent():
                        settlement.PairOffParent(None)
                        committerList.append(SettlementCommitter(settlement, CommitAction.UPDATE))

    #-------------------------------------------------------------------------
    @staticmethod
    def _ProcessDefault(settlement, oldSettlements, newSettlements):
        if Validations.IsCancelOrCorrectSettlement(settlement.GetTopSettlementInHierarchy()):
            Utils.LogVerbose('Settlement {} will not be updated as it is being canceled'.format(settlement.Oid()))

        elif not Validations.ProcessAsPreReleased(settlement):
            oldSettlementsTemp, newSettlementsTemp = SecurityProcessEngine._PerformCancelOrCorrect(settlement)
            oldSettlements.extend(oldSettlementsTemp)
            newSettlements.extend(newSettlementsTemp)

    #-------------------------------------------------------------------------
    @staticmethod
    def _ProcessAmendmentSettlements(trade, committerList):
        settlementsInPendingAmendment = Getters.GetSettlementsInPendingAmendment(trade)
        for settlement in settlementsInPendingAmendment:
            settlement.Status(SettlementStatus.NEW)
            settlement.STP()
            committerList.append(SettlementCommitter(settlement, CommitAction.UPDATE))

    #-------------------------------------------------------------------------
    @staticmethod
    def _GetSettlementToProcess(settlement, trade, committerList):
        settlementToProcess = settlement
        if (not settlementToProcess.PairOffParent() or settlementToProcess.GetTopNonCancellationSettlementInHierarchy().PartialChildren()):
            settlementToProcess = settlementToProcess.GetTopNonCancellationSettlementInHierarchy()
        if settlementToProcess.PartialParent() and not settlementToProcess.PartialChildren():
            settlementToProcess = settlementToProcess.PartialParent()
        if settlementToProcess.PairOffParent() and not settlementToProcess.PartialChildren():
            settlementToProcess = settlementToProcess.PairOffParent()

        securityType = settlement.Type()
        if not settlement.IsSecurity():
            for child in settlementToProcess.Children():
                if child.IsSecurity() and child.Trade() == trade:
                    securityType = child.Type()
        if Validations.SettlementTypeFullySettledOnTrade(trade, securityType):
            if settlement.Status() == SettlementStatus.PENDING_AMENDMENT:
                #Handle Pair Off Payments in Pending Amendment
                settlement.Status(SettlementStatus.NEW)
                settlement.STP()
                committerList.append(SettlementCommitter(settlement, CommitAction.UPDATE))            
            Utils.LogVerbose('Securities settlements for trade {} will not be updated as it is fully settled'.format(trade.Oid()))
            settlementToProcess = None
        return settlementToProcess

    #-------------------------------------------------------------------------
    @staticmethod
    def _DeletePartialHierarchy(settlement):
        committerList = list()
        canDeletePartialParent = not Validations.IsPartOfPairOff(settlement) and not settlement.PartialParent() and not Validations.IsCorrectedSingleRecord(settlement)
        if canDeletePartialParent:
            committerList.append(SettlementCommitter(settlement, CommitAction.DELETE))
        else:
            oldSettlementsTemp, newSettlementsTemp = Actions.InstructToCancel(settlement)
            oldSettl = oldSettlementsTemp[0]
            newSettl = newSettlementsTemp[0]
            cancSettl = newSettlementsTemp[1]
            Updater.Apply(oldSettl, newSettl, False)
            oldSettl.PairOffParent(None)
            committerList.append(SettlementCommitter(oldSettl, CommitAction.UPDATE))
            committerList.append(SettlementCommitter(cancSettl, CommitAction.INSERT))
            childrenInHiearchy = list()
            Getters.GetAllChildrenInHierarchy(settlement, childrenInHiearchy)
            for child in childrenInHiearchy:
                child.Status(SettlementStatus.CANCELLED)
                child.PairOffParent(None)
                committerList.append(SettlementCommitter(child, CommitAction.UPDATE))
        for partialChild in settlement.PartialChildren():
            Deleters.DeleteHierarchy(partialChild, committerList)
        if canDeletePartialParent:
            for child in settlement.Children():
                Deleters.DeleteHierarchy(child, committerList)

        return committerList

    #-------------------------------------------------------------------------
    @staticmethod
    def _PerformCancelOrCorrect(settlement):
        newSettlements = list()
        oldSettlements = list()
        if Validations.IsAcknowledgedSecuritySettlement(settlement):
            if settlement.Trade() and settlement.Trade().Status() == SettlementStatus.VOID and not Utils.IsCorrectedTrade(settlement.Trade()):
                oldSettlements, newSettlements = Actions.InstructToCancel(settlement)
            else:
                oldSettlements, newSettlements = Actions.InstructToCorrect(settlement)
        elif Validations.IsPreReleasedSecuritySettlement(settlement):
            oldSettlements, newSettlements = Actions.InstructToCancel(settlement)
        return oldSettlements, newSettlements
