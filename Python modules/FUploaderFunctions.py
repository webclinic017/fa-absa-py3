"""---------------------------------------------------------------------------------------------------
MODULE
    FUploaderFunctions

DESCRIPTION
    Date                : 2018-10-25
    Purpose             : General module for PCT uploaders for easier
                          implementation of similar uploaders
    Department and Desk : PCG
    Requester           : Nhlanhleni Mchunu
    Developer           : Sihle Gaxa
    CR Number           : CHG1001014171

HISTORY
=======================================================================================================
Date            Change no       Developer               Description
-------------------------------------------------------------------------------------------------------
2018-10-25      CHG1001014171   Sihle Gaxa              Initial Implementation.
2018-12-03      CHG1001283051   Qaqamba Ntshobane       Added logic to help cater for files with 
                                                        unusual names, and changed name
2019-10-21      PCGDEV-84       Qaqamba Ntshobane       Made script more dynamic
2020-01-15      PCGDEV-656      Qaqamba Ntshobane       Changed name from FUploaderFunctions and
                                                        moved some global variables to FUploaderParams,
                                                        added create_payment, update_payment and
                                                        log_record_status
ENDDESCRIPTION
---------------------------------------------------------------------------------------------------"""
import os

import acm
import FBDPGui

from at_logging import getLogger
from collections import OrderedDict
from at_email import EmailHelper, RTB_EMAIL
from FUploaderParams import TODAY, CALENDAR, REPORT_STATUS

LOGGER = getLogger(__name__)
REPORT_DATA = OrderedDict()
TABLE_HEADINGS = {}


def get_ael_variables():

    import FRunScriptGUI
    from at_ael_variables import AelVariableHandler

    def enable_custom_date(ael_var):
        for var in variables:
            if var[0] == "custom_date":
                var.enabled = ael_var.value == "Custom Date"

    directory_selection = FRunScriptGUI.DirectorySelection()
    directory_selection.SelectedDirectory()
    variables = AelVariableHandler()
    variables.add("run_date",
                  label="Date:",
                  collection=sorted(get_start_day_config().keys()),
                  default="Now",
                  alt="Date for which the file should be run",
                  hook=enable_custom_date
                  )
    variables.add("custom_date",
                  label="Custom Date:",
                  default=TODAY,
                  mandatory=False,
                  alt="Enter file run date in the format YYY-MM-DD",
                  enabled=False
                  )
    variables.add("file_name",
                  label="File name:",
                  alt="File name prefix, \n"
                      "It will be followed by the date in %Y%m%d format"
                  )
    variables.add("file_path",
                  label="Directory:",
                  cls='string',
                  alt="Directory where files will be uploaded from \n"
                      "A date subfolder in the form yyyy-mm-dd will "
                      "be automatically added"
                  )
    variables.add("email_address",
                  label="Email Address:",
                  alt="Use a comma as a separator",
                  multiple=True
                  )

    variables.extend(FBDPGui.LogVariables())

    return variables


def get_start_day_config():

    # Generate date options to be used as drop downs in the GUI
    return {
            "Inception": acm.Time.DateFromYMD(1970, 1, 1),
            "First Of Year": acm.Time.FirstDayOfYear(TODAY),
            "First Of Month": acm.Time.FirstDayOfMonth(TODAY),
            "PrevBusDay": CALENDAR.AdjustBankingDays(TODAY, -1),
            "TwoBusinessDaysAgo": CALENDAR.AdjustBankingDays(TODAY, -2),
            "TwoDaysAgo": acm.Time.DateAddDelta(TODAY, 0, 0, -2),
            "Yesterday": acm.Time.DateAddDelta(TODAY, 0, 0, -1),
            "Custom Date": TODAY,
            "Now": TODAY,
            }


def get_input_date(dictionary, adjust_banking_day=True):

    if dictionary["run_date"] == "Custom Date":
        date_string = dictionary["custom_date"]
    else:
        date_string = get_start_day_config()[dictionary["run_date"]]

    try:
        run_date = acm.Time().DateAdjustPeriod(TODAY, date_string)
    except:
        run_date = str(acm.Time.DateAddDelta(date_string, 0, 0, 0))

    if CALENDAR.IsNonBankingDay(None, None, run_date) and adjust_banking_day:
        run_date = CALENDAR.AdjustBankingDays(run_date, 1)
    return run_date


def process_csv_file(dictionary, class_name, trades=None, adj_banking_day=True):

    import csv

    run_date = get_input_date(dictionary, adj_banking_day)
    csv_file = get_file_path(dictionary, run_date)
    report_row_number = 1

    if csv_file:
        with open(csv_file) as file:
            data = [row for row in csv.reader(file)]
            class_name(file, run_date, data, trades, report_row_number)


