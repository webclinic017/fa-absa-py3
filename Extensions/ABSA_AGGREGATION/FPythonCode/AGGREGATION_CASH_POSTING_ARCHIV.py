
from AGGREGATION_TRADE_ARCHIVE import TRADE_ARCHIVE
from AGGREGATION_INSTRUMENT_ARCHIVE import INSTRUMENT_ARCHIVE
from AGGREGATION_SQL_HELPERS import TRADE_SQL_HELPERS
from AGGREGATION_GEN_HELPERS import GENERIC_HELPERS

class AGGREGATION_ARCHIVE():
    def __init__(self, archiveOption, parentObjects, archiveFlag):
        self.__archiveOption = archiveOption
        self.__parentObjects = parentObjects
        self.__archiveFlag = archiveFlag
        self.__tradeArchive = None
        self.__instrumentArchive = None
        self.__setDependencies()
    
    def __setDependencies(self):
        if 'Trade' in self.__archiveOption:
            helper = GENERIC_HELPERS()
            self.__tradeArchive = TRADE_ARCHIVE(self.__parentObjects, self.__archiveFlag)
            self.__parentObjects = self.__tradeArchive.getTrades()
            
        if 'Instrument' in self.__archiveOption:
            self.__instrumentArchive = INSTRUMENT_ARCHIVE(self.__parentObjects, self.__archiveFlag)

    def archiveObjects(self):
        if 'Trade' in self.__archiveOption:
            self.__tradeArchive.archiveDependencies()
        
        if 'Instrument' in self.__archiveOption:
            self.__instrumentArchive.archiveDependencies()

    def deArchiveObjects(self):
        if 'Trade' in self.__archiveOption:
            self.__tradeArchive.deArchiveDependencies()
        
        if 'Instrument' in self.__archiveOption:
            self.__instrumentArchive.deArchiveDependencies()

class AGGREGATION_DEAGGREGATE():
    def __init__(self, trades):
        self.__trades = trades
    
    def deaggregateTrades(self):
        sqlHelper = TRADE_SQL_HELPERS()
        genHelper = GENERIC_HELPERS()
        sqlHelper.setArchiveStatusAggregateTrdnbnrAggregate(genHelper.acmOidToLinstInts(self.__trades), 0, "NULL", 0, 'aggregate_trdnbr')

    def deleteCachPostingTrades(self):
        genHelper = GENERIC_HELPERS()
        for trade in self.__trades:
            oid = trade.Oid()
            trade.Delete()
            genHelper.addToSummary('Trade', 'Delete', 1)
