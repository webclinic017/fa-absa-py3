"""----------------------------------------------------------------------------
MODULE
    ATSServerController - Start or stop ATS task servers.
    The task running in the server must have an XMLRPC server
    listening for 'start', 'stop', and 'report' calls.
    
    Requirements: 
    
		1. Fnorb all-Python CORBA ORB.
		2. IONA Orbix.
		3. Derivatech MDS and database.
		4. DOM parser.
    5. The ctypes Python extension module.
    
    Copyright (c) 2006 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

ENDDESCRIPTION
"""

import OTCFAConfiguration
import os
import string
import socket
import sys
import time
import traceback
import xmlrpclib
import acm
import importlib

defaultParameters = OTCFAConfiguration.configuration.getParametersForModule(__name__)

import FBDPGui
importlib.reload(FBDPGui)
import FBDPString
importlib.reload(FBDPString)

global logme
logme = FBDPString.logme

#==================================================================
# GLOBALS
#==================================================================

try:
    import FBDPParameters
    importlib.reload(FBDPParameters)
 
    TestMode = 0
    Date = FBDPParameters.Date
    LogMode = FBDPParameters.LogMode
    LogToConsole = FBDPParameters.LogToConsole
    LogToFile = FBDPParameters.LogToFile
    SendReportByMail = FBDPParameters.SendReportByMail
    MailList = FBDPParameters.MailList
    ReportMessageType = FBDPParameters.ReportMessageType
except:
    TestMode = 1
    Date = "Today"
    LogMode = 1
    LogToConsole = 1
    LogToFile = 0
    SendReportByMail = 0
    MailList = ""
    ReportMessageType = ""

#=======================================================================
# Main
#=======================================================================

ael_variables = OTCFAConfiguration.configuration.getAelVariablesForModule(__name__)

def actionStart(parameters):
    try:
        ats_parameters = []
        ats_parameters.append(parameters['ats_path'])
        ats_parameters.append('-nonincremental')
        ats_parameters.append('-server')
        ats_parameters.append(parameters['ads_url'])
        ats_parameters.append('-username')
        ats_parameters.append(parameters['ads_username'])
        ats_parameters.append('-password')
        ats_parameters.append(parameters['ads_password'])
        ats_parameters.append('-task')
        ats_parameters.append(parameters['ats_task'])
        logme("ATS parameters: %s" % string.join(ats_parameters), 'INFO')
        pid = os.spawnv(os.P_NOWAIT, parameters['ats_path'], ats_parameters)
        logme('Started ATS with pid: %d' % (pid), 'INFO')
    except:
        traceback.print_exc()

def actionReport(parameters):
    controllerUrl = 'http://localhost:' + str(parameters['controller_port'])
    controller = xmlrpclib.ServerProxy(controllerUrl)
    try:
        controller.report()
    except:
        traceback.print_exc()
    
def actionStop(parameters):
    controllerUrl = 'http://localhost:' + str(parameters['ts_controller_port'])
    controller = xmlrpclib.ServerProxy(controllerUrl)
    try:
        controller.shutdown()
    except socket.error as e:
        if e[0] != 10054:
            traceback.print_exc()
            return
    except:
        traceback.print_exc()
        return
    logme('Stopped.', 'INFO')

def ael_main(parameters):
    try:
        ScriptName = 'FAOTCTradeServerController'
        LogMode = int(parameters['logmode'])
        LogToConsole = int(parameters['log_to_console'])
        LogToFile = int(parameters['log_to_file'])
        Logfile = parameters.get('logfile')
        logme.setLogmeVar(ScriptName, LogMode, LogToConsole, LogToFile, Logfile, SendReportByMail, MailList, ReportMessageType)

        parameters['today_date'] = acm.Time().DateNow(),
        if LogMode > 1:
            for key, value in parameters.items():
                logme('Parameter: %s = %s (%s)' % (key, value, type(value)), 'DEBUG')        
        action = parameters['action']
        if   action == 'Start':
            actionStart(parameters)
        elif action == 'Report':
            actionReport(parameters)
        elif action == 'Stop':
            actionStop(parameters)
    except:
        traceback.print_exc()
  
if __name__ == '__main__':
    ael_main(defaultParameters)
