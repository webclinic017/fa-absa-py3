""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementProcessFunctions.py"
from FOperationsExceptions import CommitException
from FSettlementCorrectTradeRecaller import FSettlementCorrectTradeRecaller
import FSettlementGetters as Getters
from   FSettlementTransactionCommitter import TransactionCommitter
from   FSettlementSelector import SettlementSelector
from   FSettlementSecuritySelector import SettlementSecuritySelector
from FSettlementSecurityProcessEngine import SecurityProcessEngine
import FSettlementCreatorSingleton as Singleton
import FSettlementUtils as SettlementUtils
import FSettlementMatcher as Matcher
from FSettlementNettingRuleQueryCache import SettlementNettingRuleQueryCache
import FOperationsUtils as Utils

class SettlementProcessData:

    def __init__(self, settlementList, trade = None, messageString = None):

        self.__settlementList = settlementList
        self.__trade = trade
        self.__messageString = messageString


    def GetSettlementList(self):
        return self.__settlementList

    def GetTrade(self):
        return self.__trade

    def GetMessageString(self):
        return self.__messageString

    def ErrorLog(self, errorString):
        if self.__trade and self.__messageString:
            msg = 'Error while committing settlements for trade %d. %s. \nAMBA message:\n %s'
            Utils.LogAlways(msg % (self.__trade.Oid(), errorString, self.__messageString))
        else:
            Utils.LogAlways('Error while committing settlements: %s' % errorString)

#-------------------------------------------------------------------------
def CreateSettlementsFromTrade(trade, messageAsString, nettingRuleQueryCache):
    settlementCorrectTradeRecaller = FSettlementCorrectTradeRecaller()
    matcher, committerlist = CreateAndMatchSettlementsForTrade(trade, settlementCorrectTradeRecaller)
    spd = SettlementProcessData(matcher.GetMatchedSettlementsList(), trade, messageAsString)
    scl = Getters.GetSettlementCommitterList(spd, trade, settlementCorrectTradeRecaller)
    scl.extend(committerlist)
    tc  = TransactionCommitter(scl, spd, nettingRuleQueryCache)
    try:
        tc.CommitSettlements()
    except CommitException as error:
        spd.ErrorLog(error)

#-------------------------------------------------------------------------
def CreateSettlementsFromTrades(trades):
    nettingRuleQueryCache = SettlementNettingRuleQueryCache()
    for trade in trades:
        committerlist = list()
        settlementCorrectTradeRecaller = FSettlementCorrectTradeRecaller()
        matcher, committerlistTemp = CreateAndMatchSettlementsForTrade(trade, settlementCorrectTradeRecaller)
        spd = SettlementProcessData(matcher.GetMatchedSettlementsList(), trade, "")
        scl = Getters.GetSettlementCommitterList(spd, trade, settlementCorrectTradeRecaller)
        scl.extend(committerlistTemp)
        committerlist.extend(scl)
        tc  = TransactionCommitter(committerlist, spd, nettingRuleQueryCache)

        tc.CommitSettlements()

#-------------------------------------------------------------------------
def CreateAndMatchSettlementsForTrade(trade, settlementCorrectTradeRecaller):
    creator = Singleton.GetSettlementCreator()

    oldSettlements = SettlementSelector(trade).GetUpdateCandidates()
    newSettlements = creator.CreateSettlements(trade, settlementCorrectTradeRecaller)
    newSettlements = SettlementUtils.MergeSameSourceSettlements(trade, newSettlements)

    securitySelector = SettlementSecuritySelector(trade, oldSettlements, newSettlements)
    oldSettlements, newSettlements = securitySelector.FilterOutSecuritySettlements()
    oldSecuritySettlements, newSecuritySettlements, committerlist = SecurityProcessEngine.Process(securitySelector.SecuritySettlements(), trade)

    oldSettlements.extend(oldSecuritySettlements)
    newSettlements.extend(newSecuritySettlements)

    return (Matcher.SettlementMatcher(oldSettlements, newSettlements), committerlist)