""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingAmendmentManager.py"
# itertools
from itertools import groupby

# accounting
from FAccountingEngineContracts import IAccountingEngine
from FAccountingAmendmentSequencer import AmendmentSequencer
from FAccountingCalculations import IsJournalAmountZero, IsJournalBaseAmountZero
from FAccountingOperations import Operation
from FAccountingOperations import GetOpForObject

import FAccountingCancellationExecutor as Cancellations

#-------------------------------------------------------------------------
class AmendmentManager(IAccountingEngine.IAmendmentManager):

    posAggLevels = ['Contract Trade Number', 'Contract Trdnbr and Moneyflow', 'Instrument and Portfolio']

    #-------------------------------------------------------------------------
    def __init__(self, liveDataForObjCb, liveDataForPositionCb):
        self.__provider = None

        self.__objCancellations = Cancellations.CreateCancellationExecutorForSingles(liveDataForObjCb)
        self.__posCancellations = Cancellations.CreateCancellationExecutorForPositions(liveDataForPositionCb)

        self.__amendmentSequencer = AmendmentSequencer(self.__IsValidJournalFilter, self.__IsValidJournal)

    #-------------------------------------------------------------------------
    def PO_Init(self, provider):
        self.__provider = provider

        self.__objCancellations.PO_Init(provider)
        self.__posCancellations.PO_Init(provider)

        self.__amendmentSequencer.PO_Init(provider)

    #-------------------------------------------------------------------------
    def PO_Clear(self):
        self.__objCancellations.PO_Clear()

    #-------------------------------------------------------------------------
    def AM_Amend(self, obj, customStartDate, newJournals):

        startDate = customStartDate if customStartDate else startDate

        transactionDict = dict()

        self.__objCancellations.CE_PrepareData(obj, startDate)
        self.__posCancellations.CE_PrepareData(obj, startDate)

        for info, currency, eventDate, journals in self.__GenerateCollection(newJournals):

            args = {
                'ai' : info.AccountingInstruction(),
                'book' : info.Book(),
                'startDate' : startDate}

            cancellations = self.__GetCancellationExcutor(info.AccountingInstruction())

            self.__amendmentSequencer.AS_ProcessSequence(info, currency, eventDate, journals, cancellations, transactionDict, args)

        self.__objCancellations.CE_PerformCancellations()

        for obj in list(transactionDict.values()):
            self.__provider.WR_AddItem(GetOpForObject(obj), obj)

    #-------------------------------------------------------------------------
    def AM_AmendCancelledPositions(self):
        self.__posCancellations.CE_PerformCancellations()
        self.__posCancellations.PO_Clear()

    #-------------------------------------------------------------------------
    def AM_ClearProcessedPositions(self):
        self.__posCancellations.CE_ClearProcessedPositions()

    #-------------------------------------------------------------------------
    def __GenerateCollection(self, journals):
        for key, group in groupby(sorted(journals, key=self.__Sort), key=self.__Sort):

            info, currency, eventDate = key

            yield info, currency, eventDate, group

    #-------------------------------------------------------------------------
    def __Sort(self, journal):
        eventDate = journal.EventDate() if journal.AccountingInstruction().IsNonPeriodic() else None

        return (journal.JournalInformation(), journal.Currency(), eventDate)

    #-------------------------------------------------------------------------
    def __GetCancellationExcutor(self, ai):
        return self.__posCancellations if ai.AggregationLevel() in AmendmentManager.posAggLevels else self.__objCancellations

    #-------------------------------------------------------------------------
    def __IsValidJournalFilter(self, journal):
        return not journal.PreventLiveJournal() and \
            self.__provider.VA_IsValidObject(Operation.CREATE, journal)

    #-------------------------------------------------------------------------
    def __IsValidJournal(self, journal):
        return self.__provider.Param('createZeroAmountJournals') or not IsJournalAmountZero(journal) or \
               not IsJournalBaseAmountZero(journal) or journal.IsBaseAmountCalculationFailed()
