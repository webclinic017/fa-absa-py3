'''
Created on 14 Jan 2016

@author: conicova

https://confluence.barcapint.com/display/ABCAPFA/PB+Settlement+Control
'''

import csv
import os.path
from datetime import datetime
from collections import defaultdict

import acm
from at_report import CSVReportCreator
from at_ael_variables import AelVariableHandler
from PS_FormUtils import DateField
from PS_Functions import (get_pb_fund_counterparties,
                          get_pb_fund_shortname,
                          get_pb_pswap_ff_flag)

from at_logging import getLogger, bp_start

LOGGER = getLogger(__name__)

VERSION = "1.0"

# set to true to turn on debugging information
DEBUG = False
# generated report only for the specified clients
DEBUG_CLIENTS = ['NOVFI2']  # 'MAP290', 'COGITO'
# Output to log information about the specified instruments
DEBUG_INSTRUMENTS = []  # 'ZAR/FUT/AGQ/JUN12/P/279.92/MTM'
SHOW_NO_BREAK = True

DEFAULT_DIR = r"C:\services\frontnt\Task\SETTLEMENT_CONTROL_INPUT\PrimeForward"

class SettlementControlException(Exception):
    """General purpose exception"""
    pass

class ColumnMapping(object):
    """Specify the mapping between the column name and the set of input reports"""
    
    NUMBER = 'number' 
    VARCHAR = 'varchar'
    
    def __init__(self, report_key, name, name_in_report, default_value=None, val_type=None, val_converter=None, computed=False):
        '''Initialise a new instance
        
        report_key - unique identifier of the report
        name - the column name, has to be unique for all collumn mappings
        name_in_report - the column name in the report
        defualt_value - the value that will be used in case if the report doesn't provide any value
        val_type - the value type (see CollumnMapping constants), used for conversion
        '''
        self.report_key = report_key
        self.name = name
        self.name_in_report = name_in_report
        self.val_type = val_type
        self.default_value = default_value
        self.val_converter = val_converter
        self.computed = computed
    
    def __str__(self):
        return ("Report key: '{0}', Name: '{1}', Val type: '{2}', Default val: '{3}'").format(self.report_key,
                                                                                              self.name,
                                                                                              self.val_type,
                                                                                              self.default_value)
    
    def fix_value(self, value):
        '''Return a converted value based on the column_map specification. If conversion 
        fails, the default value is used.s
        
        value - a string
        column_map - instance of ColumnMapping (contains the value type and default value)s 
        '''
        result = value
        if self.val_type == ColumnMapping.NUMBER:
            try:
                result = float(result)
            except Exception:
                LOGGER.debug("Could not convert value to float: %s", result)
                result = self.default_value
        
        return result
    
class ReportMapping(object):
    '''Specified the mapping between report keys and input reports'''
    
    def __init__(self, report_name, key, row_key=[], ignore_rows=0, report_dir=None):
        '''Initialise a new instance
        
        report_name - the report name with the client and timestamp placeholders
        key - unique string that used for reference in other objects
        row_key - the list of columns that form the primary key (column name, not the name from the report)
        ignore_rows - when reading the file, ignore the number of specified rows
        '''
        self.report_name = report_name 
        self.key = key
        self.row_key = row_key
        self.ignore_rows = ignore_rows
        self.column_maps_keys = None
        self.report_dir = report_dir
    
    def set_column_maps_keys(self, column_maps_keys):
        self.column_maps_keys = column_maps_keys
    
    def generate_row_key(self, se_row_key):
        """ Generated a string representation of the row key.
        This is generated based on the definition of the report key columns and the provided dictionary. 
        """
        values = []
        for column_map in self.column_maps_keys:
            if not se_row_key.has_key(column_map.name):
                raise Exception("Could not find the column '{0}' in the se_row_key '{1}'".format(column_map.name, se_row_key))
            values.append(se_row_key[column_map.name])
        
        return "||".join(values)
        
class ReportInfo(object):
    '''Contains information about each input report'''
    
    def __init__(self, report_map, date, shortname, input_path):
        '''Initialise a new instance
        
        report_map - ReportMapping instance
        date - the report date, used to identify the report name
        shortname - the client short name, used to identify the report name
        input_path - the path to the directory with all clients
        '''
        self.report_map = report_map
        self.date = date
        self.shortname = shortname
        self.input_path = input_path
    
    def get_file_name(self):
        '''Returns the file name based on the specified short name and date'''
        return self.report_map.report_name.format(client=self.shortname, timestamp=self.date.replace('-', ''))
    
    def get_file_path(self):
        '''Returns the full file path'''
        filename = self.get_file_name()
        file_path = os.path.join(self.input_path, self.shortname, self.date, filename)
        if not os.path.isfile(file_path):
            # try to get the file without the date
            filename_test = self.report_map.report_name.format(client=self.shortname, timestamp='')[:-5] + ".csv"
            file_path_test = os.path.join(self.input_path, self.shortname, self.date, filename_test)
            if os.path.isfile(file_path_test):
                file_path = file_path_test
            else:
                LOGGER.info("File not found: '%s'", file_path_test)
        return file_path
    
class SEValue(object):
    '''Start End Value. Contains a pair of values and information about them'''
    
    def __init__(self, column_map, start_value, end_value):
        '''Initialise a new instance
        
        column_map - instance of ColumnMapping
        start_value - a string
        end_value - a string
        '''
        self.column_map = column_map
        self.start_value = column_map.fix_value(start_value)
        self.end_value = column_map.fix_value(end_value)
    
    def get_any_value(self):
        if self.end_value:
            return self.end_value
        else:
            return self.start_value
    
    def __str__(self):
        return "('{0}', '{1}')".format(self.start_value, self.end_value)

class SERowKeyComponent(object):
    
    def __init__(self, column_map, value=None):
        self.column_map = column_map
        self.value = value
    
    def __str__(self):
        return "Key '{0}' value '{1}'".format(self.column_map.name, self.value)

class SERowKey(object):
    
    def __init__(self, se_row_key_components=[]):
        self.se_row_key_components = se_row_key_components
    
    def get_key(self, report_map):
        se_key_row = {}
        for item in self.se_row_key_components:
            se_key_row[item.column_map.name] = item.value
        
        return report_map.generate_row_key(se_key_row)
    
    def __str__(self):
        result = ""
        for se_row_key_component in self.se_row_key_components:
            result += "{0}; ".format(se_row_key_component)
        
        return result
    
class SERow(object):
    '''Start End Row. A container for SEValues, which represent a row from the reports.
    Each row has a unique key, which is represented by a SERowKey item.
    ''' 
    
    def __init__(self, se_values, se_row_key):
        self.se_values = {} 
        for se_value in se_values:
            self.se_values[se_value.column_map.name] = se_value
        self.se_row_key = se_row_key
    
    def get_value(self, column_name):
        return self.se_values[column_name]
    
    def has_column(self, column_name):
        return self.se_values.has_key(column_name)
    
    @classmethod
    def init_from_dic(cls, start_values, end_values, report_map):
        """ Returns a new SERow from two dictionaries (column name: value)"""
        se_values = {}
        for column_name, value in end_values.iteritems():
            column_map = CSVDataLoader.get_column_mapping(column_name, report_map)
            # ignore undefined columns
            if not column_map:
                continue
            # the start value may not exist (Ex a new trade row)
            if not start_values.has_key(column_name):
                start_value = ""
            else:
                start_value = start_values[column_name]
            se_val = SEValue(column_map, start_value, value)
            se_values[column_map.name] = se_val
        
        for column_name, value in start_values.iteritems():
            column_map = CSVDataLoader.get_column_mapping(column_name, report_map)
            # ignore undefined columns
            if not column_map:
                continue
            if not se_values.has_key(column_map.name):
                se_val = SEValue(column_map, value, end_values[column_name])
                se_values[column_map.name] = se_val 
        
        if not se_values:
            # LOGGER.info("Start Values: %s", start_values)
            # LOGGER.info("End Values: %s", end_values)
            return None
        
        se_row_key_componentes = []
        for column_map in report_map.column_maps_keys:
            if not se_values.has_key(column_map.name):
                LOGGER.debug("Values: %s", se_values)
                raise Exception("Could not find the key column: '{0}'".format(column_map))
            if se_values[column_map.name].end_value:
                value = se_values[column_map.name].end_value
            else:
                value = se_values[column_map.name].start_value
            se_row_key_componentes.append(SERowKeyComponent(column_map, value))
            
                
        return SERow(se_values.values(), SERowKey(se_row_key_componentes))
    
    def get_key(self, report_map):
        return self.se_row_key.get_key(report_map)
    
    def __str__(self):
        result = ""
        for key, se_row in self.se_values.iteritems():
            result += "{0}->{1}; ".format(key, se_row)
        return result
    
