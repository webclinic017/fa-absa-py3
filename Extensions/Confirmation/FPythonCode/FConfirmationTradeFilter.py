""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/confirmation/etc/FConfirmationTradeFilter.py"
import acm
import FOperationsUtils as Utils
from FOperationsFilter import Filter, FilterContainer
from FOperationsRuleEngine import RuleExecutor, ValueType, ActionFunction

from FConfirmationHelperFunctions import GetDefaultConfirmationProcessQuery

class ConfirmationProcessFilterHandler:

    def __init__(self):
        import FConfirmationParameters as ConfirmationParams

        self.__frc = FilterContainer(ConfirmationParams.tradeFilterQueries, GetDefaultConfirmationProcessQuery(), acm.FTrade)
        self.__ruleExecutor = RuleExecutor(self.__frc.GetFilterRules(), ActionFunction(ConfirmationProcessFilterHandler.FallBack))

    def FilterAndAddTrade(self, trade, tradeList):
        self.__ruleExecutor.Execute(trade, ValueType.SINGLE_VALUE, trade, tradeList)

    @staticmethod
    def FallBack(trade, dummyAList):
        Utils.LogVerbose('Trade %d does not match trade filter and will not be considered for confirmation processing.' % trade.Oid())

class ConfirmationEODTradeFilterHandler(Filter):
    def __init__(self):
        import FConfirmationParameters as ConfirmationParams

        super(ConfirmationEODTradeFilterHandler, self).__init__(acm.FTrade, ConfirmationParams.tradeFilterQueries, GetDefaultConfirmationProcessQuery())
