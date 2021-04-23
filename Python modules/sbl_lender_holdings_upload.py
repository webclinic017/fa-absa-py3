"""-----------------------------------------------------------------------------------------
MODULE
    sbl_lender_holdings_upload

DESCRIPTION
    Date                : 2019-12-23
    Purpose             : This will upload SASOL's holdings from a Standard Bank Statement of
                          Holdings report and create dummy SecLoans in off-tree porfolio
                          Lender_Availability.
    Department and Desk : Front Office/PTS Change
    Requester           : Natasha Williams/James Stevens
    Developer           : Qaqamba Ntshobane

HISTORY
=============================================================================================
Date            Change no       Developer               Description
---------------------------------------------------------------------------------------------
2019-12-23      PCGDEV-226      Qaqamba Ntshobane       Initial Implementation

ENDDESCRIPTION
------------------------------------------------------------------------------------------"""

import acm
import FRunScriptGUI

import sys
import xlrd

from at_logging import getLogger
from at_ael_variables import AelVariableHandler

EXTENSION_DICT = None
EXTENSION_CLASS = "FObject:%s"
CONTEXT = acm.GetDefaultContext()
MODULE = CONTEXT.GetModule("ABSA Documentation")
EXTENSION = MODULE.GetExtension('FParameters', 'FObject', 'SASOLStatementOfHoldings')

EXISTING_TRADES = acm.FPhysicalPortfolio['Lender_Availability'].Trades()
EXISTING_TRADES = {trade.Instrument().Underlying().Isin(): trade for trade in EXISTING_TRADES if trade}
TRADE_DATE = acm.Time.DateToday()
LOGGER = getLogger(__name__)

fileFilter = "XLS Files (*.xls)|*.xls|XLSX Files (*.xlsx)|*.xlsx|"
inputFile = FRunScriptGUI.InputFileSelection(FileFilter=fileFilter)
sys.setdefaultencoding('utf8')

ael_variables = AelVariableHandler()
ael_variables.add(
    'input_file',
    label='File',
    cls=inputFile,
    default=inputFile,
    mandatory=True,
    multiple=True,
    alt='Input file in XLS format.'
    )


class HoldingsContainer():

    def __init__(self):
        self.record_mapping = {}

    def add_record_mapping(self, row_number, row_data):

        if type(row_data) == str:
            row_data = str(row_data)

        self.record_mapping.update({row_number: row_data})

    def get_record_mapping(self):
        return self.record_mapping


def is_isin(string):
    return len(string) == 12


def generate_trades(holdings_container):

    for row_number, row_data in holdings_container.get_record_mapping().items():

        isin = row_data["isin"]
        existing_trade = None

        if (isin in EXISTING_TRADES.keys()) and (TRADE_DATE == str(EXISTING_TRADES[isin].TradeTime()).split(" ")[0]):
            existing_trade = EXISTING_TRADES.pop(isin)

        try:
            acm.BeginTransaction()
            if existing_trade:
                _update_ins(existing_trade.Instrument(), row_data["trade_quantity"], row_data["security_price"])
                _update_trade(existing_trade, row_data["trade_quantity"], row_data["security_price"])
            else:
                underlying = acm.FInstrument.Select("isin='%s'" % isin)

                if underlying:
                    selo_ins = _create_ins(underlying, row_data)

                    if isinstance(selo_ins, str):
                        LOGGER.info("Updated %s with underlying: %s" % (selo_ins, isin))
                        acm.CommitTransaction()
                        continue
                    elif selo_ins:
                        _create_trade(selo_ins, row_data)
                    else:
                        LOGGER.warning("Failed to create loan with underlying %s" % underlying)
                        acm.AbortTransaction()
                        continue
                else:
                    LOGGER.warning("Failed to find instrument with ISIN matching %s, writing to FParameter  SASOLStatementOfHoldings" % isin)
                    _save_security_details(row_data)
                    acm.AbortTransaction()
                    continue
            acm.CommitTransaction()
        except Exception as ex:
            LOGGER.error(ex)
            acm.AbortTransaction()

    if EXISTING_TRADES:
        for trade in EXISTING_TRADES.values():
            _update_ins(trade.Instrument())
            _update_trade(trade)


def _save_security_details(values_dict):

    global EXTENSION_DICT

    if EXTENSION:
        EXTENSION.RegisterInStorage()
        extension_dict = EXTENSION.Value()

        avail_quantity = values_dict["trade_quantity"] / 2
        avail_value = values_dict["security_price"] * avail_quantity
        extension_dict.AtPut(str(values_dict["isin"]), [str(values_dict["security_desc"]), avail_quantity, avail_value, values_dict["trade_currency"]])

        EXTENSION_DICT = extension_dict


def save_parameter(extension_dict):

    MODULE.RegisterInStorage()

    try:
        if extension_dict:
            CONTEXT.EditImport("FParameters", EXTENSION_CLASS % extension_dict, True, MODULE)
            MODULE.Apply(MODULE)
            MODULE.Commit()
    except Exception as exc:
        LOGGER.error(exc)


def clear_parameter():

    if EXTENSION:
        EXTENSION.RegisterInStorage()
        extension_dict = EXTENSION.Value()
        extension_dict.Clear()


