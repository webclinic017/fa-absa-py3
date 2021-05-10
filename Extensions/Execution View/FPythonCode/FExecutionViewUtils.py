""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/ExecutionView/etc/FExecutionViewUtils.py"
"""-------------------------------------------------------------------------------------------------
MODULE
    FExecutionViewUtils

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------"""

import FLogger

def GetLogger(name='Execution View'):
    log = FLogger.FLogger.GetLogger(name)
    return log

logger = GetLogger()