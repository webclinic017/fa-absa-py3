'''--------------------------------------------------------------------------------------
MODULE
    sbl_reporting_utils

DESCRIPTION
    Date                : 2020-04-20
    Purpose             : Reporting utils script for
                          SBL downstream reports
    Department and Desk : SBL and Collateral
    Requester           : Gasant Thulsie, James Stevens
    Developer           : Sihle Gaxa
    JIRA                : PCGDEV-15

HISTORY
=========================================================================================
Date            JIRA no        Developer               Description
-----------------------------------------------------------------------------------------
2020-04-20      PCGDEV-15      Sihle Gaxa              Initial implementation.
2020-11-25      PCGDEV-15      Jaysen Naicker          Change default filter to sbl_margin_summary_positions
ENDDESCRIPTION
--------------------------------------------------------------------------------------'''
import os
import csv
import acm
import datetime

import FBDPGui
import FRunScriptGUI
from at_logging import getLogger
import sl_all_in_price as sl_price
import FUploaderFunctions as gen_uploader
from at_ael_variables import AelVariableHandler

LOGGER = getLogger(__name__)
TODAY = acm.Time().DateToday()
CALENDAR = acm.FCalendar["ZAR Johannesburg"]
COLL_INSTYPE_BOND_QUERY = acm.FStoredASQLQuery['SL_Collateral_Bond'].Query()
COLL_INSTYPE_CASH_QUERY = acm.FStoredASQLQuery['SL_Collateral_Cash'].Query()
COLL_INSTYPE_EQUITY_QUERY = acm.FStoredASQLQuery['SL_Collateral_Equity'].Query()
CALC_SPACE = acm.Calculations().CreateCalculationSpace('Standard', 'FTradeSheet')


