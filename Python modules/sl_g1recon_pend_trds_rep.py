"""----------------------------------------------------------------------------
PURPOSE   : Create a CSV report that is used by Intellimatch to reconcile the
            Security Loan pending trades to Global One. This report contains
            pending trades and is a counterpart to the report createdy by
            script sl_global_one_recon_file.
DPT/DESK  : Prime Services PCG/Securities Lending
REQUESTER : Candice Johnson (Prime SBL Futures Team)
DEVELOPER : Vojtech Sidorin
CR NUMBER : CHNG0002087372
-------------------------------------------------------------------------------

HISTORY
===============================================================================
Date       CR Number      Developer         Description
-------------------------------------------------------------------------------
2014-06-27 CHNG0002087372 Vojtech Sidorin   Initial implementation based on
                                            sl_global_one_recon_file
"""

import os
import time
import csv

import acm
import FRunScriptGUI

import sl_functions
from PS_BrokerFeesRates import get_vat_for_date

REPORT_FILENAME_PREFIX = "ABCAP_FA_SBLRecon_Pend_Trades"

REPORT_COLUMNS = (
        # (column name, method to get the value[, format])
        ("Loan Trade Number", "loan_trade_number"),
        ("Loan Trade Date", "loan_trade_date"),
        ("Security Code", "security_code"),
        ("ISIN", "isin"),
        ("L/B", "lender_or_borrower"),
        ("Borrower Code", "borrower_code"),
        ("Lender Code", "lender_code"),
        ("Lender Fee", "lender_fee", ".3f"),
        ("Trade Number", "trade_number"),
        ("Trade Status", "trade_status"),
        ("Movement Date", "movement_date"),
        ("Movement", "movement", ".0f"),
        ("Balance", "balance", ".0f"),
        ("Start", "start_date"),
        ("End", "end_date"),
        ("Loan/Return", "movement_type"),
        ("Rate", "rate", ".3f"),
        ("Price", "price", ".2f"),
        ("VAT", "vat"),
        ("Lender Rate Excl VAT", "lender_rate_excl_vat", ".3f"),
        ("Borrower Rate Excl VAT", "borrower_rate_excl_vat", ".3f"),
        ("Ref Value", "ref_value", ".2f"),
        ("Open End Status", "open_end_status"),
        ("Mark-To-Market Indicator", "mark_to_market_indicator")
        )

ael_gui_parameters = {
    "windowCaption": "SL Global One Reconciliation Report - Pending Trades",
    }

# Variable Name, Display Name, Type, Candidate Values,
# Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = [
    ["trade_filter", "Trade Filter", "FTradeSelection", None,
        "sl_g1recon_pend_trds", 1, 1, None, None, 1],
    ["outdir", "Output Directory", FRunScriptGUI.DirectorySelection(), None,
        FRunScriptGUI.DirectorySelection(), 1, 1, None, None, 1],
    ]

def ael_main(kwargs):
    """Front Arena hook function."""
    trade_filter = kwargs["trade_filter"][0]
    outdir = str(kwargs["outdir"])

    trades = trade_filter.Trades()
    outfilename = os.path.join(outdir, "{0}_{1}.csv"
                                       .format(REPORT_FILENAME_PREFIX,
                                               time.strftime("%Y%m%d%H%M%S")))
    write_report(outfilename, trades)
    # NOTE: The following message should end with the report filename for
    # the automatic backend testing to complete successfully.
    print(("Wrote report to {0}".format(outfilename)))

def write_report(filename, trades):
    """Write CSV report based on trades to filename."""
    with open(filename, "w") as f:
        writer = csv.writer(f, lineterminator="\n")
        # Write header
        __write_header(writer)
        # Write data rows
        for trade in trades:
            if __is_pending_loan(trade):
                __write_row(writer, LoanRow(trade))
            if __is_pending_partial_return(trade):
                __write_row(writer, PartialReturnRow(trade))
            if __is_pending_full_return(trade):
                __write_row(writer, FullReturnRow(trade))

def __is_pending_loan(trade):
    """Return true if trade stores info about a pending Loan.

    Loan (Security Loan) means the movement of securities from a lender
    to a borrower.  Information about a Loan is stored in the first trade
    of the daisy chain of Security Loan trades.

    Pending means the securities movement happens in the future.

    The date of the securities movement is given by the instrument's
    Start Date.
    """
    # To qualify as a Loan, the trade must be the first trade in the daisy
    # chain, i.e. its ContractTrdnbr points to the trade itself.
    is_contract = trade.ContractTrdnbr() == trade.Oid()
    is_pending = trade.Instrument().StartDate() > acm.Time().DateToday()
    if all((is_contract, is_pending)):
        return True
    else:
        return False

