'''-------------------------------------------------------------------------------------------------
MODULE
    fatca_crs_fin_data_extract

DESCRIPTION
    Date      : 2021-03-18
    Purpose   : Extract for FATCA/CRS reporting to SARS
    Developer : Qaqamba Ntshobane
    Requester : Daveshin Chetty
    Department: PCG

=======================================================================================================
HISTORY:
    Date:               Change No:      Developer:              Description:   
-------------------------------------------------------------------------------------------------------
    2021-03-18          PCGDEV-686      Qaqamba Ntshobane       Initial Design

ENDDESCRIPTION
----------------------------------------------------------------------------------------------------'''

import os
import acm
import xlrd
import xlsxwriter
import FRunScriptGUI

from at_logging import getLogger
from at_ael_variables import AelVariableHandler
from collections import defaultdict, OrderedDict
from sars_reporting_functions import (get_val_end, get_cash_end, get_accrued_interest, get_settled_interest,
                                        get_closing_balance, get_account_number, ins_expires_in_period_,
                                        get_instrument_start_date, get_instrument_end_date, get_period_dates,
                                        send_success_notification, get_moneyflows, CALENDAR)


LOGGER = getLogger(__name__)
fileFilter = 'XLSX Files (*.xlsx)|*.xlsx|XLS Files (*.xls)|*.xls|CSV Files (*.csv)|*.csv|'
inputFile = FRunScriptGUI.InputFileSelection(FileFilter=fileFilter)

directorySelection = acm.FFileSelection()
directorySelection.PickDirectory(True)
directorySelection.SelectedDirectory(r'F:')

CALC_SPACE = acm.FCalculationMethods().CreateCalculationSpace(acm.GetDefaultContext(), 'FDealSheet')

PREMIUM_TYPES = ['Premium', 'Premium 2', 'Payment Premium', 'Aggregated Forward Premium']
DIVIDEND_TYPES = ['Dividend', 'Cashflow Dividend', 'Dividend Transfer', 'Scrip Dividend']
REPORT_HEADINGS = ['Client Name', 'Trade nr', 'Client LE SDS ID', 'Account nr', 'Account opened date', 
                    'Account closed status Y/N', 'Account closed date', 'Dividends', 'Dividends Currency code', 
                    'Interest', 'Interest Currency code', 'Gross proceeds', 'Gross Proceeds Currency code', 'Other', 
                    'Other Currency code', 'Closing Balance', 'Currency code']

ael_variables = AelVariableHandler()
ael_variables.add(
    'report_date',
    label='Report Date',
    default=acm.Time.DateToday(),
    mandatory=True
    )
ael_variables.add(
    'input_file',
    label='Reportable Clients',
    cls=inputFile,
    default=inputFile,
    mandatory=True,
    multiple=True,
    alt='Input file in CSV or XLS format.'
    )
ael_variables.add(
    'output_file_dir',
    label = 'File Drop Location',
    cls = directorySelection,
    default = directorySelection,
    multiple = True
    )
ael_variables.add(
    'email_address',
    label='Email Addresses',
    default='CIBPCGTaxReporting@groups.absa.africa',
    mandatory=False,
    multiple=True,
    alt='Email results to these recipients'
    )


def get_reportable_clients(xls_file):

    query = acm.CreateFASQLQuery(acm.FParty, 'AND')
    party_node = query.AddOpNode('OR')

    if xls_file:
        with xlrd.open_workbook(xls_file) as workbook:
            sheet = workbook.sheet_by_index(0)

        for r in range(1, sheet.nrows):
            le_sdsid = sheet.cell(r, 2).value

            if le_sdsid:
                le_sdsid = str(le_sdsid).split('.')
                party_node.AddAttrNode('AdditionalInfo.BarCap_SMS_LE_SDSID', 'EQUAL', le_sdsid[0])

    return query.Select()


