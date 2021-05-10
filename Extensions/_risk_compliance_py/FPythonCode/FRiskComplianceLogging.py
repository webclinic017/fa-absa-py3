""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/RiskCompliance/etc/FRiskComplianceLogging.py"
"""--------------------------------------------------------------------------
MODULE
    FRiskComplianceLogging

    (c) Copyright 2016 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION


-----------------------------------------------------------------------------"""

import FLogger

def GetLogger(name='Risk And Compliance view'):
    log = FLogger.FLogger.GetLogger(name)
    return log

logger = GetLogger()
