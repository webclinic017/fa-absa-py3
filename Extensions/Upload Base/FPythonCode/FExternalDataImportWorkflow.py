""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/business_data_upload/../reconciliation/etc/FExternalDataImportWorkflow.py"
"""--------------------------------------------------------------------------
MODULE
    FExternalDataImportWorkflow

    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""

import acm
import FAssetManagementUtils
import FBusinessProcessUtils

logger = FAssetManagementUtils.GetLogger()


class FExternalDataImportWorkflowBase(object):
    # Abstract base class for workflow implementations
    def __init__(self, reconciliationInstance, reconciliationItem):
        self._businessDataCreator = None
        self._businessProcess = None
        self._reconciliationItem = reconciliationItem
        self._subject = self._reconciliationItem.Subject()
        self._reconciliationInstance = reconciliationInstance

        assert self._reconciliationItem
        if self._reconciliationItem.ReconciliationDocument() is None:
            self._reconciliationItem.ReconciliationDocument(reconciliationInstance.ReconciliationDocument())

        self._errorMessage = ''
        self._isBreak = True
        self._isIdentified = False
        self._preCommitOid = None
        self._rowNumber = None
        self._ACMObject = None
        self._originatesFromADS = False

    def RowNumber(self, number=None):
        if number == None:
            return self._rowNumber
        self._rowNumber = number

    def OriginatesFromADS(self, fromADS=None):
        if fromADS is None:
            return self._originatesFromADS
        self._originatesFromADS = fromADS

    def ErrorMessage(self, errorMessage=None):
        if errorMessage is None:
            if self._errorMessage != '' and self.RowNumber() is not None:
                return 'Error on row number {}: {}'.format(self.RowNumber(), self._errorMessage)
            return self._errorMessage
        self._errorMessage = errorMessage

    def IsBreak(self, isBreak=None):
        if isBreak is None:
            return self._isBreak
        self._isBreak = isBreak

    def IsIdentified(self, isIdentified=None):
        if isIdentified is None:
            return self._isIdentified
        self._isIdentified = isIdentified

    def BusinessProcess(self, bp=None):
        if bp is None:
            return self._businessProcess
        self._businessProcess = bp

    def ACMObject(self, obj=None):
        if obj is None:
            return self._ACMObject
        self._ACMObject = obj

    def ReconciliationItem(self, reconciliationItem=None):
        if reconciliationItem is None:
            return self._reconciliationItem
        self._reconciliationItem = reconciliationItem

    def ReconciliationInstance(self):
        return self._reconciliationInstance

    def Commit(self):
        self.CommitReconciliationItem()
        self.CommitBusinessProcess()

    def CommitReconciliationItem(self):
        self.ReconciliationItem().Commit()

    def CommitBusinessProcess(self):
        if self.BusinessProcess():
            self.BusinessProcess().Commit()

    def CreateBusinessProcess(self):
        if not self.BusinessProcess():
            stateChartName = self.ReconciliationInstance().ReconciliationSpecification().StateChartName()
            self.BusinessProcess(FBusinessProcessUtils.CreateBusinessProcess(self.ReconciliationItem(), stateChartName))

    def PostCommit(self):
        #if self.ReconciliationItem().Oid() != self._preCommitOid:
        #    logger.debug('Committed reconciliation item %i (oid=%i)', self._preCommitOid, self.ReconciliationItem().Oid())
        self._UpdateBusinessProcessState()

    def _TriggerBusinessProcessEvent(self, eventName, params=None, notes=None):
        bp = self.BusinessProcess()
        logger.debug('Transitioning business process %i on reconcilation item %i with event "%s"',
                bp.Oid(), self.ReconciliationItem().Oid(), eventName)
        try:
            bp.HandleEvent(eventName, params, notes)
            bp.Commit()
        except Exception as e:
            logger.error('Business process %i failed to handle event "%s": %s', bp.Oid(), eventName, e)
            raise

    def _UpdateBusinessProcessState(self):
        '''Subclasses are free and supposed to override for different ways of
        handling business processes'''
        pass


class FBusinessProcessWrapper(object):

    READY_STATE = 'Ready'

    def __init__(self, businessProcess):
        assert businessProcess
        self._businessProcess = businessProcess

    def BusinessProcess(self):
        return self._businessProcess

    def CurrentState(self):
        return self.BusinessProcess().CurrentStep().State()

    def StateChart(self):
        return self.BusinessProcess().StateChart()

    def HasEvent(self, eventName):
        # pylint: disable-msg=W0110
        transitions = filter(lambda t: t.EventName() == eventName,
                             self.CurrentState().Transitions())
        return bool(len(transitions))

    def EventsTo(self, state):
        return FBusinessProcessUtils.EventsBetween(self.StateChart(),
                                                   self.CurrentState().Name(),
                                                   state)
    def IsReinitialized(self):
        return self.CurrentState().Name() == self.READY_STATE

    def HandleEvent(self, eventName, notes = [], params = acm.FDictionary()):
        # pylint: disable-msg=W0102
        if self.HasEvent(eventName):
            self.BusinessProcess().HandleEvent(eventName, params, notes)
            self.BusinessProcess().Commit()
        else:
            logger.info('Business process %s in status %s is missing event %s and thus cannot be transitioned' %
                       (self.BusinessProcess().Oid(), self.CurrentState().Name(), eventName))

    @classmethod
    def FromSubjectAndChart(cls, subject, chartName):
        businessProcess = FBusinessProcessUtils.GetBusinessProcessWithCache(subject, chartName)
        wrapper = cls(businessProcess)
        return wrapper
