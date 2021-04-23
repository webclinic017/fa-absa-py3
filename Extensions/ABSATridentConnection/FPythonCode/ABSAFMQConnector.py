""" Compiled: NONE NONE """
import win32com
import win32com.client
import acm
import xml.dom.minidom as xml
import sys 
import ATSParameters

class ABSAFMQConnector(object):
    def __init__(self):
        self.__MQMessageCOM = win32com.client.Dispatch('ACMQLib.WMQ6Wrapper')
        self.__MQResponseCOM = win32com.client.Dispatch('ACMQLib.MQResponse')
        self.__MQResponseConnectionCOM = win32com.client.Dispatch('ACMQLib.MQResponse')
        self.__MQResponseConnectionCOM = self.__MQMessageCOM.Initialise(ATSParameters.MQHostName, ATSParameters.MQChannel, ATSParameters.MQQueueManager, ATSParameters.MQSecExit)
        if self.__MQResponseConnectionCOM.Success:
            errorMsg = str(self.__MQResponseConnectionCOM.ReasonCode) + ' : ' + self.__MQResponseConnectionCOM.ReasonMessage
            acm.Log('Connection to MQ is successful: ' + errorMsg)
        
    def __del__(self):
        acm.Log('Closing Connection')
        self.__MQResponseConnectionCOM = self.__MQMessageCOM.Finalise()
        acm.Log('Disconnection to MQ is successful.')
        self.__MQResponseConnectionCOM = None
        self.__MQResponseCOM = None
    
    def PushMessage(self, message, operationsDocument):
        try:
            pushMessageFailed = False
            if self.__MQMessageCOM.IsQueueManagerConnected:
                self.__MQResponseCOM = self.__MQMessageCOM.Put(ATSParameters.MQTridentSenderQueue, message)
                if not self.__MQResponseCOM.Success:
                    errorMsg = str(self.__MQResponseCOM.ReasonCode) + ' : ' + self.__MQResponseCOM.ReasonMessage
                    acm.Log('Failed to put message : ' + errorMsg)
                    pushMessageFailed = True
                else:
                    if operationsDocument:
                        acm.Log("Sending BARML to Trident " + str(operationsDocument.Confirmation().Oid()))
                    else:
                        acm.Log("Received incorrect message from Trident. Sent for database logging")
            else:
                errorMsg = str(self.__MQResponseCOM.ReasonCode) + ' : ' + self.__MQResponseCOM.ReasonMessage
                acm.Log('Connection to MQ is down. Can not sent XML: ' + errorMsg)
                pushMessageFailed = True
            
        except Exception, e:
            # Some other error condition.
            print 'Error: ', e

        finally:
            self.__MQMessageCOM.Close()

        return pushMessageFailed
        
    def PeakMessage(self):
        try:
            MQMessage = ""
            if self.__MQMessageCOM.IsQueueManagerConnected:
                if self.__MQMessageCOM.GetQueueDepth(ATSParameters.MQTridentReceiverQueue) >= 1:
                    self.__MQResponseCOM = self.__MQMessageCOM.Peek(ATSParameters.MQTridentReceiverQueue)
                    if not self.__MQResponseCOM.Success:
                        errorMsg = str(self.__MQResponseCOM.ReasonCode) + ' : ' + self.__MQResponseCOM.ReasonMessage
                        acm.Log('Failed to peek message : ' + errorMsg)
                        pushMessageFailed = True
                    else:
                        MQMessage = self.__MQResponseCOM.MessageData
                        acm.Log("Peeked at message ")
            else:
                errorMsg = str(self.__MQResponseCOM.ReasonCode) + ' : ' + self.__MQResponseCOM.ReasonMessage
                acm.Log('Connection to MQ is down. Can not peek at message: ' + errorMsg)
                pushMessageFailed = True
            
        except Exception, e:
            # Some other error condition.
            print 'Error: ', e

        finally:
            self.__MQMessageCOM.Close()
        
        if MQMessage:
            print MQMessage
            return MQMessage
    
    def AcceptMessage(self):
        try:
            MQMessage = ""
            if self.__MQMessageCOM.IsQueueManagerConnected:
                self.__MQResponseCOM = self.__MQMessageCOM.Get(ATSParameters.MQTridentReceiverQueue)
                if not self.__MQResponseCOM.Success:
                    errorMsg = str(self.__MQResponseCOM.ReasonCode) + ' : ' + self.__MQResponseCOM.ReasonMessage
                    acm.Log('Failed to remove message : ' + errorMsg)
                    pushMessageFailed = True
                else:
                    MQMessage = self.__MQResponseCOM.MessageData
                    acm.Log("Removed message ")
            else:
                errorMsg = str(self.__MQResponseCOM.ReasonCode) + ' : ' + self.__MQResponseCOM.ReasonMessage
                acm.Log('Connection to MQ is down. Can not get at message: ' + errorMsg)
                pushMessageFailed = True
            
        except Exception, e:
            # Some other error condition.
            print 'Error: ', e

        finally:
            self.__MQMessageCOM.Close()

        return MQMessage
