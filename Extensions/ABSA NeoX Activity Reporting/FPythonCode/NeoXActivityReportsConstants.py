"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    NeoXActivityReportsConstants

DESCRIPTION
    This module is used to define constants used for event-driven Activity Reports to Neox
    (straight-through-processing).

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2020-10-21      FAOPS-959       Ncediso Nkambule        Cuen Edwards            Initial implementation.
2021-03-16      FAOPS-982       Ncediso Nkambule        Gasant Thulsie          Added functions to handle Cashflow driven events.

-----------------------------------------------------------------------------------------------------------------------------------------
"""

from collections import OrderedDict


COLLATERAL_ACTIVITY_COLUMN_IDS = OrderedDict()
# COLLATERAL_ACTIVITY_COLUMN_IDS["Column ID"] = "Column Label Name"
COLLATERAL_ACTIVITY_COLUMN_IDS["Trade Number"] = "Trade Reference"
COLLATERAL_ACTIVITY_COLUMN_IDS["Report Date"] = "Report Date"
COLLATERAL_ACTIVITY_COLUMN_IDS["Trade Status"] = "Status"
COLLATERAL_ACTIVITY_COLUMN_IDS["Text1"] = "Trade Type"
COLLATERAL_ACTIVITY_COLUMN_IDS["Instrument Type"] = "Collateral Type"
COLLATERAL_ACTIVITY_COLUMN_IDS["TradArea"] = "Trade Key"
COLLATERAL_ACTIVITY_COLUMN_IDS["Reporting Quantity"] = "Quantity"
COLLATERAL_ACTIVITY_COLUMN_IDS["Trade Price"] = "Price"
COLLATERAL_ACTIVITY_COLUMN_IDS["Trade Instrument"] = "Instrument"
COLLATERAL_ACTIVITY_COLUMN_IDS["SOB Market Value"] = "Market Value"
COLLATERAL_ACTIVITY_COLUMN_IDS["Trade Date"] = "Trade Time"
COLLATERAL_ACTIVITY_COLUMN_IDS["Trade Value Day"] = "Settlement Day"
COLLATERAL_ACTIVITY_COLUMN_IDS["Trade Contract"] = "Contract Reference"
COLLATERAL_ACTIVITY_COLUMN_IDS["True Counterparty Code"] = "Cpty Code"
COLLATERAL_ACTIVITY_COLUMN_IDS["Counterparty Major Code"] = "Cpty Major"
COLLATERAL_ACTIVITY_COLUMN_IDS["Trade Counterparty"] = "Counterparty"
COLLATERAL_ACTIVITY_COLUMN_IDS["Counterparty Major"] = "Counterparty Major"
COLLATERAL_ACTIVITY_COLUMN_IDS["True Counterparty Type"] = "Lender/Borrower"
COLLATERAL_ACTIVITY_COLUMN_IDS["Taxable Status"] = "Taxable Status"
COLLATERAL_ACTIVITY_COLUMN_IDS["ISIN"] = "Isin"
COLLATERAL_ACTIVITY_COLUMN_IDS["AdditionalInfo.SL_SWIFT"] = "Settlement Mode"
COLLATERAL_ACTIVITY_COLUMN_IDS["Trade Currency"] = "Currency"
COLLATERAL_ACTIVITY_COLUMN_IDS["Bought or Sold"] = "Deposit/Withdrawal"
COLLATERAL_ACTIVITY_COLUMN_IDS["True SDSID"] = "SDS ID"
COLLATERAL_ACTIVITY_COLUMN_IDS["Trade Update Time"] = "Trade Update Time"


LOAN_ACTIVITY_COLUMN_IDS = OrderedDict()
# LOAN_ACTIVITY_COLUMN_IDS["Column ID"] = "Column Label Name"
LOAN_ACTIVITY_COLUMN_IDS["Trade Number"] = "Trade Reference"
LOAN_ACTIVITY_COLUMN_IDS["Report Date"] = "Report Date"
LOAN_ACTIVITY_COLUMN_IDS["Trade Status"] = "Status"
LOAN_ACTIVITY_COLUMN_IDS["Open End"] = "Open End Status"
LOAN_ACTIVITY_COLUMN_IDS["Text1"] = "Trade Type"
LOAN_ACTIVITY_COLUMN_IDS["Reporting Quantity"] = "Quantity"
LOAN_ACTIVITY_COLUMN_IDS["AdditionalInfo.SL_ReturnedQty"] = "Return Quantity"
LOAN_ACTIVITY_COLUMN_IDS["Reference Price"] = "Loan Price"
LOAN_ACTIVITY_COLUMN_IDS["Instrument.Underlying.SLPrice"] = "Market Price"
LOAN_ACTIVITY_COLUMN_IDS["SOB Market Value"] = "Market Value"
LOAN_ACTIVITY_COLUMN_IDS["SL Rate"] = "Fee"
LOAN_ACTIVITY_COLUMN_IDS["Underlying Instrument"] = "Security"
LOAN_ACTIVITY_COLUMN_IDS["Trade Date"] = "Trade Time"
LOAN_ACTIVITY_COLUMN_IDS["Security Settlement Date"] = "Settlement Date"
LOAN_ACTIVITY_COLUMN_IDS["Contract.Oid"] = "Original Loan Trade"
LOAN_ACTIVITY_COLUMN_IDS["Contract.FaceValue"] = "Original Loan Quantity"
LOAN_ACTIVITY_COLUMN_IDS["Original Loan Value"] = "Original Loan Value"
LOAN_ACTIVITY_COLUMN_IDS["True Counterparty Code"] = "Cpty Code"
LOAN_ACTIVITY_COLUMN_IDS["Counterparty Major Code"] = "Cpty Major"
LOAN_ACTIVITY_COLUMN_IDS["Counterparty Major"] = "Counterparty Major"
LOAN_ACTIVITY_COLUMN_IDS["True Counterparty Type"] = "Lender/Borrower"
LOAN_ACTIVITY_COLUMN_IDS["Trade Currency"] = "Currency"
LOAN_ACTIVITY_COLUMN_IDS["AdditionalInfo.SL_G1Counterparty1"] = "Borrower"
LOAN_ACTIVITY_COLUMN_IDS["AdditionalInfo.SL_G1Counterparty2"] = "Lender"
LOAN_ACTIVITY_COLUMN_IDS["Taxable Status"] = "Taxable Status"
LOAN_ACTIVITY_COLUMN_IDS["True SDSID"] = "SDS ID"
LOAN_ACTIVITY_COLUMN_IDS["AdditionalInfo.SL_SWIFT"] = "Settlement Mode"
LOAN_ACTIVITY_COLUMN_IDS["AdditionalInfo.SL_CFD"] = "MTM"
LOAN_ACTIVITY_COLUMN_IDS["Underlying ISIN"] = "ISIN"
LOAN_ACTIVITY_COLUMN_IDS["Trade Update Time"] = "Trade Update Time"


CASH_COLLATERAL_ACTIVITY_COLUMN_IDS = OrderedDict()
# CASH_COLLATERAL_ACTIVITY_COLUMN_IDS["Column ID"] = "Column Label Name"
CASH_COLLATERAL_ACTIVITY_COLUMN_IDS["Trade Number"] = "Trade Reference"
CASH_COLLATERAL_ACTIVITY_COLUMN_IDS["Report Date"] = "Report Date"
CASH_COLLATERAL_ACTIVITY_COLUMN_IDS["Trade Status"] = "Status"
CASH_COLLATERAL_ACTIVITY_COLUMN_IDS["Instrument Type"] = "Trade Type"
CASH_COLLATERAL_ACTIVITY_COLUMN_IDS["IsCall"] = "Collateral Type"
CASH_COLLATERAL_ACTIVITY_COLUMN_IDS["TradArea"] = "Trade Key"
CASH_COLLATERAL_ACTIVITY_COLUMN_IDS["Reporting Quantity"] = "Quantity"
CASH_COLLATERAL_ACTIVITY_COLUMN_IDS["Trade Price"] = "Price"
CASH_COLLATERAL_ACTIVITY_COLUMN_IDS["Trade Instrument"] = "Instrument"
CASH_COLLATERAL_ACTIVITY_COLUMN_IDS["SOB Market Value"] = "Market Value"
CASH_COLLATERAL_ACTIVITY_COLUMN_IDS["Trade Date"] = "Trade Time"
CASH_COLLATERAL_ACTIVITY_COLUMN_IDS["Trade Value Day"] = "Settlement Day"
CASH_COLLATERAL_ACTIVITY_COLUMN_IDS["Trade Contract"] = "Contract Reference"
CASH_COLLATERAL_ACTIVITY_COLUMN_IDS["True Counterparty Code"] = "Cpty Code"
CASH_COLLATERAL_ACTIVITY_COLUMN_IDS["Counterparty Major Code"] = "Cpty Major"
CASH_COLLATERAL_ACTIVITY_COLUMN_IDS["Trade Counterparty"] = "Counterparty"
CASH_COLLATERAL_ACTIVITY_COLUMN_IDS["Counterparty Major"] = "Counterparty Major"
CASH_COLLATERAL_ACTIVITY_COLUMN_IDS["True Counterparty Type"] = "Lender/Borrower"
CASH_COLLATERAL_ACTIVITY_COLUMN_IDS["Taxable Status"] = "Taxable Status"
CASH_COLLATERAL_ACTIVITY_COLUMN_IDS["ISIN"] = "Isin"
CASH_COLLATERAL_ACTIVITY_COLUMN_IDS["AdditionalInfo.SL_SWIFT"] = "Settlement Mode"
CASH_COLLATERAL_ACTIVITY_COLUMN_IDS["Trade Currency"] = "Currency"
CASH_COLLATERAL_ACTIVITY_COLUMN_IDS["Bought or Sold"] = "Deposit/Withdrawal"
CASH_COLLATERAL_ACTIVITY_COLUMN_IDS["True SDSID"] = "SDS ID"
CASH_COLLATERAL_ACTIVITY_COLUMN_IDS["Trade Update Time"] = "Trade Update Time"


CASHFLOW_COLUMN_IDS = dict()
CASHFLOW_COLUMN_IDS["Cash Analysis Projected"] = "Market Value"
CASHFLOW_COLUMN_IDS["Cash Analysis Nominal"] = "Quantity"
CASHFLOW_COLUMN_IDS["Cash Analysis Pay Day"] = "Settlement Day"

DEPOSIT_COLUMN_IDS = dict()
DEPOSIT_COLUMN_IDS["Instrument Type"] = "Collateral Type"

SBL_LOAN_ADD_INFOS = ['SL_G1Counterparty1', 'SL_G1Counterparty2']
LOAN_INS_TYPE = 'SecurityLoan'
OPEN_END_STATUS = ["Open End", "Terminated"]
SETTLE_CATEGORY = "SL_STRATE", "SL_CUSTODIAN"
COLLATERAL_TRADE_STATUSES = ["BO Confirmed", "BO-BO Confirmed", "Void"]
LOANS_TRADE_STATUSES = ["BO Confirmed", "Void"]
DATE_TYPES = ["15 Minutes Intervals", "Today", "Custom Date"]
VALID_TRADE_STATUS = ["BO Confirmed", "BO-BO Confirmed"]
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
DATE_FORMAT = "%Y-%m-%d"
FILE_DATE_FORMAT = "%y%m%d%H%M%S"
