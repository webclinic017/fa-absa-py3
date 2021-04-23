""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/BDExport/./etc/FChangeTradeStatus.py"
from __future__ import print_function
"""--------------------------------------------------------------------------
MODULE
    ChangeTradeStatus -
    This module takes care of updating BusinessProcesses as defined
    by an FIntegration instance from the trade dialog GUI

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Classes for Export State transition from GUI  

---------------------------------------------------------------------------"""

import acm
import FUxCore
import FIntegration
import FBusinessProcessUtils
import FLogger
logger = FLogger.FLogger.GetLogger("BD Export")

def StartApplication(eii):
    if type(eii.ExtensionObject().CurrentObject()) == type(acm.FTrade()):
        trade = eii.ExtensionObject().CurrentObject()
        change = FChangeCurrentState(trade, trade.Status())
        change.Execute()


class FChangeCurrentState():
    def __init__(self, object, status):
        self._object = object
        self._status = status

    @staticmethod
    def _GetBusinessProcesses(object):
        return [bp for bp in acm.BusinessProcess.FindBySubject(object) if 'StateChartType' in dir(bp.StateChart().AdditionalInfo()) and bp.StateChart().AdditionalInfo().StateChartType() == 'Export']
    
    @staticmethod
    def _TransactionPushBusinessProcess(transition, businessProcess):
        subject = businessProcess.Subject()
        # There is a BP already created, and we want to push it further
        # The matched trades must have BPs and it will also be moved according to trade events that has occurred
        if (FBusinessProcessUtils.IsValidEvent(businessProcess, transition.EventId())):
            try:
                businessProcess.HandleEvent(transition.EventId())
                businessProcess.Commit()
                currentStep = businessProcess.CurrentStep()
                assert(currentStep), "A business process must have a current step"
                #currentStep.SubjectVersion(transaction.Version())
                currentStep.Commit()
                subject = businessProcess.Subject()
                #assert(subject == transaction.Current()), 'Subject and transactionEvent objects are not the same'
                logger.info("Business process %i for trade %i is now in state %s", businessProcess.Oid(), subject.Oid(), transition.EventId())
            except StandardError as error:
                errStr = 'Could not invoke %s on business process %i: %s' % (transition.EventId(), businessProcess.Oid(), error)
                logger.error(errStr)
                FBusinessProcessUtils.SetBusinessProcessToError(businessProcess, errStr)
                raise StandardError(errStr)
    def Execute(self):
        transitions = [t for t in FIntegration.TradeTransitions() if t.EventId() not in [FIntegration.FTransition.CREATE_EVENT_ID, 'Correction Confirmed', 'Void Trade']]
        trade = self._object
        for bp in self._GetBusinessProcesses(self._object):
        #for bp in acm.BusinessProcess.FindBySubject(trade):
            for transiiton in transitions:
                if bp.CurrentStep().State().Name() == 'Ready':
                    print(bp)
                    if self._status == 'FO Amend':
                        bp.ForceToState('Awaiting Confirmation', 'Forced to the state because trade was not exported before it entered into FO Amend state')
                        bp.Commit()
                    elif self._status == 'Void':
                        bp.ForceToState('Cancel Sent', 'Forced to the state because the trade was not exported before it entered into Void state')
                        bp.Commit()
                elif self._status == transiiton.ToStatus():
                    self._TransactionPushBusinessProcess(transiiton, bp)