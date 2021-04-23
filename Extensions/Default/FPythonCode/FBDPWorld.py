""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/common/FBDPWorld.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------

"""----------------------------------------------------------------------------
MODULE

    FBDPWorld.py - Logging and containers required by BDP

DESCRIPTION

ENDDESCRIPTION
----------------------------------------------------------------------------"""

import collections
import time
import os
import smtplib
import numbers


import acm


_WORLD_STORE_TOP_N_ERR_MSGS = 20
_WORLD_STORE_TOP_N_WARN_MSGS = 20


def CreateWorld(execParam):
    if 'ScriptName' not in execParam:
        execParam['ScriptName'] = ''
    if 'Logmode' not in execParam:
        execParam['Logmode'] = 0
    if 'LogToConsole' not in execParam:
        execParam['LogToConsole'] = True
    if 'LogToFile' not in execParam:
        execParam['LogToFile'] = False

    if 'Logfile' not in execParam:
        execParam['Logfile'] = ''
    else:
        #To enable enviroment variables in path
        try:
            execParam['Logfile'] = os.path.expandvars(execParam['Logfile'])
        except:
            pass

    if 'SendReportByMail' not in execParam:
        execParam['SendReportByMail'] = False
    if 'MailList' not in execParam:
        execParam['MailList'] = ''
    if 'ReportMessageType' not in execParam:
        execParam['ReportMessageType'] = 0
    if 'Testmode' not in execParam:
        execParam['Testmode'] = False
    return World(execParam)


class World(object):

    def __init__(self, execParam):

        self.__warnMsgList = []
        self.__errMsgList = []
        # Make log param
        logParam = _LogParam(scriptName=execParam['ScriptName'],
                logMode=execParam['Logmode'],
                logToConsole=execParam['LogToConsole'],
                logToFile=execParam['LogToFile'],
                logFile=execParam['Logfile'],
                sendReportByMail=execParam['SendReportByMail'],
                mailList=execParam['MailList'],
                reportMessageType=execParam['ReportMessageType'])
        self.__logger = _Logger(logParam)
        self.__summary = _Summary(self.__logger, execParam)
        self.__isTestMode = bool(execParam.get('Testmode', 0))

    def countErrorMessages(self):
        """
        Count the number of ERROR message
        """
        return len(self.__errMsgList)

    def retrieveErrorMessagesAfter(self, errMsgFrom):
        """
        Retrieve ERROR messages on and after the errMsgFrom(th).
        """
        totalErrMsgs = len(self.__errMsgList)
        assert isinstance(errMsgFrom, int), ('The given errMsgFrom must be '
                'integer, but {0} is given.'.format(errMsgFrom))
        assert errMsgFrom >= 0, ('The given errMsgFrom must be non-negative, '
                'but {0} is given.'.format(errMsgFrom))
        assert errMsgFrom <= totalErrMsgs, ('The give errMsgFrom {0} must not '
                'be greater than current total number of error messages '
                '{1}.'.format(totalErrMsgs, totalErrMsgs))
        return self.__errMsgList[errMsgFrom:]

    def hasAnyErrorMessage(self):
        """
        Has there been any ERROR message?
        """
        return bool(self.__errMsgList)

    def countWarningMessages(self):
        """
        Count the number of WARNING message
        """
        return len(self.__warnMsgList)

    def retrieveWarningMessagesAfter(self, warnMsgFrom):
        """
        Retrieve WARNING messages on and after the warnMsgFrom(th).
        """
        totalWarnMsgs = len(self.__warnMsgList)
        assert isinstance(warnMsgFrom, int), ('The given warnMsgFrom must be '
                'integer, but {0} is given.'.format(warnMsgFrom))
        assert warnMsgFrom >= 0, ('The given warnMsgFrom must be '
                'non-negative, but {0} is given.'.format(warnMsgFrom))
        assert warnMsgFrom <= totalWarnMsgs, ('The give warnMsgFrom {0} must '
                'not be greater than current total number of warning messages '
                '{1}.'.format(totalWarnMsgs, totalWarnMsgs))
        return self.__warnMsgList[warnMsgFrom:]

    def isInTestMode(self):
        """
        Is in TestMode?
        """
        return bool(self.__isTestMode)

    def listTopErrorMessages(self):
        """
        Print each error message in the self._errMsgList to the error log.
        """
        if self.__errMsgList:
            numTopErrMsgs = len(self.__errMsgList)
            if numTopErrMsgs > _WORLD_STORE_TOP_N_ERR_MSGS:
                numTopErrMsgs = _WORLD_STORE_TOP_N_ERR_MSGS
            self.__logger.logError('*********** List of Error Messages '
                    '(Maximum of {0} will be displayed) '
                    '***************'.format(numTopErrMsgs))
            for errMsg in self.__errMsgList[0:numTopErrMsgs]:
                self.__logger.logError(errMsg)

    def listTopWarningMessages(self):
        """
        Print each warning message in the self._warnMsgList to the warning log.
        """
        if self.__warnMsgList:
            numTopWarnMsgs = len(self.__warnMsgList)
            if numTopWarnMsgs > _WORLD_STORE_TOP_N_WARN_MSGS:
                numTopWarnMsgs = _WORLD_STORE_TOP_N_WARN_MSGS
            self.__logger.logWarning('*********** List of Warning Messages '
                    '(Maximum of {0} will be displayed) '
                    '***************'.format(numTopWarnMsgs))
            for warnMsg in self.__warnMsgList[0:numTopWarnMsgs]:
                self.__logger.logWarning(warnMsg)

    def logDebug(self, msg):
        """
        Log a DEBUG message.
        """
        self.__logger.logDebug(msg)

    def logError(self, msg):
        """
        Log an ERROR message.
        """
        self.__logger.logError(msg)
        self.__errMsgList.append(msg)

    def logFinish(self, msg):
        """
        Log a FINISH message.
        """
        self.__logger.logFinish(msg)

    def logInfo(self, msg):
        """
        Log an INFO message.
        """
        self.__logger.logInfo(msg)

    def logNoTime(self, msg):
        """
        Log a NOTIME message.
        """
        self.__logger.logNoTime(msg)

    def logStart(self, msg):
        """
        Log a START message.
        """
        self.__logger.logStart(msg)

    def logWarning(self, msg):
        """
        Log a WARNING message.
        """
        self.__logger.logWarning(msg)
        self.__warnMsgList.append(msg)

    def summaryAddOk(self, recType, oid, action, reasons=None):
        """
        Make summary object aware that an action on an object had been okay.
        The oid can be integer or a tuple of integers.
        """
        self.__summary.ok(recType, oid, action, reasons)

    def summaryAddFail(self, recType, oid, action, reasons):
        """
        Make summary object aware that an action on an object had been failed.
        The oid can be integer or a tuple of integers.
        """
        self.__summary.fail(recType, oid, action, reasons)

    def summaryAddIgnore(self, recType, oid, action, reasons):
        """
        Make summary object aware that an action on an object had been ignored.
        The oid can be integer or a tuple of integers.
        """
        self.__summary.ignore(recType, oid, action, reasons)

    def summarySummarise(self):
        """
        Make summary object to summarise.
        """
        self.__summary.summarise()


