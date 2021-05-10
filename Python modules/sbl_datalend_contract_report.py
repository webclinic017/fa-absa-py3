'''--------------------------------------------------------------------------------------
MODULE
    sbl_datalend_contract_report

DESCRIPTION
    Date                : 2020-04-20
    Purpose             : Script generates Datalend Contract downstream report
    Department and Desk : SBL and Collateral
    Requester           : Gasant Thulsie, James Stevens
    Developer           : Sihle Gaxa
    JIRA                : PCGDEV-59

HISTORY
=========================================================================================
Date            JIRA no        Developer               Description
-----------------------------------------------------------------------------------------
2020-04-20      PCGDEV-59      Sihle Gaxa              Initial implementation.

ENDDESCRIPTION
--------------------------------------------------------------------------------------'''
import acm
import csv

from at_logging import getLogger
import sbl_reporting_utils as reporting_utils

LOGGER = getLogger(__name__)
FILE_HEADERS = ["isin", "sedol", "cusip", "quick", "ticker", "secDesc",
                "borrowLen", "unitQty", "contractValue", "contractCurr",
                "margin", "rate", "fee", "dividendRate", "tradeType", "tradeDate",
                "termDate", "collType", "collCurr", "cptyName", "intRefId", "settlementDate",
                "divTradeInd", "Entity 1", "Entity 2", "Entity 3", "Entity 4", "reinvestmentRate"]


class RowData(reporting_utils.ReportingData):

    def __init__(self, trade, instrument, counterparty, run_date):
        super(RowData, self).__init__(trade, instrument, counterparty, run_date)
        self.data = {}

    def get_row_details(self):
        try:
            trade_date = self.get_trade_date()
            trade_min_fee = self.get_trade_fee()
            trade_quantity = self.get_trade_quantity()
            trade_currency = self.trade.Currency().Name()
            trade_settlement_id = self.get_settlement_id()
            counterparty_type = self.get_counterparty_type()
            counterparty_code = self.get_counterparty_code()
            trade_settlement_day = self.get_settlement_date()
            underlying_instrument_isin = self.instrument.Isin()
            trade_market_value = self.get_market_value(trade_quantity)
            instrument_description = self.get_instrument_description()
            if self.instrument.InsType() == "Stock":
                trade_dividend_factor = round(self.instrument.DividendFactor() * 100)
            else:
                trade_dividend_factor = 100
            counterparty_name, counterparty_flag = self.get_counterparty_name(counterparty_type)
            LOGGER.info("{code} : exposure {exp}".format(code=counterparty_code, exp=trade_market_value))

            if (self.get_counterparty_major() in self.EXCLUDED_MAJORS or not trade_settlement_id):
                return

            self.data["rate"] = ""
            self.data["sedol"] = ""
            self.data["cusip"] = ""
            self.data["quick"] = ""
            self.data["ticker"] = ""
            self.data["margin"] = ""
            self.data["termDate"] = ""
            self.data["collCurr"] = ""
            self.data["Entity 1"] = ""
            self.data["Entity 2"] = ""
            self.data["Entity 3"] = ""
            self.data["Entity 4"] = ""
            self.data["divTradeInd"] = ""
            self.data["fee"] = trade_min_fee
            self.data["reinvestmentRate"] = ""
            self.data["tradeDate"] = trade_date
            self.data["tradeType"] = self.OP_FLAG
            self.data["unitQty"] = trade_quantity
            self.data["cptyName"] = counterparty_name
            self.data["contractCurr"] = trade_currency
            self.data["borrowLen"] = counterparty_flag
            self.data["intRefId"] = trade_settlement_id
            self.data["secDesc"] = instrument_description
            self.data["collType"] = self.COLLATERAL_TYPE
            self.data["isin"] = underlying_instrument_isin
            self.data["contractValue"] = trade_market_value
            self.data["dividendRate"] = trade_dividend_factor
            self.data["settlementDate"] = trade_settlement_day

            return self.data
        except Exception as e:
            LOGGER.info("Could not add trade row because {err}".format(err=str(e)))
            raise Exception("Could not add trade row because {error}".format(error=str(e)))


def set_trade_details(trades, file_directory, run_date):
    try:
        with open(file_directory, "wb") as csv_file:
            writer = csv.DictWriter(csv_file, FILE_HEADERS, delimiter="\t")
            writer.writeheader()
            for trade in trades[0].Trades():
                LOGGER.info("Processing trade {trade}".format(trade=trade.Oid()))
                instrument = trade.Instrument().Underlying()
                lender = trade.add_info("SL_G1Counterparty2")
                borrower = trade.add_info("SL_G1Counterparty1")
                lender_counterparty = acm.FParty[lender]
                if lender_counterparty:
                    trade_row = RowData(trade, instrument, lender_counterparty, run_date)
                    row_data = trade_row.get_row_details()
                    if row_data:
                        writer.writerow(row_data)
                borrower_counterparty = acm.FParty[borrower]
                if borrower_counterparty:
                    trade_row = RowData(trade, instrument, borrower_counterparty, run_date)
                    row_data = trade_row.get_row_details()
                    if row_data:
                        writer.writerow(row_data)
    except Exception as e:
        LOGGER.exception("Could not process trade data because {err}".format(err=str(e)))
        raise Exception("Could not process trade data because {error}".format(error=str(e)))

ael_variables = reporting_utils.get_ael_variables()


def ael_main(dictionary):
    try:
        prefix = dictionary["file_name"]
        date_time_string = acm.Time.RealTimeNow().split(".")[0].replace(" ", "-").replace(":", "-")
        output_filename = "{prefix}.{date}.absacapital.intl.txt".format(prefix=prefix, date=date_time_string)
        output_file, run_date = reporting_utils.get_directory(dictionary, output_filename, True)
        set_trade_details(dictionary["sbl_trades"], output_file, run_date)
        LOGGER.info("Completed successfully")
        LOGGER.info("Wrote secondary output to: {path}".format(path=output_file))
    except Exception as e:
        LOGGER.exception("Failed to write file because {err}".format(err=str(e)))
        raise Exception("Failed to write file because {error}".format(error=str(e)))
