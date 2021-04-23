'''-------------------------------------------------------------------------------------------------
MODULE
    IT3B_Financial_Data_Extract

DESCRIPTION
    Date      : 2019-08-12
    Purpose   : Extracts Financial Data for the bank's IT3B report submission
    Developer : Qaqamba Ntshobane
    Requester : Nhlanhleni Mchunu
    Department: PCG

=======================================================================================================
HISTORY:
    Date:               Change No:      Developer:              Description:
-------------------------------------------------------------------------------------------------------
    2019-06-19          PCGDEV-156      Qaqamba Ntshobane       Initial Design
    2020-02-28          PCGDEV-324      Qaqamba Ntshobane       Redesigned script to optimise for speed
    2020-05-26          PCGDEV-137      Qaqamba Ntshobane       Enabled script to extract VAT data
                                                                for SA Debt portfolios as requested
                                                                by Leon Swart
    2021-01-28          PCGDEV-686      Qaqamba Ntshobane       Moved some functions to general functions
                                                                module

ENDDESCRIPTION
----------------------------------------------------------------------------------------------------'''
import os
import acm
import string
import calendar
import xlsxwriter
import currentNominal

from at_logging import getLogger
from at_ael_variables import AelVariableHandler
from collections import defaultdict, OrderedDict
from sars_reporting_functions import (get_instrument_end_date, get_account_number, 
                                        get_period_dates, send_success_notification)

LOGGER = getLogger(__name__)

DIRECTORY_SELECTOR = acm.FFileSelection()
DIRECTORY_SELECTOR.PickDirectory(True)
DIRECTORY_SELECTOR.SelectedDirectory(r'/services/frontnt/Task')


def switch_query_folder(ael_var):

    for var in ael_variables:
        if var[0] == 'query_folder' and ael_var.value == 'true':
            var.value = 'VAT_Extract'


def get_ael_variables():
    variables = AelVariableHandler()
    variables.add(
        'end_date',
        label='End Date',
        default=acm.Time.DateToday(),
        alt='date format: DD/MM/YYYY',
        cls='date')
    variables.add(
        'query_folder',
        label='Query Folder',
        cls='string')
    variables.add(
        'file_drop_location',
        label='File Drop Location',
        default=DIRECTORY_SELECTOR,
        cls=DIRECTORY_SELECTOR,
        multiple=True)
    variables.add(
        'email_address',
        label='Email Addresses',
        default='CIBPCGTaxReporting@groups.absa.africa',
        mandatory=False,
        multiple=True,
        alt='Email results to these recipients'
        )
    variables.add(
        'is_vat_extract',
        label='VAT Extract?',
        default=False,
        cls='bool',
        hook=switch_query_folder,
        collection=(True, False)
        )
    return variables

ael_variables = get_ael_variables()


def ael_main(dictionary):

    end_date = dictionary['end_date']
    start_date, end_date = get_period_dates(end_date)
    query_folder = str(dictionary['query_folder'])
    is_vat_extract = dictionary['is_vat_extract']
    file_drop_location = str(dictionary['file_drop_location'])

    report_name = 'VAT_Extract_%s.xlsx' if is_vat_extract else 'IT3BFinancial_Data_Extract_%s_%s.xlsx'
    report_path = os.path.join(file_drop_location, report_name)
    trades_dict = {}

    trade_processor = ProcessReportableTrades(start_date, end_date, is_vat_extract) 
    trades = trade_processor.get_trades(query_folder)

    if not trades:
        LOGGER.info("No open positions to report for %s. No report produced." %end_date)
        return

    time_now = acm.Time.TimeNow().split('.')[0]
    ins_type = trades[0].Instrument().InsType().replace("/", "")

    if is_vat_extract:
        report_path = report_path %(acm.Time.DateToYMD(end_date)[0])
    else:
        report_path = report_path %(ins_type, ''.join(filter(str.isdigit, time_now)))

    for index, trade in enumerate(trades):
        record = float(index + 1)
        percentage = round(float(record / len(trades)) * 100, 2)

        LOGGER.info('>>> %s PROCESSING RECORD, %s: %s OF %s (%s)' % (str(time_now), trade.Oid(), index+1, len(trades), percentage))

        trade_data = trade_processor.process_trade(trade)

        if trade_data:
            trades_dict[trade.Oid()] = trade_data

    report_processor = ReportProcessor(start_date, end_date, is_vat_extract)
    report_processor.generate_report(trades_dict, report_path)

    email_addresses = dictionary['email_address']
    report_name = report_name %(ins_type, ''.join(filter(str.isdigit, time_now)))

    send_success_notification(email_addresses, 'IT3B', report_name)