class WorldInterface(object):

    def __init__(self, world):
        assert isinstance(world, World), ('The given \'world\' must be '
                'an instance of FBDPWorld.')
        self.__world = world

    def _getWorldRef(self):
        return self.__world

    def _countErrorMessages(self):
        """
        Count the number of ERROR messages.
        """
        return self.__world.countErrorMessages()

    def _retrieveErrorMessagesAfter(self, errMsgFrom):
        """
        Retrieve error messages on and after the errMsgFrom(th) error messages.
        """
        return self.__world.retrieveErrorMessagesAfter(errMsgFrom)

    def _hasAnyErrorMessage(self):
        """
        Has there been any ERROR message?
        """
        return self.__world.hasAnyErrorMessage()

    def _countWarningMessages(self):
        """
        Count the number of WARNING messages.
        """
        return self.__world.countWarningMessages()

    def _retrieveWarningMessagesAfter(self, warnMsgFrom):
        """
        Retrieve WARNING messages on and after the warnMsgFrom(th).
        """
        return self.__world.retrieveWarningMessagesAfter(warnMsgFrom)

    def _isInTestMode(self):
        """
        Is in TestMode?
        """
        return self.__world.isInTestMode()

    def _listTopErrorMessages(self):
        """
        Print each error message in the self._errMsgList to the error log.
        """
        self.__world.listTopErrorMessages()

    def _listTopWarningMessages(self):
        """
        Print each warning message in the self._warnMsgList to the warning log.
        """
        self.__world.listTopWarningMessages()

    def _logDebug(self, msg):
        """
        Log a DEBUG message.
        """
        self.__world.logDebug(msg)

    def _logError(self, msg):
        """
        Log an ERROR message.
        """
        self.__world.logError(msg)

    def _logFinish(self, msg):
        """
        Log a FINISH message.
        """
        self.__world.logFinish(msg)

    def _logInfo(self, msg):
        """
        Log an INFO message.
        """
        self.__world.logInfo(msg)

    def _logNoTime(self, msg):
        """
        Log a NOTIME message.
        """
        self.__world.logNoTime(msg)

    def _logStart(self, msg):
        """
        Log a START message.
        """
        self.__world.logStart(msg)

    def _logWarning(self, msg):
        """
        Log a WARNING message.
        """
        self.__world.logWarning(msg)

    def _summaryAddOk(self, *args, **kwargs):
        """
        Make summary object aware that an action on an object had been okay.
        """
        self.__world.summaryAddOk(*args, **kwargs)

    def _summaryAddFail(self, *args, **kwargs):
        """
        Make summary object aware that an action on an object had been failed.
        """
        self.__world.summaryAddFail(*args, **kwargs)

    def _summaryAddIgnore(self, *args, **kwargs):
        """
        Make summary object aware that an action on an object had been ignored.
        """
        self.__world.summaryAddIgnore(*args, **kwargs)

    def _summarySummarise(self):
        """
        Make summary object to summarise.
        """
        self.__world.summarySummarise()


