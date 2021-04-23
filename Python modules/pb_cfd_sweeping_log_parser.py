'''
Created on 16 Feb 2016

@author: conicova
'''

import os
import re
import ael
from at_report import CSVReportCreator
from collections import defaultdict
from at_ael_variables import AelVariableHandler
from PS_FormUtils import DateField

DELIMITER = " "
DEFAULT_DIR = r"Y:\Jhb\FAReports\AtlasEndOfDay\SweepingLogs"
OUTPUT_DIRECTORY = r"C:\tmp\sett_control\CFD"

class LineItems(object):
    
    def __init__(self, value, inst_name, value_type):
        self.value = value
        self.inst_name = inst_name
        self.value_type = value_type.replace("\n", "")
    
    @staticmethod
    def is_data_line(line):
        if line.startswith("\t"):
            return True
        return False
    
    @staticmethod
    def parse_line(line):
        """ returns a list of items """
        components = line.split(DELIMITER)
        if len(components) < 3:
            raise Exception("Unexpected line structure: '{0}'".format(line))
        
        return LineItems(components[0].strip(), components[1], " ".join(components[2:]))
    
    def __str__(self, *args, **kwargs):
        return "{0};{1};{2};{3}".format(self.value, self.inst_name, self.value_type, self.total_line_item.date)

class TotalLineItem(object):
    
    _REG_EXP = "^([A-Za-z0-9_]+) ([0-9-]+) ([A-Za-z ]+): ([-0-9\.]+)"
    def __init__(self, portfolio, date, value_type, value, data_lines):
        self.portfolio = portfolio
        self.date = date
        self.value_type = value_type
        self.value = value
        self.data_lines = data_lines
        
        self.test_data = 0
        for data_line in data_lines:
            self.test_data += float(data_line.value)
    
    @staticmethod
    def is_total_line(line):
        if not line.startswith("\t"):
            data = re.findall(TotalLineItem._REG_EXP, line)
            if len(data) == 1 and len(data[0]) == 4:
                return True
        return False
    
    @staticmethod
    def parse_line(line, data_lines):
        """ returns a list of items """
        data = re.findall(TotalLineItem._REG_EXP, line)[0]
        
        return TotalLineItem(data[0], data[1], data[2], data[3], data_lines)
    
    def __str__(self, *args, **kwargs):
        return "{0};{1};{2};{3};{4};".format(self.portfolio, self.date, self.value_type, self.value, self.test_data)
    
# PB_MAP_111_CFD 2016-02-09 TPL total: 1354120.32285
    
class LogFileInfo(object):
    
    def __init__(self, shortname, date, file_name):
        self.shortname = shortname
        self.date = date
        self.file_name = file_name
        
    def __str__(self, *args, **kwargs):
        return "{0:20}\t{1}\t{2}".format(self.shortname, self.date, self.file_name)
    
    @staticmethod
    def get_log_file_infos(date, input_dir):
        log_files = LogFileInfo._get_logs(date, input_dir)
        
        result = []
        for file_name in log_files:
            result.append(LogFileInfo._init_from_file_name(file_name))
    
        return result
    
    @staticmethod
    def _init_from_file_name(file_name):
        # ats_task.PS_Sweeping_TOWSIT_SERVER_20160215_212837.log
        shortname = re.findall("ats_task.PS_Sweeping_([A-Za-z0-9_]+)_SERVER", file_name)
        if len(shortname) != 1:
            raise Exception("Could not parse the client name: '{0}'".format(file_name))
        
        shortname = shortname[0]
        
        date = re.findall(".*_SERVER_([0-9]+)_", file_name)
        if len(date) != 1:
            raise Exception("Could not parse the report date: '{0}'".format(file_name))
        
        date = date[0]
        
        return LogFileInfo(shortname, date, file_name)
        
    @staticmethod
    def _get_logs(date, input_dir):       
        # Y:\Jhb\FAReports\AtlasEndOfDay\SweepingLogs\2016-02-15
        log_dir = os.path.join(input_dir, date)
        
        if not os.path.isdir(log_dir):
            print("Could not find the log dir for date '{0}'".format(date))
            return []
        
        files = os.listdir(log_dir)
        log_files = filter(lambda f: f.startswith("ats_task.PS_Sweeping_"), files)
        # log_files = map(lambda f: os.path.split(f[-1]), log_files)
        
        return log_files

