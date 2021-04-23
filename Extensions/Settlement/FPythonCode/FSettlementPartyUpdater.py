""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementPartyUpdater.py"

# Settlement
from FOperationsProvidedObject import IEngineTask
from FSettlementProcessFunctions import SettlementProcessData
from FSettlementUtils import IsWithinTimeWindow
from FSettlementTradeAmendmentFilterHandlerSingleton import GetTradeAmendmentFilterHandler
import FSettlementGetters as Getters
import FSettlementMatcher as Matcher

# Operations
from FOperationsExceptions import CommitException

#-------------------------------------------------------------------------
class FSettlementPartyUpdater(IEngineTask):

    #-------------------------------------------------------------------------
    def __init__(self, configuration):
        self.__nettingRuleCache = configuration.nettingRuleCacheIF
        self.__picker = configuration.pickerIF
        self.__transactionCommiter = configuration.transactionCommiterIF
        self.__ambaMessageCreator = configuration.ambaMessageIF

        self.__correctTradeRecaller = configuration.correctTradeRecallerIF
        self.__partyUpdateCommiter = configuration.partyUpdateCommiterIF
        self.__securitySelector = configuration.securitySelectorIF
        self.__securityProcessEngine = configuration.securityProcessEngineIF
        self.__partyUpdateHandler = configuration.partyUpdateHandlerIF

    #-------------------------------------------------------------------------
    def PO_Init(self, provider):
        self.__provider = provider

    #-------------------------------------------------------------------------
    def PO_Clear(self):
        pass

    #-------------------------------------------------------------------------
    def ST_Run(self, msg, obj):
        ambaMessage = self.__ambaMessageCreator(msg)
        assert ambaMessage.GetNameOfUpdatedTable() == 'PARTY'

        if ambaMessage.GetTypeOfUpdate() == 'UPDATE':
            self.__Update(msg)

    #-------------------------------------------------------------------------
    def __Update(self, msg):
        ambaMessage = self.__ambaMessageCreator(msg)
        partyUpdateHandler = self.__partyUpdateHandler(ambaMessage)
        if not partyUpdateHandler.HasAnyValuesAffectingSettlementsChanged():
            self.__provider.LP_LogVerbose('The party update did not contain any changes affecting settlements so it will not be processed.')
            return
        connectedSettlements = partyUpdateHandler.FindConnectedSettlements()
        settlementsWithinTimeWindow = list()
        for settlement in connectedSettlements:
            if IsWithinTimeWindow(settlement):
                settlementsWithinTimeWindow.append(settlement)

        settlementsToProcess = self.__GetSettlementsWithoutAmendmentSettlements(self.__picker(settlementsWithinTimeWindow).GetUpdateCandidates())

        oldAndUpdatedSettlements, groupedSecuritySettlements = self.__GetSettlementsToProcess(settlementsToProcess, partyUpdateHandler)
        self.__HandleSecuritySettlements(groupedSecuritySettlements)

        spd = SettlementProcessData(oldAndUpdatedSettlements)
        scl = Getters.GetSettlementCommitterList(spd, None, self.__correctTradeRecaller)
        puc = self.__partyUpdateCommiter(scl, spd, self.__nettingRuleCache)
        puc.CommitSettlements()

    #-------------------------------------------------------------------------
    def __GetSettlementsWithoutAmendmentSettlements(self, settlementList):
        amendmentFilter = GetTradeAmendmentFilterHandler()
        returnList = list()
        for settlement in settlementList:
            if settlement.Trade():
                if amendmentFilter.IsAmendmentProcessTrade(settlement.Trade()) == False:
                    returnList.append(settlement)
            else:
                returnList.append(settlement)
        return returnList

    #-------------------------------------------------------------------------
    def __GetSettlementsToProcess(self, settlementsToProcess, partyUpdateHandler):
        oldAndUpdatedSettlements = list()
        oldSettlements = list()
        newSettlements = list()
        groupedSecuritySettlements = {}
        securitySelector = self.__securitySelector(None, None, None)
        for settlement in settlementsToProcess:
            oldSettlement = [settlement]
            newSettlement = [partyUpdateHandler.CreateUpdatedSettlement(settlement)]
            securitySelector.SetSettlements(oldSettlement, newSettlement)
            oldSettlements, newSettlements = securitySelector.FilterOutSecuritySettlements()
            if oldSettlements and newSettlements:
                oldAndUpdatedSettlements.append((oldSettlements[0], newSettlements[0]))
            securitySettlements = securitySelector.SecuritySettlements()
            if securitySettlements:
                securitySettlement = securitySettlements[0]
                if securitySettlement.Trade():
                    tradeSettlements = groupedSecuritySettlements.get(securitySettlement.Trade(), list())
                    tradeSettlements.append(securitySettlement)
                    groupedSecuritySettlements[securitySettlement.Trade()] = tradeSettlements
        return oldAndUpdatedSettlements, groupedSecuritySettlements

    #-------------------------------------------------------------------------
    def __HandleSecuritySettlements(self, groupedSecuritySettlements):
        for trade, settlements in list(groupedSecuritySettlements.items()):
            oldSecuritySettlements, newSecuritySettlements, committerlist = self.__securityProcessEngine.Process(settlements, trade)
            matcher = Matcher.SettlementMatcher(oldSecuritySettlements, newSecuritySettlements)
            matchedSettlements = matcher.GetMatchedSettlementsList()
            spd = SettlementProcessData(matchedSettlements)
            scl = Getters.GetSettlementCommitterList(spd, trade, self.__correctTradeRecaller)
            scl.extend(committerlist)
            tc  = self.__transactionCommiter(scl, spd, self.__nettingRuleCache)
            try:
                tc.CommitSettlements()
            except CommitException as error:
                spd.ErrorLog(error)