# #############################################################################
# Logger
# #############################################################################

# -----------------------------------------------------------------------------
#        msgType    string      Type of message
#                    'INFO'  -   Information (default)
#                    'WARNING' - Anything making a task being fulfilled in an
#                                unusual way.
#                    'ERROR' -   Anything making a task not being fulfilled.
#                    'START' -   Also date and time will be printed
#                    'FINISH'-   Script finished successfully
#                    'ABORT' -   Script aborted due to error
#                    'DEBUG' -   For developer purposes
# -----------------------------------------------------------------------------

_LOG_MODE_0_TYPES = ('START', 'FINISH', 'ABORT', 'ERROR', 'WARNING', 'NOTIME')
_LOG_MODE_1_TYPES = ('START', 'FINISH', 'ABORT', 'ERROR', 'WARNING', 'NOTIME',
       'INFO', 'NOTIME_INFO')
_LOG_MODE_2_TYPES = ('START', 'FINISH', 'ABORT', 'ERROR', 'WARNING', 'NOTIME',
       'INFO', 'NOTIME_INFO', 'DEBUG', 'NOTIME_DEBUG')

# -----------------------------------------------------------------------------
#        ScriptName      name of the current script
#        LogMode -       how extensive the logging will be.
#        LogToConsole -  if logging will be done to console or not
#        LogToFile -     if logging will be done to the file <Logfile>
#        Logfile -       full path to the file where logging will be done.
#                        (if only filename file will be placed in default
#                        directory, i.e. FBDPParameters.Logdir)
# -----------------------------------------------------------------------------

_LogParam = collections.namedtuple('_LogParam', ('scriptName logMode '
        'logToConsole logToFile logFile sendReportByMail mailList '
        'reportMessageType'))


def _nowDateTime():
    """
    Returns a sting with current date and time in the format
    YYYY-MM-DD HH:MM:SS, for example: 2003-01-22 10:12:43
    """
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def _nowTime():
    """
    Returns a sting with current time in the format HH:MM:SS, for example:
    10:12:43
    """
    return time.strftime('%H:%M:%S', time.localtime(time.time()))


class _FileWriter(object):
    """
    Helper class for _Logger
    """

    def __init__(self, validLogFilePath):
        self.__validLogFilePath = validLogFilePath

    @staticmethod
    def getValidLogFilePath(scriptName, logFile):
        """
        Helper function for setting full path to the logFile
        """
        pathPart, filePart = os.path.split(logFile)
        # Try determine default log directory.
        try:
            import FBDPGui
            defaultLogDir = FBDPGui.defaultLogDir()
        except ImportError as e:
            print(('\nUnable to find default log directory from FBDPGui.  '
                    'Exception: {0}'.format(e)))
            defaultLogDir = 'c:\\Temp\\'
        # Find out the path part for the log file.
        if os.path.isdir(pathPart):
            # The path is not OK or not provided
            pass
        elif os.path.isdir(defaultLogDir):
            # The path is not OK, use default from FBDPParameters
            pathPart = defaultLogDir
        else:
            # The path is not OK or not provided and default log is no good.
            os.chdir(os.pardir)
            print(('\nNo valid path found in your logging settings, please '
                    'check your logging settings.  Will use {0}.\n'.format(
                    os.getcwd())))
            pathPart = os.curdir
        # Find out the file part of the log file
        if not filePart:
            filePart = 'BDP_' + scriptName + '.log'
        # Make out the full path and file part of the log file.
        return os.path.join(pathPart, filePart)

    def writeToFile(self, msg):
        """
        Write msg to the file
        """
        try:
            lf = open(self.__validLogFilePath, 'a')
        except IOError:
            print(('\nERROR:\tFailed to open logfile {0}\n'.format(
                    self.__validLogFilePath)))
            raise
        lf.write(msg + '\n')
        lf.close()


