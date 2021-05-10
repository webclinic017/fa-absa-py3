'''----------------------------------------------------------------------------------------------------------
MODULE                  :       ATSParameters
PURPOSE                 :       Operations Document for Confirmation Manager and Trident Parameters are defined in this module
DEPARTMENT AND DESK     :       Operations
REQUESTER               :       IT
DEVELOPER               :       Tshepo Mabena
CR NUMBER               :       873236
-------------------------------------------------------------------------------------------------------------

HISTORY
=============================================================================================================
Date            Change no       Developer         Requester              Description
-------------------------------------------------------------------------------------------------------------
2012-01-12      873236          Tshepo Mabena     IT                     Reading integration parameters from a 
                                                                         config file in an environment which is 
                                                                         currently being run.
2012-02-28      XXXXXX          Heinrich Cronje   IT                     Sybase Exodus. Determine the environment first to
                                                                         get the correct settings to use. 
-------------------------------------------------------------------------------------------------------------

DESCRIPTION OF MODULE:
    
    Operations Document and Trident parameters are defined in this module.

'''

from FOperationsHook import CustomHook as Hook
import acm
import xml.dom.minidom as xml
import FOperationsUtils as Utils

environment = None
arenaDataServer = acm.FDhDatabase['ADM'].ADSNameAndPort().lower()
Utils.LogTrace()

'''===========================================================================================================
                                        Get Environment Setting Name
==========================================================================================================='''
environmentSettings = acm.GetDefaultValueFromName(acm.GetDefaultContext(), acm.FObject, 'EnvironmentSettings')
environmentSetting = xml.parseString(environmentSettings)
host = environmentSetting.getElementsByTagName('Host')
environment = [e for e in host if e.getAttribute('Name').lower() == arenaDataServer]

if len(environment) != 1:
    Utils.Log(True, 'ERROR: Could not find environment settings for %s.' % arenaDataServer)
    raise Exception('ERROR: Could not find environment settings for %s.' % arenaDataServer)

envSetting = str(environment[0].getAttribute('Setting'))

'''===========================================================================================================
                                            Get Environment Settings
==========================================================================================================='''

configuration = acm.GetDefaultValueFromName(acm.GetDefaultContext(), acm.FObject, 'FConfirmation_Config_Settings')

config = xml.parseString(configuration)

for element in config.getElementsByTagName('Environment'):
    
    if element.getAttribute('ArenaDataServer').find(envSetting) >= 0:
        environment = element
        break
else:   
    Utils.Log(True, 'ERROR: Could not find configuration settings for %s.' % arenaDataServer)
    raise Exception('ERROR: Could not find configuration settings for %s.' % arenaDataServer)

try:
    ambAddress                      = element.getElementsByTagName('ambAddress')[0].firstChild.data + ':' + element.getElementsByTagName('Port')[0].firstChild.data
    tridentConnectionReceiverMBName = element.getElementsByTagName('tridentConnectionReceiverMBName')[0].firstChild.data
    affirmationReceiverMBName       = element.getElementsByTagName('affirmationReceiverMBName')[0].firstChild.data
    documentationReceiverMBName     = element.getElementsByTagName('documentationReceiverMBName')[0].firstChild.data
    tridentConnectionSenderMBName   = element.getElementsByTagName('tridentConnectionSenderMBName')[0].firstChild.data
    
    receiverSource = element.getElementsByTagName('ReceiverSource')[0].firstChild.data
    
    MQChannel = element.getElementsByTagName('MQChannel')[0].firstChild.data
    MQSecExit = element.getElementsByTagName('MQSecExit')[0].firstChild.data
    
    MQQueueManager         = element.getElementsByTagName('MQQueueManager')[0].firstChild.data    
    MQHostName             = element.getElementsByTagName('MQHostName')[0].firstChild.data    
    MQTridentSenderQueue   = element.getElementsByTagName('MQTridentSenderQueue')[0].firstChild.data    
    MQTridentReceiverQueue = element.getElementsByTagName('MQTridentReceiverQueue')[0].firstChild.data 
    
except:
    
    Utils.Log(True, 'ERROR: Could not find environment setting elements for %s.' % arenaDataServer)
    raise Exception('ERROR: Could not find environment setting elements for %s.' % arenaDataServer)
