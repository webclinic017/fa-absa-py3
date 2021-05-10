""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/pace_runner/etc/FPaceAelTaskLogger.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
import acm

def getPACEAelTasksLogPath():
    param = acm.GetDefaultContext().GetExtension(
        'FParameters', 'FParameter', "FPACETaskRunnerParameters")
    log = param.Value()['Logfile']
    return log.Text()

def getLogger():
    import FLogger
    import logging
    logger = FLogger.FLogger.GetLogger('PACEAelTasksLogger')
    logger.Reinitialize(logToFileAtSpecifiedPath=getPACEAelTasksLogPath())
    log_formatter = logging.Formatter( '%(asctime)s %(message)s', '%y%m%d %H%M%S' )
    for hndlr in logger.Handlers():
        hndlr.setFormatter(log_formatter)
    return logger