def get_trades(party, report_end_date):

    trades = acm.FTrade.Select('counterparty={0} and '
                                'valueDay<="{1}" and '
                                'status<>"{2}" and '
                                'status<>"{3}" and '
                                'status<>"{4}" and '
                                'portfolio<>"{5}" and '
                                'portfolio<>"{6}" and '
                                'portfolio<>"{7}"'.format(party.Oid(),
                                                            report_end_date,
                                                            'Void', 'Simulated', 'Terminated',
                                                            'GRAVEYARD', 'TESTING', 'MIDAS_GY'))
    trades = [trade for trade in trades if ins_expires_in_period_(trade.Instrument(), report_end_date)]
    return trades


class TradesProcessor(object):

    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.row_data = OrderedDict()

    def process(self, client, trades):

        self.row_data.clear()

        for trade in trades:
            balance = 0.0
            currency = 'ZAR'
            trade_id = trade.Oid()

            end_date = get_instrument_end_date(trade, self.end_date)
            end_date = acm.Time.DateAddDelta(end_date, 0, 0, -1)
            
            if trade.Instrument().IsCallAccount():
                balance = -1 * get_closing_balance(trade, self.start_date, self.end_date)

            self.moneyflows = get_moneyflows(trade, self.start_date, self.end_date)

            self.row_data.setdefault(trade_id, OrderedDict())

            self.row_data[trade_id]['client_name'] = client.Name()
            self.row_data[trade_id]['trade_number'] = trade.Oid()
            self.row_data[trade_id]['client_le_sdsid'] = client.AdditionalInfo().BarCap_SMS_LE_SDSID()
            self.row_data[trade_id]['account_number'] = get_account_number(trade.MoneyFlows())
            self.row_data[trade_id]['account_opening_date'] = get_instrument_start_date(trade)
            self.row_data[trade_id]['account_closure_status'] = trade.Instrument().IsExpired()
            self.row_data[trade_id]['account_closure_date'] = end_date
            self.row_data[trade_id]['dividends'] = self.get_dividends()
            self.row_data[trade_id]['dividends_currency'] = currency
            self.row_data[trade_id]['interest'] = self.get_interest(trade)
            self.row_data[trade_id]['interest_currency'] = currency
            self.row_data[trade_id]['gross_proceeds'] = self.get_gross_proceeds(trade)
            self.row_data[trade_id]['gross_proceeds_currency'] = currency
            self.row_data[trade_id]['other'] = self.get_payments()
            self.row_data[trade_id]['other_currency'] = currency
            self.row_data[trade_id]['closing_balance'] = balance
            self.row_data[trade_id]['currency'] = currency
            
            if (self.row_data[trade_id]['dividends'] == self.row_data[trade_id]['interest'] == 0 and
                self.row_data[trade_id]['gross_proceeds'] == self.row_data[trade_id]['closing_balance'] == 0):
                self.row_data.pop(trade_id)

        return self.row_data

    def get_moneyflow(self, mf_type):

        mf_amount = 0
        mf_types = self.moneyflows.keys()

        if mf_type in mf_types:
            mf_amount = self.moneyflows.pop(mf_type)
        return mf_amount

    def get_dividends(self):

        dividends = 0

        for dividend_type in DIVIDEND_TYPES:
            dividends += self.get_moneyflow(dividend_type)
        return -1 * dividends

    def get_interest(self, trade):

        accrued_interest = get_accrued_interest(trade, self.start_date, self.end_date)
        settled_interest = get_settled_interest(trade, self.start_date, self.end_date)
        total_interest = accrued_interest

        if settled_interest:
            total_interest = (settled_interest + accrued_interest)
        return -1 * total_interest if total_interest < 0 else 0

    def get_gross_proceeds(self, trade):

        proceeds = 0

        if trade.Bought():
            for premium_type in PREMIUM_TYPES:
                proceeds += self.get_moneyflow(premium_type)
        return -1 * proceeds

    def get_payments(self):
    
        payments = sum([amount for amount in self.moneyflows.values()])
        return -1 * payments


