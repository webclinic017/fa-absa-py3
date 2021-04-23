'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_RT_MESSAGE_PROCESS
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module processes real time Front Arena AMBA messages and decorates an
                                incoming message object that will be used throughout Front Cache.
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------
'''

'''----------------------------------------------------------------------------------------------------------
Importing Front Cache Utils module for Error Handling
----------------------------------------------------------------------------------------------------------'''
import FC_UTILS as FC_UTILS
from FC_UTILS import FC_UTILS as UTILS

'''----------------------------------------------------------------------------------------------------------
Importing Front Arena and Python modules needed for Real Time ATS Worker.
----------------------------------------------------------------------------------------------------------'''
import traceback
import time
'''----------------------------------------------------------------------------------------------------------
Importing Custom modules modules needed for Real Time ATS Worker.
----------------------------------------------------------------------------------------------------------'''
from AMBA_Helper_Functions import AMBA_Helper_Functions as ambaUtils

'''----------------------------------------------------------------------------------------------------------
Real Time Message Process Class. This class will check if the mandatory fields are present on the incoming AMB
message and create a AMB message object.
----------------------------------------------------------------------------------------------------------'''
class FC_RT_MESSAGE_PROCESS():
    def __init__(self, incomingAMBAMessageData, incomingMessageObject):
        self._incomingAMBAMessage = incomingAMBAMessageData
        self._incomingMessageObject = incomingMessageObject
        self.__mapIncomingAMBAMessageToRequestResponseObject()
        
    def __mapIncomingAMBAMessageToRequestResponseObject(self):
        '''----------------------------------------------------------------------------------------------------------
        Fetch the source attribute on the message
        ----------------------------------------------------------------------------------------------------------'''
        requestSource = ambaUtils.get_AMBA_Object_Value(self._incomingAMBAMessage, UTILS.Constants.fcGenericConstants.SOURCE)
        if not requestSource:
            UTILS.Logger.flogger.warn(UTILS.Constants.fcFloggerConstants.INCOMING_AMBA_MESSAGE_)
        else:
            self._incomingMessageObject.requestSource = str(requestSource)
        
        '''----------------------------------------------------------------------------------------------------------
        Fetch the txnbr attribute on the message
        ----------------------------------------------------------------------------------------------------------'''
        ambaTxNbr = ambaUtils.get_AMBA_Object_Value(self._incomingAMBAMessage, UTILS.Constants.fcGenericConstants.TXNBR)
        if not ambaTxNbr:
            UTILS.Logger.flogger.warn(UTILS.Constants.fcFloggerConstants.COULD_NOT_RETRIEVE_TXNBR)
        else:
            self._incomingMessageObject.ambaTxNbr = int(ambaTxNbr)
            
       
        
        '''----------------------------------------------------------------------------------------------------------
        Fetch the type attribute on the message
        ----------------------------------------------------------------------------------------------------------'''
        ambaMessageType = ambaUtils.get_AMBA_Object_Value(self._incomingAMBAMessage, UTILS.Constants.fcGenericConstants.TYPE)
        if not ambaMessageType:
            UTILS.Logger.flogger.warn(UTILS.Constants.fcFloggerConstants.COULD_NOT_RETRIEVE_THE_TYPE_TAG)
        else:
            self._AMBAMessageType = ambaMessageType

        '''----------------------------------------------------------------------------------------------------------
        Build up the Request Event Type. i.e. REAL_TIME_"AMBA Message Type"
        ----------------------------------------------------------------------------------------------------------'''
        self._incomingMessageObject.requestEventType = UTILS.Constants.fcGenericConstants.REAL_TIME_S %self._AMBAMessageType
        
        '''----------------------------------------------------------------------------------------------------------
        Set the BATCH_ID = 0
        ----------------------------------------------------------------------------------------------------------'''
        self._incomingMessageObject.batchId = 0
        
        '''----------------------------------------------------------------------------------------------------------
        Based on the type of incoming message, the primary key will be fetched and set to the objectId.
        ----------------------------------------------------------------------------------------------------------'''
        objectTag = None
        if self._AMBAMessageType.__contains__(UTILS.Constants.fcGenericConstants.TRADE_UPPER):
            '''----------------------------------------------------------------------------------------------------------
            Set the Request Type for Single Trade
            ----------------------------------------------------------------------------------------------------------'''
            self._incomingMessageObject.requestType = UTILS.Constants.fcGenericConstants.SINGLE_TRADE
            self._incomingMessageObject.topic = '%s_%s' %(self._incomingMessageObject.requestType, self._incomingMessageObject.requestEventType)
            objectTag = self.__setTradeObjectId()
        
            if not objectTag:
                UTILS.Logger.flogger.warn(UTILS.Constants.fcFloggerConstants.NO_TRADE_LIST)
        
        elif self._AMBAMessageType.__contains__(UTILS.Constants.fcGenericConstants.INSTRUMENT_UPPER):
            '''----------------------------------------------------------------------------------------------------------
            Set the Request Type for Instrument Trade
            ----------------------------------------------------------------------------------------------------------'''
            self._incomingMessageObject.requestType = UTILS.Constants.fcGenericConstants.INSTRUMENT_TRADES
            self._incomingMessageObject.topic = '%s_%s' %(self._incomingMessageObject.requestType, self._incomingMessageObject.requestEventType)
            objectTag = self.__setInstrumentObjectId()
        
            if not objectTag:
                UTILS.Logger.flogger.warn(UTILS.Constants.fcFloggerConstants.NO_INSTRUMENT_LIST)
                
        elif self._AMBAMessageType.__contains__(UTILS.Constants.fcGenericConstants.SETTLEMENT_UPPER):
            '''----------------------------------------------------------------------------------------------------------
            Set the Request Type Single Settlement
            ----------------------------------------------------------------------------------------------------------'''
            self._incomingMessageObject.requestType = UTILS.Constants.fcGenericConstants.SINGLE_SETTLEMENT
            self._incomingMessageObject.topic = '%s_%s' %(self._incomingMessageObject.requestType, self._incomingMessageObject.requestEventType)
            objectTag = self.__setSettlementObjectId()
        
            if not objectTag:
                UTILS.Logger.flogger.warn(UTILS.Constants.fcFloggerConstants.NO_SETTLEMENT_LIST)
        '''----------------------------------------------------------------------------------------------------------
        Fetch the Update Time and Update User Id.
        ----------------------------------------------------------------------------------------------------------'''
        self.__setUpdateTimeAndUpdateUser(objectTag)
        
        '''----------------------------------------------------------------------------------------------------------
        Set the Type that will be used on the outgoing AMBA message
        ----------------------------------------------------------------------------------------------------------'''
        self._incomingMessageObject.type = UTILS.Constants.fcGenericConstants.REQUEST_RT
        
        
    '''----------------------------------------------------------------------------------------------------------
    Function to set the objectId based on the specific incoming AMBA Trade message.
    ----------------------------------------------------------------------------------------------------------'''
    def __setTradeObjectId(self):
        tradeTag = ambaUtils.object_by_name(self._incomingAMBAMessage, ['', '!', '+'], UTILS.Constants.fcGenericConstants.TRADE_UPPER)
        
        if not tradeTag:
            UTILS.Logger.flogger.warn(UTILS.Constants.fcFloggerConstants.COULD_NOT_RETRIEVE_TRADE_TAG)
        
        scopeNumber = ambaUtils.get_AMBA_Object_Value(tradeTag, UTILS.Constants.fcGenericConstants.TRDNBR)
        if not scopeNumber:
            UTILS.Logger.flogger.warn(UTILS.Constants.fcFloggerConstants.COULD_NOT_RETRIEVE_THE_TRDBR)
        else:
            self._incomingMessageObject.scopeNumber = int(scopeNumber)
            self._incomingMessageObject.scopeName = str(scopeNumber)
        
        return tradeTag    
    
    '''----------------------------------------------------------------------------------------------------------
    Function to set the objectId based on the specific incoming AMBA Instrument message.
    ----------------------------------------------------------------------------------------------------------'''
    def __setInstrumentObjectId(self):
        instrumentTag = ambaUtils.object_by_name(self._incomingAMBAMessage, ['', '!', '+'], UTILS.Constants.fcGenericConstants.INSTRUMENT_UPPER)
        
        if not instrumentTag:
            UTILS.Logger.flogger.warn(UTILS.Constants.fcFloggerConstants.COULD_NOT_RETRIEVE_INSTRUMENT_TAG)
        
        scopeNumber = ambaUtils.get_AMBA_Object_Value(instrumentTag, UTILS.Constants.fcGenericConstants.INSADDR)
        if not scopeNumber:
            UTILS.Logger.flogger.warn(UTILS.Constants.fcFloggerConstants.COULD_NOT_RETRIEVE_INSADDR_TAG)
        else:
            self._incomingMessageObject.scopeNumber = int(scopeNumber)
        
        scopeName = ambaUtils.get_AMBA_Object_Value(instrumentTag, UTILS.Constants.fcGenericConstants.INSID)
        if not scopeName:
            UTILS.Logger.flogger.warn(UTILS.Constants.fcFloggerConstants.COULD_NOT_RETRIEVE_INSID_TAG)
        else:
            self._incomingMessageObject.scopeName = str(scopeName)
        
        return instrumentTag
    
    '''----------------------------------------------------------------------------------------------------------
    Function to set the objectId based on the specific incoming AMBA Settlement message.
    ----------------------------------------------------------------------------------------------------------'''
    def __setSettlementObjectId(self):
        settlementTag = ambaUtils.object_by_name(self._incomingAMBAMessage, ['', '!', '+'], UTILS.Constants.fcGenericConstants.SETTLEMENT_UPPER)
        
        if not settlementTag:
            UTILS.Logger.flogger.warn(UTILS.Constants.fcFloggerConstants.COULD_NOT_RETRIEVE_THE_STL_TAG)
        
        scopeNumber = ambaUtils.get_AMBA_Object_Value(settlementTag, UTILS.Constants.fcGenericConstants.SEQNBR)
        if not scopeNumber:
            UTILS.Logger.flogger.warn(UTILS.Constants.fcFloggerConstants.COULD_NOT_RETRIEVE_SEQNBR_TAG)
        else:
            self._incomingMessageObject.scopeNumber = int(scopeNumber)
            self._incomingMessageObject.scopeName = str(scopeNumber)
        
        return settlementTag    
    
    '''----------------------------------------------------------------------------------------------------------
    Function to set the Update Time and Update User Id
    ----------------------------------------------------------------------------------------------------------'''
    def __setUpdateTimeAndUpdateUser(self, object):
        requestDateTime = ambaUtils.get_AMBA_Object_Value(object, UTILS.Constants.fcGenericConstants.UPDAT_TIME)
        if not requestDateTime:
            UTILS.Logger.flogger.warn(UTILS.Constants.fcFloggerConstants.COULD_NOT_RETRIEVE_UPDAT_TIME_TAG)
        else:
            self._incomingMessageObject.requestDateTime = FC_UTILS.formatDate(requestDateTime)
            self._incomingMessageObject.reportDate = time.strftime("%Y-%m-%d")
        
        requestUserId = ambaUtils.get_AMBA_Object_Value(object, UTILS.Constants.fcGenericConstants.UPDAT_USRNBR_USERID)
        if not requestUserId:
            UTILS.Logger.flogger.warn(UTILS.Constants.fcFloggerConstants.COULD_NOT_RETRIEVE_UPDAT_TIME_TAG)
        self._incomingMessageObject.requestUserId = requestUserId
        
        '''----------------------------------------------------------------------------------------------------------
        Fetch the backDateStart attribute on the message
        ----------------------------------------------------------------------------------------------------------'''
        backDateStart = ambaUtils.get_AMBA_Object_Value(object, 'BACKDATE_START')
        if not backDateStart:
            UTILS.Logger.flogger.warn('Could not retrieve BACKDATE_START')
        else:
            self._incomingMessageObject.backDateStart = FC_UTILS.formatDate(backDateStart)  
