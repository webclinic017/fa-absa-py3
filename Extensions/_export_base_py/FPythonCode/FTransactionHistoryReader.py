""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/export/./../AM_common/FTransactionHistoryReader.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FTransactionHistoryReader

    (c) Copyright 2012 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
import acm
import FAssetManagementUtils
import FExportUtils

logger = FAssetManagementUtils.GetLogger()


class FNotRelevantTransactionError(EnvironmentError):
    pass

class FTransactionEvent():
    """
    Class for handling a transaction and its ACM object before and after
    """
    def __init__(self, historyTransaction, transition, filterFunction = None):
        if historyTransaction.Oper() == 'Delete':
            raise FNotRelevantTransactionError("Delete transaction")

        current = acm.FTrade[historyTransaction.RecordId()]
        if not current:
            raise FNotRelevantTransactionError("Trade has already been deleted")

        if filterFunction and filterFunction(current) is False:
            raise FNotRelevantTransactionError("Did not pass filter function %s" % filterFunction.__name__)

        self._current = current
        self._oid = current.Oid()
        self._seqNbr = historyTransaction.SeqNbr()
        self._transition = transition
        self._version = historyTransaction.Version()

    def Current(self):
        return self._current

    def Transition(self):
        return self._transition

    def Version(self):
        return self._version

    def Oid(self):
        return self._oid
        
    def __lt__(self, other):
        return self._version < other._version

class FPastTradeStatusTransitions():
    """
    This class is able to read past trade events from the transaction history table.
    It includes all events, regardless of weather there is a trade status change.
    """

    def __init__(self, integrationID, tradeStatusTransitions, tradeFilterFunction = None):
        self._subscriptionId = integrationID
        self._Transactions = dict() #TransactionHandler()
        self._startingSequenceNumber = 0
        self._tradeStatusTransitions = tradeStatusTransitions
        self._tradeOids = []
        self._tradeFilter = tradeFilterFunction
        self._historySubscriber = FTransactionHistorySubscriber(self._subscriptionId)

    def Read(self):
        for transitionSpec in self._tradeStatusTransitions:
            nbrOfTransactions = self._LoadTradeTransactionsByTransition(transitionSpec)
            logger.info('Found %i "%s" events for relevant trades.', nbrOfTransactions, transitionSpec.EventId())
        return self

    def _LoadTradeTransactionsByTransition(self, transitionToFind):
        added = 0
        for historyTransaction in self._TransactionsFromTag(transitionToFind.TransactionHistoryTag()):
            try:
                pair = FTransactionEvent(historyTransaction, transitionToFind, self._tradeFilter)
            except FNotRelevantTransactionError:
                continue
            if pair.Oid() in self._tradeOids:
                self._Transactions[pair.Oid()].append(pair)
            else:
                self._tradeOids.append(pair.Oid())
                self._Transactions[pair.Oid()] = [pair, ]
            added += 1
        return added

    def _TransactionsFromTag(self, descriptionTag, recId = 19):
        self._startingSequenceNumber = self._historySubscriber.CurrentTransactionNumber()
        logger.debug('Starting at transaction number %i.', self._startingSequenceNumber)
        sqlQuery = 'transRecordType = %i AND oid > %i  AND description = "%s"' % (recId, self._startingSequenceNumber, descriptionTag)
        transactions = []
        for tradeQuery in self.StoredTradeQueries():
            for trade in tradeQuery.Query().Select():
                query = ''.join((sqlQuery, ' AND recordId = %d' % (trade.Oid())))
                transactions.extend(self._historySubscriber.SortedHistoryTransactions(query))
        return transactions
        
    def __iter__(self):
        return self._Transactions.iteritems()
    
    def StoredTradeQueries(self):
        return FExportUtils.TradeFilterQueriesForIntegration(self._subscriptionId)

    def Accept(self):
        self._historySubscriber.AcceptTransactions()



class FTransactionHistorySubscriber():

    def __init__(self, subscriptionId):
        assert(subscriptionId)
        self._subscriptionId = subscriptionId
        self._transHistSubscription = None
        self._lastSequenceNumber = -1

    def TransHistSubscription(self):
        transHistSubscription = self._transHistSubscription
        if not transHistSubscription:
            transHistSubscription = acm.FTransactionHistorySubscription[self._subscriptionId]
        if not transHistSubscription:
            logger.debug('Fetching FTransactionHistorySubscription object for subscriber "%s"', (str(self._subscriptionId)))
            transHistSubscription = self._CreateTransactionHistorySubscription()
        self._transHistSubscription = transHistSubscription
        return transHistSubscription

    def _CreateTransactionHistorySubscription(self):
        logger.info('Setting up new subscription entity for the first time.')
        transHistSubscription = acm.FTransactionHistorySubscription()
        transHistSubscription.SubscriptionId(self._subscriptionId)
        # Setting transaction number to current max number in the transhst table.
        transHistSubscription.TransactionNumber(acm.TransactionHistory.GetLastTransactionNumber())
        transHistSubscription.Commit()
        return transHistSubscription

    def CurrentTransactionNumber(self):
        return self.TransHistSubscription().TransactionNumber()

    def SortedHistoryTransactions(self, sqlQuery):
        transactions = acm.FArray()
        unsortedTransactions = acm.FTransactionHistory.Select(sqlQuery)
        if len(unsortedTransactions) > 0:
            transactions = unsortedTransactions.SortByProperty('Oid', True)
            if self._lastSequenceNumber < transactions.Last().SeqNbr():
                self._lastSequenceNumber = transactions.Last().SeqNbr()
            logger.debug('Found %i transactions.', len(transactions))
            assert len(transactions) == len(unsortedTransactions)
        else:
            logger.debug('No transactions found. (%s)', sqlQuery)
        return transactions

    def AcceptTransactions(self):
        if self._lastSequenceNumber > 0:
            sub = self.TransHistSubscription()
            sub.TransactionNumber(self._lastSequenceNumber)
            sub.Commit()
            logger.info('Accepting transaction up to: %i', self._lastSequenceNumber)
