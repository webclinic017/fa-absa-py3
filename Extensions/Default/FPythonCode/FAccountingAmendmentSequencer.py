""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingAmendmentSequencer.py"

# accounting
from FAccountingEngineContracts import IAccountingEngine
from FAccountingDates import GetStartDate, GetEndDate
from FAccountingPairReverser import PerformCancellation, PerformReversal
from FAccountingJournalPairGenerator import GeneratePairs
from FAccountingDRCRPairGenerator import GenerateDRCRPairs
from FAccountingCalculations import IncrementalBaseAmountUpdate
from FAccountingCompare import IsReversal
from FAccountingSetters import IncrementalBaseAmountFailedUpdate

import FAccountingAmendmentEvaluator as Evaluator
import FAccountingReader as Reader

#-------------------------------------------------------------------------
class AmendmentSequencer(IAccountingEngine.IAmendmentManager.IAmendmentSequencer):

    #-------------------------------------------------------------------------
    def __init__(self, dataValidationCb, processValidationCb):
        self.__provider = None

        self.__dataValidationCb = dataValidationCb
        self.__processValidationCb = processValidationCb

    #-------------------------------------------------------------------------
    def PO_Init(self, provider):
        self.__provider = provider

    #-------------------------------------------------------------------------
    def PO_Clear(self):
        pass

    #-------------------------------------------------------------------------
    def AS_ProcessSequence(self, info, currency, eventDate, journals, cancellations, trans, args):
        first, pairs, last = self.__GenerateData(info, currency, eventDate, journals, args)

        self.__ProcessSequence(first, pairs, last, cancellations, trans, args)

    #-------------------------------------------------------------------------
    # Read data to process in ProcessSequence
    #-------------------------------------------------------------------------
    def __GenerateData(self, info, currency, eventDate, journals, args):

        compareStartDate = eventDate if eventDate else args['startDate']
        compareEndDate = eventDate if eventDate else self.__provider.Param('endDate')

        aiStartDate = GetStartDate(info, compareStartDate, args['startDate'], self.__provider.Param('endDate'), self.__provider.Param('endOfDayDate'))
        aiEndDate = GetEndDate(info, compareEndDate, args['startDate'], self.__provider.Param('endDate'), self.__provider.Param('endOfDayDate'))

        firstPair = Reader.ReadPairBeforeStartDate(info, currency, aiStartDate) if not args['ai'].IsNonPeriodic() else None
        lastPair = Reader.ReadPairAfterEndDate(info, currency, aiEndDate) if not args['ai'].IsNonPeriodic() else None

        newPairs = GenerateDRCRPairs(journals, True, False, self.__dataValidationCb)
        oldPairs = Reader.ReadPairs(info, currency, aiStartDate, aiEndDate)

        return firstPair, GeneratePairs(newPairs, oldPairs), lastPair

    #-------------------------------------------------------------------------
    # Process a chronological sequence of pairs of related journals from the
    # earliest to the latest, paired with their persisted counterpart if such exist
    #-------------------------------------------------------------------------
    def __ProcessSequence(self, first, pairs, last, cancellations, trans, args):
        prev = first

        for new, old in pairs:

            self.__PerformPrevious(new, old, prev, trans, args)

            self.__PerformIncrementalBaseAmount(new, prev, args)

            if new and old:
                new.RemoveInvalidJournals(self.__processValidationCb)
                new.GenerateSuspenseJournals()

                prev = self.__PerformAmendment(new, old, prev, trans, args)
                cancellations.CE_Remove(old)

            elif new:
                new.RemoveInvalidJournals(self.__processValidationCb)
                new.GenerateSuspenseJournals()

                prev = self.__PerformCreateNew(new, old, prev, trans, args)

            elif old:
                self.__PerformRemoveOld(new, old, prev, trans, args)
                cancellations.CE_Remove(old)

        if last and prev:
            self.__PerformPrevious(last, None, prev, trans, args)

        return trans

    #-------------------------------------------------------------------------
    def __PerformAmendment(self, new, old, prev, trans, args):
        if Evaluator.SkipAmendment(new, old, prev, args):
            self.__PerformPairCancellation(old, old.EventDate(), trans, args)

            return prev

        elif Evaluator.IsAmendment(new, old, prev, self.__provider.Param('processDate')):
            self.__PerformPairCancellation(old, old.EventDate(), trans, args)
            self.__AddPairToTransaction(new, trans)

            return new

        return old

    #-------------------------------------------------------------------------
    def __PerformCreateNew(self, new, old, prev, trans, args):
        if Evaluator.IsCreateNew(new, old, prev, args):
            self.__AddPairToTransaction(new, trans)

            return new

        return prev

    #-------------------------------------------------------------------------
    def __PerformRemoveOld(self, new, old, prev, trans, args):
        if Evaluator.IsRemoveOld(new, old, prev, args):
            self.__PerformPairCancellation(old, old.EventDate(), trans, args)

    #-------------------------------------------------------------------------
    def __PerformPrevious(self, new, old, prev, trans, args):
        if not args['ai'].IsNonPeriodic() and Evaluator.IsProcessPrevious(new, old, prev, args):
            self.__PerformPairReversal(prev, new.EventDate(), trans, args)

    #-------------------------------------------------------------------------
    def __PerformPairCancellation(self, pair, eventDate, trans, args):
        for amendPair in PerformCancellation(pair, eventDate, self.__provider.Param('processDate')):
            self.__AddPairToTransaction(amendPair, trans)

    #-------------------------------------------------------------------------
    def __PerformPairReversal(self, pair, eventDate, trans, args):
        for amendPair in PerformReversal(pair, eventDate, self.__provider.Param('processDate')):
            self.__AddPairToTransaction(amendPair, trans)

    #-------------------------------------------------------------------------
    def __PerformIncrementalBaseAmount(self, new, prev, args):
        if Evaluator.IsIncrementalBaseAmount(new, prev, args):
            try:
                new.PerformWithPairs(prev, IncrementalBaseAmountUpdate)

            except AssertionError as error:
                new.PerformWith(IncrementalBaseAmountFailedUpdate)
                self.__provider.LP_Log("Alternative FX Conversion failed: {}".format(str(error)))

    #-------------------------------------------------------------------------
    def __AddPairToTransaction(self, pair, trans):
        for journal in pair.Journals():

            if IsReversal(journal) or journal.IsSuspenseAccountAmountDifference():
                self.__provider.AE_CallObjectModifier(journal)

            trans[(journal.Class(), journal.Oid())] = journal

        link = pair.JournalLink()

        if link:
            trans[(link.Class(), link.Oid())] = link

        journalInfo = pair.JournalInformation()

        if journalInfo.IsInfant():
            trans[(journalInfo.Class(), journalInfo.Oid())] = journalInfo
