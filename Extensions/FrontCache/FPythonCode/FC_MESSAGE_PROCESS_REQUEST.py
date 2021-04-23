
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_MESSAGE_PROCESS_REQUEST
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module process a REQUEST message from the AMB and tranform it into a
                                Request Object
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       XXXXXX
----------------------------------------------------------------------------------------------------------'''

'''----------------------------------------------------------------------------------------------------------
Importing Custom Modules
----------------------------------------------------------------------------------------------------------'''
from FC_UTILS import FC_UTILS as UTILS
import FC_MESSAGE_PROCESS_BASE as MESSAGE_PROCESS_BASE
from AMBA_Helper_Functions import AMBA_Helper_Functions as ambaUtils

'''----------------------------------------------------------------------------------------------------------
Request Message Process Type Class. This class will check if the mandatory fields are present on the incoming AMB
message and create an incoming message object.
----------------------------------------------------------------------------------------------------------'''
class FC_MESSAGE_PROCESS_REQUEST(MESSAGE_PROCESS_BASE.FC_MESSAGE_PROCESS_BASE):
    def __init__(self, incomingAMBAMessageData, incomingMessageObject):
        MESSAGE_PROCESS_BASE.FC_MESSAGE_PROCESS_BASE.__init__(self, incomingAMBAMessageData, incomingMessageObject)
        self.__mapRequestMessageAttributes()
        
    def __mapRequestMessageAttributes(self):

        requestBatchCount = ambaUtils.get_AMBA_Object_Value(self.dataTag, UTILS.Constants.fcGenericConstants.REQUEST_BATCH_COUNT)
        if not requestBatchCount:
            UTILS.Logger.flogger.warn(UTILS.Constants.fcFloggerConstants.COULD_NOT_RETRIEVE_REQUEST_BATCH_COUNT_TAG_FROM_INCOMING_AMBA_MSG)
        else:
            self._incomingMessageObject.requestBatchCount = int(requestBatchCount)
                    
        '''----------------------------------------------------------------------------------------------------------
        Fetch the BUILD_CONTROL_MEASURES attribute on the message
        ----------------------------------------------------------------------------------------------------------'''
        buildControlMeasures = ambaUtils.get_AMBA_Object_Value(self.dataTag, UTILS.Constants.fcGenericConstants.BUILD_CONTROL_MEASURES)
        if buildControlMeasures:
            self._incomingMessageObject.buildControlMeasures = str(buildControlMeasures)

        '''----------------------------------------------------------------------------------------------------------
        Fetch the REPLAY attribute on the message
        ----------------------------------------------------------------------------------------------------------'''
        replay = ambaUtils.get_AMBA_Object_Value(self.dataTag, UTILS.Constants.fcGenericConstants.REPLAY)
        if replay:
            self._incomingMessageObject.replay = str(replay)
                    
        '''----------------------------------------------------------------------------------------------------------
        Fetch the REQUEST_BATCH_NO attribute on the message
        ----------------------------------------------------------------------------------------------------------'''
        requestBatchNo = ambaUtils.get_AMBA_Object_Value(self.dataTag, UTILS.Constants.fcGenericConstants.REQUEST_BATCH_NO)
        if not requestBatchNo:
            UTILS.Logger.flogger.warn(UTILS.Constants.fcFloggerConstants.COULD_NOT_RETRIEVE_THE_REQUEST_BATCH_NO_TAG_FROM_INCOMING_AMBA_MSG)
        else:
            self._incomingMessageObject.requestBatchNo = int(requestBatchNo)

        '''----------------------------------------------------------------------------------------------------------
        Fetch the REQUEST_BATCH_START_INDEX attribute on the message
        ----------------------------------------------------------------------------------------------------------'''
        requestBatchStartIndex = ambaUtils.get_AMBA_Object_Value(self.dataTag, UTILS.Constants.fcGenericConstants.REQUEST_BATCH_START_INDEX)
        if not requestBatchStartIndex:
            UTILS.Logger.flogger(UTILS.Constants.fcFloggerConstants.COULD_NOT_RETRIEVE_REQUEST_BATCH_START_INDEX_TAG_FROM_INCOMING_AMBA_MSG)
        else:
            self._incomingMessageObject.requestBatchStartIndex = int(requestBatchStartIndex)

        '''----------------------------------------------------------------------------------------------------------
        Fetch the REQUEST_BATCH_END_INDEX attribute on the message
        ----------------------------------------------------------------------------------------------------------'''
        requestBatchEndIndex = ambaUtils.get_AMBA_Object_Value(self.dataTag, UTILS.Constants.fcGenericConstants.REQUEST_BATCH_END_INDEX)
        if not requestBatchEndIndex:
            UTILS.Logger.flogger(UTILS.Constants.fcFloggerConstants.COULD_NOT_RETRIEVE_REQUEST_BATCH_END_INDEX_TAG_FROM_INCOMING_AMBA_MSG)
        else:
            self._incomingMessageObject.requestBatchEndIndex = int(requestBatchEndIndex)

        '''----------------------------------------------------------------------------------------------------------
        Fetch the REQUEST_BATCH_TRADE_COUNT attribute on the message
        ----------------------------------------------------------------------------------------------------------'''
        requestBatchTradeCount = ambaUtils.get_AMBA_Object_Value(self.dataTag, UTILS.Constants.fcGenericConstants.REQUEST_BATCH_TRADE_COUNT)
        if not requestBatchTradeCount:
            UTILS.Logger.flogger.warn(UTILS.Constants.fcFloggerConstants.COULD_NOT_RETRIEVE_REQUEST_BATCH_TRADE_COUNT_FROM_INCOMING_AMBA_MSG)
        else:
            self._incomingMessageObject.requestBatchTradeCount = int(requestBatchTradeCount)
        
        '''----------------------------------------------------------------------------------------------------------
        Fetch the REQUEST_COLLECTION_TRACKER_ID attribute on the message
        ----------------------------------------------------------------------------------------------------------'''
        requestCollectionTrackerId = ambaUtils.get_AMBA_Object_Value(self.dataTag, UTILS.Constants.fcGenericConstants.REQUEST_COLLECTION_TRACKER_ID)
        if not requestCollectionTrackerId:
            UTILS.Logger.flogger.warn(UTILS.Constants.fcFloggerConstants.COULD_NOT_RETREIVE_REQUEST_COLLECTION_TRACKER_ID_FROM_INCOMING_AMBA_MSG)
        else:
            self._incomingMessageObject.requestCollectionTrackerId = int(requestCollectionTrackerId)

        '''----------------------------------------------------------------------------------------------------------
        Fetch the PORTFOLIO_NAME attribute on the message
        ----------------------------------------------------------------------------------------------------------'''
        portfolioName = ambaUtils.get_AMBA_Object_Value(self.dataTag, 'PORTFOLIO_NAME')
        if not portfolioName:
            UTILS.Logger.flogger.warn('COULD NOT RETRIEVE THE PORTFOLIO_NAME TAG %s' %__name__)
        else:
            try:
                self._incomingMessageObject.portfolioName = str(portfolioName)
            except:
                self._incomingMessageObject.portfolioName = ''

        '''----------------------------------------------------------------------------------------------------------
        Fetch the PORTFOLIO_NUMBER attribute on the message
        ----------------------------------------------------------------------------------------------------------'''
        portfolioNumber = ambaUtils.get_AMBA_Object_Value(self.dataTag, 'PORTFOLIO_NUMBER')
        if not portfolioNumber:
            UTILS.Logger.flogger.warn('COULD NOT RETRIEVE THE PORTFOLIO_NUMBER TAG %s' %__name__)
        else:
            try:
                self._incomingMessageObject.portfolioNumber = int(portfolioNumber)
            except:
                self._incomingMessageObject.portfolioNumber = 0

        '''----------------------------------------------------------------------------------------------------------
        Fetch the REQUEST_COLLECTION_PRIMARY_KEYS attribute on the message
        ----------------------------------------------------------------------------------------------------------'''
        requestCollectionPrimaryKeys = ambaUtils.get_AMBA_Object_Value(self.dataTag, UTILS.Constants.fcGenericConstants.REQUEST_COLLECTION_PRIMARY_KEYS)
        if not requestCollectionPrimaryKeys:
            UTILS.Logger.flogger.warn(UTILS.Constants.fcFloggerConstants.COULD_NOT_RETRIEVE_REQUEST_COLLECTION_PRIMARY_KEYS_FROM_INCOMING_AMBA_MSG)
        else:
            self._incomingMessageObject.requestCollectionPrimaryKeys = map(int, requestCollectionPrimaryKeys.split(','))
