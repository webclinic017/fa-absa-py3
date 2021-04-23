
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_PARAMETERS_ENVIRONMENT
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module determines the environment settings to be used to determine the
                                component settings. The specific DEV, UAT, PRD or DR environment will be
                                determined and used for the component settings.
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------
'''

'''----------------------------------------------------------------------------------------------------------
Importing all relevant Python modules.
----------------------------------------------------------------------------------------------------------'''
import acm
import xml.dom.minidom as xml
import traceback

'''----------------------------------------------------------------------------------------------------------
Importing Custom modules modules needed for Real Time ATS Worker.
----------------------------------------------------------------------------------------------------------'''
from FC_EXCEPTION import FC_EXCEPTION as EXCEPTION

'''----------------------------------------------------------------------------------------------------------
Class containing the environment settings of the environment being logged on
----------------------------------------------------------------------------------------------------------'''
class FC_PARAMETERS_ENVIRONMENT(object):
    def __init__(self):
        self._environment = None
        self._environment_name = None
    
    @property
    def environment(self):
        return self._environment
    
    @environment.setter
    def environment(self, value):
        self._environment = value

    @property
    def environment_name(self):
        return self._environment_name

    @environment_name.setter
    def environment_name(self, value):
        self._environment_name = value

'''----------------------------------------------------------------------------------------------------------
Retreiving The Current ADS Name And Port Used In This Connection
----------------------------------------------------------------------------------------------------------'''
try:
    arenaDataServer = acm.FDhDatabase['ADM'].ADSNameAndPort().lower()
except Exception, e:
    raise EXCEPTION('Could not determine the ADS Name and Port in module %s.' %__name__, traceback, 'CRITICAL', e)

'''----------------------------------------------------------------------------------------------------------
Identify Which Environment Setting Set To Use
----------------------------------------------------------------------------------------------------------'''
environmentSettings = acm.GetDefaultValueFromName(acm.GetDefaultContext(), acm.FObject, 'EnvironmentSettings')
if not environmentSettings:
    raise ValueError('The EnvironmentSettings Extension Value Module could not be retreived in module %s. The componet will not be able to retreived any settings.' %__name__)

environmentSettingsXML = xml.parseString(environmentSettings)
if not environmentSettingsXML:
    raise ValueError('The EnvironmentSettings XML could not be parsed in module %s. The componet will not be able to retreived any settings.' %__name__)

host = environmentSettingsXML.getElementsByTagName('Host')
if not host:
    raise ValueError('The Host could not be retreived from the EnvironmentSettings XML in module %s.' %__name__)

environmentSection = [e for e in host if e.getAttribute('Name').lower() == arenaDataServer]
if len(environmentSection) == 0:
    raise ValueError('No evironment item could be retreived that is matching the Arena Data Server (%s) being logged on in module %s.' %(arenaDataServer, __name__))
    
environmentSettingName = str(environmentSection[0].getAttribute('Setting'))
if not environmentSettingName:
    raise ValueError('The Setting attribute could not be retreived from the selected Environment Setting in module %s.' % __name__)

'''----------------------------------------------------------------------------------------------------------
Get Environment Settings
----------------------------------------------------------------------------------------------------------'''
configuration = acm.GetDefaultValueFromName(acm.GetDefaultContext(), acm.FObject, 'FA_CACHE_Config_Settings')
if not configuration:
    raise ValueError('The FA_CACHE_Config_Settings Extension Value Module could not be retreived in module %s. The componet will not be able to retreived any settings.' %__name__)
    
configurationXML = xml.parseString(configuration)
if not configurationXML:
    raise ValueError('The FA_CACHE_Config_Settings XML could not be parsed in module %s. The componet will not be able to retreived any settings.' %__name__)

override = configurationXML.getElementsByTagName('OverrideEnvironmentSetting')

environmentSettingName = environmentSettingName.translate(None, '0123456789')

enabled = override[0].getAttribute("Enabled")
use_setting = override[0].getAttribute("UseSetting")

if enabled == '1':
    environmentSettingName = override[0].getAttribute("UseSetting")

PARAMETERS_ENVIRONMENT = FC_PARAMETERS_ENVIRONMENT
for element in configurationXML.getElementsByTagName('Environment'):
    if element.getAttribute('ArenaDataServer').find(environmentSettingName) >= 0:
        PARAMETERS_ENVIRONMENT.environment = element
        PARAMETERS_ENVIRONMENT.environment_name = environmentSettingName.replace('Setting', '')
        break
if not PARAMETERS_ENVIRONMENT.environment:
    raise ValueError('Cannot find the Specific Environment Settings to use. This component cannot retreive the DEV, UAT, PRD or DR settings.')
