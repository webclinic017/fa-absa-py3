from __future__ import print_function
"""---------------------------------------------------------------------------------
 MODULE
     FLogger - Class for logging
     
     (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.
     
     Parameters:
     The logger can instantiated using the FLogger class constructor and can be reinitialized 
         using the Reinitialize() method. The parameters to the constructor are below. With the
         exception of name and lock, they are also the parameters to Reinitialize.
         
         name - String parameter: name of the logger. loggers with 
                different names will be indepenedent.
         
         level - Integer parameter: 1 for normal logging, 2 for debug logging, 3 for warning
                 level and above, and 4 for error level and above.
         
         keep - Boolean parameter: if True log messages will be saved in a set. The
                size of the set it controlled by module level variables.
         
         logOnce - Boolean parameter: if True log messages will be saved in a set and
                   used to filter out duplicate messages using the Filter class.
         
         logToConsole - Boolean parameter: if True log messages will be logged to
                        sys.stdout.  
                         
         logToPrime - Boolean parameter: if True log messages will be logged to
                      ael.log.
                      
         logToFileAtSpecifiedPath - String parameter: name of a file where messages 
                                    should be logged (i.e. 'c:\log.txt'), else False.          
         
         filters - List parameter: list of filter objects. Filter objects should
                   follow protocol defined by the Python 'logging' module, alse None.
         
     
     Reinitialize Parameter:
     The paramters to Reinitialize are the same as above except there is no name parameter and one additional 
     parameter, lock:
     
         lock - Boolean parameter: if True, subsequent calls to the constructor will not
                    affect the logger behavior unless lock is set to False.
     
     Usage:
     To use FLogger you must obtain an instance of the logger via the FLogger constructor.
     The constructor uses the default values at the top of the module for the parameters
     not provided.    
         
     The FLogger class is designed as a shared state class insuring that all logger objects 
     (existing and new) always share the same state if the have the same name.
     
     The logger for a given name can be reintialized via the Reinitialize() method.  
     
     One can reinitialize it at any time. The state of all existing logger objects with the 
     same name are automatically updated to reflect the new state of the logger. 
     
     Logging should be done through the interface functions:
         
         LOG      - information
         WLOG     - warnings
         ELOG     - errors
         DLOG     - debug information
         CLOG     - critical information
         
         or 
         
         info     - information
         warn     - warnings
         error    - errors
         debug    - debug information
         critical - critical information
     
     Example Usage:
     import FLogger
     
     logger = FLogger.FLogger()
     
     logger.LOG('log something using the defualt settings')
     logger.Reintialize(level=2, logOnce=True) #change the default settings
     logger.LOG('log something using the new settings')
     logger.Reinitialize(logToFileAtSpecifiedPath='c:\\temp\\log.txt') #change current state
     logger.LOG('log something using the new settings')
     
     Modifications to This Module:
     Application specific changes should never be made to this module. If application specific
     changes are needed then consider creating wrapper functions in another module that call
     functions from FLogger, or inherit from the FLogger class and define new functionality in
     the derived class.     
     
     Getting Tracebacks:
     To get tracebacks use the exc_info keyword parameter as follows:
     
     try:
         x = 1/0
     except ZeroDivisionError as e:
         logger.ELOG('an error occured: %s ' % e, exc_info=1)
     
     **exc_info is the only possible keyword argument
                          
     See more example at bottom.
     Written by Matthew Schaefer, Sungard FRONT ARENA     
------------------------------------------------------------------------------------"""
_version_ = '0.0.9'

import os
import sys
try:
    import threading
except ImportError:
    threading = None
import logging
import types

#default logging parameters
default_name                        = 'FLogger'
default_level                       = 1
default_keep                        = False
default_logOnce                     = False
default_logToConsole                = True
default_logToPrime                  = False
default_logToFileAtSpecifiedPath    = False
default_filters                     = None
default_logpath                     = "c:\\temp\\"


#max storage for message sets
maxInfoSetSize = 200
maxDebugInfoSetSize = 200
maxWarningSetSize = 200
maxErrorSetSize = 200
maxCriticalSetSize = 200

#_lock is used to serialize the construction of FLogger objects.
_lock = None

def _acquireLock():
    """Acquire the module-level lock for serializing access to shared data. This
    should be released with _releaseLock()"""
    global _lock
    if (not _lock) and threading:
        _lock = threading.RLock()
    if _lock:
        _lock.acquire()

def _releaseLock():
    """Release the module-level lock acquired by calling _acquireLock()"""
    if _lock:
        _lock.release()

