""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/FACL/ACL/./etc/FACLFXRatesUpload.py"
import acm
from FACLFXRatesUploadPerform import FACLFXRatesUploadPerform
import FBDPGui
import FACLGUIStop
from FACLMessageRouter import FACLMessageRouter
import FACLArMLMessageBuilder
from FACLArMLResponse import FACLArMLResponse
import FACLUtils
import FFileUtils

ScriptName = "FACLFXRatesUpload"

FBDPGui.DefaultVariables.defaults = FBDPGui.Parameters('FBDPParameters', ScriptName)

stopVarName = 'Stop'
ttStop = "Allow the script to be stopped."

useMarkToMarketRateVarName = "useMtM"
ttUseMarkToMarketRate= 'Use the mark-to-market rate instead of the used rate'

outputTypeVarName = 'outputType'
ttOutType = 'Output'

outputPathVarName = 'outputPath'
ttOutPath = 'ArML-file output path'

baseCurrencyVarName = 'baseCurrency'
ttBaseCurrencyName = 'This must be the same as the ACL System Parameter SYS_BASE_CODE’'

currenciesVarName = 'currencies'
ttCurrencies = 'Currencies to upload rates for'

def default_select_query():
    qCurrencies = acm.CreateFASQLQuery(acm.FCurrency, 'AND')
    op = qCurrencies.AddOpNode('AND')
    op.AddAttrNode('Name', 'RE_LIKE_NOCASE', None)
    qCurrencies.IsReadOnlyProperty(True)
    return qCurrencies

def output_cb(index, fieldValues):
    enable = fieldValues[index] == 'ArML-File'
    ael_variables.outputPath.enable(enable, ttOutPath)
    return fieldValues

qCurrencies = default_select_query()

ael_variables = FBDPGui.LogVariables(
    # [VariableName,
    #       DisplayName,
    #       Type, CandidateValues, Default,
    #       Mandatory, Multiple, Description, InputHook, Enabled]
    [stopVarName,
        'Display a stop button while the script is running',
        'int', [0,1], 1,
        False, False, ttStop, None, True],
    [useMarkToMarketRateVarName,
        'Use the mark-to-market rate',
        'int', [0,1], 1,
        False, False, ttUseMarkToMarketRate, None, True],
    [outputTypeVarName,
                'Output',
                'string', ['ACL-Service', 'ArML-File'], 'ACL-Service',
                True, 0, ttOutType, output_cb, 1],
    [outputPathVarName,
                'Output file path',
                'string', [], '',
                0, 0, ttOutPath, None, 1],
    [baseCurrencyVarName,
        'Base currency',
        'string', acm.FCurrency.Instances(), '',
        True, False, ttBaseCurrencyName],
    [currenciesVarName,
        'Currencies',
        'FCurrency', None, qCurrencies,
        True, True, ttCurrencies, None, True]

)

def start_uploader(writer, logme, summary, dictionary):
    from FACLAttributeMapper import FACLAttributeMapper
    
    builder = FACLArMLMessageBuilder.FACLArMLMessageBuilder(useMarketPricesVersion=1)
    uploader = FACLFXRatesUploadPerform(writer, builder, logme, summary)

    showStopButton = dictionary[stopVarName] == 1
    useMtM = dictionary[useMarkToMarketRateVarName]
    baseCurrency = dictionary[baseCurrencyVarName]
    currencies = dictionary[currenciesVarName]

    if showStopButton:
        with FACLGUIStop.FACLGUIStop() as stopThread:
            uploader.SendCurrencies(useMtM, baseCurrency, currencies)
    else:
        uploader.SendCurrencies(useMtM, baseCurrency, currencies)

def ael_main(dictionary):
    import time
    import FBDPString
    reload(FBDPString)
    import FBDPCommon
    reload(FBDPCommon)
    import FBDPCurrentContext
    import FACLArMLWriter
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

    from FACLParameters import PrimeSettings

    try:
        logme(None, 'START')
        baseCurrency = dictionary[baseCurrencyVarName]
        if baseCurrency is None:
            raise Exception('The base currency must be set to something.')
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

    except KeyboardInterrupt:
        logme('FX rates upload stoped by user', 'INFO')
    except Exception,e:
        logme('Error uploading currencies {0}.'.format(e), 'ERROR')
        logme(None, 'ABORT')
    
    logme(None, 'FINISH')
    summary.log(dictionary)
