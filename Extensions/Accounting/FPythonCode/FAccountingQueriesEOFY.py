""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingQueriesEOFY.py"

import acm

# accounting
from FAccountingEnums import JournalCategory, JournalType

#-------------------------------------------------------------------------
# Queries used by the balance generation engine
#-------------------------------------------------------------------------
def GetLiveRollForwardJournalsForPeriodQuery(period):
    query = acm.CreateFASQLQuery(acm.FJournal, 'AND')
    query.AddAttrNode('JournalType', 'EQUAL', JournalType.LIVE)
    query.AddAttrNode('AccountingPeriod.Oid', 'EQUAL', period.Oid())
    query.AddAttrNode('JournalCategory', 'EQUAL', JournalCategory.END_OF_FISCAL_YEAR)
    return query

#-------------------------------------------------------------------------
def GetBalancesForPeriodQuery(period):
    query = acm.CreateFASQLQuery(acm.FJournal, 'AND')
    query.AddAttrNode('JournalCategory', 'EQUAL', JournalCategory.BALANCE)
    query.AddAttrNode('JournalType', 'NOT_EQUAL', JournalType.SIMULATED)
    query.AddAttrNode('AccountingPeriod.Oid', 'EQUAL', period.Oid())

    return query

#-------------------------------------------------------------------------
def GetAccountingPeriodOfTypeQuery(fiscalYear, book, periodType):
    query = acm.CreateFASQLQuery(acm.FAccountingPeriod, 'AND')
    query.AddAttrNode('FiscalYear', 'EQUAL', fiscalYear)
    query.AddAttrNode('Book.Oid', 'EQUAL', book.Oid())
    query.AddAttrNode('Type', 'EQUAL', periodType)
    return query