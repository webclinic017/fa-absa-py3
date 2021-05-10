
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_REQT_ST_ATS_WORKER
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module will receive a Single Trade Request. It will the send a response
                                to the response coordinating ATS detailing how many trades are expected. It
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
'''----------------------------------------------------------------------------------------------------------
Main Real Time ATS Worker Class. Contains the main Start, Stop and Work function for the ATS.
----------------------------------------------------------------------------------------------------------'''
class FC_REQT_ST_ATS_WORKER(REQT_ATS_WORKER_BASE.FC_REQT_ATS_WORKER_BASE):
    def __init__(self):
        REQT_ATS_WORKER_BASE.FC_REQT_ATS_WORKER_BASE.__init__(self)
        
    def GetControlMeasureAttribute(self):
        return UTILS.Parameters.fcComponentParameters.componentControlMeasureFlag

    def registerMessageId(self):
        return
