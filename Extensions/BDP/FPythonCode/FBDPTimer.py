""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/common/FBDPTimer.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
""" ---------------------------------------------------------------------------
MODULE
    FBDPTimer.

    Simple timer class FExpiration, FDeleteInstruments and FArchiveInstruments

DESCRIPTION
    
    

----------------------------------------------------------------------------"""

import time

class Timer():

    def __init__(self, maxRunTime, log):
        if maxRunTime:
            self.maxRunTime = maxRunTime
        else:
            self.maxRunTime = 3600
        self.log = log

    def start(self, maxRunTime = None):

        self.__endTime = None
        if self.maxRunTime and self.maxRunTime > 0.0:
            self.__endTime = time.time() + self.maxRunTime
            self.log.logInfo('Setting maximum run time to {0}s'.format(
                     self.maxRunTime))
            self.log.logInfo('Will terminate after {0}'.format(time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime(self.__endTime))))

    def hasAlarmed(self):

        if not self.__endTime:
            return False
        if time.time() > self.__endTime:
            self.log.logInfo('Terminated at {0}. '
                    'Exceeded max runtime.'.format(time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime(time.time()))))
            return True
        else:
            return False
