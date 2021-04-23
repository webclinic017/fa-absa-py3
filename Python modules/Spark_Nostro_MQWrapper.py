'''-----------------------------------------------------------------------------
PROJECT                 :  Spark Non ZAR Cashflow Feed
PURPOSE                 :  Pymqi wrapper for use in FA
DEPATMENT AND DESK      :  PCG/Ops
REQUESTER               :  Nick Bance
DEVELOPER               :  Anwar Banoo
CR NUMBER               :  XXXXXX
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no Developer                 Description
--------------------------------------------------------------------------------
2011-10-25 XXXXXX                              Initial Implementation
'''

#uses install package: pymqi-1.0.1.win32-py2.5-mq6.0-client.exe
import pymqi
import CMQC
import acm
import time
import FLogger

TIME_FORMAT = '%Y/%m/%d %H:%M:%S'

class MqMessenger:
    
    def __init__(self, SparksConfig, flogger = None):
        self.__config = SparksConfig
        if not flogger:
            self.__logger = FLogger.FLogger('Spark_Nostro')
        else:
            self.__logger = flogger
        self.__queueManager = self.__ConnectToQueueManager()
                
        # Message Descriptor
        self.__md = pymqi.md()

        # Get Message Options
        self.__gmo = pymqi.gmo()
        self.__gmo.Options = CMQC.MQGMO_WAIT | CMQC.MQGMO_FAIL_IF_QUIESCING | CMQC.MQGMO_BROWSE_NEXT
        self.__gmo.WaitInterval = 5000 # 5 seconds

        
    def __ConnectToQueueManager(self):
        cd = pymqi.cd()
        cd.ChannelName  = self.__config.channel
        cd.ConnectionName = self.__config.client
        cd.ChannelType    = CMQC.MQCHT_CLNTCONN
        cd.TransportType  = CMQC.MQXPT_TCP
        
        queueManager = pymqi.QueueManager(None)
        try:
            queueManager.connectWithOptions(self.__config.queue_manager, cd)
            return queueManager
        except Exception, ex:
            raise Exception('Error connecting to queue manager [%(manager)s] on client [%(client)s]: %(ex)s' % 
                {'manager': self.__config.queue_manager, 'client': self.__config.client, 'ex': ex})
        
    def Put(self, message):        
        try:            
            self.__queueManager.put1(self.__config.queue_name, message)
            print('MQ message put on %(queueManagerName)s:%(queueName)s at %(time)s.' % \
                {'queueManagerName': self.__config.queue_manager, 'queueName': self.__config.queue_name, 'time': time.strftime(TIME_FORMAT)})
        except Exception, ex:
            raise Exception('Error while putting message on queue [%(queue)s]: %(ex)s' % {'queue': self.__config.queue_name, 'ex': ex})
            
    def ReadMessage(self, leaveMessage = True):
        msg = ''
        
        try:
            md = pymqi.md()
            gmo = pymqi.gmo()

            if leaveMessage:
                queue = pymqi.Queue(self.__queueManager, self.__config.queue_name, CMQC.MQOO_BROWSE)
                gmo.Options = CMQC.MQGMO_BROWSE_NEXT
            else:
                queue = pymqi.Queue(self.__queueManager, self.__config.queue_name)

            msg = queue.get(None, md, gmo)

        except pymqi.MQMIError, e:
            if e.comp == CMQC.MQCC_FAILED and e.reason == CMQC.MQRC_NO_MSG_AVAILABLE:
                # No messages, that's OK, we can ignore it.
                pass
            else:
                raise e            
            
        return msg
    
    def AcceptMessage(self):
        return self.ReadMessage(False) is not None        
        
    def DisconnectQueueManager(self):
        if self.__queueManager:
            self.__queueManager.disconnect()