class SEDataSet(object):  
    '''Start End DataSet. A container for SERows, which represent a set of reports (by type).'''
    
    def __init__(self):
        self.se_rows = {}
        self.start_report = None
        self.end_report = None
    
    @classmethod
    def init_from_dic(cls, start_values, end_values, report_map):
        result = SEDataSet()
        if end_values:
            for key, end_row in end_values.iteritems():
                start_row = {}
                if start_values:
                    start_row = start_values[key]
                se_row = SERow.init_from_dic(start_row, end_row, report_map)
                if se_row:
                    result.add_row(se_row, report_map)
        
        if start_values:
            for key, start_row in start_values.iteritems():
                se_row = SERow.init_from_dic(start_row, defaultdict(str), report_map)
                if se_row and not result.has_row(se_row.get_key(report_map)):
                    result.add_row(se_row, report_map)    
        return result
        
    def add_row(self, se_row, report_map):
        self.se_rows[se_row.get_key(report_map)] = se_row
    
    def has_row(self, key):
        return self.se_rows.has_key(key)
    
    def get_row(self, key):
        """ Returns an SERow """
        return self.se_rows[key]
    
    def get_value(self, column_map, key):
        """ Returns an SEValue """
        se_row = self.se_rows[key]
        if not se_row.has_column(column_map.name):
            raise Exception("Column name '{0}' could not be found for the specified key '{1}'".format(column_map.name, key))
        return self.se_rows[key].get_value(column_map.name)
    
    def get_values(self, column_maps):
        """Returns a list of dictionaries"""
        result = []
        for key in self.se_rows.keys():
            item = {}
            for column_map in column_maps:
                item[column_map.name] = self.get_value(column_map, key)
            
            result.append(item)
            
        return result
    
    def __str__(self):
        result = ""
        for key, se_row in self.se_rows.iteritems():
            result += "'{0}' -> [{1}]\n".format(key, se_row)
        return result

def _portfolio_to_financed(pname, row):
    pswap = acm.FInstrument[pname]
    financed_flag = not get_pb_pswap_ff_flag(pswap)
    if financed_flag:
        return "Financed"
    else:
        return "Fully Funded"

def _empty_to_cfd(ins_type, row):
    if not ins_type and not row['Deposit Type']:
        return "CFD"
    return ins_type

def _empty_ins_name_loan_acc(ins_name, row):
    if not ins_name:
        return str(row['Trade Number'])
    return ins_name

class CSVDataLoader(object):
    """Loads the specified CSV. Implements the ADataLoader methods"""
    CALL_REPORT = 'CallAccountSweepingReport'
    LOAN_REPORT = 'LoanAccountSweepingReport'
    POSITION_REPORT = 'PositionInstrument'
    PERFORMANCE_REPORT = 'PerfReport'
    CASH_ANALYSIS = 'CASH_ANALAYSIS'
    CFD_SWEEPING = 'CFD_SWEEPING'
    
    # !!! Use the mapping column name, not the report column name
    _REPORTS = [ReportMapping('{client}_CallAccountSweepingReport_{timestamp}.csv', CALL_REPORT, ['Instrument Name', 'Financing Method']),
              ReportMapping('{client}_LoanAccountSweepingReport_{timestamp}.csv', LOAN_REPORT , ['Instrument Name']) ,
              ReportMapping('{client}_File_PositionInstrument_{timestamp}.csv', POSITION_REPORT, ['Instrument Name'], 6),
              ReportMapping('{client}_File_Performance_{timestamp}.csv', PERFORMANCE_REPORT, ['Instrument Name', 'Financing Method'], 6),
              ReportMapping('{client}_File_CashAnalysis_{timestamp}.csv', CASH_ANALYSIS, ['PSwap Instrument Type', 'Pay Date'], 6),
              ReportMapping('{client}_CFD_Sweeping_{timestamp}.csv', CFD_SWEEPING, ['Date', 'Instrument'], 0)]
    
    """There may be multiple entries with the same caolumn name, but they have to be from different reports.
    This makes sense when we want to use the column as key, for merging different reports"""
    _COLUMN_MAPPING = [ColumnMapping(CALL_REPORT, 'Instrument Type', 'Instrument Type', '', ColumnMapping.VARCHAR),
                       ColumnMapping(CALL_REPORT, 'Instrument Name', 'Instrument Name', '', ColumnMapping.VARCHAR),
                       ColumnMapping(CALL_REPORT, 'Client TPL', 'Client TPL', 0, ColumnMapping.NUMBER),
                       ColumnMapping(CALL_REPORT, 'Diff', 'Diff', 0, ColumnMapping.NUMBER),
                       ColumnMapping(CALL_REPORT, 'Adjustment Posting', 'Adjustment Posting', 0, ColumnMapping.NUMBER),
                       ColumnMapping(CALL_REPORT, 'Portfolio Swap', 'Portfolio Swap', '', ColumnMapping.VARCHAR),
                       ColumnMapping(CALL_REPORT, 'Financing Method', 'Portfolio Swap', '', ColumnMapping.VARCHAR, _portfolio_to_financed, True),
                       ColumnMapping(CALL_REPORT, 'Portfolio Cash End', 'Portfolio Cash End', 0, ColumnMapping.NUMBER),
                       ColumnMapping(CALL_REPORT, 'Daily Provision', 'Daily Provision', 0, ColumnMapping.NUMBER),
                       ColumnMapping(CALL_REPORT, 'Daily Funding', 'Daily Funding', 0, ColumnMapping.NUMBER),
                       ColumnMapping(CALL_REPORT, 'Daily Warehousing', 'Daily Warehousing', 0, ColumnMapping.NUMBER),
                       ColumnMapping(POSITION_REPORT, 'Cash Balance', 'Cash Balance', 0, ColumnMapping.NUMBER),
                       ColumnMapping(POSITION_REPORT, 'Instrument Name', 'Instrument', '', ColumnMapping.VARCHAR),
                       ColumnMapping(LOAN_REPORT, 'Instrument Name', 'Instrument Name', '', ColumnMapping.VARCHAR, _empty_ins_name_loan_acc),
                       ColumnMapping(LOAN_REPORT, 'Portfolio Value End', 'Portfolio Value End', 0, ColumnMapping.NUMBER),
                       ColumnMapping(PERFORMANCE_REPORT, 'Instrument Name', 'Instrument', '', ColumnMapping.VARCHAR),
                       ColumnMapping(PERFORMANCE_REPORT, 'Portfolio Swap', 'Portfolio', '', ColumnMapping.VARCHAR),
                       ColumnMapping(PERFORMANCE_REPORT, 'Instrument Type', 'Instrument Type', '', ColumnMapping.VARCHAR),
                       ColumnMapping(PERFORMANCE_REPORT, 'Financing Method', 'Financing Method', '', ColumnMapping.VARCHAR),
                       ColumnMapping(PERFORMANCE_REPORT, 'Closing Value End', 'Closing Value End', 0, ColumnMapping.NUMBER),
                       ColumnMapping(PERFORMANCE_REPORT, 'Closing Cash Payments', 'Closing Cash Payments', 0, ColumnMapping.NUMBER),
                       ColumnMapping(PERFORMANCE_REPORT, 'Closing Cash Resets', 'Closing Cash Resets', 0, ColumnMapping.NUMBER),
                       ColumnMapping(PERFORMANCE_REPORT, 'Since Inception Execution Fee', 'Since Inception Execution Fee', 0, ColumnMapping.NUMBER),
                       ColumnMapping(PERFORMANCE_REPORT, 'Daily TPL', 'Daily TPL', 0, ColumnMapping.NUMBER),
                       ColumnMapping(PERFORMANCE_REPORT, 'Inception TPL', 'Inception TPL', 0, ColumnMapping.NUMBER),
                       ColumnMapping(PERFORMANCE_REPORT, 'Opening Provision', 'Opening Provision', 0, ColumnMapping.NUMBER),
                       ColumnMapping(CASH_ANALYSIS, 'PSwap Instrument Type', 'PSwap Instrument Type', '', ColumnMapping.VARCHAR, _empty_to_cfd),
                       ColumnMapping(CASH_ANALYSIS, 'Pay Date', 'Pay Date', '', ColumnMapping.VARCHAR),
                       ColumnMapping(CASH_ANALYSIS, 'Projected Cash', 'Projected Cash', 0, ColumnMapping.NUMBER),
                       # ColumnMapping(CFD_SWEEPING, 'Portfolio', 'Portfolio', 0, ColumnMapping.VARCHAR),
                       ColumnMapping(CFD_SWEEPING, 'Date', 'Date', '', ColumnMapping.VARCHAR),
                       ColumnMapping(CFD_SWEEPING, 'Instrument', 'Instrument', '', ColumnMapping.VARCHAR),
                       ColumnMapping(CFD_SWEEPING, 'Instrument Type', 'Instrument Type', '', ColumnMapping.VARCHAR),
                       ColumnMapping(CFD_SWEEPING, 'Short Premium', 'Short Premium', 0, ColumnMapping.NUMBER),
                       ColumnMapping(CFD_SWEEPING, 'Mtm', 'Mtm', 0, ColumnMapping.NUMBER),
                       ColumnMapping(CFD_SWEEPING, 'Overnight Premium', 'Overnight Premium', 0, ColumnMapping.NUMBER),
                       ColumnMapping(CFD_SWEEPING, 'Execution Premium', 'Execution Premium', 0, ColumnMapping.NUMBER),
                       ColumnMapping(CFD_SWEEPING, 'Dividend', 'Dividend', 0, ColumnMapping.NUMBER)
                       ]
    
    def __init__(self, counterparty, start_date, end_date, input_path):
        CSVDataLoader._init_column_maps_keys()
        
        self.client = get_pb_fund_shortname(counterparty)
        self.counterparty = counterparty
        self.start_date = start_date
        self.end_date = end_date
        LOGGER.info("Loading CSVs for '%s' ...", self.client)
        
        self.reports = defaultdict(dict)
        self.se_reports = defaultdict(dict)
        
        for date in [self.start_date, self.end_date]:
            for report_map in CSVDataLoader._REPORTS:
                input_dir = report_map.report_dir if report_map.report_dir else input_path
                report_info = ReportInfo(report_map, date, self.client, input_dir)
                file_path = report_info.get_file_path()
                if not os.path.isfile(file_path):
                    LOGGER.info("Could not locate the file '%s', skipping ", file_path)
                    continue
                report_data = self._read_csv(file_path, report_map.ignore_rows)
                
