""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingQueries.py"
import acm

# operations
from FOperationsQueries import CreateFilter

# accounting
from FAccountingEnums import JournalCategory, JournalType, AccountingPeriodStatus, AccountingPeriodType

#-------------------------------------------------------------------------
# Common query functions
#-------------------------------------------------------------------------
def CreateAIFilterTriggerType(triggerTypes):
    return CreateFilter(acm.FTreatmentLink, 'OR', 'AccountingInstruction.JournalTriggerType', triggerTypes, 'EQUAL')

#-------------------------------------------------------------------------
def CreateAIFilterOid(oids):
    return CreateFilter(acm.FTreatmentLink, 'OR', 'AccountingInstruction.Oid', oids, 'EQUAL')

#-------------------------------------------------------------------------
def CreateBookFilter(bookNames):
    return CreateFilter(acm.FBook, 'OR', 'Name', bookNames, 'EQUAL')

#-------------------------------------------------------------------------
# Common queries
#-------------------------------------------------------------------------
def GetJournalsForPeriodQuery(period, generationDate):
    query = acm.CreateFASQLQuery(acm.FJournal, 'AND')
    query.AddAttrNode('AccountingPeriod.Oid', 'EQUAL', period.Oid())
    query.AddAttrNode('Balance.Oid', 'EQUAL', 0)

    categoryNode = query.AddOpNode('OR')
    categoryNode.AddAttrNode('JournalCategory', 'EQUAL', JournalCategory.STANDARD)
    categoryNode.AddAttrNode('JournalCategory', 'EQUAL', JournalCategory.FX_REVALUATION)

    query.AddAttrNode('ValueDate', 'LESS_EQUAL', generationDate)
    query.AddAttrNode('JournalType', 'NOT_EQUAL', JournalType.SIMULATED)
    return query

#-------------------------------------------------------------------------
def GetManualJournalsForReversalDateQuery(book, reversalDate):
    query = acm.CreateFASQLQuery(acm.FJournal, 'AND')
    query.AddAttrNode('JournalCategory', 'EQUAL', JournalCategory.STANDARD)
    query.AddAttrNode('JournalType', 'EQUAL', JournalType.LIVE)
    query.AddAttrNode('ManualJournal', 'EQUAL', True)
    query.AddAttrNode('ManualReversalDate', 'Equal', reversalDate)
    query.AddAttrNode('JournalInformation.Book.Oid', 'EQUAL', book.Oid())
    return query

#-------------------------------------------------------------------------
def GetFXRevaluationsBeforeDateQuery(period, book, fxUplRevalAccount, currentValueDate):
    query = acm.CreateFASQLQuery(acm.FJournal, 'AND')
    query.AddAttrNode('JournalCategory', 'EQUAL', JournalCategory.FX_REVALUATION)
    query.AddAttrNode('JournalType', 'NOT_EQUAL', JournalType.SIMULATED)
    query.AddAttrNode('JournalInformation.Book.Oid', 'EQUAL', book.Oid())

    periodNode = query.AddOpNode('OR')
    periodNode.AddAttrNode('AccountingPeriod.Type', 'EQUAL', AccountingPeriodType.START_OF_FISCAL_YEAR)
    periodNode.AddAttrNode('ValueDate', 'LESS', currentValueDate)

    query.AddAttrNode('AccountingPeriod.FiscalYear', 'EQUAL', period.FiscalYear())
    query.AddAttrNode('ChartOfAccount.TAccount.Name', 'EQUAL', fxUplRevalAccount)
    return query

#-------------------------------------------------------------------------
def GetOpenAccountingPeriodFromDateQuery(book, dateInPeriod):
    query = acm.CreateFASQLQuery(acm.FAccountingPeriod, 'AND')
    query.AddAttrNode('Book.Oid', 'EQUAL', book.Oid())
    query.AddAttrNode('Status', 'EQUAL', AccountingPeriodStatus.OPEN)

    dateNode = query.AddOpNode('AND')
    dateNode.AddAttrNode('StartDate', 'LESS_EQUAL', dateInPeriod)
    dateNode.AddAttrNode('EndDate', 'GREATER_EQUAL', dateInPeriod)
    return query

#-------------------------------------------------------------------------
def GetAccountingPeriodsForFiscalYearQuery(book, fiscalYear):
    query = acm.CreateFASQLQuery(acm.FAccountingPeriod, 'AND')
    query.AddAttrNode('FiscalYear', 'EQUAL', fiscalYear)
    query.AddAttrNode('Book.Oid', 'EQUAL', book.Oid())

    return query

#-------------------------------------------------------------------------
def GetLiveBalancesForPeriodQuery(period):
    query = acm.CreateFASQLQuery(acm.FJournal, 'AND')
    query.AddAttrNode('AccountingPeriod.Oid', 'EQUAL', period.Oid())
    query.AddAttrNode('JournalType', 'EQUAL', JournalType.LIVE)
    query.AddAttrNode('JournalCategory', 'EQUAL', JournalCategory.BALANCE)
    return query

#-------------------------------------------------------------------------
def GetJournalsForBalanceQuery(balance):
    query = acm.CreateFASQLQuery(acm.FJournal, 'AND')
    query.AddAttrNode('Balance.Oid', 'EQUAL', balance.Oid())
    return query