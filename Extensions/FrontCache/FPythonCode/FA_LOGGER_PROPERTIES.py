
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FA_LOGGER_PROPERTIES
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module containis the properties of the FLogger object used for logging
                                messages
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       XXXXXX
----------------------------------------------------------------------------------------------------------'''

class FA_FLOGGER_PROPERTIES(object):
    def __init__(self, name, level, keep, logOnce, logToConsole, logToPrime, logToFileAtSpecificPath, logToFileAtDefaultPath, filters):
        self._name = name
        self._level = level
        self._keep = keep
        self._logOnce = logOnce
        self._logToConsole = logToConsole
        self._logToPrime = logToPrime
        self._logToFileAtSpecificPath = logToFileAtSpecificPath
        self._logToFileAtDefaultPath = logToFileAtDefaultPath
        self._filters = filters

    @property
    def name(self):
        return self._name
        
    @property
    def level(self):
        return self._level
        
    @property
    def keep(self):
        return self._keep
        
    @property
    def logOnce(self):
        return self._logOnce
        
    @property
    def logToConsole(self):
        return self._logToConsole
        
    @property
    def logToPrime(self):
        return self._logToPrime
        
    @property
    def logToFileAtSpecificPath(self):
        return self._logToFileAtSpecificPath
    
    @property
    def logToFileAtDefaultPath(self):
        return self._logToFileAtDefaultPath
        
    @property
    def filters(self):
        return self._filters
