""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/common/FBDPString.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------

"""----------------------------------------------------------------------------
MODULE
    FBDPString - Module for handling strings.

DESCRIPTION
    Includes function for logging, parsing, report printing and validating
    parameters.

----------------------------------------------------------------------------"""

import os
import time


import FBDPCurrentContext


class LogmeInstance:
    Instance = None


class LogmeLocal:
    """------------------------------------------------------------------------
    DESCRIPTION
        The function logme in class Logme which logs information to file or
        console.  Logme is actually an instance of class Logme() but works
        exactly as a method. In order to use the logme function you have to
        initialize it's parameters it using it's function setLogmeVar.
        This should be done as early as possible in each script. The variables
        used when calling setLogmeVar should be taken from each script's
        variable file.

        setLogmeVar is initialized called with the variables:
        ScriptName    name of the current script
        LogMode -      how extensive the logging will be.
        LogToConsole -  if logging will be done to console or not
        LogToFile -  if logging will be done to the file <Logfile>
        Logfile -      full path to the file where logging will be done.
                        (if only filename file will be placed in default
                        directory, i.e. FBDPParameters.Logdir)

        If a variable is not supplied when calling setLogmeVar, default values
        from FBDPParameters will be used.

    ARGUMENTS
        msg      string   Text to be logged

        msg_type    string    Type of message
                    'INFO'  -   Information (default)
                    'WARNING' - Anything making a task being fulfilled in an
                                unusual way.
                    'ERROR' -   Anything making a task not being fulfilled.
                    'START' -   Also date and time will be printed
                    'FINISH'-   Script finished successfully
                    'ABORT' -   Script aborted due to error
                    'DEBUG' -   For developer purposes

        Note!If msg_type is 'START', 'ERROR', 'WARNING', 'FINISH' or 'ABORT'
        msg should be set to None.

        Logfile  string   For debugging purposes, if you want some printouts
                                in a certain file.

    USAGE
        In case of a fatal error first an 'ERROR' should be sent followed by
        'ABORT'. For example:
            logme('Instrument %s does not exist' % ins.insid, 'ERROR')
            logme(None, 'ABORT')
            raise RuntimeError
    ------------------------------------------------------------------------"""

    ScriptName = 'common'
    LogmeVarsInitiated = False
    LogBuffert = []

    def setLogmeVar(self, ScriptName, LogMode, LogToConsole, LogToFile,
            Logfile, SendReportByMail, MailList, ReportMessageType):
        """Function for initializing logging variables."""
        self.ScriptName = str(ScriptName)

        try:
            Logfile = os.path.expandvars(Logfile)
        except:
            pass

        self.LogMode = int(LogMode)
        if LogMode >= 0:
            self.LogMsg = ['START', 'FINISH', 'ABORT', 'ERROR', 'WARNING',
                    'NOTIME']
        if LogMode >= 1:
            self.LogMsg = self.LogMsg + ['INFO', 'NOTIME_INFO']
        if LogMode >= 2:
            self.LogMsg = self.LogMsg + ['DEBUG', 'NOTIME_DEBUG']

        self.LogToConsole = LogToConsole is not None and int(LogToConsole)

        self.LogToFile = LogToFile is not None and int(LogToFile)

        if self.LogToFile:
            self.setLogfile(Logfile)

        self.SendReportByMail = (SendReportByMail is not None and
                int(SendReportByMail))

        if self.SendReportByMail:
            self.MailList = str(MailList)
            self.ReportMessageType = str(ReportMessageType)

        FBDPCurrentContext.Summary().clear()
        self.LogmeVarsInitiated = True

    def getLogMode(self):
        if(not self.LogmeVarsInitiated):
            return 2
        return self.LogMode

    def __call__(self, msg, msg_type='INFO', Logfile=None):
        """Log to file or console, see class description for more info."""
        if(not self.LogmeVarsInitiated):
            print('Logme variables not set!')
            print(msg)
            return

        if msg == None:
            msg = self.ScriptName  # In case of START, FINISH and ABORT
        else:
            msg = str(msg)
        # Most cases, may be defined for debug printouts
        if Logfile is None and self.LogToFile:
            Logfile = self.Logfile
            if Logfile is None:              # If still None
                self.setLogfile(None)
                Logfile = self.Logfile

        if msg_type in ['ERROR', 'WARNING']:
            if msg_type == 'ERROR':
                FBDPCurrentContext.Summary().fail(
                        FBDPCurrentContext.Summary().EMPTY,
                        FBDPCurrentContext.Summary().EMPTY, msg, None)
            else:
                FBDPCurrentContext.Summary().warning(
                        FBDPCurrentContext.Summary().EMPTY,
                        FBDPCurrentContext.Summary().EMPTY, msg, None)
            msg = current_time() + ' ' + msg_type + ': ' + msg
        elif msg_type in ['START', 'FINISH', 'ABORT']:
            line = 45 * '-'
            if 'START' in msg_type:
                msg = '\n%s\n%s STARTED %s' % (line, msg, nowstr())
                self.LogBuffert = []
            elif 'FINISH' in msg_type:
                msg = '\n%s FINISHED %s \n%s' % (msg, nowstr(), line)
            elif 'ABORT' in msg_type:
                msg = '%s ABORTED %s \n%s' % (msg, nowstr(), line)
                self.LogBuffert = []
        elif 'NOTIME' in msg_type:
            pass
        elif msg_type in ['INFO', 'DEBUG']:
            msg = current_time() + ' ' + msg
            pass
        else:
            print('UNKNOWN MESSAGE TYPE:', msg_type)  # For development only
            print('MESSAGE:', msg)
            msg = current_time() + ' ' + msg
            msg_type = 'INFO'

        if msg_type in self.LogMsg:
            self.LogBuffert.append((msg_type, msg + '\n'))
            if self.LogToFile:
                try:
                    lf = open(Logfile, 'a')
                except IOError:
                    print('\nERROR:\tFailed to open logfile %s\n' % Logfile)
                    raise

                lf.write(msg + '\n')
                lf.close()

            if self.LogToConsole:
                print(msg)

            if (msg_type == 'FINISH' and self.SendReportByMail and
                    self.MailList):
                import FBDPCommon
                subject = ("BDP Script %s finished successfully." %
                        self.ScriptName)
                MSG = ""
                for (t, m) in self.LogBuffert:
                    if ("Full Log" in self.ReportMessageType or
                            t in self.ReportMessageType):
                        MSG += m
                    if t == "ERROR":
                        subject = ("BDP Script %s failed to complete." %
                                self.ScriptName)
                if MSG:
                    FBDPCommon.sendMail(self.MailList, subject, MSG)
                self.LogBuffert = []

    def setLogfile(self, Logfile):
        """Helper function for setting full path to the Logfile"""
        if Logfile is None:  # Will crash when doing split if this is not done
            Logfile = ''

        pathPart, filePart = os.path.split(Logfile)

        try:
            import FBDPGui
            Logdir = FBDPGui.defaultLogDir()
        except:
            Logdir = "c:\\Temp\\"
        if os.path.isdir(pathPart):  # The path is not OK or not provided
            pass
        elif os.path.isdir(Logdir):  # The path is not OK, use default from
            pathPart = Logdir  # FBDPParameters
        else:
            os.chdir(os.pardir)
            print(('\nNo valid path found in your logging settings, please '
                    'check your logging settings. Will use %s.\n' %
                    os.getcwd()))
            pathPart = os.curdir
        self.LogPath = pathPart
        if filePart:
            self.Logfile = os.path.join(pathPart, filePart)
        else:  # Use the scriptname for creating the name
            filePart = 'BDP_' + self.ScriptName + '.log'
            self.Logfile = os.path.join(pathPart, filePart)


def createLogme():
    if not LogmeInstance.Instance:
        LogmeInstance.Instance = LogmeLocal()

    return LogmeInstance.Instance


logme = createLogme()


def nowstr():
    """
    Returns a string with current date and time in the format
    YYYY-MM-DD HH:MM:SS, for example: 2003-01-22 10:12:43
    """
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def current_time():
    """
    Returns a sting with current time in the format HH:MM:SS,
    for example: 10:12:43
    """
    return time.strftime('%H:%M:%S', time.localtime(time.time()))
