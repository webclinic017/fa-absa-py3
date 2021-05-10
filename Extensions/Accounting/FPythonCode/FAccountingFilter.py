""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingFilter.py"

#-------------------------------------------------------------------------
# Filter functions
#-------------------------------------------------------------------------
def IsSameSource(journal, sourceObject, currency):
    return journal.SourceObject() == sourceObject and journal.Currency() == currency and not journal.IsUserCreatedJournal()

#-------------------------------------------------------------------------
def IsVaildForBalance(journal, keyFunc):
    return keyFunc(journal) != None and not journal.IsExchangeRateMissing() and not journal.IsBaseAmountCalculationFailed()
