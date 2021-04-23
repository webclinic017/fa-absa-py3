"""---------------------------------------------------------------------------------------------------------------------
MODULE                  :       TerminationTradesReport
PURPOSE                 :       This module contains details to identify trades terminated incorrectly.
------------------------------------------------------------------------------------------------------------------------

HISTORY
========================================================================================================================
Date            Change no       Developer       Requester                           Description
------------------------------------------------------------------------------------------------------------------------
2021-02-25      FAFO-168        Ruth Nkuna      Angelique Salsone                   Initial Implementation
------------------------------------------------------------------------------------------------------------------------

"""

import acm
import csv
import os.path
from itertools import combinations
from datetime import datetime, timedelta
from logging import getLogger
from collections import OrderedDict
from at_ael_variables import AelVariableHandler
from Emails_Utils import TableEmail

LOGGER = getLogger(__name__)
CALC_SPACE = acm.Calculations().CreateCalculationSpace('Standard', 'FTradeSheet')


count = 0
total = 0
percentage = -1
start = datetime.now()
mid_time = datetime.now()
processed_trades = set()
trades_in_exceptions = list()
non_matching_trades = set()
unclosed_trades = set()


class CustomTradeClass:
    def __init__(self, trade, valuation_date):
        self.trade_number = trade.Name()
        self.valuation_date = valuation_date
        self.instrument = trade.Instrument().Name()
        self.instrument_type = trade.Instrument().InsType()
        self.portfolio = trade.Portfolio().Name()
        self.val_end = 0.0
        self.trade_type = trade.Type()
        self.nominal = round(trade.Nominal())
        self.trade = None
        self.is_expired_instrument = False
        self.update_time = acm.Time.DateTimeFromTime(trade.UpdateTime())
        self.update_date = acm.Time.DateFromTime(trade.UpdateTime())
        self.instrument_start = None
        self.instrument_end = None
        self.is_zero_val_end = False
        self.instrument_currency = trade.Instrument().Currency().Name()
        self.instrument_expiry_date = trade.Instrument().ExpiryDate()
        self.trade_currency = trade.Currency().Name()
        if self.instrument_type in ['Swap', 'Cap', 'FRA']:
            self.instrument_start = trade.Instrument().StartDate()
            self.instrument_end = trade.Instrument().EndDate()

        self.update_total_val_end(trade)
        self._is_expired_instrument(trade)
        self._is_zero_val_end()

    def update_total_val_end(self, trade):
        total_val_end = 0.0
        try:
            # Could be removed for something else
            CALC_SPACE.SimulateValue(trade, "Portfolio Currency", trade.Instrument().Currency())
            calculated_value = CALC_SPACE.CalculateValue(trade, 'Total Val End')
            total_val_end = calculated_value.Value().Number()
        except Exception as error:
            LOGGER.exception(error)
        finally:
            self.val_end = round(total_val_end, 2)

    def _is_expired_instrument(self, trade):
        if trade and trade.Instrument().ExpiryDate() < self.valuation_date:
            self.is_expired_instrument = True

    def _is_zero_val_end(self):
        if abs(round(self.val_end)) == 0.0:
            self.is_zero_val_end = True

    def get_data(self):
        self.trade = acm.FTrade[self.trade_number]
        trade_data = OrderedDict()
        trade_data['Trade Number'] = self.trade_number
        trade_data['Instrument Name'] = self.instrument
        trade_data['InsType'] = self.instrument_type
        trade_data['Status'] = self.trade.Status()
        trade_data["Nominal"] = self.nominal
        trade_data["Total Val End"] = self.val_end
        trade_data["Portfolio Name"] = self.trade.Portfolio().Name()
        trade_data["Counterparty"] = self.trade.Counterparty().Name()
        trade_data["Value Day"] = self.trade.ValueDay()
        trade_data["Instrument Expiry Date"] = self.instrument_expiry_date
        trade_data["Update Time"] = self.update_time

        return trade_data

    def __str__(self):
        message = "CustomTradeClass -> {oid}\n Val End(PV): {pv}\n Nominal: {nom}\n"
        return_str = message.format(
            oid=str(self.trade_number),
            pv=str(self.val_end),
            nom=str(self.nominal)
        )
        return return_str

    def __repr__(self):
        return "{}".format(self.trade_number)


