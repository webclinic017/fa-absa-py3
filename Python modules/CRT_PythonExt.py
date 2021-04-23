import CRT_ManualFeed
import subprocess
import acm
import ael
import os
import tempfile

today = acm.Time().DateNow()
linqBinPath = r"Y:\Jhb\CRT\Projects\Inflation Onboarding 2013\LinqBinaries"

ael_variables = [
        ['DrctValue', 'Drop path', 'string', None, r'C:\temp\dump', 1],
        ['TrdFilter', 'Trade Filter', 'string', CRT_ManualFeed.TrdFilter(), 'CRT-Inflation-ResultSet', 1],
        ['TradeNumber', 'Trade Number(s)', 'string', None, None, 0, 0, 'To run for a specific trade, enter the trade number here.', None, 1],
        ['CopyToClipboard', 'Copy Result to Clipboard', 'bool', [True, False], False, 0, 0, 'Copy the resultant XML to the clipboard', None, 1]
    ]

presetTradeVars = {
                    'ReportName'        : 'CRT_Extract',
                    'XsltExtract'       : 'FCRTTradeExtract',
                    'Templates'         : 'CRT_Trade',
                    'Date'              : today
                }

presetCashVars = {
                    'ReportName'        : 'CRT_Extract',
                    'XsltExtract'       : 'FCRTCashExtract',

                    'Templates'         : 'CRT_Cash',
                    'Date'              : today
                }

def ael_main(parameters):
    outputDir = parameters["DrctValue"]

    #extract trades
    tradeFile = tempfile.NamedTemporaryFile(prefix='FA-CRT-TradeExtract-')
    extraTradeParams = {'FileExtract' : os.path.basename(tradeFile.name)}
    tradeParams = dict(presetTradeVars.items() + parameters.items() + extraTradeParams.items())
    CRT_ManualFeed.ExtractTrades(tradeParams)
    
    #extract cash
    cashFile = tempfile.NamedTemporaryFile(prefix='FA-CRT-CashExtract-')
    extraCashParams = {'FileExtract' : os.path.basename(cashFile.name)}
    cashParams = dict(presetCashVars.items() + parameters.items() + extraCashParams.items())
    CRT_ManualFeed.ExtractTrades(cashParams)

    #create merged intermediary xml
    intermediateFile = tempfile.NamedTemporaryFile(prefix='FA-CRT-IntermediateyExtract-', suffix='.xml', delete=False)
    procParams = [      os.path.join(linqBinPath, "XMLLoaderWithLINQServices.exe"),
                        '-d' + outputDir,
                        "-p" + extraTradeParams["FileExtract"],
                        "-c" + extraCashParams["FileExtract"],
                        '-m' + os.path.join(linqBinPath, 'XMLFileMapper.xml'),
                        '-r' + os.path.join(outputDir, os.path.basename(intermediateFile.name)),
                        '-l' + os.path.join(outputDir, 'ExtractLog.log')      ]
    subprocess.call(procParams)
    
    #if parameters['CopyToClipboard']:

    tradeFile.close()
    cashFile.close()
    intermediateFile.close()