class ProcessReportableTrades(object):

    def __init__(self, start_date, end_date, is_vat_extract):

        self.trade = None
        self.start_date = start_date
        self.end_date = end_date
        self.is_vat_extract = is_vat_extract
        self.fx_rates = {}
        self.row_data = OrderedDict()
        self.local_currency = 'ZAR'
        self.calc_space = acm.FCalculationMethods().CreateCalculationSpace(acm.GetDefaultContext(), 'FDealSheet')
        self.currency_list = [curr.Name() for curr in acm.FCurrency.Select("") if not curr.Name() == self.local_currency]
        self.end_month = acm.Time.DateToYMD(end_date)[1]

        self.get_fx_rates()

    def get_trades(self, query_folder):

        query = acm.FStoredASQLQuery[query_folder].Query()
        query.AddAttrNode('ValueDay', 'LESS_EQUAL', str(self.end_date))
        query.AddAttrNode('TradeTime', 'LESS_EQUAL', str(self.end_date))
        query.AddAttrNode('Instrument.ExpiryDate', 'GREATER_EQUAL', str(self.start_date))

        return query.Select()

    def process_trade(self, trade):

        self.trade = trade
        trade_id = trade.Oid()
        start_date = acm.Time.FirstDayOfMonth(self.start_date)

        self.row_data.clear()
        self.row_data.setdefault(trade_id, OrderedDict())

        self.row_data[trade_id]['trade_number'] = trade_id
        self.row_data[trade_id]['unique_identifier'] = self.trade.Counterparty().Oid()
        self.row_data[trade_id]['source_code'] = 4201
        self.row_data[trade_id]['instype'] = self.trade.Instrument().InsType()
        self.row_data[trade_id]['funding_instype'] = self.trade.AdditionalInfo().Funding_Instype() if self.row_data[trade_id]['instype'] in ['CD', 'Deposit'] else ''
        self.row_data[trade_id]['account_number'] = get_account_number(self.trade.MoneyFlows())
        self.row_data[trade_id]['portfolio_name'] = self.trade.Portfolio().Name()
        self.row_data[trade_id]['currency'] = self.trade.Currency().Name()
        self.row_data[trade_id]['fx_rate'] = self.fx_rates[self.row_data[trade_id]['currency']]
        self.row_data[trade_id]['opening_balance'] = self.set_opening_balance()
        self.row_data[trade_id]['instrument_start_date'] = self.trade.Instrument().StartDate()
        self.row_data[trade_id].setdefault('closing_balance', 0.0)
        self.row_data[trade_id]['instrument_end_date'] = get_instrument_end_date(self.trade, self.end_date)
        self.row_data[trade_id]['counterparty_id'] = self.trade.Counterparty().AdditionalInfo().BarCap_Eagle_SDSID()
        self.row_data[trade_id].setdefault('total_income_accrued', 0.0)
        
        if self.is_vat_extract:
            self.row_data[trade_id].setdefault('total_expense_inccured', 0.0)

        self.row_data[trade_id]['March'] = self.calculate_interest(acm.Time.DateAddDelta(start_date, 0, 0, 0),
                                                         acm.Time.DateAddDelta(start_date, 0, 1, 0))
        self.row_data[trade_id]['April'] = self.calculate_interest(acm.Time.DateAddDelta(start_date, 0, 1, 0),
                                                         acm.Time.DateAddDelta(start_date, 0, 2, 0))
        self.row_data[trade_id]['May'] = self.calculate_interest(acm.Time.DateAddDelta(start_date, 0, 2, 0),
                                                       acm.Time.DateAddDelta(start_date, 0, 3, 0))
        self.row_data[trade_id]['June'] = self.calculate_interest(acm.Time.DateAddDelta(start_date, 0, 3, 0),
                                                        acm.Time.DateAddDelta(start_date, 0, 4, 0))
        self.row_data[trade_id]['July'] = self.calculate_interest(acm.Time.DateAddDelta(start_date, 0, 4, 0),
                                                        acm.Time.DateAddDelta(start_date, 0, 5, 0))
        self.row_data[trade_id]['August'] = self.calculate_interest(acm.Time.DateAddDelta(start_date, 0, 5, 0),
                                                          acm.Time.DateAddDelta(start_date, 0, 6, 0))
        if self.end_month in [2, 12]:
            self.row_data[trade_id]['September'] = self.calculate_interest(acm.Time.DateAddDelta(start_date, 0, 6, 0),
                                                                 acm.Time.DateAddDelta(start_date, 0, 7, 0))
            self.row_data[trade_id]['October'] = self.calculate_interest(acm.Time.DateAddDelta(start_date, 0, 7, 0),
                                                               acm.Time.DateAddDelta(start_date, 0, 8, 0))
            self.row_data[trade_id]['November'] = self.calculate_interest(acm.Time.DateAddDelta(start_date, 0, 8, 0),
                                                                acm.Time.DateAddDelta(start_date, 0, 9, 0))
            self.row_data[trade_id]['December'] = self.calculate_interest(acm.Time.DateAddDelta(start_date, 0, 9, 0),
                                                                acm.Time.DateAddDelta(start_date, 0, 10, 0))
            self.row_data[trade_id]['January'] = self.calculate_interest(acm.Time.DateAddDelta(start_date, 0, 10, 0),
                                                               acm.Time.DateAddDelta(start_date, 0, 11, 0))
            self.row_data[trade_id]['February'] = self.calculate_interest(acm.Time.DateAddDelta(start_date, 0, 11, 0),
                                                                acm.Time.DateAddDelta(start_date, 0, 12, 0))
        self.row_data[trade_id]['closing_balance'] = abs(round(self.row_data[trade_id]['opening_balance'] - self.row_data[trade_id]['total_income_accrued'], 2))

        if self.is_vat_extract:
            self.row_data[trade_id]['closing_balance'] = abs(round(self.row_data[trade_id]['closing_balance'] + self.row_data[trade_id]['total_expense_inccured'], 2))

            if self.row_data[trade_id]['total_income_accrued'] == 0.0 and self.row_data[trade_id]['total_expense_inccured'] == 0.0:
                return
        else:
            if self.row_data[trade_id]['total_income_accrued'] == 0.0:
                return

        return self.row_data[trade_id]

    def set_opening_balance(self):

        amount = 0
        if self.trade.ValueDay() > self.start_date:
            return amount

        self.reset_global_variables(self.start_date, self.end_date)

        if self.row_data[self.trade.Oid()]['instype'] == 'Deposit':
            amount = float(self.calc_space.CalculateValue(self.trade, 'Current Nominal'))
        else:
            amount = float(self.calc_space.CalculateValue(self.trade, 'Trade Nominal'))

        if self.is_foreign_currency():
            amount = self.convert_to_zar(amount, self.end_date)
        return abs(amount)

    def convert_to_zar(self, amount, spot_date):

        curr = self.trade.Currency().Name()

        if curr in self.fx_rates:
            self.fx_rate = self.fx_rates[curr]
            fx_mount = amount * float(self.fx_rate)
            return fx_mount

        LOGGER.info('No Currency for Trade: %s' % self.trade.Name())
        return 0

    def is_foreign_currency(self):

        return not self.trade.Currency().Name() == self.local_currency

    def calculate_interest(self, month_start_date, month_end_date):

        self.reset_global_variables(month_start_date, month_end_date)

        accrued_interest = float(self.calc_space.CalculateValue(self.trade, 'Portfolio Accrued Interest'))
        settled_interest = float(self.calc_space.CalculateValue(self.trade, 'Portfolio Settled Interest'))
        total_interest = accrued_interest

        if not settled_interest == 0:
            total_interest = settled_interest + accrued_interest

        if self.is_foreign_currency():
            total_interest = self.convert_to_zar(total_interest, month_end_date)

        if not self.is_vat_extract:
            total_interest = total_interest if total_interest < 0 else 0.0

            if not total_interest:
                return

            self.row_data[self.trade.Oid()]['total_income_accrued'] += abs(total_interest)
            return abs(total_interest)

        if not total_interest:
            return

        if total_interest < 0:
            self.row_data[self.trade.Oid()]['total_income_accrued'] += abs(total_interest)
        else:
            self.row_data[self.trade.Oid()]['total_expense_inccured'] += abs(total_interest)

    def get_fx_rates(self):

        usd = acm.FInstrument['USD']
        usd_zar = usd.UsedPrice(self.end_date, self.local_currency, 'SPOT')

        for curr in self.currency_list:
            currency = acm.FInstrument[curr]
            curr_usd = usd.UsedPrice(self.end_date, currency, 'SPOT')

            if not curr_usd == 0.0:
                fx_rate = usd_zar / curr_usd
                self.fx_rates[currency.Name()] = fx_rate

        self.fx_rates[self.local_currency] = 1.0

    def reset_global_variables(self, start_date, end_date):

        self.calc_space.SimulateGlobalValue('Portfolio Profit Loss Start Date', 'Custom Date')
        self.calc_space.SimulateGlobalValue('Portfolio Profit Loss Start Date Custom', start_date)
        self.calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
        self.calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', end_date)


