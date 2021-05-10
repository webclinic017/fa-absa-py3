
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_HEART_BEAT_TIMER_PROCESS
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module will send a heart beat to the Front Cache Database with all the
                                relevant health stats of the ATS process that is running. Memory Consumption, 
                                CPU Usage, Type of messages expected and type it can send,...
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       XXXXXX
----------------------------------------------------------------------------------------------------------'''

'''----------------------------------------------------------------------------------------------------------
Importing all relevant Python modules.
----------------------------------------------------------------------------------------------------------'''
from threading import Timer as Timer
from datetime import datetime
import time

'''----------------------------------------------------------------------------------------------------------
Importing Custom Modules
----------------------------------------------------------------------------------------------------------'''
from FC_HEART_BEAT_OBJECT_PROCESS import FC_HEART_BEAT_OBJECT_PROCESS as HEART_BEAT_OBJECT_PROCESS
from FC_HEARTBEAT_PROCESS_REPOSITORY import FC_HEARTBEAT_PROCESS_REPOSITORY as HEARTBEAT_PROCESS_REPOSITORY
import FC_HEART_BEAT_TIMER_BASE as HEART_BEAT_TIMER_BASE
import FC_UTILS as FC_UTILS
from FC_UTILS import FC_UTILS as UTILS
import FC_DATA_HELPER as DATA_HELPER
import FC_ENUMERATIONS
'''----------------------------------------------------------------------------------------------------------
Class creating a timer from initialization and exposing a function to stop the timer.
----------------------------------------------------------------------------------------------------------'''
class FC_HEART_BEAT_TIMER_PROCESS(HEART_BEAT_TIMER_BASE.FC_HEART_BEAT_TIMER_BASE):
    def __init__(self):
        HEART_BEAT_TIMER_BASE.FC_HEART_BEAT_TIMER_BASE.__init__(self)
    
    def createHeartBeat(self):
        while self._stoppingTimer == False:
            heartBeatInfo = HEART_BEAT_OBJECT_PROCESS()
            #UTILS.Logger.flogger.info(datetime.now())
            dbProvider = DATA_HELPER.getSqlDBProvider()
            serviceComponentId = FC_ENUMERATIONS.ServiceComponent.fromstring(UTILS._componentName)
            heartBeatRepository = HEARTBEAT_PROCESS_REPOSITORY(dbProvider)
            heartBeatRepository.create(serviceComponentId)
            time.sleep(UTILS.Parameters.fcGenericParameters.HeartbeatTrackInterval)
        
        UTILS.Logger.flogger.info('Timer stopped at %s' %datetime.now())
        return
    
#Testing Timer
'''
import time
t = FC_HEART_BEAT_TIMER_PROCESS()
time.sleep(15)
t.stopTimer()
'''
