'''-----------------------------------------------------------------------------
PROJECT                 :  Markets Message Gateway
PURPOSE                 :  Places messages on AMB
DEPATMENT AND DESK      :  
REQUESTER               :  
DEVELOPER               :  Francois Truter
CR NUMBER               :  XXXXXX
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no Developer                 Description
--------------------------------------------------------------------------------
2011-03-25 XXXXXX    Francois Truter           Initial Implementation
'''

import amb
import time
import acm

class SwiftMtAmbaMessageConstants:
    NewSwiftMtAmbaMessage = 'NEW_SWIFT_MT'
    SwiftMtList = 'SWIFT_MT'
    TypeTag = 'SWIFT_MT_TYPE'
    ContentTag = 'CONTENT'
    StatementList = 'STATEMENT'
    OidTag = 'OID'
    NumberTag = 'NUMBER'
    DateTag = 'DATE'

def event_cb(channel, event_p, *arg_p):
    pass
    
def _isInt(object):
    try:
        int(object)
    except:
        return False
    else:
        return True

class AmbHelper:

    @staticmethod
    def _addStatement(messageList, statementOid, statementNumber, statementDate):
        if  _isInt(statementOid) and _isInt(statementNumber) and acm.Time().IsValidDateTime(statementDate):
            statementList = messageList.mbf_start_list(SwiftMtAmbaMessageConstants.StatementList)
            statementList.mbf_add_int(SwiftMtAmbaMessageConstants.OidTag, int(statementOid))
            statementList.mbf_add_int(SwiftMtAmbaMessageConstants.NumberTag, int(statementNumber))
            statementList.mbf_add_string(SwiftMtAmbaMessageConstants.DateTag, statementDate)
            statementList.mbf_end_list()

    @staticmethod
    def _createSwiftMtAmbaMessage(source, mtType, content, statementOid, statementNumber, statementDate):
        message = amb.mbf_start_message(None, SwiftMtAmbaMessageConstants.NewSwiftMtAmbaMessage, '1.0', None, source)
        swiftMtList = message.mbf_start_list(SwiftMtAmbaMessageConstants.SwiftMtList)
        swiftMtList.mbf_add_string(SwiftMtAmbaMessageConstants.TypeTag, mtType)
        swiftMtList.mbf_add_string(SwiftMtAmbaMessageConstants.ContentTag, content)
        if statementOid and statementNumber and statementDate:
            AmbHelper._addStatement(swiftMtList, statementOid, statementNumber, statementDate)
        swiftMtList.mbf_end_list()
        message.mbf_end_message()
        return message

    @staticmethod
    def CreateSwiftMtAmbaMessage(source, mtType, content) :
        return AmbHelper._createSwiftMtAmbaMessage(source, mtType, content, None, None, None)
        
    @staticmethod
    def CreateSwiftMtAmbaMessageWithStatement(source, mtType, content, statementOid, statementNumber, statementDate):
        return AmbHelper._createSwiftMtAmbaMessage(source, mtType, content, statementOid, statementNumber, statementDate)
    
    @staticmethod
    def WriteToQueue(config, message, subject):
        amb.mb_init(config.InitString)
        channel = amb.mb_queue_init_writer(config.SenderName, event_cb, config.SenderSource)
        subject = '%s/%s' % (config.SenderSource, subject)
        
        buffer = amb.mbf_create_buffer()
        message.mbf_generate(buffer)
        data = buffer.mbf_get_buffer_data()
        dataSize = buffer.mbf_get_buffer_data_size()
        
        error = amb.mb_queue_write(channel, subject, data, dataSize, time.strftime("%Y-%m-%d %H:%M:%S"))
        if error:
            raise Exception('An error [code: %(error)s] occurred while writing the following message to Host [%(host)s] Port [%(port)s]:\n%(message)s' % 
                {'error': error, 'host': config.Host, 'port': config.Port, 'message': message.mbf_object_to_string()})        

    @staticmethod
    def WriteSwiftMtMessageToQueue(config, mtType, content):
        ambaMessage = AmbHelper.CreateSwiftMtAmbaMessage(config.SenderSource, mtType, content)
        AmbHelper.WriteToQueue(config, ambaMessage, SwiftMtAmbaMessageConstants.SwiftMtList)

    @staticmethod
    def WriteSwiftMtMessageWithStatementToQueue(config, mtType, content, statementOid, statementNumber, statementDate):
        ambaMessage = AmbHelper.CreateSwiftMtAmbaMessageWithStatement(config.SenderSource, mtType, content, statementOid, statementNumber, statementDate)
        AmbHelper.WriteToQueue(config, ambaMessage, SwiftMtAmbaMessageConstants.SwiftMtList)
