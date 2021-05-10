'''----------------------------------------------------------------------------------------------
MODULE
    initial_margin_uploader

DESCRIPTION
    Date                : 2016-11-15
    Purpose             : Uploads daily initial margin from GCMS files.
    Department and Desk : PCG and Prime Services
    Requester           : Helen Comninos
    Developer           : Paseka Motsoeneng, Sihle Gaxa

HISTORY
==================================================================================================
Date            Change no       Developer               Description
--------------------------------------------------------------------------------------------------
2017-10-17      CHNG0005044945  Sihle Gaxa              Added funding interest as payment on the
                                                        trade
2019-01-14      CHG1001283051   Qaqamba Ntshobane       Script redesign
2019-10-21      PCGDEV-84       Qaqamba Ntshobane       Amended script for a more dynamic 
                                                        FUploaderFunctions
2020-10-13      PCGDEV-531      Sihle Gaxa              Added new sender to fix email notification
2021-01-15      PCGDEV-656      Qaqamba Ntshobane       Changed script name from safex_initial_margin_uploader,
                                                        and updated code design so it can can upload
                                                        initial margin for yieldx and CDM accounts

ENDDESCRIPTION
-----------------------------------------------------------------------------------------------'''

import acm

from at_logging import getLogger
from FCallDepositFunctions import adjust, backdate
from PS_CallAccountSweeperFunctions import IsCurrentInterestPeriod
from FUploaderFunctions import (get_ael_variables, existing_cashflows, upload_payment,
                                get_input_date, add_header, process_csv_file,
                                send_report, log_record_status)
from FUploaderParams import (TABLE_HEADINGS, REPORT_HEADING_ITAC, REPORT_HEADING_YIELDX,
                             REPORT_HEADING_AGRIS, EMAIL_SENDER, EMAIL_SUBJECT_ITAC,
                             EMAIL_SUBJECT_YIELDX, EMAIL_SUBJECT_AGRIS, SUBACCOUNT_INDEX, 
                             MEMBER_MARGIN_INDEX, CLIENT_MARGIN_INDEX, FUNDING_INTEREST_INDEX,
                             TOTAL_DIV_INDEX, PAYMENT_TYPE, FUNDING_TEXT, DIVIDEND_TEXT, TODAY)

CALC_SPACE_COLLECTION = acm.Calculations().CreateStandardCalculationsSpaceCollection()
ael_variables = get_ael_variables()
LOGGER = getLogger(__name__)


class InitialMarginUploader():

    data_row = 9

    def __init__(self, file_path, run_date, file_data, trades, report_row_number):

        self.file_path = file_path
        self.run_date = run_date
        self.file_data = file_data
        self.trades = trades
        self.report_row_number = report_row_number

        # process every row after the 9th in the file
        for row in file_data[self.data_row:]:
            self.data_clean_up(row)
            if (self.file_data and self.file_data[0] == '' or
                self.file_data == [] or
                file_data[self.data_row] == 'Total'):
                break

            subaccount_code = self.file_data[SUBACCOUNT_INDEX]
            call_account = acm.FInstrument.Select01('externalId1 = %s' % subaccount_code, None)

            if not call_account:
                continue

            self._process_record(subaccount_code, call_account)
            self.report_row_number += 1
            self.data_row += 1

    def data_clean_up(self, row):

        self.file_data = [data.replace('(', '-').replace(')', '') for data in row]

    def _process_record(self, account, call_account):

        trades = call_account.Trades()
        if not trades:
            log_record_status(self.report_row_number, account, 'failure_status', 'missing_trade_error')
            LOGGER.warning('No trade booked for call account with External Id %s' % account)
            return

        margin = 0
        difference = 0
        existing_margin = 0
        trade_object = trades[0]
        trade_oid = trade_object.Oid()

        if trade_object.Status() in ('Void', 'Simulated', 'Terminated'):
            log_record_status(self.report_row_number, account, 'failure_status', 'status_error', trade_oid)
            LOGGER.exception('Failed: Trade %d is in %s status' % (trade_oid, trade_object.Status()))
            return

        self.add_payment(trade_object)

        if len(account) < 6:
            margin = -1 * float(self.file_data[MEMBER_MARGIN_INDEX])
        else:
            margin = -1 * float(self.file_data[CLIENT_MARGIN_INDEX])

        rundate_cashflows = existing_cashflows(trade_object, self.run_date)

        if rundate_cashflows:
            existing_margin = sum(rundate_cashflows)
            difference = margin - existing_margin

        if not margin:
            log_record_status(self.report_row_number, account, 'skipped_status', 'zero_margin', trade_oid)
            return

        if (round(margin, 4) in rundate_cashflows or
            round(difference, 4) in rundate_cashflows or 
            margin == sum(rundate_cashflows)):

            log_record_status(self.report_row_number, account, 'skipped_status', 'duplicate_moneyflow', trade_oid)
            LOGGER.info('Skipping existing cashflow amount %d for %i' % (margin, trade_oid))
            return

        if difference:
            margin = difference

        adjusted = None
        if IsCurrentInterestPeriod(call_account, self.run_date):
            adjusted = adjust(call_account, margin, self.run_date,
                               "Prevent Settlement", None, None, 1)
        else:
            adjusted = backdate(call_account, margin, self.run_date, TODAY,
                                 "Prevent Settlement", None, None, 1)

        if adjusted:
            if difference:
                log_record_status(self.report_row_number, account, 'updated_status', 'margin_updated', trade_oid, margin, existing_margin)
            else:
                log_record_status(self.report_row_number, account, 'success_status', '', trade_oid, margin)
            LOGGER.info('Margin %d uploaded to trade %s' % (margin, trade_oid))

    def add_payment(self, trade):

        if 'Initial Margin' not in trade.add_info('Account_Name'):
            return

        funding_amount = -1 * float(self.file_data[FUNDING_INTEREST_INDEX])
        dividend_amount = -1 * self.file_data[TOTAL_DIV_INDEX]

        upload_payment(PAYMENT_TYPE, trade, funding_amount, self.run_date, FUNDING_TEXT)
        upload_payment(PAYMENT_TYPE, trade, dividend_amount, self.run_date, DIVIDEND_TEXT)


def ael_main(dictionary):

    email_addresses = dictionary['email_address']
    file_name = dictionary['file_name']
    run_date = get_input_date(dictionary, adjust_banking_day=True)

    add_header(TABLE_HEADINGS)
    process_csv_file(dictionary, InitialMarginUploader)

    if 'ITAC' in file_name:
        send_report(email_addresses, EMAIL_SENDER, EMAIL_SUBJECT_ITAC %run_date, REPORT_HEADING_ITAC)
    if 'YIELDX' in file_name:
        send_report(email_addresses, EMAIL_SENDER, EMAIL_SUBJECT_YIELDX %run_date, REPORT_HEADING_YIELDX)
    if 'CDM' in file_name:
        send_report(email_addresses, EMAIL_SENDER, EMAIL_SUBJECT_AGRIS %run_date, REPORT_HEADING_AGRIS)

    LOGGER.info("Completed successfully.")
