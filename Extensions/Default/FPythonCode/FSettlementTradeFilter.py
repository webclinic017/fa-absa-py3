""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementTradeFilter.py"
import acm
import FOperationsUtils as Utils
from FOperationsFilter import Filter, FilterContainer
from FOperationsRuleEngine import Rule, QueryCondition, RuleExecutor, ValueType, ActionFunction, ActionValue
from FSettlementStatusQueries import GetDefaultSettlementProcessQuery, GetRecallStatusesQuery

class SettlementProcessFilterHandler:
    def __init__(self):

        import FSettlementParameters as SettlementParams
        self.__frc = FilterContainer(SettlementParams.tradeFilterQueries, GetDefaultSettlementProcessQuery(), acm.FTrade)
        self.__frc.GetFilterRules().append(Rule(QueryCondition(GetRecallStatusesQuery()), \
                               ActionFunction(FilterContainer.AddAction)))
        self.__ruleExecutor = RuleExecutor(self.__frc.GetFilterRules(), ActionFunction(SettlementProcessFilterHandler.FallBack))
        self.__isValidForProcessingRuleExecutor = RuleExecutor(self.__frc.GetActionValueFilterRules(), ActionValue(False))

    def FilterAndAddTrade(self, trade, tradeList):
        self.__ruleExecutor.Execute(trade, ValueType.SINGLE_VALUE, trade, tradeList)

    def IsTradeValidForProcessing(self, trade):
        if self.__isValidForProcessingRuleExecutor:
            return self.__isValidForProcessingRuleExecutor.Execute(trade, ValueType.SINGLE_VALUE, trade)
        else:
            return False

    @staticmethod
    def FallBack(trade, dummyTradeList):
        Utils.LogVerbose('Trade %d does not match trade filter and will not be considered for settlement processing.' % trade.Oid())

class SettlementEODTradeFilterHandler(object):

    def __init__(self):
        import FSettlementParameters as SettlementParams
        self.__defaultProcessFilterHandler = Filter(acm.FTrade, SettlementParams.tradeFilterQueries, GetDefaultSettlementProcessQuery())
        self.__amendmentProcessFilterHandler = Filter(acm.FTrade, SettlementParams.tradeAmendmentQueries, None, None, None, False)
        self.__tradeAmendmentFilterHandler = TradeAmendmentFilterHandler()

    def GetDefaultProcessTrades(self):
        defaultProcessTrades = self.__defaultProcessFilterHandler.GetObjects()
        returnList = acm.FArray()
        for trade in defaultProcessTrades:
            if self.__tradeAmendmentFilterHandler.IsAmendmentProcessTrade(trade) == False:
                returnList.Add(trade)
        return returnList

    def GetAmendmentProcessTrades(self):
        return self.__amendmentProcessFilterHandler.GetObjects()


class TradeAmendmentFilterHandler:

    def __init__(self):

        import FSettlementParameters as SettlementParams
        if SettlementParams.tradeAmendmentQueries:
            self.__frc = FilterContainer(SettlementParams.tradeAmendmentQueries, None, acm.FTrade)
            self.__ruleExecutor = RuleExecutor(self.__frc.GetFilterRules(), ActionFunction(TradeAmendmentFilterHandler.FallBack))
            self.__isAmendmentProcessTradeRuleExecutor = RuleExecutor(self.__frc.GetActionValueFilterRules(), ActionValue(False))
        else:
            self.__ruleExecutor = None
            self.__isAmendmentProcessTradeRuleExecutor = None

    def FilterAndAddTrade(self, trade, tradeList):
        if self.__ruleExecutor:
            if not GetRecallStatusesQuery().IsSatisfiedBy(trade):
                self.__ruleExecutor.Execute(trade, ValueType.SINGLE_VALUE, trade, tradeList)
        else:
            return []

    def IsAmendmentProcessTrade(self, trade):
        if self.__isAmendmentProcessTradeRuleExecutor and not GetRecallStatusesQuery().IsSatisfiedBy(trade):
            return self.__isAmendmentProcessTradeRuleExecutor.Execute(trade, ValueType.SINGLE_VALUE, trade)
        else:
            return False

    @staticmethod
    def FallBack(trade, tradeList):
        pass

class RegenerateSettlementTradeFilterHandler:
    def __init__(self):
        self.__processFilterHandler = SettlementProcessFilterHandler()
        self.__tradeAmendmentFilterHandler = TradeAmendmentFilterHandler()

    def IsTradeValidForDefaultProcessing(self, trade):
        valid = False
        if self.__processFilterHandler.IsTradeValidForProcessing(trade):
            if self.IsTradeValidForAmendmentProcessing(trade) == False:
                valid = True
        return valid

    def IsTradeValidForAmendmentProcessing(self, trade):
        return self.__tradeAmendmentFilterHandler.IsAmendmentProcessTrade(trade)

