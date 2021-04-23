#Author: Andreas Bayer
#Market value column
#Current Notional column
#
#05/07/2016: Faize Adams   -   Fixed issue by importing CSV.
#                              Added .csv extension to output file.
#
#12/07/2016: Faize Adams   -   Added print statement to print file name
#                              to output.

import csv
import acm, ael, string, time
from datetime import datetime
from at_time import acm_date, ael_date, to_datetime, to_date
from datetime import datetime

import cProfile, pstats, StringIO
import FLogger
from at_ael_variables import AelVariableHandler
from collections import defaultdict, namedtuple
import os.path

ael_variables = AelVariableHandler()

CALC_SPACE = acm.Calculations().CreateCalculationSpace(
            acm.GetDefaultContext(), 
            'FPortfolioSheet'
)

ael_variables.add(
    'trade_filter', 
    label = 'Trade Filter', 
    cls = 'string', 
    collection = acm.FTradeSelection.Select(''), 
    default = 'IRF_PB_Stock',
)

ael_variables.add(
    'output_directory', 
    label = 'Output Directory', 
    cls = 'string', 
    collection = acm.FTradeSelection.Select(''), 
    default = r'F:\temp',
)

Entry = namedtuple('Entry', [
    'Instrument', 
    'Instrument_Type', 
    'Portfolio', 
    'Counterparty', 
    'Position', 
    'Nominal', 
    'Market_Value'
    ])

def get_trades_by_filter(trade_filter_name):
    '''
    returns a snapshot of trades matching a trade_filter_name
    '''
    trade_filter = acm.FTradeSelection[trade_filter_name]
    trades = trade_filter.Snapshot()
    #in case memory is a problem, use SnapshotTradeNbrs() to avoid loading all trades at once
    return trades
    
def get_data(tf_name):
    trades_per_client = defaultdict(list)
    
    trades = get_trades_by_filter(tf_name)
    
    for trade in trades:
        counterparty = trade.Counterparty().Name()
        instrument = trade.Instrument().Name()
        instype = trade.Instrument().InsType()
        portfolio = trade.Portfolio().Name()
        
        trades_per_client[instrument, instype, portfolio, counterparty].append(trade)
        
    return trades, trades_per_client

def get_top(path, all_trades, trades_per_client, trade_filter):
    positions_per_client = defaultdict(list)
    for instrument, instype, portfolio, client in trades_per_client:
        trades = trades_per_client[instrument, instype, portfolio, client]
        portf = acm.FAdhocPortfolio()
        for trade in trades:
            portf.Add(trade)
        position = CALC_SPACE.CalculateValue(portf, 'Portfolio Position', None, False)
        nominal = CALC_SPACE.CalculateValue(portf, 'Current Nominal', None, False)
        market_value = CALC_SPACE.CalculateValue(portf, 'Portfolio Value', None, False)
        positions_per_client[instrument, instype, portfolio, client].append(position)
        positions_per_client[instrument, instype, portfolio, client].append(nominal)
        positions_per_client[instrument, instype, portfolio, client].append(market_value)
        
        
    filepath = os.path.join(path, 'Exposure_%s.csv' % trade_filter)
    with open(filepath, 'w') as f:
        writer = csv.DictWriter(
            f,
            Entry._fields,
            delimiter='|',
            lineterminator = '\n'
        )
        writer.writerow(dict(list(zip(Entry._fields, Entry._fields))))
        
        for instrument, instype, portfolio, client in positions_per_client:
            line = Entry(
                Instrument = instrument, 
                Instrument_Type = instype, 
                Portfolio = portfolio, 
                Counterparty = client, 
                Position = positions_per_client[instrument, instype, portfolio, client][0], 
                Nominal = positions_per_client[instrument, instype, portfolio, client][1], 
                Market_Value = positions_per_client[instrument, instype, portfolio, client][2].Number()
            )
            writer.writerow(line._asdict())
    
    print 'Wrote secondary output to: ', filepath
    print 'Completed successfully'
    
def ael_main(ael_dict):
    all_trades, trades_per_client = get_data(ael_dict['trade_filter'])
    get_top(ael_dict['output_directory'], all_trades, trades_per_client, ael_dict['trade_filter'])
