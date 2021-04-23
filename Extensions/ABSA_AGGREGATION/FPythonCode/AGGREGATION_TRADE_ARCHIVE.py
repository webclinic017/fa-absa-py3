import acm
from AGGREGATION_GEN_HELPERS import GENERIC_HELPERS
from AGGREGATION_SQL_HELPERS import TRADE_SQL_HELPERS
from AGGREGATION_TRADE_FILTER import TRADE_DEPENDENCY_FILTER
from AGGREGATION_TRADE_DEPENDENCIES import TRADE_DEPENDENCIES
from AGGREGATION_SQL_HELPERS import SQL_HELPERS

class TRADE_ARCHIVE():
    def __init__(self, parentTrades, archiveFlag):
        self.__helper = GENERIC_HELPERS()
        self.__parentTrdnbrs = self.__helper.acmOidToLinstInts(parentTrades)
        self.__archiveFlag = archiveFlag
        self.__trades = None
        self.__dependencies = {}
        self.__tradeArchvieFlag = 1
        self.__getAggregateTrades()
        self.__filterTrades()
        self.__getDependencies()
    
    def __getAggregateTrades(self):
        sqlHelper = TRADE_SQL_HELPERS()
        self.__trades = sqlHelper.getAggregateTrades(self.__parentTrdnbrs, self.__tradeArchvieFlag)
        
    def __filterTrades(self):
        filterHelper = TRADE_DEPENDENCY_FILTER(self.__trades)
        self.__trades = filterHelper.getFilteredTrades()

    def __getDependencies(self):
        if self.__archiveFlag == 1:
            dependencyFlag = 0
        else:
            dependencyFlag = 1
        trdDependency = TRADE_DEPENDENCIES(self.__trades, dependencyFlag)
        self.__dependencies = trdDependency.getDependencies()

    def archiveDependencies(self):
        sqlHelper = SQL_HELPERS()
        for dependencyKey in list(self.__dependencies.keys()):
            sqlHelper.archiveObjects(self.__dependencies[dependencyKey], dependencyKey[1], dependencyKey[2], acm.User().Oid(), 1)

    def deArchiveDependencies(self):
        sqlHelper = SQL_HELPERS()
        for dependencyKey in list(self.__dependencies.keys()):
            sqlHelper.archiveObjects(self.__dependencies[dependencyKey], dependencyKey[1], dependencyKey[2], acm.User().Oid(), 0)

    def getTrades(self):
        return self.__trades
