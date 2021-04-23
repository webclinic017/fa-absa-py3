
import acm
from AGGREGATION_GEN_HELPERS import GENERIC_HELPERS
from AGGREGATION_SELECTION_OBJECT import AGGREGATION_SELECTION
from AGGREGATION_SQL_HELPERS import SQL_HELPERS
from AGGREGATION_INSTRUMENT_FILTER import INSTRUMENT_DEPENDENCY_FILTER
from AGGREGATION_INS_DEPENDENCIES import INSTRUMENT_DEPENDENCIES

class INSTRUMENT_ARCHIVE():
    def __init__(self, parentObjects, archiveFlag):
        self.__parentObjects = parentObjects
        self.__archiveFlag = archiveFlag
        self.__instrumentIds = None
        self.__tradeArchvieFlag = 1
        self.__dependencies = {}
        self.__setInitialInstruments()
        if archiveFlag == 1:
            self.__filterInstruments()
        self.__getDependencies()
        
    def __setInitialInstruments(self):
        self.__helper = GENERIC_HELPERS()
        objectType = None
        if len(self.__parentObjects) > 0:
            if type(self.__parentObjects[0]) == int:
                objectType = 'int'
            else:
                objectType = self.__parentObjects[0].ClassName().Text()
        
        if objectType in ('FTrade', 'int'):
            sqlHelper = SQL_HELPERS()
            genHelper = GENERIC_HELPERS()
            selectionList = [('AND', 'archive_status', '=', self.__tradeArchvieFlag)]
            if objectType == 'FTrade':
                primarySelectionTuple = ('trdnbr', genHelper.acmOidToLinstInts(self.__parentObjects))
            else:
                primarySelectionTuple = ('trdnbr', self.__parentObjects)
            selectionObject = AGGREGATION_SELECTION('insaddr', 'trade', selectionList, primarySelectionTuple)
            self.__instrumentIds = sqlHelper.getObjectsFromSelectionObject(selectionObject)
        elif objectType == 'FInstrument':
            self.__instrumentIds = self.__helper.acmOidToLinstInts(self.__parentObjects)

    def __filterInstruments(self):
        filterHelper = INSTRUMENT_DEPENDENCY_FILTER(self.__instrumentIds)
        self.__instrumentIds = filterHelper.getFilteredInstruments()

    def __getDependencies(self):
        if self.__archiveFlag == 1:
            dependencyFlag = 0
        else:
            dependencyFlag = 1
        insDependency = INSTRUMENT_DEPENDENCIES(self.__instrumentIds, dependencyFlag)
        self.__dependencies = insDependency.getDependencies()

    def archiveDependencies(self):
        sqlHelper = SQL_HELPERS()
        for dependencyKey in self.__dependencies.keys():
            sqlHelper.archiveObjects(self.__dependencies[dependencyKey], dependencyKey[1], dependencyKey[2], acm.User().Oid(), 1)

    def deArchiveDependencies(self):
        sqlHelper = SQL_HELPERS()
        for dependencyKey in self.__dependencies.keys():
            sqlHelper.archiveObjects(self.__dependencies[dependencyKey], dependencyKey[1], dependencyKey[2], acm.User().Oid(), 0)
