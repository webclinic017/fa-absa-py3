'''---------------------------------------------------------------------------------------------------
PROJECT                 :  Markets Message Gateway
PURPOSE                 :  Put messages on MQ
DEPATMENT AND DESK      :
REQUESTER               :
DEVELOPER               :  Francois Truter
CR NUMBER               :  XXXXXX
------------------------------------------------------------------------------------------------------

HISTORY
======================================================================================================
Date       Change no            Developer                            Description
------------------------------------------------------------------------------------------------------
2011-03-25 XXXXXX               Francois Truter           Initial Implementation
2015-09-02 CHNG                 Rohan Van der Walt        Changed path to Python libraries and added
                                                          reference to Environment settings
2017                            Willie van der Bank       Updated python version for 2017 upgrade
2020-10-27 CHNG                 Jaysen Naicker            Added in option to use FParameters instead of
                                                          FExtensionValue to store MQ parameters

'''

import sys 
sys.path.append(r'/front/arena/apps/lib64/pythonextensionlib27/pymqi')

import pymqi
import CMQC
import acm
import time
from gen_absa_xml_config_settings import MqXmlConfig

TIME_FORMAT = '%Y/%m/%d %H:%M:%S'

class MqMessenger:
    
    def __init__(self, baseNodeName, connectNow = False, useFParameters = False):
        print('Retrieving Settings for:', baseNodeName)
        self._config = MqXmlConfig(baseNodeName, useFParameters)
        self._queueMgr = None
        if connectNow:
            self._connectToQueueManager(persistent = True)
        
    def _connectToQueueManager(self, persistent = False):
        if persistent:
            print('Using Queue Details:')
            print('host(port):', self._config.Client)
            print('Queue Manager', self._config.QueueManager)
            print('Channel Name:', self._config.Channel)
        cd = pymqi.cd()
        cd.ChannelName  = self._config.Channel
        cd.ConnectionName = self._config.Client
        cd.ChannelType    = CMQC.MQCHT_CLNTCONN
        cd.TransportType  = CMQC.MQXPT_TCP
        
        queueManager = pymqi.QueueManager(None)
        try:
            queueManager.connectWithOptions(self._config.QueueManager, cd)
            if persistent:
                self._queueMgr = queueManager            
            return queueManager
        except Exception, ex:
            raise Exception('Error connecting to queue manager [%(manager)s] on client [%(client)s]: %(ex)s' % 
                {'manager': self._config.QueueManager, 'client': self._config.Client, 'ex': ex})
                
    def Put(self, message, print_output = True):
        queueManager = self._connectToQueueManager()
        try:
            putq = pymqi.Queue(queueManager, self._config.QueueName)
            putq.put(message)
            if print_output:
                print('MQ message put on %(queueManagerName)s:%(queueName)s at %(time)s.' % \
                    {'queueManagerName': self._config.QueueManager, 'queueName': self._config.QueueName, 'time': time.strftime(TIME_FORMAT)})
            putq.close()
        except Exception, ex:
            raise Exception('Error while putting message on queue [%(queue)s]: %(ex)s' % {'queue': self._config.QueueName, 'ex': ex})
        finally:
            queueManager.disconnect()

    def Disconnect(self):
        if self._queueMgr:
            self._queueMgr.disconnect()

    def Get(self, get_no_rfh2 = False):
        if self._queueMgr:
            # Message Descriptor
            md = pymqi.MD()

            # Get Message Options
            gmo = pymqi.GMO()
            gmo.Options = CMQC.MQGMO_WAIT | CMQC.MQGMO_FAIL_IF_QUIESCING
            gmo.WaitInterval = 5000 # 5 seconds
            
            getq = pymqi.Queue(self._queueMgr, self._config.QueueName)
            if get_no_rfh2:
                result = getq.get_no_rfh2(None, md, gmo)
            else:
                result = getq.get(None, md, gmo)
            
            getq.close()
            
            return result
        else:
            raise Exception('QueueManager not connected')