class FLogger( object ):
    """Class that wraps Logger class objects"""
    
    LOGGERS = {}

    INFO = 'INFO'
    ERROR = 'ERROR'
    WARNING = 'WARNING'
    DEBUG = 'DEBUG'
    CRITICAL = 'CRITICAL'
    ALL = 'ALL'
        
    def __init__( self, name=default_name, level=default_level, keep=default_keep, logOnce=default_logOnce, \
                  logToConsole=default_logToConsole, logToPrime=default_logToPrime, \
                  logToFileAtSpecifiedPath=default_logToFileAtSpecifiedPath, filters=default_filters ):
          
          if not isinstance(name, str): raise TypeError("logger name must be a string")
          self.name = name
          self.lock = False

          _acquireLock()
          try:
              flogger = self.LOGGERS.get( name )
              if not flogger:
                  self.logger = Logger( name, level, keep, logOnce, logToConsole, logToPrime, logToFileAtSpecifiedPath, filters )
                  self.LOGGERS[ self.name ] = self
              else:
                  if flogger.lock == False: 
                      self.logger = flogger.logger.Reinitialize( level, keep, logOnce, logToConsole, logToPrime, logToFileAtSpecifiedPath, filters )
                  else:
                      self.logger = flogger 
          finally:
              _releaseLock()
                
    def Reinitialize( self, level=None, keep=None, logOnce=None, \
                  logToConsole=None, logToPrime=None, logToFileAtSpecifiedPath=None \
                  ,filters=None, lock=None ):
        """Reinitializes the logger object based on given parameters and returns logger instance"""
        if lock is not None:
            flogger = self.LOGGERS.get( self.name )
            flogger.lock = lock
        return self.logger.Reinitialize( level, keep, logOnce, logToConsole, logToPrime, logToFileAtSpecifiedPath, filters )
        
    def LOG( self, msg, *args, **kwargs ):
        """
        Log 'msg % args' with severity 'INFO'.
    
        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.
    
        logger.LOG("Houston, we have a %s", "interesting problem", exc_info=1)
        """
        self.logger.LOG( msg, *args, **kwargs )
            
    def DLOG( self, msg, *args, **kwargs ):
        """
        Log 'msg % args' with severity 'DEBUG'.
    
        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.
    
        logger.DLOG("Houston, we have a %s", "thorny problem", exc_info=1)
        """
        self.logger.DLOG( msg, *args, **kwargs )
        
    def WLOG( self, msg, *args, **kwargs ):
        """
        Log 'msg % args' with severity 'WARNING'.
    
        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.
    
        logger.WLOG("Houston, we have a %s", "bit of a problem", exc_info=1)
        """
        self.logger.WLOG( msg, *args, **kwargs )
        
    def ELOG( self, msg, *args, **kwargs ):
        """
        Log 'msg % args' with severity 'ERROR'.
    
        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.
    
        logger.ELOG("Houston, we have a %s", "major problem", exc_info=1)
        """
        self.logger.ELOG( msg, *args, **kwargs )
    
    def CLOG( self, msg, *args, **kwargs ):
        """
        Log 'msg % args' with severity 'CRITICAL'.
    
        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.
    
        logger.CLOG("Houston, we have a %s", "bad problem", exc_info=1)
        """
        self.logger.CLOG( msg, *args, **kwargs )
    
    def info( self, msg, *args, **kwargs ):
        """
        Log 'msg % args' with severity 'INFO'.
    
        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.
    
        logger.info("Houston, we have a %s", "interesting problem", exc_info=1)
        """
        self.logger.LOG( msg, *args, **kwargs )
            
    def debug( self, msg, *args, **kwargs ):
        """
        Log 'msg % args' with severity 'DEBUG'.
    
        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.
    
        logger.debug("Houston, we have a %s", "thorny problem", exc_info=1)
        """
        self.logger.DLOG( msg, *args, **kwargs )
        
    def warn( self, msg, *args, **kwargs ):
        """
        Log 'msg % args' with severity 'WARNING'.
    
        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.
    
        logger.warn("Houston, we have a %s", "bit of a problem", exc_info=1)
        """
        self.logger.WLOG( msg, *args, **kwargs )
        
    def error( self, msg, *args, **kwargs ):
        """
        Log 'msg % args' with severity 'ERROR'.
    
        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.
    
        logger.error("Houston, we have a %s", "major problem", exc_info=1)
        """
        self.logger.ELOG( msg, *args, **kwargs )
    
    def critical( self, msg, *args, **kwargs ):
        """
        Log 'msg % args' with severity 'CRITICAL'.
    
        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.
    
        logger.critical("Houston, we have a %s", "bad problem", exc_info=1)
        """
        self.logger.CLOG( msg, *args, **kwargs )
    
    def Lock( self ):
        """ returns lock parameter"""
        flogger = self.LOGGERS.get( self.name )
        return flogger.lock
        
    def getMessageSet( self, type ):
        """Returns set of messages given a type"""
        allSet = {}
        for flogger in self.LOGGERS.values():
            if type == self.INFO:
                func = flogger.logger.GetInfoMessages
            elif type == self.ERROR:
                func = flogger.logger.GetErrorMessages
            elif type == self.WARNING:
                func = flogger.logger.GetWarningMessages
            elif type == self.DEBUG:
                func = flogger.logger.GetDebugMessages
            elif type == self.CRITICAL:
                func = flogger.logger.GetCriticalMessages
            elif type == self.ALL:
                func = flogger.logger.GetAllMessages
                
            allSet[flogger.logger.Name()] = func()
        return allSet
    
    def GetInfoMessages( self, all=False ):
        """Returns a set containing INFO messages"""
        if not all:
            return self.logger.GetInfoMessages()
        else:
            return self.getMessageSet( self.INFO )
                
    def GetDebugMessages( self, all=False ):
        """Returns a set containing DEBUG messages"""
        if not all:
            return self.logger.GetDebugMessages()
        else:
            return self.getMessageSet( self.DEBUG )
       
    def GetErrorMessages( self, all=False ):
        """Returns a set containing ERRORS messages"""
        if not all:
            return self.logger.GetErrorMessages()
        else:
            return self.getMessageSet( self.ERROR )
     
    def GetWarningMessages( self, all=False ):
        """Returns a set containing WARNING messages"""
        if not all:
            return self.logger.GetWarningMessages()
        else:
            return self.getMessageSet( self.WARNING )
       
    def GetCriticalMessages( self, all=False ):
        """Returns a set containing CRITICAL messages"""
        if not all:
            return self.logger.GetCriticalMessages()
        else:
            return self.getMessageSet( self.CRITICAL )
       
    def GetAllMessages( self, all=False ):
        """Returns a set containing ALL messages"""
        if not all:
            return self.logger.GetAllMessages()
        else:
            return self.getMessageSet( self.ALL )

    def clearMessageSet( self, type ):
        """Clears messages by type"""
        for flogger in self.LOGGERS.values():
            if type == self.INFO:
                flogger.logger.ClearInfoMessages()
            elif type == self.ERROR:
                flogger.logger.ClearErrorMessages()
            elif type == self.WARNING:
                flogger.logger.ClearWarningMessages()
            elif type == self.DEBUG:
                flogger.logger.ClearDebugMessages()
            elif type == self.CRITICAL:
                flogger.logger.ClearCriticalMessages()
            elif type == self.ALL:
                flogger.logger.ClearAllMessages()
        
    def ClearInfoMessages( self, all=False ):
        """Clears set containing INFO messages"""
        if not all:
            self.logger.ClearInfoMessages()
        else:    
            self.clearMessageSet( self.INFO )
            
    def ClearDebugMessages( self, all=False ):
        """Clears set containing DEBUG messages"""
        if not all:
            self.logger.ClearDebugMessages()
        else:    
            self.clearMessageSet( self.DEBUG )
    
    def ClearErrorMessages( self, all=False ):
        """Clears set containing ERRORS messages"""
        if not all:
            self.logger.ClearErrorMessages()
        else:    
            self.clearMessageSet( self.ERROR )
    
    def ClearWarningMessages( self, all=False ):
        """Clears set containing WARNING messages"""
        if not all:
            self.logger.ClearWarningMessages()
        else:    
            self.clearMessageSet( self.WARNING )
    
    def ClearCriticalMessages( self, all=False ):
        """Clears set containing CRITICAL messages"""
        if not all:
            self.logger.ClearCriticalMessages()
        else:    
            self.clearMessageSet( self.CRITICAL )
        
    def ClearAllMessages( self, all=False ):
        """Clears set containing ALL messages"""
        if not all:
            self.logger.ClearAllMessages()
        else:    
            self.clearMessageSet( self.ALL )
    
    def Name( self ):
        """Returns logger's name"""
        return self.logger.Name()
    
    def Level( self ):
        """Returns logger's level"""
        return self.logger.Level()
    
    def Keep( self ):
        """Returns logger's keep state"""
        return self.logger.Keep()
    
    def LogOnce( self ):
        """Returns logger's logOne state"""
        return self.logger.LogOnce()
    
    def LogToConsole( self ):
        """Returns logger's logToConsole state"""
        return self.logger.LogToConsole()
    
    def LogToPrime( self ):
        """Returns logger's logToPrime"""
        return self.logger.LogToPrime()
    
    def LogToFileAtSpecifiedPath( self ):
        """Returns logger's logToFileAtSpecifiedPath state"""
        return self.logger.LogToFileAtSpecifiedPath()
    
    def Filters( self ):
        """Returns logger's filters"""
        return self.logger.Filters()
    
    def Handlers( self ):
        """Returns logger's handlers"""
        return self.logger.Handlers()

    def AddHandler( self, handler ):
        """Add a handler to this logger"""
        self.logger.AddHandler( handler )

    def RemoveHandler( self, handler ):
        """Remove a handler to this logger"""
        self.logger.RemoveHandler( handler )

    def AddFilter( self, filter ):
        """Add a filter to this logger"""
        self.logger.AddFilter( filter )

    def RemoveFilter( self, filter ):
        """Remove a filter to this logger"""
        self.logger.RemoveFilter( filter )
        
    def PythonLogger( self ):
        """Returns logger's logger attribute"""
        return self.logger.PythonLogger()
    
    def GetLogger( cls, name ):
        """Return a logger with a given name """
        flogger = cls.LOGGERS.get( name )
        if not flogger:
            return cls(name)
        return flogger
    GetLogger = classmethod( GetLogger )

    def HasLogger( cls, name ):
        """Return a logger with a given name, or None if it doesn't yet exist"""
        return cls.LOGGERS.get( name )
    HasLogger = classmethod( HasLogger ) 

    def getMessageStatus( self, cumulative ):
        """Returns a dictionary indicating if there are messages for each log type"""

        infoStatus = errorStatus = warningStatus = debugStatus = criticalStatus = False
        if self.logger.LoggedInfo(): infoStatus = True
        if self.logger.LoggedError(): errorStatus = True
        if self.logger.LoggedWarning(): warningStatus = True
        if self.logger.LoggedDebug(): debugStatus = True
        if self.logger.LoggedCritical(): criticalStatus = True
        
        if not cumulative:
            return { self.INFO: infoStatus, self.ERROR: errorStatus, self.WARNING: warningStatus, self.DEBUG: debugStatus, self.CRITICAL: criticalStatus }
        else:
            if infoStatus or errorStatus or warningStatus or criticalStatus: infoStatus = True
            if warningStatus or errorStatus or criticalStatus: warningStatus = True
            if errorStatus or criticalStatus: errorStatus = True
            return {self.INFO: infoStatus, self.ERROR: errorStatus, self.WARNING: warningStatus, self.DEBUG: debugStatus, self.CRITICAL: criticalStatus}
        
    def handleMessageStatusRequest( self, cumulative, all ):
        """Return dictionary of message statuses for either a single logger or all loggers"""
        if not all:
            return self.getMessageStatus( cumulative )
        else:
            allSet = {}
            for flogger in self.LOGGERS.values():
                allSet[ flogger.Name() ] = flogger.getMessageStatus( cumulative )
            return allSet    
        
    def MessageStatus( self, cumulative=False, all=False ):
        """Returns a dictionary indicating if there are messages for each type"""
        return self.handleMessageStatusRequest( cumulative, all )

    def Subscribe( self, func, *args ):
        """Subscribe to log messages for this logger"""
        self.logger.Subscribe( func, *args )

    def Unsubscribe( self, func, *args ):
        """Unsubscribe to callback for this logger"""
        self.logger.Unsubscribe( func, *args )

    def UnsubscribeAll( self ):
        """Unsubscribe to all callbacks for this logger"""
        self.logger.UnsubscribeAll()
    