class ReportProcessor(object):

    def __init__(self, output_file_dir):

        self.output_file_dir = output_file_dir

    @staticmethod
    def process_headers():

        return [{'header':str(head)} for head in REPORT_HEADINGS]

    @staticmethod
    def process_report_data(data, len_headers):

        report_data = []

        for d in data.values():
            values = d.values()[:len_headers]
            report_data.append(values)
        return report_data

    @staticmethod
    def aggregate_data(start_date, end_date, data):

        divs = 0
        interest = 0
        proceeds = 0
        payments = 0
        balance = 0
        opening = start_date
        closing = end_date

        aggregated = data.values()[0].values()
        aggregated.pop(1)

        for row in data.values():
             divs += row['dividends']
             interest += row['interest']
             proceeds += row['gross_proceeds']
             payments += row['other']
             balance += row['closing_balance']
             acc_number = row['account_number'] if row['account_number'] != 'N/A' else row['trade_number']
             opening = row['account_opening_date'] if row['account_opening_date'] < opening else opening
             closing = row['account_closure_date'] if row['account_closure_date'] < closing else closing
             acc_closure_status = 'FALSE' if closing == end_date else 'TRUE'
        
        aggregated[2] = str(acc_number)
        aggregated[3] = opening
        aggregated[4] = acc_closure_status
        aggregated[5] = closing
        aggregated[6] = divs
        aggregated[8] = interest
        aggregated[10] = proceeds
        aggregated[12] = payments
        aggregated[14] = balance
        return aggregated

    def create_report(self, data):

        aggr_headers = []
        headers = self.process_headers()
        workbook = xlsxwriter.Workbook(self.output_file_dir)

        aggregated_fatca_crs_sheet = workbook.add_worksheet('FATCA_CRS Aggregated Data')
        detailed_fatca_crs_sheet = workbook.add_worksheet('FATCA_CRS Trade Level Data')

        aggr_headers.extend(headers)
        aggr_headers.pop(1)

        return workbook, detailed_fatca_crs_sheet, aggregated_fatca_crs_sheet, headers, aggr_headers

    def add_to_report(self, sheet, headers, data):

        last_row = len(data) + 1
        last_column = xlsxwriter.utility.xl_col_to_name(len(headers)-1)
        sheet.add_table('A1:%s%s' %(last_column, last_row), {'data': data, 'columns': headers})

    def close_report(self, workbook):

        workbook.close()
        LOGGER.info('Report saved to . %s' % str(self.output_file_dir))


def ael_main(dictionary):

    input_file = str(dictionary['input_file'])
    output_file_dir = str(dictionary['output_file_dir'])
    report_date = dictionary['report_date']
    LOGGER.info('Processing input file: %s', input_file)
    
    report_run_date = list(filter(str.isdigit, report_date))
    report_name = 'FATCA_CRS_Financial_Data_{0}.xlsx'.format(report_run_date)
    report_path = os.path.join(output_file_dir, report_name)

    start_date, end_date = get_period_dates(report_date)

    processor = TradesProcessor(start_date, report_date)

    client_data = []
    aggr_data = []
    report_processor = ReportProcessor(report_path)

    wb, det_sheet, aggr_sheet, headers, aggr_headers = report_processor.create_report(client_data)
    reportable_clients = get_reportable_clients(input_file)

    for index, client in enumerate(reportable_clients):
        record = index + 1
        percentage = float(record) / len(reportable_clients)
        percentage = int(percentage * 100)

        trades = get_trades(client, end_date)

        LOGGER.info('>>> {time} PROCESSING {tot_trades} TRADE(S) FROM CLIENT {client_name}: {rec} OF {tot_clients} ({perc}%)'.format(
                                                        time=acm.Time.TimeNow().split('.')[0],
                                                        tot_trades=len(trades),
                                                        client_name=client.Name(),
                                                        rec=record,
                                                        tot_clients=len(reportable_clients),
                                                        perc=percentage))
        if not trades:
            continue

        client_data_container = processor.process(client, trades)
        if not client_data_container:
            continue
        aggregated_data = ReportProcessor.aggregate_data(start_date, end_date, client_data_container)
        flattened_data = ReportProcessor.process_report_data(client_data_container, len(headers))

        aggr_data.append(aggregated_data)
        client_data.extend(flattened_data)

    report_processor.add_to_report(det_sheet, headers, client_data)
    report_processor.add_to_report(aggr_sheet, aggr_headers, aggr_data)
    report_processor.close_report(wb)

    email_addresses = dictionary['email_address']
    send_success_notification(email_addresses, 'FATCA/CRS', report_name)

    LOGGER.info('Completed successfully.')