def process_xls_file(dictionary, class_name, trades=None, adj_banking_day=True):

    import xlrd

    run_date = get_input_date(dictionary, adj_banking_day)
    xls_file = get_file_path(dictionary, run_date)
    report_row_number = 1

    if xls_file:
        with xlrd.open_workbook(xls_file) as workbook:
            sheet = workbook.sheet_by_index(0)
            class_name(xls_file, run_date, sheet, trades, report_row_number)


def process_standard_file(class_name, dictionary, add_info_spec=None, adj_banking_day=True):

    from at_feed_processing import notify_log

    run_date = get_input_date(dictionary, adj_banking_day)
    directory = get_file_path(dictionary, run_date)
    report_row_number = 1

    if directory:
        processor = class_name(directory, run_date, report_row_number)
        processor.add_error_notifier(notify_log)
        processor.process(False)
        return True
    return False


def get_file_path(dictionary, run_date):

    import glob

    file_directory = str(dictionary["file_path"])
    file_name = dictionary["file_name"]
    file_date = run_date.replace("-", "")
    date_file_name = "%s%s.csv" % (file_name, file_date)
    xls_date_file_name = "%s%s" % (file_name, file_date)
    csv_file_path = "%s.csv" % os.path.join(file_directory, run_date, file_name)
    xls_file_path = "%s.xls" % os.path.join(file_directory, run_date, xls_date_file_name)
    date_file_path = os.path.join(file_directory, run_date, date_file_name)

    try:
        if os.path.exists(date_file_path):
            LOGGER.info("Loading file: %s" % date_file_path)
            return date_file_path
        elif os.path.exists(csv_file_path):
            LOGGER.info("Loading file: %s" % csv_file_path)
            return csv_file_path
        elif os.path.exists(xls_file_path):
            LOGGER.info("Loading file: %s" % xls_file_path)
            return xls_file_path
        else:
            ''' add wildcard to file name to cater for files
            with trailing values after date
            '''
            directory = "%s\%s\%s%s" % (file_directory, run_date, file_name, file_date)
            file_path = glob.glob("%s*.csv" % directory)[0]

            LOGGER.info("Loading file: %s" % file_path)
            return file_path
    except:
        row_info_list = ["ERROR", REPORT_STATUS['failure_status'], REPORT_STATUS['file_error']]
        add_row("ERROR", row_info_list)
        
        LOGGER.error("File path %s\%s\%s does not exist"
                    % (file_directory, run_date, file_name))


def add_cashflow(trade_cashflow, cashflow_type, cashflow_nominal, cashflow_date,
                 add_info_spec=None, add_info_value=None, cashflow_nominal_factor=1):

    # adds daily collateral amount to cashflow table
    instrument_leg = trade_cashflow.Instrument().Legs()[0]
    cashflow = acm.FCashFlow()
    cashflow.Leg(instrument_leg)
    cashflow.CashFlowType(cashflow_type)
    cashflow.FixedAmount(cashflow_nominal)
    cashflow.NominalFactor(cashflow_nominal_factor)
    cashflow.PayDate(cashflow_date)
    if add_info_spec and add_info_value:
        cashflow.AddInfoValue(add_info_spec, add_info_value)

    if cashflow_nominal == 0.00:
        return REPORT_STATUS["zero_margin"]
    else:
        try:
            cashflow.Commit()
            LOGGER.info("Cashflow add info %s:%s successfully added to trade %i"
                        % (add_info_spec, add_info_value, trade_cashflow.Oid()))
            return REPORT_STATUS["success_status"]
        except Exception as e:
            LOGGER.exception("Could not add cashflow for trade %i : %s"
                        % (trade_cashflow.Oid(), str(e)))
            return REPORT_STATUS["booking_error"]


def is_duplicate_cashflow(trade_object, margin, run_date):

    cashflows = existing_cashflows(trade_object, run_date)

    if round(margin, 4) in cashflows:
        return True
    return False


def existing_cashflows(trade_object, run_date):

    calc_space = acm.Calculations().CreateStandardCalculationsSpaceCollection()
    money_flows = trade_object.MoneyFlows()
    cashflows = []

    for money_flow in money_flows:
        money_flow_amount = money_flow.Calculation().Projected(calc_space).Number()
        money_flow_type = money_flow.Type()
        money_flow_payday = money_flow.PayDay()

        if (money_flow_type == 'Fixed Amount' and money_flow_payday == run_date):
            cashflows.append(round(money_flow_amount, 4))
    return cashflows


def upload_payment(payment_type, trade_object, amount, date, payment_description):

    trade_payment = [payment for payment in trade_object.Payments()
                     if payment.Type() == payment_type and
                     payment.Text() == payment_description and
                     payment.PayDay() == date]

    if trade_payment:
        trade_payment = trade_payment[0]
        update_payment(trade_object, trade_payment, amount, payment_type, payment_description, date)
        return

    create_payment(trade_object, amount, payment_type, payment_description, date)


