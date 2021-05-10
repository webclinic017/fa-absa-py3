'''-----------------------------------------------------------------------------
PROJECT                 : Markets Message Gateway
PURPOSE                 : Reads config settings from FExtensionValue
                          'AbsaXmlConfigSettings'
DEPATMENT AND DESK      :
REQUESTER               :
DEVELOPER               : Francois Truter
CR NUMBER               : 695005
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no            Developer               Description
--------------------------------------------------------------------------------
2011-03-25 686159               Francois Truter         Initial Implementation
2011-06-23 695005               Francois Truter         Removed filpath from error mesages
2012-02-28 XXXXXX               Heinrich Cronje         Sybase Exodus. Determine the environment first to
                                                        get the correct settings to use.
2017-12-11 CHNG0005220511       Manan Gosh	        DIS go-live
2020-10-27 CHNG                 Jaysen Naicker          Added in option to use FParameters instead of
                                                        FExtensionValue to store MQ parameters
'''

import os
import xml.dom.minidom as xml
import acm
import FOperationsUtils as Utils

MANDATORY = True
OPTIONAL = False

class AbsaXmlConfigSettings(object):
    
    def __init__(self):
        self._environmentRoot = None
        arenaDataServer = acm.FDhDatabase['ADM'].ADSNameAndPort()
        #Converting the arenaDataServer string to lower case for comparison to be successful
        arenaDataServer = arenaDataServer.lower()
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

        configuration = acm.GetDefaultValueFromName(acm.GetDefaultContext(), acm.FObject, 'AbsaXmlConfigSettings')
        self._doc = xml.parseString(configuration)
        
        for element in self._doc.getElementsByTagName('Environment'):
            if element.getAttribute('ArenaDataServer').find(envSetting) >= 0:
                self._environmentRoot = element
                break
        else:
            raise Exception('Could not find configuration settings for [%s].' % arenaDataServer)
    
    def _raiseNodeNotFound(self, nodeName):
        raise Exception('Could not find <%(node)s> to read the configuration settings.' % {'node': nodeName})
    
    def GetUniqueNode(self, nodeName, baseNode = None):
        if not baseNode:
            baseNode = self._environmentRoot

        nodes = baseNode.getElementsByTagName(nodeName)
        if not nodes:
            self._raiseNodeNotFound(nodeName)
            
        if nodes.length > 1:
            raise Exception('Expected only one instance of <%(node)s>, found %(len)i. Please correct to configuration settings.' % \
                {'node': nodeName, 'len': nodes.length})
        
        return nodes[0]
     
    def GetFParameter(self, nodeName, baseNode = None):
        try:
            import FSwiftMLUtils
            node = FSwiftMLUtils.Parameters(nodeName)
        except:
            self._raiseNodeNotFound(nodeName)
        
        return node
           
    def GetValue(self, baseNode, nodeName, mandatory):
        node = self.GetUniqueNode(nodeName, baseNode)
        value = None
        if node.hasChildNodes():
            node = node.firstChild
            if node.nodeType == node.TEXT_NODE:
                value = str(node.data)
                
        if mandatory and not value:
            raise Exception('<%(node)s> cannot be empty, please correct the configuration settings.' % {'node': nodeName})
        
        return value
        
        
class MqXmlConfig(AbsaXmlConfigSettings):
        
    def __init__(self, baseNodeName, useFParameters = False):
        super(MqXmlConfig, self).__init__()
        if useFParameters:
            self._baseNode = self.GetFParameter(baseNodeName)
        
            self._queueName = getattr(self._baseNode, 'QueueName', None)
            self._queueManager = getattr(self._baseNode, 'QueueManager', None)
            self._channel = getattr(self._baseNode, 'Channel', None)
            self._host = getattr(self._baseNode, 'Host', None)
            self._port = getattr(self._baseNode, 'Port', None)
        else:
            self._baseNode = self.GetUniqueNode(baseNodeName)
            
            self._queueName = self.GetValue(self._baseNode, 'QueueName', MANDATORY)
            self._queueManager = self.GetValue(self._baseNode, 'QueueManager', MANDATORY)
            self._channel = self.GetValue(self._baseNode, 'Channel', MANDATORY)
            self._host = self.GetValue(self._baseNode, 'Host', MANDATORY)
            self._port = self.GetValue(self._baseNode, 'Port', MANDATORY)
            
    @property
    def QueueName(self):
        return self._queueName
        
    @property
    def QueueManager(self):
        return self._queueManager
        
    @property
    def Channel(self):
        return self._channel
        
    @property
    def Host(self):
        return self._host
        
    @property
    def Port(self):
        return self._port
        
    @property
    def Client(self):
        return "%s(%s)" % (self.Host, self.Port)
        
class AmbaType(object):
    Sender = 1
    Receiver = 2
    SenderAndReceiver = 3
        
class AmbaXmlConfig(AbsaXmlConfigSettings):

    def __init__(self, baseNodeName, ambaType):
        AbsaXmlConfigSettings.__init__(self)
        self._baseNode = self.GetUniqueNode(baseNodeName)
        
        self._host = self.GetValue(self._baseNode, 'Host', MANDATORY)
        self._port = self.GetValue(self._baseNode, 'Port', MANDATORY)
        
        mandatory = (ambaType == AmbaType.Sender or ambaType == AmbaType.SenderAndReceiver)
        self._senderName = self.GetValue(self._baseNode, 'SenderName', mandatory)
        self._senderSource = self.GetValue(self._baseNode, 'SenderSource', mandatory)
        
        mandatory = (ambaType == AmbaType.Receiver or ambaType == AmbaType.SenderAndReceiver)
        self._receiverName = self.GetValue(self._baseNode, 'ReceiverName', mandatory)
        self._receiverSource = self.GetValue(self._baseNode, 'ReceiverSource', mandatory)
        
    @property
    def Host(self):
        return self._host
        
    @property
    def Port(self):
        return self._port
        
    @property
    def InitString(self):
        return '%s:%s' % (self.Host, self.Port)
        
    @property
    def SenderName(self):
        return self._senderName
        
    @property
    def SenderSource(self):
        return self._senderSource
    
    @property
    def ReceiverName(self):
        return self._receiverName
    
    @property
    def ReceiverSource(self):
        return self._receiverSource

class SwiftParamXmlConfig(AbsaXmlConfigSettings):
    def __init__(self, baseNodeName):
        AbsaXmlConfigSettings.__init__(self)
        self._baseNode = self.GetUniqueNode(baseNodeName)
        
        self._logicalTerminalBic = self.GetValue(self._baseNode, 'LogicalTerminalBic', MANDATORY)
        try:
            self._isinMgmtBicExtension = self.GetValue(self._baseNode, 'IsinMgmtBicExtension', MANDATORY)
        except:
            self._isinMgmtBicExtension = 'XXX'

        try:
            self._issueragentBicExtension = self.GetValue(self._baseNode, 'IssueragentBicExtension', MANDATORY)
        except:
            self._issueragentBicExtension = 'XXX'

        try:
            self._settlingBankBicExtension = self.GetValue(self._baseNode, 'SettlingBankBicExtension', MANDATORY)
        except:
            self._settlingBankBicExtension = 'XXX'
        
    @property
    def LogicalTerminalBic(self):
        return self._logicalTerminalBic
    
    @property
    def IsinMgmtBicExtension(self):
        return self._isinMgmtBicExtension

    @property
    def IssueragentBicExtension(self):
        return self._issueragentBicExtension

    @property
    def SettlingBankBicExtension(self):
        return self._settlingBankBicExtension        