def _create_leg(selo_ins):

    leg = selo_ins.CreateLeg(True)
    leg.RegisterInStorage()
    leg.StartDate(selo_ins.StartDate())
    leg.EndDate(TRADE_DATE)
    leg.LegType('Fixed')
    leg.DayCountMethod('Act/365')
    leg.PayCalendar('ZAR Johannesburg')
    leg.Commit()


def _update_leg(selo_ins):

    leg = selo_ins.Legs().At(0)
    leg.RegisterInStorage()

    if selo_ins.EndDate() != TRADE_DATE:
        leg.EndDate(TRADE_DATE)


def _create_ins(underlying, row_data):

    if underlying:
        selo_ins = acm.FSecurityLoan()
        selo_ins_name = "%s/SELO/%s/%s" % (underlying[0].Name()[:3], underlying[0].Name()[4:], "Avail_Holdings_Trade")

        if acm.FInstrument[selo_ins_name]:
            selo_ins = acm.FInstrument[selo_ins_name]
            _update_ins(selo_ins, row_data["trade_quantity"], row_data["security_price"])
            return selo_ins_name

        selo_ins.RegisterInStorage()
        selo_ins.FreeText(row_data["security_desc"])
        selo_ins.Underlying(underlying[0])
        selo_ins.Name(selo_ins_name)
        selo_ins.OpenEnd("Open End")
        selo_ins.RefPrice(row_data["security_price"])
        selo_ins.RefValue(row_data["trade_quantity"])
        selo_ins.StartDate(TRADE_DATE)

        if not selo_ins.Legs():
            _create_leg(selo_ins)
        else:
            _update_leg(selo_ins)
        selo_ins.ExpiryDate(TRADE_DATE)
        selo_ins.Commit()
        return selo_ins


def _create_trade(selo_ins, row_data):

    if selo_ins.Trades():
        selo_trade = selo_ins.Trades().At(0)
        _update_trade(selo_trade, row_data["trade_quantity"], row_data["security_price"])
        return

    selo_trade = acm.FTrade()
    selo_trade.RegisterInStorage()
    selo_trade.Instrument(selo_ins)
    selo_trade.Currency(row_data["trade_currency"])
    selo_trade.Quantity(row_data["trade_quantity"]/selo_ins.RefValue())
    selo_trade.Price(row_data["security_price"])
    selo_trade.Counterparty('SLL SASOL PENSION FUND')
    selo_trade.Acquirer('SECURITY LENDINGS DESK')
    selo_trade.Portfolio('Lender_Availability')
    selo_trade.Trader("ATS_SBL_COLL")
    selo_trade.TradeTime(TRADE_DATE)
    selo_trade.ValueDay(TRADE_DATE)
    selo_trade.AcquireDay(TRADE_DATE)
    selo_trade.Status("Simulated")
    selo_trade.Commit()


def _update_ins(selo_ins, quantity=0.0, price=0.0):

    if quantity == 0.0:
        selo_ins.OpenEnd("Terminated")
    elif not selo_ins.OpenEnd() == "Open End":
        selo_ins.OpenEnd("Open End")

    selo_ins.RegisterInStorage()
    _update_leg(selo_ins)
    selo_ins.ExpiryDate(TRADE_DATE)
    selo_ins.RefPrice(price)
    selo_ins.RefValue(quantity)
    selo_ins.Commit()


def _update_trade(selo_trade, quantity=0.0, price=0.0):

    ref_value = selo_trade.Instrument().RefValue()
    if ref_value == 0.0:
        ref_value = 1

    selo_trade.Quantity(quantity/ref_value)
    selo_trade.Price(price)
    selo_trade.TradeTime(TRADE_DATE)
    selo_trade.ValueDay(TRADE_DATE)
    selo_trade.Commit()


def read_holdings(file_path):

    global TRADE_DATE
    holdings_container = HoldingsContainer()

    with xlrd.open_workbook(file_path) as wb:

        LOGGER.info("Reading Statement of Holdings: %s" % file_path.split("\\")[-1])

        sheet = wb.sheet_by_index(0)
        rows = sheet.nrows

        if sheet.cell(0, 1).value and sheet.cell(0, 1).value == "DATE  :":
            trade_date = (sheet.cell(0, 2).value).replace("/", "-")
            TRADE_DATE = acm.Time.DateAddDelta(trade_date, 0, 0, 0)

        for row in range(9, rows):
            row_data = {}

            if not is_isin(sheet.cell(row, 1).value):
                continue

            row_data["isin"] = str(sheet.cell(row, 1).value)
            row_data["security_desc"] = str(sheet.cell(row, 3).value)
            row_data["trade_currency"] = str(sheet.cell(row, 8).value)
            row_data["trade_quantity"] = float((sheet.cell(row, 6).value).replace(",", ""))
            row_data["security_price"] = float((sheet.cell(row, 9).value).replace(",", ""))

            if row_data:
                holdings_container.add_record_mapping(row, row_data)

        if len(holdings_container.record_mapping) > 0:
            LOGGER.info("Statement of Holdings read successfully")
        else:
            LOGGER.info("No holdings read from statement of holdings")

    return holdings_container


def ael_main(dictionary):

    file_path = str(dictionary['input_file'])

    clear_parameter()
    holdings_container = read_holdings(file_path)
    generate_trades(holdings_container)
    save_parameter(EXTENSION_DICT)

    LOGGER.info("Completed successfully.")
