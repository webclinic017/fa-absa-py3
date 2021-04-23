'''----------------------------------------------------------------------------------------------------------
MODULE                  :       CRT_SeahawkFileExtract
PROJECT                 :       CRT Inflation Swaps from Front Arena to Seahawk
PURPOSE                 :       This module serves the purpose of extract the raw Trade and Cash XML for Inflation Swaps from Front Arena to be consumed 
                                by the Seahawk binary conversion application on the MMG space
DEPARTMENT AND DESK     :       CRT - Counterparty Risk Trading
REQUASTER               :       Declercq Wentzel
DEVELOPER               :       Arthur Grace
CR NUMBER               :       CHNG0001674016
-------------------------------------------------------------------------------------------------------------

HISTORY
=============================================================================================================
Date            Change no       Developer                       Description
-------------------------------------------------------------------------------------------------------------
2014-03-20      CHNG0001674016  Arthur Grace                    Initial Implementation

-------------------------------------------------------------------------------------------------------------

DESCRIPTION OF MODULE:

    This module reads the CRTInflationTrade and CRTInflationCash Workbooks and produces the raw XML for Trade and Cash Inflation Swaps.
    The files are placed on a directory specified in the configuration settings. These files will then be consumed by the CRT Inflation MMG component
'''

import os, sys
from datetime import datetime

import acm, ael
import xml.dom.minidom as xml
import FOperationsUtils as Utils

import CRT_ManualFeed

today = datetime.now()
environment = None

try:
    configuration = acm.GetDefaultValueFromName(acm.GetDefaultContext(), acm.FObject, 'CRT_Inflation_Seahawk_Configuration')
except:
    Utils.Log(True, 'ERROR: Could not find environment settings for %s.' % arenaDataServer)
    raise Exception('ERROR: Could not find environment settings for %s.' % arenaDataServer)
    
config = xml.parseString(configuration)

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
    crtOutputPath = element.getElementsByTagName('OutputPath')[0].firstChild.data
    crtTradeFilter = element.getElementsByTagName('TradeFilter')[0].firstChild.data
except:
    Utils.Log(True, 'ERROR: Could not find environment settings for %s.' % arenaDataServer)
    raise Exception('ERROR: Could not find environment settings for %s.' % arenaDataServer)
    
ael_variables = \
    [
        ['TrdFilter', 'Trade Filter', 'string', CRT_ManualFeed.TrdFilter(), str(crtTradeFilter), 0],
        ['TradeNumber', 'Trade Number(s)', 'string', None, None, 0, 0, 'To run for a specific trade, enter the trade number here.', None, 1],
        ['OutputDir', 'Output Directory', 'string', None, str(crtOutputPath), 1]
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
    today = datetime.now()
    outputDir = parameters["OutputDir"]
    tradeFileName = os.path.join(outputDir, 'FATrades.DetailExtract.xml')
    cashFileName = os.path.join(outputDir, 'FACash.DetailExtract.xml')
    print tradeFileName
    #extract trades
    print "Extracting Trade details..."
    extraTradeParams = {'FileExtract' : tradeFileName}
    tradeParams = dict(presetTradeVars.items() + parameters.items() + extraTradeParams.items())
    try:
        CRT_ManualFeed.ExtractTrades(tradeParams)
    except:
        Utils.Log(True, 'ERROR: Could not find environment settings for %s.' % arenaDataServer)
        raise Exception('ERROR: Could not find environment settings for %s.' % arenaDataServer)
    
    #extract cash
    print cashFileName
    print "\nExtracting Cash details..."
    extraCashParams = {'FileExtract' : cashFileName}
    cashParams = dict(presetCashVars.items() + parameters.items() + extraCashParams.items())
    try:
        CRT_ManualFeed.ExtractTrades(cashParams)
    except:
        Utils.Log(True, 'ERROR: Could not find environment settings for %s.' % arenaDataServer)
        raise Exception('ERROR: Could not find environment settings for %s.' % arenaDataServer)
    

