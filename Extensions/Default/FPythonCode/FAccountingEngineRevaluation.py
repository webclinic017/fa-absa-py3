""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingEngineRevaluation.py"

# accounting
from FAccountingEngineContracts import IAccountingRevaluationEngine, ILedgerKeyMapperProvider, ISplitTransactionPairUpdaterProvider
from FAccountingLedgerKeyParser import ComputeKeyForJournal
from FAccountingLedgerKeyMapper import TAccountLedgerKeyMapper
from FAccountingQueries import GetOpenAccountingPeriodFromDateQuery, GetAccountingPeriodsForFiscalYearQuery, GetJournalsForBalanceQuery
from FAccountingOperations import Operation
from FAccountingReader import ReadLiveBalancesForPeriodReadOnly, ReadPairsForPeriodRevaluationReadOnly
from FAccountingEnums import JournalCategory, AccountingPeriodType
from FAccountingCompare import IsLiveFXReval

#-------------------------------------------------------------------------
# Revaluation Journals Generation Engine - used by FAccountingRevaluation
#-------------------------------------------------------------------------
class RevaluationEngine(IAccountingRevaluationEngine, ILedgerKeyMapperProvider, ISplitTransactionPairUpdaterProvider):

    #-------------------------------------------------------------------------
    def __init__(self, configuration):
        super(RevaluationEngine, self).__init__(configuration)

        self.__ledgerKeys = configuration.partitionKeys
        self.__revaluatorIF = configuration.revaluatorIF
        self.__revaluatorIF.PO_Init(self)

        self.__updaterIF = configuration.updaterIF
        self.__updaterIF.PO_Init(self)

        self.__tAccountLedgerKeyMapper = TAccountLedgerKeyMapper(self.__ledgerKeys)

        self.__excludedJournals = 0

    #-------------------------------------------------------------------------
    def Clear(self):
        super(RevaluationEngine, self).Clear()
        self.__revaluatorIF.PO_Clear()
        self.__updaterIF.PO_Clear()
        self.__excludedJournals = 0

    #-------------------------------------------------------------------------
    def LKMP_TAccountLedgerKeyMapper(self):
        return self.__tAccountLedgerKeyMapper

    #-------------------------------------------------------------------------
    def STPUP_AddPairForUpdate(self, pair):
        self.__updaterIF.STPU_AddPair(pairs)

    #-------------------------------------------------------------------------
    def STPUP_AddConnectedPairsForUpdate(self, pairs):
        self.__updaterIF.STPU_AddConnectedPairs(pairs)

    #-------------------------------------------------------------------------
    def Process(self, startDate, endDate, books):

        result = self.WR_CreateResult()

        for book in books:
            try:
                assert startDate <= endDate, 'ERROR: Start Date after End Date'

                periods = GetOpenAccountingPeriodFromDateQuery(book, endDate).Select()

                assert len(periods) < 2, 'ERROR: Found to many open accounting periods for book {} on {}'.format(book, endDate)

                period = periods.First() if periods else None

                if not period:
                    self._loggerIF.LP_Log('No open accounting period for date {} and book {}'.format(endDate, book.Name()))

                else:
                    assert period.StartDate() <= startDate, 'ERROR: Start Date and End Date in different accounting periods'

                    result.RE_Accumulate(self.__ProcessBook(book, startDate, endDate, period))

            except Exception as e:
                self._loggerIF.LP_Log('Exception occurred while running balance generation: {}'.format(str(e)))

            self.Clear()

        return result

    #-------------------------------------------------------------------------
    def __ProcessBook(self, book, startDate, endDate, period):

        self._loggerIF.LP_Log('\nProcessing book: {}\n'.format(book.Name()))

        result = self.WR_CreateResult()

        keyFunc = lambda j : ComputeKeyForJournal(j, self.LKMP_TAccountLedgerKeyMapper())

        journalsForPossibleRevaluation = self.__ReadJournalsForPossibleRevaluation(startDate, endDate, period, book, keyFunc)

        self.__PerformRevaluation(journalsForPossibleRevaluation, startDate, endDate, book, keyFunc, result, period)

        self.__LogResult(result)

        return result

    #-------------------------------------------------------------------------
    def __ReadJournalsForPossibleRevaluation(self, startDate, endDate, startingPeriod, book, keyFunc):

        self._loggerIF.LP_LogVerbose('Selecting journals/balances for possible revaluation... ')
        self._loggerIF.LP_Flush()

        fiscalYear = startingPeriod.FiscalYear()

        readNextFiscalYear = True

        journalsForPossibleRevaluation = list()

        while readNextFiscalYear:

            periodsForFiscalYear = GetAccountingPeriodsForFiscalYearQuery(book, fiscalYear).Select()

            readNextFiscalYear = len(periodsForFiscalYear) != 0

            for period in periodsForFiscalYear:

                if period.Type() == AccountingPeriodType.START_OF_FISCAL_YEAR:
                    readNextFiscalYear = len(period.Journals()) == 0

                journalsForPossibleRevaluation.extend(self.__ReadJournalsForPossibleRevaluationPeriod(startDate, endDate, period, keyFunc))

            if readNextFiscalYear:
                self._loggerIF.LP_LogVerbose('WARNING: No start of fiscal year balances for fiscal year {} reading journals/balances for fiscal year {} instead, this might take a long time'.format(fiscalYear, fiscalYear-1))

            fiscalYear -= 1

        self._loggerIF.LP_LogVerbose('{} journals/balances selected for possible revaluation.\n'.format(len(journalsForPossibleRevaluation)))

        return journalsForPossibleRevaluation

    #-------------------------------------------------------------------------
    def __ReadJournalsForPossibleRevaluationPeriod(self, startDate, endDate, period, keyFunc):
        journalsForPossibleRevaluation = list()

        validPairs = ReadPairsForPeriodRevaluationReadOnly(period, endDate, keyFunc, self.__ExceptionCb)

        for pair in validPairs:
            journalsForPossibleRevaluation.extend(pair.Journals())

        liveBalances = ReadLiveBalancesForPeriodReadOnly(period)

        inValidBalances = list()

        for balance in liveBalances:
            if balance.ValueDate() < startDate:
                journalsForPossibleRevaluation.append(balance)

            else:
                inValidBalances.append(balance)

        for balance in inValidBalances:
            journalsForPossibleRevaluation.extend(GetJournalsForBalanceQuery(balance).Select())

        return journalsForPossibleRevaluation

    #-------------------------------------------------------------------------
    def __PerformRevaluation(self, journals, startDate, endDate, book, keyFunc, result, period):

        self._loggerIF.LP_LogVerbose('Selecting valid journals/balances for revaluation... ')

        self._loggerIF.LP_Flush()

        validJournals = 0
        validatedJournals = 0

        for journal in journals:

            if self.__revaluatorIF.RP_IsValidForReval(journal):

                if IsLiveFXReval(journal):
                    self.__revaluatorIF.RP_AddLiveRevalJournal(keyFunc(journal), journal)
                else:
                    self.__revaluatorIF.RP_AddForRevaluation(keyFunc(journal), journal)

                validJournals += 1

            validatedJournals += 1

            if validatedJournals % 1000 == 0:
                self._loggerIF.LP_LogVerbose('Journals/balances validated so far: {} '.format(validatedJournals))
                self._loggerIF.LP_Flush()

        self._loggerIF.LP_LogVerbose('{} of {} journals/balances valid for revaluation \n'.format(validJournals, validatedJournals))

        self._loggerIF.LP_LogVerbose('Creating revaluation journals... ')

        self._loggerIF.LP_Flush()

        self.__revaluatorIF.RP_Revaluate(startDate, endDate, book, keyFunc, period)

        self._loggerIF.LP_LogVerbose('Finished creating revaluation journals \n')

        self._loggerIF.LP_LogVerbose('Committing revaluation journals... ')

        self._loggerIF.LP_Flush()

        result.RE_Accumulate(self.__updaterIF.STPU_PerformUpdate())

        self._loggerIF.LP_LogVerbose('Revaluation journals committed \n')
        self._loggerIF.LP_Flush()

    #-------------------------------------------------------------------------
    def __LogResult(self, result):
        self._loggerIF.LP_Log('{} FX Revaluation journals created'.format(result.RE_ResultOpAndObjectType(Operation.CREATE, JournalCategory.FX_REVALUATION)))
        self._loggerIF.LP_Log('{} FX Revaluation journals updated'.format(result.RE_ResultOpAndObjectType(Operation.UPDATE, JournalCategory.FX_REVALUATION)))
        self._loggerIF.LP_Log('{} transactions failed to commit'.format(len(result.RE_Exceptions())))
        self._loggerIF.LP_Log('{} journals were excluded.\n'.format(self.__excludedJournals))

    #-------------------------------------------------------------------------
    def __ExceptionCb(self, exception, journals, keyTup):
        errorReason = 'At least one journal in the debit/credit pair has either no ledger key, Exchange rate missing or Base amount calculation failed'

        for journal in journals:
            self._loggerIF.LP_Log('WARNING: Journal with Oid {} was excluded from revaluation because: {}'.format(journal.Oid(), errorReason))

            self.__excludedJournals += 1

        self._loggerIF.LP_Flush()
