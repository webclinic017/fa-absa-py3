""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/FOperationsObservable.py"

#-------------------------------------------------------------------------
# Observable - Inherit to enable observers for an object
#-------------------------------------------------------------------------
class Observable(object):
    
    #-------------------------------------------------------------------------
    def __init__(self):
        super(Observable, self).__init__()
        self._observers = []
    
    #-------------------------------------------------------------------------
    def OO_AddObserver(self, observer):
        self._observers.append(observer)
        
    #-------------------------------------------------------------------------
    def OO_RemoveObservers(self):
        del self._observers[:]
            
    #-------------------------------------------------------------------------    
    def OO_NotifyObservers(self, callableName, *args):
        for observer in self._observers:
            getattr(observer, callableName)(*args)