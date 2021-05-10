""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingEngineBalanceCreator.py"

import acm

# operations
from FOperationsTransactionModifiers import SortingTransactionModifier
from FOperationsTransactionCommitter import TransactionCommitter
from FOperationsTransactionWriter import TransactionWriter
from FOperationsTaskConfiguration import Configuration

# accounting
from FAccountingSorting import SortOrderBalancesTup
from FAccountingEngineBalance import BalanceEngine
from FAccountingCommitterResult import MultipleUpdatesResult
from FAccountingOperations import GetOperations
from FAccountingSplitTransactionPairUpdater import SplitTransactionPairUpdater

#-------------------------------------------------------------------------
def CreateBalanceGenerationEngine(logger, committerIF=None):
    partitionKeys = acm.GetDefaultContext().MemberNames('FExtensionValue', 'accounting ledger keys', '')

    committer = committerIF if committerIF else TransactionCommitter(GetOperations(), MultipleUpdatesResult)
    transactionWriter = TransactionWriter(committer, SortingTransactionModifier(SortOrderBalancesTup))

    configuration = dict()
    configuration['loggerIF'] = logger
    configuration['writerIF'] = transactionWriter
    configuration['partitionKeys'] = partitionKeys
    configuration['isSupportedObjectCb'] = lambda obj : True
    configuration['updaterIF'] = SplitTransactionPairUpdater(1000)

    return BalanceEngine(Configuration(configuration), 1000)