class MatchedTrades:

    fully_matched_trades = set()

    def __init__(self, custom_normal_trade=None, custom_closing_trade=None):
        self.__closing_trade = custom_closing_trade
        self.__normal_trade = custom_normal_trade
        self.val_end_matches = False

        self._val_end_matches()

    def _val_end_matches(self):
        val_end_sum = round(abs(self.__closing_trade.val_end + self.__normal_trade.val_end))
        if val_end_sum == 0.0:
            self.val_end_matches = True
            MatchedTrades.fully_matched_trades.add(self)

    @property
    def closing_trade(self):
        return self.__closing_trade

    @closing_trade.setter
    def closing_trade(self, custom_trade):
        self.__closing_trade = custom_trade

    @property
    def normal_trade(self):
        return self.__normal_trade

    @normal_trade.setter
    def normal_trade(self, custom_trade):
        self.__normal_trade = custom_trade

    def __str__(self):
        return_string = 'Matching Trades Info\n'
        s_string = (" {typ} Trade\n - Trade Number: {trd}\n - Trade Nominal: {nom} \n - Total Val End: {val}"
                    "\n - Instrument Type: {ins}\n")
        if self.__closing_trade:
            return_string += s_string.format(
                typ="Closing",
                trd=str(self.closing_trade.trade_number),
                nom=str(self.closing_trade.nominal),
                val=str(self.closing_trade.val_end),
                ins=self.closing_trade.instrument)

        if self.__normal_trade:
            return_string += s_string.format(
                typ="Normal",
                trd=str(self.normal_trade.trade_number),
                nom=str(self.normal_trade.nominal),
                val=str(self.normal_trade.val_end),
                ins=self.normal_trade.instrument)
        return return_string

    def __repr__(self):
        ret_str = "NOM: {nom}, CLO: {clo}, VAL-END-SUM: {val_end_sum}"
        clo = ""
        nom = ""
        if self.closing_trade:
            clo = self.closing_trade.trade_number
        if self.normal_trade:
            nom = self.normal_trade.trade_number
        summation = round(self.normal_trade.val_end + self.closing_trade.val_end)

        return ret_str.format(nom=nom, clo=clo, val_end_sum=str(summation))


class MultipleMatchingTrades:

    fully_matched_trades = set()

    def __init__(self, matching_trades):
        self.__positive_trades = list()
        self.__negative_trades = list()
        self.val_end_matches = False

        self.classify_trade_direction(matching_trades)

        self._val_end_matches(matching_trades)

    @property
    def positive_trades(self):
        return self.__positive_trades

    @positive_trades.setter
    def positive_trades(self, custom_trade):
        self.__positive_trades.append(custom_trade)

    @property
    def negative_trades(self):
        return self.__negative_trades

    @negative_trades.setter
    def negative_trades(self, custom_trade):
        self.__negative_trades.append(custom_trade)

    def _val_end_matches(self, matching_trades):
        sum_all = round(sum([c_trade.val_end for c_trade in matching_trades]))
        if sum_all == 0.0:
            self.val_end_matches = True
            MultipleMatchingTrades.fully_matched_trades.add(self)

    def classify_trade_direction(self, matching_trades):
        for c_trade in matching_trades:
            if c_trade.val_end < 0.0:
                self.negative_trades = c_trade
            if c_trade.val_end > 0.0:
                self.positive_trades = c_trade

    def __str__(self):
        return_string = 'Multiple Matching Trades Info - {}\n'.format(str(self.negative_trades + self.positive_trades))
        s_string = (" {typ} Trade\n - Trade Number: {trd}\n - Trade Nominal: {nom} \n - Total Val End: {val}"
                    "\n - Instrument Type: {ins}\n")
        for c_trade in self.negative_trades:
            return_string += s_string.format(
                typ="Negative",
                trd=str(c_trade.trade_number),
                nom=str(c_trade.nominal),
                val=str(c_trade.val_end),
                ins=c_trade.instrument)

        for c_trade in self.positive_trades:
            return_string += s_string.format(
                typ="Positive",
                trd=str(c_trade.trade_number),
                nom=str(c_trade.nominal),
                val=str(c_trade.val_end),
                ins=c_trade.instrument)


