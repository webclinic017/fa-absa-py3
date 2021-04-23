""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/fx_position_rolls/etc/FxTradeGenerator.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FxTradeGenerator - Automatically generate FX trades
    
DESCRIPTION

ENDDESCRIPTION
"""

# Import builtin modules

import sys
import os
import string
import random
import time
import math
import traceback
try:
        import re
        reload(re)
except:
        print "Unexpected error:", sys.exc_info()[0]
import getopt
print dir(re)

# Import Front modules

import ael
import acm
import ArenaFunctionBridge
reload(ArenaFunctionBridge)
import FBDPInstrument
reload(FBDPInstrument)
import FBDPGui
reload(FBDPGui)
from FBDPCommon import *
import FBDPString

global logme
logme = FBDPString.logme
ScriptName = 'FxSpotRollover'
Logfile = ScriptName + '.log'

# Try to set parameters from GUI.
try:
    import FBDPParameters
    reload(FBDPParameters)
    TestMode = FBDPParameters.TestMode
    Date = FBDPParameters.Date
    LogMode = FBDPParameters.LogMode
    LogToConsole = FBDPParameters.LogToConsole
    LogToFile = FBDPParameters.LogToFile
# If that doesn't work, set default parameters.
except:
    TestMode = 1
    Date = "Today"
    LogMode = 1
    LogToConsole = 1
    LogToFile = 0

#==================================================================
# GLOBALS
#==================================================================

# reason_descr: Used in reporting etc.
reason_descr={0:'FX Spot Rollover'}

# report_descr: the different list describes if instrument have been deleted/archive, skipped or where delete failed.
# In the list of skipped instruments each element is a tuple (insid,reason_flag).
# keys: the value of instrument_handling, SKIP and Failed.

report_descr={}

rep_filename=None
dat_filename=None
summary={}
instrument_handling='Keep'

def accountingParametersQuery():
    q = CreateFASQLQuery(FAccountingParameters, 'AND')
    op = q.AddOpNode('OR')
    op.AddAttrNode('Name', 'RE_LIKE_NOCASE', None)
    return q

def currencyPairsQuery():
    q = CreateFASQLQuery(FCurrencyPair, 'AND')
    op = q.AddOpNode('OR')
    op.AddAttrNode('Name', 'RE_LIKE_NOCASE', None)
    return q

def portfoliosQuery():
    q = CreateFASQLQuery(FPhysicalPortfolio, 'AND')
    op = q.AddOpNode('OR')
    op.AddAttrNode('Name', 'RE_LIKE_NOCASE', None)
    return q

def partiesQuery():
    q = CreateFASQLQuery(FParty, 'AND')
    op = q.AddOpNode('OR')
    op.AddAttrNode('Name', 'RE_LIKE_NOCASE', None)
    return q

def usersQuery():
    q = CreateFASQLQuery(FUser, 'AND')
    op = q.AddOpNode('OR')
    op.AddAttrNode('Name', 'RE_LIKE_NOCASE', None)
    return q

#=======================================================================
# Main
#=======================================================================

if  __name__ == '__main__':  
    raise Exception('Must run within Prime.')
else:
    date_today = ael.date_today()
    default_report_path = 'c:/temp'
    module='FxTradeGenerator'
    dat_filevect=[]
    try:
        default_report_path = p.Logdir
    except:
        default_report_path = 'c:\\temp'
    if os.path.exists(default_report_path):
        for name in os.listdir(default_report_path):
            pass
            #if re.search("%s.*\.dat" % module,name,re.I):
            #    dat_filevect.append(os.path.normpath(os.path.join(default_report_path,name)))
    if Date == "Today":
        display_day = "Today"
    else:
        diff = Date
        if diff > 0: diff = '+ ' + str(diff)
        display_day = 'Today ' + str(diff) + ' days'

    ael_variables = \
    [
        ('testmode',              'Test mode',                    'string',               ['1', '0'],     str(TestMode), 1, 0),
        ('currency_pairs',        'Currency pairs',               'FCurrencyPair',        None,           currencyPairsQuery(), 2, 1),
        ('minimum_date',          'Minimum date',                 'date',                 date_today, None, 1),
        ('value_dates',           'Value dates (e.g. 1d 1w)',     'string',               '0d', None, 0),
        ('minimum_amount',        'Minimum amount',               'double',               1.0, 1.0, 1),
        ('maximum_amount',        'Maximum amount',               'double',               1000000.0, 1000000.0, 0),
        ('trade_count',           'Trades to create',             'int',                  100, 100, 0),
        ('delay_seconds',         'Delay in seconds',             'double',               0.0, 0.0, 0),
        ('accounting_parameters', 'Accounting parameters_Parties','FAccountingParameters',None,           accountingParametersQuery(), 2, 1),
        ('trading_portfolios',    'Trading portfolios_Parties',   'FPhysicalPortfolio',   None,           portfoliosQuery(), 2, 1),
        ('acquirers',             'Acquirers_Parties',            'FParty',               None,           partiesQuery(), 2, 1),
        ('counterparties',        'Counterparties_Parties',       'FParty',               None,           partiesQuery(), 2, 1),
        ('traders',               'Traders_Parties',              'FUser',                None,           usersQuery(), 2, 1),
        ('log_report',            'Log report in console_Logging','string',               ['Yes','No'], 'Yes', 0, 0),
        ('logmode',               'Log mode_Logging',             'string',               ['0', '1', '2'], str(LogMode), 1, 0),
        ('log_to_console',        'Log to console_Logging',       'string',               ['1', '0'], str(LogToConsole), 1, 0),
        ('log_to_file',           'Log to file_Logging',          'string',               ['1', '0'], str(LogToFile), 1, 0),
        ('logfile',               'Logfile_Logging',              'string',               [Logfile], Logfile, 0, 0),
        ('report_path',           'Report directory path_Logging','string',               [], default_report_path, 0, 0),\
    ]

    def ael_main(dictionary):
        global rep_filename
        parameters={}
        do_log_report=0
        date_today = ael.date_today()

        for (k,v) in dictionary.items():
            if k == 'testmode':
                v = int(v)
            if k == 'log_report':
                if v == 'Yes':
                    do_log_report=1
                continue
            parameters[k]=v
        
        LogMode = int(parameters['logmode'][0])
        LogToConsole = int(parameters['log_to_console'][0])
        LogToFile = int(parameters['log_to_file'][0])
        Logfile = parameters.get('logfile')
        logme.setLogmeVar(ScriptName, 
                          LogMode, 
                          LogToConsole, 
                          LogToFile, 
                          Logfile,
                          0, "", "")
        parameters['force'] = 'No'
        value_dates = string.split(parameters['value_dates'])
        
        amount_block = 100000.0
        default_portfolio = None
        portfolio = None
        portfoliosForCurrencyPairs = {}
        for portfolio in parameters['trading_portfolios']:
            portfoliosForCurrencyPairs[portfolio.CurrencyPair()] = portfolio

        logme('BEGAN GENERATING TRADES...')
        count = parameters['trade_count']
        try:
            for i in range(1, count + 1):
                currency_pair = random.choice(parameters['currency_pairs'])
                if random.choice([True, False]):
                    instrument_currency = currency_pair.Currency1()
                    trading_currency = currency_pair.Currency2()
                else:
                    instrument_currency = currency_pair.Currency2()
                    trading_currency = currency_pair.Currency1()
                amount = random.uniform(parameters['minimum_amount'], parameters['maximum_amount'])
                amount = amount_block * int(amount /amount_block + 0.5)
                acquirer = random.choice(parameters['acquirers'])
                counterparty = random.choice(parameters['counterparties'])
                period = random.choice(value_dates)
                print 'period ', period
                trader = random.choice(parameters['traders'])
                spot_date = ael.date(currency_pair.spot_date())
                ael_instrument_currency = ael.Instrument[instrument_currency.Name()]
                value_date = spot_date.add_period(period)
                value_date = value_date.adjust_to_banking_day(ael_instrument_currency)
                price = ArenaFunctionBridge.fx_forward_price(ael_instrument_currency.insid, trading_currency.Name(), value_date)
                price = price * (1 + 0.02 * (random.random() - 0.5))
                int_price = int(price * 10000.0 + 0.5)
                price = int_price / 10000.0
                trade = acm.FTrade()
                trade.Status(ael.enum_from_string('TradeStatus', 'Simulated'))
                trade.Instrument(instrument_currency)
                trade.Type(ael.enum_from_string('TradeType', 'TRADE_NORMAL'))
                #if period == '0d':
                #    trade.Type(ael.enum_from_string('TradeType', 'TRADE_FX_SPOT'))
                #else:
                #    trade.Type(ael.enum_from_string('TradeType', 'TRADE_FX_FORWARD'))
                trade.Currency(trading_currency)
                trade.Price(price)
                trade.ValueDay(value_date)
                trade.AcquireDay(value_date)
                trade.Acquirer(acquirer)
                trade.Trader(trader)
                trade.TradeTime(ael.date_today())
                portfolio = None
                portfolio_name = "No portfolio"
                if portfoliosForCurrencyPairs.has_key(currency_pair):
                    portfolio = portfoliosForCurrencyPairs[currency_pair]
                    trade.Portfolio(portfolio)
                    portfolio_name = portfolio.Name()
                if portfolio == None:
                    logme('No matching portfolio found - skipping')
                    portfolio = default_portfolio
                    continue
                trade.Counterparty(counterparty)
                if random.choice([True, False]):
                    amount = -1.0 * amount
                trade.Quantity(amount)
                trade.Premium(-1.0 * amount * price)
                trade.Status(ael.enum_from_string('TradeStatus', 'FO Confirmed'))
                logme('%7d: %-10.10s %-12.12s %14.2f %.3s at %5.5s (%s) with %-12.12s for %14.2f %3s at %9.4f in %s.' % (i, trade.Type(), acquirer.Name(), amount, instrument_currency.Name(), period, value_date, counterparty.Name(), trade.Premium(), trading_currency.Name(), price, portfolio_name))
                if not parameters['testmode']:
                    trade.Commit()
                if parameters['delay_seconds']:
                    time.sleep(parameters['delay_seconds'])
        except:
            print sys.exc_info()[0]
            print traceback.print_tb(sys.exc_info()[2])
        logme('ENDED GENERATING TRADES.')
