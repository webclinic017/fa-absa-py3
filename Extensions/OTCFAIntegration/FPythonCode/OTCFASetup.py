"""----------------------------------------------------------------------------
MODULE
    OTCFASetup - sets up additional information
    specifications, default task parameters,
    default control tasks, and default
    schedules for the OTC-FA integration module.
    
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
reload(OTCFAConfiguration)
import acm
import datetime
import os
import string
import sys
import time
import traceback
import types
import DTCOMMON

#==================================================================
# GLOBALS
#==================================================================

defaultParameters = OTCFAConfiguration.configuration.getParametersForModule(__name__)
ael_variables = OTCFAConfiguration.configuration.getAelVariablesForModule(__name__)

global logme
import FBDPGui
reload(FBDPGui)
import FBDPString
reload(FBDPString)
logme = FBDPString.logme
import OTCFAMarketServer
reload(OTCFAMarketServer)
import OTCFAMarketServerController
reload(OTCFAMarketServerController)
import OTCFATradeServer
reload(OTCFATradeServer)
import OTCFATradeServerController
reload(OTCFATradeServerController)

def createAdditionalInfoSpec(add_info_name, table, data_type):
    if acm.FAdditionalInfoSpec[add_info_name] == None:
        ais = acm.FAdditionalInfoSpec()
        ais.RecType       = table
        ais.DataTypeGroup = "Standard"
        ais.DataTypeType  = data_type
        ais.FieldName     = add_info_name
        ais.Commit()
        logme('Created additional info spec: %s (%s) for %s.' % (add_info_name, data_type, table), 'DEBUG')
        
def createTimeSeriesSpec(time_series_spec_name, table):
    if acm.FTimeSeriesSpec[time_series_spec_name] == None:
        timeSeriesSpec = acm.FTimeSeriesSpec()
        timeSeriesSpec.RecType = table
        timeSeriesSpec.FieldName = time_series_spec_name
        timeSeriesSpec.Commit()        
        logme('Created time series spec: %s for %s.' % (time_series_spec_name, table), 'DEBUG')
        
def setParameters(aelTask, defaults, overrides):
    new = {}
    for key in defaults:
        if key in overrides:
            value = overrides[key]
        else:
            value = defaults[key]
        new[key] = value
    aelTask.Parameters(new)

def printParameters(task):
    name = task.Name()
    parameters = task.Parameters()
    logme('    Parameters for %s:' % (name), 'DEBUG')
    for key in parameters.Keys().Sort():
        value = parameters[key]
        logme('        %s = %s %s' % (key, value, type(value)), 'DEBUG')
        
def createSchedule(task, hour, minute):
    schedules = task.Schedules()
    for schedule in schedules:
        schedule.Delete()
    schedule = acm.FAelTaskSchedule()
    schedule.Task(task)
    schedule.StartDate(acm.Time().DateNow())
    schedule.DailyRunTime(acm.Time().TimeOfDay(hour, minute, 0))
    schedule.Enabled(False)
    schedule.Commit()
    logme('    Scheduled: %s - %s' % (task.Name(), schedule.Schedule()), 'DEBUG')
    

#=======================================================================
# Main
#=======================================================================

def ael_main(parameters):
    try:
        logme('STARTED OTCFASetup...', 'START')
        ScriptName = 'OTCFASetup'
        LogMode = int(parameters['logmode'])
        LogToConsole = int(parameters['log_to_console'])
        LogToFile = int(parameters['log_to_file'])
        Logfile = parameters.get('setup_logfile')
        SendReportByMail = False
        MailList = []
        ReportMessageType = None
        logme.setLogmeVar(ScriptName, LogMode, LogToConsole, LogToFile, Logfile, SendReportByMail, MailList, ReportMessageType)
        parameters['today_date'] = acm.Time().DateNow()
        if LogMode > 1:
            keys = parameters.keys()
            keys.sort()
            for key in keys:
                value = parameters[key]
                logme('Parameter:   %s = %s %s' % (key, value, type(value)), 'DEBUG')
        logme('Adding additional information specifications...', 'INFO')
        createAdditionalInfoSpec('Option_Strategy', 'Trade', 3)
        createAdditionalInfoSpec('Option_Reference', 'Trade', 3)
        createTimeSeriesSpec('OTCFA Avg Price Wt', 'Instrument')
        createTimeSeriesSpec('OTCFA Avg Strike Wt', 'Instrument')
        logme('Adding tasks...', 'INFO')
        
        otcfaMarketServerTask = acm.FAelTask['OTCFAMarketServerTask']
        if not otcfaMarketServerTask:
            otcfaMarketServerTask = acm.FAelTask()
            otcfaMarketServerTask.Name('OTCFAMarketServerTask')
            otcfaMarketServerTask.ModuleName('OTCFAMarketServer')
        defaults = OTCFAConfiguration.configuration.getParametersForModule('OTCFAMarketServer')
        currencyPairs = parameters['currency_pairs']
        value = ''
        for i in range(len(currencyPairs)):
            if i > 0:
                value = value + ','
            value = value + currencyPairs[i]
        parameters['currency_pairs'] = value
        setParameters(otcfaMarketServerTask, defaults, parameters)
        otcfaMarketServerTask.Commit()
        printParameters(otcfaMarketServerTask)
        
        otcfaTradeServerTask = acm.FAelTask['OTCFATradeServerTask']
        if not otcfaTradeServerTask:
            otcfaTradeServerTask = acm.FAelTask()
            otcfaTradeServerTask.Name('OTCFATradeServerTask')
            otcfaTradeServerTask.ModuleName('OTCFATradeServer')
        defaults = OTCFAConfiguration.configuration.getParametersForModule('OTCFATradeServer')
        setParameters(otcfaTradeServerTask, defaults, parameters)
        otcfaTradeServerTask.Commit()
        printParameters(otcfaTradeServerTask)
        
        otcfaMarketServerStart = acm.FAelTask['OTCFAMarketServerStart']
        if not otcfaMarketServerStart:
            otcfaMarketServerStart = acm.FAelTask()
            otcfaMarketServerStart.Name('OTCFAMarketServerStart')
            otcfaMarketServerStart.ModuleName('OTCFAMarketServerController')
        defaults = OTCFAMarketServerController.defaultParameters
        parameters['action'] = 'Start'
        parameters['ats_task'] = 'OTCFAMarketServerTask'
        setParameters(otcfaMarketServerStart, defaults, parameters)
        otcfaMarketServerStart.Commit()
        printParameters(otcfaMarketServerStart)
        
        otcfaMarketServerStop = acm.FAelTask['OTCFAMarketServerStop']
        if not otcfaMarketServerStop:
            otcfaMarketServerStop = acm.FAelTask()
            otcfaMarketServerStop.Name('OTCFAMarketServerStop')
            otcfaMarketServerStop.ModuleName('OTCFAMarketServerController')
        defaults = OTCFAMarketServerController.defaultParameters
        parameters['action'] = 'Stop'
        setParameters(otcfaMarketServerStop, defaults, parameters)
        otcfaMarketServerStop.Commit()
        printParameters(otcfaMarketServerStop)
        
        otcfaTradeServerStart = acm.FAelTask['OTCFATradeServerStart']
        if not otcfaTradeServerStart:
            otcfaTradeServerStart = acm.FAelTask()
            otcfaTradeServerStart.Name('OTCFATradeServerStart')
            otcfaTradeServerStart.ModuleName('OTCFATradeServerController')
        defaults = OTCFATradeServerController.defaultParameters
        parameters['action'] = 'Start'
        parameters['ats_task'] = 'OTCFATradeServerTask'
        setParameters(otcfaTradeServerStart, defaults, parameters)
        otcfaTradeServerStart.Commit()
        printParameters(otcfaTradeServerStart)
        
        otcfaTradeServerStop = acm.FAelTask['OTCFATradeServerStop']
        if not otcfaTradeServerStop:
            otcfaTradeServerStop = acm.FAelTask()
            otcfaTradeServerStop.Name('OTCFATradeServerStop')
            otcfaTradeServerStop.ModuleName('OTCFATradeServerController')
        defaults = OTCFATradeServerController.defaultParameters
        parameters['action'] = 'Stop'
        setParameters(otcfaTradeServerStop, defaults, parameters)
        otcfaTradeServerStop.Commit()
        printParameters(otcfaTradeServerStop)
       
        logme('Adding schedules for tasks...', 'INFO')
        createSchedule(otcfaMarketServerStart, 1, 1)
        createSchedule(otcfaMarketServerStop, 23, 50)
        createSchedule(otcfaTradeServerStart, 1, 1)
        createSchedule(otcfaTradeServerStop, 23, 50)
            
        logme('ENDED OTCFASetup.', 'FINISH')
    except:
        traceback.print_exc()
