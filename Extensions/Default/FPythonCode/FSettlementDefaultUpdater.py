""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementDefaultUpdater.py"
import acm

# Settlement
from FOperationsProvidedObject import IEngineTask
from FSettlementProcessFunctions import SettlementProcessData, CreateSettlementsFromTrade
from FSettlementProcessFilterHandlerSingleton import GetSettlementProcessFilterHandler
from FSettlementTradeAmendmentFilterHandlerSingleton import GetTradeAmendmentFilterHandler
from FSettlementUpdaterSingleton import GetSettlementUpdater
from FSettlementUtils import IsWithinTimeWindow
import FSettlementValidations as Validations
from FSettlementEnums import SettlementStatus

# Operations
import FOperationsUtils as Utils

#-------------------------------------------------------------------------
class FSettlementDefaultUpdater(IEngineTask):

    #-------------------------------------------------------------------------
    def __init__(self, configuration):
        self.__nettingRuleCache = configuration.nettingRuleCacheIF
        self.__processTradeSelector = configuration.processTradeSelectorIF
        self.__selector = configuration.selectorIF
        self.__transactionCommiter = configuration.transactionCommiterIF

    #-------------------------------------------------------------------------
    def PO_Init(self, provider):
        self.__provider = provider

    #-------------------------------------------------------------------------
    def PO_Clear(self):
        pass

    #-------------------------------------------------------------------------
    def ST_Run(self, msg, obj):
        self.__provider.LP_LogVerbose('Got ' + str(obj.Class().Name()) + ' with name ' + str(obj.Name() + \
                  ' updated by user ' + obj.UpdateUser().Name()))
        
        messageAsString = msg.mbf_object_to_string()

        tradeSelector = self.__processTradeSelector(obj, GetSettlementProcessFilterHandler(),
                                                       GetTradeAmendmentFilterHandler())
        tradeSelector.FilterAndAddTrades()
        amendmentProcessTrades = tradeSelector.GetAmendmentProcessTrades()
        defaultProcessTrades = tradeSelector.GetDefaultProcessTrades()

        amendmentProcessTrades.sort(Utils.SortByOid)
        defaultProcessTrades.sort(Utils.SortByOid)
        numberOfTrades = tradeSelector.GetNumberOfTrades()

        for amendmentProcessTrade in amendmentProcessTrades:
            self.__provider.LP_LogVerbose("Processing trade %d, %d left in trade queue" % (amendmentProcessTrade.Oid(), numberOfTrades))
            numberOfTrades = numberOfTrades - 1
            self.__AmendmentProcess(amendmentProcessTrade, messageAsString)

        for defaultProcessTrade in defaultProcessTrades:
            self.__provider.LP_LogVerbose("Processing trade %d, %d left in trade queue" % (defaultProcessTrade.Oid(), numberOfTrades))
            numberOfTrades = numberOfTrades - 1
            CreateSettlementsFromTrade(defaultProcessTrade, messageAsString, self.__nettingRuleCache)

    def __AmendmentProcess(self, trade, messageAsString):
        settlementUpdater = GetSettlementUpdater()
        oldSettlements = self.__selector(trade).GetUpdateCandidates()
        settlementCommitterList = list()
        oldSettlementsTemp = set()
        for oldSettlement in oldSettlements:
            originalSettlement = oldSettlement
            topSettlement = oldSettlement.GetTopSettlementInHierarchy()
            if originalSettlement.Parent():
                originalSettlement = originalSettlement.Parent()
            if originalSettlement.PartialChildren():
                for partialChild in originalSettlement.PartialChildren():
                    oldSettlementsTemp.add(partialChild)
            elif originalSettlement.PairOffParent():
                pairOffParent = originalSettlement.PairOffParent()
                if pairOffParent.IsSettled():
                    for pairOffChild in pairOffParent.PairOffChildren():
                        if not pairOffChild.IsPairedOff() and pairOffChild.Trade() == trade:
                            oldSettlementsTemp.add(pairOffChild)
            elif not Validations.IsCancelOrCorrectSettlement(topSettlement) and \
                    not (topSettlement.IsSecurity() and \
                    topSettlement.Status() == SettlementStatus.ACKNOWLEDGED):
                oldSettlementsTemp.add(oldSettlement)

        oldSettlements = list(oldSettlementsTemp)
        for oldSettlement in oldSettlements:
            if IsWithinTimeWindow(oldSettlement):
                settlementCommitterList.extend(settlementUpdater.UpdateSettlements(oldSettlement, None, True))
        for settlementCommitter in settlementCommitterList:
            settlement = settlementCommitter.GetSettlement()
            stateChart = acm.Operations.GetMappedSettlementProcessStateChart(settlement)
            settlement.StateChart(stateChart)
            settlement.UpdateStatusFromSettlementProcess(settlement.GetSettlementProcess())

        settlementProcessData = SettlementProcessData(None, trade, messageAsString)

        transactionCommitter = self.__transactionCommiter(settlementCommitterList, settlementProcessData, self.__nettingRuleCache)

        try:
            transactionCommitter.CommitSettlements()
        except CommitException as error:
            settlementProcessData.ErrorLog(error)
