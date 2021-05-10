""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingCreation.py"
import acm

# accounting
from FAccountingLedgerKeyParser import SetValuesFromLedgerKey
from FAccountingEnums import JournalType, DebitOrCredit, JournalCategory, AccountingPeriodStatus

#-------------------------------------------------------------------------
def CreateBalanceFromAttributes(amount, baseAmount, journal, period, ledgerKeyAttributes):
    balance = CreateBalance(amount, baseAmount, journal.Currency(), journal.ChartOfAccount(), period)

    info = acm.FJournalInformation()
    info.Book(journal.Book())
    balance.JournalInformation(info)
    SetValuesFromLedgerKey(ledgerKeyAttributes, journal, balance)

    return balance

#-------------------------------------------------------------------------
def CreateBalance(amount, baseAmount, currency, chartOfAccount, period):
    balance = acm.FJournal()
    balance.JournalType(JournalType.LIVE)
    balance.JournalCategory(JournalCategory.BALANCE)
    balance.Amount(amount)
    balance.BaseAmount(baseAmount)
    balance.Currency(currency)
    balance.ChartOfAccount(chartOfAccount)
    balance.AccountingPeriod(period)
    return balance

#-------------------------------------------------------------------------
def CreateJournal(amount, baseAmount, chartOfAccount, currency, category, journalInfo, date, accountingPeriod, processDate, debitOrCredit = None):
    journal = acm.FJournal()
    journal.ChartOfAccount(chartOfAccount)
    journal.Currency(currency)
    journal.Amount(amount)
    journal.BaseAmount(baseAmount)
    journal.DebitOrCredit(debitOrCredit if debitOrCredit else (DebitOrCredit.CREDIT if baseAmount < 0 else DebitOrCredit.DEBIT))
    journal.JournalCategory(category)
    journal.JournalType(JournalType.LIVE)
    journal.JournalInformation(journalInfo)
    journal.AccountingPeriod(accountingPeriod)
    journal.EventDate(date)
    journal.ProcessDate(processDate)
    journal.ValueDate(date)
    return journal

#-------------------------------------------------------------------------
def CreateSuspenseJournal(diffLocal, diffBase, info, curr, eventDate, \
                          valueDate, processDate, journalLink, ap, \
                          status):
    book = info.Book()
    chartOfAccount = book.SuspenseChartOfAccount()

    suspense = acm.FJournal()
    suspense.Amount(-diffLocal)
    suspense.BaseAmount(-diffBase)
    suspense.JournalInformation(info)
    suspense.JournalType(JournalType.LIVE)
    suspense.JournalCategory(JournalCategory.STANDARD)
    suspense.IsSuspenseAccountAmountDifference(True)
    suspense.Currency(curr)
    suspense.EventDate(eventDate)
    suspense.ValueDate(valueDate)
    suspense.AccountingPeriod(ap)
    suspense.ChartOfAccount(chartOfAccount)
    suspense.ProcessDate(processDate)
    suspense.JournalType(status)
    suspense.DebitOrCredit(DebitOrCredit.CREDIT if (diffLocal > 0 or diffBase > 0) else DebitOrCredit.DEBIT)
    suspense.JournalLink(journalLink)
    return suspense

#-------------------------------------------------------------------------
def CreateFXRevaluationJournals(journal, revalAmount, date, tAccountLedgerKeyMapper, revalAccount):

    period = journal.Book().FindPeriodByDate(date)
    ledgerKey = journal.Account().LedgerKey()

    journalInfo = acm.FJournalInformation()
    journalInfo.Book(journal.Book())

    sourceAccountDebitOrCredit = DebitOrCredit.CREDIT if revalAmount < 0 else DebitOrCredit.DEBIT
    revaluationAccountDebitOrCredit = DebitOrCredit.CREDIT if sourceAccountDebitOrCredit == DebitOrCredit.DEBIT else DebitOrCredit.DEBIT

    sourceAccountJournal = CreateJournal(0, revalAmount, journal.ChartOfAccount(), \
         journal.Currency(), JournalCategory.FX_REVALUATION, journalInfo, date, period, journal.Book().ProcessDate(), sourceAccountDebitOrCredit)

    revaluationAccountJournal = CreateJournal(0, -revalAmount, revalAccount, \
         journal.Currency(), JournalCategory.FX_REVALUATION, journalInfo, date, period, journal.Book().ProcessDate(), revaluationAccountDebitOrCredit)

    if ledgerKey:
        attributesToSet = tAccountLedgerKeyMapper.GetLedgerKeyAttributes(journal.Account())
        SetValuesFromLedgerKey(attributesToSet, journal, sourceAccountJournal)
        journalAttributes = [(domain, attribute) for (domain, attribute) in attributesToSet if domain in ['FJournal', 'FJournalAdditionalInfo']]
        SetValuesFromLedgerKey(journalAttributes, journal, revaluationAccountJournal)

    return [sourceAccountJournal, revaluationAccountJournal]

#-------------------------------------------------------------------------
def CreateRollForwardJournals(amount, baseAmount, balance, accountingPeriod, tAccountLedgerKeyMapper):
    rollForwardChartOfAccount = balance.ChartOfAccount().RollForwardChartOfAccount()

    journalInfo = acm.FJournalInformation()
    journalInfo.Book(balance.Book())

    sourceAccountJournal = CreateJournal(-amount, -baseAmount, balance.ChartOfAccount(), \
         balance.Currency(), JournalCategory.END_OF_FISCAL_YEAR, journalInfo, None, accountingPeriod, None)

    rollForwardJournal = CreateJournal(amount, baseAmount, rollForwardChartOfAccount, \
         balance.Currency(), JournalCategory.END_OF_FISCAL_YEAR, journalInfo, None, accountingPeriod, None)

    attributesToSet = tAccountLedgerKeyMapper.GetLedgerKeyAttributes(balance.Account())
    SetValuesFromLedgerKey(attributesToSet, balance, sourceAccountJournal)
    journalAttributes = [(domain, attribute) for (domain, attribute) in attributesToSet if domain in ['FJournal', 'FJournalAdditionalInfo']]
    SetValuesFromLedgerKey(journalAttributes, balance, rollForwardJournal)

    if sourceAccountJournal.DebitOrCredit() == rollForwardJournal.DebitOrCredit():
        sourceAccountJournal.DebitOrCredit(DebitOrCredit.CREDIT if rollForwardJournal.DebitOrCredit() == DebitOrCredit.DEBIT else DebitOrCredit.DEBIT)

    return [sourceAccountJournal, rollForwardJournal]

#-------------------------------------------------------------------------
def CreateAccountingPeriod(fiscalYear, book, periodType):
    accountingPeriod = acm.FAccountingPeriod()
    accountingPeriod.FiscalYear(fiscalYear)
    accountingPeriod.HasJournals(True)
    accountingPeriod.Status(AccountingPeriodStatus.CLOSED)
    accountingPeriod.Book(book)
    accountingPeriod.Type(periodType)
    return accountingPeriod

#-------------------------------------------------------------------------
def CreateChartOfAccount(parentChartOfAccount, tAccount):
    chartOfAccount = acm.FChartOfAccount()
    chartOfAccount.Parent(parentChartOfAccount)
    chartOfAccount.Book(parentChartOfAccount.Book())
    chartOfAccount.Account(tAccount)
    return chartOfAccount