def _read_file(date, file_info, input_dir):
    
    result_totals = []
    # Y:\Jhb\FAReports\AtlasEndOfDay\SweepingLogs\2016-02-15\ats_task.PS_Sweeping_TOWSIT_SERVER_20160215_212837.log
    file_path = os.path.join(input_dir, date, file_info.file_name)
    prev_total_line_item = None
    with open(file_path, "rb") as f:
        result = []
        line = f.readline()
        while line != '':
            
            if LineItems.is_data_line(line):
                result.append(LineItems.parse_line(line))
            if TotalLineItem.is_total_line(line):
                prev_total_line_item = TotalLineItem.parse_line(line, result)
                result_totals.append(prev_total_line_item)
                result = []
            
            line = f.readline()
        
    return result_totals

class CFDSweepingReport(CSVReportCreator):
    
    def __init__(self, input_path, full_file_path, total_lines):
        file_name = os.path.basename(full_file_path)
        file_name_only = os.path.splitext(file_name)[0]
        file_suffix = os.path.splitext(file_name)[1][1:]
        file_path = os.path.dirname(full_file_path)

        self.input_path = input_path
        
        self.total_lines = total_lines

        super(CFDSweepingReport, self).__init__(file_name_only,
                                          file_suffix,
                                          file_path)
    
    def _collect_data(self):
        """Collect PnL and cash movement data."""
        rows = defaultdict(lambda: defaultdict(float))
        for total_line in self.total_lines:
            for data_line in total_line.data_lines:
                key = "{0}|{1}|{2}|".format(total_line.portfolio, total_line.date, data_line.inst_name)
                rows[key]["Instrument"] = data_line.inst_name + "/CFD"
                rows[key]["Portfolio"] = total_line.portfolio
                rows[key]["Date"] = total_line.date
                rows[key][data_line.value_type] += float(data_line.value)
                rows[key]["Instrument Type"] = "CFD"
                if data_line.value_type not in CFDSweepingReport.HEADER:
                    print("Got something new '{0}'".format(data_line.value_type))
        
        for key in rows.keys():
            line = []
            for header_column in CFDSweepingReport.HEADER:
                line.append(rows[key][header_column])
            self.content.append(line)
    
    HEADER = ["Portfolio", "Date", "Instrument", "Instrument Type", "Short Premium", "Mtm", "Overnight Premium", "Execution Premium", "Dividend"]
                
    def _header(self):
        return CFDSweepingReport.HEADER


def _generate(date, input_dir, output_dir, output_filename):
    """
    date - ael date
    """
    files = LogFileInfo.get_log_file_infos(date.to_string("%Y-%m-%d"), input_dir)
    result = []
    for file_info in files:
        print(file_info)
        total_lines = _read_file(date.to_string("%Y-%m-%d"), file_info, input_dir)
        input_path = os.path.join(output_dir, file_info.shortname, date.to_string("%Y-%m-%d"))
        if not os.path.exists(input_path):
            os.makedirs(input_path)
        report_file_path = os.path.join(input_path, "{0}_{2}_{1}.csv".format(file_info.shortname, date.to_string("%Y%m%d"), output_filename))
        
        report = CFDSweepingReport(input_path, report_file_path, total_lines)
        report.create_report()
        result.append("Secondary output wrote to {0}".format(report_file_path))
    
    return result

START_DATES = DateField.get_captions([
    'Inception',
    'First Of Year',
    'First Of Month',
    'Last of Previous Month',
    'TwoBusinessDaysAgo',
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

ael_variables = AelVariableHandler()
ael_variables.add('start_date',
                  label='Date',
                  default='PrevBusDay',
                  collection=START_DATES,
                  alt='Start date',
                  hook=custom_start_date_hook)

ael_variables.add('start_date_custom',
                  label='Start Date Custom',
                  default=DateField.read_date('TwoBusinessDaysAgo'),
                  alt='Custom start date',
                  enabled=False)
ael_variables.add("input_dir",
                  label="Input dir",
                  default=DEFAULT_DIR,
                  mandatory=True)
ael_variables.add("output_dir",
                  label="Output dir",
                  default=OUTPUT_DIRECTORY,
                  mandatory=True)
ael_variables.add("output_filename",
                  label="Output Filename",
                  default="CFD_Sweeping",
                  mandatory=True)

def ael_main(config):
    """Entry point of the script."""
    if config['start_date'] == 'Custom Date':
        start_date = ael.date(config['start_date_custom'])
    else:
        start_date = ael.date(DateField.read_date(config['start_date']))
    
    if not os.path.exists(config["output_dir"]):
        os.mkdir(config["output_dir"])
    
    result = _generate(start_date, config["input_dir"], config["output_dir"], config["output_filename"])
    
    print("\n".join(result))
    print("Completed Successfully")


