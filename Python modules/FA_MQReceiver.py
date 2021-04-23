#------------------------------------------------------------------------------------------------------------
#  Developer           : Tshepo Mabena
#  Purpose             : This module reads-off the response message from MQ which is sent from Midas.
#  Department and Desk : Fx Desk
#  Requester           : Justin Nichols
#  CR Number           : CR 431665
#------------------------------------------------------------------------------------------------------------

import acm
import os
import time
import xml.dom.minidom as xml

import sys 
sys.path.append(r"C:\Program Files\Front\Front Arena\CommonLib\PythonLib25\pymqi")
import pymqi
import CMQC

timeFormat = ' %Y%m%d %H %M %S'

class Config:
    _filepath = r'C:\Program Files\FRONT\ReceiveConfig\config.xml'
    
    _baseNode = 'FAMIDAS'
    
    @staticmethod
    def raiseNodeNotFound(nodeName):
        raise Exception('Could not find <%(node)s> in file [%(filepath)s] to read the configuration settings.' % \
            {'node': nodeName, 'filepath': Config._filepath})
            
    @staticmethod
    def getMandatoryValue(baseNode, nodeName):
        nodes = baseNode.getElementsByTagName(nodeName)
            
        if not nodes:
            Config.raiseNodeNotFound(nodeName)
            
        if nodes.length > 1:
            raise Exception('<%(node)s> cannot have more than one value, please correct in [%(filepath)s].' % \
            {'node': nodeName, 'filepath': Config._filepath})
        
        node = nodes[0]
        value = None
        if node.hasChildNodes():
            node = node.firstChild
            if node.nodeType == node.TEXT_NODE:
                value = str(node.data)
                
        if not value:
            raise Exception('<%(node)s> cannot be empty, please correct in [%(filepath)s].' % \
            {'node': nodeName, 'filepath': Config._filepath})
        
        return value
        
    
    def __init__(self):
        if not os.path.exists(Config._filepath):
            raise Exception('Config file not found: %s' % Config._filepath)
            
        configDoc = xml.parse(Config._filepath)
    
        nodes = configDoc.getElementsByTagName(Config._baseNode)
        baseNode = nodes[0]
        
        if not baseNode:
            Config.raiseNodeNotFound(Config._baseNode)
                
        self.queueName = Config.getMandatoryValue(baseNode, 'QueueName')
        self.queueManager = Config.getMandatoryValue(baseNode, 'QueueManager')
        self.channel = Config.getMandatoryValue(baseNode, 'Channel')
        self.host = Config.getMandatoryValue(baseNode, 'Host')
        self.port = Config.getMandatoryValue(baseNode, 'Port')
        self.inbox = Config.getMandatoryValue(baseNode, 'Inbox')
        self.sleep = float(Config.getMandatoryValue(baseNode, 'SleepSeconds'))
        
def getOffQueue(config):

    queueManager = pymqi.QueueManager(None)
    
    client = "%s(%s)" % (config.host, config.port)
    cd = pymqi.cd()
    cd.SecurityExit   = "BCPKIJCExit_60R(SECSEND)"
    cd.ChannelName    = config.channel
    cd.ConnectionName = client
    cd.ChannelType    = CMQC.MQCHT_CLNTCONN
    cd.TransportType  = CMQC.MQXPT_TCP                    
    
    try:
        queueManager.connectWithOptions(config.queueManager, cd)
    except Exception, e:
        raise Exception('Error during connection: ' + str(e))
        
    msg = ''
    
    try:    
        queue = pymqi.Queue(queueManager, config.queueName)
        msg   = queue.get()
        if msg:
            file_name = os.path.join(config.inbox, "Midas_Message" + time.strftime(timeFormat) + ".xml")
            outfile   = open(file_name, 'w')
            outfile.write(msg)
            outfile.close()
            queue.close()
        else:
            pass
    except Exception, e:
        print 'Message not received' + ' ' + msg, Exception
        
    return msg    
        
def start():
    
    acm.Log('Startng FA_MQReceiver process at ' + time.strftime(timeFormat))
    config = Config()
    
    sleeptime = config.sleep
    if sleeptime < 5.0:
        sleeptime = 5.0

    while True:
        getOffQueue(config)
        time.sleep(sleeptime)
       

