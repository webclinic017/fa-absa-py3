
from AGGREGATION_SELECTION_OBJECT import AGGREGATION_SELECTION
from AGGREGATION_SQL_HELPERS import SQL_HELPERS

class INSTRUMENT_DEPENDENCIES():
    def __init__(self, insaddr, archiveFlag):
        self.__insaddrs = insaddr
        self.__archiveFlag = archiveFlag
        self.__dependencies = {}
        self.__getInstruments()
        self.__getLegs()
        self.__getCashFlows()
        self.__getResets()
        self.__getResetAdditionalInfo()
        self.__getCashFlowAdditionalInfo()
        self.__getLegAdditionalInfo()
        self.__getInstrumentAdditionalInfo()

    def __getInstruments(self):
        sqlHelper = SQL_HELPERS()
        selectionList = [('AND', 'archive_status', '=', '%s' %self.__archiveFlag)]
        primarySelectionTuple = ('insaddr', self.__insaddrs)
        selectionObject = AGGREGATION_SELECTION('insaddr', 'instrument', selectionList, primarySelectionTuple)
        self.__dependencies[('instruments', 'instrument', 'insaddr')] = sqlHelper.getObjectsFromSelectionObject(selectionObject)

    def __getLegs(self):
        sqlHelper = SQL_HELPERS()
        selectionList = [('AND', 'archive_status', '=', '%s' %self.__archiveFlag)]
        primarySelectionTuple = ('insaddr', self.__insaddrs)
        selectionObject = AGGREGATION_SELECTION('legnbr', 'leg', selectionList, primarySelectionTuple)
        self.__dependencies[('legs', 'leg', 'legnbr')] = sqlHelper.getObjectsFromSelectionObject(selectionObject)
        
    def __getCashFlows(self):
        sqlHelper = SQL_HELPERS()
        selectionList = [('AND', 'archive_status', '=', '%s' %self.__archiveFlag)]
        primarySelectionTuple = ('legnbr', self.__dependencies[('legs', 'leg', 'legnbr')])
        selectionObject = AGGREGATION_SELECTION('cfwnbr', 'cash_flow', selectionList, primarySelectionTuple)
        self.__dependencies[('cashFlows', 'cash_flow', 'cfwnbr')] = sqlHelper.getObjectsFromSelectionObject(selectionObject)

    def __getResets(self):
        sqlHelper = SQL_HELPERS()
        selectionList = [('AND', 'archive_status', '=', '%s' %self.__archiveFlag)]
        primarySelectionTuple = ('cfwnbr', self.__dependencies[('cashFlows', 'cash_flow', 'cfwnbr')])
        selectionObject = AGGREGATION_SELECTION('resnbr', 'reset', selectionList, primarySelectionTuple)
        self.__dependencies[('resets', 'reset', 'resnbr')] = sqlHelper.getObjectsFromSelectionObject(selectionObject)

    def __getResetAdditionalInfo(self):
        sqlHelper = SQL_HELPERS()
        selectionList = [('AND', 'o.archive_status', '=', '%s' %self.__archiveFlag)]
        primarySelectionTuple = ('recaddr', self.__dependencies[('resets', 'reset', 'resnbr')])
        selectionObject = AGGREGATION_SELECTION('valnbr', 'additional_info', selectionList, primarySelectionTuple)
        self.__dependencies[('resetAdditionalInfos', 'additional_info', 'valnbr')] = sqlHelper.getObjectsFromSelectionObject(selectionObject, 14)

    def __getCashFlowAdditionalInfo(self):
        sqlHelper = SQL_HELPERS()
        selectionList = [('AND', 'o.archive_status', '=', '%s' %self.__archiveFlag)]
        primarySelectionTuple = ('recaddr', self.__dependencies[('cashFlows', 'cash_flow', 'cfwnbr')])
        selectionObject = AGGREGATION_SELECTION('valnbr', 'additional_info', selectionList, primarySelectionTuple)
        self.__dependencies[('cashFlowAdditionalInfos', 'additional_info', 'valnbr')] = sqlHelper.getObjectsFromSelectionObject(selectionObject, 13)

    def __getLegAdditionalInfo(self):
        sqlHelper = SQL_HELPERS()
        selectionList = [('AND', 'o.archive_status', '=', '%s' %self.__archiveFlag)]
        primarySelectionTuple = ('recaddr', self.__dependencies[('legs', 'leg', 'legnbr')])
        selectionObject = AGGREGATION_SELECTION('valnbr', 'additional_info', selectionList, primarySelectionTuple)
        self.__dependencies[('legAdditionalInfos', 'additional_info', 'valnbr')] = sqlHelper.getObjectsFromSelectionObject(selectionObject, 12)

    def __getInstrumentAdditionalInfo(self):
        sqlHelper = SQL_HELPERS()
        selectionList = [('AND', 'o.archive_status', '=', '%s' %self.__archiveFlag)]
        primarySelectionTuple = ('recaddr', self.__insaddrs)
        selectionObject = AGGREGATION_SELECTION('valnbr', 'additional_info', selectionList, primarySelectionTuple)
        self.__dependencies[('instrumentAdditionalInfos', 'additional_info', 'valnbr')] = sqlHelper.getObjectsFromSelectionObject(selectionObject, 4)

    def getDependencies(self):
        return self.__dependencies
