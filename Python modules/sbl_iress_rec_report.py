'''--------------------------------------------------------------------------------------
MODULE
    sbl_iress_rec_report

DESCRIPTION
    Date                : 2020-04-20
    Purpose             : Script generates IRESS Recon downstream report
    Department and Desk : SBL and Collateral
    Requester           : Gasant Thulsie, James Stevens
    Developer           : Sihle Gaxa
    JIRA                : PCGDEV-60

HISTORY
=========================================================================================
Date            JIRA no        Developer               Description
-----------------------------------------------------------------------------------------
2020-04-20      PCGDEV-60      Sihle Gaxa              Initial implementation.

ENDDESCRIPTION
--------------------------------------------------------------------------------------'''
import acm
import csv
import datetime

from at_logging import getLogger
import FUploaderFunctions as gen_uploader
import sbl_reporting_utils as reporting_utils

LOGGER = getLogger(__name__)
FILE_HEADERS = ["BGNREF", "LINKREF", "CPTY",
                "PTYPE", "QTY", "STOCK", "TRADE",
                "SSET_DT", "SMODE", "LNRATE", "MIN_FEE",
                "LNPRC", "COLL_FLG", "OP", "STATUS", "LNVAL", "CLASS"]


class RowData(reporting_utils.ReportingData):

    def __init__(self, trade, instrument, counterparty, run_date):
        super(RowData, self).__init__(trade, instrument, counterparty, run_date)
        self.data = {}

    def get_row_data(self):
        try:
            default_value = 0
            trade_date = self.get_trade_date()
            trade_quantity = self.get_trade_quantity()
            instrument_name = self.instrument.Name()[4:]
            instrument_class = self.get_instrument_class()
            counterparty_code = self.get_counterparty_code()
            trade_settlement_date = self.get_settlement_date()
            trade_settlement_type = self.trade.add_info("SL_SWIFT")
            trade_market_value = self.get_market_value(trade_quantity)
            if int(trade_market_value) == 0:
                return
            if not trade_settlement_type:
                trade_settlement_type = "SWIFT"
            if self.get_counterparty_major() in self.EXCLUDED_MAJORS:
                return

            LOGGER.info("Writing common row details for {trade}".format(trade=self.trade.Oid()))

            self.data["QTY"] = trade_quantity
            self.data["LNPRC"] = default_value
            self.data["MIN_FEE"] = default_value
            self.data["STOCK"] = instrument_name
            self.data["CPTY"] = counterparty_code
            self.data["CLASS"] = instrument_class
            self.data["OP"] = self.OPEN_TRADE_FLAG
            self.data["STATUS"] = self.LOANED_FLAG
            self.data["LNVAL"] = trade_market_value
            self.data["TRADE"] = self.get_trade_date()
            self.data["SMODE"] = trade_settlement_type
            self.data["SSET_DT"] = trade_settlement_date
            self.data["BGNREF"] = self.get_settlement_id()
            self.data["COLL_FLG"] = self.TRADE_FLAG["Loan"]
            self.data["LINKREF"] = self.trade.Oid()

            if self.trade.Instrument().InsType() == "SecurityLoan":
                return self.add_loan_details()
            elif (reporting_utils.COLL_INSTYPE_BOND_QUERY.IsSatisfiedBy(self.trade.Instrument()) 
                    or reporting_utils.COLL_INSTYPE_EQUITY_QUERY.IsSatisfiedBy(self.trade.Instrument())):
                return self.add_non_cash_collateral_details()
            elif reporting_utils.COLL_INSTYPE_CASH_QUERY.IsSatisfiedBy(self.trade.Instrument()):
                return self.add_cash_collateral_details()
        except Exception as e:
            LOGGER.info("Could not add row because {err}".format(err=str(e)))
            raise Exception("Could not add row because {error}".format(error=str(e)))

    def add_loan_details(self):
        trade_rate = self.get_trade_rate()
        trade_price = self.get_trade_price()
        LOGGER.info("Writing loan details for {loan}".format(loan=self.trade.Instrument().Name()))
        self.data["LNPRC"] = trade_price
        self.data["LNRATE"] = trade_rate
        self.data["BGNREF"] = self.get_settlement_id()
        self.data["LNVAL"] = abs(round((trade_price * self.data["QTY"]), 2))
        if self.get_counterparty_type() == "Borrower":
            self.data["PTYPE"] = self.LOANED_FLAG
        else:
            self.data["PTYPE"] = self.BORROWED_FLAG
        return self.data

    def add_non_cash_collateral_details(self):
        self.data["LNVAL"] = 0
        self.data["LNRATE"] = 0
        counterparty_type = self.get_counterparty_type()
        if self.instrument.InsType() == "CD":
            self.data["STOCK"] = "NCD"
        collateral_flag = self.get_collateral_flag(self.get_trade_quantity(), counterparty_type)
        LOGGER.info("Writing non-cash collateral details for {ins}".format(ins=self.instrument.Name()))
        self.data["PTYPE"] = collateral_flag
        self.data["COLL_FLG"] = self.TRADE_FLAG["Collateral"]
        return self.data

    def add_cash_collateral_details(self):
        counterparty_type = self.get_counterparty_type()
        counterparty_code = self.get_counterparty_code()
        deposit_rate = self.instrument.Legs()[0].FixedRate()
        if counterparty_type == "Borrower":
            self.data["PTYPE"] = self.LOANED_FLAG
        else:
            self.data["PTYPE"] = self.BORROWED_FLAG
        deposit_name = "{code}:{flag}:{currency}".format(
                        code=counterparty_code, flag=self.data["PTYPE"],
                        currency=self.instrument.Currency().Name())
        LOGGER.info("Writing cash collateral details for {cash}".format(cash=self.instrument.Name()))
        self.data["QTY"] = 0
        self.data["CLASS"] = ""
        self.data["STOCK"] = ""
        self.data["TRADE"] = ""
        self.data["SMODE"] = ""
        self.data["STATUS"] = ""
        self.data["LINKREF"] = ""
        self.data["SSET_DT"] = ""
        self.data["BGNREF"] = deposit_name
        self.data["LNRATE"] = deposit_rate
        return self.data


