""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingSuspenseGenerator.py"

# itertools
from itertools import groupby

# accounting
from FAccountingCalculations import IsAmountZero, CalculateDebitCreditDelta
from FAccountingCreation import CreateSuspenseJournal

#-------------------------------------------------------------------------
# Creator for generating suspense journals
#-------------------------------------------------------------------------
def GenerateSuspense(journals):
    suspenseJournals = list()

    for _, journals in groupby(sorted(journals, key=__Sort), key=__Sort):
        journals = list(journals)
        diffLocal, diffBase = CalculateDebitCreditDelta(journals)

        if IsAmountZero(diffLocal) and IsAmountZero(diffBase):
            continue
        else:
            suspenseJournals.append(__GenerateJournal(diffLocal, diffBase, journals[0]))

    return suspenseJournals

#-------------------------------------------------------------------------
def __Sort(journal):
    return journal.Currency()

#-------------------------------------------------------------------------
def __GenerateJournal(diffLocal, diffBase, firstJournal):
    info = firstJournal.JournalInformation()
    curr = firstJournal.Currency()
    ed = firstJournal.EventDate()
    vd = firstJournal.ValueDate()
    pd = firstJournal.ProcessDate()
    ap = firstJournal.AccountingPeriod()
    jl = firstJournal.JournalLink()
    status = firstJournal.JournalType()

    return CreateSuspenseJournal(diffLocal, diffBase, info, curr, ed, vd, pd, jl, ap, status)
    