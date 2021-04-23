"""---------------------------------------------------------------------------------------------------------------------
MODULE
    NeoXActivityReportsHookBase

DESCRIPTION
    This module contains STP logic to terminate manually settled full returns.

------------------------------------------------------------------------------------------------------------------------
HISTORY
========================================================================================================================
Date            Change no        Developer            Requester               Description
------------------------------------------------------------------------------------------------------------------------
2020-10-21      FAOPS-959        Ncediso Nkambule     Cuen Edwards            Initial implementation.
2021-02-02      FAOPS-1044       Ncediso Nkambule     Gasant Thulsie          Fixed Column Header issue
2021-03-16      FAOPS-982        Ncediso Nkambule     Gasant Thulsie          Added functions to handle Cashflow driven events.

------------------------------------------------------------------------------------------------------------------------
"""

import acm
from logging import getLogger
import sbl_booking_utils as sbl_utils
import NeoXActivityReportsConstants as Constants
from NeoXActivityReportsBase import CalculationBase, FileBase
import NeoXActivityReportsUtils as NeoXUtils


LOGGER = getLogger(__name__)


class CollateralReport(CalculationBase, FileBase):

    def __init__(self, directory, file_name, start_date_str=None, end_date_str=None, statuses=None):
        """

        :param directory:
        :param file_name:
        :param start_date_str:
        :type start_date_str: str
        :param end_date_str:
        :type end_date_str: str
        :param statuses:
        """
        super(CollateralReport, self).__init__(directory, file_name)

        self.execution_date = start_date_str
        self.end_date = end_date_str
        if statuses is None:
            statuses = Constants.COLLATERAL_TRADE_STATUSES
        self.trade_statuses = statuses
        self.party_name_prefix = "SL"

    def is_valid_collateral_trade(self, acm_trade):
        return NeoXUtils.is_valid_sbl_collateral_trade(acm_trade, self.party_name_prefix)

    def select_collateral_trades(self):
        select_string = "executionTime >= '{execution_time}'".format(execution_time=self.execution_date)
        select_string += " and updateTime >= '{update_time}'".format(update_time=self.execution_date)
        select_string += " and executionTime < '{end_date}'".format(end_date=self.end_date)
        select_string += " and updateTime < '{end_date}'".format(end_date=self.end_date)
        select_string += " and status in {status}".format(status=tuple(self.trade_statuses))
        select_string += " and tradeCategory = '{category}'".format(category=sbl_utils.COLLATERAL_CATEGORY)
        select_string += " and acquirer = '{acquirer}'".format(acquirer=sbl_utils.ACQUIRER.Name())
        trade_selection = acm.FTrade.Select(select_string)
        valid_trades = list()
        for acm_trade in trade_selection:
            if self.is_valid_collateral_trade(acm_trade):
                valid_trades.append(acm_trade)
        return valid_trades

    def generate_report(self, file_name=None):
        self._get_latest_file_path()
        collateral_calculated_data = list()
        col_trades = self.select_collateral_trades()
        LOGGER.info("Got {} Collateral Trades.".format(str(len(col_trades))))
        for trade in col_trades:
            collateral_calculated_data.append(self.get_calculated_values(trade, Constants.COLLATERAL_ACTIVITY_COLUMN_IDS))
        final_data = self.compare_data(collateral_calculated_data)
        self.dict_list_to_csv(final_data, file_name=file_name, headers=list(Constants.COLLATERAL_ACTIVITY_COLUMN_IDS.values()))


class SecurityLoanReport(CalculationBase, FileBase):

    def __init__(self, directory, file_name, start_date_str=None, end_date_str=None, statuses=None):
        super(SecurityLoanReport, self).__init__(directory, file_name,)
        self.execution_date = start_date_str
        self.end_date = end_date_str
        if statuses is None:
            statuses = Constants.LOANS_TRADE_STATUSES
        self.trade_statuses = statuses

    @staticmethod
    def is_valid_loan_trade(acm_trade):
        return NeoXUtils.is_valid_sbl_loan_trade(acm_trade)

    def select_loan_trades(self):
        select_string = "executionTime >= '{execution_time}'".format(execution_time=self.execution_date)
        select_string += " and executionTime < '{end_date}'".format(end_date=self.end_date)
        select_string += " and updateTime >= '{update_time}'".format(update_time=self.execution_date)
        select_string += " and updateTime < '{end_date}'".format(end_date=self.end_date)
        select_string += " and status in {status}".format(status=tuple(self.trade_statuses))
        select_string += " and acquirer = '{acquirer}'".format(acquirer=sbl_utils.ACQUIRER.Name())
        select_string += " and settleCategoryChlItem in {set_cat}".format(set_cat=tuple(sbl_utils.SETTLE_CATEGORY.values()))
        trade_selection = acm.FTrade.Select(select_string)
        valid_trades = list()
        for acm_trade in trade_selection:
            if self.is_valid_loan_trade(acm_trade):
                valid_trades.append(acm_trade)
        return valid_trades

    def generate_report(self, file_name=None):
        self._get_latest_file_path()
        loans_calculated_data = list()
        col_trades = self.select_loan_trades()
        LOGGER.info("Got {} Loan trades.".format(str(len(col_trades))))
        for trade in col_trades:
            loans_calculated_data.append(self.get_calculated_values(trade, Constants.LOAN_ACTIVITY_COLUMN_IDS))
        final_data = self.compare_data(loans_calculated_data)
        self.dict_list_to_csv(final_data, file_name=file_name, headers=list(Constants.LOAN_ACTIVITY_COLUMN_IDS.values()))


