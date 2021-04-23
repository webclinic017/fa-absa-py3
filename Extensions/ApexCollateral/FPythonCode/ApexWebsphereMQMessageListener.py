"""
Entry point for Apex -> FA integration.

This job takes messages from MQ and makes changes to FA data accordingly.

Contact mail group: CIB Africa MAPEX BTB
"""
import sys 
#sys.path.append(r'/opt/front/arena/lib64/pythonextensionlib27/pymqi')

import socket
import time
import acm
import ApexParameters
import ApexMessageProcessors as apex
import pymqi
from pymqi import CMQC
import FOperationsUtils as Utils

Params = ApexParameters.load()

sleepTime = None
queueManager = None
messageCount = 0


def getMessageOffQueue(queueManager, queueName):

    msg = None

    try:
        queue = pymqi.Queue(queueManager, queueName)
        msg = queue.get()
        if msg is not None:
            queue.close()
    except pymqi.MQMIError as e:
        if not (e.comp == CMQC.MQCC_FAILED and e.reason == CMQC.MQRC_NO_MSG_AVAILABLE):
            raise

    return msg


def work():
    global messageCount
    messageCount = messageCount + 1
    if messageCount % 100 == 0:
        Utils.Log(True, 'Checking if any messages have been placed on queues')
        messageCount = 0

    message = getMessageOffQueue(queueManager, Params.TradeActivityQueueName)
    if message is not None:
        apex.processTradeActivityQueueMessage(message)

    agreementMessage = getMessageOffQueue(queueManager, Params.AgreementQueueName)
    if agreementMessage is not None:
        apex.processCsaAgreementItemMessage(agreementMessage)

    if message == None and agreementMessage == None:
        time.sleep(sleepTime)


def start():
    global queueManager, sleepTime, messageCount
    messageCount = 0
    Utils.Log(True, "Starting %s at %s on %s" % (__name__, acm.Time.TimeNow(), socket.gethostname()))
    sleepTime = Params.SleepTime

    client = "%s(%s)" % (Params.WebSphereMQHost, Params.WebSphereMQPort)
    cd = pymqi.cd()
    cd.ChannelName = Params.WebSphereMQChannel
    cd.ConnectionName = client
    cd.ChannelType = CMQC.MQCHT_CLNTCONN
    cd.TransportType = CMQC.MQXPT_TCP
    '''
    if Params.WebSphereChannelSecured.lower() == 'true':
        Utils.Log(True, 'Using security exit channel %s' %Params.WebSphereMQChannel)
        cd.SecurityExit = "BCPKIJCExit_70R(SECSEND)"
    else:
        Utils.Log(True, 'Using unsecured exit channel %s' %Params.WebSphereMQChannel)
    '''
    queueManager = pymqi.QueueManager(None)
    Utils.Log(True, "Connecting to: %s" % client)
    queueManager.connectWithOptions(Params.WebSphereMQQueueManager, cd)
    Utils.Log(True, "Connected!")


def stop():
    if queueManager is not None:
        queueManager.disconnect()
    Utils.Log(True, "Stopping %s at %s on %s" % (__name__, acm.Time.TimeNow(), socket.gethostname()))

