
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_RT_ATS_WORKER
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module is the base module for all Real Time ATSs. It will connect to the
                                AMB and prcess Real Time events from Front Arena and transform them into request
                                messages.
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       XXXXXX
----------------------------------------------------------------------------------------------------------'''

'''----------------------------------------------------------------------------------------------------------
Importing Custom modules
----------------------------------------------------------------------------------------------------------'''
import FC_UTILS as FC_UTILS
from FC_RT_MESSAGE_PROCESS import FC_RT_MESSAGE_PROCESS as RT_MESSAGE_PROCESS
from FC_MESSAGE_OBJECT_REQUEST import FC_MESSAGE_OBJECT_REQUEST as MESSAGE_OBJECT_REQUEST
import FC_ATS_WORKER_BASE as ATS_WORKER_BASE

'''----------------------------------------------------------------------------------------------------------
Main Real Time ATS Worker Class. Contains the main Start, Stop and Work function for the ATS.
----------------------------------------------------------------------------------------------------------'''
class FC_RT_ATS_WORKER(ATS_WORKER_BASE.FC_ATS_WORKER_BASE):
    def __init__(self):
        ATS_WORKER_BASE.FC_ATS_WORKER_BASE.__init__(self)

    def getLastProcessedMessageId(self):
        pass

    def mapIncomingAMBAMessageToIncomingMessageObject(self):
        '''----------------------------------------------------------------------------------------------------------
        The AMBA message will be validated and an IncomingMessageObject will be created which will contain all 
        detail needed to process the incoming message further.
        ----------------------------------------------------------------------------------------------------------'''
        self.incomingMessageObject = MESSAGE_OBJECT_REQUEST()
        
        RT_MESSAGE_PROCESS(self.incomingAMBAMessageData, self.incomingMessageObject)
        
    def processIncommingAMBAMessage(self):
        return

    def CreateConfirmationOfSentEndMessage(self):
        return

    def createOutgoingMessageObjects(self):
        outgoingMessageObject = MESSAGE_OBJECT_REQUEST()
        outgoingMessageObject.ambaTxNbr = self.incomingMessageObject.ambaTxNbr
        outgoingMessageObject.batchId = self.incomingMessageObject.batchId
        outgoingMessageObject.isEOD = self.incomingMessageObject.isEOD
        outgoingMessageObject.reportDate = FC_UTILS.getCorrectReportDate(str(FC_UTILS.dateTimeStringFromISODateTimeString(self.incomingMessageObject.reportDate)))
        outgoingMessageObject.requestDateTime = FC_UTILS.dateTimeStringFromISODateTimeString(self.incomingMessageObject.requestDateTime)
        outgoingMessageObject.requestEventType = self.incomingMessageObject.requestEventType
        outgoingMessageObject.requestId = self.incomingMessageObject.requestId
        outgoingMessageObject.requestSource = self.incomingMessageObject.requestSource
        outgoingMessageObject.requestType = self.incomingMessageObject.requestType
        outgoingMessageObject.requestUserId = self.incomingMessageObject.requestUserId
        outgoingMessageObject.scopeName = self.incomingMessageObject.scopeName
        outgoingMessageObject.scopeNumber = self.incomingMessageObject.scopeNumber
        outgoingMessageObject.topic = self.incomingMessageObject.topic
        outgoingMessageObject.type = self.incomingMessageObject.type
        outgoingMessageObject.backDateStart = self.incomingMessageObject.backDateStart
        self.outgoingAMBADataDictionaries.append((outgoingMessageObject.type, outgoingMessageObject.mapMessageObjectToAMBADataDictionary()))

    def registerMessageId(self):
        return
