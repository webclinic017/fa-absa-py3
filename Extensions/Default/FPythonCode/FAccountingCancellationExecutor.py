""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingCancellationExecutor.py"
import acm

# itertools


# accounting
from FAccountingEngineContracts import IAccountingEngine
from FAccountingDRCRPairGenerator import GenerateDRCRPairs
from FAccountingValidation import IsValidForCancellation
from FAccountingOperations import GetOpForObject
from FAccountingPairReverser import PerformCancellation
from FAccountingAggregation import IsPositionCancelled

#-------------------------------------------------------------------------
def CreateCancellationExecutorForSingles(cb):
    return __CancellationExecutor(__CancellationHelperSingle(cb))

#-------------------------------------------------------------------------
def CreateCancellationExecutorForPositions(cb):
    return __CancellationExecutor(__CancellationHelperPosition(cb))

#-------------------------------------------------------------------------
# Common functionality for all cancellation executors
#-------------------------------------------------------------------------
class __CancellationExecutor(IAccountingEngine.IAmendmentManager.ICancellationExecutor):

    #-------------------------------------------------------------------------
    def __init__(self, cancellationHelper):
        self.__provider = None
        self.__livePairsToCancel = dict()
        self.__cancellationHelper = cancellationHelper

    #-------------------------------------------------------------------------
    def PO_Init(self, provider):
        self.__provider = provider
        self.__cancellationHelper.PO_Init(self.__provider)

    #-------------------------------------------------------------------------
    def PO_Clear(self):
        self.__livePairsToCancel.clear()
        self.__cancellationHelper.PO_Clear()

    #-------------------------------------------------------------------------
    def CE_Remove(self, obj):
        self.__livePairsToCancel.pop(obj.Name(), None)

    #-------------------------------------------------------------------------
    def CE_PrepareData(self, obj, customStartDate):
        for pair in GenerateDRCRPairs(self.__cancellationHelper.CH_SelectCandidates(obj, customStartDate)):
            self.__livePairsToCancel[pair.Name()] = pair

    #-------------------------------------------------------------------------
    def CE_PerformCancellations(self):
        for _, pair in self.__livePairsToCancel.iteritems():

            if self.__cancellationHelper.CH_IsValidCancellation(pair):

                reversalPairs = PerformCancellation(pair, pair.EventDate(), self.__provider.Param('processDate'))

                for reversalPair in reversalPairs:
                    journalLink = reversalPair.JournalLink()
                    self.__provider.WR_AddItems([(GetOpForObject(obj), obj) for obj in reversalPair.Journals()])
                    self.__provider.WR_AddItem(GetOpForObject(journalLink), journalLink)

    #-------------------------------------------------------------------------
    def CE_ClearProcessedPositions(self):
        self.__cancellationHelper.CH_ClearProcessedPositions()

#-------------------------------------------------------------------------
# Cancellation Helper for cancellations on a single trade or settlement
#-------------------------------------------------------------------------
class __CancellationHelperSingle(IAccountingEngine.IAmendmentManager.ICancellationExecutor.ICancellationHelper):

    #-------------------------------------------------------------------------
    def __init__(self, liveDataToCancelCb):
        self.__provider = None
        self.__liveDataToCancelCb = liveDataToCancelCb

    #-------------------------------------------------------------------------
    def PO_Init(self, provider):
        self.__provider = provider

    #------------------------------------------------------------------------
    def CH_SelectCandidates(self, obj, customStartDate):

        startDate = customStartDate
        endDate = self.__provider.Param("endDate")
        eodDate = self.__provider.Param("endOfDayDate")
        bFilter = self.__provider.Param("bookFilter")
        blFilter = self.__provider.Param("bookLinkFilter")
        tlFilter = self.__provider.Param("treatmentLinkFilter")

        validationFunctor = lambda j: IsValidForCancellation(j, startDate, endDate, eodDate, bFilter, blFilter, tlFilter)

        return imap(lambda j: j.Clone(), ifilter(validationFunctor, self.__liveDataToCancelCb(obj).Select()))

    #------------------------------------------------------------------------
    def CH_IsValidCancellation(self, pair):
        return True

    #------------------------------------------------------------------------
    def CH_ClearProcessedPositions(self):
        pass

#-------------------------------------------------------------------------
# Cancellation Helper for positions
#-------------------------------------------------------------------------
class __CancellationHelperPosition(IAccountingEngine.IAmendmentManager.ICancellationExecutor.ICancellationHelper):

    #-------------------------------------------------------------------------
    def __init__(self, liveDataToCancelCb):
        self.__provider = None
        self.__processedPositions = set()
        self.__liveDataToCancelCb = liveDataToCancelCb

    #-------------------------------------------------------------------------
    def PO_Init(self, provider):
        self.__provider = provider

    #------------------------------------------------------------------------
    def CH_SelectCandidates(self, obj, customStartDate):

        if self.__liveDataToCancelCb:

            aggLevels = self.__GetAggLevelsToAddDataFor(obj)

            if len(aggLevels) > 0:

                startDate = customStartDate
                endDate = self.__provider.Param("endDate")
                eodDate = self.__provider.Param("endOfDayDate")
                bFilter = self.__provider.Param("bookFilter")
                blFilter = self.__provider.Param("bookLinkFilter")
                tlFilter = self.__provider.Param("treatmentLinkFilter")

                validationFunctor = lambda j: IsValidForCancellation(j, startDate, endDate, eodDate, bFilter, blFilter, tlFilter)

                return imap(lambda j: j.Clone(), ifilter(validationFunctor, self.__liveDataToCancelCb(obj, aggLevels).Select()))

        return []

    #------------------------------------------------------------------------
    def CH_IsValidCancellation(self, pair):
        key = acm.Accounting().GetPositionKey(pair.JournalInformation())

        if not key or \
          (self.__provider.AE_IsPositionCached(key) or \
           IsPositionCancelled(pair.JournalInformation())):
            return True
        return False

    #------------------------------------------------------------------------
    def CH_ClearProcessedPositions(self):
        self.__processedPositions.clear()

    #-------------------------------------------------------------------------
    def __GetAggLevelsToAddDataFor(self, obj):
        aggLevels = []

        if obj.ContractTrade() and \
           obj.ContractTrade().Oid() not in self.__processedPositions:

            self.__processedPositions.add(obj.ContractTrade().Oid())
            aggLevels.append('Contract Trade Number')
            aggLevels.append('Contract Trdnbr and Moneyflow')

        if obj.Portfolio() and obj.Instrument() and \
           (obj.Portfolio().Oid(), obj.Instrument().Oid()) not in self.__processedPositions:

            self.__processedPositions.add((obj.Portfolio().Oid(), obj.Instrument().Oid()))
            aggLevels.append('Instrument and Portfolio')

        return aggLevels
        