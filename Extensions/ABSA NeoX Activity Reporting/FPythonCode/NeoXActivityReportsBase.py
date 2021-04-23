"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    NeoXActivityReportHook

DESCRIPTION
    This module is used to define the API of a hook used for event-driven Activity Reports to Neox
    (straight-through-processing).

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2020-10-21      FAOPS-959       Ncediso Nkambule        Cuen Edwards            Initial implementation.
2020-11-12      FAOPS-981       Ncediso Nkambule        Cuen Edwards            Update Production file Path.
2021-03-16      FAOPS-982       Ncediso Nkambule        Gasant Thulsie          Added functions to handle Cashflow driven events.

-----------------------------------------------------------------------------------------------------------------------------------------
"""

import os
import acm
import csv
from math import isnan
from glob import glob
from logging import getLogger
from collections import OrderedDict
from datetime import datetime, timedelta
from at_type_helpers import is_acm, to_ael
import NeoXActivityReportsConstants as Constants
from NeoXActivityReportsUtils import get_add_info_value, is_float


LOGGER = getLogger(__name__)
CALCULATION_SPACE = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FTradeSheet')
MONEY_FLOW_CALCULATION_SPACE = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FMoneyFlowSheet')


class FileBase(object):
    transaction_id_name = "Transaction ID"

    def __init__(self, directory, file_name, is_instrument_update=False):
        self.directory = directory
        self.latest_file = None
        self.file_name = file_name
        self.latest_file_has_data = True
        self.latest_file_exist = False
        self._temp_absolute_path = os.path.join(directory, file_name + ".tmp")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return True

    @staticmethod
    def _is_valid_data_for_file(data):
        if not isinstance(data, list):
            return False
        if data and not isinstance(data[0], (dict, OrderedDict)):
            return False
        return True

    @staticmethod
    def _latest_file_path(directory, file_name, extension=".csv"):
        list_of_files = glob(os.path.join(directory, r"*{}".format(extension)))
        list_of_files = [f for f in list_of_files if file_name in f]
        latest_file = None
        if list_of_files:
            latest_file = max(list_of_files, key=os.path.getctime)
        return latest_file

    def _get_latest_file_path(self):
        self.latest_file = self._latest_file_path(self.directory,  self.file_name, extension=".csv")
        if self._is_latest_file_empty():
            self.latest_file_has_data = False

    def _read_latest_file_data(self):
        file_data = self._read_file(self.latest_file)
        return file_data

    @staticmethod
    def _read_file(absolute_path):
        reader = csv.DictReader(open(absolute_path, 'rU'))
        return list(reader)

    def _latest_file_exist(self, file_path=None):
        if not file_path:
            file_path = self.latest_file
        self.latest_file_exist = os.path.isfile(file_path)
        return self.latest_file_exist

    def _is_latest_file_empty(self, file_path=None):
        """ Check if file is empty by confirming if its size is 0 bytes"""
        if not file_path:
            file_path = self.latest_file
        if not self._latest_file_exist(file_path):
            return True
        return self._latest_file_exist(file_path) and os.stat(file_path).st_size == 0

    def compare_data(self, new_report_data):
        old_report_data = self._read_latest_file_data()
        clean_result_data = self.perform_data_comparison(
            new_report_data=new_report_data,
            old_report_data=old_report_data,
            unique_id="Trade Reference",
            ignore_columns=["Trade Update Time"])
        return clean_result_data

    def perform_data_comparison(self, new_report_data, old_report_data, unique_id="Trade Reference", ignore_columns=None):
        new_data_rows = []
        updated_data_rows = []
        ignore_list = [self.transaction_id_name]
        if ignore_columns and isinstance(ignore_columns, str):
            ignore_list.append(ignore_columns)
        if ignore_columns and isinstance(ignore_columns, list):
            ignore_list += ignore_columns

        for dictionary in new_report_data:
            is_new = not any([dictionary[unique_id] == row_dict[unique_id] for row_dict in old_report_data])
            has_changed = False
            if not is_new:
                if ignore_list:
                    has_changed = any([
                        any([dictionary[key] != row_dict[key] for key in list(dictionary.keys()) if key not in ignore_list])
                        for row_dict in old_report_data if dictionary[unique_id] == row_dict[unique_id]])
                else:
                    has_changed = any([any([dictionary[key] != row_dict[key] for key in list(dictionary.keys())])
                                       for row_dict in old_report_data if dictionary[unique_id] == row_dict[unique_id]])
            if is_new:
                new_data_rows.append(dictionary)
            if has_changed:
                updated_data_rows.append(dictionary)

        LOGGER.info("Got {} New Report Rows".format(str(len(new_data_rows))))
        LOGGER.info("Got {} Updated Report Rows".format(str(len(updated_data_rows))))
        result_data = new_data_rows + updated_data_rows
        LOGGER.info("Removing Duplicates on data")
        clean_result_data = [i for n, i in enumerate(result_data) if i not in result_data[n + 1:]]
        return clean_result_data

    def dict_list_to_csv(self, data_dict_list, file_name=None, headers=None, directory=None):
        if self._is_valid_data_for_file(data_dict_list) is False:
            return
        LOGGER.info("Ready to create report for {} - {}".format(self.__class__.__name__, str(len(data_dict_list))))
        if data_dict_list:
            try:
                if not directory:
                    directory = self.directory
                if not file_name:
                    file_name = self.file_name
                start_date = datetime.now()
                date_string = start_date.strftime(Constants.FILE_DATE_FORMAT)
                absolute_path = os.path.join(directory, file_name + "_" + date_string + ".csv")
                if headers is None:
                    headers = list(data_dict_list[0].keys())
                data_to_file = [i for n, i in enumerate(data_dict_list) if i not in data_dict_list[n + 1:]]
                with open(absolute_path, "wb") as data_file:
                    writer = csv.DictWriter(data_file, fieldnames=headers)
                    writer.writeheader()
                    writer.writerows(data_to_file)
                os.chmod(absolute_path, 0o777)
                LOGGER.info("Generated File to {}".format(absolute_path))
            except Exception as error:
                LOGGER.exception(error)
        else:
            LOGGER.info("Empty Data Set. No file will be created.")

    def append_dict_to_temp_file(self, trade_info_dict, headers):
        try:
            file_is_empty = self._is_latest_file_empty(self._temp_absolute_path)
            with open(self._temp_absolute_path, "ab") as temp:
                writer = csv.DictWriter(temp, fieldnames=headers)
                if file_is_empty:
                    writer.writeheader()

                writer.writerow(trade_info_dict)
                message = "Check Temp File: {}".format(str(self._temp_absolute_path))
                LOGGER.info(message)
        except Exception as error:
            LOGGER.exception(error)

    def move_file(self, destination_directory, headers=None):
        try:

            LOGGER.info("Moving Data from Temp File to Y Drive.")
            from_dir, temp_file_name = os.path.split(self._temp_absolute_path)
            file_name, bak_extension = temp_file_name.split(".")
            if not headers:
                if "collateral" in file_name.lower():
                    headers = [self.transaction_id_name] + list(Constants.COLLATERAL_ACTIVITY_COLUMN_IDS.values())
                else:
                    headers = [self.transaction_id_name] + list(Constants.LOAN_ACTIVITY_COLUMN_IDS.values())
            new_report_data = self._read_file(self._temp_absolute_path)
            latest_path = self._latest_file_path(destination_directory, file_name)
            if latest_path:
                old_report_data = self._read_file(latest_path)
            else:
                old_report_data = []
            result_data = self.perform_data_comparison(
                new_report_data=new_report_data,
                old_report_data=old_report_data,
                unique_id="Trade Reference",
                ignore_columns=["Trade Update Time"])
            self.dict_list_to_csv(result_data, file_name, directory=destination_directory, headers=headers)

        except Exception as error:
            LOGGER.exception(error)

        self.perform_backup()

    def perform_backup(self):
        try:
            from_dir, temp_file_name = os.path.split(self._temp_absolute_path)
            file_name, bak_extension = temp_file_name.split(".")
            date_string = datetime.now().strftime(Constants.FILE_DATE_FORMAT)
            file_name_full = "_".join(["BAC", file_name, date_string]) + '.bac'
            bak_absolute_path = os.path.join(os.path.join(from_dir, 'backup'), file_name_full)
            message = "Backing up {} File {} to {}"
            LOGGER.info(message.format(temp_file_name, self._temp_absolute_path, bak_absolute_path))
            os.rename(self._temp_absolute_path, bak_absolute_path)
            with open(self._temp_absolute_path, "wb") as fil:
                fil.write("")
        except Exception as error:
            LOGGER.exception(error)


class DateManager(object):
    @staticmethod
    def get_start_of_day_datetime(today):
        day_start = datetime(year=today.year, month=today.month, day=today.day, hour=0, second=0)
        return day_start

    @classmethod
    def get_start_of_day_datetime_str(cls, today):
        day_start = cls.get_start_of_day_datetime(today)
        return day_start.strftime(Constants.DATETIME_FORMAT)

    @staticmethod
    def datetime_from_string(string_date, date_format=Constants.DATE_FORMAT):
        return datetime.strptime(string_date, date_format)

    @classmethod
    def to_datetime_str(cls, string_date):
        start_date = cls.datetime_from_string(string_date)
        return start_date.strftime(Constants.DATETIME_FORMAT)

    @classmethod
    def get_datetime(cls, string_date=None):
        end_datetime = datetime.now()
        if string_date:
            end_datetime = cls.datetime_from_string(string_date)
        return end_datetime

    @classmethod
    def get_datetime_str(cls, string_date=None):
        end_datetime = cls.get_datetime(string_date)
        return end_datetime.strftime(Constants.DATETIME_FORMAT)

    @staticmethod
    def get_activity_adjusted_datetime(string_date=None, date_time=None, days=0, minutes=15):
        is_date = isinstance(date_time, datetime)
        is_string = isinstance(string_date, str)
        if date_time is None and string_date is None:
            date_time = datetime.now()
        elif (date_time and string_date is None) or (string_date and is_date and date_time and is_date):
            LOGGER.info("Using date_time since both string_date and date_time are provided")
        elif (date_time is None and string_date) and (is_string or string_date and date_time and is_string):
            date_time = DateManager.datetime_from_string(string_date)
        time_delta = timedelta(days=days, minutes=minutes)
        adjusted_datetime = date_time - time_delta
        return adjusted_datetime

    @classmethod
    def get_activity_adjusted_datetime_str(cls, string_date=None, date_time=None, days=0, minutes=15):
        adjusted_datetime = cls.get_activity_adjusted_datetime(string_date, date_time, days, minutes)
        return adjusted_datetime.strftime(Constants.DATETIME_FORMAT)


class CalculationBase:
    is_instrument_update = False
    transaction_id_name = "Transaction ID"

    def __init__(self, directory, file_name, is_instrument_update=False):
        self.is_instrument_update = is_instrument_update

    @staticmethod
    def _is_acm_object(f_object):
        try:
            f_object.Oid()
            return True
        except Exception as error:
            LOGGER.debug(error)
            return False

    @staticmethod
    def _is_fobject(obj, object_type=None):
        to_return = False
        if hasattr(obj, 'IsKindOf'):
            if object_type is None:
                to_return = True
            else:
                to_return = obj.IsKindOf(object_type)
        return to_return

    @classmethod
    def perform_calculation(cls, acm_object, column_name, calc_space=None):
        value = None
        try:
            if calc_space is None:
                calc_space = CALCULATION_SPACE
            loan = calc_space.InsertItem(acm_object)
            calc_space.Refresh()
            calc_value = calc_space.CalculateValue(loan, column_name)
            if cls._is_fobject(calc_value, acm.FDenominatedValue):
                value = calc_value.Number()
            elif is_acm(calc_value) and cls._is_acm_object(calc_value):
                value = calc_value.Name()
            elif value is not None:
                value = calc_value.Value()
            else:
                value = calc_value
            if cls.is_instrument_update and column_name == "Trade Update Time":
                value = acm_object.Instrument().UpdateTime()
        except Exception as error:
            LOGGER.exception(error)
        finally:
            return value

    @classmethod
    def get_calculated_values(cls, acm_trade, columns_dict):
        trade_data = OrderedDict()
        max_len = max([len(v) for v in list(columns_dict.values())])
        for col in list(columns_dict.keys()):
            white_space = " " * (max_len + 2 - len(columns_dict[col]))
            val = None
            if all(a in col for a in ['AdditionalInfo', "."]):
                val = get_add_info_value(acm_trade, col.split(".")[1])
            elif "Instrument.Underlying.SLPrice" == col:
                val = acm_trade.Instrument().Underlying().SLPrice()
            elif "Contract.Oid" == col and acm_trade.Contract():
                val = acm_trade.Contract().Oid()
            elif "Contract.FaceValue" == col and acm_trade.Contract():
                val = acm_trade.Contract().FaceValue()
            elif col in ["Text1"]:
                val = acm_trade.Text1()
            else:
                val = cls.perform_calculation(acm_object=acm_trade, column_name=col)
            if col in ['Trade Update Time']:
                val = acm.Time.DateTimeFromTime(val)
            if val is None:
                val = ""
            if is_float(val) and isnan(float(val)):
                val = ""
            LOGGER.debug(columns_dict[col], white_space + ":", val)
            trade_data[columns_dict[col]] = str(val)
        LOGGER.debug("\n")
        return trade_data

    @classmethod
    def get_deposit_cashflow_specific_data(cls, cashflow, is_delete=False):
        data = dict()
        for column_name in list(Constants.CASHFLOW_COLUMN_IDS.keys()):
            try:
                value = cls.perform_calculation(
                    acm_object=cashflow,
                    column_name=column_name,
                    calc_space=MONEY_FLOW_CALCULATION_SPACE)
            except Exception as error:
                LOGGER.exception(error)
                value = None

            if is_delete and isinstance(value, (float, int)):
                value = 0.0
            data[Constants.CASHFLOW_COLUMN_IDS[column_name]] = str(value)

        for column_name in list(Constants.DEPOSIT_COLUMN_IDS.keys()):
            if Constants.DEPOSIT_COLUMN_IDS[column_name] == "Collateral Type" and cashflow.Instrument().IsCallAccount():
                data[Constants.DEPOSIT_COLUMN_IDS[column_name]] = "Cash"

        return data
