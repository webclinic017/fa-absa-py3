'''-----------------------------------------------------------------------------
Date:                   2010-05-13
Purpose:                Polls a directory for files and places them on an MQ 
                        queue. The queue detail and directory to poll are stored
                        in a conig file. This module requires pymqi 
                        (http://packages.python.org/pymqi) and MQ Client.
Department and Desk:    Cash Equities
Requester:              Nicole Dunlop
Developer:              Francois Truter
CR Number:              313068

Date:                   2010-05-27
Purpose:                Amended code to connect to a secure MQ channel
Department and Desk:    Cash Equities
Requester:              Nicole Dunlop
Developer:              Herman Hoon
CR Number:              325180
-----------------------------------------------------------------------------'''
import acm
import os
import time
import xml.dom.minidom as xml

import sys 
sys.path.append(r"C:\Program Files\Front\Front Arena\CommonLib\PythonLib25\pymqi")
import pymqi
import CMQC

timeFormat = '%Y/%m/%d %H:%M:%S'

class Config:
    _filepath = r'C:\Program Files\Front\config.xml'
    _baseNode = 'CashEquityCompassIntegration'
    
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
        self.maxFileAge = Config.getMandatoryValue(baseNode, 'MaxFileAgeSeconds')
        self.sleep = float(Config.getMandatoryValue(baseNode, 'SleepSeconds'))
            
def PutFileOnQueue(config):
    errorSuffix = '.err'
    filepath = ''
    try:
        client = "%s(%s)" % (config.host, config.port)
        for path in os.listdir(config.inbox):
            filepath = os.path.join(config.inbox, path)
            if os.path.isfile(filepath) and not filepath.endswith(errorSuffix) and time.time() - os.path.getmtime(filepath) < config.maxFileAge:
                fileContents = ''
                with open(filepath, 'r') as file:
                    fileContents = file.read()

                if fileContents:
                    queueManager = pymqi.QueueManager(None)
                    
                    cd = pymqi.cd()
                    cd.SecurityExit = "BCPKIJCExit_60R(SECSEND)"
                    cd.ChannelName  = config.channel
                    cd.ConnectionName = client
                    cd.ChannelType    = CMQC.MQCHT_CLNTCONN
                    cd.TransportType  = CMQC.MQXPT_TCP                    

                    try:
                        queueManager.connectWithOptions(config.queueManager, cd)
                    except Exception as e:
                        raise Exception('Error during connection: ' + str(e))
                    
                    try:
                        queueManager.put1(config.queueName, fileContents)
                        acm.Log('MQ message put on %(queueManagerName)s:%(queueName)s at %(time)s.' % \
                            {'queueManagerName': config.queueManager, 'queueName': config.queueName, 'time': time.strftime(timeFormat)})
                        
                        os.remove(filepath)
                        
                    finally:
                        queueManager.disconnect()

    except Exception as ex:
        acm.Log('The following exception occured %(time)s: %(exception)s' % {'time': time.strftime(timeFormat), 'exception': str(ex)})
        
        
        if os.path.exists(filepath):
            newFilepath = filepath + errorSuffix
            os.rename(filepath, newFilepath)
            acm.Log('[%(original)s] renamed [%(new)s]' % {'original': filepath, 'new': newFilepath})
           
def start():
    acm.Log('Startng CashEquityMQProcessor at ' + time.strftime(timeFormat))
    config = Config()
    sleeptime = config.sleep
    if sleeptime < 5.0:
        sleeptime = 5.0

    while True:
        PutFileOnQueue(config)
        time.sleep(sleeptime)
        
def stop():
    acm.Log('Stopping CashEquityMQProcessor at ' + time.strftime(timeFormat))
