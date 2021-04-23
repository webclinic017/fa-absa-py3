'''----------------------------------------------------------------------------------------------------------
MODULE                  :       DDM_REQUEST_MESSAGE
PROJECT                 :       (Pegasus) Data Distribution Model - ATS
PURPOSE                 :       This module defines a request message for report generation 
                                
DEPARTMENT AND DESK     :       PCG Change
REQUASTER               :       Pegasus Project
DEVELOPER               :       Heinrich Momberg/Heinrich Cronje
CR NUMBER               :       TBA
-------------------------------------------------------------------------------------------------------------
'''
from AMBA_Helper_Functions import AMBA_Helper_Functions as ambaUtils

class DDM_REQUEST_MESSAGE():


    #local members
    requestId=0
    requestDateTime=None
    reportDate=None
    requestSource=None
    batchNumber=0
    batchName=None
    requestEventType=None
    requestType=None
    scopeNumber=0
    scopeName=None
    requestBatchCount=0
    requestBatchNo=0
    requestBatchStartIndex=0
    requestBatchEndIndex=0
    requestBatchTradeCount=0
    
    #********************************************************************************************************
    # Class Constructor
    #******************************************************************************************************** 
    def __init__(self, msg):
        try:
            #Fetch the source attribute on the message
            self.source = ambaUtils.get_AMBA_Object_Value(msg, 'SOURCE')
            if not self.source:
                raise Exception('SOURCE tag not found')
                
            #Fetch the messagae data tag
            dataTag = ambaUtils.object_by_name(msg, [''], 'DATA')
            if not dataTag:
                raise Exception('Data tag not found')
            
            #requestId
            self.requestId = ambaUtils.get_AMBA_Object_Value(dataTag, 'REQUEST_ID').strip()
            if not self.requestId:
                raise Exception('REQUEST_ID tag not found')
                
            #requestDateTime
            self.requestDateTime = ambaUtils.get_AMBA_Object_Value(dataTag, 'REQUEST_DATETIME').strip()
            if not self.requestDateTime:
                raise Exception('REQUEST_DATETIME tag not found')
            
            #reportDate
            self.reportDate = ambaUtils.get_AMBA_Object_Value(dataTag, 'REPORT_DATE').strip()
            if not self.reportDate:
                raise Exception('REPORT_DATE tag not found')
            
            #requestSource
            self.requestSource = ambaUtils.get_AMBA_Object_Value(dataTag, 'REQUEST_SOURCE').strip()
            if not self.requestSource:
                raise Exception('REQUEST_SOURCE tag not found')
            
            #batchNumber
            self.batchNumber = ambaUtils.get_AMBA_Object_Value(dataTag, 'BATCH_NUMBER').strip()
            if not self.batchNumber:
                raise Exception('BATCH_NUMBER tag not found')
                
            #batchName
            self.batchName = ambaUtils.get_AMBA_Object_Value(dataTag, 'BATCH_NAME').strip()
            if not self.batchName:
                raise Exception('BATCH_NAME tag not found')
            
                        
            #requestEventType
            self.requestEventType = ambaUtils.get_AMBA_Object_Value(dataTag, 'REQUEST_EVENT_TYPE').strip()
            if not self.requestEventType:
                raise Exception('REQUEST_EVENT_TYPE tag not found')
           
            #requestType
            self.requestType = ambaUtils.get_AMBA_Object_Value(dataTag, 'REQUEST_TYPE').strip()
            if not self.requestType:
                raise Exception('REQUEST_TYPE tag not found')
                
            #scopeNumber
            self.scopeNumber = ambaUtils.get_AMBA_Object_Value(dataTag, 'SCOPE_NUMBER').strip()
            if not self.scopeNumber:
                self.scopeNumber=0
                
                
            #scopeName
            self.scopeName = ambaUtils.get_AMBA_Object_Value(dataTag, 'SCOPE_NAME').strip()
            if not self.scopeName:
                self.scopeName=''
                
            #Fetch the request batch tag if any
            requestBatchTag = ambaUtils.object_by_name(msg, [''], 'REQUEST_BATCH')
            if requestBatchTag:
                
                #requestBatchCount
                self.requestBatchCount = ambaUtils.get_AMBA_Object_Value(requestBatchTag, 'REQUEST_BATCH_COUNT')
                if not self.requestBatchCount:
                    self.requestBatchCount=0
                    
                #requestBatchNo
                self.requestBatchNo = ambaUtils.get_AMBA_Object_Value(requestBatchTag, 'REQUEST_BATCH_NO')
                if not self.requestBatchNo:
                    self.requestBatchNo=0
                
                #requestBatchStartIndex
                self.requestBatchStartIndex = ambaUtils.get_AMBA_Object_Value(requestBatchTag, 'REQUEST_BATCH_START_INDEX')
                if not self.requestBatchStartIndex:
                    self.requestBatchStartIndex=0
                    
                    
                #requestBatchEndIndex
                self.requestBatchEndIndex = ambaUtils.get_AMBA_Object_Value(requestBatchTag, 'REQUEST_BATCH_END_INDEX')
                if not self.requestBatchEndIndex:
                    self.requestBatchEndIndex=0
                    
                #requestBatchTradeCount
                self.requestBatchTradeCount = ambaUtils.get_AMBA_Object_Value(requestBatchTag, 'REQUEST_BATCH_TRADE_COUNT')
                if not self.requestBatchTradeCount:
                    self.requestBatchTradeCount=0
                        
            
        except Exception, e:
            raise Exception('Could not create the request message. %s' % str(e))
