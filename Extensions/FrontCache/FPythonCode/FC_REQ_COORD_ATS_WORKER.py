
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_REQ_COORD_ATS_WORKER
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module is the base module for all Request Coordinating ATSs. It will connect to the
                                AMB and process Requests events from real time, EOD and intraday event triggers. This
                                ATS will distribute the REQUEST messages to the appropriate REQUEST TYPE ATSs.
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       XXXXXX
----------------------------------------------------------------------------------------------------------'''

'''----------------------------------------------------------------------------------------------------------
Importing Custom Modules
----------------------------------------------------------------------------------------------------------'''
import FC_UTILS as FC_UTILS
import FC_ENUMERATIONS
from FC_UTILS import FC_UTILS as UTILS
from FC_MESSAGE_PROCESS_REQUEST import FC_MESSAGE_PROCESS_REQUEST as MESSAGE_PROCESS_REQUEST
from FC_MESSAGE_OBJECT_REQUEST import FC_MESSAGE_OBJECT_REQUEST as MESSAGE_OBJECT_REQUEST
import FC_ATS_WORKER_BASE as ATS_WORKER_BASE
import FC_DATA_HELPER as DATA_HELPER

'''----------------------------------------------------------------------------------------------------------
Main Real Time ATS Worker Class. Overrides specific methods from the Base Class.
----------------------------------------------------------------------------------------------------------'''
class FC_REQ_COORD_ATS_WORKER(ATS_WORKER_BASE.FC_ATS_WORKER_BASE):
    def __init__(self):
        ATS_WORKER_BASE.FC_ATS_WORKER_BASE.__init__(self)

    def mapIncomingAMBAMessageToIncomingMessageObject(self):
        '''----------------------------------------------------------------------------------------------------------
        The AMBA message will be validated and an IncomingMessageObject will be created which will contain all 
        detail needed to process the incoming message further.
        ----------------------------------------------------------------------------------------------------------'''
        self.incomingMessageObject = MESSAGE_OBJECT_REQUEST()
        
        MESSAGE_PROCESS_REQUEST(self.incomingAMBAMessageData, self.incomingMessageObject)

    def registerMessageId(self):
        DATA_HELPER.RegisterMessageId(FC_ENUMERATIONS.ServiceComponent.fromstring(UTILS.ComponentName), self.currentMessageId, self.incomingMessageObject.requestId)

    def getLastProcessedMessageId(self):
        self.last_processed_messageId, self.requestId, self.retryCount  = DATA_HELPER.GetLastProcessedMessageInfo(FC_ENUMERATIONS.ServiceComponent.fromstring(UTILS.ComponentName))

    def processIncommingAMBAMessage(self):
        if (self.last_processed_messageId == self.currentMessageId):
            self._recovery_mode = True #Issue has occured and the message should not be reprocessed. Manual fixing may occur
            UTILS.Logger.flogger.info("Ats is attempting to reprocess amb messageId %s" % self.currentMessageId)
            UTILS.Logger.flogger.info("Ats will enter into recovery mode for the RequestId")
        self.incomingMessageObject.requestId = DATA_HELPER.RegisterRequest(self.incomingMessageObject, self._recovery_mode)
        self.registerMessageId()

        #self.setHeartBeatCandidateComponent('REQ_COORD') #_AL
        return
    
    def createOutgoingMessageObjects(self):
        outgoingMessageObject = MESSAGE_OBJECT_REQUEST()
        outgoingMessageObject.ambaTxNbr = self.incomingMessageObject.ambaTxNbr
        outgoingMessageObject.batchId = self.incomingMessageObject.batchId
        outgoingMessageObject.isEOD = self.incomingMessageObject.isEOD
        outgoingMessageObject.reportDate = FC_UTILS.dateTimeStringFromISODateTimeString(self.incomingMessageObject.reportDate)
        outgoingMessageObject.requestDateTime = FC_UTILS.dateTimeStringFromISODateTimeString(self.incomingMessageObject.requestDateTime)
        outgoingMessageObject.requestEventType = self.incomingMessageObject.requestEventType
        outgoingMessageObject.isDateToday = self.incomingMessageObject.isDateToday
        outgoingMessageObject.requestId = self.incomingMessageObject.requestId
        outgoingMessageObject.requestSource = self.incomingMessageObject.requestSource
        outgoingMessageObject.requestType = self.incomingMessageObject.requestType
        outgoingMessageObject.requestUserId = self.incomingMessageObject.requestUserId
        outgoingMessageObject.scopeName = self.incomingMessageObject.scopeName
        outgoingMessageObject.scopeNumber = self.incomingMessageObject.scopeNumber    
        #outgoingMessageObject.senderSubject = 'SenderSubject'
        outgoingMessageObject.topic = self.incomingMessageObject.topic
        outgoingMessageObject.type = self.incomingMessageObject.type
        outgoingMessageObject.backDateStart = self.incomingMessageObject.backDateStart
        self.outgoingAMBADataDictionaries.append((outgoingMessageObject.type, outgoingMessageObject.mapMessageObjectToAMBADataDictionary()))

