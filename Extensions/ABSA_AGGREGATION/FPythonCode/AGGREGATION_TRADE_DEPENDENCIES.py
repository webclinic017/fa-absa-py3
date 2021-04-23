
from AGGREGATION_SELECTION_OBJECT import AGGREGATION_SELECTION
from AGGREGATION_SQL_HELPERS import SQL_HELPERS

class TRADE_DEPENDENCIES():
    def __init__(self, trdnbrs, archiveFlag):
        self.__trdnbrs = trdnbrs
        self.__archiveFlag = archiveFlag
        self.__dependencies = {}
        self.__getPayments()
        self.__getTradeAccountLinks()
        self.__getBusinessEventTradeLinks()
        self.__getPaymentAdditionalInfo()
        self.__getTradeAdditionalInfo()

    def __getPayments(self):
        sqlHelper = SQL_HELPERS()
        selectionList = [('AND', 'archive_status', '=', '%s' %self.__archiveFlag)]
        primarySelectionTuple = ('trdnbr', self.__trdnbrs)
        selectionObject = AGGREGATION_SELECTION('paynbr', 'payment', selectionList, primarySelectionTuple)
        self.__dependencies[('payments', 'payment', 'paynbr')] = sqlHelper.getObjectsFromSelectionObject(selectionObject)
        
    def __getTradeAccountLinks(self):
        sqlHelper = SQL_HELPERS()
        selectionList = [('AND', 'archive_status', '=', '%s' %self.__archiveFlag)]
        primarySelectionTuple = ('trdnbr', self.__trdnbrs)
        selectionObject = AGGREGATION_SELECTION('seqnbr', 'trade_account_link', selectionList, primarySelectionTuple)
        self.__dependencies[('accountLinks', 'trade_account_link', 'seqnbr')] = sqlHelper.getObjectsFromSelectionObject(selectionObject)

    def __getBusinessEventTradeLinks(self):
        sqlHelper = SQL_HELPERS()
        selectionList = [('AND', 'archive_status', '=', '%s' %self.__archiveFlag)]
        primarySelectionTuple = ('trdnbr', self.__trdnbrs)
        selectionObject = AGGREGATION_SELECTION('business_event_seqnbr', 'business_event_trd_link', selectionList, primarySelectionTuple)
        self.__dependencies[('businessEventTradeLinks', 'business_event_trd_link', 'business_event_seqnbr')] = sqlHelper.getObjectsFromSelectionObject(selectionObject)

    def __getPaymentAdditionalInfo(self):
        sqlHelper = SQL_HELPERS()
        selectionList = [('AND', 'o.archive_status', '=', '%s' %self.__archiveFlag)]
        primarySelectionTuple = ('recaddr', self.__dependencies[('payments', 'payment', 'paynbr')])
        selectionObject = AGGREGATION_SELECTION('valnbr', 'additional_info', selectionList, primarySelectionTuple)
        self.__dependencies[('paymentAdditionalInfos', 'additional_info', 'valnbr')] = sqlHelper.getObjectsFromSelectionObject(selectionObject, 22)

    def __getTradeAdditionalInfo(self):
        sqlHelper = SQL_HELPERS()
        selectionList = [('AND', 'o.archive_status', '=', '%s' %self.__archiveFlag)]
        primarySelectionTuple = ('recaddr', self.__trdnbrs)
        selectionObject = AGGREGATION_SELECTION('valnbr', 'additional_info', selectionList, primarySelectionTuple)
        self.__dependencies[('paymentAdditionalInfos', 'additional_info', 'valnbr')] = sqlHelper.getObjectsFromSelectionObject(selectionObject, 19)

    def getDependencies(self):
        return self.__dependencies