#                 if report_map.key==CSVDataLoader.PERFORMANCE_REPORT:
#                     print report_data
                    
                col_maps = filter(lambda item: item.report_key == report_map.key, CSVDataLoader._COLUMN_MAPPING)
                
                # Enrich the report data. Add the computed columns
                computed_col_maps = filter(lambda col_map: col_map.computed, col_maps)
                for col_map in computed_col_maps:
                    LOGGER.info("Adding computed value '%s' to report '%s'", col_map.name, report_map.key)
                    for row in report_data:
                        row[col_map.name] = col_map.val_converter(row[col_map.name_in_report], row)
                
                # Apply the converter
                convert_col_maps = filter(lambda col_map: col_map.val_converter != None and not col_map.computed, col_maps)
                for col_map in convert_col_maps:
                    LOGGER.info("Applying the converter on column '%s' in report '%s'", col_map.name, report_map.key)
                    for row in report_data:
                        row[col_map.name_in_report] = col_map.val_converter(row[col_map.name_in_report], row)
                
                # Rename the columns if required
                renamed_col_maps = filter(lambda col_map: col_map.name != col_map.name_in_report and not col_map.computed, col_maps)
                for col_map in renamed_col_maps:
                    LOGGER.info("Renaming column '%s' to '%s' in report '%s'", col_map.name_in_report, col_map.name, report_map.key)
                    for row in report_data:
                        row[col_map.name] = row.pop(col_map.name_in_report)
                self.reports[date][report_map.key] = (report_info, report_data)       
        
        self._aggregate_report(CSVDataLoader.POSITION_REPORT, lambda row: row["Instrument Name"] == "")
        self._aggregate_report(CSVDataLoader.LOAN_REPORT)
        self._aggregate_report(CSVDataLoader.CASH_ANALYSIS)
        self._aggregate_report(CSVDataLoader.CFD_SWEEPING)
        
        for report_map in CSVDataLoader._REPORTS:
            se_dataset = self._get_se_dataset_from_report(report_map)
            self.se_reports[report_map.key] = se_dataset
        
        if DEBUG:
            # print self.se_reports[CSVDataLoader.PERFORMANCE_REPORT]
            for ins_name in DEBUG_INSTRUMENTS:
                LOGGER.info("\t\t%s", ins_name)
                for report_map in CSVDataLoader._REPORTS:
                    se_dataset = self.se_reports[report_map.key]
                    if se_dataset.has_row(ins_name):
                        LOGGER.info("%s: %s", report_map.key, self.se_reports[report_map.key].get_row(ins_name))
                    else:
                        LOGGER.info("%s not found", report_map.key)
    
    @classmethod
    def _init_column_maps_keys(cls):
        for report_map in cls._REPORTS:
            column_maps_keys = []
            for col_name in report_map.row_key:
                column_map = cls.get_column_mapping(col_name, report_map)
                if not column_map:
                    raise Exception("Could not identify the column mapping for the key column '{0}' in report '{1}'".format(col_name, report_map.key))
                column_maps_keys.append(column_map)
            report_map.set_column_maps_keys(column_maps_keys)
            
    @classmethod
    def get_report_mapping(cls, report_key):
        for item in cls._REPORTS:
            if item.key == report_key:
                return item
        
        raise Exception("The specified report key '{0}' could not be found".format(report_key))
           
    def _read_csv(self, file_path, ignore_rows=0):
        try:
            with open(file_path, 'rU') as csvfile:
                for _ in range(0, ignore_rows):
                    next(csvfile)
                LOGGER.info("Loaded: %s", file_path)
                return list(csv.DictReader(csvfile))
        except IOError as ex:
            message = "WARNING - report not available: {0}"
            raise SettlementControlException(message.format(ex))
    
    def _aggregate_report(self, report_key, exclude_func=None):
        """ exclude_func - takes as a parameter the row and returns true if the row has to be excluded"""
        LOGGER.info("Aggregating report %s", report_key)
        # col_map = self.get_column_mapping('Portfolio Value End', CSVDataLoader.get_report_mapping(report_key))
        rep_map = self.get_report_mapping(report_key)
        col_mappings = filter(lambda item: item.report_key == report_key, CSVDataLoader._COLUMN_MAPPING)
        report_columns = {}
        for item in col_mappings:
            report_columns[item.name] = item
        for date in self.reports.keys():
            if not self.reports[date].has_key(report_key):
                continue
            data = self.reports[date][report_key][1]
            if not data:
                continue
            result = defaultdict(lambda: defaultdict(int))
            for row in data:
                if exclude_func and exclude_func(row):
                    continue
                se_row_key = rep_map.generate_row_key(row)
