""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingRevaluator.py"

# itertools
from itertools import groupby

# accounting
from FAccountingQueries import GetFXRevaluationsBeforeDateQuery
from FAccountingCalculations import CalculateFXRevaluationAmount, CalculateFXRevaluationAmountXPL, IsAmountZero, CalculateAmountAndBaseAmount
from FAccountingCreation import CreateFXRevaluationJournals
from FAccountingEngineContracts import IAccountingRevaluationEngine
from FAccountingDRCRPairGenerator import GenerateDRCRPairs
from FAccountingPairReverser import PerformCancellation
from FAccountingGetters import GetLinkedAccount

#-------------------------------------------------------------------------
class Revaluator(IAccountingRevaluationEngine.IRevaluationProvider):

    #-------------------------------------------------------------------------
    def __init__(self, createZeroAmountJournals):
        self.__createZeroAmountJournals = createZeroAmountJournals
        self.__toRevalueJournals = dict()
        self.__liveRevaluationJournals = dict()
        self.__templateJournals = dict()

    #-------------------------------------------------------------------------
    def PO_Init(self, provider):
        self.__provider = provider

    #-------------------------------------------------------------------------
    def PO_Clear(self):
        self.__toRevalueJournals.clear()
        self.__liveRevaluationJournals.clear()
        self.__templateJournals.clear()

    #-------------------------------------------------------------------------
    def RP_IsValidForReval(self, journal):
        return journal.ChartOfAccount().HasActiveRevaluationTAccount()

    #-------------------------------------------------------------------------
    def RP_AddForRevaluation(self, key, journal):
        self.__toRevalueJournals.setdefault(key, dict()).setdefault(journal.ValueDate(), list()).append(journal)
        self.__templateJournals[key] = journal

    #-------------------------------------------------------------------------
    def RP_AddLiveRevalJournal(self, key, journal):
        self.__liveRevaluationJournals.setdefault(key, dict()).setdefault(journal.ValueDate(), list()).append(journal)

    #-------------------------------------------------------------------------
    def RP_Revaluate(self, startDate, endDate, book, keyFunc, period):
        assert book, 'ERROR: No book given for revaluation'

        calendar = book.GetUsedCalendar()

        assert calendar, 'ERROR: book {} given for revaluation has no used calendar'.format(book.Name())

        for key, journalsForKeyDict in self.__toRevalueJournals.items():

            currentValueDate = startDate

            amountUpToDate, baseAmountUpToDate = self.__GetSumsBeforeValueDateForKey(key, startDate)
            totalUplUpToDate = 0
            splitProfitLoss = self.__SplitProfitLoss(self.__templateJournals[key])
            if splitProfitLoss:
                totalUplUpToDate = self.__TotalUplUpToDateForKey(period, book, keyFunc, currentValueDate, key, self.__templateJournals[key])


            while(currentValueDate <= endDate):
                journalsForDate = journalsForKeyDict.get(currentValueDate, list())
                amountUpToDate, baseAmountUpToDate, totalUplUpToDate = self.__RevaluateJournals(\
                    currentValueDate, key, keyFunc, journalsForDate, totalUplUpToDate, amountUpToDate, baseAmountUpToDate, splitProfitLoss)

                currentValueDate = calendar.AdjustBankingDays(currentValueDate, 1)

    #-------------------------------------------------------------------------
    def __SplitProfitLoss(self, journal):
        assert journal.Account(), 'Journal does not have an account'
        return journal.Account().RevaluationTAccount2()

    #-------------------------------------------------------------------------
    def __TotalUplUpToDateForKey(self, period, book, keyFunc, currentValueDate, key, journal):
        # To be able to find FXUpl journals in our standard accounts, we first have to fetch the journals in the FXUpl account
        # and then ask for the linked pair journal. For the moment you are unable to read FXUpl journals direct from
        # the standard account, as there is no way to differentiate between FXUpl and FXRpl journals
        fxUplSums = dict()
        name = journal.Account().RevaluationTAccount2().Name() if journal.Account().RevaluationTAccount2() else None
        if name:
            # Get Journals of type FX Revaluation from the FX Reval account
            query = GetFXRevaluationsBeforeDateQuery(period, book, name, currentValueDate)
            # Get the FX Reval Journal for the Standard accounts
            linkedJournals = [j.LinkedJournals()[0] for j in query.Select()]
            for linkedJournal in linkedJournals:
                currentkey = keyFunc(linkedJournal)
                if currentkey == key:
                    fxUplSums[key] = fxUplSums.get(key, 0) + linkedJournal.BaseAmount()

        return fxUplSums.get(key, 0)

    #-------------------------------------------------------------------------
    def __GetSumsBeforeValueDateForKey(self, key, date):
        journalsValueDateDict = self.__toRevalueJournals.get(key, dict())

        journalsAmount, journalsBaseAmount = self.__GetSumsBeforeValueDate(journalsValueDateDict, date)

        revalValueDateDict = self.__liveRevaluationJournals.get(key, dict())

        revalsAmount, revalsBaseAmount = self.__GetSumsBeforeValueDate(revalValueDateDict, date)

        return journalsAmount + revalsAmount, journalsBaseAmount + revalsBaseAmount

    #-------------------------------------------------------------------------
    def __GetSumsBeforeValueDate(self, journalsValueDateDict, valueDate):
        amountSum = 0
        baseAmountSum = 0

        for currentValueDate, journalsForValueDate in journalsValueDateDict.items():
            if currentValueDate < valueDate:
                amount, baseAmount = CalculateAmountAndBaseAmount(journalsForValueDate)

                amountSum += amount
                baseAmountSum += baseAmount

        return amountSum, baseAmountSum

    #-------------------------------------------------------------------------
    def __RevaluateJournals(self, date, key, keyFunc, journals, totalUPL, previousAmount, previousBaseAmount, splitProfitLoss):
        oldLiveRevalJournals = self.__liveRevaluationJournals.get(key, dict()).get(date, list())
        assert len(oldLiveRevalJournals) <= 2, 'ERROR: Found more than two live FX revaluation journal for ledger key {} and value date {}'.format(key, date)
        amount, baseAmount = CalculateAmountAndBaseAmount(journals)

        amount += previousAmount
        baseAmount += previousBaseAmount
        templateJournal = self.__templateJournals[key]

        if splitProfitLoss:
            uplRevalAmount, rplRevalAmount = CalculateFXRevaluationAmountXPL(date, templateJournal, journals, amount, baseAmount, totalUPL)
            baseAmount += rplRevalAmount + uplRevalAmount
            totalUPL += uplRevalAmount

            #RPL
            rplAccount = templateJournal.ChartOfAccount().RevaluationTAccount()
            oldRplRevalJournal = self.__OldRevalJournal(rplAccount, oldLiveRevalJournals, key, date, 'RPL')
            self.__ReverseAndCreateNewRevals(oldRplRevalJournal, rplRevalAmount, date, key, keyFunc, templateJournal.ChartOfAccount().RevaluationChartOfAccount())

            #UPL
            uplAccount = templateJournal.ChartOfAccount().RevaluationTAccount2()
            oldUplRevalJournal = self.__OldRevalJournal(uplAccount, oldLiveRevalJournals, key, date, 'UPL')
            self.__ReverseAndCreateNewRevals(oldUplRevalJournal, uplRevalAmount, date, key, keyFunc, templateJournal.ChartOfAccount().RevaluationChartOfAccount2())

        else:
            assert len(oldLiveRevalJournals) <= 1, 'ERROR: Found more than one live FX revaluation journal for ledger key {} and value date {}'.format(key, date)
            revalAmount = CalculateFXRevaluationAmount(amount, baseAmount, templateJournal, date)
            baseAmount += revalAmount
            oldRevalJournal = oldLiveRevalJournals[0] if oldLiveRevalJournals else None
            self.__ReverseAndCreateNewRevals(oldRevalJournal, revalAmount, date, key, keyFunc, templateJournal.ChartOfAccount().RevaluationChartOfAccount())

        return amount, baseAmount, totalUPL

    #-------------------------------------------------------------------------
    def __OldRevalJournal(self, account, oldLiveRevalJournals, key, date, plType):
        revalJournals = [journal for journal in oldLiveRevalJournals if GetLinkedAccount(journal) == account]
        assert len(revalJournals) <= 1, 'ERROR: Found more than one live {} FX revaluation journal for ledger key {} and value date {}'.format(plType, key, date)
        return revalJournals[0] if revalJournals else None

    #-------------------------------------------------------------------------
    def __ReverseAndCreateNewRevals(self, oldRevalJournal, revalAmount, date, key, keyFunc, revalAccount):
        oldRevalAmount = oldRevalJournal.BaseAmount() if oldRevalJournal else 0

        oldAndNewEqual = IsAmountZero(revalAmount - oldRevalAmount)

        pairs = list()

        if not oldAndNewEqual and oldRevalJournal:
            pairs.extend(self.__ReverseOldRevaluationJournals(oldRevalJournal, date, key))

        if self.__ShouldCreateNewRevaluationJournals(oldAndNewEqual, revalAmount, oldRevalJournal):
            pairs.append(self.__CreateNewRevaluationJournals(date, key, keyFunc, revalAmount, revalAccount))

        if pairs:
            self.__provider.STPUP_AddConnectedPairsForUpdate(pairs)

    #-------------------------------------------------------------------------
    def __CreateNewRevaluationJournals(self, date, key, keyFunc, revalAmount, revalAccount):
        accountMapper = self.__provider.LKMP_TAccountLedgerKeyMapper()
        revaluationPair = next(GenerateDRCRPairs(CreateFXRevaluationJournals(self.__templateJournals[key], revalAmount, date, accountMapper, revalAccount), True))
        for journal in revaluationPair.Journals():
            self.__liveRevaluationJournals.setdefault(keyFunc(journal), dict()).setdefault(date, list()).append(journal)

        return revaluationPair

    #-------------------------------------------------------------------------
    def __ReverseOldRevaluationJournals(self, revalJournal, date, key):
        pairs = list()

        oldRevalPair = next(GenerateDRCRPairs([journal.Clone() for journal in revalJournal.JournalLink().Journals()]))

        self.__liveRevaluationJournals[key][date].remove(revalJournal)
        processDate = revalJournal.Book().ProcessDate()
        for pair in PerformCancellation(oldRevalPair, date, processDate):
            pairs.append(pair)

        return pairs

    #-------------------------------------------------------------------------
    def __ShouldCreateNewRevaluationJournals(self, oldAndNewEqual, newRevalAmount, oldRevalJournal):
        shouldCreateBasedOnAmount = (newRevalAmount or self.__createZeroAmountJournals)

        return (not oldAndNewEqual and shouldCreateBasedOnAmount) or (oldAndNewEqual and not oldRevalJournal and shouldCreateBasedOnAmount)
