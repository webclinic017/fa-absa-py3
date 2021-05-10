""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/business_data_upload/../reconciliation/etc/FReconciliationWorkflow.py"
"""--------------------------------------------------------------------------
MODULE
    FReconciliationWorkflow

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""
from FExternalDataImportWorkflow import FExternalDataImportWorkflowBase
import FBusinessProcessUtils
import acm

class FReconciliationWorkflow(FExternalDataImportWorkflowBase):

    EVENT_IDENTIFIED = "Identified"
    EVENT_NOT_FOUND_IN_DOCUMENT = 'Not found in document'
    EVENT_NOT_FOUND_IN_ADS = 'Not found in ADS'
    EVENT_MISMATCH_FOUND = 'Mismatch found'
    EVENT_CLOSED = 'Closed'

    def __init__(self, reconciliationInstance, externalValues=None, internalValues=None, acmObject=None, reconItem=None):
        if reconItem is not None:
            reconciliationItem = reconItem
        elif externalValues is not None:
            reconciliationItem = acm.FReconciliationItem()
            reconciliationItem.ExternalValues(externalValues)            
        elif internalValues is not None and acmObject is not None:
            reconciliationItem = acm.FReconciliationItem()
            reconciliationItem.InternalValues(internalValues)
            reconciliationItem.Subject(acmObject)            
        else:
            raise ValueError('Either externalValues or acmObject or reconItem need to be set')
        reconciliationItem.ReconciliationDocument(reconciliationInstance.ReconciliationDocument())
        super(FReconciliationWorkflow, self).__init__(reconciliationInstance, reconciliationItem)
        self.ACMObject(acmObject)

    def IdentifiedOrNotEmptyPosition(self):
        return self.ACMObject() != None
        
    def IsUnclosed(self):
        boolIsUnclosed = False
        if self.ErrorMessage():
            boolIsUnclosed = True
        elif self.OriginatesFromADS():
            boolIsUnclosed = True
        elif not self.IdentifiedOrNotEmptyPosition():
            boolIsUnclosed = True
        elif self.IsBreak():
            boolIsUnclosed = True            
        return boolIsUnclosed
        
    def IsClosed(self):
        return not self.IsUnclosed()

    def _UpdateBusinessProcessState(self):
        if self.ErrorMessage():
            # A failure occurred during processing
            FBusinessProcessUtils.SetBusinessProcessToError(self.BusinessProcess(), self.ErrorMessage())
            return
        if self.OriginatesFromADS():
            # Item is an internal object missing from the reconciled document
            self._TriggerBusinessProcessEvent(self.EVENT_NOT_FOUND_IN_DOCUMENT)
            return
        if not self.IdentifiedOrNotEmptyPosition():
            # Could not identify this item in the system
            self._TriggerBusinessProcessEvent(self.EVENT_NOT_FOUND_IN_ADS)
            return
        # Set item as identified and closed if not a break, or discrepancy if it is
        self._TriggerBusinessProcessEvent(self.EVENT_IDENTIFIED)
        if self.IsBreak():
            self._TriggerBusinessProcessEvent(self.EVENT_MISMATCH_FOUND)
            return

        self._TriggerBusinessProcessEvent(self.EVENT_CLOSED)
        return