#                 if se_row_key not in result.keys():
#                     result[se_row_key]={}
                for key, value in row.iteritems():
                    if key not in report_columns.keys():
                        continue
                    if report_columns[key].val_type == ColumnMapping.NUMBER:
                        value = report_columns[key].fix_value(value)
                        result[se_row_key][key] += value
                    if report_columns[key].val_type == ColumnMapping.VARCHAR:
                        result[se_row_key][key] = value
                    
            self.reports[date][report_key] = (self.reports[date][report_key][0], result.values())

    def get_all_keys(self, report_key):
        """ Returns a list of dictionaries of SEValues """        
        rep_map = self.get_report_mapping(report_key)
        key_column_map = []
        for column_map in rep_map.column_maps_keys:
            key_column_map.append(column_map)
        se_dataset = self.se_reports[report_key]
        items = se_dataset.get_values(key_column_map)
        
        return items  # filter(lambda i: i[column_map.name].end_value and i[column_map.name].end_value != '-', items)
        
    @classmethod    
    def get_column_mapping(cls, column_name, report_map):
        rep_col_maps = filter(lambda col_map: col_map.report_key == report_map.key, CSVDataLoader._COLUMN_MAPPING)
        
        col_mappings = filter(lambda col_map: col_map.name == column_name, rep_col_maps)
        
        if not col_mappings:
            LOGGER.debug("Could not find the column mapping '%s'", column_name)
            return None
        if len(col_mappings) > 1:
            raise Exception("Column mapping '{0}' not unique".format(column_name))
        
        return col_mappings[0]
    
    @classmethod    
    def get_report_column_mapping(cls, report_column_name, report_map):
        rep_col_maps = filter(lambda col_map: col_map.report_key == report_map.key, CSVDataLoader._COLUMN_MAPPING)
        
        col_mappings = filter(lambda col_map: col_map.name_in_report == report_column_name, rep_col_maps)
        
        if not col_mappings:
            LOGGER.debug("Could not find the column mapping '%s'", report_column_name)
            return None
        if len(col_mappings) > 1:
            raise Exception("Column mapping '{0}' not unique".format(report_column_name))
        
        return col_mappings[0]
        
    def _get_rows_from_report(self, date, report_map):
        """ Returns a dictionary  of dictionaries {row key:{(column name: value)}}
        """
        if not self.reports[date].has_key(report_map.key):
            return None
        report = self.reports[date][report_map.key]
        report_info = report[0]
        report_data = report[1]
        
        result = defaultdict(dict)
        for row in report_data:
            key = ""
            for col_map_key in report_map.column_maps_keys:
                if col_map_key.name not in row.keys():
                    LOGGER.info("%s", row)
                    raise Exception("The report '{0}' does not contain the column '{1}'".format(report_info.get_file_name(), col_map_key.name))
                key += "||" + str(row[col_map_key.name])
                                    
            result[key] = row 
        
        return result
    
    def _get_se_dataset_from_report(self, report_map):
        """ Returns a SEDataset
        """
        start_values = self._get_rows_from_report(self.start_date, report_map)
        end_values = self._get_rows_from_report(self.end_date, report_map)
        
        se_dataset = SEDataSet.init_from_dic(start_values, end_values, report_map)

        return se_dataset
    
    def get_value(self, column_name, se_key_value, report_key):
        """ Returns an SEValue 
            se_key_value - a dictionary that corresponds to the structure of the report key column_name:value"""
        report_map = CSVDataLoader.get_report_mapping(report_key)
        column_map = CSVDataLoader.get_column_mapping(column_name, CSVDataLoader.get_report_mapping(report_key))
        if not column_map:
            raise Exception("Column mapping for '{0}:{1}' not found".format(report_key, column_name))
        se_dataset = self.se_reports[column_map.report_key]
        
        key_value = report_map.generate_row_key(se_key_value)
        if not se_dataset.has_row(key_value) and column_map.default_value == None:
            LOGGER.info(se_dataset)
            raise Exception("Could not find the specified key '{0}' in the report '{1}'.".format(key_value, column_map.report_key))
        
        if not se_dataset.has_row(key_value) and column_map.default_value != None:
            return SEValue(column_map, column_map.default_value, column_map.default_value)
        
        value = se_dataset.get_value(column_map, key_value)
        
        return value

