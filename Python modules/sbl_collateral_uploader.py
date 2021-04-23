"""----------------------------------------------------------------------------
MODULE
    sbl_collateral_uploader

DESCRIPTION
    Date                : 2018-10-25
    Purpose             : Uploads daily sbl collateral amounts from a flat file
                          from GlobalOne portal.
    Department and Desk : PCG
    Requester           : Nhlanhleni Mchunu
    Developer           : Sihle Gaxa
    CR Number           : CHG1001014171

HISTORY
===============================================================================
Date            Change no       Developer               Description
-------------------------------------------------------------------------------
2018-10-25      CHG1001014171   Sihle Gaxa              Initial Implementation
2019-01-14      CHG1001283051   Qaqamba Ntshobane       Script redesign
2019-05-23      CHG1001765411   Sihle Gaxa              Removed duplicate check
                                                        and email only sent if
                                                        source file found
2019-06-04      CHG1001835557   Sihle Gaxa              Re-instated duplicate
                                                        validation
2019-10-21      PCGDEV-84       Qaqamba Ntshobane       Amended script for a 
                                                        more dynamic 
                                                        FUploaderFunctions

ENDDESCRIPTION
----------------------------------------------------------------------------"""
import os
import acm
import datetime
import FRunScriptGUI

import FUploaderFunctions
from at_logging import getLogger
from at_ael_variables import AelVariableHandler
from at_feed_processing import (SimpleCSVFeedProcessor,
                                SimpleXLSFeedProcessor,
                                notify_log)
from FUploaderParams import REPORT_STATUS

LOGGER = getLogger(__name__)
CALC_SPACE = acm.Calculations().CreateStandardCalculationsSpaceCollection()
FILE_FILTER = "CSV Files (*.csv)|*.csv|XLS Files (*.xls)|*.xls|XLSX Files (*.xlsx)|*.xlsx|"
INPUT_FILE = FRunScriptGUI.InputFileSelection(FileFilter=FILE_FILTER)


ael_variables = AelVariableHandler()
ael_variables.add(
    'input_file',
    label='File',
    cls=INPUT_FILE,
    mandatory=False,
    multiple=True,
    alt='Input file in CSV or XLS format.'
    )
ael_variables.add(
    'email_address',
    label='Email address',
    mandatory=False,
    multiple=True,
    alt='Email results to these recipients'
    )

