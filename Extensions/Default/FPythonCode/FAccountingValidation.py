""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingValidation.py"

# accounting
from FAccountingEnums import JournalType, ReallocationStatus
from FAccountingDates import GetStartDate, GetEndDate

#-------------------------------------------------------------------------
# Validation functions
#-------------------------------------------------------------------------
def IsValidPeriodicReversal(journal):
    ai = journal.AccountingInstruction()
    return ai and ai.IsPeriodic() and journal.JournalType() == JournalType.LIVE

#-------------------------------------------------------------------------
def IsValidReallocationReversal(journal, newPair, oldPair):
    ai = journal.AccountingInstruction()

    if ai and ai.IsReallocation() and journal.ReallocationStatus() == ReallocationStatus.TO_BE_REALLOCATED:

        if journal.JournalType() == JournalType.LIVE:
            return True

        elif journal.JournalType() == JournalType.REALLOCATION_REVERSED:
            return (newPair and oldPair and newPair.EventDate() != oldPair.EventDate() and ai.AmendHistoricJournals())

    return False

#-------------------------------------------------------------------------
def IsValidForCancellation(journal, startDate, endDate, endOfDayDate, bookFilter, bookLinkFilter, treatmentLinkFilter):

    if journal.IsUserCreatedJournal():
        return False

    book = journal.Book()
    treatment = journal.Treatment()
    ai = journal.AccountingInstruction()

    bookLink = book.BookLink(treatment) if book and treatment else None
    treatmentLink = book.TreatmentLink(treatment, ai) if book and treatment and ai else None

    if journal.AccountingInstruction() and journal.AccountingInstruction().KeepHistoricJournals():
        return False

    if journal.Book() and bookFilter and not bookFilter.IsSatisfiedBy(journal.Book()):
        return False

    if bookLink and bookLinkFilter and not bookLinkFilter.IsSatisfiedBy(bookLink):
        return False

    if treatmentLink and treatmentLinkFilter and not treatmentLinkFilter.IsSatisfiedBy(treatmentLink):
        return False

    info = journal.JournalInformation()
    journalStartDate = GetStartDate(info, journal.EventDate(), startDate, endDate, endOfDayDate)
    journalEndDate = GetEndDate(info, journal.EventDate(), startDate, endDate, endOfDayDate)

    return IsLiveAndInTimeWindow(journal, journalStartDate, journalEndDate)

#-------------------------------------------------------------------------
def IsLiveAndInTimeWindow(journal, startDate, endDate):
    if journal.JournalType() in [JournalType.LIVE, JournalType.PERIODIC_REVERSED, JournalType.REALLOCATION_REVERSED]:
        if startDate and endDate and endDate >= journal.EventDate() and journal.EventDate() >= startDate:
            return True
        return False
    return False

#-------------------------------------------------------------------------
def IsValidForIncrementalBaseAmount(newJournal, prevJournal):
    isValid = False
    if newJournal and prevJournal and len(prevJournal.ReversalJournals()):

        reversal = prevJournal.ReversalJournals().First()
        isValid = reversal.JournalType() == JournalType.PERIODIC_REVERSAL and reversal.EventDate() == newJournal.EventDate()

    else:

        isValid = not prevJournal

    return isValid

#-------------------------------------------------------------------------
def IsValidForBalanceGeneration(generationDate, lastRevalDate):
    return not lastRevalDate or generationDate >= lastRevalDate