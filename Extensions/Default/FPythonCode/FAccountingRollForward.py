""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingRollForward.py"


# operations
from FOperationsCollectionUtils import PopObject

# accounting
from FAccountingEngineEOFY import IAccountingEOFYEngine
from FAccountingCreation import CreateRollForwardJournals
from FAccountingPairReverser import PerformCancellation
from FAccountingReader import ReadRollForwardPairs
from FAccountingDRCRPairGenerator import GenerateDRCRPairs
from FAccountingCalculations import IsAmountZero

#-------------------------------------------------------------------------
class BalanceRollForward(IAccountingEOFYEngine.IRollForwardProvider):

    #-------------------------------------------------------------------------
    def __init__(self, fiscalYear):

        self.__provider = None
        self.__toRollForwardBalances = dict()

    #-------------------------------------------------------------------------
    def PO_Init(self, provider):

        self.__provider = provider

    #-------------------------------------------------------------------------
    def PO_Clear(self):

        self.__toRollForwardBalances.clear()

    #-------------------------------------------------------------------------
    def RFP_IsValidForRollForward(self, balance):

        return balance.ChartOfAccount().HasActiveRollForwardTAccount() and \
               (not IsAmountZero(balance.Amount()) or not IsAmountZero(balance.BaseAmount()))

    #-------------------------------------------------------------------------
    def RFP_AddForRollForward(self, key, balance):

        self.__toRollForwardBalances[key] = balance

    #-------------------------------------------------------------------------
    def RFP_RollForward(self, book, fiscalYear, endPeriod, keyFunc):

        accountMapper = self.__provider.LKMP_TAccountLedgerKeyMapper()

        oldPairs = dict((self.__FindKey(pair, keyFunc), pair) for pair in ReadRollForwardPairs(book, fiscalYear))


        for key, balance in self.__toRollForwardBalances.items():

            oldPair = PopObject(oldPairs, key)

            rollforwardAmount, rollforwardBaseAmount = self.__CalculateRollForwardAmount(balance, oldPair)

            newPair = next(GenerateDRCRPairs(CreateRollForwardJournals(rollforwardAmount, rollforwardBaseAmount, balance, endPeriod, accountMapper), True))

            self.__ProcessPairs(oldPair, newPair, keyFunc, balance.AccountingPeriod())

    #-------------------------------------------------------------------------
    def __FindKey(self, pair, keyFunc):

        for journal in pair.Journals():

            if journal.Account().RollForwardTAccount():
                return keyFunc(journal)

        return None

    #-------------------------------------------------------------------------
    def __CalculateRollForwardAmount(self, balance, oldPair):

        rollforwardAmount = balance.Amount()
        rollforwardBaseAmount = balance.BaseAmount()

        if oldPair:
            for journal in oldPair.Journals():
                if journal.Balance() == balance.Original():
                    rollforwardAmount -= journal.Amount()
                    rollforwardBaseAmount -= journal.BaseAmount()

        return rollforwardAmount, rollforwardBaseAmount

    #-------------------------------------------------------------------------
    def __ProcessPairs(self, oldPair, newPair, keyFunc, startPeriod):

        if newPair and oldPair:

            connectedPairs = [pair for pair in PerformCancellation(oldPair, None, None)]
            connectedPairs.append(newPair)

            for pair in connectedPairs:
                self.__SetBalanceRef(pair, keyFunc, startPeriod)

            self.__provider.STPUP_AddConnectedPairsForUpdate(connectedPairs)

        elif newPair:

            self.__SetBalanceRef(newPair, keyFunc, startPeriod)

            self.__provider.STPUP_AddPairForUpdate(newPair)

    #-------------------------------------------------------------------------
    def __SetBalanceRef(self, pair, keyFunc, startPeriod):

        for journal in pair.Journals():

            key = keyFunc(journal)

            balanceForKey = self.__provider.BC_GetOrCreateBalanceForKey(key, journal, startPeriod)

            journal.Balance(balanceForKey)
