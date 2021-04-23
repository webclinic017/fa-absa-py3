""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingEngineBalance.py"

# accounting
from FAccountingEngineContracts import IAccountingBalanceEngine
from FAccountingLedgerKeyParser import ComputeKeyForJournal
from FAccountingLedgerKeyMapper import TAccountLedgerKeyMapper
from FAccountingQueries import GetOpenAccountingPeriodFromDateQuery
from FAccountingCreation import CreateBalanceFromAttributes
from FAccountingOperations import Operation, GetOpForObject
from FAccountingReader import ReadPairsForPeriodBalance, ReadLiveBalancesForPeriod
from FAccountingEnums import JournalCategory

#-------------------------------------------------------------------------
# Ledger Balance Generation Engine - used by FAccountingBalances
#-------------------------------------------------------------------------
class BalanceEngine(IAccountingBalanceEngine):

    #-------------------------------------------------------------------------
    def __init__(self, configuration, transactionSize):
        super(BalanceEngine, self).__init__(configuration)

        self.__ledgerKeys = configuration.partitionKeys

        self.__updaterIF = configuration.updaterIF
        self.__updaterIF.PO_Init(self)

        self.__tAccountLedgerKeyMapper = TAccountLedgerKeyMapper(self.__ledgerKeys)

        self.__currentBalances = dict()
        self.__excludedJournals = 0

        self.__transactionSize = transactionSize

    #-------------------------------------------------------------------------
    def Clear(self):
        super(BalanceEngine, self).Clear()
        self.__updaterIF.PO_Clear()
        self.__currentBalances.clear()
        self.__excludedJournals = 0

    #-------------------------------------------------------------------------
    def Process(self, date, books):

        result = self.WR_CreateResult()

        for book in books:
            try:
                periods = GetOpenAccountingPeriodFromDateQuery(book, date).Select()

                assert len(periods) < 2, 'ERROR: Found to many open accounting periods for book {} on {}'.format(book, date)

                period = periods.First() if periods else None

                if not period:
                    self._loggerIF.LP_Log('No open accounting period for date {} and book {}'.format(date, book.Name()))

                else:
                    result.RE_Accumulate(self.__ProcessBook(book, date, period))

            except Exception as e:
                self._loggerIF.LP_Log('Exception occurred while running balance generation: {}'.format(str(e)))

            self.Clear()

        return result

    #-------------------------------------------------------------------------
    def __ProcessBook(self, book, date, period):

        self._loggerIF.LP_Log('\nProcessing book: {}\n'.format(book.Name()))

        result = self.WR_CreateResult()

        keyFunc = lambda j : ComputeKeyForJournal(j, self.__tAccountLedgerKeyMapper)

        self.__UpdateBalances(date, period, keyFunc, result)

        self.__LogResult(result)

        return result

    #-------------------------------------------------------------------------
    def __UpdateBalances(self, date, period, keyFunc, result):

        self._loggerIF.LP_LogVerbose('Selecting pairs for period... ')
        self._loggerIF.LP_Flush()

        validPairsForPeriod = [pair for pair in ReadPairsForPeriodBalance(period, date, keyFunc, self.__ExceptionCb)]

        self._loggerIF.LP_LogVerbose('{} pairs selected for balance generation.\n'.format(len(validPairsForPeriod)))

        self._loggerIF.LP_LogVerbose('Selecting current balances for period... ')
        self._loggerIF.LP_Flush()

        self.__currentBalances = dict((keyFunc(balance), balance) for balance in ReadLiveBalancesForPeriod(period))

        self._loggerIF.LP_LogVerbose('Selected {} balances for period \n'.format(len(self.__currentBalances)))

        self._loggerIF.LP_LogVerbose('Processing pairs... ')

        self._loggerIF.LP_Flush()

        processedPairs = 0

        for pair in validPairsForPeriod:
            for journal in pair.Journals():
                balanceForKey = self.__GetOrCreateBalanceForKey(keyFunc(journal), journal, journal.AccountingPeriod())

                if balanceForKey.ValueDate() < date:
                    balanceForKey.ValueDate(date)
                    balanceForKey.EventDate(date)
                else:
                    balanceForKey.EventDate(balanceForKey.ValueDate())


                journal.Balance(balanceForKey)

            self.__updaterIF.STPU_AddPair(pair)

            processedPairs += 1

            if processedPairs % 1000 == 0:
                self._loggerIF.LP_LogVerbose('Pairs processed so far: {} '.format(processedPairs))
                self._loggerIF.LP_Flush()

        self._loggerIF.LP_LogVerbose('Finished processing pairs, {} pairs processed \n'.format(processedPairs))

        self._loggerIF.LP_LogVerbose('Performing balance updates... ')

        self._loggerIF.LP_Flush()

        result.RE_Accumulate(self.__updaterIF.STPU_PerformUpdate())

        self._loggerIF.LP_LogVerbose('Balance updates finished \n')
        self._loggerIF.LP_Flush()

        self._loggerIF.LP_LogVerbose('Updating process date for balances... ')

        self._loggerIF.LP_Flush()

        addedBalances = 0

        for balance in list(self.__currentBalances.values()):
            bookProcessDate = balance.Book().ProcessDate()
            if balance.Original() and not balance.Original().IsInfant() and balance.ProcessDate() < bookProcessDate:

                balance.ProcessDate(bookProcessDate)

                self.WR_AddItem(GetOpForObject(balance), balance)

                addedBalances += 1

            if addedBalances == self.__transactionSize:
                result.RE_Accumulate(self.WR_Commit())

                self._loggerIF.LP_LogVerbose('Balances updated so far: {} '.format(addedBalances))
                self._loggerIF.LP_Flush()

                addedBalances == 0

        result.RE_Accumulate(self.WR_Commit())

        self._loggerIF.LP_LogVerbose('Updating process date for balances finished \n')
        self._loggerIF.LP_Flush()

        self.__currentBalances.clear()

    #-------------------------------------------------------------------------
    def __LogResult(self, result):
        self._loggerIF.LP_Log('{} balances created'.format(result.RE_ResultOpAndObjectType(Operation.CREATE, JournalCategory.BALANCE)))
        self._loggerIF.LP_Log('{} balances updated'.format(result.RE_ResultOpAndObjectType(Operation.UPDATE, JournalCategory.BALANCE)))
        self._loggerIF.LP_Log('{} transactions failed to commit'.format(len(result.RE_Exceptions())))
        self._loggerIF.LP_Log('{} journals were excluded.\n'.format(self.__excludedJournals))

    #-------------------------------------------------------------------------
    def __ExceptionCb(self, exception, journals, keyTup):

        errorReason = 'At least one journal in the debit/credit pair has either no ledger key, Exchange rate missing or Base amount calculation failed'

        for journal in journals:
            self._loggerIF.LP_Log('WARNING: Journal with Oid {} was excluded from balance generation because: {}'.format(journal.Oid(), errorReason))

            self.__excludedJournals += 1

        self._loggerIF.LP_Flush()

    #-------------------------------------------------------------------------
    def __GetOrCreateBalanceForKey(self, key, journal, accountingPeriod):

        currentBalance = self.__currentBalances.get(key, None)

        if not currentBalance:
            ledgerKeyAttributes = self.__tAccountLedgerKeyMapper.GetLedgerKeyAttributes(journal.Account())
            currentBalance = CreateBalanceFromAttributes(0, 0, journal, accountingPeriod, ledgerKeyAttributes).Clone()

            self.__currentBalances[key] = currentBalance

        return currentBalance