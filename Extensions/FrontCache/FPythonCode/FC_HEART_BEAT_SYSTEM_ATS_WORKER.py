
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_HEART_BEAT_SYSTEM_ATS_WORKER
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module retreives the System statistics and saves it to the database.
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       XXXXXX
----------------------------------------------------------------------------------------------------------'''

'''----------------------------------------------------------------------------------------------------------
Importing Python modules
----------------------------------------------------------------------------------------------------------'''
import datetime, traceback

'''----------------------------------------------------------------------------------------------------------
Importing Custom modules
----------------------------------------------------------------------------------------------------------'''
from FC_UTILS import FC_UTILS as UTILS
import FC_ATS_WORKER_BASE as ATS_WORKER_BASE
from FC_HEART_BEAT_TIMER_SYSTEM import FC_HEART_BEAT_TIMER_SYSTEM as HEART_BEAT_TIMER_SYSTEM
from FC_EXCEPTION import FC_EXCEPTION as EXCEPTION

'''----------------------------------------------------------------------------------------------------------
Main Real Time ATS Worker Class. Contains the main Start, Stop and Work function for the ATS.
----------------------------------------------------------------------------------------------------------'''
class FC_HEART_BEAT_SYSTEM_ATS_WORKER(ATS_WORKER_BASE.FC_ATS_WORKER_BASE):
    def __init__(self):
        ATS_WORKER_BASE.FC_ATS_WORKER_BASE.__init__(self)
    
        try:
            self.heartBeatSystem = HEART_BEAT_TIMER_SYSTEM()
            UTILS.Logger.flogger.info('Heart Beat System Timer started at %s' %datetime.datetime.now())
        except Exception as e:
            UTILS.ErrorHandler.processError(None,\
                    EXCEPTION('Could not create a System Heart Beat in module %s.' %__name__, traceback, 'CRITICAL', e))
        

    def work(self):
        return
