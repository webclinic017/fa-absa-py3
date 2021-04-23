""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/FACL/ACL/./etc/FACLTradesUpload.py"
import acm
from FACLBatchUploadPerform import FACLBatchUploadPerform

import FBDPGui
import FACLGUIStop
import FACLWebService
import FACLUtils
import FACLArMLMessageBuilder
from FACLMessageRouter import FACLMessageRouter
from FACLObjectGateway import FACLObjectGateway
from FACLArMLMessageFactory import FACLArMLMessageFactory
from FACLFilterQuery import FACLFilterQuery
from FACLParameters import CommonSettings
import FFileUtils

ScriptName = "FACLTradesUpload"

FBDPGui.DefaultVariables.defaults = FBDPGui.Parameters('FBDPParameters', ScriptName)

stopVarName = 'Stop'
ttStop = 'Allow the script to be stopped.'

outputTypeVarName = 'outputType'
ttOutType = 'Output'

outputPathVarName = 'outputPath'
ttOutPath = 'ArML-file output path'

tradeVarName = 'trades'
ttTrade = 'Select the trades to upload'

def default_select_query():
    queryName = CommonSettings.tradeFilterQuery      
    faclFilter = FACLFilterQuery(queryName, None)
    qTrades = faclFilter.Query()
    return qTrades

def output_cb(index, fieldValues):
    enable = fieldValues[index] == 'ArML-File'
    ael_variables.outputPath.enable(enable, ttOutPath)
    return fieldValues
    
qTrades = default_select_query()

ael_variables = FBDPGui.LogVariables(
    [stopVarName,
        'Display a stop button while the script is running',
        'int', [0, 1], 1,
        0, 0, ttStop],
    [outputTypeVarName,
                'Output',
                'string', ['ACL-Service', 'ArML-File'], 'ACL-Service',
                True, 0, ttOutType, output_cb, 1],
    [outputPathVarName,
                'Output file path',
                'string', [], '',
                0, 0, ttOutPath, None, 1],
    [tradeVarName,
        'Trades',
        'FTrade', None, qTrades,
        False, 1, ttTrade, None, None]               
)

def start_uploader(writer, logme, summary, dictionary):
    from FACLAttributeMapper import FACLAttributeMapper
    
    builder = FACLArMLMessageBuilder.FACLArMLMessageBuilder(useMarketPricesVersion=1)
    mapper = FACLAttributeMapper()
    gateway = FACLObjectGateway()
    factory = FACLArMLMessageFactory(builder, mapper)
    uploader = FACLBatchUploadPerform(gateway, factory, writer, logme, summary)

    showStopButton = dictionary[stopVarName] == 1

    if showStopButton:
        with FACLGUIStop.FACLGUIStop() as stopThread:
            uploader.SendObjects(dictionary[tradeVarName])                
    else:
        uploader.SendObjects(dictionary[tradeVarName])

def ael_main(dictionary):
    import FBDPString
    reload(FBDPString)
    import FBDPCommon
    reload(FBDPCommon)
    import FBDPCurrentContext
    import FACLArMLWriter
    from FACLArMLResponse import FACLArMLResponse
    from FACLParameters import PrimeSettings
    
    FBDPCurrentContext.CreateLog(ScriptName,
                      dictionary['Logmode'],
                      dictionary['LogToConsole'],
                      dictionary['LogToFile'],
                      dictionary['Logfile'],
                      dictionary['SendReportByMail'],
                      dictionary['MailList'],
                      dictionary['ReportMessageType'])
    logme = FBDPCurrentContext.Logme()
    summary = FBDPCurrentContext.Summary()

    try:
        logme(None, 'START')
        
        if dictionary[outputTypeVarName] == 'ArML-File':
            filePath = FFileUtils.expandEnvironmentVar(dictionary[outputPathVarName])
            with open( filePath, 'w+' ) as fileObject:
                with FACLArMLWriter.FACLArMLFileWriter( fileObject, logme, summary ) as writer:
                    start_uploader(writer, logme, summary, dictionary)
        elif dictionary[outputTypeVarName] == 'ACL-Service':
            router = FACLMessageRouter(PrimeSettings.senderMBName,
                                       PrimeSettings.senderSource,
                                       PrimeSettings.timeoutForReplyInSeconds,
                                       PrimeSettings.receiverMBName)
                                       
            FACLUtils.ensureConnectedToAMB(PrimeSettings.ambUser, PrimeSettings.ambPassword, PrimeSettings.ambAddress)
            
            writer = FACLArMLWriter.FACLArMLACRWriter(router, FACLArMLResponse, logme, summary)
            start_uploader(writer, logme, summary, dictionary)
        else:
            raise Exception('Output type must be either ACR or ArML-File.')
        

    except Exception as e:
        logme('Error uploading trades {0}.'.format(e), 'ERROR')
        logme(None, 'ABORT')

    logme(None, 'FINISH')
    summary.log(dictionary)
    return summary.buildErrorsAndWarningsStr()