class Logger( object ):
    """Class that wraps logger objects from Python logging module. The inner class type of FLogger"""    

    INFO = 'INFO'
    ERROR = 'ERROR'
    WARNING = 'WARNING'
    DEBUG = 'DEBUG'
    CRITICAL = 'CRITICAL'
    ALL = 'ALL'
    LOGPATH = default_logpath
        
    def __init__( self, name, level, keep, logOnce, logToConsole, logToPrime, logToFileAtSpecifiedPath, filters ):
        self.init( name, level, keep, logOnce, logToConsole, logToPrime, logToFileAtSpecifiedPath, filters )
    
    def init( self, name, level, keep, logOnce, logToConsole, logToPrime, logToFileAtSpecifiedPath, filters ):
        """initializes self via __init__ and Reinitialize"""
        if name is not None: self.name = name
        if level is not None: self.level = level
        if keep is not None: self.keep = keep
        if logOnce is not None: self.logOnce = logOnce
        if logToConsole is not None: self.logToConsole = logToConsole
        if logToPrime is not None: self.logToPrime = logToPrime
        if logToFileAtSpecifiedPath is not None and logToFileAtSpecifiedPath is not False:
            if isinstance( logToFileAtSpecifiedPath, str ):
                path, filename = os.path.split( logToFileAtSpecifiedPath )
                if not path:
                    path = self.LOGPATH
                self.checkThatPathExists( os.path.normpath( path ) )
                logToFileAtSpecifiedPath = os.path.normpath( os.path.join( path, filename ) )
                self.logToFileAtSpecifiedPath = logToFileAtSpecifiedPath
            else: raise TypeError("logToFileAtSpecifiedPath parameter must be None, False or a string")
        else:
            self.logToFileAtSpecifiedPath = None 
        if filters is not None:
            if isinstance( filters, list ):    
                self.filters = filters
            else:
                raise TypeError("filters parameter must be a list")
        else:
            self.filters = None

        #attributes without corresponding parameters to __init__; don't want to override on Reinitialize
        if not hasattr( self, "infoSet" ): self.infoSet = {}
        if not hasattr( self, "errorSet" ): self.errorSet = {}
        if not hasattr( self, "warningSet" ): self.warningSet = {}
        if not hasattr( self, "debugInfoSet" ): self.debugInfoSet = {}
        if not hasattr( self, "criticalSet" ): self.criticalSet = {}
        if not hasattr( self, "callbacks" ): self.callbacks = {}
        if not hasattr( self, "loggedInfo" ): self.loggedInfo = False
        if not hasattr( self, "loggedError" ): self.loggedError = False
        if not hasattr( self, "loggedDebug" ): self.loggedDebug = False
        if not hasattr( self, "loggedWarning" ): self.loggedWarning = False
        if not hasattr( self, "loggedCritical" ): self.loggedCritical = False
                
        #get Python logger and set handlers        
        self.logger = logging.getLogger( self.name )
        self.closeFileHandlers( self.logger )
        self.logger.handlers = self.get_empty_list()
        self.logger.filters = self.get_empty_list()
        self.python_formatter = logging.Formatter( '%(asctime)s %(levelname).1s %(process)04X %(name)s %(message)s', '%y%m%d %H%M%S')
        self.prime_formatter = logging.Formatter( '%(levelname)s %(message)s' )
        
        if self.logToConsole: 
            hdlr = logging.StreamHandler( sys.stdout )    
            hdlr.setFormatter( self.python_formatter )
            self.logger.addHandler( hdlr )
        if self.logToFileAtSpecifiedPath: 
            hdlr = logging.FileHandler( self.logToFileAtSpecifiedPath )    
            hdlr.setFormatter( self.python_formatter )
            self.logger.addHandler( hdlr )
        if self.logToPrime:
            hdlr = PrimeHandler()    
            hdlr.setFormatter( self.prime_formatter )
            self.logger.addHandler( hdlr )
        
        if self.filters is not None:    
            for filter in self.filters:
                self.logger.addFilter( filter )
                
        if self.logOnce:
            self.logger.addFilter( DuplicateFilter( self.errorSet, self.ERROR ) )
            self.logger.addFilter( DuplicateFilter( self.infoSet, self.INFO ) )
            self.logger.addFilter( DuplicateFilter( self.warningSet, self.WARNING ) )
            self.logger.addFilter( DuplicateFilter( self.debugInfoSet, self.DEBUG ) )
            self.logger.addFilter( DuplicateFilter( self.criticalSet, self.CRITICAL ) )

        if self.level == 1:
            self.logger.setLevel( logging.INFO )
        elif self.level == 2:
            self.logger.setLevel( logging.DEBUG )
        elif self.level == 3:
            self.logger.setLevel( logging.WARN )
        elif self.level == 4:
            self.logger.setLevel( logging.ERROR )
        else:
            raise RuntimeError('parameter "level" must be either 1 ( INFO ), 2 ( DEBUG ), 3 ( WARN ), 4 ( ERROR ).')
        
        self.createLock()

    def createLock( self ):
        """Acquire a thread lock for serializing access shared structures"""
        if not hasattr( self, "lock" ) and threading:
            self.lock = threading.RLock()
        else:
            self.lock = None

    def acquireLock( self ):
        """Acquire the thread lock"""
        if self.lock:
            self.lock.acquire()

    def releaseLock( self ):
        """Release the thread lock"""
        if self.lock:
            self.lock.release()
                                
    def checkThatPathExists( self, path ):
        """Creates log directory if it doesn't exist"""
        if not os.path.exists( path ):
            try:
                os.makedirs( path)
                logging.warning("FLogger created missing directory: %s", path )
            except:
                logging.error("FLogger unable to create missing directory: %s", path )

    def get_empty_list( self ):
        """Returns an empty list to clear handles and filters"""
        return []
    
    def manage_set( self, set, size, logRecord ):
        """Checks that set is not larger than max size and adds elements"""
        if len( set ) < size:
            self.acquireLock()
            try:
                msg = logRecord.getMessage()
                if set.get( msg ):
                    set[ msg ].append( logRecord )
                else:
                    set[ msg ] = [ logRecord ]
            finally:
                self.releaseLock()
        else:
            pass

    def manage_callbacks( self, logRecord ):
        """calls all callbacks functions passing the logger name, message, type, and additional arguments"""
        if self.callbacks:
            for key, func in self.callbacks.items():
                func( logRecord, key[ 1 ]  )
        
    def closeFileHandlers( self, logger ):
        """Close all file handlers"""
        [ h.close() for h in logger.handlers if h.__class__.__name__ == 'FileHandler' ]
        
    def Reinitialize( self, level, keep, logOnce, logToConsole, logToPrime, logToFileAtSpecifiedPath, filters ):
        """Reinitializes the logger object based on given parameters and returns logger instance"""
        self.init( None, level, keep, logOnce, logToConsole, logToPrime, logToFileAtSpecifiedPath, filters )
        return self
    
    def makeLogRecord( self, level, msg, args, exc_info=None, extra=None ):
        """
        Low-level logging routine which creates a LogRecord and then calls
        all the handlers of this logger to handle the record.
        """
        if logging._srcfile:
            try:
                fn, lno, func = self.logger.findCaller()
            except ValueError:
                fn, lno, func, stack = self.logger.findCaller()
        else:
            fn, lno, func = "(unknown file)", 0, "(unknown function)"
        if exc_info:
            if type(exc_info) != types.TupleType:
                exc_info = sys.exc_info()
        record = self.logger.makeRecord(self.logger.name, level, fn, lno, msg, args, exc_info, func, extra)
        return record  
                 
    def LOG( self, msg, *args, **kwargs ):
        """Log 'msg % args' with severity 'INFO'"""
        self.logger.info( msg, *args, **kwargs )
        record = self.makeLogRecord( *(logging.INFO, msg, args), **kwargs )
        if self.keep or self.logOnce:
            self.manage_set( self.infoSet, maxInfoSetSize, record )
        self.manage_callbacks( record )
        self.loggedInfo = True
                    
    def DLOG( self, msg, *args, **kwargs ):
        """Log 'msg % args' with severity 'DEBUG'"""
        self.logger.debug( msg, *args, **kwargs )
        record = self.makeLogRecord( *(logging.DEBUG, msg, args), **kwargs )
        if self.keep or self.logOnce:
            self.manage_set( self.debugInfoSet, maxDebugInfoSetSize, record )
        self.manage_callbacks( record )
        self.loggedDebug = True
                
    def ELOG( self, msg, *args, **kwargs ):
        """Log 'msg % args' with severity 'ERROR'"""
        self.logger.error( msg, *args, **kwargs )
        record = self.makeLogRecord( *(logging.ERROR, msg, args), **kwargs )
        if self.keep or self.logOnce:
            self.manage_set( self.errorSet, maxErrorSetSize, record )
        self.manage_callbacks( record )
        self.loggedError = True
                
    def WLOG( self, msg, *args, **kwargs ):
        """Log 'msg % args' with severity 'WARNING'"""
        self.logger.warning( msg, *args, **kwargs )
        record = self.makeLogRecord( *(logging.WARNING, msg, args), **kwargs )
        if self.keep or self.logOnce:
            self.manage_set( self.warningSet, maxWarningSetSize, record )
        self.manage_callbacks( record )
        self.loggedWarning = True
            
    def CLOG( self, msg, *args, **kwargs ):
        """Log 'msg % args' with severity 'CRITICAL'"""
        self.logger.critical( msg, *args, **kwargs )
        record = self.makeLogRecord( *(logging.CRITICAL, msg, args), **kwargs )
        if self.keep or self.logOnce:
            self.manage_set( self.criticalSet, maxCriticalSetSize, record )
        self.manage_callbacks( record ) 
        self.loggedCritical = True
        
    def LoggedInfo( self ):
        return self.loggedInfo
    
    def LoggedWarning( self ):
        return self.loggedWarning
    
    def LoggedError( self ):
        return self.loggedError
    
    def LoggedCritical( self ):
        return self.loggedCritical
    
    def LoggedDebug( self ):
        return self.loggedDebug
                
    def GetInfoMessages( self ):
        """Returns a set containing INFO messages"""
        return self.infoSet.items()
                
    def GetDebugMessages( self ):
        """Returns a set containing DEBUG messages"""
        return self.debugInfoSet.items()
            
    def GetErrorMessages( self ):
        """Returns a set containing ERRORS messages"""
        return self.errorSet.items()
    
    def GetWarningMessages( self ):
        """Returns a set containing WARNING messages"""
        return self.warningSet.items()
    
    def GetCriticalMessages( self ):
        """Returns a set containing CRITICAL messages"""
        return self.criticalSet.items()
    
    def GetAllMessages( self ):
        """Returns a set containing ALL messages"""
        allSet = {}
        allSet.update( self.infoSet )
        allSet.update( self.warningSet )
        allSet.update( self.errorSet )
        allSet.update( self.debugInfoSet )
        allSet.update( self.criticalSet )
        return allSet.items()
    
    def ClearInfoMessages( self ):
        """Clears set containing INFO messages"""
        self.infoSet.clear()
                
    def ClearDebugMessages( self ):
        """Clears set containing DEBUG messages"""
        self.debugInfoSet.clear()
    
    def ClearErrorMessages( self ):
        """Clears set containing ERRORS messages"""
        self.errorSet.clear()
    
    def ClearWarningMessages( self ):
        """Clears set containing WARNING messages"""
        self.warningSet.clear()
    
    def ClearCriticalMessages( self ):
        """Clears set containing CRITICAL messages"""
        self.criticalSet.clear()
                
    def ClearAllMessages( self ):
        """Clears set containing ALL messages"""
        self.infoSet.clear()
        self.warningSet.clear()
        self.errorSet.clear()
        self.debugInfoSet.clear()
        self.criticalSet.clear()
                
    def Name( self ):
        """Returns logger's name"""
        return self.name
            
    def Level( self ):
        """Returns logger's level"""
        return self.level
                
    def Keep( self ):
        """Returns logger's keep state"""
        return self.keep
    
    def LogOnce( self ):
        """Returns logger's logOne state"""
        return self.logOnce
            
    def LogToConsole( self ):
        """Returns logger's logToConsole state"""
        return self.logToConsole
    
    def LogToPrime( self ):
        """Returns logger's logToPrime"""
        return self.logToPrime
            
    def LogToFileAtSpecifiedPath( self ):
        """Returns logger's logToFileAtSpecifiedPath state"""
        return self.logToFileAtSpecifiedPath
            
    def Filters( self ):
        """Returns logger's handlers"""
        return [ flter.__class__.__name__ for flter in self.logger.filters ]
    
    def Handlers( self ):
        """Returns logger's handlers"""
        return [ hdlr for hdlr in self.logger.handlers ]

    def AddHandler( self, handler ):
        """Add a handler to this logger"""
        self.logger.addHandler( handler )

    def RemoveHandler( self, handler ):
        """Remove a handler to this logger"""
        self.logger.removeHandler( handler )

    def AddFilter( self, filter ):
        """Add a filter to this logger"""
        self.logger.addFilter( filter )

    def RemoveFilter( self, filter ):
        """Remove a filter to this logger"""
        self.logger.removeFilter( filter )    
    
    def PythonLogger( self ):
        """Returns the logger object"""
        return self.logger

    def Subscribe( self, func, *args ):
        """Subscribe to log messages for this logger"""
        self.acquireLock()
        try:
            self.callbacks[ ( hash( func ), args ) ] = func
        finally:
            self.releaseLock()
            
    def Unsubscribe( self, func, *args ):
        """Unsubscribe to log messages for this logger"""
        if self.callbacks.has_key( ( hash( func ), args ) ):
            del self.callbacks[ ( hash( func ), args ) ]

    def UnsubscribeAll( self ):
        """Unsubscribe to all callbacks for this logger"""
        for key in self.callbacks.keys():
            del self.callbacks[ key ]
    
