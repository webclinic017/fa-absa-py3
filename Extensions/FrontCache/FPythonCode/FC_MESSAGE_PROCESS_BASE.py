
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_MESSAGE_PROCESS_BASE
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module process a REQUEST message from the AMB and tranform it into a
                                Request Object. This class will process the common attributes available on all
                                type of messages.
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       XXXXXX
----------------------------------------------------------------------------------------------------------'''

'''----------------------------------------------------------------------------------------------------------
Importing all relevant Python modules.
----------------------------------------------------------------------------------------------------------'''
from datetime import datetime

'''----------------------------------------------------------------------------------------------------------
Importing Custom Modules
----------------------------------------------------------------------------------------------------------'''
import FC_UTILS as FC_UTILS
from FC_UTILS import FC_UTILS as UTILS
from AMBA_Helper_Functions import AMBA_Helper_Functions as ambaUtils

'''----------------------------------------------------------------------------------------------------------
Request Message Process Type Class. This class will check if the mandatory fields are present on the incoming AMB
message and create an incoming message object.
----------------------------------------------------------------------------------------------------------'''
class FC_MESSAGE_PROCESS_BASE():
    def __init__(self, incomingAMBAMessageData, incomingMessageObject):
        self._incomingAMBAMessage = incomingAMBAMessageData
        self._incomingMessageObject = incomingMessageObject
        self.dataTag = None
        self.__mapIncomingAMBAMessageToRequestResponseObject()
    
    def __mapIncomingAMBAMessageToRequestResponseObject(self):
        try:
            '''----------------------------------------------------------------------------------------------------------
            Fetch the Data Tag where all the request/response details is located
            ----------------------------------------------------------------------------------------------------------'''
            dataTag = ambaUtils.object_by_name(self._incomingAMBAMessage, [''], UTILS.Constants.fcGenericConstants.DATA)
            if not dataTag:
                UTILS.Logger.flogger.warn(UTILS.Constants.fcFloggerConstants.COULD_NOT_RETRIEVE_DATA_TAG_FROM_INCOMMING_AMBA_MSG %__name__)
            else:
                self.dataTag = dataTag

            buildControlMeasures = ambaUtils.get_AMBA_Object_Value(self.dataTag, UTILS.Constants.fcGenericConstants.BUILD_CONTROL_MEASURES)
            if buildControlMeasures:
                self._incomingMessageObject.buildControlMeasures = str(buildControlMeasures)

            replay = ambaUtils.get_AMBA_Object_Value(self.dataTag, UTILS.Constants.fcGenericConstants.REPLAY)
            if replay:
                self._incomingMessageObject.replay = str(replay)
                
            '''----------------------------------------------------------------------------------------------------------
            Fetch the AMBA_TXNBR attribute on the message
            ----------------------------------------------------------------------------------------------------------'''
                    
            ambaTxNbr = ambaUtils.get_AMBA_Object_Value(self.dataTag, UTILS.Constants.fcGenericConstants.AMBA_TXNBR)
            if not ambaTxNbr:
                UTILS.Logger.flogger.warn(UTILS.Constants.fcFloggerConstants.COULD_NOT_RETRIEVE_AMBA_TXNBR_FROM_INCOMING_AMBA_MSG %__name__)
            else:
                self._incomingMessageObject.ambaTxNbr = int(ambaTxNbr)

            '''----------------------------------------------------------------------------------------------------------
            Fetch the BATCH_ID attribute on the message
            ----------------------------------------------------------------------------------------------------------'''
            batchId = ambaUtils.get_AMBA_Object_Value(self.dataTag, UTILS.Constants.fcGenericConstants.BATCH_ID)
            if not batchId:
                UTILS.Logger.flogger.warn(UTILS.Constants.fcFloggerConstants.COULD_NOT_RETRIEVE_THE_BATCH_ID_TAG_FROM_INCOMING_AMBA_MSG_S %__name__)
            else:
                self._incomingMessageObject.batchId = int(batchId)

            '''----------------------------------------------------------------------------------------------------------
            Fetch the IS_DATE_TODAY attribute on the message
            ----------------------------------------------------------------------------------------------------------'''
            isDateToday = ambaUtils.get_AMBA_Object_Value(self.dataTag, UTILS.Constants.fcGenericConstants.IS_DATE_TODAY)
            if not isDateToday:
                UTILS.Logger.flogger.warn(UTILS.Constants.fcFloggerConstants.COULD_NOT_RETRIEVE_IS_DATE_TODAY_TAG_FROM_INCOMING_AMBA_MSG_S %__name__)
            else:
                self._incomingMessageObject.isDateToday = int(isDateToday)

            '''----------------------------------------------------------------------------------------------------------
            Fetch the IS_EOD attribute on the message
            ----------------------------------------------------------------------------------------------------------'''
            isEOD = ambaUtils.get_AMBA_Object_Value(self.dataTag, UTILS.Constants.fcGenericConstants.IS_EOD)
            if not isEOD:
                UTILS.Logger.flogger.warn(UTILS.Constants.fcFloggerConstants.COULD_NOT_RETRIEVE_IS_EOD_TAG_FROM_INCOMING_AMBA_MSG_S %__name__)
            else:
                self._incomingMessageObject.isEOD = int(isEOD)

            '''----------------------------------------------------------------------------------------------------------
            Fetch the REPORT_DATE attribute on the message
            ----------------------------------------------------------------------------------------------------------'''
            reportDate = ambaUtils.get_AMBA_Object_Value(self.dataTag, UTILS.Constants.fcGenericConstants.REPORT_DATE)
            if not reportDate:
                UTILS.Logger.flogger.warn(UTILS.Constants.fcFloggerConstants.COULD_NOT_RETRIEVE_THE_REPORT_DATE_TAG_FROM_INCOMING_AMBA_MSG_S %__name__)
            else:
                self._incomingMessageObject.reportDate = FC_UTILS.formatDate(reportDate)

            '''----------------------------------------------------------------------------------------------------------
            Fetch the REQUEST_DATETIME attribute on the message
            ----------------------------------------------------------------------------------------------------------'''
            requestDateTime = ambaUtils.get_AMBA_Object_Value(self.dataTag, UTILS.Constants.fcGenericConstants.REQUEST_DATETIME)
            if not requestDateTime:
                UTILS.Logger.flogger.warn(UTILS.Constants.fcFloggerConstants.COULD_NOT_RETRIEVE_REQUEST_DATETIME_TAG_FROM_INCOMING_AMBA_MSG_S %__name__)
            else:
                self._incomingMessageObject.requestDateTime = FC_UTILS.formatDate(requestDateTime)

            '''----------------------------------------------------------------------------------------------------------
            Fetch the REQUEST_EVENT_TYPE attribute on the message
            ----------------------------------------------------------------------------------------------------------'''
            requestEventType = ambaUtils.get_AMBA_Object_Value(self.dataTag, UTILS.Constants.fcGenericConstants.REQUEST_EVENT_TYPE)
            if not requestEventType:
                UTILS.Logger.flogger.warn(UTILS.Constants.fcFloggerConstants.COULD_NOT_RETRIEVE_THE_REQUEST_EVENT_TYPE_TAG_FROM_INCOMING_AMBA_MSG_S %__name__)
            else:
                self._incomingMessageObject.requestEventType = str(requestEventType)

            '''----------------------------------------------------------------------------------------------------------
            Fetch the REQUEST_ID attribute on the message
            ----------------------------------------------------------------------------------------------------------'''
            requestId = ambaUtils.get_AMBA_Object_Value(self.dataTag, UTILS.Constants.fcGenericConstants.REQUEST_ID)
            if not requestId:
                UTILS.Logger.flogger.warn(UTILS.Constants.fcFloggerConstants.COULD_NOT_RETRIEVE_THE_REQUEST_ID_TAG_FROM_INCOMING_AMBA_MSG_S %__name__)
            else:
                self._incomingMessageObject.requestId = int(requestId)

            '''----------------------------------------------------------------------------------------------------------
            Fetch the REQUEST_SOURCE attribute on the message
            ----------------------------------------------------------------------------------------------------------'''
            requestSource = ambaUtils.get_AMBA_Object_Value(self.dataTag, UTILS.Constants.fcGenericConstants.REQUEST_SOURCE)
            if not requestSource:
                UTILS.Logger.flogger.warn(UTILS.Constants.fcFloggerConstants.COULD_NOT_RETRIEVE_THE_REQUEST_SOURCE_TAG_FROM_INCOMING_AMBA_MSG_S %__name__)
            else:
                self._incomingMessageObject.requestSource = str(requestSource)

            '''----------------------------------------------------------------------------------------------------------
            Fetch the REQUEST_TYPE attribute on the message
            ----------------------------------------------------------------------------------------------------------'''
            requestType = ambaUtils.get_AMBA_Object_Value(self.dataTag, UTILS.Constants.fcGenericConstants.REQUEST_TYPE)
            if not requestType:
                UTILS.Logger.flogger.warn(UTILS.Constants.fcFloggerConstants.COULD_NOT_RETRIEVE_THE_REQUEST_TYPE_TAG_FROM_THE_INCOMING_AMBA_MSG_S %__name__)
            else:
                self._incomingMessageObject.requestType = str(requestType)

            '''----------------------------------------------------------------------------------------------------------
            Fetch the REQUEST_USER_ID attribute on the message
            ----------------------------------------------------------------------------------------------------------'''
            requestUserId = ambaUtils.get_AMBA_Object_Value(self.dataTag, UTILS.Constants.fcGenericConstants.REQUEST_USER_ID)
            if not requestUserId:
                UTILS.Logger.flogger.warn(UTILS.Constants.fcFloggerConstants.COULD_NOT_RETRIEVE_THE_REQUEST_USER_ID_TAG_FROM_INCOMING_AMBA_MSG_S %__name__)
            else:
                self._incomingMessageObject.requestUserId = str(requestUserId)

            '''----------------------------------------------------------------------------------------------------------
            Fetch the SCOPE_NAME attribute on the message
            ----------------------------------------------------------------------------------------------------------'''
            scopeName = ambaUtils.get_AMBA_Object_Value(self.dataTag, UTILS.Constants.fcGenericConstants.SCOPE_NAME)
            if not scopeName:
                UTILS.Logger.flogger.warn(UTILS.Constants.fcFloggerConstants.COULD_NOT_RETRIEVE_THE_SCOPE_NAME_TAG_FROM_INCOMING_AMBA_MSG_S %__name__)
            else:
                self._incomingMessageObject.scopeName = str(scopeName)

            '''----------------------------------------------------------------------------------------------------------
            Fetch the SCOPE_NUMBER attribute on the message
            ----------------------------------------------------------------------------------------------------------'''
            scopeNumber = ambaUtils.get_AMBA_Object_Value(self.dataTag, UTILS.Constants.fcGenericConstants.SCOPE_NUMBER)
            if not scopeNumber:
                UTILS.Logger.flogger.warn(UTILS.Constants.fcFloggerConstants.COULD_NOT_RETRIEVE_THE_SCOPE_NUMBER_TAG_FROM_INCOMING_AMBA_MSG_S %__name__)
            else:
                try:
                    self._incomingMessageObject.scopeNumber = int(scopeNumber)
                except:
                    self._incomingMessageObject.scopeNumber = 0

            '''----------------------------------------------------------------------------------------------------------
            Fetch the PORTFOLIO_NAME attribute on the message
            ----------------------------------------------------------------------------------------------------------'''
            portfolioName = ambaUtils.get_AMBA_Object_Value(self.dataTag, 'PORTFOLIO_NAME')
            if not scopeNumber:
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
            Fetch the TOPIC attribute on the message
            ----------------------------------------------------------------------------------------------------------'''
            topic = ambaUtils.get_AMBA_Object_Value(self.dataTag, UTILS.Constants.fcGenericConstants.TOPIC)
            if not topic:
                UTILS.Logger.flogger.warn(UTILS.Constants.fcFloggerConstants.COULD_NOT_RETRIEVE_THE_TOPIC_TAG_FROM_INCOMING_AMBA_MSG_S %__name__)
            else:
                self._incomingMessageObject.topic = topic

            '''----------------------------------------------------------------------------------------------------------
            Set the type of RequestResponseMessage object
            ----------------------------------------------------------------------------------------------------------'''
            self._incomingMessageObject.type = UTILS.Constants.fcGenericConstants.REQUEST_S %self._incomingMessageObject.requestType


            '''----------------------------------------------------------------------------------------------------------
            Fetch the BACKDATE_START attribute on the message
            ----------------------------------------------------------------------------------------------------------'''
            backDateStart = ambaUtils.get_AMBA_Object_Value(self.dataTag, "BACKDATE_START")
            if not backDateStart:
                UTILS.Logger.flogger.warn('Could not retrieve the "BACKDATE_START" value from the incoming amba message %s' %__name__)
            else:
                self._incomingMessageObject.backDateStart = FC_UTILS.formatDate(backDateStart)
        except Exception, e:
            UTILS.Logger.flogger.warn(str(e))