def create_payment(trade, amount, type, payment_text, date):

    payment = acm.FPayment()
    trade.Payments().Add(payment)
    update_payment(trade, payment, amount, type, payment_text, date)


def update_payment(trade, payment, amount, type, payment_text, date):

    payment.Amount(amount)
    payment.Text(payment_text)  # max 19 chars
    payment.Currency(trade.Instrument().Currency().Name())
    payment.Type(type)
    payment.Party(trade.Counterparty())
    payment.PayDay(date)
    payment.ValidFrom(date)
    payment.Commit()


def add_row(report_row_number, row_info_list):

    row_data = ''
    open_row = '<tr>'
    close_row = '</tr>'

    open_data_tag = '<td>'
    close_data_tag = '</td>'

    for row_info in row_info_list:
        row_data = row_data + open_data_tag + row_info + close_data_tag

    report_row = open_row + row_data + close_row
    REPORT_DATA[report_row_number] = report_row

    return REPORT_DATA


def add_header(table_headings_list):

    table_headings = ''
    open_row = '<tr>'
    close_row = '</tr>'

    open_header_tag = '<th>'
    close_header_tag = '</th>'
    
    table_headings = open_header_tag + table_headings + close_header_tag

    for table_heading in table_headings_list:
        table_headings = table_headings + open_header_tag + table_heading + close_header_tag

    header_row = open_row + table_headings + close_row
    TABLE_HEADINGS[len(table_headings_list)+1] = header_row

    return TABLE_HEADINGS


def create_report(report_header, table_headers=list(TABLE_HEADINGS.values()), content=REPORT_DATA):

    report_content = ''
    col_span = list(TABLE_HEADINGS.keys())[0] if list(TABLE_HEADINGS.keys()) else 7

    if list(content.values()) and ("ERROR" or "SUCCESS" in list(content.values())[0]):
        table_headers = ''
    elif not table_headers and list(TABLE_HEADINGS.values()):
        table_headers = list(TABLE_HEADINGS.values())

    if len(table_headers) > 0:
        table_headers = table_headers[0]
    else:
        table_headers = ''

    for row in list(content.keys()):
        report_content = report_content + content[row]

    report = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
            "http://www.w3.org/TR/html4/strict.dtd">
            <html dir="ltr" lang="en">
            <head>
                <meta http-equiv="content-type" content="text/html; charset=utf-8">
                <meta http-equiv="content-style-type" content="text/css">
                <title></title>
                <style type="text/css">
                    table {
                        border-collapse: collapse;
                        width: 1000px;
                        font-family: Arial, Brave Sans, sans-serif;
                    }
                    th, td {
                        text-align: left;
                        padding: 8px;
                        border: 1px solid #ddd;
                    }
                    th {
                        font-size: 20;
                        background-color: #dc0032;
                        color: white;
                    }
                    h1 {
                        text-align: center;
                        width: 1000px;
                        color: 	#870032;
                        font-size: 30;
                    }
                    td {
                        font-size: 12;
                    }
                    .main_header {
                        text-align: center;
                        background-color: #870032;
                        width: 1000px;
                        font-size: 30;
                    }
                </style>
            </head>
            <body>
                <table>
                    <th class="main_header" colspan="%s">%s</th>
                    %s
                    %s
                </table>
            </body>
            </html>''' % (col_span, report_header, table_headers, report_content)
    return report


def send_email(body, subject, email_addresses, email_sender):

    if not email_sender:
        email_sender=RTB_EMAIL

    email_helper = EmailHelper(body, subject, list(email_addresses),
                               email_sender)

    email_helper.sender_type = EmailHelper.SENDER_TYPE_SMTP
    email_helper.host = EmailHelper.get_acm_host()
    try:
        email_helper.send()
    except Exception as e:
        LOGGER.error(e)


def send_report(email_address, email_sender, email_subject, report_header, adj_banking_day=True):

    report = create_report(report_header)

    LOGGER.info('Sending emails')
    send_email(report, email_subject, email_address, email_sender)
    REPORT_DATA.clear()
    TABLE_HEADINGS.clear()


def get_ins_name(trade_oid):

    instrument = '-'

    if trade_oid != '-':
        instrument = acm.FTrade[trade_oid].Instrument().Name()
    return instrument


def log_record_status(row_number, account, status, comment, trade_oid='-', margin='-', prev_margin=0):

    if comment == 'margin_updated':
        comment = REPORT_STATUS[comment] % prev_margin
    elif comment != '':
        comment = REPORT_STATUS[comment]

    row_info_list = [str(row_number),
                     str(account),
                     get_ins_name(trade_oid),
                     str(trade_oid), 
                     REPORT_STATUS[status],
                     str(margin),
                     comment]
    add_row(row_number, row_info_list)