class DuplicateFilter( object ):
    """Filter class for filtering duplicate log messages"""
    def __init__( self, set, msg_type ):
        self.set = set
        self.msg_type = msg_type
        
    def filter( self, logRecord ):
        """Filters duplicate log messages by checking membership in set"""
        if self.set.get( logRecord.getMessage() ):
            return 0
        else:
            return 1
        
class PrimeHandler( logging.Handler ):
    """Handler class for ael.log"""
    def emit( self, record ):
        """Protocol function for logging Handlers"""
        try:
            import ael
            msg = self.format( record )
            ael.log( msg )
        except:
            self.handleError( record )
            
if __name__ == "__main__":
    """ To execute tests pass command line arguments as follows:
        
        >python FLogger.py -s127.0.0.1:9037 -uSYSTEM -pINTAS -t1  #NULL passwords are entered as -p 
    """    
    import sys
    import getopt
    import ael
    
    def usage():
        print ("-h, --help", "    get options")
        print ("-t, --test", "    test to perform")
        print ("-s, --server", "  server")
        print ("-u, --user", "    username")
        print ("-p, --password", "password")
        
    try:
        opts, args = getopt.getopt( sys.argv[1:], "ht:s:u:p", ["help", "test", "server", "user", "password"] )
    except getopt.GetoptError:
        # print help information and exit:
        usage()
        sys.exit( 2 )
    print (opts, args)
    
    test = None
    server = "127.0.0.1:9037"
    user = 'TRADER1'
    password = 'Holistic1'
    for o, a in opts:
        
        if o in ( "-h", "--help" ):
            usage()
            sys.exit()
        if o in ( "-t", "--test" ):
            test = a
        if o in ( "-s", "--server" ):
            server = a
        if o in ( "-u", "--user" ):
            user = a
        if o in ( "-p", "--password" ):
            password = a
    try:        
        ael.connect( server, user, password )
    except:
        print ("Error: ael.connect(%s, %s, %s) failed" % ( server, user, password ))
        sys.exit()

    if test == '1':
        #Example 1: log without initializing via init_logger, then change some settings
        
        log = FLogger()
        
        print ('All default settings')
        #start logging using module interface without using init_logger
        log.LOG( "Houston, we have a %s", "interesting problem" )
        log.WLOG( "Houston, we have a %s", "bit of a problem" )
        log.ELOG( "Houston, we have a %s", "major problem" )
        log.DLOG( "Houston, we have a %s", "thorny problem" )
        log.CLOG( "Houston, we have a %s", "bad problem" )
        
        #re-init logger to print debug information
        print ("level 2: re-init logger to print debug information")
        log.Reinitialize( level=2 )
        
        #use FLogger interface
        log.LOG( "Houston, we have a %s", "interesting problem" )
        log.WLOG( "Houston, we have a %s", "bit of a problem" )
        log.ELOG( "Houston, we have a %s", "major problem" )
        log.DLOG( "Houston, we have a %s", "thorny problem" )
        log.CLOG( "Houston, we have a %s", "bad problem" )
                
    
    elif test == '2':
        #Example 2: Log to ael.log, log to file, and use a custom filter, turn on debug logging
        class EndsWithFilter( object ):
            "Filter class for filtering log messages"
                
            def filter( self, msg ):
                "Example filter: exclude all messages ending with 'major problem'"
                if msg.args[ 0 ].endswith( 'major problem' ):
                    return 0
                else:
                    return 1
        
        filters = [ EndsWithFilter() ]            
        
              
        print ("level 2, logToPrime, logToFileAtSpecifiedPath, EndsWithFilter")
        log = FLogger( level=2, logToPrime=True, logToFileAtSpecifiedPath="C:\\temp\\FLogger.txt", filters=filters )
        
        log.LOG( "Houston, we have a %s", "interesting problem" )
        log.WLOG( "Houston, we have a %s", "bit of a problem" ) 
        log.ELOG( "Houston, we have a %s", "major problem" )
        log.DLOG( "Houston, we have a %s", "thorny problem" )
        log.CLOG( "Houston, we have a %s", "bad problem" )
        
        log.LOG( "Houston, we have a %s", "interesting problem" )
        log.WLOG( "Houston, we have a %s", "bit of a problem" )
        log.ELOG( "Houston, we have a %s", "major problem" )
        log.DLOG( "Houston, we have a %s", "thorny problem" )
        log.CLOG( "Houston, we have a %s", "bad problem" )
        
        
    elif test == '3':
        #Example 3: Keep log messages in a set so they can be processed.
        print ("keep on, level 2")
        log = FLogger( keep=True, level=2 )
        
        log.LOG( "Houston, we have a %s", "interesting problem" )
        log.WLOG( "Houston, we have a %s", "bit of a problem" )
        log.ELOG( "Houston, we have a %s", "major problem" )
        log.DLOG( "Houston, we have a %s", "thorny problem" )
        log.CLOG( "Houston, we have a %s", "bad problem" )
        
        print (log.GetInfoMessages())
        print (log.GetWarningMessages())
        print (log.GetErrorMessages())
        print (log.GetDebugMessages())
        print (log.GetCriticalMessages())
        print (log.GetAllMessages())
        
        #log some more and see if they are in sets
        log.LOG( "Houston, we have more %s", "interesting problems" )
        log.WLOG( "Houston, we have more %s", "of a problem" )
        log.ELOG( "Houston, we have more %s", "major problems" )
        log.DLOG( "Houston, we have more %s", "thorny problems" )
        log.CLOG( "Houston, we have a %s", "bad problems" )
        
        print (log.GetInfoMessages())
        print (log.GetWarningMessages())
        print (log.GetErrorMessages())
        print (log.GetDebugMessages())
        print (log.GetCriticalMessages())
        print (log.GetAllMessages())
        
        
    elif test == '4':
        #Example 4: Don't log duplicate messages
        print ("level 2, logOnce")
        log = FLogger( level = 2, logOnce=True )
        log.LOG( "Houston, we have a %s", "interesting problem" )
        log.WLOG( "Houston, we have a %s", "bit of a problem" )
        log.ELOG( "Houston, we have a %s", "major problem" )
        log.DLOG( "Houston, we have a %s", "thorny problem" )
        log.CLOG( "Houston, we have a %s", "bad problem" )
        
        log.LOG( "Houston, we have a %s", "interesting problem" )
        log.WLOG( "Houston, we have a %s", "bit of a problem" )
        log.ELOG( "Houston, we have a %s", "major problem" )
        log.DLOG( "Houston, we have a %s", "thorny problem" )
        log.CLOG( "Houston, we have a %s", "bad problem" )
                
    elif test == '5':
        #Example 5: Change state of logger
        print ("level 2, logOnce")
        log = FLogger( level = 2, logOnce=True )
        print ('testing with first instance; logOnce')
        log.LOG( "Houston, we have a %s", "interesting problem" )
        log.WLOG( "Houston, we have a %s", "bit of a problem" )
        log.ELOG( "Houston, we have a %s", "major problem" )
        log.DLOG( "Houston, we have a %s", "thorny problem" )
        log.CLOG( "Houston, we have a %s", "bad problem" )
        
        log.LOG( "Houston, we have a %s", "interesting problem" )
        log.WLOG( "Houston, we have a %s", "bit of a problem" )
        log.ELOG( "Houston, we have a %s", "major problem" )
        log.DLOG( "Houston, we have a %s", "thorny problem" )
        log.CLOG( "Houston, we have a %s", "bad problem" )
        
        #change parameters to logger
        log.Reinitialize( level = 1, logToPrime=True, logOnce=False )
        print ('level 1,  logToPrime, turn off logOnce')
        log.LOG( "Houston, we have a %s", "interesting problem" )
        log.WLOG( "Houston, we have a %s", "bit of a problem" )
        log.ELOG( "Houston, we have a %s", "major problem" )
        log.DLOG( "Houston, we have a %s", "thorny problem" )
        log.CLOG( "Houston, we have a %s", "bad problem" )
        
        log.LOG( "Houston, we have a %s", "interesting problem" )
        log.WLOG( "Houston, we have a %s", "bit of a problem" )
        log.ELOG( "Houston, we have a %s", "major problem" )
        log.DLOG( "Houston, we have a %s", "thorny problem" )
        log.CLOG( "Houston, we have a %s", "bad problem" )
        
        
    elif test == '6':
        #Example 6: Reverse of 5 with respect to logOnce
        
        log = FLogger( level = 2, logOnce=False )
        print ('level 2, logOnce off')
        log.LOG( "Houston, we have a %s", "interesting problem" )
        log.WLOG( "Houston, we have a %s", "bit of a problem" )
        log.ELOG( "Houston, we have a %s", "major problem" )
        log.DLOG( "Houston, we have a %s", "thorny problem" )
        log.CLOG( "Houston, we have a %s", "bad problem" )
        
        log.LOG( "Houston, we have a %s", "interesting problem" )
        log.WLOG( "Houston, we have a %s", "bit of a problem" )
        log.ELOG( "Houston, we have a %s", "major problem" )
        log.DLOG( "Houston, we have a %s", "thorny problem" )
        log.CLOG( "Houston, we have a %s", "bad problem" )
        
        #change parameters to logger
        log.Reinitialize( level = 1, logToPrime=True, logOnce=True ) 
        print ('level 1, logToprime, logOnce')
        log.LOG( "Houston, we have a %s", "interesting problem" )
        log.WLOG( "Houston, we have a %s", "bit of a problem" )
        log.ELOG( "Houston, we have a %s", "major problem" )
        log.DLOG( "Houston, we have a %s", "thorny problem" )
        log.CLOG( "Houston, we have a %s", "bad problem" )
        
        log.LOG( "Houston, we have a %s", "interesting problem" )
        log.WLOG( "Houston, we have a %s", "bit of a problem" )
        log.ELOG( "Houston, we have a %s", "major problem" )
        log.DLOG( "Houston, we have a %s", "thorny problem" )
        log.CLOG( "Houston, we have a %s", "bad problem" )
                
        
    elif test == '7':
        #Example 2: re-init without filter as parameter. filters should still exist
        class EndsWithFilter( object ):
            "Filter class for filtering duplicate log messages"
                
            def filter( self, msg ):
                "Example filter: exclude all messages ending with 'major problem'"
                if msg.getMessage().endswith( 'major problem' ):
                    return 0
                else:
                    return 1
        
        filters = [ EndsWithFilter() ]            
        
        log = FLogger( level = 2, logToPrime=True, logToFileAtSpecifiedPath="C:\\temp\\FLogger.txt", filters=filters )
        print ("level 2, logToPrime, logToFileAtSpecifiedPath, using EndsWithFilter")
        log.LOG( "Houston, we have a %s", "interesting problem" )
        log.WLOG( "Houston, we have a %s", "bit of a problem" )
        log.ELOG( "Houston, we have a %s", "major problem" )
        log.DLOG( "Houston, we have a %s", "thorny problem" )
        log.CLOG( "Houston, we have a %s", "bad problem" )
        
        
        #filters should still exist
        print ('level 1, logToPrime off, EndsWithFilter should be turned off')
        log.Reinitialize( logToPrime=False )
        log.LOG( "Houston, we have a %s", "interesting problem" )
        log.WLOG( "Houston, we have a %s", "bit of a problem" )
        log.ELOG( "Houston, we have a %s", "major problem" )
        log.DLOG( "Houston, we have a %s", "thorny problem" )
        log.CLOG( "Houston, we have a %s", "bad problem" )
                
        #filters should still exist
        print ('level 2, EndsWithFilter should be on again')
        log.Reinitialize( level=2, filters=filters )
        log.LOG( "Houston, we have a %s", "interesting problem" )
        log.WLOG( "Houston, we have a %s", "bit of a problem" )
        log.ELOG( "Houston, we have a %s", "major problem" )
        log.DLOG( "Houston, we have a %s", "thorny problem" )
        log.CLOG( "Houston, we have a %s", "bad problem" )
        
        
    elif test == '8':
        #Example 8: Change state of logger
        print ("log everywhere")
        log = FLogger( logToPrime=True, logToFileAtSpecifiedPath="C:\\temp\\FLogger.txt")
        print ('testing with first instance; logOnce')
        log.LOG( "Houston, we have a %s", "interesting problem" )
        log.WLOG( "Houston, we have a %s", "bit of a problem" )
        log.ELOG( "Houston, we have a %s", "major problem" )
        log.DLOG( "Houston, we have a %s", "thorny problem" )
        log.CLOG( "Houston, we have a %s", "bad problem" )
        
        log.LOG( "Houston, we have a %s", "interesting problem" )
        log.WLOG( "Houston, we have a %s", "bit of a problem" )
        log.ELOG( "Houston, we have a %s", "major problem" )
        log.DLOG( "Houston, we have a %s", "thorny problem" )
        log.CLOG( "Houston, we have a %s", "bad problem" )
        
        #change parameters to logger
        log.Reinitialize( logToConsole=False, logToPrime=False, logToFileAtSpecifiedPath=False )
        print ('turn off all logging')
        log.LOG( "Houston, we have a %s", "interesting problem" )
        log.WLOG( "Houston, we have a %s", "bit of a problem" )
        log.ELOG( "Houston, we have a %s", "major problem" )
        log.DLOG( "Houston, we have a %s", "thorny problem" )
        log.CLOG( "Houston, we have a %s", "bad problem" )
        
        log.LOG( "Houston, we have a %s", "interesting problem" )
        log.WLOG( "Houston, we have a %s", "bit of a problem" )
        log.ELOG( "Houston, we have a %s", "major problem" )
        log.DLOG( "Houston, we have a %s", "thorny problem" )
        log.CLOG( "Houston, we have a %s", "bad problem" )
    
    elif test == '9':
        #Example 9: test that states are independent
        print ("log everywhere")
        log = FLogger( logToPrime=True, logToFileAtSpecifiedPath="C:\\temp\\FLogger.txt")
        print ('testing with first instance log everywhere')
        log.LOG( "Houston, we have a %s", "interesting problem" )
        log.WLOG( "Houston, we have a %s", "bit of a problem" )
        log.ELOG( "Houston, we have a %s", "major problem" )
        log.DLOG( "Houston, we have a %s", "thorny problem" )
        log.CLOG( "Houston, we have a %s", "bad problem" )
        
        log.LOG( "Houston, we have a %s", "interesting problem" )
        log.WLOG( "Houston, we have a %s", "bit of a problem" )
        log.ELOG( "Houston, we have a %s", "major problem" )
        log.DLOG( "Houston, we have a %s", "thorny problem" )
        log.CLOG( "Houston, we have a %s", "bad problem" )
        
        #change parameters to logger
        log2 = FLogger( name = 'another', logToConsole=False, logToPrime=False, logToFileAtSpecifiedPath=False )
        print ('\nturn off all logging with log2')
        log2.LOG( "Houston, we have a %s", "interesting problem" )
        log2.WLOG( "Houston, we have a %s", "bit of a problem" )
        log2.ELOG( "Houston, we have a %s", "major problem" )
        log2.DLOG( "Houston, we have a %s", "thorny problem" )
        log2.CLOG( "Houston, we have a %s", "bad problem" )
        
        log2.LOG( "Houston, we have a %s", "interesting problem" )
        log2.WLOG( "Houston, we have a %s", "bit of a problem" )
        log2.ELOG( "Houston, we have a %s", "major problem" )
        log2.DLOG( "Houston, we have a %s", "thorny problem" )
        log2.CLOG( "Houston, we have a %s", "bad problem" )

        print ("\log with original logger")
        log.Reinitialize( logToPrime=True, logToFileAtSpecifiedPath="C:\\temp\\FLogger.txt")
        log.LOG( "Houston, we have a %s", "interesting problem" )
        log.WLOG( "Houston, we have a %s", "bit of a problem" )
        log.ELOG( "Houston, we have a %s", "major problem" )
        log.DLOG( "Houston, we have a %s", "thorny problem" )
        log.CLOG( "Houston, we have a %s", "bad problem" )
        
        log.LOG( "Houston, we have a %s", "interesting problem" )
        log.WLOG( "Houston, we have a %s", "bit of a problem" )
        log.ELOG( "Houston, we have a %s", "major problem" )
        log.DLOG( "Houston, we have a %s", "thorny problem" )
        log.CLOG( "Houston, we have a %s", "bad problem" )
        
        
    elif test == '10':
        #Example 10: re-init without filter as parameter. filters should still exist
        class EndsWithFilter( object ):
            "Filter class for filtering duplicate log messages"
                
            def filter( self, msg ):
                "Example filter: exclude all messages ending with 'major problem'"
                if msg.getMessage().endswith( 'one' ):
                    return 0
                else:
                    return 1
        
        filters = [ EndsWithFilter() ]            
        
        log = FLogger( level = 2, logToPrime=True, logToFileAtSpecifiedPath="C:\\temp\\FLogger.txt", filters=filters )
        print ("log1: level 2, logToPrime, logToFileAtSpecifiedPath, using EndsWithFilter")
        print ("log name", log.Name())
        log.LOG( "ilog %s", "1 one" )
        log.WLOG( "wlog %s", "1" )
        log.ELOG( "elog %s", "1" )
        log.DLOG( "dlog %s", "1" )
        log.CLOG( "clog %s", "1" )
        
                
        #filters should still exist
        print ('\nlog with log2 defaults')
        log2 = FLogger(name='another')
        print ("log2 name", log2.Name())
        log2.LOG( "ilog %s", "2" )
        log2.WLOG( "wlog %s", "2" )
        log2.ELOG( "elog %s", "2" )
        log2.DLOG( "dlog %s", "2" )
        log2.CLOG( "clog %s", "2" )
        
        print ('Resume with log1')
        print ("log name", log.Name())
        log.LOG( "ilog %s", "1 one" )
        log.WLOG( "wlog %s", "1" )
        log.ELOG( "elog %s", "1" )
        log.DLOG( "dlog %s", "1" )
        log.CLOG( "clog %s", "1" )
        
    elif test == '11':
        """Example 11: see that log messages are separated by logger name"""
        print ("keep on, level 2")
        log = FLogger( keep=True, level=2 )
        
        log.LOG( "ilog %s", "1" )
        log.WLOG( "wlog %s", "1" )
        log.ELOG( "elog %s", "1" )
        log.DLOG( "dlog %s", "1" )
        log.CLOG( "clog %s", "1" )
        
        print (log.GetInfoMessages())
        print (log.GetWarningMessages())
        print (log.GetErrorMessages())
        print (log.GetDebugMessages())
        print (log.GetCriticalMessages())
        print (log.GetAllMessages())
        
        
        log2 = FLogger( name='another', keep=True, level=2 )
        #log some more and see if they are in sets
        print ('\nprint using logger2')
        log2.LOG( "ilog %s", "2" )
        log2.WLOG( "wlog %s", "2" )
        log2.ELOG( "elog %s", "2" )
        log2.DLOG( "dlog %s", "2" )
        log2.CLOG( "clog %s", "2" )
        
        print (log2.GetInfoMessages())
        print (log2.GetWarningMessages())
        print (log2.GetErrorMessages())
        print (log2.GetDebugMessages())
        print (log2.GetCriticalMessages())
        print (log2.GetAllMessages())
        
        print ('\nlog logger1 messages')
        print (log.GetInfoMessages())
        print (log.GetWarningMessages())
        print (log.GetErrorMessages())
        print (log.GetDebugMessages())
        print (log.GetCriticalMessages())
        print (log.GetAllMessages())

        log.ClearInfoMessages()
        log.ClearWarningMessages()
        log.ClearErrorMessages()
        log.ClearDebugMessages()
        log.ClearCriticalMessages()
        log.ClearAllMessages()

        print ('\nlog logger1 messages after clearing')
        print (log.GetInfoMessages())
        print (log.GetWarningMessages())
        print (log.GetErrorMessages())
        print (log.GetDebugMessages())
        print (log.GetCriticalMessages())
        print (log.GetAllMessages())

    
    elif test == '12':
        """test message separation using inheritence, and get, clear, and status functions"""
        class MyLogger( FLogger ):
            LOGGERS = {}
        
        flog = FLogger(keep=True)
        mylog = MyLogger(keep=True)

        flog.LOG('flog')
        flog.WLOG('flog')
        flog.ELOG('flog')
        flog.CLOG('flog')
        
        mylog.LOG('mylog')
        mylog.WLOG('mylog')
        mylog.ELOG('mylog')
        mylog.CLOG('mylog')  
        
        print (flog.GetInfoMessages( all=True ))
        print (mylog.GetInfoMessages( all=True ))

        print ('flog')
        print (flog.GetInfoMessages( all=True ))
        print (flog.GetWarningMessages( all=True ))
        print (flog.GetErrorMessages( all=True ))
        print (flog.GetDebugMessages( all=True ))
        print (flog.GetCriticalMessages( all=True ))
        print (flog.GetAllMessages( all=True ))

        print ('mylog')
        print (mylog.GetInfoMessages( all=True ))
        print (mylog.GetWarningMessages( all=True ))
        print (mylog.GetErrorMessages( all=True ))
        print (mylog.GetDebugMessages( all=True ))
        print (mylog.GetCriticalMessages( all=True ))
        print (mylog.GetAllMessages( all=True ))

        print ('MESSAGE STATUS:', flog.MessageStatus())

        print( 'clear flog')
        flog.ClearInfoMessages( all=True )
        flog.ClearWarningMessages( all=True )
        flog.ClearErrorMessages( all=True )
        flog.ClearDebugMessages( all=True )
        flog.ClearCriticalMessages( all=True )
        flog.ClearAllMessages( all=True )

        print ('flog after clear all')
        print (flog.GetInfoMessages( all=True ))
        print (flog.GetWarningMessages( all=True ))
        print (flog.GetErrorMessages( all=True ))
        print (flog.GetDebugMessages( all=True ))
        print (flog.GetCriticalMessages( all=True ))
        print (flog.GetAllMessages( all=True ))

        print ('MESSAGE STATUS:', flog.MessageStatus())
        
    elif test == '13':
        """inherit from FLogger with out partitioning messages: don't redefine Loggers and LOGGERS in derived class"""
        class MyLogger( FLogger ): pass
            
        
        flog = FLogger(keep=True)
        mylog = MyLogger(keep=True)

        flog.LOG('flog')
        mylog.LOG('mylog')
        
        print (flog.GetInfoMessages( all=True ))
        print (mylog.GetInfoMessages( all=True ))

        
    elif test == '14':
        """test that inheriting from FLogger partitions messages: redefine Loggers and LOGGERS in derived class"""
        class MyLogger( FLogger ):
            LOGGERS = {}
        
        flog = FLogger(keep=True)
        mylog = MyLogger(keep=True)

        flog.LOG('flog')
        mylog.LOG('mylog')  
        
        print (flog.GetInfoMessages( all=True ))
        print (mylog.GetInfoMessages( all=True ))

    elif test == '15':
        """test default log path"""
        logger = FLogger(logToFileAtSpecifiedPath='noPathTest.txt')
        logger.LOG('hello')
        
    elif test == '16':
        """test default log path"""
        logger = FLogger(keep=True)
        logger.LOG('i')
        print (logger.MessageStatus(cumulative=True))
        logger.WLOG('w')
        print (logger.MessageStatus(cumulative=True))
        logger.ELOG('e')
        print (logger.MessageStatus(cumulative=True))
        logger.CLOG('c')
        print (logger.MessageStatus(cumulative=True))

    elif test == '17':
        """test message status"""
        logger = FLogger(keep=True)
        logger.ELOG('e')
        print (logger.MessageStatus(cumulative=True))

    elif test == '18':
        """test message status cumulative"""
        logger = FLogger(name = 'log1', keep=True)
        logger.ELOG('e')
        print (logger.MessageStatus(cumulative=True, all=True))
        logger2 = FLogger(name = 'log2', keep=True)
        logger2.WLOG('e')
        print (logger2.MessageStatus(cumulative=True, all=True))

    elif test == '19':
        """test create log path"""
        logger = FLogger(logToFileAtSpecifiedPath='c:\\temp2\\noPathTest.txt')
        logger.LOG('hello')

    elif test == '20':
        """test subscription/unsubscription"""

        def msg_callback( logRecord, args ):
            print (logRecord.name)
            print (logRecord.getMessage())
            print (args)
            print ()

        logger = FLogger()
        logger.Subscribe( msg_callback, 'info1', 'info2' )
        logger.LOG( 'message %s %s', 'for', 'matthew' )
        logger.Unsubscribe( msg_callback, 'info1', 'info2' )
        logger.LOG( 'another message %s %s', 'for', 'matthew' )

    elif test == '21':
        """test multiple subscription/unsubscription"""
        def msg_callback( logRecord, args ):
            print (logRecord.name)
            print (logRecord.getMessage())
            print (args)
            print ()
            
        logger = FLogger()
        logger.Subscribe( msg_callback, 'info1', 'info2' )
        logger.Subscribe( msg_callback, 'info3', 'info4' )
        logger.LOG( 'message %s %s', 'for', 'logging' )
        logger.Unsubscribe( msg_callback, 'info1', 'info2' )
        logger.Unsubscribe( msg_callback, 'info3', 'info4' )
        logger.LOG( 'another message %s %s', 'for', 'logging' )


    elif test == '22':
        """test UnsubscribeAll"""
        def msg_callback( logRecord, args ):
            print (logRecord.name)
            print (logRecord.getMessage())
            print (args)
            print ()
            
        logger = FLogger()
        logger.Subscribe( msg_callback, 'info1', 'info2' )
        logger.Subscribe( msg_callback, 'info3', 'info4' )
        logger.LOG( 'message %s %s', 'for', 'logging' )
        logger.UnsubscribeAll()
        logger.LOG( 'another message %s %s', 'for', 'logging' )


    elif test == '23':
        #Example 23: test AddFilter and RemoveFilter
        class EndsWithFilter( object ):
            "Filter class for filtering duplicate log messages"
                
            def filter( self, msg ):
                "Example filter: exclude all messages ending with 'major problem'"
                if msg.getMessage().endswith( 'one' ):
                    return 0
                else:
                    return 1
        
        log = FLogger()
        filter = EndsWithFilter()

        log.AddFilter( filter )
        print ("using EndsWithFilter added from AddFilter")
        log.LOG( "ilog %s", "1 one" )
        log.WLOG( "wlog %s", "1" )
        log.ELOG( "elog %s", "1" )
        log.DLOG( "dlog %s", "1" )
        log.CLOG( "clog %s", "1" )

        log.RemoveFilter( filter )
        print ("removing EndsWithFilter added from AddFilter")
        log.LOG( "ilog %s", "1 one" )
        log.WLOG( "wlog %s", "1" )
        log.ELOG( "elog %s", "1" )
        log.DLOG( "dlog %s", "1" )
        log.CLOG( "clog %s", "1" )

    elif test == '24':
        """test Add and Remove Handler"""
        python_formatter = logging.Formatter( '%(asctime)s %(levelname)s %(message)s' )
        hdlr = logging.FileHandler( "c:\\temp\\handlerTest.txt" )    
        hdlr.setFormatter( python_formatter )
        logger = FLogger()
        logger.AddHandler( hdlr )
        logger.LOG( "hello test 24" )
        logger.RemoveHandler( hdlr )
        logger.LOG( "hello again test 24" )
        
        
