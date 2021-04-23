'''--------------------------------------------------------------------------------------
MODULE
    sbl_credit_exposure

DESCRIPTION
    Date                : 2020-04-20
    Purpose             : Script to generate SBL Credit Exposure report
    Department and Desk : SBL and Collateral
    Requester           : Shaun Du Plessis and James Stevens
    Developer           : Sihle Gaxa
    JIRA                : PCGDEV-49 and PCGDEV-27

HISTORY
=========================================================================================
Date            JIRA no         Developer               Description
-----------------------------------------------------------------------------------------
2020-04-20      PCGDEV-49       Sihle Gaxa              Initial implementation.

ENDDESCRIPTION
--------------------------------------------------------------------------------------'''
import csv
import acm

import FRunScriptGUI
from at_logging import getLogger
import sl_all_in_price as sl_price
from collections import defaultdict
import sbl_reporting_utils as reporting_utils

LOGGER = getLogger(__name__)
LENDERS = defaultdict(lambda: defaultdict(float))
BORROWERS = defaultdict(lambda: defaultdict(float))
FILE_HEADERS = ["Client Major Code", "Client Full Name",
                "Exposure", "Cash Collateral", "Equities Collateral",
                "Bonds/NCDs Collateral", "Total Collateral", "% of Exp"]


