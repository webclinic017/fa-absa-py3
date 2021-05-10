""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/templates/FAccountingHooksTemplate.py"
import acm

# accounting
from FAccountingEnums import ReportingClass

def GetDynamicAccount(journal, parentAccount):
    """
    DESCRIPTION:    A function that creates dynamic T-Account for journal.
                    Please do not commit in the hook, just return T-Account.
    INPUT:          FJournal and corresponding T-Account
    OUTPUT:         FTAccount
    """
    tAccount = acm.FTAccount()
    tAccount.Name("Warning Using The Default Hook")
    tAccount.Number("Warning Using The Default Hook")
    tAccount.ReportingClass(ReportingClass.TACCOUNT)
    tAccount.Active(True)
    return tAccount

def GetTradesForEOD():
    """
    DESCRIPTION:    A function that determines which trades that should be processed in the accounting
                    End of Day process. Please note that if this hook is not configured in the FAccountingParams
                    the trades that matched the parameter "tradeFilterQueries" will be processed.
    INPUT:          None
    OUTPUT:         A list containing the trades that should be processed in End of Day.
    """
    return list()

def GetSettlementsForEOD():
    """
    DESCRIPTION:    A function that determines which settlements that should be processed in the accounting
                    End of Day process. Please note that if this hook is not configured in the FAccountingParams
                    the settlements that matched the parameter "settlementFilterQueries" will be processed.
    INPUT:          None
    OUTPUT:         A list containing the settlements that should be processed in End of Day.
    """
    return list()

def GetDaysBackAsDateTrade(trade):
    """
    DESCRIPTION:    A function that determines the start date for journal creation for trade accounting.
    INPUT:          An FTrade
    OUTPUT:         A string representing a date
    """
    accountingCurrency = acm.FCurrency[str(acm.UsedAccountingCurrency())]
    return accountingCurrency.Calendar().AdjustBankingDays(acm.Time.DateToday(), -3)

def GetDaysBackAsDateSettlement(settlement):
    """
    DESCRIPTION:    A function that determines the start date for journal creation for settlement accounting.
    INPUT:          An FSettlement
    OUTPUT:         A string representing a date
    """
    accountingCurrency = acm.FCurrency[str(acm.UsedAccountingCurrency())]
    return accountingCurrency.Calendar().AdjustBankingDays(acm.Time.DateToday(), -3)


def GetCommitJournalLogMessage(journal, actionString):
    """
    DESCRIPTION:    A function that returns a log string that will be included in the log
                    when the journal is committed.
    INPUT:          A FJournal to be committed. Treat as read-only.
                    A string representing the type of action being performed on the journal.
    OUTPUT:         A string representing the log message
    """

    aIName = ''
    tradeOrSettlementOid = '\n'
    if journal.AccountingInstruction():
        aIName = journal.AccountingInstruction().Name()
    if journal.Trade():
        tradeOrSettlementOid = ' for trade %d\n' % journal.Trade().Oid()
    if journal.Settlement():
        tradeOrSettlementOid = ' for settlement %d\n' % journal.Settlement().Oid()
    accountNumber = journal.Account().Number()
    accountName = journal.Account().Name()
    bookName = journal.Book().Name()

    logString = actionString + ' Journal %d' % journal.Oid() + tradeOrSettlementOid \
    + '\tValue date: %s\n' % journal.ValueDate() \
    + '\tEvent date: %s\n' % journal.EventDate() \
    + '\tAmount: %s %f %s\n' % (journal.DebitOrCredit(), journal.Amount(), journal.Currency().Name())  \
    + '\tAccount name: %s\n' % accountName \
    + '\tAccount number: %s\n' %  accountNumber \
    + '\tAccounting instruction: %s\n' % aIName \
    + '\tBook: %s' % bookName
    return logString


def IsValidTrade(trade):
    """
    DESCRIPTION:    A function validating if a trade is valid for accounting processing.
    INPUT:          An FTrade  to be validated. Treat as read-only.
    OUTPUT:         True or False
    """

    return True

def JournalModification(journal):
    """
    DESCRIPTION:    A function modifying a journal. It is possible to set CustomType and
                    add additional infos.
    INPUT:          A journal to be modified.
    OUTPUT:         Modified journal
    """
    return journal

def JournalInformationModification(journalInformation):
    """
    DESCRIPTION:    A function modifying a journal information. It is possible to add
                    additional infos.
    INPUT:          A journal information to be modified.
    OUTPUT:         Modified journal information.
    """
    return journalInformation
