'''--------------------------------------------------------------------------------------
MODULE
    sbl_sasla_report

DESCRIPTION
    Date                : 2020-04-20
    Purpose             : Script generates SBL SASLA report
    Department and Desk : SBL
    Requester           : Gasant Thulsie, James Stevens
    Developer           : Sihle Gaxa
    JIRA                : PCGDEV-30

HISTORY
=========================================================================================
Date            JIRA no        Developer               Description
-----------------------------------------------------------------------------------------
2020-04-20      PCGDEV-30      Sihle Gaxa              Initial implementation.

ENDDESCRIPTION
--------------------------------------------------------------------------------------'''
import os
import csv
import acm

import FBDPGui
import FRunScriptGUI
from at_logging import getLogger
import FUploaderFunctions as gen_uploader
import sbl_reporting_utils as reporting_utils
from at_ael_variables import AelVariableHandler


LOGGER = getLogger(__name__)
BORROWER_DIRECTION = "Loaned to"
LENDER_DIRECTION = "Borrowed to"
FILE_HEADERS = ["Report Date", "Len/Bor", "Trade Reference",
                "Security Settlement Date", "Security or Cash",
                "Quantity (Authorised)", "Market Value",
                "Major Code", "Cpty Code", "Cpty", "Cpty Full Name",
                "Legal Entity Id", "SASLA", "Local/Int", "Class"]


class RowData(reporting_utils.ReportingData):

    def __init__(self, trade, instrument, counterparty, run_date):
        super(RowData, self).__init__(trade, instrument, counterparty, run_date)
        self.data = {}

    def add_trade_details(self):
        try:
            underlying_type = None
            trade_quantity = self.get_trade_quantity()
            underlying_name = self.instrument.Name()[4:]
            trade_settlement_date = self.trade.ValueDay()
            trade_exposure = self.get_market_value(trade_quantity)

            if self.instrument_type in ["Stock", "ETF"]:
                underlying_type = "Equities"
            elif self.instrument_type in ["Bond", "IndexLinkedBond"]:
                underlying_type = "Bonds"

            self.data["Class"] = underlying_type
            self.data["Report Date"] = self.run_date
            self.data["Market Value"] = trade_exposure
            self.data["Trade Reference"] = self.trade.Oid()
            self.data["Security or Cash"] = underlying_name
            self.data["Quantity (Authorised)"] = trade_quantity
            self.data["Security Settlement Date"] = trade_settlement_date
            self.add_counterparty_details()
            return self.data

        except Exception as e:
            LOGGER.info("Could not get trade data because {err}".format(err=str(e)))
            raise Exception("Could not get trade data because {error}".format(error=str(e)))

    def add_counterparty_details(self):
        try:
            LOGGER.info("Setting {party} details".format(
                        party=self.counterparty.Name()))
            counterparty_region = None
            counterparty_name = self.counterparty.Name()
            counterparty_type = self.get_counterparty_type()
            counterparty_code = self.get_counterparty_code()
            counterparty_sdsid = self.get_counterparty_sdsid()
            counterparty_fullname = self.counterparty.FullName()
            counterparty_major_code = self.get_counterparty_major()
            counterparty_sasla_membership = self.counterparty.Free1()

            if self.counterparty.Free2ChoiceList():
                counterparty_region = "International"
            else:
                counterparty_region = "Local"
            if counterparty_type == "Lender":
                self.data["Len/Bor"] = LENDER_DIRECTION
            elif counterparty_type == "Borrower":
                self.data["Len/Bor"] = BORROWER_DIRECTION
            self.data["Cpty"] = counterparty_name
            self.data["Cpty Code"] = counterparty_code
            self.data["Local/Int"] = counterparty_region
            self.data["Major Code"] = counterparty_major_code
            self.data["Legal Entity Id"] = counterparty_sdsid
            self.data["SASLA"] = counterparty_sasla_membership
            self.data["Cpty Full Name"] = counterparty_fullname
            return self.data
        except Exception as e:
            LOGGER.info("Could not get counterparty data because {err}".format(err=str(e)))
            raise Exception("Could not get counterparty data because {error}".format(error=str(e)))

def add_file_data(trades, run_date, directory):
    try:
        with open(directory, "wb") as csv_file:
            writer = csv.DictWriter(csv_file, FILE_HEADERS)
            writer.writeheader()
            for trade in trades[0].Trades():
                LOGGER.info("Processing trade {trade}".format(trade=trade.Oid()))
                lender = trade.add_info("SL_G1Counterparty2")
                borrower = trade.add_info("SL_G1Counterparty1")
                lender_counterparty = acm.FParty[lender]
                borrower_counterparty = acm.FParty[borrower]
                instrument = trade.Instrument().Underlying()
                if lender_counterparty:
                    trade_row = RowData(trade, instrument, lender_counterparty, run_date)
                    row_data = trade_row.add_trade_details()
                    if row_data:
                        writer.writerow(row_data)
                if borrower_counterparty:
                    trade_row = RowData(trade, instrument, borrower_counterparty, run_date)
                    row_data = trade_row.add_trade_details()
                    if row_data:
                        writer.writerow(row_data)
    except Exception as e:
        LOGGER.info("Could not trade data because {err}".format(err=str(e)))
        raise Exception("Could not trade data because {error}".format(error=str(e)))

ael_variables = reporting_utils.get_ael_variables()


def ael_main(dictionary):
    try:
        output_file, run_date = reporting_utils.get_directory(dictionary, None, True)
        add_file_data(dictionary["sbl_trades"], run_date, output_file)
        LOGGER.info("Completed successfully")
        LOGGER.info("Wrote secondary output to: {path}".format(path=output_file))
    except Exception as e:
        LOGGER.info("Failed to generate file because {err}".format(err=str(e)))
        raise Exception("Failed to generate file because {error}".format(error=str(e)))
