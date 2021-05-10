""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/ArenaExcel/etc/ConnectionInterface.py"
import acm
import time

from SingleValueTask import TaskInterface, TaskArguments

class ConnectionArguments(TaskArguments):

    def __init__(self, *args):
        super(ConnectionArguments, self).__init__(*args)
        
    @property
    def UpdateFreq(self):
        try:
            return int(self.Get(0))
        except TypeError:
            return 2        
        

class Heartbeat(TaskInterface):

    def __init__(self, *args):
        conectionArgs = ConnectionArguments(*args)
        self._updateFrequency = conectionArgs.UpdateFreq
        self._lastUpdate = time.time()
        
    def Result(self):
        return 'Latest update received at {0}'.format(acm.Time.TimeNow().split('.')[0])
        
    def HasPendingResult(self):
        timeNow = time.time()
        if timeNow - self._lastUpdate > self._updateFrequency:
            self._lastUpdate = timeNow
            return True
        return False
