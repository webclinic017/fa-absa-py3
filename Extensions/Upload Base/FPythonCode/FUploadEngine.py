""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/business_data_upload/etc/FUploadEngine.py"
'''
Created on 20 apr 2015

@author: marcus.lundin
'''
import FExternalDataImportEngine
import FUploadWorkflow

class FUploadEngine(FExternalDataImportEngine.FExternalDataImportEngine):
    def __init__(self,filename,reconciliationSpecification,options=None):
        self._filename = filename
        calculationParams = FExternalDataImportEngine.GetCalculationParameters(options) if options else None
        super(FUploadEngine, self).__init__(reconciliationSpecification, calculationParams)
        
    def Run(self,resolveBreaks=False):
        # pylint: disable-msg=W0221
        self.CreateReconciliationInstance(self._filename)
        with open(self._filename, 'rb') as fp:
            valDict = self.LoadFromFile(fp)
            valDict = self.ApplyImportHook(valDict)
            for (rowNumber, fieldValues) in self.UnzipDocumentContents(valDict):
                try:
                    externalValues = self.ApplyDataTypeConvertion(fieldValues)
                    workflow = FUploadWorkflow.FUploadWorkflow(self.ReconciliationInstance(), externalValues)
                    workflow.RowNumber(rowNumber)
                    self.AddWorkflow(workflow)
                except (ValueError, TypeError, AttributeError) as err:
                    workflow = FUploadWorkflow.FUploadWorkflow(self.ReconciliationInstance(), {})
                    workflow.RowNumber(rowNumber)
                    workflow.ErrorMessage(str(err))
                    self.AddWorkflow(workflow)
        self.RunIdentification()
        self.RunComparison()
        for wf in self.ReconciliationInstance().Workflows():
            try:
                if not wf.IsIdentified():
                    wf.CreateBusinessObject()
                elif not wf.IsBreak():
                    wf.CreateBusinessObject()
                elif resolveBreaks and wf.IsBreak():
                    wf.CreateBusinessObject()
                    wf.IsBreak(False)
            except StandardError as err:
                wf.ErrorMessage(str(err))
                continue
            if wf.BusinessDataCreator() != None:
                wf.CommitBusinessObject()

        self.ReconciliationInstance().Commit()
        self.CreateBusinessProcessesForWorkflows()
        self.CommitWorkflows()
        self.PostProcessingHook()
        return self.ReconciliationInstance()