class SBLCashflowUploader(object):

    amount_col = 'Amount'
    counterparty_col = 'Cpty'
    cashflow_paydate_col = 'Payday'
    trade_number_col = 'TradeNumber'

    def __init__(self):
        self._dict_reader_kwargs = {'delimiter': ','}
        self.report_row_number = 1
    
    def _validate_input_and_return_amount(self, cashflow_amount, external_id, trade_number):
                
        ext_id = external_id if external_id else '-'
        trd_number = trade_number if trade_number else '-'
        
        try:
            amount = float(cashflow_amount)
            
            if external_id and amount:
                LOGGER.info('%s processing %s %s', '-' * 20, external_id, '-' * 20)                
            elif trade_number and amount:
                LOGGER.info('%s processing %s %s', '-' * 20, trade_number, '-' * 20)
            return amount
            
        except ValueError as e:
            LOGGER.info("Amount %s needs to be a valid number" % cashflow_amount)
            row_info_list = [str(self.report_row_number), ext_id, trd_number,
                             REPORT_STATUS['failure_status'], '-', '-',
                             REPORT_STATUS['amount_error']]
            FUploaderFunctions.add_row(self.report_row_number, row_info_list)

            self.report_row_number += 1
            return

    def _process_record(self, record, dry_run):

        settle_type = None
        sbl_instrument = None
        (_index, record_data) = record
        external_id = record_data[self.counterparty_col]
        trade_number = record_data[self.trade_number_col]
        cashflow_amount = record_data[self.amount_col].replace(",", "")        
        amount = self._validate_input_and_return_amount(cashflow_amount, external_id, trade_number)
        
        if not amount:
            return

        try:
            if external_id:
                sbl_instrument = acm.FInstrument.Select01('externalId1 = %s' % external_id, None)

                if not sbl_instrument:
                    row_info_list = [str(self.report_row_number), str(external_id), '-',
                                     REPORT_STATUS['failure_status'], '-', '-',
                                     REPORT_STATUS['externalId_error']]
                    FUploaderFunctions.add_row(self.report_row_number, row_info_list)

                    self.report_row_number += 1
                    LOGGER.warning('Sbl collateral instrument with External Id %s not found' % external_id)
                    return
                else:
                        trades = sbl_instrument.Trades()

                        if trades:
                            sbl_trade = trades[0]
                            trade_oid = sbl_trade.Oid()
                        else:
                            row_info_list = [str(self.report_row_number), str(external_id), 'No trade',
                                             REPORT_STATUS['failure_status'], '-', '-',
                                             REPORT_STATUS['missing_trade_error']]
                            FUploaderFunctions.add_row(self.report_row_number, row_info_list)

                            self.report_row_number += 1
                            LOGGER.warning('No trade booked for instrument with External Id %s' % external_id)
                            return
            else:
                sbl_trade = acm.FTrade[str(trade_number.replace(",", ""))]
                if sbl_trade:
                    trade_oid = sbl_trade.Oid()
                    settle_type = 'Internal'
                else:
                    row_info_list = [str(self.report_row_number), str(external_id), 'No trade',
                                     REPORT_STATUS['failure_status'], '-', '-',
                                     REPORT_STATUS['trade_error']]
                    FUploaderFunctions.add_row(self.report_row_number, row_info_list)

                    self.report_row_number += 1
                    return

            file_date = record_data[self.cashflow_paydate_col]
            cashflow_paydate = acm.Time.DateAddDelta(file_date, 0, 0, 0)

            if sbl_trade.Status() not in ('Void', 'Simulated', 'Terminated'):

                # Checking that cashflow is not a duplicate
                is_duplicate = FUploaderFunctions.is_duplicate_cashflow(sbl_trade, amount, cashflow_paydate)

                if is_duplicate:
                    row_info_list = [str(self.report_row_number), str(external_id), str(trade_oid),
                                     REPORT_STATUS['failure_status'], str(amount),
                                     cashflow_paydate, REPORT_STATUS['duplicate_moneyflow']]
                    FUploaderFunctions.add_row(self.report_row_number, row_info_list)

                    self.report_row_number += 1
                    LOGGER.info('Skipping existing cashflow amount %d for %i' % (amount, trade_oid))
                    return

                # Uploading cashflow
            
                LOGGER.info('Uploading cashflow for %s' % trade_oid)
                if settle_type:
                    is_uploaded = FUploaderFunctions.add_cashflow(sbl_trade, 'Fixed Amount', amount, cashflow_paydate,
                                                                "Settle_Type", settle_type)
                else:
                    is_uploaded = FUploaderFunctions.add_cashflow(sbl_trade, 'Fixed Amount', amount, cashflow_paydate)

                LOGGER.info('%s uploaded for trade %s' % (str(amount), sbl_trade.Oid()))

                # Uploading row to email report sent to business
                row_info_list = [str(self.report_row_number), str(external_id), str(trade_oid),
                                 REPORT_STATUS['success_status'], str(amount), cashflow_paydate, '-']
                FUploaderFunctions.add_row(self.report_row_number, row_info_list)

                self.report_row_number += 1

            else:
                row_info_list = [str(self.report_row_number), str(external_id), str(trade_oid),
                                 REPORT_STATUS['failure_status'], '-',
                                 cashflow_paydate, REPORT_STATUS['status_error']]
                FUploaderFunctions.add_row(self.report_row_number, row_info_list)

                self.report_row_number += 1
                LOGGER.warning('Failed: Trade %d is in %s status'
                               % (trade_oid, sbl_trade.Status()))

        except Exception as exc:
            raise self.RecordProcessingException(
                                'ERROR while processing row %d of file %s: %s'
                                % (_index, os.path.basename(self._file_path), str(exc)))


class CSVCreator(SBLCashflowUploader, SimpleCSVFeedProcessor):

    def __init__(self, file_path):

        SBLCashflowUploader.__init__(self)
        SimpleCSVFeedProcessor.__init__(self, file_path, do_logging=False)


class XLSCreator(SBLCashflowUploader, SimpleXLSFeedProcessor):

    def __init__(self, file_path):

        SBLCashflowUploader.__init__(self)
        SimpleXLSFeedProcessor.__init__(self, file_path, sheet_index=0, sheet_name=None)


def ael_main(dictionary):

    file_path = str(dictionary['input_file'])

    LOGGER.info("Processing input file: %s", file_path)
    
    if file_path.endswith(".csv"):
        proc = CSVCreator(file_path)
    else:
        proc = XLSCreator(file_path)

    proc.add_error_notifier(notify_log)
    proc.process(False)
    
    email_addresses = dictionary['email_address']
    if email_addresses:
        run_date = acm.Time.DateNow()
        report_header = 'SBL call account cashflows'
        email_sender = 'xraeqdcollateralmana@absa.africa'
        email_subject = 'SBL call account cash flow uplaod report %s' % run_date
        table_headings = 'SubAccount', 'Trade', 'Status', 'Amount Uploaded', 'Pay Day', 'Failure Reason'
        FUploaderFunctions.add_header(table_headings)
        FUploaderFunctions.send_report(email_addresses, email_sender, email_subject, report_header)

    LOGGER.info('Completed successfully')
