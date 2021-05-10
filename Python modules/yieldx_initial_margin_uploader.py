"""----------------------------------------------------------------------------
MODULE
    yieldx_inital_margin_uploader

DESCRIPTION
    Date                : 2016-11-15
    Purpose             : Uploads daily YIELDX initial margin amounts from a
                          flat file from GCMS.
    Department and Desk : TODO
    Requester           : TODO
    Developer           : Paseka Motsoeneng, Sihle Gaxa
    CR Number           : TODO

HISTORY
===============================================================================
Date       Change no    Developer          Description
-------------------------------------------------------------------------------
2019-01-14      CHG1001283051   Qaqamba Ntshobane       Script redesign
2019-10-21      PCGDEV-84       Qaqamba Ntshobane       Amended script for a 
                                                        more dynamic 
                                                        FUploaderFunctions

ENDDESCRIPTION
----------------------------------------------------------------------------"""

import xlrd
import acm

from at_logging import getLogger

import FUploaderFunctions

LOGGER = getLogger(__name__)

ael_variables = FUploaderFunctions.get_ael_variables()
ael_variables.add('yieldx_trades',
                  label='Trades',
                  cls="FTrade",
                  default="?YieldX_IniMargin_Instruments",
                  multiple=True,
                  alt='Query folder containing trades to which initial margin will be uploaded.'
                  )


def ael_main(dictionary):

    trades = dictionary['yieldx_trades']
    email_addresses = dictionary['email_address']
    run_date = FUploaderFunctions.get_input_date(dictionary, adjust_banking_day=True)

    class_name = YIELDXInitialMarginUploader

    report_header = 'YieldX Initial Margin'
    table_headings = 'SubAccount', 'Trade', 'Status', 'Margin Uploaded', 'Failure Reason'

    email_sender = 'PCITACNotifications@absa.africa'
    email_subject = 'YieldX Initial Margins Report %s' % run_date

    FUploaderFunctions.add_header(table_headings)
    FUploaderFunctions.process_xls_file(dictionary, class_name, trades)
    FUploaderFunctions.send_report(email_addresses, email_sender, email_subject, report_header)

    LOGGER.info('Completed Successfully')


class YIELDXInitialMarginUploader():

    data_row = 17

    def __init__(self, file_path, run_date, sheet, trades, report_row_number):

        self.file_path = file_path
        self.run_date = run_date
        self.sheet = sheet
        self.trades = trades
        self.margin = 0.00
        self.trade = None
        self.report_row_number = report_row_number

        for d in range(self.data_row, sheet.nrows):
            self._process_record()
            self.data_row = d

            if self.sheet.cell(self.data_row, 0).value == xlrd.empty_cell.value or\
               self.sheet.cell(self.data_row, 0).value == 'Total':
                break

    def _process_record(self):

        subaccount_index = 0
        initial_margin_index = 7

        try:
            subaccount_code = self.sheet.cell(self.data_row, subaccount_index).value
        except Exception:
            return

        yieldx_instrument = acm.FInstrument.Select01("externalId1 = %s" % str(subaccount_code), None)
        yieldx_instrument_ids = [trade.Instrument().ExternalId1() for trade in self.trades]

        if subaccount_code not in yieldx_instrument_ids:
            return

        if not yieldx_instrument:
            row_info_list = [str(self.report_row_number), str(subaccount_code), "-",
                             FUploaderFunctions.report_status["failure_status"], '-',
                             FUploaderFunctions.report_status["externalId_error"]]
            FUploaderFunctions.add_row(self.report_row_number, row_info_list)

            self.report_row_number += 1
            LOGGER.warning("Yieldx trade with External Id %s not found"
                           % subaccount_code)
            return
        else:
            trades = yieldx_instrument.Trades()

            if trades:
                trade_object = trades[0]
                trade_oid = trade_object.Oid()

                margin = -1 * float(self.sheet.cell(self.data_row, initial_margin_index).value)

                if not self.margin == margin and\
                   not self.trade == trade_oid:
                    self.margin = margin
                    self.trade = trade_oid
                else:
                    return
            else:
                row_info_list = [str(self.report_row_number), str(subaccount_code), 'No trade',
                                 FUploaderFunctions.report_status['failure_status'], '-',
                                 FUploaderFunctions.report_status['missing_trade_error']]
                FUploaderFunctions.add_row(self.report_row_number, row_info_list)

                self.report_row_number += 1
                LOGGER.warning('Trade with External Id %s not found in FA' % subaccount_code)
                return

        if trade_object.Status() not in ('Void', 'Simulated', 'Terminated'):

            is_duplicate = FUploaderFunctions.is_duplicate_cashflow(trade_object, margin, self.run_date)

            if is_duplicate:
                row_info_list = [str(self.report_row_number), str(subaccount_code), str(trade_oid),
                                 FUploaderFunctions.report_status['failure_status'], str(margin),
                                 FUploaderFunctions.report_status['duplicate_moneyflow']]
                FUploaderFunctions.add_row(self.report_row_number, row_info_list)

                self.report_row_number += 1
                LOGGER.info('Skipping existing cashflow amount %d for %i' % (margin, trade_oid))
                return

            if margin:
                result = False

                # Upload margin if value is not 0.0
                result = yieldx_instrument.AdjustDeposit(margin, self.run_date, trade_object.Quantity())

                if result:
                    row_info_list = [str(self.report_row_number), str(subaccount_code), str(trade_oid), 'Success', str(margin), '-']
                    FUploaderFunctions.add_row(self.report_row_number, row_info_list)

                    self.report_row_number += 1
                    LOGGER.info('Margin %d uploaded to trade %s' % (margin, trade_oid))
            else:
                row_info_list = [str(self.report_row_number), str(subaccount_code), str(trade_oid),
                                 FUploaderFunctions.report_status['failure_status'], '-',
                                 FUploaderFunctions.report_status['margin_error']]
                FUploaderFunctions.add_row(self.report_row_number, row_info_list)

                self.report_row_number += 1
                LOGGER.info('Margin %d has not been uploaded for trade %s' % (margin, trade_oid))
        else:
            row_info_list = [str(self.report_row_number), str(subaccount_code), str(trade_oid),
                             FUploaderFunctions.report_status['failure_status'], '-',
                             FUploaderFunctions.report_status['status_error']]
            FUploaderFunctions.add_row(self.report_row_number, row_info_list)

            self.report_row_number += 1
            LOGGER.warning('Failed: Trade %d is in %s status'
                           % (trade_oid, trade_object.Status()))