class _MailBuffer(object):
    """
    Helper class for _Logger
    """

    def __init__(self, logger, scriptName, mailList, reportMessageType):
        self.__buffer = []  # Initialise to empty list.  Will be set to None
                            # after flushed.
        self.__logger = logger
        self.__scriptName = scriptName
        self.__mailList = mailList
        self.__reportMessageType = reportMessageType

    def writeToBuffer(self, msgType, msg):
        """
        Write msg to the buffer if its msgType is to be reported.
        """
        # After buffer flushed self.__buffer will be None
        if self.__buffer is None:
            return
        if (('Full Log' in self.__reportMessageType) or
                (msgType in self.__reportMessageType)):
            self.__buffer.append((msgType, msg + '\n'))

    def __buildMailSubjectAndMailMsgFromBuffer(self):
        """
        Build the mail subject and mail msg from the buffer.
        """
        hasError = False
        mailMsg = ''
        for msgType, msg in self.__buffer:
            mailMsg += msg
            if msgType == 'ERROR':
                hasError = True
        # Has error
        if hasError:
            mailSubject = ('BDP Script {0} failed to complete.'.format(
                    self.__scriptName))
        else:
            mailSubject = ('BDP Script {0} finished successfully.'.format(
                    self.__scriptName))
        return mailSubject, mailMsg

    def flushBufferAndSendMail(self):
        """
        Flush the buffer to a mail and send the mail out.
        """
        mailSubject, mailMsg = self.__buildMailSubjectAndMailMsgFromBuffer()
        # Flush buffer
        self.__buffer = None
        # No message to send
        if not mailMsg:
            return
        # Have message to send. Build the mail
        mailHost = acm.GetCalculatedValue(0, acm.GetDefaultContext().Name(),
                'mailServerAddress').Value()
        mailFrom = 'PRIME client'
        mailBody = '\r\n'.join(['From: {0}'.format(mailFrom),
                'To: {0}'.format(self.__mailList),
                'Subject: {0}'.format(mailSubject), '{0}'.format(mailMsg)])
        if not mailHost:
            self.__logger.logInfo('No mail server address specified!\n Please '
                    'specify your mail server name or IP address in the '
                    'extension attribute mailServerAddress!')
        try:
            server = smtplib.SMTP(mailHost)
            server.sendmail(mailFrom, self.__mailList.split(','), mailBody)
            server.quit()
            self.__logger.logInfo('Mail sent to: {0}'.format(self.__mailList))
        except smtplib.SMTPException:
            self.__logger.logInfo('Failed sending mail.')


