#-----------------------------------------------------------------------------------------------------------------
#  Developer           : Tshepo Mabena
#  Purpose             : This module reads off midas xml response messages from the MQ and removes them.
#  Department and Desk : Front Arena BTB/RTB
#  Requester           : Front Arena BTB/RTB
#  CR Number           : CR 587810
#-----------------------------------------------------------------------------------------------------------------

import acm, time
import win32com
import win32com.client
import MidasParameters
from  Midas_FATradeUpdate import ProcessTradeXML

def ReceiveMessage(MQMessageCOM, MQResponseCOM):
    
    try:
        MQMessage = ""
        
        if MQMessageCOM.IsQueueManagerConnected:
            if MQMessageCOM.GetQueueDepth(MidasParameters.MidasMQReceiverQueue) >= 1:
                MQResponseCOM = MQMessageCOM.Peek(MidasParameters.MidasMQReceiverQueue)
                if not MQResponseCOM.Success:
                    errorMsg = str(MQResponseCOM.ReasonCode) + ' : ' + MQResponseCOM.ReasonMessage
                    acm.Log('Failed to peek message : ' + errorMsg)
                    pushMessageFailed = True
                elif MQResponseCOM.Success:
                    MQMessage = MQResponseCOM.MessageData
                    
                    ProcessTradeXML(MQMessage) 
                    acm.Log("Peeked at message ")
                    AcceptMessage(MQMessageCOM, MQResponseCOM)
                    
        else:
            errorMsg = str(MQResponseCOM.ReasonCode) + ' : ' + str(MQResponseCOM.ReasonMessage)
            acm.Log('No messages on MQ. Cannot peek at message: ' + errorMsg)
            pushMessageFailed = True
        
    except Exception, e:
        
        print 'Error: ', e
       
        
def AcceptMessage(MQMessageCOM, MQResponseCOM):

    try:
        MQMessage = ""
        if MQMessageCOM.IsQueueManagerConnected:
            MQResponseCOM = MQMessageCOM.Get(MidasParameters.MidasMQReceiverQueue)
            if not MQResponseCOM.Success:
                errorMsg = str(MQResponseCOM.ReasonCode) + ' : ' + MQResponseCOM.ReasonMessage
                acm.Log('Failed to remove message : ' + errorMsg)
                pushMessageFailed = True
            else:
                MQMessage = MQResponseCOM.MessageData
                
                acm.Log("Removed message ")
        else:
            errorMsg = str(MQResponseCOM.ReasonCode) + ' : ' + MQResponseCOM.ReasonMessage
            acm.Log('Connection to MQ is down. Can not get at message: ' + errorMsg)
            pushMessageFailed = True
        
    except Exception, e:
        
        print 'Error: ', e
    
def start():
    
    MQMessageCOM = win32com.client.Dispatch('ACMQLib.WMQ6Wrapper')
    MQResponseCOM = win32com.client.Dispatch('ACMQLib.MQResponse')
    MQResponseConnectionCOM = win32com.client.Dispatch('ACMQLib.MQResponse')
    MQResponseConnectionCOM = MQMessageCOM.Initialise(MidasParameters.MidasMQHostName, MidasParameters.MidasMQChannel, MidasParameters.MidasMQQueueManager, MidasParameters.MQSecExit)
    
    if MQResponseConnectionCOM.Success:
        errorMsg = str(MQResponseConnectionCOM.ReasonCode) + ' : ' + MQResponseConnectionCOM.ReasonMessage
        acm.Log('Connection to MQ is successful: ' + errorMsg)
        
        while MQResponseConnectionCOM.Success:
            time.sleep(2)
            ReceiveMessage(MQMessageCOM, MQResponseCOM)
            
        errorMsg = str(MQResponseCOM.ReasonCode) + ' : ' + MQResponseCOM.ReasonMessage
        acm.Log('Connection to MQ not successful: ' + errorMsg)
    else:
        errorMsg = str(MQResponseCOM.ReasonCode) + ' : ' + MQResponseCOM.ReasonMessage
        acm.Log('Connection to MQ not successful: ' + errorMsg)

