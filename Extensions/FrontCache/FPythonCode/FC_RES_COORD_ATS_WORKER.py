
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_RES_COORD_ATS_WORKER
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module is the base module for the Response Coordinating ATSs. It will connect to the
                                AMB and process Response events from various Request Type and Collection ATSs. This
                                ATS will distribute the EVENT_RESPONSE messages to the AMB where subscribers will be notified
                                the status of requests.
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       XXXXXX
----------------------------------------------------------------------------------------------------------'''

'''----------------------------------------------------------------------------------------------------------
Importing Custom Modules
----------------------------------------------------------------------------------------------------------'''
import FC_UTILS as FC_UTILS
from FC_MESSAGE_PROCESS_RESPONSE import FC_MESSAGE_PROCESS_RESPONSE as MESSAGE_PROCESS_RESPONSE
from FC_MESSAGE_OBJECT_RESPONSE import FC_MESSAGE_OBJECT_RESPONSE as MESSAGE_OBJECT_RESPONSE
import FC_ATS_WORKER_BASE as ATS_WORKER_BASE

'''----------------------------------------------------------------------------------------------------------
Main Real Time ATS Worker Class. Contains the main Start, Stop and Work function for the ATS.
----------------------------------------------------------------------------------------------------------'''
class FC_RES_COORD_ATS_WORKER(ATS_WORKER_BASE.FC_ATS_WORKER_BASE):
    def __init__(self):
        ATS_WORKER_BASE.FC_ATS_WORKER_BASE.__init__(self)
    
    def mapIncomingAMBAMessageToIncomingMessageObject(self):
        '''----------------------------------------------------------------------------------------------------------
        The AMBA message will be validated and an IncomingMessageObject will be created which will contain all 
        detail needed to process the incoming message further.
        ----------------------------------------------------------------------------------------------------------'''
        self.incomingMessageObject = MESSAGE_OBJECT_RESPONSE()
        
        MESSAGE_PROCESS_RESPONSE(self.incomingAMBAMessageData, self.incomingMessageObject)

    def CreateConfirmationOfSentEndMessage(self):
        return
            
    def processIncommingAMBAMessage(self):
        return
    
    def createOutgoingMessageObjects(self):
        outgoingMessageObject = MESSAGE_OBJECT_RESPONSE()
        outgoingMessageObject.ambaTxNbr = self.incomingMessageObject.ambaTxNbr
        outgoingMessageObject.batchId = self.incomingMessageObject.batchId
        outgoingMessageObject.isEOD = self.incomingMessageObject.isEOD
        outgoingMessageObject.reportDate = FC_UTILS.dateTimeStringFromISODateTimeString(self.incomingMessageObject.reportDate)
        outgoingMessageObject.requestDateTime = FC_UTILS.dateTimeStringFromISODateTimeString(self.incomingMessageObject.requestDateTime)
        outgoingMessageObject.requestEventType = self.incomingMessageObject.requestEventType
        outgoingMessageObject.requestId = self.incomingMessageObject.requestId
        outgoingMessageObject.requestSource = self.incomingMessageObject.requestSource
        outgoingMessageObject.requestType = self.incomingMessageObject.requestType
        outgoingMessageObject.requestUserId = self.incomingMessageObject.requestUserId
        outgoingMessageObject.scopeName = self.incomingMessageObject.scopeName
        outgoingMessageObject.scopeNumber = self.incomingMessageObject.scopeNumber
        outgoingMessageObject.topic = self.incomingMessageObject.topic
        outgoingMessageObject.type = 'EVENT_RESPONSE'
        outgoingMessageObject.responseType = self.incomingMessageObject.responseType
        outgoingMessageObject.expectedObjectCount = self.incomingMessageObject.expectedObjectCount
        self.outgoingAMBADataDictionaries.append((outgoingMessageObject.type, outgoingMessageObject.mapMessageObjectToAMBADataDictionary()))   