class CollateralTradeToReport(FileBase, CalculationBase):

    def __init__(self, directory, file_name, acm_trade, is_instrument_update=False):
        super(CollateralTradeToReport, self).__init__(directory, file_name, is_instrument_update)
        self.acm_trade = acm_trade

    def is_valid_collateral_trade(self):
        return NeoXUtils.is_valid_sbl_collateral_trade(self.acm_trade)

    def process_trade(self, message_id):
        LOGGER.info("Processing Collateral Trade To Report")
        if self.is_valid_collateral_trade():
            data = self.get_calculated_values(self.acm_trade, Constants.COLLATERAL_ACTIVITY_COLUMN_IDS)
            column_headers = list(Constants.COLLATERAL_ACTIVITY_COLUMN_IDS.values())
            if message_id:
                column_headers = [self.transaction_id_name] + list(Constants.COLLATERAL_ACTIVITY_COLUMN_IDS.values())
                data[self.transaction_id_name] = message_id
            LOGGER.info("Writing Collateral Trade {} to Temp {} Report".format(self.acm_trade.Oid(), self.file_name))
            self.append_dict_to_temp_file(data, column_headers)
        else:
            LOGGER.info("Skipping Is not Valid Collateral Trade")


class SecurityLoanTradeToReport(FileBase, CalculationBase):

    def __init__(self, directory, file_name, acm_trade, is_instrument_update=False):
        super(SecurityLoanTradeToReport, self).__init__(directory, file_name, is_instrument_update)
        self.acm_trade = acm_trade

    def is_valid_loan_trade(self):
        return NeoXUtils.is_valid_sbl_loan_trade(self.acm_trade)

    def process_trade(self, message_id=None):
        LOGGER.info("Processing Security Loan Trade To Report")
        if self.is_valid_loan_trade():
            data = self.get_calculated_values(self.acm_trade, Constants.LOAN_ACTIVITY_COLUMN_IDS)
            LOGGER.info("Writing Security Loan Trade {} to Temp {} Report".format(self.acm_trade.Oid(), self.file_name))
            column_headers = list(Constants.LOAN_ACTIVITY_COLUMN_IDS.values())
            if message_id:
                column_headers = [self.transaction_id_name] + list(Constants.LOAN_ACTIVITY_COLUMN_IDS.values())
                data[self.transaction_id_name] = message_id
            self.append_dict_to_temp_file(data, column_headers)
        else:
            LOGGER.info("Skipping Is not Valid Security Loan Trade")


class CashCollateralCashFlowToReport(FileBase, CalculationBase):

    def __init__(self, directory, file_name, acm_cash_flow, is_deleted_cashflow=False):
        super(CashCollateralCashFlowToReport, self).__init__(directory, file_name)
        self.acm_cash_flow = acm_cash_flow
        self.acm_trade = None
        self.is_deleted_cashflow = is_deleted_cashflow

        self._get_related_trade()

    def _get_related_trade(self):
        self.acm_trade = NeoXUtils.get_trade_related_to_cashflow(self.acm_cash_flow)

    def is_valid_cash_collateral_cash_flow(self):
        if self.acm_trade and NeoXUtils.is_valid_cash_collateral_trade(self.acm_trade) is False:
            return False
        return True

    def process_cash_flow(self, message_id=None, is_delete=False):
        LOGGER.info("Processing Cash Collateral Trade and Cash Flow To Report")
        if self.is_valid_cash_collateral_cash_flow():
            data = self.get_calculated_values(self.acm_trade, Constants.CASH_COLLATERAL_ACTIVITY_COLUMN_IDS)
            cf_data = self.get_deposit_cashflow_specific_data(self.acm_cash_flow, is_delete=is_delete)
            data.update(cf_data)
            LOGGER.info("Writing Security Loan Trade {} to Temp {} Report".format(self.acm_trade.Oid(), self.file_name))
            column_headers = list(Constants.CASH_COLLATERAL_ACTIVITY_COLUMN_IDS.values())
            if message_id:
                column_headers = [self.transaction_id_name] + list(Constants.CASH_COLLATERAL_ACTIVITY_COLUMN_IDS.values())
                data[self.transaction_id_name] = message_id
            self.append_dict_to_temp_file(data, column_headers)
        else:
            LOGGER.info("Skipping Is not Valid Cash Collateral Trade")