class AnalyserClass:

    def __init__(self, portfolios, path_to_exception_trades, email_addresses, cc_email_addresses, output_file, valuation_date):
        self.cc_email_addresses = cc_email_addresses
        self.trades_in_exceptions = list()
        self.termination_set = set()
        self.email_addresses = email_addresses
        self.portfolios = portfolios
        self.data_to_file_or_email = None
        self.output_file = output_file
        self.valuation_date = valuation_date
        self.unclosed_trades = None

        self._get_trade_list_from_file(path_to_exception_trades)

    def prepare_report_dict(self):
        not_in_exceptions = filter(lambda t: t.trade_number not in trades_in_exceptions, self.unclosed_trades)
        unclosed_trades_data = [trd.get_data() for trd in not_in_exceptions]
        without_duplicates = [i for n, i in enumerate(unclosed_trades_data) if i not in unclosed_trades_data[n + 1:]]
        self.data_to_file_or_email = without_duplicates

    @staticmethod
    def is_qualifying_trade(trade):

        if not trade:
            return False
        if trade.ArchiveStatus() or trade.Aggregate():
            return False
        if trade.Status() != "Terminated":
            return False
        return True

    def get_portfolio_trades(self):
        start_p = datetime.now()
        total_trades = set()
        for portfolio in self.portfolios:
            terminated_portfolios_trades = set(filter(lambda t: self.is_qualifying_trade(t), portfolio.Trades()))
            total_trades.update(terminated_portfolios_trades)
            LOGGER.info("Took {tim} to process {num} trades from {prf}".format(
                tim=datetime.now() - start_p,
                num=str(len(terminated_portfolios_trades)),
                prf=portfolio.Name()))
            start_p = datetime.now()
        return total_trades

    def email_uploaded_trades(self):
        email_sender = 'Abcap-IT-Front-Arena-Front-Office@absa.africa'
        report_header = 'Trades for Termination Report'
        email_subject = 'Termination Report on {}'.format(self.valuation_date)
        if self.data_to_file_or_email:
            table_headings = self.data_to_file_or_email[0].keys()
            table_email = TableEmail(email_subject, self.email_addresses, self.cc_email_addresses, email_sender, attachments=[self.output_file])
            table_email.add_header(table_headings)
            table_email.add_rows(self.data_to_file_or_email)
            table_email.create_report(report_header)
            table_email.send_report()

    @staticmethod
    def read_csv_to_list(absolute_path, column_name=None):
        return_data = list()
        with open(absolute_path, 'rb') as file_obj:
            file_reader = csv.DictReader(file_obj)
            file_data = list(file_reader)
            if file_data and column_name and column_name in file_data[0].keys():
                for item in file_data:
                    for k in item.keys():
                        if k.strip() == column_name:
                            return_data.append(item[column_name])
            LOGGER.info("Successfully read data ({} Rows) from file {}".format(str(len(file_data)), absolute_path))
        return return_data

    def _get_trade_list_from_file(self, file_path):
        if os.path.exists(file_path):
            self.trades_in_exceptions = self.read_csv_to_list(file_path, 'Trade Numbers')
            global trades_in_exceptions
            trades_in_exceptions = self.trades_in_exceptions


    def write_dict_list_to_file(self, headers=None, data=None, absolute_path=None):
        if absolute_path is None:
            absolute_path = self.output_file
        if not data:
            data = self.data_to_file_or_email
        if headers is None and data:
            headers = data[0].keys()
        if data and headers:
            with open(absolute_path, 'wb') as file_path:
                writer = csv.DictWriter(file_path, fieldnames=headers)
                writer.writeheader()
                writer.writerows(data)

    def get_portfolio_instruments(self):
        LOGGER.info("Fetching instruments from portfolios: {}".format(",".join([p.Name() for p in self.portfolios])))
        start_p = datetime.now()
        trades = self.get_portfolio_trades()
        instruments = set(map(lambda t: t.Instrument(), trades))
        LOGGER.info("Took {tim} to fetch {num} instruments\n".format(
            tim=datetime.now() - start_p,
            num=str(len(instruments))))
        return instruments

    @staticmethod
    def investigate_set(sorted_set, check_update_date=False):
        processed_set = set()
        date_format = "%Y-%m-%d %H:%M:%S"

        for i in combinations(sorted_set, 2):
            _sum = sum([k.val_end for k in i])
            if any(k in processed_set for k in i):
                continue
            if abs(round(_sum)) == 0:
                trade_1 = i[0]
                trade_2 = i[1]
                if trade_1.portfolio != trade_2.portfolio:
                    continue
                if check_update_date:
                    date_time_diff = datetime.strptime(trade_1.update_time, date_format) - datetime.strptime(
                        trade_2.update_time, date_format)
                    if timedelta(seconds=-10) > date_time_diff or date_time_diff > timedelta(seconds=10):
                        continue
                    if len({k.update_date for k in i}) != 1:
                        continue
                processed_set.update(i)
                MatchedTrades(custom_normal_trade=trade_1, custom_closing_trade=trade_2)

        left_aside = set(sorted_set) - processed_set
        val_end_sum = round(sum([t.val_end for t in left_aside]))
        if val_end_sum == 0:
            processed_set.update(left_aside)
            _left_aside = list(left_aside)
            if len(_left_aside) == 2:
                MatchedTrades(custom_normal_trade=_left_aside[0], custom_closing_trade=_left_aside[1])
            else:
                MultipleMatchingTrades(matching_trades=left_aside)

        left_aside = set(sorted_set) - processed_set
        return left_aside

    def process_termination_report_per_ins(self):
        global total
        un_matched = set()
        instruments = self.get_portfolio_instruments()
        total = len(instruments)
        LOGGER.info("Removing Matching Trades per Instrument")

        for instrument in instruments:
            display_percentages("Processing Instruments")
            if instrument.ExpiryDate() < self.valuation_date:
                continue
            terminated_trades = set(filter(lambda t: self.is_qualifying_trade(t), instrument.Trades()))
            calculated_set = map(lambda trade: CustomTradeClass(trade, self.valuation_date), terminated_trades)
            valid_set = filter(lambda t: t.is_expired_instrument is False and t.is_zero_val_end is False, calculated_set)
            sorted_set = sorted(valid_set, key=lambda t: t.update_time, reverse=False)
            left_aside = self.investigate_set(sorted_set, check_update_date=False)

            if left_aside:
                un_matched.update(left_aside)

        self.unclosed_trades = un_matched

        self.prepare_report_dict()


