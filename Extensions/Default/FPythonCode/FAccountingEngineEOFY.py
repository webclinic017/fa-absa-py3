""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingEngineEOFY.py"

# accounting
from FAccountingEngineContracts import IAccountingEOFYEngine, ILedgerKeyMapperProvider, ISplitTransactionPairUpdaterProvider, IBalanceCache
from FAccountingBalanceGenerator import GenerateBalance
from FAccountingCreation import CreateBalanceFromAttributes, CreateAccountingPeriod
from FAccountingLedgerKeyParser import ComputeKeyForJournal

from FAccountingReader import ReadAccountingPeriod, ReadBalancesForFiscalYearReadOnly, \
                              ReadLiveRollForwardJournalsReadOnly, ReadLiveBalancesForPeriod

from FAccountingLedgerKeyMapper import TAccountLedgerKeyMapper
from FAccountingOperations import Operation, GetOpForObject
from FAccountingCompare import IsAmountEqual, IsBaseAmountEqual
from FAccountingEnums import AccountingPeriodType, JournalCategory

#-------------------------------------------------------------------------
class EOFYEngine(IAccountingEOFYEngine, ILedgerKeyMapperProvider, ISplitTransactionPairUpdaterProvider, IBalanceCache):

    #-------------------------------------------------------------------------
    def __init__(self, configuration):
        super(EOFYEngine, self).__init__(configuration)

        self.__ledgerKeys = configuration.partitionKeys
        self.__tAccountLedgerKeyMapper = TAccountLedgerKeyMapper(self.__ledgerKeys)

        self.__rollForward = configuration.rollForwardIF
        self.__rollForward.PO_Init(self)

        self.__updaterIF = configuration.updaterIF
        self.__updaterIF.PO_Init(self)

        self.__currentBalances = dict()

    #-------------------------------------------------------------------------
    def Clear(self):
        super(EOFYEngine, self).Clear()
        self._loggerIF.LP_Flush()
        self.__rollForward.PO_Clear()
        self.__updaterIF.PO_Clear()
        self.__currentBalances.clear()

    #-------------------------------------------------------------------------
    def LKMP_TAccountLedgerKeyMapper(self):
        return self.__tAccountLedgerKeyMapper

    #-------------------------------------------------------------------------
    def Process(self, fiscalYear, books):
        totalResult = self._writerIF.WR_CreateResult()
        self._loggerIF.LP_Log('\nStarting EOFY for fiscal year: {}\n'.format(fiscalYear))

        for book in books:
            try:
                result = self.__ProcessBook(book, fiscalYear)
                totalResult.RE_Accumulate(result)
            except Exception as e:
                self._loggerIF.LP_Log('Exception occurred while running EOFY script: {}'.format(str(e)))

            self.Clear()

        return totalResult

    #-------------------------------------------------------------------------
    def STPUP_AddPairForUpdate(self, pair):
        self.__updaterIF.STPU_AddPair(pair)

    #-------------------------------------------------------------------------
    def STPUP_AddConnectedPairsForUpdate(self, pairs):
        self.__updaterIF.STPU_AddConnectedPairs(pairs)

    #-------------------------------------------------------------------------
    def BC_GetOrCreateBalanceForKey(self, key, journal, accountingPeriod):

        currentBalance = self.__currentBalances.get(key, None)

        if not currentBalance:
            ledgerKeyAttributes = self.__tAccountLedgerKeyMapper.GetLedgerKeyAttributes(journal.Account())
            currentBalance = CreateBalanceFromAttributes(0, 0, journal, accountingPeriod, ledgerKeyAttributes).Clone()

            self.__currentBalances[key] = currentBalance

        return currentBalance

    #-------------------------------------------------------------------------
    def __ProcessBook(self, book, fiscalYear):
        self._loggerIF.LP_Log('\nProcessing book: {}\n'.format(book.Name()))
        self._loggerIF.LP_Flush()

        result = self._writerIF.WR_CreateResult()

        self.__CreateStartOfYearBalances(book, fiscalYear, result)

        self.__PerformRollForward(book, fiscalYear, result)

        self.__LogResult(result)

        return result

    #-------------------------------------------------------------------------
    def __CreateStartOfYearBalances(self, book, fiscalYear, result):

        beginningPeriod = self.__GetOrCreatePeriod(book, fiscalYear + 1, AccountingPeriodType.START_OF_FISCAL_YEAR, result)

        keyFunc = lambda j: ComputeKeyForJournal(j, self.LKMP_TAccountLedgerKeyMapper())

        self._loggerIF.LP_LogVerbose('Selecting balances for fiscal year... ')
        self._loggerIF.LP_Flush()

        selectedBalancesForFiscalYear = [balance for balance in ReadBalancesForFiscalYearReadOnly(book, fiscalYear)]

        self._loggerIF.LP_LogVerbose('Selected {} balances for fiscal year \n'.format(len(selectedBalancesForFiscalYear)))

        self._loggerIF.LP_LogVerbose('Selecting rollforward journals for fiscal year... ')

        self._loggerIF.LP_Flush()

        selectedRollforwardJournalsForFiscalYear = [journal for journal in ReadLiveRollForwardJournalsReadOnly(book, fiscalYear)]

        self._loggerIF.LP_LogVerbose('Selected {} rollforward journals for fiscal year \n'.format(len(selectedBalancesForFiscalYear)))

        self._loggerIF.LP_LogVerbose('Sorting journals to create balances from... ')
        self._loggerIF.LP_Flush()

        selectedJournalsForFiscalYear = list()
        selectedJournalsForFiscalYear.extend(selectedBalancesForFiscalYear)
        selectedJournalsForFiscalYear.extend(selectedRollforwardJournalsForFiscalYear)

        journalsForFiscalYear = sorted(selectedJournalsForFiscalYear, key=keyFunc)

        self._loggerIF.LP_LogVerbose('Finished sorting journals \n')

        self._loggerIF.LP_LogVerbose('Selecting period zero balances... ')

        self._loggerIF.LP_Flush()

        self.__currentBalances = dict((keyFunc(balance), balance) for balance in ReadLiveBalancesForPeriod(beginningPeriod))

        self._loggerIF.LP_LogVerbose('Selected {} period zero balances \n'.format(len(self.__currentBalances)))

        self._loggerIF.LP_LogVerbose('Creating/updating period zero balances... ')

        self._loggerIF.LP_Flush()

        createdUpdatedBalances = 0
        amountUpdated = False

        for key, balances, amount, baseAmount in GenerateBalance(journalsForFiscalYear, keyFunc):

            beginningBalance = self.BC_GetOrCreateBalanceForKey(key, balances[0], beginningPeriod)

            beginningBalance.Amount(amount)
            beginningBalance.BaseAmount(baseAmount)

            if not IsAmountEqual(beginningBalance, beginningBalance.Original()) or \
               not IsBaseAmountEqual(beginningBalance, beginningBalance.Original()):

                self.__AddBalanceToTransaction(beginningBalance)

                createdUpdatedBalances += 1
                amountUpdated = True

            if createdUpdatedBalances % 1000 == 0 and amountUpdated:

                result.RE_Accumulate(self._writerIF.WR_Commit())

                self._loggerIF.LP_LogVerbose('Balances created/updated so far: {} '.format(createdUpdatedBalances))
                self._loggerIF.LP_Flush()

                amountUpdated = False

        result.RE_Accumulate(self._writerIF.WR_Commit())

        self._loggerIF.LP_LogVerbose('Finished creating/updating period zero balances, {} balances created/updated \n'.format(createdUpdatedBalances))
        self._loggerIF.LP_Flush()

        self.__currentBalances.clear()

    #-------------------------------------------------------------------------
    def __PerformRollForward(self, book, fiscalYear, result):

        beginningPeriod = self.__GetOrCreatePeriod(book, fiscalYear + 1, AccountingPeriodType.START_OF_FISCAL_YEAR, result)

        keyFunc = lambda j: ComputeKeyForJournal(j, self.LKMP_TAccountLedgerKeyMapper())

        self._loggerIF.LP_LogVerbose('Selecting period zero balances for possible rollforward... ')
        self._loggerIF.LP_Flush()

        self.__currentBalances = dict((keyFunc(balance), balance) for balance in ReadLiveBalancesForPeriod(beginningPeriod))

        self._loggerIF.LP_LogVerbose('Selected {} period zero balances \n'.format(len(self.__currentBalances)))

        self._loggerIF.LP_LogVerbose('Selecting valid balances for rollforward... ')

        self._loggerIF.LP_Flush()

        validBalances = 0
        validatedBalances = 0

        for key, balance in self.__currentBalances.items():

            if self.__rollForward.RFP_IsValidForRollForward(balance):

                self.__rollForward.RFP_AddForRollForward(key, balance)

                validBalances += 1

            validatedBalances += 1

            if validatedBalances % 1000 == 0:
                self._loggerIF.LP_LogVerbose('Balances validated so far: {} '.format(validatedBalances))
                self._loggerIF.LP_Flush()

        self._loggerIF.LP_LogVerbose('{} of {} balances valid for rollforward \n'.format(validBalances, validatedBalances))
        self._loggerIF.LP_Flush()

        endPeriod = self.__GetOrCreatePeriod(book, fiscalYear, AccountingPeriodType.END_OF_FISCAL_YEAR, result)

        self._loggerIF.LP_LogVerbose('Creating rollforward journals... ')

        self._loggerIF.LP_Flush()

        self.__rollForward.RFP_RollForward(book, fiscalYear, endPeriod, keyFunc)

        self._loggerIF.LP_LogVerbose('Finished creating rollforward journals \n')

        self._loggerIF.LP_LogVerbose('Performing balance updates... ')

        self._loggerIF.LP_Flush()

        result.RE_Accumulate(self.__updaterIF.STPU_PerformUpdate())

        self._loggerIF.LP_LogVerbose('Balance updates finished \n')
        self._loggerIF.LP_Flush()

        self.__currentBalances.clear()

    #-------------------------------------------------------------------------
    def __AddBalanceToTransaction(self, balance):
        balanceToAdd = balance

        if balance.Original().IsInfant():

            original = balance.Original()
            original.Apply(balance)

            balanceToAdd = original

        self._writerIF.WR_AddItem(GetOpForObject(balanceToAdd), balanceToAdd)
        self._writerIF.WR_AddItem(GetOpForObject(balanceToAdd.JournalInformation()), balanceToAdd.JournalInformation())

    #-------------------------------------------------------------------------
    def __GetOrCreatePeriod(self, book, fiscalYear, apType, result):
        beginningPeriod = ReadAccountingPeriod(book, fiscalYear, apType)

        if not beginningPeriod:
            beginningPeriod = CreateAccountingPeriod(fiscalYear, book, apType)
            self._writerIF.WR_AddItem(GetOpForObject(beginningPeriod), beginningPeriod)
            result.RE_Accumulate(self._writerIF.WR_Commit())

        return beginningPeriod

    #-------------------------------------------------------------------------
    def __LogResult(self, result):
        self._loggerIF.LP_Log('{} balances created'.format(result.RE_ResultOpAndObjectType(Operation.CREATE, JournalCategory.BALANCE)))
        self._loggerIF.LP_Log('{} balances updated'.format(result.RE_ResultOpAndObjectType(Operation.UPDATE, JournalCategory.BALANCE)))
        self._loggerIF.LP_Log('{} End of Fiscal Year journals created'.format(result.RE_ResultOpAndObjectType(Operation.CREATE, JournalCategory.END_OF_FISCAL_YEAR)))
        self._loggerIF.LP_Log('{} End of Fiscal Year journals updated'.format(result.RE_ResultOpAndObjectType(Operation.UPDATE, JournalCategory.END_OF_FISCAL_YEAR)))
        self._loggerIF.LP_Log('{} transactions failed to commit.\n'.format(len(result.RE_Exceptions())))

