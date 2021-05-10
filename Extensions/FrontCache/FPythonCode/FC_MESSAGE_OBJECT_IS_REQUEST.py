
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_MESSAGE_OBJECT_REQUEST
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module contains a REQUEST type that inherits from the MESSAGE OBJECT BASE.
                                It contains a couple of additional properties only applicable for a REQUEST
                                Message Type.
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       XXXXXX
----------------------------------------------------------------------------------------------------------'''

'''----------------------------------------------------------------------------------------------------------
Importing Custom modules modules needed for Real Time ATS Worker.
----------------------------------------------------------------------------------------------------------'''
import FC_MESSAGE_OBJECT_REQUEST as MESSAGE_OBJECT_REQUEST
from FC_UTILS import FC_UTILS as UTILS
'''----------------------------------------------------------------------------------------------------------
Class defining the REQUEST MESSAGE OBJECT
----------------------------------------------------------------------------------------------------------'''
class FC_MESSAGE_OBJECT_IS_REQUEST(MESSAGE_OBJECT_REQUEST.FC_MESSAGE_OBJECT_REQUEST):
    def __init__(self):
        MESSAGE_OBJECT_REQUEST.FC_MESSAGE_OBJECT_REQUEST.__init__(self)
        self.portfolioName = ''
        self.portfolioNumber = 0
    
    def mapMessageObjectToAMBADataDictionary(self):
        dataDictionary = {UTILS.Constants.fcGenericConstants.AMBA_TXNBR : str(self.ambaTxNbr),
                        UTILS.Constants.fcGenericConstants.BATCH_ID : str(self.batchId),
                        UTILS.Constants.fcGenericConstants.BUILD_CONTROL_MEASURES : str(self.buildControlMeasures),
                        UTILS.Constants.fcGenericConstants.REPLAY : str(self.replay),
                        UTILS.Constants.fcGenericConstants.IS_EOD : str(self.isEOD),
                        UTILS.Constants.fcGenericConstants.IS_DATE_TODAY : str(self.isDateToday),
                        UTILS.Constants.fcGenericConstants.REPORT_DATE : str(self.reportDate),
                        UTILS.Constants.fcGenericConstants.REQUEST_DATETIME : str(self.requestDateTime),
                        UTILS.Constants.fcGenericConstants.REQUEST_EVENT_TYPE : str(self.requestEventType),
                        UTILS.Constants.fcGenericConstants.REQUEST_ID  : str(self.requestId),
                        UTILS.Constants.fcGenericConstants.REQUEST_SOURCE : str(self.requestSource),
                        UTILS.Constants.fcGenericConstants.REQUEST_TYPE : str(self.requestType),
                        UTILS.Constants.fcGenericConstants.REQUEST_USER_ID  : str(self.requestUserId),
                        UTILS.Constants.fcGenericConstants.SCOPE_NAME : str(self.scopeName),
                        UTILS.Constants.fcGenericConstants.SCOPE_NUMBER : str(self.scopeNumber),
                        UTILS.Constants.fcGenericConstants.SENDER_SUBJECT : str(self.senderSubject),
                        UTILS.Constants.fcGenericConstants.TOPIC : str(self.topic),
                        UTILS.Constants.fcGenericConstants.REQUEST_BATCH_COUNT : str(self.requestBatchCount),
                        UTILS.Constants.fcGenericConstants.REQUEST_BATCH_NO : str(self.requestBatchNo),
                        UTILS.Constants.fcGenericConstants.REQUEST_BATCH_START_INDEX : str(self.requestBatchStartIndex),
                        UTILS.Constants.fcGenericConstants.REQUEST_BATCH_END_INDEX : str(self.requestBatchEndIndex),
                        UTILS.Constants.fcGenericConstants.REQUEST_BATCH_TRADE_COUNT : str(self.requestBatchTradeCount),
                        UTILS.Constants.fcGenericConstants.REQUEST_COLLECTION_TRACKER_ID : str(self.requestCollectionTrackerId),
                        "PORTFOLIO_NAME" : str(self.portfolioName),
                        "PORTFOLIO_NUMBER" : str(self.portfolioNumber),
                        UTILS.Constants.fcGenericConstants.REQUEST_COLLECTION_PRIMARY_KEYS : str(self.requestCollectionPrimaryKeys),
                        "BACKDATE_START" : str(self.backDateStart)}
        return dataDictionary
