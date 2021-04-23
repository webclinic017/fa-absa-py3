"""-----------------------------------------------------------------------------
PROJECT                 :  Security Borrowing and Lending
PURPOSE                 :  Process log class used to build formatted log 
                           messages
DEPATMENT AND DESK      :  Prime Services, Securities Lending
REQUESTER               :  Linda Breytenbach
DEVELOPER               :  Francois Truter
CR NUMBER               :  494829
-----------------------------------------------------------------------------

HISTORY
=============================================================================
Date       Change no Developer          Description
-----------------------------------------------------------------------------
2010-11-16 494829    Francois Truter    Initial Implementation
2012-12-11 620455    Peter Fabian       Added method to print just errors from the log
2013-04-02 951379    Peter Fabian       Added method to print just warnings from the log
"""

from datetime import datetime
import traceback
import string

class ProcessLogException(Exception): pass

class ProcessLog:
    NEWLINE = '\n'
    SPACE = ' '
    LINE = '-' * 80 + NEWLINE

    class _ProcessLogMessageType:
        Information = 'Information'
        Warning = 'Warning'
        Error = 'Error'
        Exception = 'Exception'

    class _ProcessLogMessage:

        def __str__(self):
            prefix = '%(time)s %(type)-11s : ' % {'time': ProcessLog._strTime(self._time), 'type': self._type}
            message = string.replace(self._message, ProcessLog.NEWLINE, ProcessLog.NEWLINE + ProcessLog.SPACE * len(prefix))
            return prefix + message

        def __init__(self, messageType, message):
            self._type = messageType
            self._message = message
            self._time = datetime.now()

    @staticmethod
    def _strTime(time):
        return time.strftime('%Y-%m-%d %H:%M:%S')

    def _getHeader(self):
        now = datetime.now()
        output = ProcessLog.LINE
        output += '%(name)s started at %(time)s' % {'name': self._name, 'time': ProcessLog._strTime(self._startTime)} + ProcessLog.NEWLINE
        output += 'Current time: %s' % ProcessLog._strTime(now) + ProcessLog.NEWLINE
        output += 'Time elapsed: %s' % str(now - self._startTime) + ProcessLog.NEWLINE
        output += ProcessLog.LINE
        return output

    def _getNotes(self):
        output = ''
        if self._exception:
            output += '!!!A serious error has occurred and this process has been stopped. Please review the message log for the EXCEPTION that caused this!!!' + ProcessLog.NEWLINE
        if self._errors:
            output += '%(number)i %(message)s logged. Please review the log messages and take corrective action.' % \
                {'number': self._errors, 'message': 'ERROR was' if self._errors == 1 else 'ERRORS were'} + ProcessLog.NEWLINE
        if self._warnings:
            output += '%(number)i %(message)s logged. Please review the log messages.' % \
                {'number': self._warnings, 'message': 'warning was' if self._warnings == 1 else 'warnings were'} + ProcessLog.NEWLINE
        if self._exception or self._errors or self._warnings:
            output += ProcessLog.LINE
        return output

    def _getMessages(self):
        output = 'Log Messages:' + ProcessLog.NEWLINE
        output += '-' * len(output) + ProcessLog.NEWLINE
        if not self._messages:
            output += 'No messages.'
        for message in self._messages:
            output += str(message) + ProcessLog.NEWLINE
        output += ProcessLog.LINE
        return output

    def __str__(self):
        output = self._getHeader()
        output += self._getNotes()
        output += self._getMessages()
        return output

    def __init__(self, name):
        self._name = name
        self._messages = []
        self._exception = False
        self._errors = 0
        self._warnings = 0
        self._startTime = datetime.now()

    def _log(self, type, message):
        logMessage = ProcessLog._ProcessLogMessage(type, message)
        self._messages.append(logMessage)
        print(logMessage)

    def HasErrors(self):
        return self._exception or self._errors or self._warnings

    def Information(self, message):
        self._log(ProcessLog._ProcessLogMessageType.Information, message)

    def Warning(self, message):
        self._log(ProcessLog._ProcessLogMessageType.Warning, message)
        self._warnings += 1

    def Error(self, message):
        self._log(ProcessLog._ProcessLogMessageType.Error, message)
        self._errors += 1

    def PrintErrors(self):
        print(self.GetErrors())

    def GetErrors(self):
        return self._GetMsgType(ProcessLog._ProcessLogMessageType.Error)
    
    def _GetMsgType(self, msgType):
        msgs = ""
        for logMessage in self._messages:
            if logMessage._type == msgType:
                msgs += str(logMessage) + "\n"
        return msgs

    def GetWarnings(self):
        return self._GetMsgType(ProcessLog._ProcessLogMessageType.Warning)
    
    def PrintWarnings(self):
        print(self.GetWarnings())

    def GetExceptions(self):
        return self._GetMsgType(ProcessLog._ProcessLogMessageType.Exception)
        
    def _logException(self, message, limit):
        tracebackLines = traceback.format_stack(None, limit)
        if len(tracebackLines) > 2:
            message += ProcessLog.NEWLINE
            for line in tracebackLines[0:len(ProcessLog.NEWLINE) - 3]:
                message += line
        self._log(ProcessLog._ProcessLogMessageType.Exception, message)
        self._exception = True

    def Exception(self, message):
        self._logException(message, 3)

    def RaiseException(self, message, _raise=True):
        if _raise:
            try:
                raise ProcessLogException(message)
            except Exception, ex:
                self._logException(message, 3)
                raise ex
        else:
            self.Error(message)
