
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_FLOGGER_SINGLETON
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module will expose the Logger instance that will be used for logging in
                                Front Cache as well as Logging Properties so that the Logger instance can be
                                Reinitialized. This Logger will be able to be accessed via FC_UTILS.
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Heinrich Cronje/Heinrich Momberg
CR NUMBER               :       XXXXXX
----------------------------------------------------------------------------------------------------------'''

'''----------------------------------------------------------------------------------------------------------
Importing all relevant Python modules.
----------------------------------------------------------------------------------------------------------'''
import FLogger

'''----------------------------------------------------------------------------------------------------------
Class containing the flogger object that will be used for logging.
----------------------------------------------------------------------------------------------------------'''
class FC_FLOGGER_SINGLETON(object):
    instance = None
    flogger = None
    
    class FC_FLOGGER_SINGLETON_HELPER:
        def __call__(self, *args, **kwargs):
            if FC_FLOGGER_SINGLETON.instance is None:
                object = FC_FLOGGER_SINGLETON()
                FC_FLOGGER_SINGLETON.instance = object
            return FC_FLOGGER_SINGLETON.instance
    
    Instance = FC_FLOGGER_SINGLETON_HELPER()

    def __init__(self):
        if not FC_FLOGGER_SINGLETON.instance == None:
            raise RuntimeError('Only one instance of FA_FLOGGER_SINGLETON is allowed!')
        else:
            self.flogger = FLogger.FLogger()
            self.__logLevel = self.LogLevel
            self.__keep = self.Keep
            self.__logOnce = self.LogOnce
            self.__logToConsole = self.LogToConsole
            self.__logToPrime = self.LogToPrime
            self.__logToFileAtSpecifiedPath = self.LogToFileAtSpecifiedPath
            self.__filters = self.Filters

    @property
    def Name(self):
        if self.flogger == None:
            return None
        return self.flogger.Name()
    
    @property
    def LogLevel(self):
        if self.flogger == None:
            return None
        return self.flogger.Level()
    
    @LogLevel.setter
    def LogLevel(self, value):
        if self.LogLevel != value:
            self.__logLevel = value

    @property
    def Keep(self):
        if self.flogger == None:
            return None
        return self.flogger.Keep()
    
    @Keep.setter
    def Keep(self, value):
        if self.Keep != value:
            self.__keep = value

    @property
    def LogOnce(self):
        if self.flogger == None:
            return None
        return self.flogger.LogOnce()
    
    @LogOnce.setter
    def LogOnce(self, value):
        if self.LogOnce != value:
            self.__logOnce = value

    @property
    def LogToConsole(self):
        if self.flogger == None:
            return None
        return self.flogger.LogToConsole()

    @LogToConsole.setter
    def LogToConsole(self, value):
        if self.LogToConsole != value:
            self.__logToConsole = value
    
    @property
    def LogToPrime(self):
        if self.flogger == None:
            return None
        return self.flogger.LogToPrime()

    @LogToPrime.setter
    def LogToPrime(self, value):
        if self.LogToPrime != value:
            self.__logToPrime = value
    
    @property
    def LogToFileAtSpecifiedPath(self):
        if self.flogger == None:
            return None
        return self.flogger.LogToFileAtSpecifiedPath()

    @LogToFileAtSpecifiedPath.setter
    def LogToFileAtSpecifiedPath(self, value):
        if self.LogToFileAtSpecifiedPath != value:
            self.__logToFileAtSpecifiedPath = value
    
    @property
    def Filters(self):
        if self.flogger == None:
            return None
        return self.flogger.Filters()

    @Filters.setter
    def Filters(self, value):
        if self.Filters != value:
            self.__filters = value

    '''----------------------------------------------------------------------------------------------------------
    If there is any need to change any property of the Logger, the properties should be set and then the
    Reinitialized fuctions should be called.
    ----------------------------------------------------------------------------------------------------------'''
    def Reinitialize(self):
        if self.flogger != None:
            try:
                self.flogger.Reinitialize(level = self.__logLevel,\
                                        keep = self.__keep,\
                                        logOnce = self.__logOnce,\
                                        logToConsole = self.__logToConsole,\
                                        logToPrime = self.__logToPrime,\
                                        logToFileAtSpecifiedPath = self.__logToFileAtSpecifiedPath,\
                                        filters  = self.__filters )
            except Exception as e:
                self.flogger.flogger.info('Could not Reinitialize the FLog object. Currenct settings will still apply...')
                self.flogger.flogger.info('Log Level : %s' %str(self.flogger.flogger.Level()))
                self.flogger.flogger.info('Keep : %s' %str(self.flogger.flogger.Keep()))
                self.flogger.flogger.info('Log Once : %s' %str(self.flogger.flogger.LogOnce()))
                self.flogger.flogger.info('Log To Console : %s' %str(self.flogger.flogger.LogToConsole()))
                self.flogger.flogger.info('Log To Prime : %s' %str(self.flogger.flogger.LogToPrime()))
                self.flogger.flogger.info('Log To File At Specified Path : %s' %str(self.flogger.flogger.LogToFileAtSpecifiedPath()))
                self.flogger.flogger.info('Filters : %s' %str(self.flogger.flogger.Filters()))
                self.flogger.flogger.info('ERROR in Reinitializing...')
                self.flogger.flogger.info('%s' %str(e))

'''
#Testing FLogger Songleton
#Print the default values of Flogger
print FC_FLOGGER_SINGLETON.Instance().Name
print FC_FLOGGER_SINGLETON.Instance().LogLevel
print FC_FLOGGER_SINGLETON.Instance().Keep
print FC_FLOGGER_SINGLETON.Instance().LogOnce
print FC_FLOGGER_SINGLETON.Instance().LogToConsole
print FC_FLOGGER_SINGLETON.Instance().LogToPrime
print FC_FLOGGER_SINGLETON.Instance().LogToFileAtSpecifiedPath
print FC_FLOGGER_SINGLETON.Instance().Filters
#set a specific property
FC_FLOGGER_SINGLETON.Instance().LogLevel = 2
#test that the original property value is not changes
print FC_FLOGGER_SINGLETON.Instance().LogLevel
#Reinitialize the flogger object to take the changes into concideration
FC_FLOGGER_SINGLETON.Instance().Reinitialize()
#Test that the new vlaue is applied on the FLog object
print FC_FLOGGER_SINGLETON.Instance().LogLevel
'''
