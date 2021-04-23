
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_PARAMETERS_FLOGGER
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module retreives and sets the flogger variables from the environment
                                variables in Extension Manager.
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------
'''

'''----------------------------------------------------------------------------------------------------------
Importing Custom modules modules needed for Real Time ATS Worker.
----------------------------------------------------------------------------------------------------------'''
from FC_PARAMETERS_ENVIRONMENT import FC_PARAMETERS_ENVIRONMENT as ENVIRONMENT_PARAMETERS
from FC_EXCEPTION import FC_EXCEPTION as EXCEPTION
import at_type_helpers as TYPE_UTILS
import traceback

'''----------------------------------------------------------------------------------------------------------
Class containing all the properties for the Specific ATS that is starting up for thr FLogger component.
----------------------------------------------------------------------------------------------------------'''
class FC_PARAMETERS_FLOGGER(object):
    def __init__(self, componentName):
        self._componentName = componentName
        self._floggerName = None
        self._floggerLevel = None
        self._floggerKeep = None
        self._floggerLogOnce = None
        self._floggerLogToConsole = None
        self._floggerLogToPrime = None
        self._floggerLogToFileAtSpecificPath = None
        self._floggerLogToFileAtDefaultPath = None
        self._floggerFilters = []
        self._floggerMaxBytes = None
        self._floggerBackupCount = None
        self._setFloggerParameters()
    
    @property
    def FloggerName(self):
        return self._floggerName
        
    @property
    def FloggerLevel(self):
        return self._floggerLevel
    
    @property
    def FloggerKeep(self):
        return self._floggerKeep
    
    @property
    def FloggerLogOnce(self):
        return self._floggerLogOnce
    
    @property
    def FloggerLogToConsole(self):
        return self._floggerLogToConsole
    
    @property
    def FloggerLogToPrime(self):
        return self._floggerLogToPrime
    
    @property
    def FloggerLogToFileAtSpecificPath(self):
        return self._floggerLogToFileAtSpecificPath
    
    @property
    def FLoggerLogToFileAtDefaultPath(self):
        return self._floggerLogToFileAtDefaultPath
        
    @property
    def FloggerFilters(self):
        return self._floggerFilters

    @property
    def FloggerMaxBytes(self):
        return self._floggerMaxBytes

    @property
    def FloggerBackupCount(self):
        return self._floggerBackupCount
        
    def _setFloggerParameters(self):
        componentSettingsXML = ENVIRONMENT_PARAMETERS.environment.getElementsByTagName(self._componentName)
        if not componentSettingsXML:
            raise ValueError('The component settings for component %s could not be retreived from the environment settings in module %s' %(self._componentName, __name__))
            
        floggerSettingsXML = componentSettingsXML[0].getElementsByTagName('FloggerSettings')
        if not floggerSettingsXML:
            raise ValueError('The Flogger XML Settings for component %s could not be retreived in module %s.' %(self._componentName, __name__))
        
        try:
            self._floggerName = str(floggerSettingsXML[0].getElementsByTagName('FloggerName')[0].firstChild.data)
        except Exception as e:
            raise EXCEPTION('The Flogger Name for component %s could not be retreived in module %s.' %(self._componentName, __name__),\
                                traceback, 'CRITICAL', e)
        
        try:
            self._floggerLevel = int(str(floggerSettingsXML[0].getElementsByTagName('FloggerLevel')[0].firstChild.data))
        except Exception as e:
            raise EXCEPTION('The Flogger Level for component %s could not be retreived in module %s.' %(self._componentName, __name__),\
                                traceback, 'CRITICAL', e)
        
        try:
            self._floggerKeep = TYPE_UTILS.to_bool(str(floggerSettingsXML[0].getElementsByTagName('FloggerKeep')[0].firstChild.data))
        except Exception as e:
            raise EXCEPTION('The Flogger Keep for the component %s could not be retreived in module %s.' %(self._componentName, __name__),\
                                traceback, 'CRITICAL', e)
        
        try:
            self._floggerLogOnce = TYPE_UTILS.to_bool(str(floggerSettingsXML[0].getElementsByTagName('FloggerLogOnce')[0].firstChild.data))
        except Exception as e:
            raise EXCEPTION('The Flogger Log Once for the component %s could not be retreived in module %s.' %(self._componentName, __name__),\
                                traceback, 'CRITICAL', e)
        
        try:
            self._floggerLogToConsole = TYPE_UTILS.to_bool(str(floggerSettingsXML[0].getElementsByTagName('FloggerLogToConsole')[0].firstChild.data))
        except EXCEPTION as e:
            raise EXCEPTION('The Flogger Log To Console for the component %s could not be retreived in module %s.' %(self._componentName, __name__),\
                                traceback, 'CRITICAL', e)
        
        try:
            self._floggerLogToPrime = TYPE_UTILS.to_bool(str(floggerSettingsXML[0].getElementsByTagName('FloggerLogToPrime')[0].firstChild.data))
        except Exception as e:
            raise EXCEPTION('The Flogger Log To Prime for component %s could not be retreived in module %s.' %(self._componentName, __name__),\
                                traceback, 'CRITICAL', e)
        
        try:
            self._floggerLogToFileAtSpecificPath = None
        except Exception as e:
            raise EXCEPTION('The Flogger Log To File At Specific Path for component %s could not be retreived in module %s.' %(self._componentName, __name__),\
                                traceback, 'CRITICAL', e)
        
        try:
            self._floggerLogToFileAtDefaultPath = str(floggerSettingsXML[0].getElementsByTagName('FloggerLogToFileAtDefaultPath')[0].firstChild.data) + \
                    self._floggerName + '.log'
        except Exception as e:
            raise EXCEPTION('The Flogger Log To File At Default Path for component %s could not be retreived in module %s.' %(self._componentName, __name__),\
                                traceback, 'CRITICAL', e)
            
        try:
            self._floggerFilters = str(floggerSettingsXML[0].getElementsByTagName('FloggerFilters')[0].firstChild.data).split(',')
        except:
            self._floggerFilters = []

        try:
            self._floggerMaxBytes = int(str(floggerSettingsXML[0].getElementsByTagName('FloggerMaxBytes')[0].firstChild.data))
        except Exception as e:
            raise EXCEPTION('The Flogger MaxBytes for component %s could not be retreived in module %s.' %(self._componentName, __name__),\
                                traceback, 'CRITICAL', e)

        try:
            self._floggerBackupCount = int(str(floggerSettingsXML[0].getElementsByTagName('FloggerBackupCount')[0].firstChild.data))
        except Exception as e:
            raise EXCEPTION('The Flogger BackupCount for component %s could not be retreived in module %s.' %(self._componentName, __name__),\
                                traceback, 'CRITICAL', e)