class FileWriter(object):

    def __init__(self, file_directory):
        self.data = {}
        self.file_directory = file_directory

    def write_file(self):
        try:
            available_collateral = 0
            loan_exposure_balance = 0
            available_bond_collateral = 0
            available_cash_collateral = 0
            available_equity_collateral = 0
            LOGGER.info("Starting file writing process")
            LOGGER.info("=" * 80)
            with open(self.file_directory, "wb") as csv_file:
                writer = csv.DictWriter(csv_file, FILE_HEADERS)
                writer.writeheader()
                writer.writerow(self.add_empty_line("BORROWERS"))
                borrower_exp, borrower_cash, borrower_eqty, borrower_bond, borrower_coll = self.add_trade_rows(writer, BORROWERS)
                writer.writerow(self.add_counterparty_totals("Total Borrowers",
                                                             borrower_exp, borrower_cash,
                                                             borrower_eqty, borrower_bond, borrower_coll))
                LOGGER.info("Borrower counterparty details successfully added")
                writer.writerow(self.add_empty_line())
                writer.writerow(self.re_write_header())
                writer.writerow(self.add_empty_line("LENDERS"))
                lender_exposure, lender_cash, lender_eqty, lender_bonds, lender_collateral = self.add_trade_rows(writer, LENDERS)
                writer.writerow(self.add_counterparty_totals("Total Lenders",
                                                             lender_exposure,
                                                             lender_cash, lender_eqty,
                                                             lender_bonds, lender_collateral))
                writer.writerow(self.add_empty_line())
                LOGGER.info("Lender counterparty details successfully added")
                self.add_summary_totals(writer, borrower_cash, lender_cash,
                                        borrower_bond, lender_bonds, borrower_eqty,
                                        lender_eqty, borrower_exp, lender_exposure)
        except Exception as e:
            LOGGER.info("Could not write file because {err}".format(err=str(e)))
            raise Exception("Could not write file because {error}".format(error=str(e)))

    def add_trade_rows(self, writer, trade_data):
        try:
            total_cash = 0
            total_bonds = 0
            total_equities = 0
            total_exposure = 0
            total_collateral = 0
            for counterparty_major in sorted(trade_data.keys()):
                counterparty_exposure = 0
                counterparty_total_collateral = 0
                counterparty_percentage_collateral = 0

                for column_name, exposure in trade_data[counterparty_major].items():
                    self.data[column_name] = exposure
                    self.data["Client Major Code"] = counterparty_major
                    LOGGER.info("{code} : {column} = {exposure}".format(code=counterparty_major,
                                                                        column=column_name,
                                                                        exposure=exposure))
                    if column_name == "Exposure":
                        total_exposure += exposure
                        counterparty_exposure += exposure
                    if column_name in ["Cash Collateral", "Equities Collateral", "Bonds/NCDs Collateral"]:
                        total_collateral += exposure
                        counterparty_total_collateral += exposure
                        if column_name == "Cash Collateral":
                            total_cash += exposure
                        elif column_name == "Equities Collateral":
                            total_equities += exposure
                        elif column_name == "Bonds/NCDs Collateral":
                            total_bonds += exposure
                if counterparty_exposure != 0:
                    counterparty_percentage_collateral = round((counterparty_total_collateral /
                                                                counterparty_exposure) * 100, 0)
                if not counterparty_exposure and counterparty_total_collateral == 0:
                    continue

                self.data["Client Full Name"] = self.get_cpty_fullname(counterparty_major)
                self.data["Total Collateral"] = counterparty_total_collateral
                self.data["% of Exp"] = counterparty_percentage_collateral
                writer.writerow(self.data)
                self.data.clear()

            return total_exposure, total_cash, total_equities, total_bonds, total_collateral
        except Exception as e:
            LOGGER.info("Could not add row because {err}".format(err=str(e)))
            raise Exception("Could not add row because {error}".format(error=str(e)))

    def get_cpty_fullname(self, major_code):
        counterparty = [party for party in acm.FParty.Select("")
                        if party.add_info("SL_MajorPtyCode") == major_code]
        if counterparty:
            return counterparty[0].FullName()

    def add_empty_line(self, counterparty_type=None):

        self.data["% of Exp"] = ""
        self.data["Exposure"] = ""
        self.data["Cash Collateral"] = ""
        self.data["Client Full Name"] = ""
        self.data["Total Collateral"] = ""
        self.data["Equities Collateral"] = ""
        self.data["Bonds/NCDs Collateral"] = ""
        if counterparty_type:
            self.data["Client Major Code"] = counterparty_type
        else:
            self.data["Client Major Code"] = ""
        return self.data

    def re_write_header(self):
        for column in FILE_HEADERS:
            self.data[column] = column
        return self.data

    def add_total(self, total_column, total_amount):

        self.data["% of Exp"] = ""
        self.data["Cash Collateral"] = ""
        self.data["Total Collateral"] = ""
        self.data["Client Major Code"] = ""
        self.data["Exposure"] = total_amount
        self.data["Equities Collateral"] = ""
        self.data["Bonds/NCDs Collateral"] = ""
        self.data["Client Full Name"] = total_column
        return self.data

    def add_counterparty_totals(self, party_type, exposure,
                                cash, equity, bond, total):
        self.data["% of Exp"] = ""
        self.data["Exposure"] = exposure
        self.data["Cash Collateral"] = cash
        self.data["Client Major Code"] = ""
        self.data["Total Collateral"] = total
        self.data["Equities Collateral"] = equity
        self.data["Bonds/NCDs Collateral"] = bond
        self.data["Client Full Name"] = party_type
        return self.data

    def add_summary_totals(self, writer, borrower_cash, lender_cash,
                           borrower_bonds, lender_bonds, borrower_eqty,
                           lender_eqty, borrower_exposure, lender_exposure):

        available_cash_collateral = borrower_cash-lender_cash
        available_bond_collateral = borrower_bonds-lender_bonds
        available_equity_collateral = borrower_eqty-lender_eqty
        available_collateral = (available_cash_collateral +
                                available_bond_collateral +
                                available_equity_collateral)
        loan_exposure_balance = borrower_exposure-lender_exposure
        LOGGER.info("Writing summary total")
        writer.writerow(self.add_total("Total Collateral:",
                                       available_collateral))
        writer.writerow(self.add_total("Available Cash Collateral:",
                                       available_cash_collateral))
        writer.writerow(self.add_total("Available Equities Collateral:",
                                       available_equity_collateral))
        writer.writerow(self.add_total("Available Bonds Collateral:",
                                       available_bond_collateral))
        writer.writerow(self.add_empty_line())
        writer.writerow(self.add_total("Balancing:", ""))
        writer.writerow(self.add_total("Total Borrowers Exposure",
                                       borrower_exposure))
        writer.writerow(self.add_total("Total Lenders Exposure",
                                       lender_exposure))
        writer.writerow(self.add_total("Exposure Difference",
                                       loan_exposure_balance))