class ReportProcessor(object):

    column_headings = [{'header': 'TRADE_NUMBER'},
                       {'header': 'UNIQUE_IDENTIFIER'},
                       {'header': 'SOURCE_CODE'},
                       {'header': 'PRODUCT_TYPE'},
                       {'header': 'FUNDING_TYPE'},
                       {'header': 'ACCOUNT_NUMBER'},
                       {'header': 'PORTFOLIO_NAME'},
                       {'header': 'CURRENCY'},
                       {'header': 'FX_RATE'},
                       {'header': 'OPENING_BALANCE'},
                       {'header': 'ACCOUNT_START_DATE'},
                       {'header': 'CLOSING_BALANCE'},
                       {'header': 'ACCOUNT_CLOSE_DATE'},
                       {'header': 'BARCAP_EAGLE_SDID'},
                       {'header': 'TOTAL_INCOME_ACCRUED'},
                       {'header': 'TOTAL_EXPENSE_INCCURED'}]

    def __init__(self, start_date, end_date, vat_extract):

        self.start_date = start_date
        self.end_date = end_date
        self.column_titles = OrderedDict(defaultdict())
        self.sheet_name = 'VAT Data'

        if not vat_extract:
            self.sheet_name = 'IT3B Financial Data'
            self.column_headings = self.column_headings[:-1]
            self.append_month_columns()

    def append_month_columns(self):

        start_month = acm.Time.DateToYMD(self.start_date)[1]
        end_month = acm.Time.DateToYMD(self.end_date)[1]

        if self.column_headings[-1]['header'].endswith('_CR'):
            return

        if start_month > end_month:
            for i in range(start_month,13):
                self.column_headings.append({'header': calendar.month_name[i].upper()[:3] + '_CR'})

            for i in range(1,end_month+1):
                self.column_headings.append({'header': calendar.month_name[i].upper()[:3] + '_CR'})
        else:
            for i in range(start_month,end_month+1):
                self.column_headings.append({'header': calendar.month_name[i].upper()[:3] + '_CR'})
    
    def process_report_data(self, data):

        report_data = []
        if isinstance(data, OrderedDict) or isinstance(data, defaultdict) or isinstance(data, dict):
            
            for d in data.values():
                if isinstance(d, OrderedDict) or isinstance(d, defaultdict):
                    values = d.values()[:len(self.column_headings)]
                    report_data.append(values)
                else:
                    report_data.append(d)
            return report_data

    def validate_report_data(self, report_data):

        if len(report_data[0]) == len(self.column_headings):
            return
        raise Exception("Report headings and data are inconsistent")

    def generate_report(self, report_data, output_file):

        if not output_file:
            LOGGER.info("No open positions to report for %s. No report produced." %self.end_date)
            return

        if not isinstance(report_data, list):
            report_data = self.process_report_data(report_data)

        workbook = xlsxwriter.Workbook(output_file)
        sheet = workbook.add_worksheet(self.sheet_name)

        self.validate_report_data(report_data)

        number_of_columns = len(self.column_headings)

        if number_of_columns in range(1, 26):
            column_letter = list(zip(range(1, 27), string.ascii_uppercase))[number_of_columns-1][1]
        else:
            num_of_columns = number_of_columns - 26
            column_letter = list(zip(range(1, 27), string.ascii_uppercase))[num_of_columns-1][1]
            column_letter += column_letter

        sheet.add_table('A1:%s%s' %(column_letter, len(report_data) + 1), {'data': report_data, 'columns': self.column_headings})

        workbook.close()
    
        LOGGER.info('Report saved to . %s' % str(output_file))
