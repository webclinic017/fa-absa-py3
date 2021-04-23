""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/business_data_upload/etc/FUploadWorkflow.py"
from FExternalDataImportWorkflow import FExternalDataImportWorkflowBase
import FBusinessProcessUtils
import acm

class FUploadWorkflow(FExternalDataImportWorkflowBase):

    EVENT_IDENTIFIED = "Identified"
    EVENT_NOT_FOUND_IN_ADS = 'Not identified'
    EVENT_MISMATCH_FOUND = 'Mismatch found'
    EVENT_CLOSED = 'Matched'
    EVENT_VALIDATION_FAILED = 'Validation failed'
    EVENT_CREATE_BUSINESS_OBJECT = 'Create business object'
    EVENT_UPLOAD_SUCCESSFUL = 'Uploaded successfully'
    EVENT_UPDATE_BUSINESS_OBJECT = 'Update business object'
    
    def __init__(self,reconciliationInstance, externalValues=None,reconItem=None):
        self._businessObjectValidationMessage = ''
        self._businessObjectCommitErrorMessage = ''

        if reconItem != None:
            reconciliationItem = reconItem
        elif externalValues != None:
            reconciliationItem = acm.FReconciliationItem()
            reconciliationItem.ExternalValues(externalValues)
            reconciliationItem.ReconciliationDocument(reconciliationInstance.ReconciliationDocument())
        else:
            raise ValueError('Either externalValues or reconItem need to be set')
        super(FUploadWorkflow, self).__init__(reconciliationInstance, reconciliationItem)

    def BusinessObjectValidationMessage(self, message=None):
        if message is None:
            if self._businessObjectValidationMessage != '' and self.RowNumber() != None:
                return 'Validation error on row number %d: %s'%(self.RowNumber(), self._businessObjectValidationMessage)
            return self._businessObjectValidationMessage
        self._businessObjectValidationMessage = message

    def BusinessObjectCommitErrorMessage(self, message=None):
        if message is None:
            if self._businessObjectCommitErrorMessage != '' and self.RowNumber() != None:
                return 'Commit error on row number %d: %s'%(self.RowNumber(), self._businessObjectCommitErrorMessage)
            return self._businessObjectCommitErrorMessage
        self._businessObjectCommitErrorMessage = message

    def BusinessDataCreator(self, creator=None):
        #pylint: disable-msg=E0203
        if creator is None:
            return self._businessDataCreator
        self._businessDataCreator = creator

    def CreateBusinessObject(self):
        if self.ErrorMessage():
            self.BusinessObjectValidationMessage('Validation not possible because of previous errors')
            return
        import FBusinessDataCreator
        reconSpec = self.ReconciliationInstance().ReconciliationSpecification()
        creator = FBusinessDataCreator.GetCreator(reconSpec, self.ReconciliationItem(), self.ACMObject())
        self.ACMObject(creator.BusinessObject())
        try:
            creator.PreCommitHook()
        except StandardError as err:
            self.ErrorMessage(str(err))
            creator.BusinessObject().Undo()
            raise StandardError('Unable to create business object:', err)
        try:
            creator.Validate()
        except ReferenceError as err:
            self.BusinessObjectValidationMessage(str(err))
            creator.BusinessObject().Undo()
            raise StandardError('Unable to create business object:', err)
        self.BusinessDataCreator(creator)

    def CommitBusinessObject(self):
        if self.ErrorMessage() != '' or self.BusinessObjectValidationMessage() != '':
            return None
        creator = self.BusinessDataCreator()
        try: 
            creator.Execute()
        except SystemError as err:
            self.BusinessObjectCommitErrorMessage(str(err))
            return None
        self.ACMObject(creator.BusinessObject())
        self.ReconciliationItem().Subject(self.ACMObject())



    def _UpdateBusinessProcessState(self):
        if self.ErrorMessage():
            # A failure occurred during processing
            FBusinessProcessUtils.SetBusinessProcessToError(self.BusinessProcess(), self.ErrorMessage())
            return
        elif not self.IsIdentified():
            # Could not identify this item in the system
            self._TriggerBusinessProcessEvent(self.EVENT_NOT_FOUND_IN_ADS)          
            if self.BusinessObjectValidationMessage():
                self._TriggerBusinessProcessEvent(self.EVENT_VALIDATION_FAILED, None, [self.BusinessObjectValidationMessage()])
            else:
                self._TriggerBusinessProcessEvent(self.EVENT_CREATE_BUSINESS_OBJECT)
                if self.BusinessObjectCommitErrorMessage():
                    FBusinessProcessUtils.SetBusinessProcessToError(self.BusinessProcess(), self.BusinessObjectCommitErrorMessage())
                else:
                    self._TriggerBusinessProcessEvent(self.EVENT_UPLOAD_SUCCESSFUL)
        else:
            # Set item as identified and closed if not a break, or discrepancy if it is
            self._TriggerBusinessProcessEvent(self.EVENT_IDENTIFIED)
            if self.IsBreak():
                self._TriggerBusinessProcessEvent(self.EVENT_MISMATCH_FOUND)
                if self.BusinessDataCreator():
                    self._TriggerBusinessProcessEvent(self.EVENT_UPDATE_BUSINESS_OBJECT)
                    if self.BusinessObjectValidationMessage():
                        self._TriggerBusinessProcessEvent(self.EVENT_VALIDATION_FAILED, None, [self.BusinessObjectValidationMessage()])
                    elif self.BusinessObjectCommitErrorMessage():
                        FBusinessProcessUtils.SetBusinessProcessToError(self.BusinessProcess(), self.BusinessObjectCommitErrorMessage())
                    else:
                        self._TriggerBusinessProcessEvent(self.EVENT_UPLOAD_SUCCESSFUL)
            else:
                if self.BusinessObjectValidationMessage():
                    FBusinessProcessUtils.SetBusinessProcessToError(self.BusinessProcess(), self.BusinessObjectValidationMessage())
                elif self.BusinessObjectCommitErrorMessage():
                    FBusinessProcessUtils.SetBusinessProcessToError(self.BusinessProcess(), self.BusinessObjectCommitErrorMessage())
                else:
                    self._TriggerBusinessProcessEvent(self.EVENT_CLOSED)
