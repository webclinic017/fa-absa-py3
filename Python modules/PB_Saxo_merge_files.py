"""-----------------------------------------------------------------------
MODULE
    PB_Saxo_merge_files

DESCRIPTION
    Date                : 2016-11-08
    Purpose             : Create one report from Saxo TradesExecuted reports.
    Department and Desk : Prime Services
    Requester           : Eveshnee Naidoo
    Developer           : Ondrej Bahounek
    CR Number           : 4078305

HISTORY
===============================================================================
Date       Change no    Developer          Description
-------------------------------------------------------------------------------
2016-11-08 4078305      Ondrej Bahounek    Merge all files into one report.
                                           Add common columns first,
                                           sort rest alphabetically.
----------------------------------------------------------------------------"""

import acm
from at_feed_processing import SimpleCSVFeedProcessor, notify_log
from at_ael_variables import AelVariableHandler
from PB_Saxo_general import (get_account_alias,
                             DATE_LIST,
                             DATE_KEYS)
                             

import os
import string
import csv
import datetime


DEFAULT_DELIMITER = ","
DELIMITER = DEFAULT_DELIMITER

TODAY = acm.Time().DateToday()


def enable_custom_start_date(selected_variable):
    cust = ael_variables.get("custom_date")
    cust.enabled = (selected_variable.value == 'Custom Date')
    cust.value = TODAY


FILE_NAMES = (
    "FuturesTradesExecuted_${DATE}.txt,"
    "CFDTradesExecuted_${DATE}.txt,"
    "ETOTradesExecuted_${DATE}.txt,"
    "FXTradesExecuted_${DATE}.txt,"
    "FXOptionTradesExecuted_${DATE}.txt,"
    "ShareTradesExecuted_${DATE}.txt"
    )

ael_variables = AelVariableHandler()
ael_variables.add("date",
                  label="Date",
                  cls="string",
                  default="PrevNonWeekendDay",
                  collection=DATE_KEYS,
                  hook=enable_custom_start_date,
                  mandatory=True,
                  alt=("A date for which files will be taken."))
ael_variables.add("custom_date",
                  label="Custom Date",
                  cls="string",
                  default=TODAY,
                  enabled=False,
                  alt=("Format: '2016-09-30'."))
ael_variables.add("file_dir",
                  label="Directory",
                  default=r"y:\Jhb\FAReports\AtlasEndOfDay\PrimeClients\SAXO\${DATE}",
                  alt=("A Directory template with all input files. "
                       "It can contain the variable DATE (\"$DATE\") "
                       "which will be replaced by the today's date (format YYYY-MM-DD)"))
ael_variables.add("file_names",
                  label="List of Trades Executed filenames",
                  default=FILE_NAMES,
                  cls="string",
                  mandatory=True,
                  alt=("A list of path templates to trades executed files. "
                       "Filenames can contain the variable DATE (\"$DATE\") "
                       "which will be replaced by the today's date (format DD-MM-YYYY)"))
ael_variables.add("output_file",
                  label="Output file",
                  default="TradesExecuted_${DATE}.csv",
                  alt=("A path template to the trades executed output file. \n"
                       "It can be both absolute or just a relative path. "
                       "It can contain the variable DATE (\"$DATE\") "
                       "which will be replaced by the today's date (format DD-MM-YYYY)"))
ael_variables.add("csv_delimiter",
                  label="CSV Delimiter (default=;)",
                  cls="string",
                  default=",",
                  mandatory=False,
                  alt=("A delimiter character used in input csv file. "
                    "Comma (,) will be used as default if field is left empty."))


class MissingFileException(Exception): pass


