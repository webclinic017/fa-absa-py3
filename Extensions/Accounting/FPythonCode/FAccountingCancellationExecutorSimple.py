""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingCancellationExecutorSimple.py"

import acm

# operations
from FOperationsExceptions import CommitException

# accounting
from FAccountingSorting import SortOrderDefault
from FAccountingDRCRPairGenerator import GenerateDRCRPairs
from FAccountingPairReverser import PerformCancellation

#-------------------------------------------------------------------------
# Simple cancellation executor that can reverse a set of journals
#-------------------------------------------------------------------------
def PerformCancellations(journals, processDate):
    reversals = __PrepareData(journals, processDate)
    __CommitData(reversals)

#-------------------------------------------------------------------------
def __PrepareData(journals, processDate):
    reversals = list()

    for pair in GenerateDRCRPairs(journals):

        for reversalPair in PerformCancellation(pair, processDate):

            reversals.extend(reversalPair.Journals())
            reversals.append(reversalPair.JournalLink())

    return reversals

#-------------------------------------------------------------------------
def __CommitData(objects):
    objects.sort(key= lambda j: SortOrderDefault(j), reverse=True)

    acm.BeginTransaction()
    try:
        for obj in objects:
            obj.Commit()

        acm.CommitTransaction()
    except Exception as e:
        acm.AbortTransaction()
        raise CommitException('ERROR: Failed to commit cancellation: %s' % str(e))
