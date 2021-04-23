
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FA_LOGGER_SINGLETON
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module producess only one instace of FLogger that can be used throughout
                                the program. No need to pass it any parameters again.
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       XXXXXX
----------------------------------------------------------------------------------------------------------'''

'''----------------------------------------------------------------------------------------------------------
Importing Front Arena and Python modules needed for Real Time ATS Worker.
----------------------------------------------------------------------------------------------------------'''
try:
    import FLogger
except ImportError, e:
    raise Exception('Import Error in module %s.' %__name__, e)

class FA_FLOGGER_SINGLETON:
    instance = None
    flogger = None
    floggerProperties = None
    
    class FA_FLOGGER_HELPER:
        def __call__(self, *args, **kwargs):
            if FA_FLOGGER_SINGLETON.instance is None:
                object = FA_FLOGGER_SINGLETON()
                FA_FLOGGER_SINGLETON.instance = object
                try:
                    FA_FLOGGER_SINGLETON.flogger = FLogger.FLogger(FA_FLOGGER_SINGLETON.floggerProperties.name,\
                        FA_FLOGGER_SINGLETON.floggerProperties.level, FA_FLOGGER_SINGLETON.floggerProperties.keep,\
                        FA_FLOGGER_SINGLETON.floggerProperties.logOnce, FA_FLOGGER_SINGLETON.floggerProperties.logToConsole,\
                        FA_FLOGGER_SINGLETON.floggerProperties.logToPrime, FA_FLOGGER_SINGLETON.floggerProperties.logToFileAtSpecificPath,\
                        FA_FLOGGER_SINGLETON.floggerProperties.filters)
                except:
                    FA_FLOGGER_SINGLETON.flogger = FLogger.FLogger(FA_FLOGGER_SINGLETON.floggerProperties.name,\
                        FA_FLOGGER_SINGLETON.floggerProperties.level, FA_FLOGGER_SINGLETON.floggerProperties.keep,\
                        FA_FLOGGER_SINGLETON.floggerProperties.logOnce, FA_FLOGGER_SINGLETON.floggerProperties.logToConsole,\
                        FA_FLOGGER_SINGLETON.floggerProperties.logToPrime, FA_FLOGGER_SINGLETON.floggerProperties.logToFileAtDefaultPath,\
                        FA_FLOGGER_SINGLETON.floggerProperties.filters)
                    
            return FA_FLOGGER_SINGLETON.instance
    
    getFloggerInstance = FA_FLOGGER_HELPER()
    
    def __init__(self):
        if not FA_FLOGGER_SINGLETON.instance == None : 
            raise RuntimeError('Only one instance of FA_FLOGGER_SINGLETON is allowed!')

    @property
    def FLoggerObject(self):
        return self.flogger

    @property
    def floggerProperties(self):
        return self.floggerProperties
        
    @floggerProperties.setter
    def floggerProperties(self, value):
        self.floggerProperties = value