class RowData(reporting_utils.ReportingData):

    def __init__(self, trade, instrument, counterparty, run_date, column_name):
        super(RowData, self).__init__(trade, instrument, counterparty, run_date)
        self.data = {}
        self.column_name = column_name

    def get_row_data(self):
        try:
            trade_quantity = self.get_trade_quantity()
            trade_instrument = self.trade.Instrument()
            instrument_type = trade_instrument.InsType()
            counterparty_code = self.get_counterparty_code()
            counterparty_type = self.get_counterparty_type()
            counterparty_fullname = self.counterparty.FullName()
            trade_exposure = self.get_market_value(trade_quantity)
            counterparty_major_code = self.get_counterparty_major()
            LOGGER.info("{type}: {major} = {exposure}".format(type=counterparty_type,
                                                              major=counterparty_major_code,
                                                              exposure=trade_exposure))
            if counterparty_major_code in self.EXCLUDED_MAJORS or int(trade_exposure) == 0:
                return

            if counterparty_type == "Lender" or self.counterparty.Name().startswith("SLL"):
                if counterparty_major_code in LENDERS:
                    LENDERS[counterparty_major_code][self.column_name] += trade_exposure
                else:
                    LENDERS[counterparty_major_code][self.column_name] = trade_exposure
            elif counterparty_type == "Borrower" or self.counterparty.Name().startswith("SLB"):
                if counterparty_major_code in BORROWERS:
                    BORROWERS[counterparty_major_code][self.column_name] += trade_exposure
                else:
                    BORROWERS[counterparty_major_code][self.column_name] = trade_exposure
        except Exception as e:
            LOGGER.exception("Could not process because {err}".format(err=str(e)))
            raise Exception("Could not process because {error}".format(error=str(e)))


def add_file_data(trades, run_date, collateral_instype_bond_query,
                  collateral_instype_cash_query, collateral_instype_equity_query):
    try:
        for trade in trades[0].Trades():
            LOGGER.info("Processing trade {trade}".format(trade=trade.Oid()))
            trade_row = None
            instrument = trade.Instrument()
            if instrument.InsType() == "SecurityLoan":
                lender = trade.add_info("SL_G1Counterparty2")
                borrower = trade.add_info("SL_G1Counterparty1")
                lender_counterparty = acm.FParty[lender]
                borrower_counterparty = acm.FParty[borrower]
                if lender_counterparty:
                    trade_row = RowData(trade,
                                        instrument.Underlying(),
                                        lender_counterparty, run_date,
                                        "Exposure")
                    trade_row.get_row_data()
                if borrower_counterparty:
                    trade_row = RowData(trade,
                                        instrument.Underlying(),
                                        borrower_counterparty, run_date,
                                        "Exposure")
                    trade_row.get_row_data()
            elif collateral_instype_equity_query.IsSatisfiedBy(instrument):
                trade_row = RowData(trade, instrument,
                                    trade.Counterparty(),
                                    run_date, "Equities Collateral")
                trade_row.get_row_data()
            elif collateral_instype_bond_query.IsSatisfiedBy(instrument):
                trade_row = RowData(trade, instrument,
                                    trade.Counterparty(),
                                    run_date, "Bonds/NCDs Collateral")
                trade_row.get_row_data()
            elif collateral_instype_cash_query.IsSatisfiedBy(instrument):
                trade_row = RowData(trade, instrument,
                                    trade.Counterparty(),
                                    run_date, "Cash Collateral")
                trade_row.get_row_data()
    except Exception as e:
        LOGGER.exception("Could not process trade data because {err}".format(err=str(e)))
        raise Exception("Could not process trade data because {error}".format(error=str(e)))

ael_variables = reporting_utils.get_ael_variables()


def ael_main(dictionary):
    try:
        file_name = "%s.csv" % (str(dictionary["file_name"]))
        output_file, run_date = reporting_utils.get_directory(dictionary, file_name, True)
        add_file_data(dictionary["sbl_trades"], run_date,
                      reporting_utils.COLL_INSTYPE_BOND_QUERY,
                      reporting_utils.COLL_INSTYPE_CASH_QUERY,
                      reporting_utils.COLL_INSTYPE_EQUITY_QUERY)
        file_writer = FileWriter(output_file)
        file_writer.write_file()
        LOGGER.info("Completed successfully")
        LOGGER.info("Wrote secondary output to: {path}".format(path=output_file))
    except Exception as e:
        LOGGER.exception("Failed to write file because {err}".format(err=str(e)))
        raise Exception("Failed to write file because {error}".format(error=str(e)))
