import clr, codecs, os, sys, tempfile
from datetime import datetime

import acm, ael
import xml.dom.minidom as xml

import CRT_ManualFeed

today = datetime.now()

environment = None

configuration = acm.GetDefaultValueFromName(acm.GetDefaultContext(), acm.FObject, 'CRT_Inflation_Seahawk_Configuration')
config = xml.parseString(configuration)
crtBinaryPath = ''
crtOutputPath = ''
crtTradeFilter = ''
crtTransforms = ''

arenaDataServer = acm.FDhDatabase['ADM'].ADSNameAndPort().lower()
environmentSettings = acm.GetDefaultValueFromName(acm.GetDefaultContext(), acm.FObject, 'EnvironmentSettings')
environmentSetting = xml.parseString(environmentSettings)

host = environmentSetting.getElementsByTagName('Host')
environment = [e for e in host if e.getAttribute('Name').lower() == arenaDataServer]

if len(environment) != 1:
    Utils.Log(True, 'ERROR: Could not find environment settings for %s.' % arenaDataServer)
    raise Exception('ERROR: Could not find environment settings for %s.' % arenaDataServer)

envSetting = str(environment[0].getAttribute('Setting'))

for element in config.getElementsByTagName('Environment'):
    if element.getAttribute('ArenaDataServer').find(envSetting) >= 0:
        environment = element
        break
else:   
    Utils.Log(True, 'ERROR: Could not find configuration settings for %s.' % arenaDataServer)
    raise Exception('ERROR: Could not find configuration settings for %s.' % arenaDataServer)

try:
    crtBinaryPath = element.getElementsByTagName('BinaryPath')[0].firstChild.data
    crtOutputPath = element.getElementsByTagName('OutputPath')[0].firstChild.data
    crtTradeFilter = element.getElementsByTagName('TradeFilter')[0].firstChild.data
    crtTransforms = element.getElementsByTagName('Transforms')[0].firstChild.data
except:
    Utils.Log(True, 'ERROR: Could not find environment settings for %s.' % arenaDataServer)
    raise Exception('ERROR: Could not find environment settings for %s.' % arenaDataServer)

ael_variables = \
    [
        ['TrdFilter', 'Trade Filter', 'string', CRT_ManualFeed.TrdFilter(), str(crtTradeFilter), 1],
        ['TradeNumber', 'Trade Number(s)', 'string', None, None, 0, 0, 'To run for a specific trade, enter the trade number here.', None, 1],
        ['OutputDir', 'Output Directory', 'string', None, str(crtOutputPath), 1],
        ['crt_bin_path', 'Source Binaries', 'string', None, str(crtBinaryPath), 1, None, None, None, 0],
        ['PostProcessXslt', 'Post Process Transform', 'string', None, str(crtTransforms), 1, None, None, None, 0],
        ['CopyToClipboard', 'Copy Result to Clipboard', 'bool', [True, False], False, 0, 0, 'Copy the resultant XML to the clipboard', None, 1]
    ]


    
presetTradeVars =   {
                        'ReportName'        : 'CRT_Extract',
                        'XsltExtract'       : 'FCRTTradeExtract',
                        'Templates'         : 'CRT_Trade',
                        'Date'              : today.strftime("%Y-%m-%d")
                    }

presetCashVars =    {
                        'ReportName'        : 'CRT_Extract',
                        'XsltExtract'       : 'FCRTCashExtract',
                        'Templates'         : 'CRT_Cash',
                        'Date'              : today.strftime("%Y-%m-%d")
                    }

def CreateTemporaryFileName(filePrefix, fileSuffix = '.xml'):
    tmpFile = tempfile.NamedTemporaryFile(prefix=filePrefix, suffix=fileSuffix)
    try:
        fileName = tmpFile.name
    finally:
        tmpFile.close()
    return fileName

def copy_to_clipboard(filename):
    from FClipboardUtilities import SetClipboardText
    
    with codecs.open(filename, 'r', 'utf-8-sig') as f:
        SetClipboardText(f.read())

def ael_main(parameters):
    crt_bin_path = parameters["crt_bin_path"]

    if crt_bin_path not in sys.path:
        sys.path.append(crt_bin_path)
    
    clr.AddReference('CRT.TradeExtractTransform')
    import CRT.TradeExtractTransform as crt

    today = datetime.now()
    
    outputDir = parameters["OutputDir"]
    postProcXsltPath = parameters["PostProcessXslt"]
    copyToClipboard = parameters["CopyToClipboard"]

    tradeFileName = CreateTemporaryFileName('FATrades.DetailExtract.')
    cashFileName = CreateTemporaryFileName('FACash.DetailExtract.')

    #extract trades
    print "Extracting Trade details..."
    extraTradeParams = {'FileExtract' : tradeFileName}
    tradeParams = dict(presetTradeVars.items() + parameters.items() + extraTradeParams.items())
    CRT_ManualFeed.ExtractTrades(tradeParams)
    
    #extract cash
    print "\nExtracting Cash details..."
    extraCashParams = {'FileExtract' : cashFileName}
    cashParams = dict(presetCashVars.items() + parameters.items() + extraCashParams.items())
    CRT_ManualFeed.ExtractTrades(cashParams)

    #create trade+cash xml and CRT xml
    timeStr = today.strftime("%Y%m%dT%H%M")
    xmlFileName = "{0}.{1}.FATrades.xml".format(os.environ.get("USERNAME"), timeStr)
    crtFileName = "{0}.{1}.CRTTrades.xml".format(os.environ.get("USERNAME"), timeStr)
    crtFilePath = os.path.join(outputDir, crtFileName)
    logFileName = "{0}.{1}.ExtractLog.log".format(os.environ.get("USERNAME"), timeStr)
    
    configInput = crt.CRTConfigInput()
    configInput.MapperFileName = os.path.join(crt_bin_path, 'XMLFileMapper.xml')
    configInput.XsltFileName = postProcXsltPath
    configInput.LogFileName = os.path.join(outputDir, logFileName)
    
    transformInput = crt.CRTTransformInput()
    transformInput.TradeFileNames = extraTradeParams["FileExtract"].split(',')
    print "TradeFileNames", extraTradeParams["FileExtract"].split(',')
    transformInput.CashFileNames = extraCashParams["FileExtract"].split(',')
    print "CashFileNames", extraCashParams["FileExtract"].split(',')
    transformInput.MergedFileNames = os.path.join(outputDir, xmlFileName).split(',')
    print "MergedFileNames", os.path.join(outputDir, xmlFileName).split(',')
    transformInput.OutputFileNames = crtFilePath.split(',')
    print "OutputFileNames", crtFilePath.split(',')
    print 'Config output', configInput
        
    transform = crt.TradeTransformer(configInput)
    transform.Transform(transformInput)
    
    print "Produced CRT output file:\n{0}\n".format(crtFilePath)
    if copyToClipboard:
        copy_to_clipboard(crtFilePath)
        print "File content has been copied to clipboard and can be imported into DTRE using the copy from clipboard functionality."
