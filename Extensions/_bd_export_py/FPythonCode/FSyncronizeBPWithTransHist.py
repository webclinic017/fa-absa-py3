""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/BDExport/./etc/FSyncronizeBPWithTransHist.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FSyncronizeBPWithTransHist -
    This module takes care of creating and updating BusinessProcesses as defined
    by an FIntegration instance

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    See ExportBaseReadMe.py for more information about this module

-------------------------------------------------------------------------------------------------------"""
import acm
import FAssetManagementUtils
import FBusinessProcessUtils
import FExportUtils
import FIntegration
import FTransactionHistoryReader
import FLogger
logger = FLogger.FLogger.GetLogger("BD Export")

class FSyncronizeBPWithTransHist():

    def __init__(self, integrationInstance, additionalQueryDictionary=dict(), ACMTradeQueryIdList=None):
        assert(integrationInstance)
        self._integrationInstance = integrationInstance
        self._query = integrationInstance.TradeACMQueryPrefix()
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
                        if self._additionalQueryDictionary.has_key('Instruments'):
                            if not self._additionalQueryDictionary['Instruments'] == linkQueries or self._integrationInstance.InstrumentExport == 'true':
                                if FExportUtils.FindMatchingQueryId(linkedObject, linkQueries):
                                    if "Name" in dir(linkedObject) and acm.FInstrument[linkedObject.Name()]:
                                        #code for creation business processs
                                        businessProcess = FBusinessProcessUtils.GetOrCreateBusinessProcess(linkedObject, stateChartId)
                                        errStr = "Could not create business process for %s %i on state chart %s" % (linkedObject.Class().Name(), linkedObject.Oid(), stateChartId)
                                        assert(businessProcess), errStr
                                        businessProcess.Commit()
                                        logger.debug("Created business process %i for %s %i" % (businessProcess.Oid(), linkedObject.Class().Name(), linkedObject.Oid()))
                        else:
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
        query = self._query
        reader = FTransactionHistoryReader.FPastTradeStatusTransitions(subscriptionId, query, transitionsSpecification, self._Filter)
        try:
            readerItems = reader.Read()
        except StandardError as error:
            logger.error('Past transactions could not be read. %s', error)
        else:
            for tradeOid, transactions in readerItems:
                trade = acm.FTrade[tradeOid]
                assert(trade)
                transactions.sort()
                n = len(transactions)
                bp = acm.BusinessProcess.FindBySubjectAndStateChart(acm.FTrade[tradeOid], self._stateChart)
                if bp:
                    bp = bp[0]
                #See that this trade matches the selected queries
                if self.TradeQueryIdList() == None or FExportUtils.FindMatchingQueryId(trade, self.TradeQueryIdList()):
                    for transaction in transactions:
                        try:
                            if not (transactions[n-1].Transition().ToStatus() == 'FO Amend') and bp:
                                if not (bp.CurrentStep().State().Name() == 'Ready' and transactions[n-1].Transition().ToStatus()=='Void'):
                                    self._TransactionCreateAndPushBusinessProcess(transaction)
                                else:
                                    if bp:
                                        bp.ForceToState('Cancel Sent', 'Forced to the state because the trade was not exported before it entered into Void state')
                                        bp.Commit()
                            else:
                                if bp and bp.CurrentStep().State().Name() in ['Ready', 'Corrected']:
                                    bp.ForceToState('Awaiting Confirmation', 'Forced to the state because trade was not exported before it entered into FO Amend state')
                                    bp.Commit()
                                else:								
                                    if not transaction.Transition().ToStatus() == 'BO Confirmed':
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
        
        
class FSyncronizeBPWithTransHistInsExport(FSyncronizeBPWithTransHist):

    def _CreateBusinessProcessToIns(self, ins, transition, businessProcesses):
        businessProcess = FBusinessProcessUtils.GetBusinessProcessWithCache(ins, self._integrationInstance.InstrumentStateChart)
        if not businessProcess:
            # Create a BP if there is a create event for the transition, and the trade is still in this state
            if transition.EventId() == FIntegration.FTransition.CREATE_EVENT_ID and ins.AdditionalInfo().InsStatus() == transition.ToStatus():
                businessProcess = FBusinessProcessUtils.CreateBusinessProcess(ins, self._integrationInstance.InstrumentStateChart)
                businessProcess.Commit()
                logger.debug("Created business process %i for %s %i" % (businessProcess.Oid(), ins.Class().Name(), ins.Oid()))
        if businessProcess:
            businessProcesses.append(businessProcess)
        return bool(businessProcess)

    def InitialiseIntegration(self):
        """
        Initialises all exportable trades (and linked objects) with business processes, without
        considering transaction history state.
        """
        logger.info('Initialising all exportable instrument for integration "%s"', self._integrationInstance.Id())
        creationTransitions = [t for t in FIntegration.InstrumentTransitions() if t.EventId() == FIntegration.FTransition.CREATE_EVENT_ID]
        if not creationTransitions:
            raise RuntimeError('No export creation transitions found for integration')
        businessProcesses = list()
        storedQuery = acm.FStoredASQLQuery[self._additionalQueryDictionary['Instruments']]
        instruments = storedQuery.Query().Select()
        logger.debug('Processing %d instruments for query "%s"',  instruments.Size(), storedQuery.Name())
        for ins in instruments:
            for transition in creationTransitions:
                if self._CreateBusinessProcessToIns(ins, transition, businessProcesses):
                    break
        logger.info('Processed %d export business processes initialising integration.', len(businessProcesses))
        
    def Execute(self):
        pass

    def _TransactionCreateAndPushBusinessProcess(self, transition, ins):
        businessProcesses = list()
        self._CreateBusinessProcessToIns(ins, transition, businessProcesses)
        for businessProcess in businessProcesses:
            self._TransactionPushBusinessProcess(transition, businessProcess)
            
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
                currentStep.Commit()
                subject = businessProcess.Subject()
                logger.info("Business process %i for trade %i is now in state %s", businessProcess.Oid(), subject.Oid(), transition.EventId())
            except StandardError as error:
                errStr = 'Could not invoke %s on business process %i: %s' % (transition.EventId(), businessProcess.Oid(), error)
                logger.error(errStr)
                FBusinessProcessUtils.SetBusinessProcessToError(businessProcess, errStr)
                raise StandardError(errStr)

class FSyncronizeBPWithTransHistTradeExport(FSyncronizeBPWithTransHist):

    def _TransactionCreateAndPushBusinessProcess(self, transaction):
        businessProcesses = list()
        transition = transaction.Transition()
        trade = transaction.Current()
        self._CreateBusinessProcessToTrade(trade, transition, businessProcesses)
        for businessProcess in businessProcesses:
            self._TransactionPushBusinessProcess(transaction, businessProcess)
            
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
                        break
        logger.info('Processed %d export business processes initialising integration.', len(businessProcesses))