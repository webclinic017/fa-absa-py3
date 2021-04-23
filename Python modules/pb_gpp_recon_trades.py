"""
Description
===========
Date                          :  2018-02-06
Purpose                       :  GPP project: Identify missing trades in FA
Department and Desk           :  FO Prime Services
Requester                     :  Eveshnee Naidoo
Developer                     :  Ondrej Bahounek

Details:
========
A user has to download trades from GPP Portal in csv files.
There are 3 different files - for Equity, Equity Swaps and Futures & Options.
This module can be given all 3 on its input.
Result will be a report with all trades that are in input files, but not in FA.
"""

import csv
from collections import defaultdict
from os.path import basename, join
import string
from datetime import datetime
import acm
import FRunScriptGUI
from at_logging import getLogger
from at_ael_variables import AelVariableHandler


LOGGER = getLogger(__name__)
ael_variables = AelVariableHandler()
DEFAULT_OUT_FILENAME = '${DATE}_gpp_recon.csv'


class ColumnIndexer(object):

    def __init__(self, file_path):
    
        self.file_path = file_path    
        self.trade_ref = None
        self.account = None
        self.trade_date = None
        self.ins_descr = None
        self.ins_code = None
        self.ins_type = None
        self.trans_desc_col = None
        self.trans_desc_excl = None
        
    def line_to_row(self, line):
        return [
            line[self.ins_type] if isinstance(self.ins_type, int) else self.ins_type,
            line[self.trade_ref],
            line[self.account],
            line[self.trade_date],
            line[self.ins_descr],
            
            basename(self.file_path)
            ]
            
    @staticmethod
    def get_headers():
        return ["Ins Type", "Trade Ref", "Account", "Trade Date", "Instr Description",
            "Filename"]


fileFilter = "CSV Files (*.csv)|*.csv|"
inputFile = FRunScriptGUI.InputFileSelection(FileFilter=fileFilter)
directorySelection = acm.FFileSelection()
directorySelection.PickDirectory(True)
directorySelection.SelectedDirectory('')


ael_variables.add(
    'file_equities',
    label = 'File Equities',
    cls = inputFile,
    default = inputFile,
    #default=r'c:\DEV\Perforce\FA\features\ABITFA-5097 - SBL uploader.br\input\sl_upload_file_excel_test.xlsx',
    mandatory = False,
    multiple = True,
    alt = 'Input file equities.'
    )
ael_variables.add(
    'file_equity_swaps',
    label = 'File Equity Swaps',
    cls = inputFile,
    default = inputFile,
    #default=r'c:\DEV\Perforce\FA\features\ABITFA-5097 - SBL uploader.br\input\sl_upload_file_excel_test.xlsx',
    mandatory = False,
    multiple = True,
    alt = 'Input file equity swaps (CFDs).'
    )
ael_variables.add(
    'file_futures',
    label = 'File Futs Opts',
    cls = inputFile,
    default = inputFile,
    #default=r'c:\DEV\Perforce\FA\features\ABITFA-5097 - SBL uploader.br\input\sl_upload_file_excel_test.xlsx',
    mandatory = False,
    multiple = True,
    alt = 'Input file futures and options.'
    )
ael_variables.add(
    'out_filename',
    label = 'Output File',
    cls = 'string',
    default = DEFAULT_OUT_FILENAME,
    mandatory = False,
    multiple = False,
    alt = 'Name of output file'
    )
ael_variables.add(
    'directory',
    label = 'Directory',
    cls = directorySelection,
    collection =  None,
    default = directorySelection,
    mandatory = False,
    multiple = True,
    alt = 'Output path'
    )
ael_variables.add_bool(
    'show_all',
    label = 'Show All Trades?',
    default = False,
    alt = 'Show all trades or just missing trades?'
    )


def porcess_trdref(trd_ref):
    if trd_ref.startswith('0'):
        trd_ref = trd_ref[1:]
        
    if trd_ref[-3:-1] == 'T0':
        trd_ref = trd_ref[:-3]
        
    return trd_ref


def get_output_fn(directory, file_name):
    fname_template = string.Template(file_name)
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    file_name = fname_template.substitute(DATE=today)

    return join(directory, file_name)
    
def ael_main(ael_dict):
    LOGGER.msg_tracker.reset()
    out_file = None
    if ael_dict['out_filename']:
        out_file = get_output_fn(str(ael_dict['directory']), str(ael_dict['out_filename']))
    show_all = ael_dict['show_all']
    missing_trades = defaultdict(list)
    
    eq_col_obj = ColumnIndexer(str(ael_dict['file_equities']))
    eq_col_obj.trade_ref = 0
    eq_col_obj.account = 2
    eq_col_obj.trade_date = 15
    eq_col_obj.ins_descr = 4
    eq_col_obj.ins_type = 1
    
    fut_col_obj = ColumnIndexer(str(ael_dict['file_futures']))
    fut_col_obj.trade_ref = 1
    fut_col_obj.account = 0
    fut_col_obj.trade_date = 2
    fut_col_obj.ins_descr = 11
    fut_col_obj.ins_type = "F&O"
    fut_col_obj.trans_desc_col = 3
    fut_col_obj.trans_desc_excl = ('Future Settlement',)
    
    swap_col_obj = ColumnIndexer(str(ael_dict['file_equity_swaps']))
    swap_col_obj.trade_ref = 3
    swap_col_obj.account = 0
    swap_col_obj.trade_date = 11
    swap_col_obj.ins_descr = 9
    swap_col_obj.ins_type = 2
    
    file_objects = (eq_col_obj, fut_col_obj, swap_col_obj)
    
    for file_obj in file_objects:
        if not file_obj.file_path:
            continue
        
        base_name = basename(file_obj.file_path)
        col_index = file_obj.trade_ref  # GPP trade ref column number
        LOGGER.info('Reading: %s', file_obj.file_path)
        
        with open(file_obj.file_path, "rb") as csv_file:
            
            reader = csv.reader(csv_file, delimiter=",")
            reader.next()
            for line in reader:
                if file_obj.trans_desc_col is not None and \
                        line[file_obj.trans_desc_col] in file_obj.trans_desc_excl:
                    continue
                orig_trd_ref = line[col_index]
                trd_ref = porcess_trdref(orig_trd_ref)
                gpp_trade = orig_trd_ref
                fa_trade = acm.FTrade.Select('optionalKey="%s"' %trd_ref)
                if show_all:
                    print("%s --> %s" %(gpp_trade, fa_trade))
                if not fa_trade:
                    missing_trades[base_name].append(file_obj.line_to_row(line))
            
    for fn, lines in missing_trades.items():
        LOGGER.error("Missing GPP trades from: '%s'", fn)
        for row in lines:
            print(row[1])
    
    if out_file:  # output report is not mandatory
        with open(out_file, "wb") as csv_out_file:
            writer = csv.writer(csv_out_file)
            writer.writerow(ColumnIndexer.get_headers())
            for fn, lines in missing_trades.items():
                for row in lines:
                    writer.writerow(row)
        LOGGER.info("Wrote output to: '%s'", out_file)
        
    if LOGGER.msg_tracker.errors_counter:
        raise RuntimeError("ERRORS occurred. Please check the log.")
        
    LOGGER.info("Completed successfully.")
        