class BreakReportRow(object):
    
    def __init__(self, se_row_key, data_loader, report_key=CSVDataLoader.CALL_REPORT):
        self.data_loader = data_loader
        
        get_value = lambda col_name, report_key = report_key: data_loader.get_value(col_name, se_row_key, report_key)
                
        pswap_key = get_value("Portfolio Swap").get_any_value()
        if pswap_key:
            pswap = acm.FInstrument[pswap_key]
            instrument_class = pswap.AdditionalInfo().PB_Sweeping_Class()
        else:
            LOGGER.info("Unknown instrument class for key: '%s'", se_row_key) 
            instrument_class = "Unknown"
        self.ins_class = instrument_class
        
        self.client = data_loader.client
        self.financing_method = se_row_key["Financing Method"]
        self.ins_name = se_row_key["Instrument Name"]
        
        self.se_row_perf = {'Instrument Name':self.ins_name, 'Financing Method':self.financing_method}

        self.ins_type = self._get_instype(get_value)
        if not self.ins_type and self.ins_name.endswith("CFD"):
            self.ins_type = "CFD"
               
        self.tpl_movement = self._get_tpl_movement(get_value)
        self.tpl_t1 = self._get_tpl_t1(get_value)
        self.tpl_t2 = self._get_tpl_t2(get_value)
       
        self.val_end = data_loader.get_value("Closing Value End", self.se_row_perf, CSVDataLoader.PERFORMANCE_REPORT).end_value
        
        self.daily_prov = get_value("Daily Provision").end_value
        self.opening_prov_t1 = get_value("Opening Provision", CSVDataLoader.PERFORMANCE_REPORT).start_value
        self.opening_prov_t2 = get_value("Opening Provision", CSVDataLoader.PERFORMANCE_REPORT).end_value
        self.daily_fund = get_value("Daily Funding").end_value
        self.daily_ware = get_value("Daily Warehousing").end_value
        self.port_cash_end = get_value("Portfolio Cash End").end_value
                       
        self.call_acc_t1 = get_value("Cash Balance", CSVDataLoader.POSITION_REPORT).end_value
        self.call_acc_t2 = get_value("Cash Balance", CSVDataLoader.POSITION_REPORT).start_value
        self.call_movement = self._get_call_movement(get_value)
        
        if self.financing_method == "Financed":
            self.loan_movemnet = self._get_loan_movement(get_value)
            self.loan_acc_t1 = get_value("Portfolio Value End", CSVDataLoader.LOAN_REPORT).end_value
            self.loan_acc_t2 = get_value("Portfolio Value End", CSVDataLoader.LOAN_REPORT).start_value
        else:
            self.loan_movemnet = 0
            self.loan_acc_t1 = 0
            self.loan_acc_t2 = 0
        
        self.pswap = get_value("Adjustment Posting").end_value
        self.daily_financing = self._get_daily_financing(get_value)
        # Posting depends on loan movement and daily financing
        self.posting_by_loan = self._get_posting(get_value)
        self.posting = get_value("Diff").end_value
        self.adjustment_posting = get_value("Adjustment Posting").end_value
        # Status depends on other attributes
        self.staus = self._get_status()
        self.call_loan_break = self._get_client_daily_tpl(get_value) - self.loan_movemnet 
        
        self.cash_end_perf_t1 = (data_loader.get_value("Closing Cash Payments", self.se_row_perf, CSVDataLoader.PERFORMANCE_REPORT).end_value + 
                                 data_loader.get_value("Closing Cash Resets", self.se_row_perf, CSVDataLoader.PERFORMANCE_REPORT).end_value + 
                                 data_loader.get_value("Since Inception Execution Fee", self.se_row_perf, CSVDataLoader.PERFORMANCE_REPORT).end_value)
        
        if self.ins_type in ["Future/Forward", "Option"]:
            self.cash_end_perf_t1 += data_loader.get_value("Closing Value End", self.se_row_perf, CSVDataLoader.PERFORMANCE_REPORT).end_value
        
        self.cash_end_perf_t2 = (data_loader.get_value("Closing Cash Payments", self.se_row_perf, CSVDataLoader.PERFORMANCE_REPORT).start_value + 
                                 data_loader.get_value("Closing Cash Resets", self.se_row_perf, CSVDataLoader.PERFORMANCE_REPORT).start_value + 
                                 data_loader.get_value("Since Inception Execution Fee", self.se_row_perf, CSVDataLoader.PERFORMANCE_REPORT).start_value)
        
        if self.ins_type in ["Future/Forward", "Option"]:
            self.cash_end_perf_t2 += data_loader.get_value("Closing Value End", self.se_row_perf, CSVDataLoader.PERFORMANCE_REPORT).start_value
        
        self.since_ic_exec_fee_t1 = data_loader.get_value("Since Inception Execution Fee", self.se_row_perf, CSVDataLoader.PERFORMANCE_REPORT).end_value
        self.since_ic_exec_fee_t2 = data_loader.get_value("Since Inception Execution Fee", self.se_row_perf, CSVDataLoader.PERFORMANCE_REPORT).start_value
        self.since_ic_exec_fee_movement = self.since_ic_exec_fee_t1 - self.since_ic_exec_fee_t2
        
        self.cash_end_perf_movement = self.cash_end_perf_t1 - self.cash_end_perf_t2
        
        self.cash_end_t1 = self.cash_end_perf_t1
        self.cash_end_t2 = self.cash_end_perf_t2
        self.cash_end_movement = self.cash_end_perf_movement
        
        
        self.inception_tpl_t1 = data_loader.get_value("Inception TPL", self.se_row_perf, CSVDataLoader.PERFORMANCE_REPORT).end_value
        self.inception_tpl_t2 = data_loader.get_value("Inception TPL", self.se_row_perf, CSVDataLoader.PERFORMANCE_REPORT).start_value 
        if self.financing_method == "Financed":
            self.posting_break = self.inception_tpl_t1 - self.inception_tpl_t2 - self.posting
        else:
            # for fully funded we use the closing cash payments, cash resets, inception exec fee)
            self.posting_break = self.cash_end_perf_t1 - self.cash_end_perf_t2 - self.posting
            
    def _get_status(self):
        if self.tpl_movement == self.call_movement or self.loan_movemnet == self.pswap:
            return "OK"
        if (self.tpl_movement == self.call_movement or self.loan_movemnet and\
            self.call_movement or self.loan_movemnet != self.pswap):
            return "Pswap Break"
        if (self.call_movement or self.loan_movemnet != self.pswap and\
            self.call_movement or self.loan_movemnet != self.tpl_movement):
            return "TPL BReak"
        if (self.tpl_movement == self.pswap and\
            self.tpl_movement != self.call_movement or self.loan_movemnet):
            return "Call Break"
        if (self.tpl_movement != self.pswap and\
            self.tpl_movement != self.call_movement or self.loan_movemnet and\
            self.call_movement or self.loan_movemnet != self.pswap):
            return "Break All"
        
        return "Not defined"
        
    def _get_tpl_movement(self, get_value):
        return self._get_tpl_t1(get_value) - self._get_tpl_t2(get_value)
    
    def _get_tpl_t1(self, get_value):
        return get_value("Client TPL").end_value + get_value("Portfolio Value End", CSVDataLoader.LOAN_REPORT).end_value
    
    def _get_tpl_t2(self, get_value):
        return get_value("Client TPL").start_value + get_value("Portfolio Value End", CSVDataLoader.LOAN_REPORT).start_value
    
    def _get_loan_movement(self, get_value):
        return get_value("Portfolio Value End", CSVDataLoader.LOAN_REPORT).end_value - get_value("Portfolio Value End", CSVDataLoader.LOAN_REPORT).start_value 
    
    def _get_call_movement(self, get_value):
        return self.call_acc_t1 - self.call_acc_t2
    
    def _get_daily_financing(self, get_value):
        return (get_value("Daily Provision").end_value + 
                get_value("Daily Funding").end_value + 
                get_value("Daily Warehousing").end_value + 
                get_value("Portfolio Cash End").end_value)
    
    def _get_posting(self, get_value):
        return self.loan_movemnet + self.daily_financing 
    
    def _get_client_daily_tpl(self, get_value):
        return get_value("Client TPL").end_value - get_value("Client TPL").start_value
    
    def _get_instype(self, get_value):
        return get_value("Instrument Type").get_any_value()
    
    def to_list(self):
        return [self.client, self.financing_method, self.ins_class, self.ins_type, self.ins_name,
        self.staus, self.tpl_movement, self.tpl_t1, self.tpl_t2,
        self.cash_end_movement, self.cash_end_t1, self.cash_end_t2,
        # self.cash_end_perf_movement, self.cash_end_perf_t1, self.cash_end_perf_t2,
        self.val_end, self.daily_prov, self.daily_fund, self.daily_ware,
        self.call_movement, self.call_acc_t1, self.call_acc_t2,
        self.loan_movemnet, self.loan_acc_t1, self.loan_acc_t2,
        self.pswap,
        self.daily_financing,
        self.posting_by_loan,
        self.call_loan_break,
        self.since_ic_exec_fee_movement, self.since_ic_exec_fee_t1, self.since_ic_exec_fee_t2, self.posting,
        self.inception_tpl_t1, self.inception_tpl_t2, self.posting_break]
    
class MovementReportRow(BreakReportRow):    
    
    def __init__(self, se_row_key, data_loader):
        super(MovementReportRow, self).__init__(se_row_key, data_loader)
        
        # the CashAnalysis is a 'special' report. We don't need to look at the prev day report. The Last report contains the most recent values, 
        # for the full period. As a result, need just to select by the correct cashflow date.
        se_row_key_cash_analysis_t1 = {'PSwap Instrument Type':self.ins_type, 'Pay Date':data_loader.end_date}
        self.sweept_amount_t1 = data_loader.get_value('Projected Cash', se_row_key_cash_analysis_t1, CSVDataLoader.CASH_ANALYSIS).end_value
        se_row_key_cash_analysis_t2 = {'PSwap Instrument Type':self.ins_type, 'Pay Date':data_loader.start_date}
        self.sweept_amount_t2 = data_loader.get_value('Projected Cash', se_row_key_cash_analysis_t2, CSVDataLoader.CASH_ANALYSIS).end_value

class MovementReportRow2(BreakReportRow):    
    
    def __init__(self, ins_type, data_loader):
        
        # the CashAnalysis is a 'special' report. We don't need to look at the prev day report. The Last report contains the most recent values, 
        # for the full period. As a result, need just to select by the correct cashflow date.
        se_row_key_cash_analysis_t1 = {'PSwap Instrument Type':ins_type, 'Pay Date':data_loader.end_date}
        self.sweept_amount_t1 = data_loader.get_value('Projected Cash', se_row_key_cash_analysis_t1, CSVDataLoader.CASH_ANALYSIS).end_value
        se_row_key_cash_analysis_t2 = {'PSwap Instrument Type':ins_type, 'Pay Date':data_loader.start_date}
        self.sweept_amount_t2 = data_loader.get_value('Projected Cash', se_row_key_cash_analysis_t2, CSVDataLoader.CASH_ANALYSIS).end_value

