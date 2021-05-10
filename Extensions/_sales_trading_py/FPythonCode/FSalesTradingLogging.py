""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FSalesTradingLogging.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FSalesTradingLogging

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import FLogger

def GetLogger(name='Sales Trading'):
    log = FLogger.FLogger.GetLogger(name)
    return log

logger = GetLogger()