def __is_pending_partial_return(trade):
    """Return true if trade stores info about a pending Partial Return.

    Partial Return (on a Security Loan) means the movement of securities
    back from a borrower to a lender. The movement quantity is less than
    the remaining balance on the loan, hence the term Partial Return.

    Pending means the securities movement happens in the future.

    The date of the securities movement is given by the instrument's
    Start Date.
    """
    # To qualify as a Partial Return, the trade must not be the first
    # trade in the daisy chain, i.e. its ContractTrdnbr must point to some
    # other trade.
    is_not_contract = trade.ContractTrdnbr() != trade.Oid()
    is_pending = trade.Instrument().StartDate() > acm.Time().DateToday()
    if all((is_not_contract, is_pending)):
        return True
    else:
        return False

def __is_pending_full_return(trade):
    """Return true if trade stores info about a pending Full Return.

    Full Return (on a Security Loan) means the movement of securities
    back from a borrower to a lender, so that the loan is fully repaid.
    I.e. the movement quantity is same as the remaining balance on the
    loan, thus the loan can be closed.

    Pending means the securities movement happens in the future.

    The date of the securities movement is given by the instrument's
    End Date.
    """
    # To qualify as a Full Return, the trade must not be Open Ended
    # and it must have no regular descendant.
    is_not_open_ended = trade.Instrument().OpenEnd() != "Open End"
    has_no_regular_descendant = (
        trade.ConnectedTrade() is None or
        trade.ConnectedTrade().Status() in (
            "Void", "Confirmed Void", "Simulated") or
        trade.ConnectedTrade().Oid() in (trade.Oid(), trade.ContractTrdnbr())
        )
    is_pending = trade.Instrument().EndDate() > acm.Time().DateToday()
    if all((is_not_open_ended, has_no_regular_descendant, is_pending)):
        return True
    else:
        return False

def __write_header(writer):
    """Write the header row using (CSV) writer."""
    header = [column[0] for column in REPORT_COLUMNS]
    writer.writerow(header)

def __write_row(writer, row):
    """Write a data row using (CSV) writer."""
    values = []
    for colspec in REPORT_COLUMNS:
        colmethod = getattr(row, colspec[1])
        if len(colspec) >= 3:
            format_ = "{{value:{f}}}".format(f=colspec[2])
        else:
            format_ = "{value}"
        value = colmethod()
        if value is not None:
            values.append(format_.format(value=value))
        else:
            values.append(None)
    writer.writerow(values)

def get_parent_trade(trade):
    """Return parent trade."""
    parent = None
    try:
        if trade.Oid() == trade.TrxTrade().ConnectedTrdnbr():
            # Case 1: Trade is a descendant of Contract.
            parent = trade.TrxTrade()
        elif (trade.Oid() ==
                trade.TrxTrade().ConnectedTrade().MirrorTrade().Oid()):
            # Case 2: Trade is a descendant of Contract mirror.
            parent = trade.TrxTrade().MirrorTrade()
    except AttributeError:
        parent = None
    return parent