class BreakCFDReportRow(object):
    
    def __init__(self, se_row_key, data_loader, report_key=CSVDataLoader.CFD_SWEEPING):
        self.data_loader = data_loader
        self.client = data_loader.client
        
        self.ins_name = se_row_key["Instrument Name"]
        self.financing_method = se_row_key["Financing Method"]
        se_row_key = {'Instrument':self.ins_name, 'Date':data_loader.end_date}
        get_value = lambda col_name, report_key = report_key: data_loader.get_value(col_name, se_row_key, report_key)
        
        self.ins_type = get_value("Instrument Type").end_value
        
        self.short_premium_t1 = get_value('Short Premium').end_value
        self.mtm_t1 = get_value('Mtm').end_value
        self.overnight_premium_t1 = get_value('Overnight Premium').end_value
        self.execution_premium_t1 = get_value('Execution Premium').end_value
        self.dividend_t1 = get_value('Dividend').end_value
        
        self.tpl_t1 = self.short_premium_t1 + self.mtm_t1 + self.overnight_premium_t1 + self.execution_premium_t1 + self.dividend_t1
        
        se_row_key = {'Instrument':self.ins_name, 'Date':data_loader.start_date}
        get_value = lambda col_name, report_key = report_key: data_loader.get_value(col_name, se_row_key, report_key)
        
        self.short_premium_t2 = get_value('Short Premium').end_value
        self.mtm_t2 = get_value('Mtm').end_value
        self.overnight_premium_t2 = get_value('Overnight Premium').end_value
        self.execution_premium_t2 = get_value('Execution Premium').end_value
        self.dividend_t2 = get_value('Dividend').end_value
        
        self.tpl_t2 = self.short_premium_t2 + self.mtm_t2 + self.overnight_premium_t2 + self.execution_premium_t2 + self.dividend_t2
        
        
        self.se_row_perf = {'Instrument Name':self.ins_name, 'Financing Method':self.financing_method}
        self.cash_end_perf_t1 = (data_loader.get_value("Closing Cash Payments", self.se_row_perf, CSVDataLoader.PERFORMANCE_REPORT).end_value + 
                                 data_loader.get_value("Closing Cash Resets", self.se_row_perf, CSVDataLoader.PERFORMANCE_REPORT).end_value + 
                                 data_loader.get_value("Since Inception Execution Fee", self.se_row_perf, CSVDataLoader.PERFORMANCE_REPORT).end_value)
        self.daily_tpl_t1 = data_loader.get_value("Daily TPL", self.se_row_perf, CSVDataLoader.PERFORMANCE_REPORT).end_value
        self.daily_tpl_t2 = data_loader.get_value("Daily TPL", self.se_row_perf, CSVDataLoader.PERFORMANCE_REPORT).start_value
        
        
        se_row_key_cash_analysis_t1 = {'PSwap Instrument Type':self.ins_type, 'Pay Date':data_loader.end_date}
        self.sweept_amount_t1 = data_loader.get_value('Projected Cash', se_row_key_cash_analysis_t1, CSVDataLoader.CASH_ANALYSIS).end_value
        se_row_key_cash_analysis_t2 = {'PSwap Instrument Type':self.ins_type, 'Pay Date':data_loader.start_date}
        self.sweept_amount_t2 = data_loader.get_value('Projected Cash', se_row_key_cash_analysis_t2, CSVDataLoader.CASH_ANALYSIS).end_value
        
    def to_list(self):
        return [self.client, self.ins_name, self.ins_type, self.financing_method,
                self.short_premium_t1, self.mtm_t1, self.overnight_premium_t1, self.execution_premium_t1, self.dividend_t1,
                self.tpl_t1, self.cash_end_perf_t1, self.sweept_amount_t1, self.sweept_amount_t2, self.daily_tpl_t1, self.daily_tpl_t2]
        
class BreakReport(CSVReportCreator):
    
    def __init__(self, input_path, full_file_path, data_loaders):
        file_name = os.path.basename(full_file_path)
        file_name_only = os.path.splitext(file_name)[0]
        file_suffix = os.path.splitext(file_name)[1][1:]
        file_path = os.path.dirname(full_file_path)

        self.input_path = input_path
        
        self.data_loaders = data_loaders

        super(BreakReport, self).__init__(file_name_only,
                                          file_suffix,
                                          file_path)
    
    def _get_all_keys(self, data_loader):
        keys_perf = data_loader.get_all_keys(CSVDataLoader.PERFORMANCE_REPORT)  # 'Instrument', 'Financing Method'
        keys_call = data_loader.get_all_keys(CSVDataLoader.CALL_REPORT)
        keys_perf.extend(keys_call)
        
        result = {}
        for item_key in keys_perf:
            key = "{0}||{1}".format(item_key["Instrument Name"].get_any_value(), item_key["Financing Method"].get_any_value())
            result[key] = item_key

        return result.values()
    
    def _collect_data(self):
        """Collect PnL and cash movement data."""
        for data_loader in self.data_loaders:
            LOGGER.info("%s", data_loader.client)
            inst_port_swap = self._get_all_keys(data_loader)
#             print "*"*40
#             print data_loader.se_reports[CSVDataLoader.CALL_REPORT]
#             print "*"*40
            for item_key in inst_port_swap:
                instrument_name = item_key["Instrument Name"].get_any_value()
                if instrument_name == "" or instrument_name == "-":
                    continue
                financing_method = item_key["Financing Method"].get_any_value()
                if instrument_name:
                    # LOGGER.info("%s; %s", instrument_name, financing_method)
                    se_row_key = {"Instrument Name": instrument_name, "Financing Method": financing_method}
                    break_report_row = BreakReportRow(se_row_key, data_loader)
                    
                    if break_report_row.ins_type == "CFD":
                        continue
                    
                    if break_report_row.staus != 'OK' or SHOW_NO_BREAK: 
                        self.content.append(break_report_row.to_list())
                # self._collect_instrument_data(ins_name, data_loader)
        
    def _header(self):
        """Return columns of the header."""
        header = [
            "Client",
            "Financed Flag",
            "Instrument Class",
            "Instrument Type",
            "Instrument Name",
            "Status",
            "TPL Movement", "TPL T-1", "TPL T-2",
            "Cash End Movement", "Cash End T1", "Cash End T2",
            "Val End",
            "Short End Provision",
            "Daily Funding",
            "Daily Warehousing",
            "Call Movement", "Call Acc T-1", "Call Acc T-2",
            "Loan Movement", "Loan Acc T-1", "Loan Acc T-2",
            "Pswap Value",
            "Daily Financing",
            "CallLoan Posting",
            "CallLoan Movement Break",
            "Since Inc Exec Fee Movement", "Since Inc Exec Fee T1", "Since Inc Exec Fee T2", "Posting",
            "Inception TPL T1", "Inception TPL T2", "Posting Break"
        ]
        
        return header

