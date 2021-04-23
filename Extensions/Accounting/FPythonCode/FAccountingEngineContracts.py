""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingEngineContracts.py"
from abc import abstractmethod, ABCMeta
# operations
from FOperationsProvidedObject import Provided
from FOperationsEnginesBase import OperationsEngine, OperationsSimpleEngine

#-------------------------------------------------------------------------
class IAccountingEngine(OperationsEngine, metaclass=ABCMeta):
    class IAccountingObjectCreator(Provided, metaclass=ABCMeta):
        class IAccountAllocator(Provided, metaclass=ABCMeta):
            @abstractmethod
            def AA_AddItemsToTransaction(self):
                pass

            @abstractmethod
            def AA_CreateDynamicAccount(self, journal, parentAccount):
                pass

            @abstractmethod
            def AA_IsApplicableForDynamicAccount(self, journal):
                pass

        @abstractmethod
        def AOC_CreateObjects(self, obj):
            pass

        @abstractmethod
        def AOC_IsPositionCached(self, positionKey):
            pass

        @abstractmethod
        def AOC_ClearCalculations(self):
            pass

        @abstractmethod
        def AOC_ClearProcessedPositions(self):
            pass

    #-------------------------------------------------------------------------
    class IAmendmentManager(Provided, metaclass=ABCMeta):
        class ICancellationExecutor(Provided, metaclass=ABCMeta):
            class ICancellationHelper(Provided, metaclass=ABCMeta):
                @abstractmethod
                def CH_SelectCandidates(self):
                    pass

                @abstractmethod
                def CH_IsValidCancellation(self):
                    pass

                @abstractmethod
                def CH_ClearProcessedPositions(self):
                    pass

            @abstractmethod
            def CE_PrepareData(self, obj, startDate):
                pass

            @abstractmethod
            def CE_Remove(self, obj):
                pass

            @abstractmethod
            def CE_PerformCancellations(self):
                pass

            @abstractmethod
            def CE_ClearProcessedPositions(self):
                pass

        #-------------------------------------------------------------------------
        class IAmendmentSequencer(Provided, metaclass=ABCMeta):
            @abstractmethod
            def AS_ProcessSequence(self, info, currency, eventDate, journals, cancellations, trans, args):
                pass

        #-------------------------------------------------------------------------
        @abstractmethod
        def AM_Amend(self, obj, startDate, journals):
            pass

        @abstractmethod
        def AM_AmendCancelledPositions(self):
            pass

        @abstractmethod
        def AM_ClearProcessedPositions(self):
            pass

    #-------------------------------------------------------------------------
    @abstractmethod
    def AE_IsPositionCached(self, positionKey):
        pass

    #-------------------------------------------------------------------------
    @abstractmethod
    def AE_CallObjectModifier(self, obj):
        pass

#-------------------------------------------------------------------------
class ILedgerKeyMapperProvider(object, metaclass=ABCMeta):
    @abstractmethod
    def LKMP_TAccountLedgerKeyMapper(self):
        pass

#-------------------------------------------------------------------------
class ISplitTransactionPairUpdater(Provided, metaclass=ABCMeta):
    @abstractmethod
    def STPU_AddPair(self, pair):
        pass

    @abstractmethod
    def STPU_AddConnectedPairs(self, pairs):
        pass

    @abstractmethod
    def STPU_PerformUpdate(self):
        pass

#-------------------------------------------------------------------------
class ISplitTransactionPairUpdaterProvider(object, metaclass=ABCMeta):
    @abstractmethod
    def STPUP_AddPairForUpdate(self, pair):
        pass

    @abstractmethod
    def STPUP_AddConnectedPairsForUpdate(self, pairs):
        pass

#-------------------------------------------------------------------------
class IBalanceCache(object, metaclass=ABCMeta):
    @abstractmethod
    def BC_GetOrCreateBalanceForKey(self, key, journal, accountingPeriod):
        pass

#-------------------------------------------------------------------------
class IAccountingBalanceEngine(OperationsSimpleEngine):
    pass

#-------------------------------------------------------------------------
class IAccountingRevaluationEngine(OperationsSimpleEngine):

    #-------------------------------------------------------------------------
    class IRevaluationProvider(Provided, metaclass=ABCMeta):
        @abstractmethod
        def RP_IsValidForReval(self, journal):
            pass

        @abstractmethod
        def RP_Revaluate(self, keyfunc):
            pass

        @abstractmethod
        def RP_AddForRevaluation(self, key, journal):
            pass

        @abstractmethod
        def RP_AddLiveRevalJournal(self, key, fxJournal):
            pass

#-------------------------------------------------------------------------
class IAccountingEOFYEngine(OperationsSimpleEngine, metaclass=ABCMeta):
    class IRollForwardProvider(Provided):

        @abstractmethod
        def RFP_IsValidForRollForward(self, tAccount):
            pass

        @abstractmethod
        def RFP_RollForward(self, book, fiscalYear, functor, startOfYearBalances):
            pass

        @abstractmethod
        def RP_AddForRollForward(self, key, balance):
            pass

