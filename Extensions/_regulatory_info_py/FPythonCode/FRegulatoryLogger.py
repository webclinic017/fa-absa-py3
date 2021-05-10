""" Compiled: 2020-09-18 10:38:56 """

#__src_file__ = "extensions/RegulatoryInfo/../SwiftIntegration/RegulatoryInfo/General/FRegulatoryLogger.py"
"""------------------------------------------------------------------------
MODULE
    FRegulatoryLogger -
DESCRIPTION:
    This file is used for logging all messages within the component
VERSION: %R%
RESTRICTIONS/ LIMITATIONS:
    1. Any modifications to the scripts/ encrypted modules/ clear text code within the core is not supported. 
    2. This module is not customizable
    3. The component may not work as expected with any modifications done to this module at user end 
--------------------------------------------------------------------------"""
from FLogger import FLogger
import FRegulatoryConfigParam


logger = None
bNotification = False
try:
    notifier = None
    import FANotification
    bNotification = True
except:
    pass

def getLogger(verbosityLevel, loggerName):
    global logger    
    if not logger:        
        logger = FLogger.HasLogger(name=loggerName)
    if not logger:
        logger = FLogger(name=loggerName, level= verbosityLevel, keep= False, logOnce=False,
                  logToConsole=True, logToPrime=False,
                  logToFileAtSpecifiedPath=False, filters=None)        
    if logger.Level() !=  verbosityLevel:            
            logger = logger.Reinitialize(level= verbosityLevel, keep= False, logOnce=False,
                  logToConsole=True, logToPrime=False,
                  logToFileAtSpecifiedPath=False, filters=None)            
    return logger

def createLogMessage(sourceFile, message, param):    
    if param != "":        
        if param.find(':') != -1:
            param_tuple = param.split(':')
            i = 0
            while i < len(param_tuple):
                str_replace = '<%s>'
                if i > 0:
                    str_replace = '<%s' + str(i) + '>'
                message = message.replace(str_replace, param_tuple[i])
                i = i + 1
        else:
            message = message.replace('%s', param)
    message = sourceFile + ": " + message
    return message

def LogMessage(funcCall, msg):
    config_parameters = FRegulatoryConfigParam.FRegulatoryConfigParam()
    global logger
    if not config_parameters.get_paramvalue('FREGULATORY_VERBOSITY_LEVEL'):
        config_parameters.set_paramvalue('FREGULATORY_VERBOSITY_LEVEL', 2)
    global notifier
    bTrace = 0
    if bNotification and config_parameters.get_paramvalue('FREGULATORY_NOTIFICATION_MEDIA') != 'OFF':
        log_level = config_parameters.get_paramvalue('FREGULATORY_MESSAGE_VERBOSE')
        if log_level == 'WARNING':
            log_level = 'WARN'
        notifier = FANotification.FANotification(name = config_parameters.get_paramvalue('FREGULATORY_LOGGER_NAME'), \
                                                 notification_media = config_parameters.get_paramvalue('FREGULATORY_NOTIFICATION_MEDIA'), \
                                                 notify_level = config_parameters.get_paramvalue('FREGULATORY_NOTIFY_LEVEL'), \
                                                 logging_level = log_level, \
                                                 message_broker = config_parameters.get_paramvalue('FREGULATORY_NOTIFICATION_MESSAGE_BROKER'), \
                                                 user = config_parameters.get_paramvalue('FREGULATORY_NOTIFY_USERS'), \
                                                 user_emails = config_parameters.get_paramvalue('FREGULATORY_USER_EMAILS'), \
                                                 smtp_server = config_parameters.get_paramvalue('FREGULATORY_SMTP_SERVER'))
        if funcCall == 'ERROR':
            if 'DEBUG' == config_parameters.get_paramvalue('FREGULATORY_MESSAGE_VERBOSE').strip():
                bTrace = 1
            notifier.ERROR(msg, exc_info = bTrace)
        elif funcCall == 'DEBUG':
            notifier.DEBUG(msg)
        elif funcCall == 'WARN':
            notifier.WARN(msg)
        elif funcCall == 'INFO':
            notifier.INFO(msg)
    else:
        notifier = getLogger(config_parameters.get_paramvalue('FREGULATORY_VERBOSITY_LEVEL'), \
                       config_parameters.get_paramvalue('FREGULATORY_LOGGER_NAME'))
        if 'DEBUG' == config_parameters.get_paramvalue('FREGULATORY_MESSAGE_VERBOSE').strip():
            bTrace = 1
        if funcCall == 'ERROR':
            notifier.ELOG(msg, exc_info = bTrace)
        elif funcCall == 'DEBUG':
            notifier.DLOG(msg)
        elif funcCall == 'WARN':
            notifier.WLOG(msg)
        elif funcCall == 'INFO':
            notifier.LOG(msg)

def DEBUG(sourceFile, msg, param = ''):
    msg = createLogMessage(sourceFile, msg, param)        
    LogMessage('DEBUG', msg)

def INFO(sourceFile, msg, param = ''):
    msg = createLogMessage(sourceFile, msg, param)    
    LogMessage('INFO', msg)

def ERROR(sourceFile, msg, param = ''):
    msg = createLogMessage(sourceFile, msg, param)    
    LogMessage('ERROR', msg)

def WARN(sourceFile, msg, param = ''):
    msg = createLogMessage(sourceFile, msg, param)    
    LogMessage('WARN', msg)
