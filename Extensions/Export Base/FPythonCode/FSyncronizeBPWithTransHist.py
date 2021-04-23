""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/export/./etc/FSyncronizeBPWithTransHist.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FSyncronizeBPWithTransHist -
    This module takes care of creating and updating BusinessProcesses as defined
    by an FIntegration instance

    (c) Copyright 2012 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    See ExportBaseReadMe.py for more information about this module

-------------------------------------------------------------------------------------------------------"""
import acm
import FAssetManagementUtils
import FBusinessProcessUtils
import FExportUtils
import FIntegration
import FTransactionHistoryReader

logger = FAssetManagementUtils.GetLogger()


class FSyncronizeBPWithTransHist():

    def __init__(self, integrationInstance, ACMTradeQueryIdList=None, additionalQueryDictionary=dict()):
        assert(integrationInstance)
        self._integrationInstance = integrationInstance
        self._stateChart = self._integrationInstance.StateChart()
        self._ACMTradeQueryIdList = ACMTradeQueryIdList
        self._additionalQueryDictionary = additionalQueryDictionary

    def _Filter(self, trade):
        for storedQuery in FExportUtils.TradeFilterQueriesForIntegration(self._integrationInstance.TradeACMQueryPrefix()):
            if storedQuery.Query().IsSatisfiedBy(trade):
                return True
        return False

    def TradeQueryIdList(self):
        return self._ACMTradeQueryIdList

    def AdditionalQueryDictionary(self):
        return self._additionalQueryDictionary

    def _CreateBusinessProcessToTrade(self, trade, transition, businessProcesses):
        businessProcess = FBusinessProcessUtils.GetBusinessProcessWithCache(trade, self._stateChart.Name())
        if not businessProcess:
            # Create a BP if there is a create event for the transition, and the trade is still in this state
            if transition.EventId() == FIntegration.FTransition.CREATE_EVENT_ID and trade.Status() == transition.ToStatus():
                businessProcess = FBusinessProcessUtils.CreateBusinessProcess(trade, self._stateChart.Name())
                businessProcess.Commit()
                logger.debug("Created business process %i for %s %i" % (businessProcess.Oid(), trade.Class().Name(), trade.Oid()))
        if businessProcess:
            businessProcesses.append(businessProcess)
        return bool(businessProcess)

    def _CreateBusinessProcessToLinkedObject(self, trade, businessProcesses):
        if self._integrationInstance.LinkedExportObjects():
            for (linkedObjectFunc, stateChartId, exportObjectId) in self._integrationInstance.LinkedExportObjects():
                linkedObject = linkedObjectFunc(trade)
                if linkedObject:
                    logger.debug("Found linked object %s %i from trade %i using %s function" % (linkedObject.Class().Name(), linkedObject.Oid(), trade.Oid(), str(linkedObjectFunc)))
                    businessProcess = FBusinessProcessUtils.GetBusinessProcessWithCache(linkedObject, stateChartId)
                    if not businessProcess:
                        errStr = "The linked export objects with id '%s' has no matching query list. Check the initialization of FExportProcess." % exportObjectId
                        assert self.AdditionalQueryDictionary().has_key(exportObjectId), errStr
                        linkQueries = self.AdditionalQueryDictionary()[exportObjectId]
                        if FExportUtils.FindMatchingQueryId(linkedObject, linkQueries):
                            businessProcess = FBusinessProcessUtils.GetOrCreateBusinessProcess(linkedObject, stateChartId)
                            errStr = "Could not create business process for %s %i on state chart %s" % (linkedObject.Class().Name(), linkedObject.Oid(), stateChartId)
                            assert(businessProcess), errStr
                            businessProcess.Commit()
                            logger.debug("Created business process %i for %s %i" % (businessProcess.Oid(), linkedObject.Class().Name(), linkedObject.Oid()))
                    if businessProcess:
                        businessProcesses.append(businessProcess)

    @staticmethod
    def _TransactionPushBusinessProcess(transaction, businessProcess):
        transition = transaction.Transition()
        subject = transaction.Current()
        # There is a BP already created, and we want to push it further
        # The matched trades must have BPs and it will also be moved according to trade events that has occurred
        if (FBusinessProcessUtils.IsValidEvent(businessProcess, transition.EventId())):
            try:
                businessProcess.HandleEvent(transition.EventId())
                businessProcess.Commit()
                currentStep = businessProcess.CurrentStep()
                assert(currentStep), "A business process must have a current step"
                currentStep.SubjectVersion(transaction.Version())
                currentStep.Commit()
                subject = businessProcess.Subject()
                assert(subject == transaction.Current()), 'Subject and transactionEvent objects are not the same'
                logger.info("Business process %i for trade %i is now in state %s", businessProcess.Oid(), subject.Oid(), transition.EventId())
            except StandardError as error:
                errStr = 'Could not invoke %s on business process %i: %s' % (transition.EventId(), businessProcess.Oid(), error)
                logger.error(errStr)
                FBusinessProcessUtils.SetBusinessProcessToError(businessProcess, errStr)
                raise StandardError(errStr)

    def _TransactionCreateAndPushBusinessProcess(self, transaction):
        businessProcesses = list()
        transition = transaction.Transition()
        trade = transaction.Current()

        if self._CreateBusinessProcessToTrade(trade, transition, businessProcesses):
            # Linked object business processes are only created if a business process on the trade exists
            self._CreateBusinessProcessToLinkedObject(trade, businessProcesses)
        for businessProcess in businessProcesses:
            self._TransactionPushBusinessProcess(transaction, businessProcess)

    def Execute(self):
        """
        This synchronises the relevant Business Processes with events that has occurred
        in the ADS since last run.
        """
        subscriptionId = self._integrationInstance.Id()
        transitionsSpecification = self._integrationInstance.TradeTransitions()
        reader = FTransactionHistoryReader.FPastTradeStatusTransitions(subscriptionId, transitionsSpecification, self._Filter)
        try:
            readerItems = reader.Read()
        except StandardError as error:
            logger.error('Past transactions could not be read. %s', error)
        else:
            for tradeOid, transactions in readerItems:
                trade = acm.FTrade[tradeOid]
                assert(trade)
                transactions.sort()
                n1=len(transactions)
                bp=acm.FTrade[tradeOid].BusinessProcesses()
                ready_state=False
                if bp:
                    bp=bp[0]
                    ready_state=bp.CurrentStep().State().Name()=='Ready'
                p1=transactions[n1-1].Transition().ToStatus()=='FO Amend'
                p2=ready_state and transactions[n1-1].Transition().ToStatus()=='Void'
                #See that this trade matches the selected queries
                if self.TradeQueryIdList() == None or FExportUtils.FindMatchingQueryId(trade, self.TradeQueryIdList()):
                    for transaction in transactions:
                        try:
                            if not p1:
                                if not p2:
                                    self._TransactionCreateAndPushBusinessProcess(transaction)
                                else:
                                    if bp:
                                        bp.ForceToState('Cancel Sent', 'Forced to the state because the trade was not exported before it entered into Void state')
                                        bp.Commit()
                                    #if transaction.Transition().ToStatus()=='Void':
                                    #    self._TransactionCreateAndPushBusinessProcess(transaction)
                            else:
                                if ready_state:
                                    if bp:
                                        bp.ForceToState('Awaiting Confirmation', 'Forced to the state because trade was not exported before it entered into FO Amend state')
                                        bp.Commit()
                                else:								
                                    if not transaction.Transition().ToStatus()=='BO Confirmed':
                                        self._TransactionCreateAndPushBusinessProcess(transaction)
                        except StandardError as error:
                            logger.error('Error in _TransactionCreateAndPushBusinessProcess: %s' % error)
        try:
            reader.Accept()
        except StandardError as error:
            logger.error('Could not recover all transactions. Please try again. %s', error)

    def InitialiseIntegration(self):
        """
        Initialises all exportable trades (and linked objects) with business processes, without
        considering transaction history state.
        """
        logger.info('Initialising all exportable trades for integration "%s"', self._integrationInstance.Id())
        creationTransitions = [t for t in self._integrationInstance.TradeTransitions() if t.EventId() == FIntegration.FTransition.CREATE_EVENT_ID]
        if not creationTransitions:
            raise RuntimeError('No export creation transitions found for integration')

        businessProcesses = list()
        for storedQuery in FExportUtils.TradeFilterQueriesForIntegration(self._integrationInstance.TradeACMQueryPrefix()):
            trades = storedQuery.Query().Select()
            logger.debug('Processing %d trades for query "%s"', trades.Size(), storedQuery.Name())
            for trade in trades:
                for transition in creationTransitions:
                    if self._CreateBusinessProcessToTrade(trade, transition, businessProcesses):
                        self._CreateBusinessProcessToLinkedObject(trade, businessProcesses)
                        break
        logger.info('Processed %d export business processes initialising integration.', len(businessProcesses))