class MovementReport(BreakReport):
    
    def __init__(self, input_path, full_file_path, data_loaders):
        super(MovementReport, self).__init__(input_path, full_file_path, data_loaders)
    
    def _collect_data(self):
        """Collect PnL and cash movement data."""
        lines = []
        for data_loader in self.data_loaders:
            inst_port_swap = self._get_all_keys(data_loader)

            for item_key in inst_port_swap:
                instrument_name = item_key["Instrument Name"].get_any_value()
                if instrument_name == "" or instrument_name == "-":
                    continue
                financing_method = item_key["Financing Method"].get_any_value()
                if instrument_name:
                    # LOGGER.info("%s; %s", instrument_name, financing_method)
                    se_row_key = {"Instrument Name": instrument_name, "Financing Method": financing_method}
                    report_row = MovementReportRow(se_row_key, data_loader)
                    
                    if report_row.ins_type == "CFD":
                        continue
                    
                    lines.append(report_row)
            
        lines_ins_type = {}
        for data_loader in self.data_loaders:
            lines_client_ins_type = {}
            inst_port_swap = data_loader.get_all_keys(CSVDataLoader.CASH_ANALYSIS)  # 'PSwap Instrument Type', 'Pay Date'
            for item_key in inst_port_swap:
                # we want to select only the latest cash flows
                if item_key["Pay Date"].get_any_value() != data_loader.end_date:
                    continue
                ins_type = item_key["PSwap Instrument Type"].get_any_value()
                if ins_type == "" or ins_type == "-":
                    continue
                report_row = MovementReportRow2(ins_type, data_loader)
                if lines_client_ins_type.has_key(ins_type):
                    LOGGER.info("The instrument type '%s' was already processed", ins_type)
                lines_client_ins_type[ins_type] = report_row
            
            lines_ins_type[data_loader.client] = lines_client_ins_type
         
        for client in set(map(lambda item: item.client, lines)):
            lines_by_client = filter(lambda item: item.client == client, lines)
            call_acc_ins_types = lines_ins_type[client].keys()
            ins_types = list(set(map(lambda item: item.ins_type, lines_by_client)))
            ins_types.extend(call_acc_ins_types)
            ins_types = set(ins_types)
            for ins_type in ins_types:
                if ins_type == "CFD":
                    continue
                lines_by_ins_type = filter(lambda item: item.ins_type == ins_type, lines_by_client)
                tpl_movement = tpl_t1 = tpl_t2 = 0
                call_movement = 0
                posting = 0
                cash_movement = cash_t1 = cash_t2 = 0;
                loan_movemnet = loan_acc_t1 = loan_acc_t2 = 0
                inception_tpl_t1 = inception_tpl_t2 = posting_break = 0
                opening_prov_t1 = opening_prov_t2 = 0
                # cash_end_perf_movement = cash_end_perf_t1 = cash_end_perf_t2 = 0
                since_ic_exec_fee_movement = since_ic_exec_fee_t1 = since_ic_exec_fee_t2 = 0
                sweept_t1 = sweept_t2 = 0
                if lines_ins_type[client].has_key(ins_type):
                    sweept_t1 = lines_ins_type[client][ins_type].sweept_amount_t1
                    sweept_t2 = lines_ins_type[client][ins_type].sweept_amount_t2
                for line in lines_by_ins_type:
                    tpl_movement += line.tpl_movement
                    tpl_t1 += line.tpl_t1
                    tpl_t2 += line.tpl_t2
                    call_movement += line.call_movement
                    posting += line.posting
                    cash_movement += line.cash_end_movement;
                    cash_t1 += line.cash_end_t1
                    cash_t2 += line.cash_end_t2
                    loan_movemnet += line.loan_movemnet
                    loan_acc_t1 += line.loan_acc_t1
                    loan_acc_t2 += line.loan_acc_t2
                    since_ic_exec_fee_movement += line.since_ic_exec_fee_movement
                    since_ic_exec_fee_t1 += line.since_ic_exec_fee_t1
                    since_ic_exec_fee_t2 += line.since_ic_exec_fee_t2
                    inception_tpl_t1 += line.inception_tpl_t1
                    inception_tpl_t2 += line.inception_tpl_t2
                    posting_break += line.posting_break
                    opening_prov_t1 += line.opening_prov_t1
                    opening_prov_t2 += line.opening_prov_t2
#                     cash_esnd_perf_t1 += line.cash_end_perf_t1
#                     cash_end_perf_t2 += line.cash_end_perf_t2
#                     cash_end_perf_movement += line.cash_end_perf_movement
                
                                                
                line = [client, ins_type,
                        # tpl_movement, tpl_t1, tpl_t2, call_movement,
                        sweept_t1, sweept_t2, posting, sweept_t1 - posting,
                        cash_movement, cash_t1, cash_t2,
                        # cash_end_perf_movement, cash_end_perf_t1, cash_end_perf_t2,
                        loan_movemnet, loan_acc_t1, loan_acc_t2,
                        since_ic_exec_fee_movement, since_ic_exec_fee_t1, since_ic_exec_fee_t2,
                        inception_tpl_t1, inception_tpl_t2, posting_break,
                        opening_prov_t1, opening_prov_t2
                        ]
                
                self.content.append(line)  
        
    def _header(self):
        """Return columns of the header."""
        header = [
            "Client",
            "Instrument Type",
#           "TPL Movement", "TPL T-1", TPL T-2", "Call Movement",
            "SweepT1", "SweepT2", "Posting", "PostingVsSweepT1",
            "Cash End Movement", "Cash End T1", "Cash End T2",
            # "Cash End T1 Perf",
            "Loan Movement", "Loan Acc T-1", "Loan Acc T-2",
            "Since Inc Exec Fee Movement", "Since Inc Exec Fee T1", "Since Inc Exec Fee T2",
            "Inception TPL T1", "Inception TPL T2", "Posting Break",
            "Short End Provision T1", "Short End Provision T2"
        ]
        
        return header

class BreakCFDReport(BreakReport):
    
    def __init__(self, input_path, full_file_path, data_loaders):
        super(BreakCFDReport, self).__init__(input_path, full_file_path, data_loaders)
    
    def _collect_data(self):
        """Collect PnL and cash movement data."""
        lines = []
        for data_loader in self.data_loaders:
            inst_port_swap = self._get_all_keys(data_loader)
            
            for item_key in inst_port_swap:
                instrument_name = item_key["Instrument Name"].get_any_value()
                if instrument_name == "" or instrument_name == "-":
                    continue
                financing_method = item_key["Financing Method"].end_value
                # LOGGER.info("%s; %s", instrument_name, financing_method)
                se_row_key = {"Instrument Name": instrument_name, "Financing Method": financing_method}
                report_row = BreakCFDReportRow(se_row_key, data_loader)
                lines.append(report_row)
                # self._collect_instrument_data(ins_name, data_loader)
        
        for line in lines:
            if line.ins_type != "CFD":
                continue                
            self.content.append(line.to_list())  
        
    def _header(self):
        """Return columns of the header."""
        header = [
            "Client", "Instrument Name", "Instrument Type", "Financed Method",
            "Short Premium T1", "MTM T1", "Overnight Premium T1", "Execution Premium T1", "Dividend T1", "TPL T1", "Cash End Perf T1",
            "SweepT1", "SweepT2", "Daily TPL Perf T2", "TPL & TPL Perf T1"
        ]
        
        return header

