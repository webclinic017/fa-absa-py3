""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/IntegratedWorkbench/./etc/FIntegratedWorkbenchLogging.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FIntegratedWorkbenchLogging

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import FLogger

def GetLogger(name=''):
    name = 'Integrated Workbench ' + name
    aLogger = FLogger.FLogger.GetLogger(name)
    return aLogger

def SetLoggingLevel(aLogger, level):
    ''' Levels are 1-4 signifying
        1: Info: get warnings, errors and info
        2: Debug: get everything
        3: Warn: get warnings and errors
        4: Error: get only errors
    '''
    aLogger.Reinitialize(level=level)


logger         = GetLogger(':')
creationLogger = GetLogger('View Creation:')
