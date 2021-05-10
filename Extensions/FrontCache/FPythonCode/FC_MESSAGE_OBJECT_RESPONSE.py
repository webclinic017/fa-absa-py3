
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_MESSAGE_OBJECT_RESPONSE
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module contains a RESPONSE type that inherits from the MESSAGE OBJECT BASE.
                                It contains a couple of additional properties only applicable for a RESPONSE
                                Message Type.
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       XXXXXX
----------------------------------------------------------------------------------------------------------'''

'''----------------------------------------------------------------------------------------------------------
Importing Custom modules modules needed for Real Time ATS Worker.
----------------------------------------------------------------------------------------------------------'''
import FC_MESSAGE_OBJECT_BASE as MESSAGE_OBJECT_BASE
from FC_UTILS import FC_UTILS as UTILS
'''----------------------------------------------------------------------------------------------------------
Class defining the RESPONSE MESSAGE OBJECT
----------------------------------------------------------------------------------------------------------'''
class FC_MESSAGE_OBJECT_RESPONSE(MESSAGE_OBJECT_BASE.FC_MESSAGE_OBJECT_BASE):
    def __init__(self):
        MESSAGE_OBJECT_BASE.FC_MESSAGE_OBJECT_BASE.__init__(self)
        self.responseType = None
        self.expectedObjectCount = None

    def mapMessageObjectToAMBADataDictionary(self):
        dataDictionary = {UTILS.Constants.fcGenericConstants.AMBA_TXNBR : str(self.ambaTxNbr),
                        UTILS.Constants.fcGenericConstants.BATCH_ID : str(self.batchId),
                        UTILS.Constants.fcGenericConstants.IS_EOD : str(self.isEOD),
                        UTILS.Constants.fcGenericConstants.REPORT_DATE : str(self.reportDate),
                        UTILS.Constants.fcGenericConstants.REQUEST_DATETIME : str(self.requestDateTime),
                        UTILS.Constants.fcGenericConstants.REQUEST_EVENT_TYPE : str(self.requestEventType),
                        UTILS.Constants.fcGenericConstants.REQUEST_ID : str(self.requestId),
                        UTILS.Constants.fcGenericConstants.REQUEST_SOURCE : str(self.requestSource),
                        UTILS.Constants.fcGenericConstants.REQUEST_TYPE : str(self.requestType),
                        UTILS.Constants.fcGenericConstants.REQUEST_USER_ID : str(self.requestUserId),
                        UTILS.Constants.fcGenericConstants.SCOPE_NAME : str(self.scopeName),
                        UTILS.Constants.fcGenericConstants.SCOPE_NUMBER : str(self.scopeNumber),
                        UTILS.Constants.fcGenericConstants.TOPIC : str(self.topic),
                        UTILS.Constants.fcGenericConstants.RESPONSE_TYPE : str(self.responseType),
                        UTILS.Constants.fcGenericConstants.REPLAY : str(self.replay),
                        UTILS.Constants.fcGenericConstants.EXPECTED_OBJECT_COUNT : str(self.expectedObjectCount)}
        return dataDictionary