class _Logger(object):
    """
    The Logger
    """

    def __init__(self, logParam):
        """
        Function for initializing logging variables.
        """
        assert isinstance(logParam, _LogParam)
        self.__scriptName = str(logParam.scriptName)
        self.__logMode = int(logParam.logMode)
        if self.__logMode >= 2:
            self.__typesToLog = _LOG_MODE_2_TYPES
        elif self.__logMode >= 1:
            self.__typesToLog = _LOG_MODE_1_TYPES
        else:
            self.__typesToLog = _LOG_MODE_0_TYPES
        # For log to console
        self.__logToConsole = bool(logParam.logToConsole)
        # For log to file
        logToFile = bool(logParam.logToFile)
        if logToFile:
            logFile = str(logParam.logFile)
            validLogFilePath = _FileWriter.getValidLogFilePath(
                self.__scriptName, logFile)
            self.__fileWriter = _FileWriter(validLogFilePath)
        else:
            self.__fileWriter = None
        # For log to mail
        self.__sendReportByMail = bool(logParam.sendReportByMail)
        if self.__sendReportByMail:
            self.__mailBuffer = _MailBuffer(self, self.__scriptName,
                    str(logParam.mailList), str(logParam.reportMessageType))
        else:
            self.__mailBuffer = None
        # Special case.  If not going to log to either console, file or mail
        # Set self.__typesToLog to empty list so nothing will be logged.
        if ((not self.__logToConsole) and (not self.__fileWriter) and
                (not self.__mailBuffer)):
            self.__typesToLog = []

    def getLogMode(self):
        """
        Get the log mode.
        """
        return self.__logMode

    def __addPrefixToMsg(self, msg, msgType):
        if msgType in ['ERROR', 'WARNING']:
            msg = _nowTime() + ' ' + msgType + ': ' + msg
        elif msgType in ['START', 'FINISH', 'ABORT']:
            line = 45 * '-'
            if 'START' in msgType:
                msg = '\n%s\n%s STARTED %s' % (line, self.__scriptName,
                        _nowDateTime())
            elif 'FINISH' in msgType:
                msg = '\n%s FINISHED %s \n%s' % (self.__scriptName,
                        _nowDateTime(), line)
            elif 'ABORT' in msgType:
                msg = '%s ABORTED %s \n%s' % (self.__scriptName,
                        _nowDateTime(), line)
                self.__mailBuffer = None
        elif 'NOTIME' in msgType:
            pass
        elif msgType in ['INFO', 'DEBUG']:
            msg = _nowTime() + ' ' + msg
        else:
            # For development only
            print(('UNKNOWN MESSAGE TYPE: {0}'.format(msgType)))
            print(('MESSAGE: {0}'.format(msg)))
            msg = _nowTime + ' ' + msg
        return msg

    def __log(self, msg, msgType):
        """
        Log to file or console, see class description for more info.
        """
        if msgType in self.__typesToLog:
            msg = self.__addPrefixToMsg(msg, msgType)
            # Log to Console
            if self.__logToConsole:
                print(msg)
            # Log to file
            if self.__fileWriter:
                self.__fileWriter.writeToFile(msg)
            # Log to mail
            if self.__mailBuffer:
                self.__mailBuffer.writeToBuffer(msgType, msg)
                if msgType == 'FINISH':
                    self.__mailBuffer.flushBufferAndSendMail()
                    self.__mailBuffer = None

    def logAbort(self, msg):
        """
        Log an ABORT message.
        """
        self.__log(str(msg), 'ABORT')

    def logDebug(self, msg):
        """
        Log a DEBUG message.
        """
        self.__log(str(msg), 'DEBUG')

    def logError(self, msg):
        """
        Log an ERROR message.
        """
        self.__log(str(msg), 'ERROR')

    def logFinish(self, msg):
        """
        Log a FINISH message.
        """
        self.__log(str(msg), 'FINISH')

    def logInfo(self, msg):
        """
        Log an INFO message.
        """
        self.__log(str(msg), 'INFO')

    def logNoTime(self, msg):
        """
        log a NOTIME message.
        """
        self.__log(str(msg), 'NOTIME')

    def logStart(self, msg):
        """
        log a START message.
        """
        self.__log(str(msg), 'START')

    def logWarning(self, msg):
        """
        Log a WARNING message.
        """
        self.__log(str(msg), 'WARNING')


# #############################################################################
# Summary
# #############################################################################


_SUMMARY_RESULT_OK = 'ok'
_SUMMARY_RESULT_IGNORE = 'ignored'
_SUMMARY_RESULT_FAIL = 'failed'


def _convertDurationInSecondsToHoursMinutesSeconds(timeInSeconds):
    timeInSeconds = int(timeInSeconds)
    mins = timeInSeconds // 60
    hrs = mins // 60
    return '{0:02d}:{1:02d}:{2:02d}'.format(hrs, mins % 60, timeInSeconds % 60)


def _toNameFlattenedString(obj):

    if hasattr(obj, 'Name') and callable(obj.Name):
        return obj.Name()
    if hasattr(obj, '__iter__'):
        nfsList = [_toNameFlattenedString(i) for i in obj]
        return '[{0}]'.format(','.join(nfsList))
    return str(obj)


