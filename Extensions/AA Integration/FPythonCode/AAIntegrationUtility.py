""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/aa_integration/./etc/AAIntegrationUtility.py"
"""----------------------------------------------------------------------------
MODULE
    AAIntegrationUtility - Misc. helper functions

    (c) Copyright 2016 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

----------------------------------------------------------------------------"""
import datetime
import logging
import os
import re

import FFileUtils
import FLogger
import FScenarioExportUtils

DEFAULT_INDENTATION = '  '

def forwardSlashedPath(path, real=False, check=False):
    path = str(path).strip()
    path = FFileUtils.expandEnvironmentVar(path)
    if real:
        path = os.path.realpath(path).strip()

    path = re.sub('[\\\?]', '/', path).strip()
    if check:
        assert path, 'No %s specified' % key
        assert os.path.exists(path), 'Path does not exist: ' + path

    return path

def getAAFormattedDate(date):
    """
    Common field, present in almost all AA calculations.
    Is required to be in the particular format of %d%b%Y (e.g. 02Oct2011)
    """
    return datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%d%b%Y')


def getInputDirectory(dir_path, ref_date, ext):
    dir_path = forwardSlashedPath(path=dir_path, real=True)
    if not dir_path:
        raise ValueError('Input \'Directory Path\' not specified')

    dir_path = FScenarioExportUtils.get_directory(dir_path, ref_date, bool(ref_date))
    paths = []
    if not os.path.isdir(dir_path):
        raise ValueError('{0} is not a valid directory path'.format(dir_path))

    dir_path = forwardSlashedPath(path=dir_path)
    for fname in os.listdir(dir_path):
        fpath = os.path.join(dir_path, fname)
        if os.path.isfile(fpath):
            if (not ext) or fname.endswith(ext):
                paths.append(forwardSlashedPath(path=fpath))

        return dir_path, tuple(sorted(paths))

    msg = 'No files found. Path=%s, Extension=%s' % (dir_path, ext)
    raise Exception(msg)

def getLogger(name, ael_params):
    kwargs = __getLoggerKwArgsFromAelParams(ael_params)
    log_path = kwargs['logToFileAtSpecifiedPath']
    if log_path:
        log_dir = os.path.dirname(log_path)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

    logger = FLogger.FLogger.LOGGERS.get(name)
    if not logger:
        logger = FLogger.FLogger(name=name)

    logger.Reinitialize(**kwargs)
    log_formatter = logging.Formatter(
        fmt='%(asctime)s %(name)s[%(levelname)8s]: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    for handler in logger.Handlers():
        handler.setFormatter(log_formatter)

    return logger

def __getLoggerKwArgsFromAelParams(ael_params):
    # workaround for bug in FLogger which duplicates logging
    log_path = None
    if bool(int(ael_params['LogToFile'])):
        log_path = forwardSlashedPath(path=ael_params['Logfile'], real=True)

    logger_kwargs = {
        'level': int(ael_params['Logmode']),
        'logToConsole': bool(int(ael_params['LogToConsole'])),
        'logToPrime': False,
        'keep': False,
        'logOnce': False,
        'logToFileAtSpecifiedPath': log_path
    }
    return logger_kwargs
