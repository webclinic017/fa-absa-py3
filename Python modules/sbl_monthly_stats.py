"""--------------------------------------------------------------------------------------
MODULE
    sbl_collateral_file_uploader

DESCRIPTION
    Date                : 2019-07-18
    Purpose             : This script will be used to book bonds, ncds and equity
                          collateral trades from a file
    Department and Desk : PCG
    Requester           : Shaun Du Plessis
    Developer           : Sihle Gaxa
    CR Number           : CHG1001992765

HISTORY
=========================================================================================
Date            Change no       Developer               Description
-----------------------------------------------------------------------------------------
2019-07-18      CHG1001283051   Sihle Gaxa              Initial implementation.
2021-02-23      PCGDEV-672      Sihle Gaxa              Fixed run period dates

ENDDESCRIPTION
--------------------------------------------------------------------------------------"""
import acm
import csv
import datetime

import FRunScriptGUI
from at_logging import getLogger
from collections import defaultdict

import sbl_booking_utils as sbl_utils
import FUploaderFunctions as pcgUploader
import sbl_booking_validator as sbl_validator
from at_ael_variables import AelVariableHandler
from at_feed_processing import (SimpleCSVFeedProcessor,
                                SimpleXLSFeedProcessor,
                                notify_log)

LOGGER = getLogger(__name__)
FILE_HEADER = ["SBL Monthly Data", "Total"]
FILE_FILTER = "CSV Files (*.csv)|*.csv|XLS Files (*.xls)|*.xls|XLSX Files (*.xlsx)|*.xlsx|"
INPUT_FILE = FRunScriptGUI.InputFileSelection(FileFilter=FILE_FILTER)


def get_run_period():
    TODAY = acm.Time().DateToday()
    return {"PREV_DAY": acm.Time.DateAddDelta(acm.Time.DateToday(), 0, 0, -1),
            "FIRST_DAY_OF_MONTH": acm.Time.DateAddDelta(acm.Time.DateToday(), 0, -1, 0),
            }

ael_variables = AelVariableHandler()
ael_variables.add(
    "start_date",
    label=" Start Date",
    collection=list(get_run_period().keys()),
    default="FIRST_DAY_OF_MONTH",
    mandatory=True,
    multiple=False,
    alt="Start date for time period to run report for"
)
ael_variables.add(
    "end_date",
    label="End Date",
    collection=list(get_run_period().keys()),
    default="PREV_DAY",
    mandatory=True,
    multiple=False,
    alt="End date for time period to run report for"
)
ael_variables.add(
    'input_file',
    label='File',
    cls=INPUT_FILE,
    default=INPUT_FILE,
    mandatory=True,
    multiple=True,
    alt='Input file in CSV or XLS format.'
)


