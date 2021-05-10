""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/reconciliation/./etc/FRerunReconciliationEngine.py"
"""--------------------------------------------------------------------------
MODULE
    FRerunReconciliationEngine

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""

import acm

import FReconciliationSpecification
import FExternalDataImportEngine
import FReconciliationWorkflow
import FReconciliationContainer
import FAssetManagementUtils

logger = FAssetManagementUtils.GetLogger()


class FRerunReconciliationEngine(FExternalDataImportEngine.FExternalDataImportEngine):

    REDO_EVENT_NAME = 'Redo'

    def __init__(self, reconItem):
        assert reconItem is not None, 'Action redo requires a reconciliation item.'
        self._reconItem = reconItem
        reconciliationSpecification = self._GetReconciliationSpecification()
        reconciliationSpecification.StoreReconciledItems(True)
        super(FRerunReconciliationEngine, self).__init__(reconciliationSpecification, None)
        
    def _GetReconciliationSpecification(self):
        ''' Returns the FReconciliationSpecification instance for a stored reconciliation item object.
            Use this (helper) method when accessing the specification during recon processing. 
        '''
        reconciliationName = self.ReconciliationItem().ReconciliationDocument().ReconciliationName()
        try:
            return FReconciliationSpecification.FReconciliationSpecification(reconciliationName, upload = False)
        except ValueError as e:
            logger.error('Failed to load reconciliation specification "%s" for reconciliation item %d: %s',
                          reconciliationName, self.ReconciliationItem().Oid(), e)
            raise
        return None  

    def ReconciliationItem(self):
        return self._reconItem  
        
    def ParametersForReRun(self):
        # Return a tuple (redo event name, notes, params) of input parameters for redo
        return (self.REDO_EVENT_NAME, 
                ['Manually triggered redo event by user %s' % acm.User().Name(), ], 
                acm.FDictionary())
        
    def __PrivatePrepareForRun(self):  
        reconDocument = self.ReconciliationItem().ReconciliationDocument()
        self.ReconciliationInstance(FReconciliationContainer.FReconciliationInstance(self.ReconciliationSpecification(), 
                                                                                     fileName = None, 
                                                                                     forceReRun = False,
                                                                                     reconDocument = reconDocument))
        try:
            workflow = FReconciliationWorkflow.FReconciliationWorkflow(self.ReconciliationInstance(),
                                                                       reconItem = self.ReconciliationItem())
            bpw = self.ReinitializeBusinessProcess(self.ReconciliationItem(), 
                                                   self.ReconciliationSpecification(), 
                                                   self.ParametersForReRun())
            if bpw and bpw.IsReinitialized(): 
                workflow.BusinessProcess(bpw.BusinessProcess())
                self.AddWorkflow(workflow)
            else:
                return None
        except (ValueError, TypeError, AttributeError) as err:
            workflow = FReconciliationWorkflow.FReconciliationWorkflow(self.ReconciliationInstance(), 
                                                                       externalValues = {}, 
                                                                       internalValues = {})
            workflow.ErrorMessage('Error on workflow creation: %s' % (str(err)))
            self.AddWorkflow(workflow)   
        return bpw.IsReinitialized()
            
    def __PrivateRun(self):
        self.RunIdentification()
        self.RunComparison()
        self.ReconciliationInstance().Commit()
        self.CommitWorkflows()            

    def Run(self):
        logger.debug('Redoing reconciliation process for recon item %i' % self.ReconciliationItem().Oid())    
        isPrepared = self.__PrivatePrepareForRun()
        if isPrepared:
            self.__PrivateRun()
            return self.ReconciliationInstance()