class ExecTradesCSV(SimpleCSVFeedProcessor):


    col_account_number = "AccountNumber"

    _required_columns = [
        "ReportingDate",
        "InstrumentType",
        "CounterpartID",
        "CounterpartName",
        col_account_number,
        "PartnerAccountKey",
        "AccountCurrency",
        "InstrumentCode",
        "InstrumentCurrency",
        "TradedAmount",
        "TradeNumber",
        "OrderNumber",
        "TradeTime",
        "TradeDate",
        "ValueDate",
        "BuySell",
        "Price",
        "CommissionInstrumentCurrency",
        "RelatedTradeID",
        "TradeType",
        "TradeAllocation",
        "RootTradeID",
        "OriginalTradeID",
        "CorrectionLeg",
        ]

    @staticmethod
    def get_common_headers():
        return ExecTradesCSV._required_columns

    def __init__(self, file_path):
        super(ExecTradesCSV, self).__init__(file_path)
        self._dict_reader_kwargs = {'delimiter':DELIMITER}
        self.data = []
        self.headers = []

    def _process_record(self, record, dry_run):
        (_, _record_data) = record
        alias = get_account_alias(_record_data[self.col_account_number])
        if not alias:
            print("Skipping %s: %s" % (self.col_account_number,
                                       _record_data[self.col_account_number]))
            return
        self.data.append(_record_data)

    def get_headers_keep_order(self):
        """List of all headers with the same ordering as in file."""
        if not self.headers:
            with open(self._file_path, 'rb') as csvfile:
                reader = csv.reader(csvfile, delimiter=DELIMITER)
                self.headers = reader.next()
        return self.headers

    def get_extra_headers(self):
        """List of extra headers that are not in required columns."""
        if not self.data:
            return []
        all_keys = set(self.data[0].keys())
        common_keys = set(self._required_columns)
        extra_keys = all_keys.difference(common_keys)
        return sorted(extra_keys)

    def get_headers(self):
        """List of all headers with a random ordering.

        Every record contains dictionary with same keys.
        """
        return self.data[0].keys()


def merge_to_file(output_path, *args):
    """ Take N ExecTradesCSV objects and save their data to file.

    Merged file will have following column ordering:
        1) common columns
        2) remaining columns from obj1 and obj2 (sorted)

    Merged file will have following row ordering:
        1) rows from obj1 (same order as in original file)
        2) rows from obj2 (same order as in original file)
    """

    extra = []
    data = []
    for csvobj in args:
        extra += csvobj.get_extra_headers()
        data += csvobj.data

    extra = sorted(set(extra))

    common = ExecTradesCSV.get_common_headers()

    all_headers = common + extra

    with open(output_path, 'wb') as csvfile:
        writer = csv.DictWriter(csvfile, all_headers)
        writer.writer.writerow(all_headers)
        for row in data:
            writer.writerow(row)


def get_file_path(ael_dict, file_name, check_existing=False):

    if not file_name:
        return None

    # date in string
    if ael_dict['date'] == 'Custom Date':
        the_date = ael_dict['custom_date']
    else:
        the_date = DATE_LIST[ael_dict['date']]

    # file date will be converted to "dd-mm-YYYY"
    # directory date will be converted to "YYYY-mm-dd"
    _dt = datetime.datetime.strptime(the_date, "%Y-%m-%d")
    file_date_string = _dt.strftime("%d-%m-%Y")
    dir_date_string = the_date

    # directory in string
    file_dir = ael_dict["file_dir"]
    fdir_template = string.Template(file_dir)
    file_dir = fdir_template.substitute(DATE=dir_date_string)
    # filename in string
    fname_template = string.Template(file_name)
    file_name = fname_template.substitute(DATE=file_date_string)

    if not os.path.isabs(file_name):
        fullpath = os.path.join(file_dir, file_name)
    else:
        fullpath = file_name

    if check_existing and not os.path.exists(fullpath):
        print("ERROR: File not found: '%s'" % fullpath)
        raise MissingFileException(fullpath)
    return fullpath


def ael_main(ael_dict):

    global DELIMITER
    DELIMITER = DEFAULT_DELIMITER
    if ael_dict['csv_delimiter']:
        DELIMITER = ael_dict['csv_delimiter']

    file_templates = ael_dict['file_names'].split(',')
    csv_objects = []

    for name_templ in file_templates:
        file_name = get_file_path(ael_dict, name_templ, True)
        print("File: '%s'..." % os.path.basename(file_name))

        exec_trds_obj = ExecTradesCSV(file_name)
        exec_trds_obj.add_error_notifier(notify_log)
        exec_trds_obj.process(False)
        csv_objects.append(exec_trds_obj)

        print("\n")


    output_file = get_file_path(ael_dict, ael_dict['output_file'])
    print("Writing output to '%s'" % output_file)
    merge_to_file(output_file, *csv_objects)

    errors = []
    for proc_obj in csv_objects:
        for err in proc_obj.errors:
            print("ERROR: %s (%s)" % (err, proc_obj._file_path))
            errors.append(str(err))

    if errors:
        raise RuntimeError("Errors while processing files. %s" % errors)

    print("*" * 66)
    print("Completed successfully.")
