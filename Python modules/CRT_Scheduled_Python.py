import clr, os, sys, tempfile
from datetime import datetime

import acm, ael
import xml.dom.minidom as xml
import FOperationsUtils as Utils

import CRT_ManualFeed

today = datetime.now()
environment = None

configuration = acm.GetDefaultValueFromName(acm.GetDefaultContext(), acm.FObject, 'CRT_Inflation_Seahawk_Configuration')
config = xml.parseString(configuration)
crtBinaryPath = ''
crtOutputPath = ''
crtTradeFilter = ''

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
except:
    Utils.Log(True, 'ERROR: Could not find environment settings for %s.' % arenaDataServer)
    raise Exception('ERROR: Could not find environment settings for %s.' % arenaDataServer)
    
ael_variables = \
    [
        ['TrdFilter', 'Trade Filter', 'string', CRT_ManualFeed.TrdFilter(), str(crtTradeFilter), 0],
        ['TradeNumber', 'Trade Number(s)', 'string', None, None, 0, 0, 'To run for a specific trade, enter the trade number here.', None, 1],
        ['OutputDir', 'Output Directory', 'string', None, str(crtOutputPath), 1],
        ['linq_bin_path', 'Source Binaries', 'string', None, str(crtBinaryPath), 1, None, None, None, 1]
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

def ael_main(parameters):

    linq_bin_path = parameters['linq_bin_path']

    if linq_bin_path not in sys.path:
        sys.path.append(linq_bin_path)

    clr.AddReference('CRT.XMLLoaderWithLINQServices')    
    import CRT.XMLLoaderWithLINQServices as xlls

    today = datetime.now()
    outputDir = parameters["OutputDir"]
    tradeFileName = os.path.join(outputDir, 'FATrades.DetailExtract.{0}.xml'.format(today.strftime("%Y-%m-%d")))
    cashFileName = os.path.join(outputDir, 'FACash.DetailExtract.{0}.xml'.format(today.strftime("%Y-%m-%d")))
    print tradeFileName
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
    
    rg = xlls.ReportGenerator()
    rg.MapperFile = os.path.join(str(linq_bin_path), 'XMLFileMapper.xml')
    rg.SeahawkOutputDirectory = outputDir
    rg.SiteId = "10250696"
    rg.Product = 'SWAP'
    rg.ProductSubType = 'IRSWAP'
    rg.TradeFile = tradeFileName
    rg.CashFile = cashFileName
    print "Generating Seahawk report..."
    result_file = rg.GenerateSeahawkReport()
    print "Report written to", result_file
    print "Completed successfully."
