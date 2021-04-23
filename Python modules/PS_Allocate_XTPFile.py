"""
Description
===========
Date                          :  2018-07-04
Purpose                       :  Generate Allocations XTP File
Department and Desk           :  FO Prime Services
Requester                     :  Naidoo, Eveshnee: Markets (JHB)
Developer                     :  Ondrej Bahounek

Details:
========
Generate csv file that will be used for XTP booking.
The file will contain information about OD and GU trades.
"""

import csv
import os
from collections import defaultdict

import acm
from at_ael_variables import AelVariableHandler
from at_logging import getLogger
from FBDPCommon import toDate


LOGGER = getLogger(__name__)
TODAY = acm.Time.DateToday()

DIRECTORY_SELECTION = acm.FFileSelection()
DIRECTORY_SELECTION.PickDirectory(True)
DIRECTORY_SELECTION.SelectedDirectory('')
DEFAULT_FILE_NAME = 'ABSA_OD file [date].csv'

ael_variables = AelVariableHandler()

ael_variables.add(
    'for_date',
    label = 'Date',
    cls = 'string',
    collection = [TODAY, 'Today'],
    default = 'Today',
    mandatory = True,
    multiple = False,
    alt = 'Trades from this will be selected.'
    )
ael_variables.add(
    'report_type',
    label = 'Report Type',
    cls = 'string',
    collection =  ['OD', 'GU'],
    default = 'OD',
    mandatory = True,
    multiple = False,
    alt = 'Trades type to select'
    )
ael_variables.add(
    'broker_code',
    label = 'Broker Code',
    cls = 'string',
    default = 'FNEQZAJJXXX',
    mandatory = True,
    multiple = False,
    alt = 'Broker code'
    )
ael_variables.add(
    'acc_portf',
    label = 'Account Portfolio',
    cls = acm.FPhysicalPortfolio,
    default = None,
    mandatory = True,
    multiple = False,
    alt = 'OD/GU Portfolio'
    )
ael_variables.add(
    'points',
    label = 'Points',
    cls = 'float',
    default = 5,
    mandatory = True,
    multiple = False,
    alt = 'Basis points added during Price calculation.'
    )
ael_variables.add(
    'directory',
    label = 'Directory',
    cls = DIRECTORY_SELECTION,
    collection = None,
    default = DIRECTORY_SELECTION,
    mandatory = True,
    multiple = True,
    alt = 'Output path'
    )
ael_variables.add(
    'file_name',
    label = 'Output File',
    cls = 'string',
    collection = [DEFAULT_FILE_NAME],
    default = None,
    mandatory = False,
    multiple = False,
    alt = 'Name of output file'
    )


def get_OD_trades(portf, for_date):
    query = acm.CreateFASQLQuery('FTrade', 'AND')
    query.AddAttrNode('TradeTime', 'GREATER_EQUAL', for_date)
    query.AddAttrNode('TradeTime', 'LESS_EQUAL', for_date)   
    query.AddAttrNode('Portfolio.Name', 'EQUAL', portf.Name())

    query.AddAttrNode('Status', 'NOT_EQUAL', 'Void')
    query.AddAttrNode('Status', 'NOT_EQUAL', 'Simulated')
    query.AddAttrNode('Status', 'NOT_EQUAL', 'Terminated')
    
    trades = query.Select()
    trades = sorted(trades, key=lambda t: t.Instrument().Name())
    return trades


def instr_code_to_stoke(instr_name):
    parts = instr_name.split('/')
    if parts[1] == 'NPN':
        stoke = parts[1] + 'Jn.J'
    else:
        stoke = parts[1] + 'J.J'
    return stoke


def calc_price(trade, bps):
    sign = trade.Quantity() / abs(trade.Quantity())
    price = trade.Price() * (1 + sign * bps / 10000)
    return round(price, 4)


def generate_data(trades, report_type, broker_code, acc_portf, bps):
    bda_num = acc_portf.add_info('prt_BDA AccountNum')
    cap = "P" if report_type == "OD" else "A"
    
    HEADER_FUNC_MAPPING = (
        ('Report Type', lambda t: report_type),
        ('Direction', lambda t: "B" if t.Direction()[0] == "S" else "S"),
        ('StokeCode', lambda t: instr_code_to_stoke(t.Instrument().Name())),
        ('Qty', lambda t: abs(t.Quantity())),
        ('Price', lambda t: calc_price(t, bps)),
        ('Broker Code', lambda t: broker_code),
        ('Trd Date', lambda t: acm.Time.DateFromTime(t.TradeTime())),
        ('Trd Time', lambda t: ""),
        ('Buy Acc', lambda t: bda_num if t.Quantity() < 0 else ""),
        ('Buy Capacity', lambda t: cap if t.Quantity() < 0 else ""),
        ('Sell Acc', lambda t: bda_num if t.Quantity() > 0 else ""),
        ('Sell Capacity', lambda t: cap if t.Quantity() > 0 else ""),
        )
    
    header = [col_name for col_name, _f in HEADER_FUNC_MAPPING]
    rows = list()
    
    for t in trades:
        data_dict = {}
        for col, fnc in HEADER_FUNC_MAPPING:
            data_dict[col] = fnc(t)
        rows.append(data_dict)
    
    return (header, rows)


def write_to_file(header, data_rows, file_path):
    LOGGER.info('Writing to output: %s', file_path)
    with open(file_path, "wb") as outfile:
        dicwriter = csv.DictWriter(outfile, header)
        dicwriter.writeheader()
        dicwriter.writerows(data_rows)


def get_file_name(directory, file_name, for_date):
    if not file_name:
        file_name = DEFAULT_FILE_NAME
    if not file_name.endswith('.csv'):
        file_name += '.csv'
    
    file_name = file_name.replace('[date]', for_date)
    full_path = os.path.join(directory, file_name)
    
    while os.path.isfile(full_path):  # create unique file
        full_path = full_path.replace('.csv', '(1).csv')
    
    return full_path


def ael_main(ael_dict):
    LOGGER.msg_tracker.reset()
    for_date = toDate(ael_dict['for_date'])
    file_path = get_file_name(str(ael_dict['directory']), ael_dict['file_name'], for_date)
    
    report_type = ael_dict['report_type']
    broker_code = ael_dict['broker_code']
    acc_portf = ael_dict['acc_portf']
    bps = ael_dict['points']
    
    trades = get_OD_trades(acc_portf, for_date)
    header, data_rows = generate_data(trades, report_type, broker_code, acc_portf, bps)
    write_to_file(header, data_rows, file_path)
    LOGGER.info('Completed successfully.')