class SBLMonthlyData(object):
    acquirer = "SECURITY LENDINGS DESK"
    settlement_types = ("Security Nominal", "End Security")

    def __init__(self, start_date, end_date, file_directory):
        self.data = defaultdict(list)
        self.end_date = end_date
        self.start_date = start_date
        self.file_directory = file_directory

    def set_report_data(self):
        settlements = self.get_settlements()
        self.set_batch_trades(settlements)
        self.set_manual_trades(settlements)
        self.set_settled_loans(settlements)
        self.set_settled_returns(settlements)
        self.set_cancelled_loans(settlements)
        self.set_on_market_trades(settlements)
        self.set_cancelled_returns(settlements)
        self.set_off_market_trades(settlements)
        self.set_lender_settled_trades(settlements)
        self.set_borrower_settled_trades(settlements)
        self.set_failed_on_market_trades(settlements)
        self.set_failed_off_market_trades(settlements)
        self.set_settled_on_market_trades(settlements)
        self.set_settled_off_market_trades(settlements)
        self.set_internal_counterparty_trades(settlements)
        self.set_external_counterparty_trades(settlements)
        self.set_fee_statements_sent()
        self.set_confirmation_sent()

    def get_settlements(self):
        sbl_settlement_query = "acquirer = '{acq_name}' and valueDay <= '{end_date}' and"
        sbl_settlement_query += " valueDay >= '{start_date}' and type in {types}"
        sbl_settlements = [settlement for settlement in acm.FSettlement.Select(
            sbl_settlement_query.format(
                acq_name=self.acquirer,
                end_date=self.end_date,
                start_date=self.start_date,
                types=self.settlement_types))
                           if self.is_valid_settlement(settlement)]
        return sbl_settlements

    @staticmethod
    def is_valid_settlement(settlement):
        if (settlement.Trade() and
                settlement.Trade().add_info("SL_SWIFT") and
                settlement.Trade().add_info("SL_G1Counterparty1") and
                settlement.Trade().add_info("SL_G1Counterparty2") and
                settlement.Trade().Instrument().InsType() == "SecurityLoan" and
                settlement.Trade().Status() in ["BO Confirmed", "BO-BO Confirmed"]):
            return True
        return False

    def set_settled_loans(self, settlements):
        for settlement in settlements:
            trade = settlement.Trade()
            if (settlement.Status() == "Settled" and not trade.Text1() and
                    trade.Oid() not in self.data["Settled loans"]):
                self.data["Settled loans"].append(trade.Oid())

    def set_settled_returns(self, settlements):
        for settlement in settlements:
            trade = settlement.Trade()
            if (trade.Text1() and settlement.Status() == "Settled" and
                    trade.Oid() not in self.data["Settled returns"]):
                self.data["Settled returns"].append(trade.Oid())

    def set_cancelled_loans(self, settlements):
        for settlement in settlements:
            trade = settlement.Trade()
            if (settlement.Status() == "Recalled" and not trade.Text1() and
                    trade.Oid() not in self.data["Cancelled loans"]):
                self.data["Cancelled loans"].append(trade.Oid())

    def set_cancelled_returns(self, settlements):
        for settlement in settlements:
            trade = settlement.Trade()
            if (trade.Text1() and settlement.Status() == "Recalled" and
                    trade.Oid() not in self.data["Cancelled returns"]):
                self.data["Cancelled returns"].append(trade.Oid())

    def set_on_market_trades(self, settlements):
        for settlement in settlements:
            trade = settlement.Trade()
            if (trade.add_info("SL_SWIFT") == "SWIFT" and
                    trade.Oid() not in self.data["On-market trades"]):
                self.data["On-market trades"].append(trade.Oid())

    def set_settled_on_market_trades(self, settlements):
        for settlement in settlements:
            trade = settlement.Trade()
            if (trade.add_info("SL_SWIFT") == "SWIFT" and
                    settlement.Status() == "Settled" and
                    trade.Oid() not in self.data["Settled on-market trades"]):
                self.data["Settled on-market trades"].append(trade.Oid())

    def set_failed_on_market_trades(self, settlements):
        for settlement in settlements:
            trade = settlement.Trade()
            if (trade.add_info("SL_SWIFT") == "SWIFT" and
                    settlement.Status() != "Settled" and
                    trade.Oid() not in self.data["Settled on-market trades"]):
                self.data["Settled on-market trades"].append(trade.Oid())

    def set_off_market_trades(self, settlements):
        for settlement in settlements:
            trade = settlement.Trade()
            if (trade.add_info("SL_SWIFT") == "DOM" and
                    trade.Oid() not in self.data["Off market trades"]):
                self.data["Off market trades"].append(trade.Oid())

    def set_settled_off_market_trades(self, settlements):
        for settlement in settlements:
            trade = settlement.Trade()
            if (trade.add_info("SL_SWIFT") == "DOM" and
                    settlement.Status() == "Settled" and
                    trade.Oid() not in self.data["Settled off-market trades"]):
                self.data["Settled off-market trades"].append(trade.Oid())

    def set_failed_off_market_trades(self, settlements):
        for settlement in settlements:
            trade = settlement.Trade()
            if (trade.add_info("SL_SWIFT") == "DOM" and
                    settlement.Status() != "Settled" and
                    trade.Oid() not in self.data["Failed off-market trades"]):
                self.data["Failed off-market trades"].append(trade.Oid())

    def set_borrower_settled_trades(self, settlements):
        for settlement in settlements:
            trade = settlement.Trade()
            if (settlement.Status() == "Settled" and
                    trade.add_info("SL_G1Counterparty1").startswith("SLB") and
                    trade.Oid() not in self.data["Settled borrower trades"]):
                self.data["Settled borrower trades"].append(trade.Oid())

    def set_lender_settled_trades(self, settlements):
        for settlement in settlements:
            trade = settlement.Trade()
            if (settlement.Status() == "Settled" and
                    trade.add_info("SL_G1Counterparty2").startswith("SLL") and
                    trade.Oid() not in self.data["Settled lender trades"]):
                self.data["Settled lender trades"].append(trade.Oid())

    def set_external_counterparty_trades(self, settlements):
        for settlement in settlements:
            trade = settlement.Trade()
            counterparty = settlement.Counterparty()
            external_flag = counterparty.Free3ChoiceList()
            if (external_flag and external_flag.Name() == "External" and
                    settlement.Status() == "Settled" and
                    trade.Oid() not in self.data["Settled external trades"]):
                self.data["Settled external trades"].append(trade.Oid())

    def set_internal_counterparty_trades(self, settlements):
        for settlement in settlements:
            trade = settlement.Trade()
            counterparty = settlement.Counterparty()
            external_flag = counterparty.Free3ChoiceList()
            if (not external_flag and
                    settlement.Status() == "Settled" and
                    trade.Oid() not in self.data["Settled internal trades"]):
                self.data["Settled internal trades"].append(trade.Oid())

    def set_batch_trades(self, settlements):
        for settlement in settlements:
            trade = settlement.Trade()
            update_user = settlement.UpdateUser().Name()
            if (settlement.Status() == "Settled" and
                    update_user in ["ATS_SWIFT_IN_1", "ATS"] and
                    trade.Oid() not in self.data["Batch trades"]):
                self.data["Batch trades"].append(trade.Oid())

    def set_manual_trades(self, settlements):
        for settlement in settlements:
            trade = settlement.Trade()
            update_group = settlement.UpdateUser().UserGroup().Name()
            if (settlement.Status() == "Settled" and
                    update_group in ["OPS SecLend", "IT RTB"] and
                    trade.Oid() not in self.data["Manual trades"]):
                self.data["Manual trades"].append(trade.Oid())

    def set_fee_statements_sent(self):
        fee_statements = self.get_fee_statements()
        for fee_statement in fee_statements:
            party_name = fee_statement.Subject().Name()
            statement_steps = fee_statement.Steps()
            if statement_steps:
                for statement_step in statement_steps:
                    if (statement_step.StateName() == "Sent" and
                            party_name not in self.data["Sent fee statements"]):
                        self.data["Sent fee statements"].append(party_name)

    def get_fee_statements(self):
        fee_statements = [business_process for business_process in acm.FBusinessProcess.Select(
            "stateChart = {state}".format(state="Statements"))
                          if business_process.add_info("BP_Event") == "SBL Fee Statement" and
                          business_process.add_info("BP_ValuationDate") == self.end_date and
                          business_process.add_info("BP_InsType") == "SecurityLoan"]
        return fee_statements

    def set_confirmation_sent(self):
        confirmations = self.get_confirmations()
        for confirmation in confirmations:
            for confirmation_step in confirmation.Steps():
                if confirmation_step.StateName() == "Sent":
                    self.data["Sent confirmations"].append(confirmation.Subject().Name())

    def get_confirmations(self):
        confirmations = [business_process for business_process in acm.FBusinessProcess.Select(
            "stateChart = '{state}'".format(
                state="SecurityLoan Confirmation"))
                         if self.end_date >= business_process.CreateDay() >= self.start_date and
                         business_process.add_info("BP_Event") == "SecurityLoan Confirmation" and
                         business_process.add_info("BP_InsType") == "SecurityLoan"]
        return confirmations

    def write_data(self):
        try:
            file_data = {}
            LOGGER.info("Starting file writing process")
            LOGGER.info("=" * 80)
            with open(self.file_directory, "wb") as csv_file:
                writer = csv.DictWriter(csv_file, FILE_HEADER)
                writer.writeheader()
                self.set_report_data()
                for column_name, column_values in self.data.items():
                    file_data["SBL Monthly Data"] = column_name
                    file_data["Total"] = len(column_values)
                    writer.writerow(file_data)
                    file_data.clear()
                self.data.clear()
        except Exception as e:
            LOGGER.exception("Could not write file data because {error}".format(error=str(e)))
            raise Exception("Could not write file data because {error}".format(error=str(e)))


def ael_main(dictionary):
    try:
        file_directory = str(dictionary['input_file'])
        end_date = dictionary["end_date"]
        start_date = dictionary["start_date"]
        if end_date in list(get_run_period().keys()):
            end_date = get_run_period()[end_date]
        if start_date in list(get_run_period().keys()):
            start_date = get_run_period()[start_date]
        end_period = str(acm.Time.DateAddDelta(end_date, 0, 0, 0))
        start_period = str(acm.Time.DateAddDelta(start_date, 0, 0, 0))
        LOGGER.info("Retrieving SBL data from {start_date} to {end_date}".format(
            start_date=start_period, end_date=end_period))
        month_end_data = SBLMonthlyData(start_period, end_period, file_directory)
        month_end_data.write_data()
        LOGGER.info("Completed successfully")
        LOGGER.info("Wrote secondary output to: {path}".format(path=file_directory))
    except Exception as e:
        LOGGER.exception("Could not generate file because {error}".format(error=str(e)))
        raise Exception("Could not generate file because {error}".format(error=str(e)))
