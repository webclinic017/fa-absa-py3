
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_PARAMETERS_GENERIC
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module retreives and sets the generic variables from the environment
                                variables in Extension Manager.
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------
'''

'''----------------------------------------------------------------------------------------------------------
Import python modules
----------------------------------------------------------------------------------------------------------'''
import ael, traceback

'''----------------------------------------------------------------------------------------------------------
Importing Custom modules modules needed for Real Time ATS Worker.
----------------------------------------------------------------------------------------------------------'''
from FC_PARAMETERS_ENVIRONMENT import FC_PARAMETERS_ENVIRONMENT as ENVIRONMENT_PARAMETERS
from FC_EXCEPTION import FC_EXCEPTION as EXCEPTION
import at_type_helpers as TYPE_UTILS
'''----------------------------------------------------------------------------------------------------------
Class containing all the generic properties for the ATS.
----------------------------------------------------------------------------------------------------------'''
class FC_PARAMETERS_GENERIC(object):
    def __init__(self):
        self._frontArenaInstanceName = None
        self._heartbeatTrackInterval = None
        self._memoryThreshold = None
        self._restartIfMemoryThresholdExceeded = None
        self._dataBaseRetryThreshold = None
        self._unixConnectionString = None
        self._dataSource = None
        self._initialCatalog = None
        self._ambPrincipal = None
        self._ambUser = None
        self._ambSingleSignOn = None  
        self._invalidTradeStatusesList = []
        self._invalidTradeStatuses = None
        self._invalidEODTradeStatusesList = []
        self._invalidEODTradeStatuses = None
        self._dateFormatLabelOverrides = []
        self._dateTimeFormatLabelOverrides = []
        self._numberFormatLabelOverrides = []
        self._tradeCreateCutOffTime = None
        self._tradeEODCreateCutOffTime = None
        self._controlMeasureColumnsList = []
        self._shutdownTimes = []
        self._restartAfterWork = False
        self._setGenericParameters()

    @property
    def ShutdownTimes(self):
        return self._shutdownTimes

    @property
    def ControlMeasureColumnsList(self):
        return self._controlMeasureColumnsList
            
    @property
    def HeartbeatTrackInterval(self):
        return self._heartbeatTrackInterval
    
    @property
    def FrontArenaInstanceName(self):
        return self._frontArenaInstanceName

    @property
    def memoryThreshold(self):
        return self._memoryThreshold

    @property
    def restartIfMemoryThresholdExceeded(self):
        return self._restartIfMemoryThresholdExceeded
        
    @property
    def DataBaseRetryThreshold(self):
        return self._dataBaseRetryThreshold

    @property
    def DataSource(self):
        return self._dataSource

    @property
    def InitialCatalog(self):
        return self._initialCatalog

    @property
    def AmbPrincipal(self):
        return self._ambPrincipal
        
    @property
    def AmbUser(self):
        return self._ambUser

    @property
    def AmbSingleSignOn(self):
        return self._ambSingleSignOn            
    
    @property
    def UnixConnectionString(self):
        return self._unixConnectionString
    
    @property
    def invalidTradeStatuses(self):
        return self._invalidTradeStatuses
    
    @property
    def invalidEODTradeStatuses(self):
        return self._invalidEODTradeStatuses
    
    @property
    def DateFormatLabelOverrides(self):
        return self._dateFormatLabelOverrides
    
    @property
    def DateTimeFormatLabelOverrides(self):
        return self._dateTimeFormatLabelOverrides
    
    @property
    def NumberFormatLabelOverrides(self):
        return self._numberFormatLabelOverrides
    
    @property
    def TradeCreateCutOffTime(self):
        return self._tradeCreateCutOffTime
    
    @property
    def TradeEODCreateCutOffTime(self):
        return self._tradeEODCreateCutOffTime

    @property
    def RestartAfterWork(self):
        return self._restartAfterWork

    @RestartAfterWork.setter
    def RestartAfterWork(self, value):
        self._restartAfterWork = value
    
    def _setGenericParameters(self):
        genericSettingsXML = ENVIRONMENT_PARAMETERS.environment.getElementsByTagName('GENERIC_PARAMETERS')
        if not genericSettingsXML:
            raise ValueError('The generic settings could not be retreived from the environment settings in module %s.' %__name__)
        
        try:
            self._heartbeatTrackInterval = float(str(genericSettingsXML[0].getElementsByTagName('HeartbeatTrackInterval')[0].firstChild.data))
        except Exception, e:
            raise EXCEPTION('The generic variable HeartbeatTrackInterval could not be retreived in module %s.' %__name__,\
                            traceback, 'CRITICAL', e)

        try:
            self._frontArenaInstanceName = str(genericSettingsXML[0].getElementsByTagName('FrontArenaInstanceName')[0].firstChild.data)
        except Exception, e:
            raise EXCEPTION('The generic variable FrontArenaInstanceName could not be retreived in module %s.' %__name__,\
                            traceback, 'CRITICAL', e)
        
        try:
            self._memoryThreshold = str(genericSettingsXML[0].getElementsByTagName('MemoryThreshold')[0].firstChild.data)
        except Exception, e:
            raise EXCEPTION('The generic variabale Memory Threshold could not be retreived in module %s.' %__name__,\
                            traceback, 'CRITICAL', e)
        
        try:
            self._restartIfMemoryThresholdExceeded = str(genericSettingsXML[0].getElementsByTagName('RestartIfMemoryThresholdExceeded')[0].firstChild.data)
        except Exception, e:
            raise EXCEPTION('The generic variable Restart If Memory Threshold Exceeded could not be retreived in module %s.' %__name__,\
                            traceback, 'CRITICAL', e)

        try:
            self._unixConnectionString = str(genericSettingsXML[0].getElementsByTagName('UnixConnectionString')[0].firstChild.data)
        except Exception, e:
            raise EXCEPTION('The generic variable UNIX Connection String could not be retreived in module %s.' %__name__,\
                            traceback, 'CRITICAL', e)

        try:
            self._dataSource = str(genericSettingsXML[0].getElementsByTagName('DataSource')[0].firstChild.data)
        except Exception, e:
            raise EXCEPTION('The generic variable DataSource could not be retreived in module %s.' %__name__,\
                            traceback, 'CRITICAL', e)


        try:
            self._initialCatalog = str(genericSettingsXML[0].getElementsByTagName('InitialCatalog')[0].firstChild.data)
        except Exception, e:
            raise EXCEPTION('The generic variable InitialCatalog could not be retreived in module %s.' %__name__,\
                            traceback, 'CRITICAL', e)


        try:
            self._ambPrincipal = str(genericSettingsXML[0].getElementsByTagName('AmbPrincipal')[0].firstChild.data)
        except Exception, e:
            raise EXCEPTION('The generic variable AmbPrincipal could not be retreived in module %s.' %__name__, traceback, 'CRITICAL', e)


        try:
            self._ambSingleSignOn = str(genericSettingsXML[0].getElementsByTagName('AmbSingleSignOn')[0].firstChild.data)
        except Exception, e:
            raise EXCEPTION('The generic variable AmbSingleSignOn could not be retrieved in module %s.' %__name__, traceback, 'CRITICAL', e)


        try:
            self._ambUser = str(genericSettingsXML[0].getElementsByTagName('AmbUser')[0].firstChild.data)
        except Exception, e:
            raise EXCEPTION('The generic variable AmbUser could not be retrieved in module %s.' %__name__, traceback, 'CRITICAL', e)
                

        try:
            self._dataBaseRetryThreshold = int(str(genericSettingsXML[0].getElementsByTagName('DataBaseRetryThreshold')[0].firstChild.data))
        except Exception, e:
            raise EXCEPTION('The generic variable Data Base Retry Threshold could not be retreived in module %s.' %__name__,\
                            traceback, 'CRITICAL', e)
                            
        try:
            self._tradeCreateCutOffTime = str(genericSettingsXML[0].getElementsByTagName('TradeCreateCutOffTime')[0].firstChild.data)
        except Exception, e:
            raise EXCEPTION('The generic variable Trade Create Cut Off Time could not be retreived in module %s.' %__name__,\
                            traceback, 'CRITICAL', e)
        
        try:
            self._tradeEODCreateCutOffTime = str(genericSettingsXML[0].getElementsByTagName('TradeEODCreateCutOffTime')[0].firstChild.data)
        except Exception, e:
            raise EXCEPTION('The generic variable Trade EOD Create Cut Off Time could not be retreived in module %s.' %__name__,\
                            traceback, 'CRITICAL', e)

        try:
            self._restartAfterWork = TYPE_UTILS.to_bool(str(genericSettingsXML[0].getElementsByTagName('RestartAfterWork')[0].firstChild.data))
        except Exception, e:
            raise EXCEPTION('The generic variable RestartAfterWork could not be retreived in module %s.' %__name__,\
                            traceback, 'CRITICAL', e)
                            
        #Invalid Trade Statuses
        invalidTradeStatusesXML = genericSettingsXML[0].getElementsByTagName('InvalidTradeStatuses')
        if invalidTradeStatusesXML:
            invalidTradeStatuses = invalidTradeStatusesXML[0].getElementsByTagName('InvalidTradeStatus')
            if not invalidTradeStatuses:
                raise ValueError('No InvalidTradeStatuses settings could be retreived in module %s.' %__name__)
            
            for invalidTradeStatus in invalidTradeStatuses:
                try:
                    self._invalidTradeStatusesList.append(str(ael.enum_from_string('TradeStatus', str(invalidTradeStatus.firstChild.data))))
                except Exception, e:
                    raise EXCEPTION('One of the Invalid Trade Statuses could not be retreived in module %s.' %__name__,\
                    traceback, 'CRITICAL', e)
            self._invalidTradeStatuses = '(' + ",".join(self._invalidTradeStatusesList) + ')'
        else:
            raise ValueError('No InvalidTradeStatuses settings could be retreived in module %s.' %__name__)

        #Invalid EOD Trade Statuses
        invalidEODTradeStatusesXML = genericSettingsXML[0].getElementsByTagName('InvalidEODTradeStatuses')
        if invalidEODTradeStatusesXML:
            invalidEODTradeStatuses = invalidEODTradeStatusesXML[0].getElementsByTagName('InvalidTradeStatus')
            if not invalidEODTradeStatuses:
                raise ValueError('No InvalidEODTradeStatuses settings could be retreived in module %s.' %__name__)
            
            for invalidEODTradeStatus in invalidEODTradeStatuses:
                try:
                    self._invalidEODTradeStatusesList.append(str(ael.enum_from_string('TradeStatus', str(invalidEODTradeStatus.firstChild.data))))
                except Exception, e:
                    raise EXCEPTION('One of the Invalid EOD Trade Statuses could not be retreived in module %s.' %__name__,\
                    traceback, 'CRITICAL', e)
            self._invalidEODTradeStatuses = '(' + ",".join(self._invalidEODTradeStatusesList) + ')'
        else:
            raise ValueError('No InvalidEODTradeStatuses settings could be retreived in module %s.' %__name__)

        #Control Measure Columns
        controlMeasureColumnsXML = genericSettingsXML[0].getElementsByTagName('ControlMeasureColumns')
        if not controlMeasureColumnsXML:
            raise ValueError('No control measure column settings could be retrieved in module %s.' %__name__)
        if controlMeasureColumnsXML:
            controlMeasureColumns = controlMeasureColumnsXML[0].getElementsByTagName('ControlMeasureColumn')
            for controlMeasureColumn in controlMeasureColumns:
                try:
                    self._controlMeasureColumnsList.append(str(controlMeasureColumn.firstChild.data))
                except Exception, e:
                    raise EXCEPTION('One of the control measure columns could not be retreived in module %s.' %__name__,\
                        traceback, 'CRITICAL', e)

        #Shutdown times
        shutdownTimesXML = genericSettingsXML[0].getElementsByTagName('ShutdownTimes')
        if not shutdownTimesXML:
            raise ValueError('No shutdown time settings could be retrieved in module %s.' %__name__)
        if shutdownTimesXML:
            shutdownTimes = shutdownTimesXML[0].getElementsByTagName('ShutdownTime')
            for shutdownTime in shutdownTimes:
                try:
                    self._shutdownTimes.append(str(shutdownTime.firstChild.data))
                except Exception, e:
                    raise EXCEPTION('One of the shutdown times could not be retreived in module %s.' %__name__,\
                        traceback, 'CRITICAL', e)

            
        #List of labels that should be forced to a date due to the column definitions applying different formatting or none
        dateFormatLabelOverridesXML = genericSettingsXML[0].getElementsByTagName('DateFormatLabelOverrides')
        if dateFormatLabelOverridesXML:
            dateFormatLabelOverrides = dateFormatLabelOverridesXML[0].getElementsByTagName('Label')
            if not dateFormatLabelOverrides:
                raise ValueError('No Labels for Date Format Overrides could be retreived in module %s.' %__name__)
            
            for label in dateFormatLabelOverrides:
                try:
                    self._dateFormatLabelOverrides.append(str(label.firstChild.data))
                except Exception, e:
                    raise EXCEPTION('One of the Labels for Date Format Overrides could not be retreived in module %s.' %__name__,\
                    traceback, 'CRITICAL', e)

        #List of labels that should be forced to a date time due to the column definitions not applying any formatting
        dateTimeFormatLabelOverridesXML = genericSettingsXML[0].getElementsByTagName('DateTimeFormatLabelOverrides')
        if dateTimeFormatLabelOverridesXML:
            dateTimeFormatLabelOverrides = dateTimeFormatLabelOverridesXML[0].getElementsByTagName('Label')
            if not dateTimeFormatLabelOverrides:
                raise ValueError('No Labels for Date Time Format Overrides could be retreived in module %s.' %__name__)
            
            for label in dateTimeFormatLabelOverrides:
                try:
                    self._dateTimeFormatLabelOverrides.append(str(label.firstChild.data))
                except Exception, e:
                    raise EXCEPTION('One of the Labels for Date Time Format Overrides could not be retreived in module %s.' %__name__,\
                    traceback, 'CRITICAL', e)

        #List of labels that should be forced to a number due to the column definitions not applying any formatting
        numberFormatLabelOverridesXML = genericSettingsXML[0].getElementsByTagName('NumberFormatLabelOverrides')
        if numberFormatLabelOverridesXML:
            numberFormatLabelOverrides = numberFormatLabelOverridesXML[0].getElementsByTagName('Label')
            if not numberFormatLabelOverrides:
                raise ValueError('No Labels for Number Format Overrides could be retreived in module %s.' %__name__)
            
            for label in numberFormatLabelOverrides:
                try:
                    self._numberFormatLabelOverrides.append(str(label.firstChild.data))
                except Exception, e:
                    raise EXCEPTION('One of the Labels for Number Format Overrides could not be retreived in module %s.' %__name__,\
                    traceback, 'CRITICAL', e)
