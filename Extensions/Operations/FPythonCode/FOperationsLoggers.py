""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/FOperationsLoggers.py"

import acm, os, types
import tempfile

from FOperationsLogger import Logger
from FOperationsIO import IsValidFileLogParameters
from tempfile import TemporaryFile

#-------------------------------------------------------------------------
def CreateLogger(logToConsole, logToFile, isDetailed, filePath, fileName):

    if logToConsole and logToFile:
        logger = CompositeLogger()
        logger.Add(ConsoleLogger(isDetailed))
        logger.Add(FileLogger(isDetailed, filePath, fileName))
    elif logToConsole:
        logger = ConsoleLogger(isDetailed)
    elif logToFile:
        logger = FileLogger(isDetailed, filePath, fileName)        
    else:
        logger = DummyLogger()

    return logger

#-------------------------------------------------------------------------
# CompositeLogger - Combines 0..m loggers 
#-------------------------------------------------------------------------
class CompositeLogger(Logger):

    #-------------------------------------------------------------------------
    def __init__(self):
        super(CompositeLogger, self).__init__()
        self.__loggers = list()

    #-------------------------------------------------------------------------
    def Loggers(self):
        return self.__loggers

    #-------------------------------------------------------------------------
    def Add(self, logger):
        self.__loggers.append(logger)

    #-------------------------------------------------------------------------
    def Clear(self):
        for logger in self.__loggers:
            logger.Clear()

    #-------------------------------------------------------------------------
    def LP_LogVerbose(self, log):
        for logger in self.__loggers:
            logger.LP_LogVerbose(log)

    #-------------------------------------------------------------------------
    def LP_Log(self, log):
        for logger in self.__loggers:
            logger.LP_Log(log)

    #-------------------------------------------------------------------------
    def LP_Flush(self):
        for logger in self.__loggers:
            logger.LP_Flush()


#-------------------------------------------------------------------------
# DummyLogger - Will not perform any logging 
#-------------------------------------------------------------------------
class DummyLogger(Logger):

    #-------------------------------------------------------------------------
    def __init__(self):
        super(DummyLogger, self).__init__()
        pass

#-------------------------------------------------------------------------
# BufferLogger - Will collect log text in an internal buffer
#-------------------------------------------------------------------------
class BufferLogger(Logger):

    #-------------------------------------------------------------------------
    def __init__(self, isDetailed):
        super(BufferLogger, self).__init__()
        self._logs = list()
        self._isDetailed = isDetailed
    
    #-------------------------------------------------------------------------
    def __IsValidLog(self, log):
        return isinstance(log, types.StringType)
        
    #-------------------------------------------------------------------------    
    def __AppendLog(self, log):
        if self.__IsValidLog(log):
            self._logs.append(log)
        else:
            self._logs.append('ERROR: Invalid log string, expected type string, but got type {}: {}'.format(type(log), str(log)))

    #-------------------------------------------------------------------------
    def IsDetailed(self):
        return self._isDetailed

    #-------------------------------------------------------------------------
    def Clear(self):
        del self._logs[:]
    
    #-------------------------------------------------------------------------    
    def Logs(self):
        return self._logs

    #-------------------------------------------------------------------------
    def LP_LogVerbose(self, log):
        if self._isDetailed:
            self.__AppendLog(log)

    #-------------------------------------------------------------------------
    def LP_Log(self, log):
        self.__AppendLog(log)

#-------------------------------------------------------------------------
# ConsoleLogger - Will log to the console
#-------------------------------------------------------------------------
class ConsoleLogger(BufferLogger):

    #-------------------------------------------------------------------------
    def __init__(self, isDetailed):
        super(ConsoleLogger, self).__init__(isDetailed)

    #-------------------------------------------------------------------------
    def LP_Flush(self):
        if len(self._logs) > 0:
            
            try:
                acm.LogAll('\n'.join(self._logs))
            except Exception as e:
                acm.LogAll('Exception occurred when flushing logs: {}'.format(str(e)))
                
            self.Clear()

#-------------------------------------------------------------------------
# FileLogger - Will log to a specified file
#-------------------------------------------------------------------------
class FileLogger(BufferLogger):

    #-------------------------------------------------------------------------
    def __init__(self, isDetailed, filePath, fileName, temp=False):
        super(FileLogger, self).__init__(isDetailed)
        
        IsValidFileLogParameters(filePath, fileName)
        
        self.__filePath = os.path.join(filePath, fileName)
        
        self.__temp = temp
    
    #-------------------------------------------------------------------------    
    def GetFile(self):
        if self.__temp:
            return tempfile.TemporaryFile()
        else:
            return open(self.__filePath, 'a')

    #-------------------------------------------------------------------------
    def LP_Flush(self):
        if len(self._logs) > 0:
            with self.GetFile() as f:
                for log in self._logs:
                    
                    try:
                        f.write(''.join([log, '\n']))
                    except Exception as e:
                        f.write('Exception occurred when writing log to file: {}'.format(str(e)))
                    
            self.Clear()

#-------------------------------------------------------------------------
# ProxyLogger - Will send the logger to a registered cb
#-------------------------------------------------------------------------
class ProxyLogger(BufferLogger):

    #-------------------------------------------------------------------------
    def __init__(self, isDetailed, logCb):
        super(ProxyLogger, self).__init__(isDetailed)
        self.__logCb = logCb

    #-------------------------------------------------------------------------
    def LP_Flush(self):
        if len(self._logs) > 0:
            
            try:
                self.__logCb('\n'.join(self._logs))
            except Exception as e:
                self.__logCb('Exception occurred when flushing logs: {}'.format(str(e)))
            
            self.Clear()