class ReportRow(object):
    """Base class for report rows."""

    def __init__(self, trade):
        self.trade = trade
        self.instrument = self.trade.Instrument()
        self.ins_addinfo = self.instrument.AdditionalInfo()
        self.underlying = self.instrument.Underlying()
        self.trade_addinfo = self.trade.AdditionalInfo()
        self.contract = self.trade.Contract()

    def loan_trade_number(self):
        return self.contract.Oid()

    def loan_trade_date(self):
        return self.contract.AcquireDay()

    def loan_start_date(self):
        return self.contract.Instrument.StartDate()

    def security_code(self):
        """Last part of instrument name after slash."""
        return self.underlying.Name().split("/")[-1]

    def isin(self):
        return self.underlying.Isin()

    def borrower_code(self):
        return self.__get_party_code(self.trade_addinfo.SL_G1Counterparty1())

    def lender_code(self):
        return self.__get_party_code(self.trade_addinfo.SL_G1Counterparty2())

    def lender_fee(self):
        try:
            fee = float(self.trade_addinfo.SL_G1Fee2())
        except (ValueError, TypeError):
            fee = None
        return fee

    def trade_number(self):
        return self.trade.Oid()

    def trade_status(self):
        return self.trade.Status()

    def quantity(self):
        return self.trade.QuantityInUnderlying()

    def lender_or_borrower(self):
        if self.trade.Quantity() < 0.:
            return "Lender"
        else:
            return "Borrower"

    def start_date(self):
        return self.instrument.StartDate()

    def end_date(self):
        return self.instrument.EndDate()

    def rate(self):
        return self.instrument.Legs()[0].FixedRate()

    def price(self):
        # NOTE: Logic based on script sl_global_one_recon_file.py.
        _price = None
        if self.ins_addinfo.SL_CFD():
            today = acm.Time().DateToday()
            mtm_date = sl_functions.GetMtMDate(today)
            if self.underlying.InsType() in ("Bond", "IndexLinkedBond"):
                calendar = acm.FCalendar["ZAR Johannesburg"]
                adjust_banking_days = calendar.AdjustBankingDays(
                    mtm_date, self.underlying.SpotBankingDaysOffset())
                bond_mtm_price = self.underlying.UsedPrice(
                    mtm_date, "ZAR", "SPOT_BESA")
                _price = sl_functions.YTM_To_Price(
                    self.underlying, adjust_banking_days, bond_mtm_price, True)
            else:
                _price = self.underlying.MtMPrice(
                        mtm_date, self.underlying.Currency(), 0)
        else:
            _price = self.trade.AllInPrice()
        return _price*self.underlying.Quotation().QuotationFactor()

    def vat(self):
        return self.ins_addinfo.SL_VAT()

    def lender_rate_excl_vat(self):
        rate = self.lender_fee()
        if rate is not None and self.vat():
            rate /= self.__vat_rate()
        return rate

    def borrower_rate_excl_vat(self):
        rate = self.instrument.Legs()[0].FixedRate()
        if self.vat():
            rate /= self.__vat_rate()
        return rate

    def ref_value(self):
        # NOTE: Logic based on script sl_global_one_recon_file.py.
        value = 0.
        today = acm.Time().DateToday()
        csc = acm.FStandardCalculationsSpaceCollection()
        for cf in self.instrument.Legs()[0].CashFlows():
            if (cf.CashFlowType() in ("Fixed Rate",
                                      "Fixed Rate Adjustable") and
                    cf.StartDate() <= today <= cf.EndDate()):
                value = cf.Calculation().Nominal(
                        csc, self.trade, self.trade.Currency()).Number()
        return value

    def open_end_status(self):
        return self.instrument.OpenEnd()

    def mark_to_market_indicator(self):
        return self.instrument.MtmFromFeed()

    def movement(self):
        raise NotImplementedError

    def movement_date(self):
        raise NotImplementedError

    def balance(self):
        raise NotImplementedError

    def movement_type(self):
        """Loan/Return"""
        raise NotImplementedError

    def __get_party_code(self, party_name):
        """Return borrower/lender party code."""

        # NOTE: Logic based on script sl_global_one_recon_file.py.

        if not party_name:
            return None

        choicelist = None
        party_type = party_name[0]
        if party_type == "F":
            choicelist = acm.FChoiceList.Select01(
                    "name = 'GlobalOneFunds'",
                    "Duplicate choicelists 'GlobalOneFunds'.")
        elif party_type == "B":
            choicelist = acm.FChoiceList.Select01(
                    "name = 'GlobalOneBorrowers'",
                    "Duplicate choicelists 'GlobalOneBorrowers'.")
        elif party_type == "L":
            choicelist = acm.FChoiceList.Select01(
                    "name = 'GlobalOneLenders'",
                    "Duplicate choicelists 'GlobalOneLenders'.")

        party_code = None
        if choicelist is not None:
            for choice in choicelist.Choices():
                if choice.Name() == party_name:
                    party_code = choice.Description()
        else:
            party = acm.FParty[party_name]
            if party is not None:
                party_code = party.AdditionalInfo().SL_G1PartyCode()
        return party_code

    def __vat_rate(self):
        return get_vat_for_date(self.trade.ValueDay())


class LoanRow(ReportRow):
    """Row representing the first trade in a loan daisy chain.

    Interpret a trade as the initial quantity movement (loan).
    """

    def movement(self):
        return abs(self.trade.QuantityInUnderlying())

    def movement_date(self):
        return self.instrument.StartDate()

    def balance(self):
        return abs(self.trade.QuantityInUnderlying())

    def movement_type(self):
        return "Loan"

class PartialReturnRow(ReportRow):
    """Row representing partial return.

    Interpret a trade as a partial return.
    """

    def movement(self):
        _movement = None
        parent = get_parent_trade(self.trade)
        if parent is not None:
            _movement = (self.trade.QuantityInUnderlying() -
                         parent.QuantityInUnderlying())
        if _movement is not None:
            return abs(_movement)
        else:
            return None

    def movement_date(self):
        return self.instrument.StartDate()

    def balance(self):
        return abs(self.trade.QuantityInUnderlying())

    def movement_type(self):
        return "Return"

class FullReturnRow(ReportRow):
    """Row representing full return.

    Interpret a trade as a full return.
    """

    def movement(self):
        return abs(self.trade.QuantityInUnderlying())

    def movement_date(self):
        return self.instrument.EndDate()

    def balance(self):
        return 0.

    def movement_type(self):
        return "Return"
