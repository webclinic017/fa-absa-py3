
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_HEART_BEAT_TIMER_SYSTEM
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module will send a heart beat to the Front Cache Database with all the
                                relevant health stats of the box where the ATS is running. Memory Consumption, 
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
import datetime

'''----------------------------------------------------------------------------------------------------------
Importing Custom Modules
----------------------------------------------------------------------------------------------------------'''
from FC_HEART_BEAT_OBJECT_SYSTEM import FC_HEART_BEAT_OBJECT_SYSTEM as HEART_BEAT_OBJECT_SYSTEM
import FC_HEART_BEAT_TIMER_BASE as HEART_BEAT_TIMER_BASE

'''----------------------------------------------------------------------------------------------------------
Class creating a timer from initialization and exposing a function to stop the timer.
----------------------------------------------------------------------------------------------------------'''
class FC_HEART_BEAT_TIMER_SYSTEM(HEART_BEAT_TIMER_BASE.FC_HEART_BEAT_TIMER_BASE):
    def __init__(self):
        HEART_BEAT_TIMER_BASE.FC_HEART_BEAT_TIMER_BASE.__init__(self)
    
    def createHeartBeat(self):
        heartBeatInfo = HEART_BEAT_OBJECT_SYSTEM()
        print('TimerSystem: ' + datetime.datetime.now())
        self.createTimer()
    
'''
#Testing Timer
import time
t = FC_HEART_BEAT_TIMER_SYSTEM()
time.sleep(15)
t.stopTimer()
'''
