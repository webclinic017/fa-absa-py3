""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingSplitTransactionPairUpdater.py"
# accounting
from FAccountingEngineContracts import ISplitTransactionPairUpdater
from FAccountingOperations import GetOpForObject

#-------------------------------------------------------------------------
class SplitTransactionPairUpdater(ISplitTransactionPairUpdater):

    #-------------------------------------------------------------------------
    def __init__(self, transactionSize):
        self.__transactionList = list()
        self.__transactionSize = transactionSize
        self.__provider = None

    #-------------------------------------------------------------------------
    def PO_Init(self, provider):
        self.__provider = provider

    #-------------------------------------------------------------------------
    def PO_Clear(self):
        del self.__transactionList[:]

    #-------------------------------------------------------------------------
    def STPU_AddConnectedPairs(self, pairs):
        self.__transactionList.append(pairs)

    #-------------------------------------------------------------------------
    def STPU_AddPair(self, pair):
        self.__transactionList.append([pair])

    #-------------------------------------------------------------------------
    def STPU_PerformUpdate(self):
        result = self.__provider.WR_CreateResult()

        updatedBalancesSet = set()

        for idx, pairs in enumerate(self.__transactionList):

            for pair in pairs:

                self.__AddPairAndUpdateBalances(pair, updatedBalancesSet)

            if (idx + 1) % self.__transactionSize == 0:

                partialResult = self.__provider.WR_Commit()

                if len(partialResult.RE_Exceptions()):
                    self.__ResetBalances(updatedBalancesSet)

                result.RE_Accumulate(partialResult)

                updatedBalancesSet.clear()

        result.RE_Accumulate(self.__provider.WR_Commit())

        self.PO_Clear()

        return result

    #-------------------------------------------------------------------------
    def __AddPairAndUpdateBalances(self, pair, updatedBalancesSet):
        for journal in pair.Journals():

            if not self.__IncludedInBalance(journal) and journal.Balance():

                self.__UpdateAndAddBalance(journal, updatedBalancesSet)

            self.__provider.WR_AddItem(GetOpForObject(journal), journal)

        self.__provider.WR_AddItem(GetOpForObject(pair.JournalLink()), pair.JournalLink())
        self.__provider.WR_AddItem(GetOpForObject(pair.JournalInformation()), pair.JournalInformation())

    #-------------------------------------------------------------------------
    def __UpdateAndAddBalance(self, journal, updatedBalancesSet):
        balance = journal.Balance()

        balance.Amount(balance.Amount() + journal.Amount())
        balance.BaseAmount(balance.BaseAmount() + journal.BaseAmount())

        balanceToAdd = balance

        if balance.Original().IsInfant():
            original = balance.Original()
            original.Apply(balance)

            balanceToAdd = original

        self.__provider.WR_AddItem(GetOpForObject(balanceToAdd), balanceToAdd)
        self.__provider.WR_AddItem(GetOpForObject(balanceToAdd.JournalInformation()), balanceToAdd.JournalInformation())

        updatedBalancesSet.add(balance)

        journal.Balance(balance.OriginalOrSelf())

    #-------------------------------------------------------------------------
    def __ResetBalances(self, updatedBalancesSet):
        for balance in updatedBalancesSet:

            if balance.Original().IsInfant():
                balance.Original().Amount(0)
                balance.Original().BaseAmount(0)

            balance.Amount(balance.Original().Amount())
            balance.BaseAmount(balance.Original().BaseAmount())

    #-------------------------------------------------------------------------
    def __IncludedInBalance(self, journal):
        return journal.IsClone() and journal.Original().Balance()
