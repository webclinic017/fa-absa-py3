#-----------------------------------------------------------------------------------------------------------------
#  Developer           : Tshepo Mabena
#  Purpose             : This module connects to the MQ and places the xml messages to be sent to midas and logs
#                        the messages into the database.       
#  Department and Desk : Front Arena BTB/RTB
#  Requester           : Front Arena BTB/RTB
#  CR Number           : 587810
#-----------------------------------------------------------------------------------------------------------------

import acm, ael, amb, time
import win32com
import win32com.client
import MidasParameters
from  Midas_FATradeUpdate import ProcessTradeXML

def MQConnector():

    MQMessageCOM = win32com.client.Dispatch('ACMQLib.WMQ6Wrapper')
    MQResponseCOM = win32com.client.Dispatch('ACMQLib.MQResponse')
    MQResponseConnectionCOM = win32com.client.Dispatch('ACMQLib.MQResponse')
    MQResponseConnectionCOM = MQMessageCOM.Initialise(MidasParameters.MidasMQHostName, MidasParameters.MidasMQChannel, MidasParameters.MidasMQQueueManager, MidasParameters.MQSecExit)
    
    if MQResponseConnectionCOM.Success:
        errorMsg = str(MQResponseConnectionCOM.ReasonCode) + ' : ' + MQResponseConnectionCOM.ReasonMessage
        acm.Log('Connection to MQ is successful: ' + errorMsg)
        return [MQMessageCOM, MQResponseCOM]
    return None
        
def SendMessage(message, MQMessageCOM, MQResponseCOM):
    
    DBResponseCOM = win32com.client.Dispatch('ACMQDBLib.DBResponse')
    MQDBWriter    = win32com.client.Dispatch('ACMQDBLib.MQDBWriter')
    
    #DBResponse     = MQDBWriter.Initialise('JHDPCM05001V05A\JF1_MAIN1_LIVE', 'FAMidas') # DR
    DBResponse     = MQDBWriter.Initialise('JHBPCM05002V05A\JF1_MAIN1_LIVE', 'FAMidas') # PROD
    #DBResponse    = MQDBWriter.Initialise('JHBPSM05005\JF1_MAIN1_TEST', 'FAMidas')     # UAT
    #DBResponse    = MQDBWriter.Initialise('JHBDSM05001\JF1_MAIN1_DEV', 'FAMidas')      # DEV
    
    msg_buffer = amb.mbf_create_buffer_from_data(message)
    msg        = msg_buffer.mbf_read()
    
    MessageSource = 'FRONT ARENA'
    AmbMsg        = msg.mbf_find_object("TRADE")
    MsgAmb        = AmbMsg.mbf_find_object("LEG")
    key1          = MsgAmb.mbf_find_object("SPI1").mbf_get_value()
    
    findTrdnbr = key1.find('_BTB')
    Type       = ''
    if findTrdnbr != -1:
        key1 = key1[:findTrdnbr]
        Type = 'BTB'
    else:
        key1
        Type = 'Client'
 
    Messagekey1  = key1   
    Messagekey2  = MsgAmb.mbf_find_object("DEALCO").mbf_get_value()
    Messagekey5  = Type
        
    try:
        
        if MQMessageCOM.IsQueueManagerConnected:
            MQResponseCOM = MQMessageCOM.Put(MidasParameters.MidasMQSenderQueue, message)
            if not MQResponseCOM.Success:
                errorMsg = str(MQResponseCOM.ReasonCode) + ' : ' + MQResponseCOM.ReasonMessage
                acm.Log('Failed to put message : ' + errorMsg)
                   
            elif MQResponseCOM.Success:
                acm.Log('Message successfully sent')
                
                if DBResponse.Success:
                    DBResponse = MQDBWriter.WriteMessageLog(MessageSource, Messagekey1, Messagekey2, 'Sent', 'Success', Messagekey5, message) 
                    acm.Log('Message successfully logged into Database:' + DBResponse.ReasonMessage)
                else:
                    acm.Log('Message failed to log into Database: ' + DBResponse.ReasonMessage)    
        else:
            errorMsg = str(MQResponseCOM.ReasonCode) + ' : ' + MQResponseCOM.ReasonMessage
            acm.Log('Connection to MQ is down. Can not send XML: ' + errorMsg)
            
            if DBResponse.Success:
                DBResponse = MQDBWriter.WriteMessageLog(MessageSource, Messagekey1, Messagekey2, 'Not Sent', 'Failed', Messagekey5, message) 
                acm.Log('Connection to MQ is down. Can not send XML')
            else:
                acm.Log('Message failed to log into Database: ' + DBResponse.ReasonMessage)
                
    except Exception, e:
        print 'Error: ', e 

def ProcessTradeXML(XMLMessage, MQMessageCOM, MQResponseCOM):
        
    buffer     = amb.mbf_create_buffer_from_data(XMLMessage)
    MSG        = buffer.mbf_read()
    message    = MSG.mbf_object_to_string_xml()
    
    try:
        if message:
            SendMessage(message, MQMessageCOM, MQResponseCOM)
    except Exception, e:
        print e
     
def xmlMessage(Msg):

    MQConnect = MQConnector()
    
    if MQConnect:
        
        try:
            ProcessTradeXML(Msg, MQConnect[0], MQConnect[1])  
        except Exception, e:
            print e                
  
