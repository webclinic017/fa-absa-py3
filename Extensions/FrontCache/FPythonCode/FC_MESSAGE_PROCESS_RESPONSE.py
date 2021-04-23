
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_MESSAGE_PROCESS_RESPONSE
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module process a RESPONSE message from the AMB and tranform it into a
                                Response Object
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       XXXXXX
----------------------------------------------------------------------------------------------------------'''

'''----------------------------------------------------------------------------------------------------------
Importing Custom Modules
----------------------------------------------------------------------------------------------------------'''
from FC_UTILS import FC_UTILS as UTILS
from AMBA_Helper_Functions import AMBA_Helper_Functions as ambaUtils
import FC_MESSAGE_PROCESS_BASE as MESSAGE_PROCESS_BASE

'''----------------------------------------------------------------------------------------------------------
Response Message Process Type Class. This class will check if the mandatory fields are present on the incoming AMB
message and create an incoming message object.
----------------------------------------------------------------------------------------------------------'''
class FC_MESSAGE_PROCESS_RESPONSE(MESSAGE_PROCESS_BASE.FC_MESSAGE_PROCESS_BASE):
    def __init__(self, incomingAMBAMessageData, incomingMessageObject):
        MESSAGE_PROCESS_BASE.FC_MESSAGE_PROCESS_BASE.__init__(self, incomingAMBAMessageData, incomingMessageObject)
        self.__mapResponseMessageAttributes()
        
    def __mapResponseMessageAttributes(self):
        '''----------------------------------------------------------------------------------------------------------
        Fetch the EXPECTED_OBJECT_COUNT attribute on the message
        ----------------------------------------------------------------------------------------------------------'''
        expectedObjectCount = ambaUtils.get_AMBA_Object_Value(self.dataTag, UTILS.Constants.fcGenericConstants.EXPECTED_OBJECT_COUNT)
        if not expectedObjectCount:
            UTILS.Logger.flogger.warn(UTILS.Constants.fcFloggerConstants.COULD_NOT_RETRIEVE_EXPECTED_OBJ_COUNT_TAG_FROM_INCOMING_AMBA_MSG_S %__name__)
        else:
            self._incomingMessageObject.expectedObjectCount = expectedObjectCount

        '''----------------------------------------------------------------------------------------------------------
        Fetch the REPLAY attribute on the message
        ----------------------------------------------------------------------------------------------------------'''
        replay = ambaUtils.get_AMBA_Object_Value(self.dataTag, UTILS.Constants.fcGenericConstants.REPLAY)
        if replay:
            self._incomingMessageObject.replay = str(replay)

        '''----------------------------------------------------------------------------------------------------------
        Fetch the RESPONSE_TYPE attribute on the message
        ----------------------------------------------------------------------------------------------------------'''
        responseType = ambaUtils.get_AMBA_Object_Value(self.dataTag, UTILS.Constants.fcGenericConstants.RESPONSE_TYPE)
        if not responseType:
            UTILS.Logger.flogger.warn(UTILS.Constants.fcFloggerConstants.COULD_NOT_RETRIEVE_RESPONSE_TYPE_TAG_FROM_INCOMING_AMBA_MSG_S %__name__)
        else:
            self._incomingMessageObject.responseType = responseType
