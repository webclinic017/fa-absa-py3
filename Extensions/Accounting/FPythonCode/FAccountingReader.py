""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingReader.py"



# accounting
from FAccountingDRCRPairGenerator import GenerateDRCRPairs

import FAccountingQueries as Queries
import FAccountingQueriesBase as QueriesBase
import FAccountingQueriesEOFY as QueriesEOFY
import FAccountingFilter as Filter
import FAccountingCompare as Compare

#-------------------------------------------------------------------------
def ReadPairs(ji, currency, startDate, endDate):

    journals = QueriesBase.GetRelatedJournalsForPeriodQuery(ji, startDate, endDate).Select()
    return GenerateDRCRPairs(__FilterAndClone(journals, Filter.IsSameSource, ji.SourceObject(), currency))

#-------------------------------------------------------------------------
def ReadPairBeforeStartDate(ji, currency, startDate):

    journals = QueriesBase.GetRelatedBeforeDateQuery(ji, startDate).Select()
    return next(GenerateDRCRPairs(__FilterAndClone(journals, Filter.IsSameSource, ji.SourceObject(), currency), revSort=True), None)

#-------------------------------------------------------------------------
def ReadPairAfterEndDate(ji, currency, endDate):

    journals = QueriesBase.GetRelatedAfterDateQuery(ji, endDate).Select()
    return next(GenerateDRCRPairs(__FilterAndClone(journals, Filter.IsSameSource, ji.SourceObject(), currency)), None)

#-------------------------------------------------------------------------
def ReadAccountingPeriod(book, fiscalYear, periodType):

    accPeriods = QueriesEOFY.GetAccountingPeriodOfTypeQuery(fiscalYear, book, periodType).Select()
    return accPeriods.First() if len(accPeriods) else None

#-------------------------------------------------------------------------
def ReadRollForwardPairs(book, fiscalYear):

    rollforwardJournals = ReadLiveRollForwardJournalsReadOnly(book, fiscalYear)
    return GenerateDRCRPairs(__Clone(rollforwardJournals))

#-------------------------------------------------------------------------
def ReadLiveRollForwardJournalsReadOnly(book, fiscalYear):
    periodsForFiscalYear = Queries.GetAccountingPeriodsForFiscalYearQuery(book, fiscalYear).Select()

    rollforwardJournals = list()

    for period in periodsForFiscalYear:
        rollforwardJournalsForPeriod = QueriesEOFY.GetLiveRollForwardJournalsForPeriodQuery(period).Select()
        rollforwardJournals.extend(rollforwardJournalsForPeriod)

    return rollforwardJournals

#-------------------------------------------------------------------------
def ReadLiveBalancesForPeriod(period):

    balances = Queries.GetLiveBalancesForPeriodQuery(period).Select()
    return __Clone(balances)

#-------------------------------------------------------------------------
def ReadLiveBalancesForPeriodReadOnly(period):

    balances = Queries.GetLiveBalancesForPeriodQuery(period).Select()
    return balances

#-------------------------------------------------------------------------
def ReadPairsForPeriodBalance(period, generationDate, keyFunc, exceptionCb):

    journals = Queries.GetJournalsForPeriodQuery(period, generationDate).Select()
    return GenerateDRCRPairs(__FilterAndClone(journals, Filter.IsVaildForBalance, keyFunc), exceptionCb=exceptionCb)

#-------------------------------------------------------------------------
def ReadPairsForPeriodRevaluationReadOnly(period, generationDate, keyFunc, exceptionCb):

    journals = Queries.GetJournalsForPeriodQuery(period, generationDate).Select()
    return GenerateDRCRPairs(__Filter(journals, Filter.IsVaildForBalance, keyFunc), exceptionCb=exceptionCb)

#-------------------------------------------------------------------------
def ReadBalancesForFiscalYearReadOnly(book, fiscalYear):

    periodsForFiscalYear = Queries.GetAccountingPeriodsForFiscalYearQuery(book, fiscalYear).Select()

    balances = list()

    for period in periodsForFiscalYear:
        balancesForPeriod = QueriesEOFY.GetBalancesForPeriodQuery(period).Select()
        balances.extend(balancesForPeriod)

    return balances

#-------------------------------------------------------------------------
def ReadJournalInfosReadOnly(journalInfos):

    persisted = dict()

    for journalInfo in journalInfos:
        persistedJournalInfos = QueriesBase.GetJournalInfosQuery(journalInfo).Select()

        for persistedJournalInfo in persistedJournalInfos:

            if Compare.IsEqualJournalInformation(journalInfo, persistedJournalInfo):

                persisted[journalInfo.Oid()] = persistedJournalInfo
                break

    return persisted

#-------------------------------------------------------------------------
# Utility functions
#-------------------------------------------------------------------------
def __FilterAndClone(journals, filterFunc, *args):

    return imap(lambda j: j.Clone(), ifilter(lambda j: filterFunc(j, *args), journals))

#-------------------------------------------------------------------------
def __Clone(journals):

    return imap(lambda j: j.Clone(), journals)

#-------------------------------------------------------------------------
def __Filter(journals, filterFunc, *args):

    return imap(lambda j: j, ifilter(lambda j: filterFunc(j, *args), journals))