class MovementCFDReport(BreakReport):
    
    def __init__(self, input_path, full_file_path, data_loaders):
        super(MovementCFDReport, self).__init__(input_path, full_file_path, data_loaders)
    
    def _get_all_keys(self, data_loader):
        inst_port_swap = super(MovementCFDReport, self)._get_all_keys(data_loader)
        
        instruments = map(lambda i:i["Instrument Name"].end_value, inst_port_swap)
            
        cfd_sweeping = data_loader.get_all_keys(CSVDataLoader.CFD_SWEEPING)
        col_map_ins = CSVDataLoader.get_column_mapping("Instrument Name", CSVDataLoader.get_report_mapping(CSVDataLoader.PERFORMANCE_REPORT))
        col_map_fin_meth = CSVDataLoader.get_column_mapping("Financing Method", CSVDataLoader.get_report_mapping(CSVDataLoader.PERFORMANCE_REPORT))
        for item in cfd_sweeping:
            if item['Instrument'].end_value and item['Instrument'].end_value not in instruments:
                LOGGER.info("Adding missing instrument '%s'", item['Instrument'].end_value)
                se_ins_name = SEValue(col_map_ins, item['Instrument'].start_value, item['Instrument'].end_value)
                se_fin_meth = SEValue(col_map_fin_meth, "Financed", "Financed")
                inst_port_swap.append({"Instrument Name":se_ins_name, "Financing Method":se_fin_meth})
                instruments.append(item['Instrument'].end_value)
                
        return inst_port_swap
        
    def _collect_data(self):
        """Collect PnL and cash movement data."""
        lines = []
        for data_loader in self.data_loaders:
            inst_port_swap = self._get_all_keys(data_loader)  # 'Instrument', 'Financing Method'
            
            for item_key in inst_port_swap:
                instrument_name = item_key["Instrument Name"].get_any_value()
                if instrument_name == "" or instrument_name == "-":
                    continue
                financing_method = item_key["Financing Method"].get_any_value()
                if instrument_name:
                    # LOGGER.info("%s; %s", instrument_name, financing_method)
                    se_row_key = {"Instrument Name": instrument_name, "Financing Method": financing_method}
                    report_row = BreakCFDReportRow(se_row_key, data_loader)
                    lines.append(report_row)
                # self._collect_instrument_data(ins_name, data_loader)
        
        for client in set(map(lambda item: item.client, lines)):
            lines_by_client = filter(lambda item: item.client == client, lines)
            for ins_type in set(map(lambda item: item.ins_type, lines_by_client)):
                if ins_type != "CFD":
                    continue
                lines_by_ins_type = filter(lambda item: item.ins_type == ins_type, lines_by_client)
                tpl_t1 = tpl_t2 = 0
                sweept_t1 = sweept_t2 = 0
                cash_end_perf_t1 = 0
                daily_tpl_t1 = daily_tpl_t2 = 0
                for line in lines_by_ins_type:
                    tpl_t1 += line.tpl_t1
                    tpl_t2 += line.tpl_t2
                    daily_tpl_t1 += line.daily_tpl_t1
                    daily_tpl_t2 += line.daily_tpl_t2
                    sweept_t1 = line.sweept_amount_t1
                    sweept_t2 = line.sweept_amount_t2
#                    posting += line.posting
                    cash_end_perf_t1 += line.cash_end_perf_t1
                                                        
                line = [client, ins_type, tpl_t1, tpl_t2, cash_end_perf_t1, sweept_t1, sweept_t2,
                        tpl_t1 + sweept_t1, tpl_t2 + sweept_t2,
                        daily_tpl_t1, daily_tpl_t2, tpl_t1 + daily_tpl_t1, tpl_t2 + daily_tpl_t2,
                        ]
                
                self.content.append(line) 
        
    def _header(self):
        """Return columns of the header."""
        header = ["Client", "Instrument Type", "TPL T1", "TPL T2", "Cash End Perf T1", "SweepT1", "SweepT2",
                  "TPL & Sweep T1", "TPL & Sweep T2",
                  "Daily TPL Perf T1", "Daily TPL Perf T2", "TPL & TPL Perf T1", "TPL & TPL Perf T2", ]
        return header
                
    
START_DATES = DateField.get_captions([
    'Inception',
    'First Of Year',
    'First Of Month',
    'Last of Previous Month',
    'TwoBusinessDaysAgo',
    'PrevBusDay',
    'Custom Date'])

END_DATES = DateField.get_captions([
    'Now',
    'PrevBusDay',
    'Custom Date'])       
    

def custom_start_date_hook(selected_variable):
    """Enable/Disable Custom Start Date base on Start Date value."""
    start_date = ael_variables.get('start_date')
    start_date_custom = ael_variables.get('start_date_custom')

    if start_date.value == 'Custom Date':
        start_date_custom.enabled = True
    else:
        start_date_custom.enabled = False


def custom_end_date_hook(selected_variable):
    """Enable/Disable Custom End Date base on End Date value."""
    end_date = ael_variables.get('end_date')
    end_date_custom = ael_variables.get('end_date_custom')

    if end_date.value == 'Custom Date':
        end_date_custom.enabled = True
    else:
        end_date_custom.enabled = False
        
        # load for every client the REPORTS
ael_variables = AelVariableHandler()
ael_variables.add('start_date',
                  label='Start Date (relative to End Date)',
                  default='PrevBusDay',
                  collection=START_DATES,
                  alt='Start date'
                      '(relative to the end date)',
                  hook=custom_start_date_hook)

ael_variables.add('start_date_custom',
                  label='Start Date Custom',
                  default=DateField.read_date('TwoBusinessDaysAgo'),
                  alt='Custom start date',
                  enabled=False)

ael_variables.add('end_date',
                  label='End Date',
                  default='PrevBusDay',
                  collection=END_DATES,
                  alt='End date',
                  hook=custom_end_date_hook)

ael_variables.add('end_date_custom',
                  label='End Date Custom',
                  default=DateField.read_date('PrevBusDay'),
                  alt='Custom end date',
                  enabled=False)
ael_variables.add("input_path",
                  label="Input path",
                  mandatory=True)  
ael_variables.add("break_report_filename",
                  label="Break Report Filename",
                  mandatory=True)  
ael_variables.add("movement_report_filename",
                  label="Movement Report Filename",
                  mandatory=True) 
ael_variables.add("cfd_break_report_filename",
                  label="CFD Break Report Filename",
                  mandatory=True) 
ael_variables.add("cfd_movement_report_filename",
                  label="CFD Movement Report Filename",
                  mandatory=True)        

def ael_main(config):
    """Entry point of the script."""
    
    with bp_start("pb_settlement_control", ael_main_args=config):
        if config['end_date'] == 'Custom Date':
                end_date = config['end_date_custom']
        else:
            end_date = DateField.read_date(config['end_date'])
    
        if config['start_date'] == 'Custom Date':
            start_date = config['start_date_custom']
        else:
            start_date = DateField.read_date(config['start_date'], end_date)
    
        input_path = config["input_path"]
        if not input_path:
            input_path = DEFAULT_DIR
        break_report_filename = "{0}_{1}.csv".format(config["break_report_filename"], end_date)
        cfd_break_report_filename = "{0}_{1}.csv".format(config["cfd_break_report_filename"], end_date)
        movement_report_filename = "{0}_{1}.csv".format(config["movement_report_filename"] , end_date)
        cfd_movement_report_filename = "{0}_{1}.csv".format(config["cfd_movement_report_filename"] , end_date)
    
        # Create break report
        try:
            
            data_loaders = []
            
            LOGGER.info("Loading CSVs ...")
            for counterparty in get_pb_fund_counterparties():
                shortname = get_pb_fund_shortname(counterparty)
                if DEBUG and DEBUG_CLIENTS and not shortname in DEBUG_CLIENTS:
                    LOGGER.info("Client '%s' ignored (debug mode)", shortname)
                    continue
                data_loaders.append(CSVDataLoader(counterparty, start_date, end_date, input_path))
            LOGGER.info("All CSVs loaded")
            
            break_report = BreakReport(input_path, break_report_filename, data_loaders)
            break_report.create_report()
            
            cfd_break_report = BreakCFDReport(input_path, cfd_break_report_filename, data_loaders)
            cfd_break_report.create_report()
            
            movement_report = MovementReport(input_path, movement_report_filename, data_loaders)
            movement_report.create_report()
            
            cfd_movement_report = MovementCFDReport(input_path, cfd_movement_report_filename, data_loaders)
            cfd_movement_report.create_report()
            
            LOGGER.output(break_report_filename)
            LOGGER.output(cfd_break_report_filename)
            LOGGER.output(movement_report_filename)
            LOGGER.output(cfd_movement_report_filename)
            
            LOGGER.info("Completed Successfully")
        except SettlementControlException:
            LOGGER.exception("Generation of Settlement Control report FAILED.")