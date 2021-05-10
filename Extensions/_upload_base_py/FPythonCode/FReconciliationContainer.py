""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/business_data_upload/../reconciliation/etc/FReconciliationContainer.py"
"""--------------------------------------------------------------------------
MODULE
    FReconciliationContainer

    (c) Copyright 2012 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""
import acm
import FAssetManagementUtils

logger = FAssetManagementUtils.GetLogger()

class FReconciliationInstance(object):

    def __init__(self, reconciliationSpecification, fileName=None, forceReRun=False, reconDocument=None):
        self._fileName = fileName
        self._forceReRun = forceReRun
        self._reconciliationDocument = reconDocument
        self._reconciliationSpecification = reconciliationSpecification
        self._workflows = []
        self._unclosedWorkflows = []
        self._calculationParams = dict()
        self._reconciliationItemsLoaded = 0
        self._missingACMObjectCount = 0
        self._removedClosedItems = list()
        self._maxNbrOfUnclosedWfsCount = self.ReconciliationSpecification().MaxNbrOfUnclosedReconItems()

    def FileName(self):
        return self._fileName

    def ForceReRun(self):
        return self._forceReRun

    def Add(self, workflow):
        assert workflow
        assert workflow.ReconciliationItem()
        if not workflow.ReconciliationItem().ExternalValues().IsEmpty():
            self.TickReconciliationItemsLoaded(+1)
        elif workflow.ReconciliationItem().Subject() is not None:
            self.TickMissingACMObjectCount(+1)
        self.Workflows().append(workflow)
        self.ReconciliationDocument().ReconciliationItems().Add(workflow.ReconciliationItem())

    def Remove(self, workflow):
        assert workflow
        assert workflow.ReconciliationItem()
        assert self.ReconciliationDocument()
        if workflow in self.Workflows():
            logger.debug('Removing workflow for reconciliation item %i', workflow.ReconciliationItem().Oid())
            if not workflow.ReconciliationItem().ExternalValues().IsEmpty():
                self.TickReconciliationItemsLoaded(-1)
            elif workflow.ReconciliationItem().Subject() is not None:
                self.TickMissingACMObjectCount(-1)
            self.Workflows().remove(workflow)
            self.ReconciliationDocument().ReconciliationItems().Remove(workflow.ReconciliationItem())
            if workflow.IsClosed():
                self.RemovedClosedItems(workflow)

    def TickMissingACMObjectCount(self, tickSize):
        self._missingACMObjectCount += tickSize

    def TickReconciliationItemsLoaded(self, tickSize):
        self._reconciliationItemsLoaded += tickSize

    def MaxNbrOfUnclosedWorkflowItems(self):
        return self._maxNbrOfUnclosedWfsCount

    def RemovedClosedItems(self, item = None):
        if item is None:
            return self._removedClosedItems
        self._removedClosedItems.append(item)

    def UnclosedWorkflows(self, workflow=None):
        if workflow is None:
            return self._unclosedWorkflows
        self._unclosedWorkflows.append(workflow)

    def NbrOfReconciliationItems(self):
        return len(self.ReconciliationItems())

    def NbrOfUnclosedWorkflows(self):
        return len(self._unclosedWorkflows)

    def NbrOfRemovedClosedItems(self):
        return len(self._removedClosedItems)

    def CreateReconciliationDocument(self):
        reconciliationDocument = acm.FReconciliationDocument()
        assert (self.FileName() is not None and self.ReconciliationSpecification().ReconciliationObjectType() \
               is not None and self.ReconciliationSpecification().Name() is not None)
        reconciliationDocument.SourceId(self.FileName())
        reconciliationDocument.ObjectType(self.ReconciliationSpecification().ReconciliationObjectType() \
                if not self.ReconciliationSpecification().ReconciliationObjectType() == 'Order' else 'Trade')
        reconciliationDocument.ReconciliationName(self.ReconciliationSpecification().Name())
        return reconciliationDocument

    def ReconciliationDocument(self, document=None):
        if document:
            self._reconciliationDocument = document
        elif self._reconciliationDocument is None:
            self._reconciliationDocument = self.CreateReconciliationDocument()
        return self._reconciliationDocument

    def ReconciliationSpecification(self):
        return self._reconciliationSpecification

    def Workflows(self):
        return self._workflows

    def ReconciliationItems(self):
        reconItems = [w.ReconciliationItem() for w in self.Workflows()]
        return reconItems

    def Commit(self):
        self._PrepareDocumentForCommit()
        self.ReconciliationDocument().Commit()

    def CalculationParams(self, calculationParams=None):
        if calculationParams is None:
            return self._calculationParams
        self._calculationParams = calculationParams

    def ReconciliationItemsLoaded(self):
        return self._reconciliationItemsLoaded

    def _PrepareDocumentForCommit(self):
        processedItemCount = len(self.Workflows())
        reconciliationDocument = self.ReconciliationDocument()
        if reconciliationDocument.Originator().IsInfant() and self.ForceReRun():
            # Do not overwrite the processed item count for re-run processes
            self.ReconciliationDocument().ProcessedItemCount(processedItemCount)
        for key in self._calculationParams:
            self.ReconciliationDocument().SetProperty(key, self._calculationParams[key])