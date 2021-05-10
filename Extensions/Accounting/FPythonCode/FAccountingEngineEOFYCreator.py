""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingEngineEOFYCreator.py"

import acm

# operations
from FOperationsTransactionModifiers import SortingTransactionModifier
from FOperationsTransactionWriter import TransactionWriter
from FOperationsTransactionCommitter import TransactionCommitter
from FOperationsTaskConfiguration import Configuration

# accounting
from FAccountingCommitterResult import MultipleUpdatesResult
from FAccountingEngineEOFY import EOFYEngine
from FAccountingOperations import GetOperations
from FAccountingSorting import SortOrderBalancesTup
from FAccountingRollForward import BalanceRollForward
from FAccountingSplitTransactionPairUpdater import SplitTransactionPairUpdater

#-------------------------------------------------------------------------
def CreateEOFYGenerationEngine(fiscalYear, logger, committerIF=None):
    partitionKeys = acm.GetDefaultContext().MemberNames('FExtensionValue', 'accounting ledger keys', '')

    committer = committerIF if committerIF else TransactionCommitter(GetOperations(), MultipleUpdatesResult)
    transactionWriter = TransactionWriter(committer, SortingTransactionModifier(SortOrderBalancesTup))
    rollForwarder = BalanceRollForward(fiscalYear)

    configuration = dict()
    configuration['loggerIF'] = logger
    configuration['writerIF'] = transactionWriter
    configuration['rollForwardIF'] = rollForwarder
    configuration['partitionKeys'] = partitionKeys
    configuration['isSupportedObjectCb'] = lambda o : True
    configuration['updaterIF'] = SplitTransactionPairUpdater(1000)

    return EOFYEngine(Configuration(configuration))