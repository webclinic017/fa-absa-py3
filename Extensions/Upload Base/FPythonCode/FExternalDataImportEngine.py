""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/business_data_upload/../reconciliation/etc/FExternalDataImportEngine.py"
"""--------------------------------------------------------------------------
MODULE
    FExternalDataImportEngine

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""

import acm
import FAssetManagementUtils
from FExternalDataImportWorkflow import FBusinessProcessWrapper
import FStateChartUtils
import FReconciliationValueMapping
import FReconciliationContainer
import FBusinessDataImportHook
from FReconciliationIdentification import FIdentificationEngine

logger = FAssetManagementUtils.GetLogger()


def CreateStateChart(name='Reconciliation'):
    # Create the default reconciliation state chart if required
    limit = 'Single'
    layout = 'Unidentified,-106,113;Discrepancy,386,-207;Closed,392,157;Comparison,191,-100;Not in document,54,128;Ready,-109,-209;Missing in document,103,35;'

    stateChart = {
        'Ready':           {'Identified': 'Comparison',
                            'Not found in ADS': 'Unidentified',
                            'Not found in document': 'Missing in document'},
        'Comparison':      {'Mismatch found': 'Discrepancy',
                            'Closed': 'Closed'},
        'Discrepancy':     {'Closed': 'Closed', 'Redo' : 'Ready'},
        'Unidentified':    {'Closed': 'Closed', 'Redo' : 'Ready'},
        'Missing in document': {'Closed': 'Closed'},
    }
    return FStateChartUtils.CreateStateChart(name, stateChart, layout, limit)

def GetCalculationParameters(options):
    try:
        keys = FReconciliationValueMapping.GetCalculationParamsColumnId().keys()
        return dict((key, getattr(options, key)) for key in keys)
    except AttributeError:
        return None

def GetExistingReconciliationDocuments(filePath):
    return acm.FReconciliationDocument.Select('sourceId = ' + filePath).SortByProperty('CreateTime')


class FExternalDataImportEngine(object):

    def __init__(self, reconciliationSpecification, calculationParams):
        self._reconciliationSpecification = reconciliationSpecification
        self._calculationParams = calculationParams
        self._reconInstance = None
        self._identificationEngine = None

    def ReconciliationSpecification(self):
        return self._reconciliationSpecification

    def ReconciliationInstance(self, reconInstance=None):
        if reconInstance is None:
            return self._reconInstance
        self._reconInstance = reconInstance

    def IdentificationEngine(self, identificationEngine = None):
        if identificationEngine is None:
            return self._identificationEngine
        self._identificationEngine = identificationEngine

    def UnzipDocumentContents(self, valDict):
        # Generate contents for memory efficiency
        for i, fieldValues in enumerate(valDict):
            # Ignore rows returning empty fieldValues (potentially filtered by hook)
            if fieldValues:
                yield i+1, fieldValues

    def Process(self):
        upload = self.ReconciliationInstance().ReconciliationSpecification().Upload()
        return 'reconciliation' if not upload else 'data upload'

    @staticmethod
    def IsValidForReconciliation(filename, forceReRun):
        reconciliationDocs = GetExistingReconciliationDocuments(filename)
        if reconciliationDocs.Size() > 0:
            firstReconDoc = reconciliationDocs.First()
            lastReconDoc = reconciliationDocs.Last()
            logger.warn('This document has already been reconciled %i time(s)', reconciliationDocs.Size())
            logger.warn('First run by %s at %s and last by %s at %s',
                    firstReconDoc.CreateUser().Name(),
                    acm.Time().DateTimeFromTime(firstReconDoc.CreateTime()),
                    lastReconDoc.CreateUser().Name(),
                    acm.Time().DateTimeFromTime(lastReconDoc.CreateTime()))
            if not forceReRun:
                logger.warn('Aborting reconciliation operation')
                return False
        return True

    def RunIdentification(self):
        reconInstance = self.ReconciliationInstance()
        reconType = reconInstance.ReconciliationSpecification().ReconciliationObjectType()
        logger.info('Performing %s %s' % (str(reconType).lower(), self.Process()))
        identificationEngine = FIdentificationEngine(reconInstance)
        logger.info('Identifying items contained in document...')
        identificationEngine.IdentifyItems()
        logger.info('Identified %i/%i items contained in document' % (len(identificationEngine.IdentifiedObjects()), len(reconInstance.Workflows())))
        self.IdentificationEngine(identificationEngine)

    def RunComparison(self):
        # pylint: disable-msg=W0110
        reconInstance = self.ReconciliationInstance()
        FReconciliationValueMapping.ValidateReconciliationItems(reconInstance)
        identifiedWorkflows = [w for w in self.GenerateWorkflows(reconInstance) if w.IsIdentified()]
        logger.info('Validated %i/%i item(s)' % (len(identifiedWorkflows), len(self.ReconciliationInstance().Workflows())))

    def CommitReconciliationInstance(self):
        logger.info('Persisting processed information')
        self.ReconciliationInstance().Commit()

    def Run(self):
        raise NotImplementedError

    @staticmethod
    def CreateReconciliationItem(externalValues):
        reconciliationItem = acm.FReconciliationItem()
        reconciliationItem.ExternalValues(externalValues)
        return reconciliationItem

    @staticmethod
    def GenerateWorkflows(reconInstance):
        workflows = reconInstance.Workflows()
        for w in workflows:
            yield w

    @staticmethod
    def GarbageCollectItemSubject(reconItem):
        ''' Implement in child class '''
        pass

    def ApplyImportHook(self, extValuesDictGen):
        if self._reconciliationSpecification.HasExternalValuesHook():
            extValuesDictGen = FBusinessDataImportHook.TransformDictionary(
                self._reconciliationSpecification.GetExternalValues, extValuesDictGen)
        return extValuesDictGen

    def ApplyDataTypeConvertion(self, fields, typeMap=None):
        if typeMap == None:
            typeMap = self._reconciliationSpecification.DataTypeMapping()
        return FReconciliationValueMapping.GetExternalValueObjects(fields, typeMap)

    def CreateReconciliationInstance(self, fileName=None, forceReRun=False):
        reconInstance = FReconciliationContainer.FReconciliationInstance(self.ReconciliationSpecification(),
                                                                         fileName,
                                                                         forceReRun,
                                                                         reconDocument=None)
        reconInstance.CalculationParams(self._calculationParams)
        self.ReconciliationInstance(reconInstance)

    def AddWorkflow(self, workflow):
        self.ReconciliationInstance().Add(workflow)
        logger.debug('Created reconciliation item %d',
                     workflow.ReconciliationItem().Oid())

    def CommitWorkflows(self):
        reconInstance = self.ReconciliationInstance()
        workflows = self.GenerateWorkflows(reconInstance)
        acm.BeginTransaction()
        try:
            for w in workflows:
                w.Commit()
        except Exception as err:
            logger.error('Error committing workflows: ', err)
            acm.AbortTransaction()
            raise err
        else:
            acm.CommitTransaction()
        workflows = self.GenerateWorkflows(reconInstance)
        for w in workflows:
            w.PostCommit()
            self.GarbageCollectItemSubject(w.ReconciliationItem()) # Possibly garbage collect remnants

    def ReinitializeBusinessProcess(self, reconItem, reconSpec, params):
        bps = acm.BusinessProcess.FindBySubjectAndStateChart(reconItem, reconSpec.StateChart())
        if not bps:
            logger.error('No business process was found for recon item %i.' \
                         'Aborting redo procedures.' % reconItem.Oid())
            return

        bpw = FBusinessProcessWrapper(bps[0])
        bpw.HandleEvent(params[0], notes = params[1])
        return bpw

    def CreateBusinessProcessesForWorkflows(self):
        workflows = self.GenerateWorkflows(self.ReconciliationInstance())
        for w in workflows:
            w.CreateBusinessProcess()

    def LoadFromFile(self, fp):
        extValuesDictGen = self._reconciliationSpecification.ParseDocument(fp)
        return extValuesDictGen
        
    def PostProcessingHook(self):
        self.ReconciliationSpecification().PostProcessing(self)