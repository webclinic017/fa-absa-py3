
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_REQT_PT_ATS_WORKER
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module will receive a Portfolio Trades Request. It will the send a response
                                to the response coordinating ATS detailing how many trades is expected. It
                                will then send a Request to the collection trade ATSs to retreive the trade detail.
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       XXXXXX
----------------------------------------------------------------------------------------------------------'''

'''----------------------------------------------------------------------------------------------------------
Importing Custom modules
----------------------------------------------------------------------------------------------------------'''
import FC_REQT_ATS_WORKER_BASE as REQT_ATS_WORKER_BASE
from FC_UTILS import FC_UTILS as UTILS
import FC_DATA_HELPER as DATA_HELPER
import FC_ENUMERATIONS
'''----------------------------------------------------------------------------------------------------------
Main Real Time ATS Worker Class. Contains the main Start, Stop and Work function for the ATS.
----------------------------------------------------------------------------------------------------------'''
class FC_REQT_PT_ATS_WORKER(REQT_ATS_WORKER_BASE.FC_REQT_ATS_WORKER_BASE):
    def __init__(self):
        REQT_ATS_WORKER_BASE.FC_REQT_ATS_WORKER_BASE.__init__(self)
    def GetControlMeasureAttribute(self):
        return UTILS.Parameters.fcComponentParameters.componentControlMeasureFlag        
    def getLastProcessedMessageId(self):
        self.last_processed_messageId, self.requestId, self.retryCount = DATA_HELPER.GetLastProcessedMessageInfo(FC_ENUMERATIONS.ServiceComponent.fromstring(UTILS.ComponentName))
    def registerMessageId(self):
        DATA_HELPER.RegisterMessageId(FC_ENUMERATIONS.ServiceComponent.fromstring(UTILS.ComponentName), self.currentMessageId, self.incomingMessageObject.requestId)