def display_percentages(message):
    global count, percentage, start, mid_time
    count += 1
    temp = int((float(count) / total) * 100)
    if count <= total and temp > percentage and temp % 5 == 0:
        percentage = temp
        elapsed = datetime.now() - mid_time
        LOGGER.info("{} - Processed {}% of {} Trades - Time: {}".format(message, str(percentage), str(total), elapsed))
        mid_time = datetime.now()
    if percentage == 100:
        percentage = -1
        count = 0


default_path = r"C:\Temp\Termination Report"
portfolio_names = ['GROUP TREASURY', 'SECONDARY MARKETS BANKING', 'SECONDARY MARKETS TRADING']
path_to_exception = r"C:\Temp\Termination Report\Termination Report Exclusions.csv"
emails = ['ruth.nkuna@absa.africa']
run_date = acm.Time.DateToday()

# region AEL Variables
ael_variables = AelVariableHandler()
ael_variables.add(
    'portfolios',
    label='Portfolio(s)',
    cls='FPhysicalPortfolio',
    default=",".join(portfolio_names),
    multiple=True, mandatory=False)
ael_variables.add_input_file(
    'input_file_path',
    label='File Directory',
    cls='FFileSelection',
    default=path_to_exception)
ael_variables.add_directory(
    'output_directory',
    label='Output Directory',
    cls='FFileSelection',
    default=default_path)
ael_variables.add(
    "email_addresses",
    label="Email Addresses:",
    default=",".join(emails),
    alt="Use a comma as a separator",
    multiple=True)
ael_variables.add(
    "cc_email_addresses",
    label="CC Email Addresses:",
    default=None,
    alt="Use a comma as a separator",
    mandatory=False,
    multiple=True)
# endregion


def ael_main(parameters_dict):
    global start, processed_trades, trades_in_exceptions
    start = datetime.now()
    LOGGER.info("Starting Time: {}".format(start))
    out_put_directory = parameters_dict['output_directory'].AsString()
    if parameters_dict['output_directory']:
        if os.path.isdir(out_put_directory) is False:
            os.makedirs(out_put_directory)
    absolute_path = os.path.join(out_put_directory, "Temp-Termination.csv")

    trade_analyser = AnalyserClass(
        portfolios=parameters_dict['portfolios'],
        path_to_exception_trades=parameters_dict['input_file_path'].AsString(),
        email_addresses=parameters_dict['email_addresses'],
        cc_email_addresses=parameters_dict["cc_email_addresses"],
        output_file=absolute_path,
        valuation_date=run_date)

    trade_analyser.process_termination_report_per_ins()
    trade_analyser.write_dict_list_to_file()
    trade_analyser.email_uploaded_trades()

    LOGGER.info("stop time: {}".format(datetime.now().isoformat()))
    LOGGER.info("Duration: {}\n".format(datetime.now() - start))

    processed_trades = set()
    trades_in_exceptions = list()
