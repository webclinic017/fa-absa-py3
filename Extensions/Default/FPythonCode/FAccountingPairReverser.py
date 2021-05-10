""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingPairReverser.py"

import acm

from FOperationsUtils import IsCorrectedTrade

from FAccountingEnums import ReversalType, JournalType, DebitOrCredit
from FAccountingDRCRPairGenerator import GenerateDRCRPairs

#-------------------------------------------------------------------------
# Use this function to reverse a debit/credit pair according to the accounting instruction.
# If no ai is set, fallback to regular cancellation
#-------------------------------------------------------------------------
def PerformReversal(pair, eventDate, processDate):
    return __PerformReversal(pair, __GetReversalType(pair), eventDate, processDate)

#-------------------------------------------------------------------------
# Use this function to cancel a debit/credit pair (always non periodic reversal)
#-------------------------------------------------------------------------
def PerformCancellation(pair, eventDate, processDate):
    return __PerformReversal(pair, ReversalType.NON_PERIODIC_REVERSAL, eventDate, processDate)

#-------------------------------------------------------------------------
# Private functions
#-------------------------------------------------------------------------
def __PerformReversal(pair, rType, eventDate, processDate):
    pairs = list()

    # Cancel previous reversal
    cancellationPairs = GenerateDRCRPairs([r.Clone() for j in pair.Journals() for r in j.ReversalJournals()])

    for revPair in cancellationPairs:
        pairs.extend(PerformCancellation(revPair, revPair.EventDate(), processDate))

    # Create new reversal
    link = acm.FJournalLink()
    inverseFunc = lambda j: __CreateInverse(j, rType, eventDate, processDate, link)

    cancellationPairs = [newPair for newPair in GenerateDRCRPairs([inverseFunc(j) for j in pair.Journals()], True)]

    for cancellationPair in cancellationPairs:
        cancellationPair.GenerateSuspenseJournals()

    pairs.extend(cancellationPairs)
    pairs.append(pair)

    return pairs

#-------------------------------------------------------------------------
def __CreateInverse(journal, rType, eventDate, processDate, jl):

    assert journal.JournalType() != JournalType.REVERSED, \
        "Trying to reverse a reversed journal: {}".format(str(journal))

    inverse = acm.FJournal()
    inverse.Apply(journal)
    inverse.Balance(None)
    inverse.JournalLink(jl)
    inverse.JournalInformation(journal.JournalInformation())
    inverse.DebitOrCredit(DebitOrCredit.CREDIT if inverse.DebitOrCredit() == DebitOrCredit.DEBIT else DebitOrCredit.DEBIT)
    inverse.EventDate(eventDate)
    inverse.ProcessDate(processDate)
    inverse.Amount(-journal.Amount())
    inverse.BaseAmount(-journal.BaseAmount())
    inverse.ReversedJournal(journal.OriginalOrSelf())
    journal.ReversedJournal(None)
    journal.ReversalJournals().Add(inverse)

    if eventDate:
        assert inverse.Book(), "The journal does not belong to any book"

        ap = inverse.Book().FindPeriodByDate(eventDate)

        assert ap, "No accounting period found that matches the journals event date"

        inverse.AccountingPeriod(ap)
        inverse.ValueDate(ap.AdjustDateToPeriod(eventDate))

    else:
        inverse.ValueDate(None)

    __SetReversalType(journal, inverse, rType)
    __SetStatusExplanation(journal, inverse)

    return inverse

#-------------------------------------------------------------------------
def __SetReversalType(journal, inverse, rType):
    if rType == ReversalType.PERIODIC_REVERSAL:
        journal.JournalType(JournalType.PERIODIC_REVERSED)
        inverse.JournalType(JournalType.PERIODIC_REVERSAL)

    elif rType == ReversalType.NON_PERIODIC_REVERSAL:
        journal.JournalType(JournalType.REVERSED)
        inverse.JournalType(JournalType.REVERSAL)

    else:
        journal.JournalType(JournalType.REALLOCATION_REVERSED)
        inverse.JournalType(JournalType.REALLOCATION_REVERSAL)

#-------------------------------------------------------------------------
def __SetStatusExplanation(journal, inverse):
    if journal.Trade() and IsCorrectedTrade(journal.Trade()):
        journal.IsCorrectTradeReversed(True)
        inverse.IsCorrectTradeReversed(True)

#-------------------------------------------------------------------------
def __GetReversalType(pair):
    ai = pair.AccountingInstruction()

    if ai:
        if ai.IsNonPeriodic():
            return ReversalType.NON_PERIODIC_REVERSAL
        elif ai.IsPeriodic():
            return ReversalType.PERIODIC_REVERSAL
        elif ai.IsReallocation():
            return ReversalType.REALLOCATION_REVERSAL
        else:
            raise Exception('Unsupported reversal type for accounting instruction {}'.format(ai.Name()))
    else:
        return ReversalType.NON_PERIODIC_REVERSAL

