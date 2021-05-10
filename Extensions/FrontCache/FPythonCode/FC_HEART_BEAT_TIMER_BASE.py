
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_HEART_BEAT_TIMER_BASE
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       Tis module will is the base of the heart beat monitor the the Front Cache ATSs.
                                The __createHeartBeat method needs to be overridden to get the desired functionality
                                of different heart beats.
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       XXXXXX
----------------------------------------------------------------------------------------------------------'''

'''----------------------------------------------------------------------------------------------------------
Importing all relevant Python modules.
----------------------------------------------------------------------------------------------------------'''
from threading import Timer as Timer
import datetime, time, threading

'''----------------------------------------------------------------------------------------------------------
Importing Custom Modules
----------------------------------------------------------------------------------------------------------'''
from FC_HEART_BEAT_OBJECT_PROCESS import FC_HEART_BEAT_OBJECT_PROCESS as HEART_BEAT_OBJECT_PROCESS
from FC_UTILS import FC_UTILS as UTILS

'''----------------------------------------------------------------------------------------------------------
Class creating a timer from initialization and exposing a function to stop the timer.
----------------------------------------------------------------------------------------------------------'''
class FC_HEART_BEAT_TIMER_BASE():
    def __init__(self):
        self._timer = None
        self._stoppingTimer = False
        self.createTimer()
    
    def createHeartBeat(self):
        raise NotImplementedError('The method __createHeartBeat in module %s needs to be implemented.' %__name__)

    def createTimer(self):
        if not self._stoppingTimer:
            if self._timer != None:
                self._timer = None
            #self._timer = Timer(UTILS.Parameters.fcGenericParameters.HeartbeatTrackInterval, self.createHeartBeat)
            #self.startTimer()
            hbThread = threading.Thread(name='HeartBeat_Daemon', target = self.createHeartBeat)
            hbThread.setDaemon(True)
            hbThread.start()
    
    def startTimer(self):
        if self._timer:
            self._timer.start()
            
    def stopTimer(self):
        self._stoppingTimer = True
        '''if self._timer:
            UTILS.Logger.flogger.info('Stopping timer at %s' %datetime.datetime.now())
            #self._timer.cancel()
            self._timer = None
            UTILS.Logger.flogger.info('Timer stopped')
        '''
