""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingSorting.py"
import acm

from FAccountingEnums import JournalCategory, JournalType

#-------------------------------------------------------------------------
def SortOrderDefaultTup(tup):
    _, obj = tup

    return SortOrderDefault(obj)

#-------------------------------------------------------------------------
def SortOrderBalancesTup(tup):
    _, obj = tup

    return SortOrderBalances(obj)

#-------------------------------------------------------------------------
def SortOrderDefault(obj):

    if obj.IsKindOf(acm.FJournal):
        return SortOrderJournal(obj.JournalType())
    elif obj.IsKindOf(acm.FChartOfAccount):
        return 50
    elif obj.IsKindOf(acm.FJournalLink):
        return 60
    elif obj.IsKindOf(acm.FJournalInformation):
        return 70
    elif obj.IsKindOf(acm.FAccountingPeriod):
        return 80
    elif obj.IsKindOf(acm.FTAccount):
        return 90
    else:
        raise Exception('ERROR: Trying to commit unsupported object: {} {}'.format(obj.ClassName(), obj.Oid()))

#-------------------------------------------------------------------------
def SortOrderBalances(obj):

    if obj.IsKindOf(acm.FJournal):
        if obj.JournalCategory() == JournalCategory.BALANCE:
            return 20
        else:
            return SortOrderJournal(obj.JournalType())
    elif obj.IsKindOf(acm.FJournalInformation):
        return 50
    elif obj.IsKindOf(acm.FJournalLink):
        return 10

#-------------------------------------------------------------------------
def SortOrderJournal(journalType):
    if journalType == JournalType.LIVE:
        return 7
    elif journalType == JournalType.REVERSED:
        return 6
    elif journalType == JournalType.REVERSAL:
        return 5
    elif journalType == JournalType.PERIODIC_REVERSED:
        return 4
    elif journalType == JournalType.PERIODIC_REVERSAL:
        return 3
    elif journalType == JournalType.REALLOCATION_REVERSED:
        return 2
    elif journalType == JournalType.REALLOCATION_REVERSAL:
        return 1
    else:
        raise Exception('ERROR: Unsupported journal status {}'.format(journalType))