def add_file_data(trades, run_date, directory):
    try:
        with open(directory, "wb") as csv_file:
            writer = csv.DictWriter(csv_file, FILE_HEADERS)
            writer.writeheader()
            for trade in trades[0].Trades():
                LOGGER.info("Processing trade {trade}".format(trade=trade.Oid()))
                instrument = trade.Instrument()
                instrument_type = instrument.InsType()
                trade_counterparty = trade.Counterparty()
                if instrument_type == "SecurityLoan":
                    lender = trade.add_info("SL_G1Counterparty2")
                    borrower = trade.add_info("SL_G1Counterparty1")
                    lender_counterparty = acm.FParty[lender]
                    borrower_counterparty = acm.FParty[borrower]
                    if lender_counterparty and lender_counterparty.add_info("PERFIX_CLIENT") == "Yes":
                        trade_row = RowData(trade, instrument.Underlying(),
                                            lender_counterparty, run_date)
                        row_data = trade_row.get_row_data()
                        if row_data:
                            writer.writerow(row_data)
                    if borrower_counterparty and borrower_counterparty.add_info("PERFIX_CLIENT") == "Yes":
                        trade_row = RowData(trade, instrument.Underlying(),
                                            borrower_counterparty, run_date)
                        row_data = trade_row.get_row_data()
                        if row_data:
                            writer.writerow(row_data)
                elif ((reporting_utils.COLL_INSTYPE_BOND_QUERY.IsSatisfiedBy(instrument) 
                            or reporting_utils.COLL_INSTYPE_EQUITY_QUERY.IsSatisfiedBy(instrument))
                        and trade_counterparty.add_info("PERFIX_CLIENT") == "Yes"):
                    trade_row = RowData(trade, instrument, trade.Counterparty(), run_date)
                    row_data = trade_row.get_row_data()
                    if row_data:
                        writer.writerow(row_data)
                elif instrument_type == "Deposit" and trade_counterparty.add_info("PERFIX_CLIENT") == "Yes":
                    trade_row = RowData(trade, instrument, trade.Counterparty(), run_date)
                    row_data = trade_row.get_row_data()
                    if row_data:
                        writer.writerow(row_data)
    except Exception as e:
        LOGGER.info("Could not get file data because {err}".format(err=str(e)))
        raise Exception("Could not get file data because {err}".format(err=str(e)))

ael_variables = reporting_utils.get_ael_variables()


def ael_main(dictionary):
    try:
        file_name = dictionary["file_name"]
        run_date = gen_uploader.get_input_date(dictionary)
        date_string = datetime.datetime.strptime(str(run_date), '%Y-%m-%d').strftime('%m%d')
        filename = "{file_name}_{file_date}01.txt".format(file_name=file_name,
                                                          file_date=date_string)
        output_file, run_date = reporting_utils.get_directory(dictionary, filename, True)
        add_file_data(dictionary["sbl_trades"], run_date, output_file)
        LOGGER.info("Completed successfully")
        LOGGER.info("Wrote secondary output to: {path}".format(path=output_file))
    except Exception as e:
        LOGGER.info("Failed to write file because {err}".format(err=str(e)))
        raise Exception("Failed to write file because {error}".format(error=str(e)))