class ReportingData(object):

    OP_FLAG = "OP"
    LOANED_FLAG = "L"
    BORROWED_FLAG = "B"
    OPEN_TRADE_FLAG = "O"
    COLLATERAL_TYPE = "MX"
    LENDER_FLAG = "LENDER"
    BORROWER_FLAG = "BORROWER"
    COLLATERAL_RECEIVED = "CLR"
    COLLATERAL_DELIVERED = "CLD"
    EXCLUDED_MAJORS = ["ABSASL", "COLLAC"]
    TRADE_FLAG = {"Loan": "T", "Collateral": "C"}
    INSTRUMENT_CLASS = {"Bond": "BND", "Stock": "OS",
                        "CD": "NCD", "Deposit": "",
                        "Bill": "BILL", "IndexLinkedBond": "BND"}

    def __init__(self, trade, instrument, counterparty, run_date):
        self.trade = trade
        self.run_date = run_date
        self.instrument = instrument
        self.counterparty = counterparty
        self.instrument_type = instrument.InsType()

    def get_counterparty_code(self):
        counterparty_code = self.counterparty.add_info("SL_G1PartyCode")
        return counterparty_code

    def get_counterparty_major(self):
        counterparty_major = self.counterparty.add_info("SL_MajorPtyCode")
        return counterparty_major

    def get_counterparty_type(self):
        counterparty_type = self.counterparty.add_info("SL_CptyType")
        return counterparty_type

    def get_trade_quantity(self):
        instrument = self.trade.Instrument()
        if (COLL_INSTYPE_BOND_QUERY.IsSatisfiedBy(instrument) 
                or COLL_INSTYPE_EQUITY_QUERY.IsSatisfiedBy(instrument)):
            return abs(round(CALC_SPACE.CalculateValue(self.trade, "Reporting Quantity"), 0))
        return abs(round(CALC_SPACE.CalculateValue(self.trade, "Quantity"), 0))

    def get_settlement_date(self):
        settlement_date = datetime.datetime.strptime(self.trade.ValueDay(), "%Y-%m-%d").strftime("%Y%m%d")
        return settlement_date

    def get_trade_date(self):
        return datetime.datetime.strptime(self.trade.TradeTime(), "%Y-%m-%d %H:%M:%S").date().strftime("%Y%m%d")

    def get_counterparty_sdsid(self):
        return self.counterparty.add_info("BarCap_SMS_CP_SDSID")

    def get_trade_fee(self):
        trade_fee = 0
        if CALC_SPACE.CalculateValue(self.trade, "SL Fee Excl. VAT"):
            trade_fee = abs(round(CALC_SPACE.CalculateValue(self.trade, "SL Fee Excl. VAT"), 3))
        return trade_fee

    def get_market_value(self, quantity):
        market_value = self.get_trade_value(quantity)
        return market_value

    def get_trade_value(self, trade_quantity):
        trade_instrument = self.trade.Instrument()
        previous_day = CALENDAR.AdjustBankingDays(self.run_date, -1)
        if trade_instrument.InsType() == "SecurityLoan" and trade_instrument.Legs()[0].EndDate() == self.run_date:
            trade_price = sl_price.sl_all_in_price(trade_instrument.Underlying(), previous_day)
            return abs(round((trade_quantity * trade_price), 2))
        try:
            return abs(round(CALC_SPACE.CalculateValue(self.trade, "SOB Market Value").Number(), 2))
        except Exception as e:
            LOGGER.exception("Could not get market value for trade {trade} because {error}".format(
                            trade=self.trade.Oid(), error=str(e)))
            return 0

    def get_counterparty_name(self, counterparty_type):
        if (self.counterparty.Name().startswith("SLB") or counterparty_type == "Borrower"):
            return "{cpty_name}-{cpty_type}".format(
                    cpty_name=self.counterparty.Name(),
                    cpty_type=self.BORROWER_FLAG), self.LOANED_FLAG
        else:
            return "{cpty_name}-{cpty_type}".format(
                    cpty_name=self.counterparty.Name(),
                    cpty_type=self.LENDER_FLAG), self.BORROWED_FLAG

    def get_instrument_description(self):
        if self.instrument.InsType() == "Stock" and self.instrument.Issuer():
            return self.instrument.Issuer().Name()
        return self.instrument.Name()[4:]

    def get_trade_rate(self):
        trade_rate = 0
        if CALC_SPACE.CalculateValue(self.trade, "SL Fee Excl. VAT"):
            trade_rate = CALC_SPACE.CalculateValue(self.trade, "SL Fee Excl. VAT")
        return trade_rate

    def get_trade_price(self):
        trade_price = 0
        if self.instrument in ["Stock", "ETF"]:
            trade_price = abs(float(CALC_SPACE.CalculateValue(self.trade, "Original Price")/100))
        else:
            trade_price = abs(float(self.trade.AllInPrice()/100))
        return trade_price

    def get_instrument_class(self):
        if self.instrument_type in ["Stock", "ETF"]:
            return self.INSTRUMENT_CLASS["Stock"]
        if self.instrument_type in ["Bond", "IndexLinkedBond"]:
            return self.INSTRUMENT_CLASS["Bond"]
        if self.instrument_type in ["CD", "Bill"]:
            return self.INSTRUMENT_CLASS["CD"]
        if self.instrument_type == "Deposit":
            return self.INSTRUMENT_CLASS["Deposit"]
        return ""

    def get_collateral_flag(self, quantity, counterparty_type):
        if counterparty_type == "Borrower" and quantity > 0:
            return self.COLLATERAL_RECEIVED
        elif counterparty_type == "Borrower" and quantity < 0:
            return self.COLLATERAL_DELIVERED
        elif counterparty_type == "Lender" and quantity > 0:
            return self.COLLATERAL_DELIVERED
        else:
            return self.COLLATERAL_RECEIVED

    def get_settlement_id(self):
        try:
            trade_settlements = self.trade.Settlements()
            for trade_settlement in trade_settlements:
                if (trade_settlement.Type() in ["Security Nominal", "End Security"] and
                    trade_settlement.Status() != "Void" and
                    trade_settlement.Counterparty().Oid() == self.counterparty.Oid()):
                    return trade_settlement.Oid()
            return self.trade.Oid()
        except Exception as e:
            return self.trade.Oid()


def get_ael_variables():

    ael_variables = gen_uploader.get_ael_variables()
    email_variable = ael_variables[4]
    ael_variables.remove(email_variable)
    ael_variables.add("sbl_trades",
                      label="Trades",
                      cls="FTradeSelection",
                      default=acm.FTradeSelection["sbl_margin_summary_positions"],
                      multiple=True,
                      alt="sbl margin summary positions"
                      )
    ael_variables.extend(FBDPGui.LogVariables())
    return ael_variables


def reset_global_variables(run_date):
    global_simulations = [("Portfolio Profit Loss End Date", 'Custom Date'),
                          ("Portfolio Profit Loss End Date Custom", run_date),
                          ("Valuation Parameter Date", run_date),
                          ("Valuation Date", run_date)]
    for column, value in global_simulations:
        CALC_SPACE.SimulateGlobalValue(column, value)