class _Summary(object):

    def __init__(self, logger, execParam):
        self.__logger = logger
        self.__table = OrderedDict()
        self.__startTime = time.time()
        self.__execParam = execParam
        self.__statsTableEntityTypeCmp = None
        self.__statsTableEntityTypeActionCmpMap = {}

    __ResultAndReasons = collections.namedtuple('__ResultAndReasons',
            'result reasons')

    __StatReportEntry = collections.namedtuple('__StatReportEntry',
            'recType action numOk numFail numIgnore')

    __FailedReasons = collections.namedtuple('__FailedReasons',
            'recType action oid reasons')

    __IgnoredReasons = collections.namedtuple('__IgnoredReasons',
            'recType action oid reasons')

    def __record(self, recType, action, oid, result, reasons):
        """
        Record the entry (recType, action, oid, result, reasons) into the
        table.  The entry is placed into data structure by having named tuple
        (result, reasons) placed in the three-level dictionary accessed by
        recType, action and then by oid.  That is,
        self.__table[recType][action][id] = (result, reasons)
        """
        # Index level 1 - recType.  e.g. Instrument, Trade, CashFlow,... etc.
        assert (reasons is None) or isinstance(reasons, list), ('Not None '
                'nor List')
        assert result in [_SUMMARY_RESULT_OK, _SUMMARY_RESULT_IGNORE,
                _SUMMARY_RESULT_FAIL], ('Result not right')
        assert isinstance(oid, (numbers.Integral, tuple)), (
                'The given oid must be an '
                'integer or a tuple of integers, but \'{0}\' is '
                'given.'.format(oid))
        if isinstance(oid, tuple):
            for i in oid:
                assert isinstance(i, numbers.Integral), (
                        'The given oid must be an '
                        'integer or a tuple of integers, but \'{0}\' is '
                        'given.'.format(oid))
        assert isinstance(action, str), 'action not string'
        i1 = self.__table
        if recType not in i1:
            i1[recType] = OrderedDict()
        # Index level 2 - action.  e.g. INSPECT, PROCESS, ARCHIVE,
        # DEARCHIVE,... etc.
        i2 = i1[recType]
        if action not in i2:
            i2[action] = {}  # no need to be ordered dict
        # Index level 3 - oid.  e.g. trdnbr for trades, insaddr for
        # instruments,... etc.
        i3 = i2[action]
        if oid in i3 and i3[oid].result is not result:
            self.__logger.logWarning('Summary statistic had previously '
                    'recorded object (recType={0}, oid={1}) having action '
                    '{2} reported {3}, but now overwritten by with result '
                    '{4}.'.format(recType, self._strColonSeparatedOid(oid),
                    action, i3[oid].result, result))
            del i3[oid]
        if oid not in i3:
            i3[oid] = self.__ResultAndReasons(result=result, reasons=reasons)
        else:
            if result is not _SUMMARY_RESULT_OK:
                i3[oid].reasons.extend(reasons)

    def __audit(self):
        """
        Audit through the table and generate the statistics report.  For each
        valid (recType, action), it counts number of ok'd, ignored and failed
        oids.  Then it returns them for each (recType, action) in a list.
        """
        statReport = []
        ignoredReasonReport = []
        failedReasonReport = []
        i1 = self.__table
        for recType in i1.keys():
            i2 = i1[recType]
            for action in i2.keys():
                i3 = i2[action]
                numOk = 0
                numIgnore = 0
                numFail = 0
                for oid in sorted(i3.keys()):
                    result = i3[oid].result
                    if result is _SUMMARY_RESULT_OK:
                        numOk += 1
                    if result is _SUMMARY_RESULT_IGNORE:
                        numIgnore += 1
                        ignoredReasonReport.append(self.__IgnoredReasons(
                                recType=recType, action=action, oid=oid,
                                reasons=i3[oid].reasons))
                    if result is _SUMMARY_RESULT_FAIL:
                        numFail += 1
                        failedReasonReport.append(self.__FailedReasons(
                                recType=recType, action=action, oid=oid,
                                reasons=i3[oid].reasons))
                statReport.append(self.__StatReportEntry(recType=recType,
                        action=action, numOk=numOk, numIgnore=numIgnore,
                        numFail=numFail))
        return failedReasonReport, ignoredReasonReport, statReport

    def ok(self, recType, oid, action, reasons=None):
        """
        Tell the summary an action on an object has been okay'ed.
        The oid can be integer or a tuple of integers.
        """
        # Note, for _SUMMARY_RESULT_OK, usually don't need a reason, hence
        # reasons default to None.
        self.__record(recType, action, oid, _SUMMARY_RESULT_OK, reasons)

    def ignore(self, recType, oid, action, reasons):
        """
        Tell the summary an action on an object has been ignored.
        The oid can be integer or a tuple of integers.
        """
        self.__record(recType, action, oid, _SUMMARY_RESULT_IGNORE, reasons)

    def fail(self, recType, oid, action, reasons):
        """
        Tell the summary an action on an object has failed.
        The oid can be integer or a tuple of integers.
        """
        self.__record(recType, action, oid, _SUMMARY_RESULT_FAIL, reasons)

    def summarise(self):
        """
        Write the summary
        """
        self.__writeSummaryHeader()
        self.__writeSummaryExecutionParameters()
        failedReasonReport, ignoredReasonReport, statReport = self.__audit()
        self.__writeSummaryFailedReasons(failedReasonReport)
        self.__writeSummaryIgnoredReasons(ignoredReasonReport)
        self.__writeSummaryActionStatistics(statReport)

    @staticmethod
    def _strColonSeparatedOid(oid):
        """
        Returns a colon separated string to represent the oid.  The oid can be
        integer or a tuple of integers.
        """
        ss = None
        if isinstance(oid, tuple):
            ss = [str(i) for i in oid]
        else:
            ss = [str(oid)]
        return ':'.join(ss)

    def __writeSummaryHeader(self):
        """
        Build header part of the summary string and write it to the log.
        """
        s = '\n'
        s += '{0} S U M M A R Y {0}\n'.format('------------------------------')
        s += '\n'
        s += 'Report date: {0}\n'.format(acm.Time.DateToday())
        s += '\n'
        s += 'Execution time (hh:mm:ss): {0}\n'.format(
                _convertDurationInSecondsToHoursMinutesSeconds(
                time.time() - self.__startTime))
        self.__logger.logNoTime(s)

    def __writeSummaryExecutionParameters(self):
        """
        Build execution parameter part of the summary string and write it to
        the log.
        """
        s = 'Execution parameters:\n'
        keys = self.__execParam.keys()
        keys = [(x.upper(), x) for x in keys]
        keys.sort()
        for k in keys:
            x = self.__execParam[k[1]]
            v = _toNameFlattenedString(x)
            if len(v) > 60:
                v = v[0:60] + '...'
            s += '   {0}: {1}\n'.format(k[1], v)
            if k[0] == 'LOGFILE' and 'LogPath' in dir(self.__logger):
                s += '   {0}: {1}\n'.format('Logpath', self.__logger.LogPath)
        self.__logger.logNoTime(s)

    def __writeSummaryFailedReasons(self, failedReasonReport):
        """
        Build failed reasons part of the summary string and write it to the
        log.
        """
        s = 'Failed Reasons:\n'
        if failedReasonReport:
            for fr in failedReasonReport:
                s += '    {0} {1} {2} failed.\n'.format(fr.action, fr.recType,
                          self._strColonSeparatedOid(fr.oid))
                for reason in fr.reasons:
                    s += '            {0}\n'.format(reason)
        else:
            s += '    None.\n'
        self.__logger.logNoTime(s)

    def __writeSummaryIgnoredReasons(self, ignoredReasonReport):
        """
        Build ignore reasons part of the summary string and write it to the
        log.
        """
        s = 'Ignored Reasons:\n'
        if ignoredReasonReport:
            for ir in ignoredReasonReport:
                s += '    {0} {1} {2} ignored.\n'.format(ir.action, ir.recType,
                          self._strColonSeparatedOid(ir.oid))
                for reason in ir.reasons:
                    s += '            {0}\n'.format(reason)
        else:
            s += '    None.\n'
        self.__logger.logNoTime(s)

    def __writeSummaryActionStatistics(self, statReport):
        """
        build action statistics part of the summary string and write it to the
        log.
        """
        s = 'ENTITY                   ACTION         OK     FAILED   IGNORED\n'
        s += '{0}{0}\n'.format('---------------------------------')
        for entry in statReport:
            s += '{0:<25}{1:<15}{2:<9}{3:<9}{4:<9}\n'.format(entry.recType,
                    entry.action, entry.numOk, entry.numFail, entry.numIgnore)
        s += '{0}{0}\n'.format('---------------------------------')
        self.__logger.logNoTime(s)


