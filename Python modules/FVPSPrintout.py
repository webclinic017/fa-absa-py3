""" VPS:1.0.0 """

"""------------------------------------------------------------------------
MODULE
    FVPSPrintout - Module for logging.

    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    Includes function for logging

------------------------------------------------------------------------"""

#Import builtin modules

import string
import time
import sys
import os.path

#Import Front modules

import ael

"""
------------------------------------------------------------------------------
DESCRIPTION
    The function logme in class Logme which logs information to file or
    console. Logme is actually an instance of class Logme() but works
    exactly as a method. In order to use the logme function you have to
    initialize it's parameters it using it's function setLogmeVar. This
    should be done as early as possible in each script. The variables used
    when calling setLogmeVar should be taken from each script's variable
    file. 
   
    setLogmeVar is initialized called with the variables:
    ScriptName      name of the current script
    LogMode -       how extensive the logging will be.
    LogToConsole -  if logging will be done to console or not
    LogToFile -     if logging will be done to the file <Logfile>
    Logfile -       full path to the file where logging will be done.
                    

ARGUMENTS
    msg         string      Text to be logged
    
    msg_type    string      Type of message
                'INFO'  -   Information (default)
                'WARNING' - Anything making a task being
                            fulfilled in an unusual way. 
                'ERROR' -   Anything making a task not being
                            fulfilled.
                'START' -   Also date and time will be printed 
                'FINISH'-   Script finished successfully
                'ABORT' -   Script aborted due to error
                'DEBUG' -   For developer purposes
            
    Note!If msg_type is 'START', 'ERROR', 'WARNING', 'FINISH' or 
    'ABORT' msg should be set to None.

    Logfile     string      For debugging purposes, if you
                            want some printouts in a certain
                            file.

USAGE
    In case of a fatal error first an 'ERROR' should be sent
    followed by 'ABORT'. For example:
    
    logme('Instrument %s does not exist' % ins.insid, 'ERROR')
    logme(None, 'ABORT')
    raise RuntimeError
--------------------------------------------------------------------------"""

class Logme:
    ScriptName = 'common'
    LogMode = 1
    LogToConsole = 1
    LogToFile = 1
    Logfile = 'VPS.log'
    if LogMode >= 0:
        LogMsg = ['START', 'FINISH', 'ABORT', 'ERROR', 'WARNING']
    if LogMode >= 1:
        LogMsg = LogMsg + ['INFO']
    if LogMode >= 2:
        LogMsg = LogMsg + ['DEBUG']
        
    def setLogmeVar(self, ScriptName, LogMode, LogToConsole, LogToFile, Logfile = None):
        """Function for initializing logging variables."""        
        Logme.ScriptName = ScriptName                        
        
        if LogMode == None:
            Logme.LogMode = 1
        else:
            Logme.LogMode = LogMode
                      
        if LogMode >= 0:
            Logme.LogMsg = ['START', 'FINISH', 'ABORT', 'ERROR', 'WARNING']
        if LogMode >= 1:
            Logme.LogMsg = Logme.LogMsg + ['INFO']
        if LogMode >= 2:
            Logme.LogMsg = Logme.LogMsg + ['DEBUG']
        
        if LogToConsole == None:
            Logme.LogToConsole = 1
        else:
            Logme.LogToConsole = LogToConsole

        Logme.LogToFile = LogToFile

        if Logme.LogToFile:       #i.e LogToFile = 1
            self.setLogfile(Logfile)
    
                    
    def __call__(self, msg, msg_type='INFO', Logfile = None):
        """Log to file or console, see class description for more info."""

        if msg == None:
            msg = Logme.ScriptName   #In case of START, FINISH and ABORT
            
        if Logfile == None and Logme.LogToFile: #Most cases, may be defined for debug printouts
            Logfile = Logme.Logfile
            
        if msg_type in ['ERROR', 'WARNING']:
            msg = msg_type + ':\t' + msg
        elif msg_type in ['START', 'FINISH', 'ABORT']:
            line = 45*'-'
                        
            if msg_type == 'START':
                msg = '\n%s\n%s STARTED %s' % (line, msg, nowstr())    
            elif msg_type == 'FINISH':
                msg = '%s FINISHED %s \n%s' % (msg, nowstr(), line)
            elif msg_type == 'ABORT':
                msg = '%s ABORTED %s \n%s' % (msg, nowstr(), line)
                
        elif msg_type in ['INFO', 'DEBUG']:
            pass
        else:
            print 'UNKNOWN MESSAGE TYPE:', msg_type     #For development only
            print 'MESSAGE:', msg                   
            msg_type = 'INFO'
            
                            
        if msg_type in Logme.LogMsg:      

            if Logme.LogToFile:
                try:
                    lf = open(Logfile, 'a')                     
                except IOError:                    
                    print '\nERROR:\tFailed to open logfile %s\n' % Logfile
                    raise
                
                lf.write(msg + '\n')
                lf.close()
                
            if Logme.LogToConsole:                
                print msg
         
                
    def setLogfile(self, Logfile):
        """Helper function for setting full path to the Logfile"""

        if Logfile == None:             #If this is not done it will crash when doing split
            Logfile = 'VPS.log'
            
        pathPart, filePart = os.path.split(Logfile)

        if os.path.isdir(pathPart):                #The path is not OK or not provided
            pass
        elif os.path.isdir('.'): #The path is not OK, use default from 
            pathPart = FBDPParameters.Logdir       #FBDPParameters            
        else:
            print '\nERROR:\tNo valid path found in your logging settings, \
            please check your default settings in FVPSVariables.\n'
            raise RuntimeError
        
        if filePart:
            Logme.Logfile = os.path.join(pathPart, filePart)
        else:                   #Use the scriptname for creating the name
            filePart = 'BDP_' + Logme.ScriptName + '.log'
            Logme.Logfile = os.path.join(pathPart, filePart)

logme = Logme()

def nowstr():
    """Returns a sting with current date and time in the format
YYYY-MM-DD HH:MM:SS, for example: 2003-01-22 10:12:43
"""
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
