""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/scripts/FAccountingReverseManualJournals.py"
from itertools import groupby

import acm, time

from FAccountingQueries import GetManualJournalsForReversalDateQuery
from FAccountingEnums import DebitOrCredit, JournalType

#-------------------------------------------------------------------------
def __CreateInverse(journal, eventDate, processDate):

    inverse = acm.FJournal()
    inverse.Apply(journal)
    inverse.Balance(None)
    inverse.JournalLink(None)
    inverse.JournalInformation(journal.JournalInformation())
    inverse.DebitOrCredit(DebitOrCredit.CREDIT if inverse.DebitOrCredit() == DebitOrCredit.DEBIT else DebitOrCredit.DEBIT)
    inverse.EventDate(eventDate)
    inverse.ProcessDate(processDate)
    inverse.Amount(-journal.Amount())
    inverse.BaseAmount(-journal.BaseAmount())
    inverse.ReversedJournal(journal.OriginalOrSelf())
    journal.ReversedJournal(None)


    if eventDate:
        assert inverse.Book(), "The journal does not belong to any book"

        ap = inverse.Book().FindPeriodByDate(eventDate)

        assert ap, "No accounting period found that matches the journals event date"

        inverse.AccountingPeriod(ap)
        inverse.ValueDate(ap.AdjustDateToPeriod(eventDate))

    else:
        inverse.ValueDate(None)

    journal.JournalType(JournalType.REVERSED)
    inverse.JournalType(JournalType.REVERSAL)

    return inverse

#-------------------------------------------------------------------------
def ReverseJournals(journals, reversalDate):
    transaction = list()

    for journal in journals:
        transaction.append(journal)
        transaction.append(__CreateInverse(journal, reversalDate, acm.Time.DateToday()))

    return transaction

#-------------------------------------------------------------------------
def CommitJournals(journals):
    acm.BeginTransaction()
    try:
        for journal in journals:
            journal.Commit()
        acm.CommitTransaction()
    except Exception as e:
        acm.AbortTransaction()
        acm.Log('Exception occurred while committing journals: ' + str(e))

#-------------------------------------------------------------------------
def ProcessBook(book, reversalDate):
    keyfunc = lambda journal : journal.JournalInformation().Oid()

    manualJournals = GetManualJournalsForReversalDateQuery(book, reversalDate).Select()
    manualJournals = sorted(manualJournals, key=keyfunc)

    acm.Log("%d manual journals selected to reverse.\n" % len(manualJournals))

    for _, journals in groupby(manualJournals, key=keyfunc):
        reversedJournals = ReverseJournals(list(journals), reversalDate)
        CommitJournals(reversedJournals)


#-------------------------------------------------------------------------
ael_variables = [['books', 'Books', 'string', acm.FBook.Select(""), None, 1, 1, 'The books to reverse manual journals for.', None, 1],
                 ['reversalDate', 'Reversal Date', 'string', None, acm.Time.DateToday(), 0, 1, 'The date on which to reverse manual journals.', None, 1]]

#-------------------------------------------------------------------------
def ael_main(variablesDict):
    books = [acm.FBook[name] for name in variablesDict['books']]
    reversalDate = acm.Time.AsDate(variablesDict['reversalDate'])

    if not reversalDate:
        reversalDate = acm.Time.DateToday()

    acm.Log('Manual journal reversing started at %s.\n' % time.ctime())

    acm.Log('Reversal date: %s' % reversalDate)

    for book in books:
        period = book.FindPeriodByDate(reversalDate)

        if period:
            ProcessBook(book, reversalDate)
        else:
            acm.Log('The reversal date %s is not in an open accounting period.\n' % reversalDate)

    acm.Log('Manual journal reversing ended at %s.\n' % time.ctime())