def get_directory(dictionary, explicit_filename=None, is_feed=None):

    file_name = dictionary["file_name"]
    directory = str(dictionary["file_path"])
    run_date = gen_uploader.get_input_date(dictionary)
    reset_global_variables(run_date)
    output_filename = "%s_%s.csv" % (file_name, run_date)
    if explicit_filename:
        output_filename = explicit_filename

    if is_feed:
        output_file = os.path.join(directory, output_filename)
        return output_file, run_date

    file_directory = os.path.join(directory, "{}".format(run_date))
    if not os.path.exists(file_directory):
        os.makedirs(file_directory)
    output_file = os.path.join(file_directory, output_filename)
    return output_file, run_date


def get_open_trade(ael_trade, *rest):
    trade = acm.FTrade[ael_trade.contract_trdnbr]
    return get_last_settled_trade(trade)


def get_last_settled_trade(trade, buffer=None):
    if trade and trade.SLPartialReturnIsPartOfChain():
        LOGGER.info("Processing trade {trd}".format(trd=trade.Oid()))
        trade_pending = acm.FSettlement.Select("trade = {trade_number} and \
                                                type in {types} and status in {statuses}".format(
                                                trade_number=trade.Oid(), types=("End Security", "Security Nominal"),
                                                statuses=tuple(set(acm.FEnumeration["enum(SettlementStatus)"].Enumerators()) -
                                                {"Closed", "Settled", "Cancelled", "Pending Closure"})))
        if trade_pending:
            LOGGER.info("{pending_trade} has a pending settlement".format(
                        pending_trade=trade.Oid()))
            if trade.Oid() == trade.ContractTrdnbr():
                LOGGER.info("Original loan trade {loan} has not settled".format(loan=trade.Oid()))
                return 0
            return trade.TrxTrade().Oid()
        elif buffer and trade.Oid() in buffer:
            return trade.TrxTrade().Oid()
        else:
            if not buffer:
                buffer = set()
            buffer.add(trade.Oid())
            return get_last_settled_trade(get_next_trade(trade), buffer)
    else:
        return 0


def is_partially_returned(trade):
    return (trade.Instrument().InsType() == "SecurityLoan" and
            trade.Oid() != trade.ConnectedTrdnbr() and
            trade.ContractTrdnbr() != trade.ConnectedTrdnbr())


def get_next_trade(trade):
    if is_partially_returned(trade):
        return trade.ConnectedTrade()
    else:
        return None


def is_loan_settled(trade):
    settlements = acm.FSettlement.Select('trade=%s and type in ("Security Nominal", "End Security")'
                                         % trade.Oid())
    if not settlements:
        return False
    if any([settlement.Status() == 'Settled' for settlement in settlements]):
        return True
    return False


def is_coll_settled(trade):
    if trade.Instrument().InsType() == 'Deposit':
        return True
    settlements = acm.FSettlement.Select('trade=%s' % trade.Oid())
    if not settlements:
        return False
    if any([settlement.Status() == 'Settled' for settlement in settlements]):
        return True
    return False


def get_next_loan(trade):
    contract = trade.Contract().Oid()
    trades = list(acm.FTrade.Select("contract=%s and status in ('FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed')"
                                     % contract))
    trades.sort(key = lambda t: (t.Instrument().StartDate(), t.Oid()))
    if trades:
        if not trade in trades:
            return trades[-1]
        index = trades.index(trade)
        try:
            return trades[index+1]
        except IndexError:
            return trades[-1]
    return None


def include_loan(ael_trade, *_args):
    trade = acm.FTrade[ael_trade.trdnbr]
    if not trade:
        return False
    settled = is_loan_settled(trade)
    if not settled:
        return False
    if trade.Instrument().OpenEnd() != 'Terminated':
        return True
    if trade.Instrument().ExpiryDateOnly() > TODAY:
        return True
    next_trade = get_next_loan(trade)
    if (next_trade and trade != next_trade 
            and not is_loan_settled(next_trade)):
        return True
    return False


def include_coll(ael_trade, *_args):
    trade = acm.FTrade[ael_trade.trdnbr]
    if not trade:
        return False
    settled = is_coll_settled(trade)
    if trade.Text1() in ('PARTIAL_RETURN', 'FULL_RETURN'):
        if not settled:
            return True
        return False
    if settled:
        return True
    return False
