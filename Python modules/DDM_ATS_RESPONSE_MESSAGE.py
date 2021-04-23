'''----------------------------------------------------------------------------------------------------------
MODULE                  :       DDM_ATS_RESPINSE_MESSAGE
PROJECT                 :       (Pegasus) Data Distribution Model - ATS
PURPOSE                 :       This module defines a response message to pass to external Trade Event Listeners
DEPARTMENT AND DESK     :       PCG Change
REQUASTER               :       Pegasus Project
DEVELOPER               :       Heinrich Momberg/Heinrich Cronje
CR NUMBER               :       TBA
-------------------------------------------------------------------------------------------------------------
'''
import zlib 
import base64
import DDM_ATS_HELPER as helper
import DDM_ATS_PARAMS as params
from xml.etree.ElementTree import Element, SubElement, dump, XML, tostring, ElementTree, parse, fromstring
from xml.parsers import expat 

class DDM_ATS_RESPONSE_MESSAGE():
    #local members
    processResult=False
    processMessage=None
    reportOutput=None
    compressedMessage=None
    
    #Compression
    def deflate_and_base64_encode(self, input):
        zlibbed_str = zlib.compress(input)     
        compressed_string = zlibbed_str[2:-4]     
        return base64.b64encode(compressed_string)  
        
        
    #********************************************************************************************************
    # Class Constructor
    #******************************************************************************************************** 
    def __init__(self, atsName, requestMessage, processResult, processMessage, reportOutput):
        try:
            
            self.processResult=processResult
            self.processMessage=processMessage
            self.reportOutput=reportOutput
            
            if processResult==True and not reportOutput:
                raise Exception('The report output is empty')
            
            #Construct the message content
            messageTag = Element('MESSAGE')
            
             #Add the message and event id's that was originally passed in
            helper.AddXmlChildElement(messageTag, 'ATS_NAME', atsName)
            helper.AddXmlChildElement(messageTag, 'SOURCE_SYSTEM', params.sourceSystem)
            helper.AddXmlChildElement(messageTag, 'SOURCE', requestMessage.source)
            helper.AddXmlChildElement(messageTag, 'EVENT_DATE_TIME', requestMessage.eventDateTime)
            helper.AddXmlChildElement(messageTag, 'REPORT_DATE', requestMessage.reportDate)
            helper.AddXmlChildElement(messageTag, 'IS_REQUEST', str(requestMessage.isRequest))
            helper.AddXmlChildElement(messageTag, 'REQUEST_BATCH_NAME', requestMessage.requestBatchName)
            helper.AddXmlChildElement(messageTag, 'REQUEST_BATCH_NUMBER', requestMessage.requestBatchNumber)
            helper.AddXmlChildElement(messageTag, 'IS_EOD_REQUEST', str(requestMessage.isEODRequest))
            helper.AddXmlChildElement(messageTag, 'REQUEST_SCOPE_NUMBER', str(requestMessage.requestScopeNumber))
            helper.AddXmlChildElement(messageTag, 'REQUEST_SCOPE_NAME', str(requestMessage.requestScopeName))
            helper.AddXmlChildElement(messageTag, 'REQUEST_TYPE', str(requestMessage.requestType,))
            helper.AddXmlChildElement(messageTag, 'REQUEST_LOG_ID', str(requestMessage.requestLogId))
            helper.AddXmlChildElement(messageTag, 'TRADE_BATCH_ID', str(requestMessage.tradeBatchId))
            helper.AddXmlChildElement(messageTag, 'TRADE_BATCH_NO', str(requestMessage.tradeBatchNo))
            helper.AddXmlChildElement(messageTag, 'TRADE_BATCH_TOTAL', str(requestMessage.tradeBatchTotal))
            helper.AddXmlChildElement(messageTag, 'INTRADAY_EVENT_ID', str(requestMessage.intradayEventId))
            helper.AddXmlChildElement(messageTag, 'TRADE_COUNT', str(len(requestMessage.tradeNumberList)))
            
            #Add the process result
            helper.AddXmlChildElement(messageTag, 'PROCESS_RESULT', str(processResult))
            helper.AddXmlChildElement(messageTag, 'PROCESS_MESSAGE', str(processMessage))
                
            #Add the report output
            reportOutputTag = fromstring(reportOutput)
            messageTag.append(reportOutputTag)
            
            #Set the compressed message
            try:
                self.compressedMessage = self.deflate_and_base64_encode(tostring(messageTag))
            except Exception, e:
                raise Exception('Message compression failed. %s' % str(e))
        except Exception, e:
            raise Exception('Could not create the response message. %s' % str(e))