# #############################################################################
# OrderedDict
# The followings is a chopped-down version of that taken from the python 2.7
# standard library.
# !!! Remove the following code once migrate to 2.7 or above !!!
# #############################################################################


from collections import MutableMapping


class OrderedDict(dict):
    """
    Dictionary that remembers insertion order
    """
    # An inherited dict maps keys to values.
    # The inherited dict provides __getitem__, __len__, __contains__, and get.
    # The remaining methods are order-aware.
    # Big-O running times for all methods are the same as for regular
    # dictionaries.

    # The internal self.__map dictionary maps keys to links in a doubly
    # linked list.
    # The circular doubly linked list starts and ends with a sentinel element.
    # The sentinel element never gets deleted (this simplifies the algorithm).
    # Each link is stored as a list of length three:  [PREV, NEXT, KEY].

    def __init__(self, *args, **kwds):
        """Initialize an ordered dictionary.  Signature is the same as for
        regular dictionaries, but keyword arguments are not recommended
        because their insertion order is arbitrary.
        """
        if len(args) > 1:
            raise TypeError('expected at most 1 arguments, got %d' % len(args))
        try:
            self.__root
        except AttributeError:
            self.__root = root = [None, None, None]     # sentinel node
            PREV = 0
            NEXT = 1
            root[PREV] = root[NEXT] = root
            self.__map = {}
        self.__update(*args, **kwds)

    def __setitem__(self, key, value, PREV=0, NEXT=1,
            dict_setitem=dict.__setitem__):
        """
        od.__setitem__(i, y) <==> od[i]=y
        """
        # Setting a new item creates a new link which goes at the end of the
        # linked list, and the inherited dictionary is updated with the new
        # key/value pair.
        if key not in self:
            root = self.__root
            last = root[PREV]
            last[NEXT] = root[PREV] = self.__map[key] = [last, root, key]
        dict_setitem(self, key, value)

    def __delitem__(self, key, PREV=0, NEXT=1,
            dict_delitem=dict.__delitem__):
        """
        od.__delitem__(y) <==> del od[y]
        """
        # Deleting an existing item uses self.__map to find the link which is
        # then removed by updating the links in the predecessor and successor
        # nodes.
        dict_delitem(self, key)
        link = self.__map.pop(key)
        link_prev = link[PREV]
        link_next = link[NEXT]
        link_prev[NEXT] = link_next
        link_next[PREV] = link_prev

    def __iter__(self, NEXT=1, KEY=2):
        """
        od.__iter__() <==> iter(od)
        """
        # Traverse the linked list in order.
        root = self.__root
        curr = root[NEXT]
        while curr is not root:
            yield curr[KEY]
            curr = curr[NEXT]

    def __reduce__(self):
        """
        Return state information for pickling
        """
        items = [[k, self[k]] for k in self]
        tmp = self.__map, self.__root
        del self.__map, self.__root
        inst_dict = vars(self).copy()
        self.__map, self.__root = tmp
        if inst_dict:
            return (self.__class__, (items,), inst_dict)
        return self.__class__, (items,)

    def clear(self):
        """
        od.clear() -> None.  Remove all items from od.
        """
        try:
            for node in self.__map.itervalues():
                del node[:]
            self.__root[:] = [self.__root, self.__root, None]
            self.__map.clear()
        except AttributeError:
            pass
        dict.clear(self)

    update = __update = MutableMapping.update
    keys = MutableMapping.keys
    values = MutableMapping.values
    items = MutableMapping.items
    iterkeys = MutableMapping.iterkeys
    itervalues = MutableMapping.itervalues
    iteritems = MutableMapping.iteritems

#############################################################################
# OrderedSet
# #############################################################################

from collections import MutableSet


class OrderedSet(MutableSet):

    def __init__(self, iterable=None):
        self.end = end = []
        end += [None, end, end]         # sentinel node for doubly linked list
        self.map = {}                   # key --> [key, prev, next]
        if iterable is not None:
            self |= iterable

    def __len__(self):
        return len(self.map)

    def __contains__(self, key):
        return key in self.map

    def add(self, key):
        if key not in self.map:
            end = self.end
            curr = end[1]
            curr[2] = end[1] = self.map[key] = [key, curr, end]

    def discard(self, key):
        if key in self.map:
            key, prev, next = self.map.pop(key)
            prev[2] = next
            next[1] = prev

    def __iter__(self):
        end = self.end
        curr = end[2]
        while curr is not end:
            yield curr[0]
            curr = curr[2]

    def __reversed__(self):
        end = self.end
        curr = end[1]
        while curr is not end:
            yield curr[0]
            curr = curr[1]

    def pop(self, last=True):
        if not self:
            raise KeyError('set is empty')
        key = self.end[1][0] if last else self.end[2][0]
        self.discard(key)
        return key

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))

    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and list(self) == list(other)
        return set(self) == set(other)
