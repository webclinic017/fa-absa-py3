""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingEngineRevaluationCreator.py"

import acm

# operations
from FOperationsTransactionModifiers import SortingTransactionModifier
from FOperationsTransactionCommitter import TransactionCommitter
from FOperationsTransactionWriter import TransactionWriter
from FOperationsTaskConfiguration import Configuration

# accounting
from FAccountingSorting import SortOrderDefaultTup
from FAccountingRevaluator import Revaluator
from FAccountingEngineRevaluation import RevaluationEngine
from FAccountingOperations import GetOperations
from FAccountingSplitTransactionPairUpdater import SplitTransactionPairUpdater
from FAccountingCommitterResult import MultipleUpdatesResult

#-------------------------------------------------------------------------
def CreateRevaluationGenerationEngine(logger, committerIF=None):
    import FAccountingParams as Params

    partitionKeys = acm.GetDefaultContext().MemberNames('FExtensionValue', 'accounting ledger keys', '')

    committer = committerIF if committerIF else TransactionCommitter(GetOperations(), MultipleUpdatesResult)
    transactionWriter = TransactionWriter(committer, SortingTransactionModifier(SortOrderDefaultTup))
    revaluator = Revaluator(Params.createZeroAmountJournals)

    configuration = dict()
    configuration['loggerIF'] = logger
    configuration['writerIF'] = transactionWriter
    configuration['revaluatorIF'] = revaluator
    configuration['partitionKeys'] = partitionKeys
    configuration['isSupportedObjectCb'] = lambda obj : True
    configuration['updaterIF'] = SplitTransactionPairUpdater(1000)

    return RevaluationEngine(Configuration(configuration))