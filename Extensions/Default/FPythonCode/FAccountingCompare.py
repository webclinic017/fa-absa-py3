""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingCompare.py"

import acm

# operations
from FOperationsCompare import IsEqualAddInfos

# accounting
from FAccountingEnums import JournalType, ReversalExclusion, JournalCategory, DebitOrCredit
from FAccountingDates import IsLastBankingDayOfMonth, IsLastBankingDayOfYear

#-------------------------------------------------------------------------
# Comparing journals functions
#-------------------------------------------------------------------------
def IsAmendmentPreventLive(new, old):
    if new and old:
        return new.PreventLiveJournal() and old.JournalType() == JournalType.PERIODIC_REVERSED
    return False

#-------------------------------------------------------------------------
def IsSupressed(previous, new):
    if previous and new and new.AccountingInstruction().SuppressIfUnchanged():
        return not __IsJournalChanged(previous, new)
    return False

#-------------------------------------------------------------------------
def IsAmendment(new, old, processDate):
    if not new or not old:
        return True
    if old.JournalType() != JournalType.LIVE and old.Book().OnlyReverseLiveJournals():
        return False
    if new.EventDate() < processDate and not new.AccountingInstruction().AmendHistoricJournals():
        return False
    if new.EventDate() != old.EventDate():
        return True
    if __IsJournalChanged(new, old):
        return True
    return False

#-------------------------------------------------------------------------
def __IsJournalChanged(j1, j2):
    if j1.JournalInformation() != j2.JournalInformation():
        return True
    if not IsAmountEqual(j1, j2):
        return True
    if not IsBaseAmountEqual(j1, j2):
        return True
    if j1.ChartOfAccount() != j2.ChartOfAccount():
        return True
    if j1.Currency() != j2.Currency():
        return True
    if j1.DebitOrCredit() != j2.DebitOrCredit():
        return True
    if not IsEqualAddInfos(j1, j2):
        return True
    return False

#-------------------------------------------------------------------------
def IsAmountEqual(j1, j2):
    return acm.Math.AlmostEqual(j1.Amount(), j2.Amount())

#-------------------------------------------------------------------------
def IsBaseAmountEqual(j1, j2):
    return acm.Math.AlmostEqual(j1.BaseAmount(), j2.BaseAmount())

#-------------------------------------------------------------------------
# Comparing attributes of a single journal
#-------------------------------------------------------------------------
def IsLive(journal):
    return journal.JournalType() == JournalType.LIVE

#-------------------------------------------------------------------------
def IsManual(journal):
    return journal.ManualJournal()

#-------------------------------------------------------------------------
def IsPreventHistoricalAmendments(journal):
    if journal and journal.IsPeriodic() and journal.EventDate() <= journal.Book().ProcessDate():
        if not journal.AccountingInstruction().AmendHistoricJournals():
            return True
    return False

#-------------------------------------------------------------------------
def IsReversalExclusion(journal):
    calendar = journal.Book().GetUsedCalendar()
    excludeReversals = journal.AccountingInstruction().ReversalExclusion()

    if excludeReversals == ReversalExclusion.LAST_DAY_OF_MONTH:
        return IsLastBankingDayOfMonth(journal.EventDate(), calendar)
    elif excludeReversals == ReversalExclusion.LAST_DAY_OF_YEAR:
        return IsLastBankingDayOfYear(journal.EventDate(), calendar)
    elif excludeReversals == ReversalExclusion.ALWAYS:
        return True
    return False

#-------------------------------------------------------------------------
def IsReversal(journal):
    return journal.JournalType() == JournalType.REVERSAL or \
           journal.JournalType() == JournalType.PERIODIC_REVERSAL or \
           journal.JournalType() == JournalType.REALLOCATION_REVERSAL

#-------------------------------------------------------------------------
def IsLiveFXReval(journal):
    return IsLive(journal) and journal.JournalCategory() == JournalCategory.FX_REVALUATION

#-------------------------------------------------------------------------
def BelongsToDebitSide(journal):
    return (journal.DebitOrCredit() == DebitOrCredit.DEBIT) ^ (journal.JournalType() in (JournalType.PERIODIC_REVERSAL, JournalType.REVERSAL))


#-------------------------------------------------------------------------
# Comparing journalinformations functions
#-------------------------------------------------------------------------

def IsEqualJournalInformation(ji1, ji2):
    if not ji1 or not ji2:
        return False

    if ji1.SourceObject() != ji2.SourceObject():
        return False

    if ji1.Trade() != ji2.Trade():
        return False

    if ji1.Settlement() != ji2.Settlement():
        return False

    if ji1.Instrument() != ji2.Instrument():
        return False

    if ji1.Portfolio() != ji2.Portfolio():
        return False

    if ji1.Book() != ji2.Book():
        return False

    if ji1.Treatment() != ji2.Treatment():
        return False

    if ji1.Leg() != ji2.Leg():
        return False

    if ji1.ContractTrade() != ji2.ContractTrade():
        return False

    if ji1.CombinationLink() != ji2.CombinationLink():
        return False

    if ji1.Acquirer() != ji2.Acquirer():
        return False

    if ji1.Broker() != ji2.Broker():
        return False

    if ji1.Counterparty() != ji2.Counterparty():
        return False

    if ji1.MoneyFlowType() != ji2.MoneyFlowType():
        return False

    if ji1.AccountingInstruction() != ji2.AccountingInstruction():
        return False

    if ji1.AggregationDate() != ji2.AggregationDate():
        return False

    if not IsEqualAddInfos(ji1, ji2):
        return False

    return True