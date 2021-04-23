
import copy
from AGGREGATION_SQL_HELPERS import INSTRUMENT_SQL_HELPERS
from AGGREGATION_SQL_HELPERS import SQL_HELPERS
from AGGREGATION_SELECTION_OBJECT import AGGREGATION_SELECTION

class INSTRUMENT_DEPENDENCY_FILTER():
    def __init__(self, setOfInstruments):
        self.__setOfInstruments = setOfInstruments
        self.__filterInstrumentsWithNonArchiveTrades()
    
    def __filterInstrumentSet(self, instrumentsToFilter):
        tempList = self.__setOfInstruments
        
        for insaddr in instrumentsToFilter:
            if insaddr in tempList:
                tempList.remove(insaddr)
        
        self.__setOfInstruments = tempList
    
    def __filterInstrumentsWithNonArchiveTrades(self):
        sqlHelper = INSTRUMENT_SQL_HELPERS()
        instrumentsToFilter = sqlHelper.getInstrumentsWithNonArchiveTrades(self.__setOfInstruments)
        self.__filterInstrumentSet(instrumentsToFilter)
    
    def __filterUnderlyingInstruments(self):
        self.__filterCreditRefUnderlyings()
        self.__filterIndexRefUnderlyings()
        self.__filterCombinationUnderlyings()
        self.__filterUnderlyings()
    
    def __filterCreditRefUnderlyings(self):
        sqlHelper = SQL_HELPERS()
        selectionList = [('AND', 'archive_status', '=', '0')]
        primarySelectionTuple = ('credit_ref', self.__setOfInstruments)
        selectionObject = AGGREGATION_SELECTION('credit_ref', 'leg', selectionList, primarySelectionTuple)
        creditRefUnderlyings = sqlHelper.getObjectsFromSelectionObject(selectionObject)
        self.__filterInstrumentSet(creditRefUnderlyings)
    
    def __filterIndexRefUnderlyings(self):
        sqlHelper = SQL_HELPERS()
        selectionList = [('AND', 'archive_status', '=', '0')]
        primarySelectionTuple = ('index_ref', self.__setOfInstruments)
        selectionObject = AGGREGATION_SELECTION('index_ref', 'leg', selectionList, primarySelectionTuple)
        indexRefUnderlyings = sqlHelper.getObjectsFromSelectionObject(selectionObject)
        self.__filterInstrumentSet(indexRefUnderlyings)
    
    def __filterCombinationUnderlyings(self):
        sqlHelper = SQL_HELPERS()
        selectionList = [('AND', 'archive_status', '=', '0')]
        primarySelectionTuple = ('member_insaddr', self.__setOfInstruments)
        selectionObject = AGGREGATION_SELECTION('member_insaddr', 'combination_link', selectionList, primarySelectionTuple)
        combinationUnderlyings = sqlHelper.getObjectsFromSelectionObject(selectionObject)
        self.__filterInstrumentSet(combinationUnderlyings)
    
    def __filterUnderlyings(self):
        sqlHelper = SQL_HELPERS()
        selectionList = [('AND', 'archive_status', '=', '0')]
        primarySelectionTuple = ('und_insaddr', self.__setOfInstruments)
        selectionObject = AGGREGATION_SELECTION('und_insaddr', 'instrument', selectionList, primarySelectionTuple)
        underlyings = sqlHelper.getObjectsFromSelectionObject(selectionObject)
        self.__filterInstrumentSet(underlyings)
    
    def getFilteredInstruments(self):
        return self.__setOfInstruments
