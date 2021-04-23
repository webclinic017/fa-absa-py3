""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/BDExport/./etc/FSyncronizeBPWithCurrentState.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FSyncronizeBPWithCurrentState -
    This module takes care of creating and updating BusinessProcesses as defined
    by an FIntegration instance

    (c) Copyright 2018 SunGard FRONT ARENA. All rights reserved.


-------------------------------------------------------------------------------------------------------"""
import acm
import FBusinessProcessUtils
import FIntegration
import FLogger
logger = FLogger.FLogger.GetLogger("BD Export")
from FSyncronizeBPWithTransHist import FSyncronizeBPWithTransHist
        
class FSyncronizeBPWithCurrentState(FSyncronizeBPWithTransHist):

    def _TransactionCreateAndPushBusinessProcess(self, transition, trade):
        businessProcesses = list()
        if self._CreateBusinessProcessToTrade(trade, transition, businessProcesses):
            # Linked object business processes are only created if a business process on the trade exists
            self._CreateBusinessProcessToLinkedObject(trade, businessProcesses)
        for businessProcess in businessProcesses:
            self._TransactionPushBusinessProcess(transition, businessProcess)
    @staticmethod
    def _TransactionPushBusinessProcess(transition, businessProcess):
        subject = businessProcess.Subject()
        # There is a BP already created, and we want to push it further
        # The matched trades must have BPs and it will also be moved according to trade events that has occurred
        if businessProcess.CurrentStep().State().Name() in ['Ready', 'Corrected'] and subject.Status() == 'FO Amend':
            businessProcess.ForceToState('Awaiting Confirmation', 'Forced to the state because trade was not exported before it entered into FO Amend state')
            businessProcess.Commit()
        elif businessProcess.CurrentStep().State().Name() in ['Ready'] and subject.Status() == 'Void':
            businessProcess.ForceToState('Cancel Sent', 'Forced to the state because the trade was not exported before it entered into Void state')
            businessProcess.Commit()
        elif (FBusinessProcessUtils.IsValidEvent(businessProcess, transition.EventId())):
            try:
                businessProcess.HandleEvent(transition.EventId())
                businessProcess.Commit()
                currentStep = businessProcess.CurrentStep()
                assert(currentStep), "A business process must have a current step"
                currentStep.Commit()
                subject = businessProcess.Subject()
                logger.info("Business process %i for trade %i is now in state %s", businessProcess.Oid(), subject.Oid(), transition.EventId())
            except StandardError as error:
                errStr = 'Could not invoke %s on business process %i: %s' % (transition.EventId(), businessProcess.Oid(), error)
                logger.error(errStr)
                FBusinessProcessUtils.SetBusinessProcessToError(businessProcess, errStr)
                raise StandardError(errStr)
    def Execute(self):
        subscriptionId = self._integrationInstance.Id()
        transitionsSpecification = self._integrationInstance.TradeTransitions()
        query = acm.FStoredASQLQuery[self._query]
        transitions = [t for t in self._integrationInstance.TradeTransitions() if t.EventId() not in [FIntegration.FTransition.CREATE_EVENT_ID]]
        for trade in query.Query().Select():
            for transiiton in transitions:
                if trade.Status() == transiiton.ToStatus():
                    self._TransactionCreateAndPushBusinessProcess(transiiton, trade)