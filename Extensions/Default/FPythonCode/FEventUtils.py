""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/AMUtils/./etc/FEventUtils.py"
"""--------------------------------------------------------------------------
MODULE
    FEventUtils

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    
-----------------------------------------------------------------------------"""

from FAssetManagementUtils import logger


class Observer(object):
    
    def Update(self, subject, aspect, param):
        pass
        
        
class Observable(object):

    def __init__(self):
        self._observers = []
        
    def AddObserver(self, observer):
        if observer not in self._observers:
            logger.debug('Adding observer {0} to observer list'.format(observer))
            if not self.IsObserved():
                self.OnObservableStart()
            self._observers.append(observer)
            
    def RemoveObserver(self, observer):
        if observer in self._observers:
            logger.debug('Removing observer {0} from observer list'.format(observer))
            self._observers.remove(observer)
            if not self.IsObserved():
                self.OnObservableEnd()

    def IsObserved(self):
        return bool(self._observers)
            
    def NotifyObservers(self, aspect, param):
        for observer in self.Observers():
            try:
                logger.debug('Notifying {0} with {1} {2} {3}'.format(observer, self, aspect, param))
                observer.Update(self, aspect, param)
            except Exception as err:
                logger.error(err, exc_info=True)                    
            
    def Observers(self):
        return self._observers
        
    def Update(self, sender, aspect, param):
        self.NotifyObservers(aspect, param)

    def OnObservableStart(self):
        pass

    def OnObservableEnd(self):
        pass