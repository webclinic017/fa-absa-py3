""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/reconciliation/./etc/FReconciliationEngine.py"
"""--------------------------------------------------------------------------
MODULE
    FReconciliationEngine

    (c) Copyright 2016 FIS Front Arena. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""

import FExternalDataImportEngine
import FReconciliationWorkflow
import FReconciliationUtils

logger = FExternalDataImportEngine.FAssetManagementUtils.GetLogger()


class FReconciliationEngine(FExternalDataImportEngine.FExternalDataImportEngine):
    def __init__(self, fileName, reconciliationSpecification, options=None):
        self._fileName = fileName
        self._forceReRun = options.ForceReRun == '1' if options else False
        calculationParams = FExternalDataImportEngine.GetCalculationParameters(options) if options else None
        super(FReconciliationEngine, self).__init__(reconciliationSpecification, calculationParams)

    def FileName(self):
        return self._fileName

    def ForceReRun(self):
        return self._forceReRun

    def AbortReconciliation(self):
        reconInstance = self.ReconciliationInstance()
        return reconInstance.NbrOfUnclosedWorkflows() >= reconInstance.MaxNbrOfUnclosedWorkflowItems()

    def Run(self):
        self.CreateReconciliationInstance(self.FileName(), self.ForceReRun())
        self.RetrieveFromFile()
        self.RunIdentification()
        self.RetrieveFromUniverse()
        self.ApplyPreFiltering()
        self.RunComparison()
        self.FilterReconItems()
        self.ReconciliationInstance().Commit()
        self.CreateBusinessProcessesForWorkflows()
        self.CommitWorkflows()
        return self.ReconciliationInstance()

    @staticmethod
    def GarbageCollectItemSubject(reconItem):
        ''' Removes pointer to an infant dynamic position '''
        if reconItem.ReconciliationDocument().ObjectType() == "Position":
            reconItem.Subject(None)

    def ApplyPreFiltering(self):
        ''' Filter (i.e., remove) zero position recon items. This filter will
            only have effect for items originating from the ADS; that is, in a
            2-way reconciliation setting.
        '''
        reconInstance = self.ReconciliationInstance()
        if reconInstance.ReconciliationDocument().ObjectType() == "Position":
            FReconciliationUtils.RemoveZeroPositions(reconInstance)

    def FilterReconItems(self):
        ''' Filter (i.e., remove) recon items that are not subject to storage requirements.
            Do not alter the filtering order - the filtering should be carried out
            by starting with item cleansing and finalized with removal of the completed recon items
            given that the global setting StoreReconciledItems() dictates such.
        '''
        reconInstance = self.ReconciliationInstance()
        for w in reconInstance.Workflows():
            if w.IsUnclosed():
                reconInstance.UnclosedWorkflows(w)
            if self.AbortReconciliation():
                logger.warn('The maximum number of unclosed items (%d) to be reconciled has been reached. Halting reconciliation. ' %
                            reconInstance.MaxNbrOfUnclosedWorkflowItems()
                            )
                break
        if self.AbortReconciliation():
            FReconciliationUtils.RemoveRemainingReconItems(reconInstance)
        if not reconInstance.ReconciliationSpecification().StoreReconciledItems():
            FReconciliationUtils.RemoveSuccessfulReconItems(reconInstance)

    def RetrieveFromFile(self):
        # Make workflows from the rows in the file
        with open(self.FileName(), 'rb') as fp:
            valDict = self.LoadFromFile(fp)
            valDict = self.ApplyImportHook(valDict)
            for rowNumber, fieldValues in self.UnzipDocumentContents(valDict):
                try:
                    externalValues = self.ApplyDataTypeConvertion(fieldValues)
                    workflow = FReconciliationWorkflow.FReconciliationWorkflow(
                               self.ReconciliationInstance(), externalValues)
                except (ValueError, TypeError, AttributeError) as err:
                    workflow = FReconciliationWorkflow.FReconciliationWorkflow(
                               self.ReconciliationInstance(), externalValues = {}, internalValues = {})
                    workflow.ErrorMessage(str(err))
                finally:
                    workflow.RowNumber(rowNumber+1)
                    self.AddWorkflow(workflow)

    def RetrieveFromUniverse(self):
        ''' Find additional items by looking at the universe query.
            Scalable iteration - possibly covering a large set of missing objects.
        '''
        for obj in self.IdentificationEngine().MissingObjects():
            try:
                internalValues = self.IdentificationEngine().InternalValuesForMissingObject(obj)
                internalValues = self.ApplyDataTypeConvertion(internalValues)
                workflow = FReconciliationWorkflow.FReconciliationWorkflow(self.ReconciliationInstance(),
                                                                           externalValues=None,
                                                                           internalValues=internalValues,
                                                                           acmObject=obj)
                workflow.OriginatesFromADS(True)
            except (ValueError, TypeError, AttributeError) as err:
                workflow = FReconciliationWorkflow.FReconciliationWorkflow(self.ReconciliationInstance(),
                                                                           externalValues = {},
                                                                           internalValues = {})
                workflow.ErrorMessage('Error while looking for missing items (Universe Query): %s' % err)
            self.AddWorkflow(workflow)
            self.ReconciliationInstance().TickMissingACMObjectCount(+1)
