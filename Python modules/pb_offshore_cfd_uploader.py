"""-----------------------------------------------------------------------------
Module to book offshore instruments and trades using a generic container
to help populate the economics. Booked for PRIME SERVICES DESK.

Current implementation books CFD's.

HISTORY
================================================================================
Date           Developer          Description
--------------------------------------------------------------------------------
2021-02-24     Marcus Ambrose     Implemented
-----------------------------------------------------------------------------"""
import os

import acm

from PS_Functions import get_pb_fund_counterparty
import pb_offshore_cfd_booker
from at_logging import getLogger
from pb_offshore_cfd_config import BROKER_PORTFOLIOS
from pb_offshore_cfd_utils import csv_dict_list, str_to_float, get_fa_date

LOGGER = getLogger(__name__)
VALID_BROKERS = ["SocGen"]


class AbstractTradeCSVProcessor(object):
    UPDATE_INSTRUMENTS = True
    # Define required column's in report
    column_account = None
    column_ins_type = None
    column_currency = None
    column_ins_exp_date = None
    column_trade_quantity = None
    column_trans_ref = None
    column_trade_date = None
    column_trade_value_date = None
    column_trade_price = None
    column_strike_price = None
    column_isin = None
    column_ins_description = None
    column_ins_sedol = None
    column_trade_status = None
    column_funding_currency = None

    INSTRUMENT_TYPE = "CFD"
    DATE_FORMAT = None
    VOID_STATUS = None
    BROKER = None
    BROKER_COUNTERPARTY = None

    def __init__(self, file_path, alias):
        self.file_path = file_path
        self.alias = alias

        self.record_data = csv_dict_list(file_path)
        self.trade_container = pb_offshore_cfd_booker.GenericContainer()
        self.portfolio = self._get_broker_portfolio()

    def process_records(self):
        for index, record in enumerate(self.record_data):
            try:
                self.populate_container(record)

                if not self.trade_container.acm_client_counterparty:
                    LOGGER.error(
                        "ERROR while processing trade row {}, no mapped counterparty found".format(
                            index
                        )
                    )
                    continue

                void_trades = record[self.column_trade_status] == self.VOID_STATUS

                builder = self.get_builder(void_trades)

                ins = builder.get_instrument()
                if not ins or self.UPDATE_INSTRUMENTS:
                    builder.create_instrument()

                builder.book_trades()
            except Exception as e:
                LOGGER.error(
                    "ERROR while processing trade row {} of file {}: {}".format(
                        str(index + 1), os.path.basename(self.file_path), str(e)
                    )
                )

    def populate_container(self, record):
        self.trade_container.ins_type = self.INSTRUMENT_TYPE
        self.trade_container.acm_currency = acm.FCurrency[record[self.column_currency]]
        self.trade_container.ins_expiry_date = get_fa_date(
            record[self.column_ins_exp_date], self.DATE_FORMAT
        )
        self.trade_container.trade_price = str_to_float(record[self.column_trade_price])
        self.trade_container.trade_opt_key = record[self.column_trans_ref]
        self.trade_container.trade_date = get_fa_date(
            record[self.column_trade_date], self.DATE_FORMAT
        )
        self.trade_container.value_date = get_fa_date(
            record[self.column_trade_value_date], self.DATE_FORMAT
        )
        self.trade_container.trade_qty = record[self.column_trade_quantity]
        self.trade_container.ins_description = record[self.column_ins_description]
        self.trade_container.acm_portf = acm.FPhysicalPortfolio[self.portfolio]
        self.trade_container.acm_extern_curr = acm.FCurrency["USD"]
        self.trade_container.ins_sedol = self._clean_text(record[self.column_ins_sedol])
        self.trade_container.isin = record[self.column_isin]
        self.trade_container.strike_price = record[self.column_strike_price]

        self.trade_container.acm_client_counterparty = self.get_pb_fund_counterparty()
        self.trade_container.acm_offshore_counterparty = self.BROKER_COUNTERPARTY
        self.trade_container.broker = self.BROKER
        self.trade_container.funding_currency = record[self.column_funding_currency]

    def get_builder(self, void_trades):
        return pb_offshore_cfd_booker.CFDObjectBuilder(
            self.trade_container, void_trades
        )

    @staticmethod
    def _clean_text(raw_ins_code):
        forbid_chars = (":", "/", ",", ".", " ")

        non_ascii = "".join(chr if ord(chr) < 128 else "" for chr in raw_ins_code)
        for ch in forbid_chars:
            non_ascii = non_ascii.replace(ch, "")
        return non_ascii

    def get_pb_fund_counterparty(self):
        return get_pb_fund_counterparty(self.alias)

    def _get_broker_portfolio(self):
        return BROKER_PORTFOLIOS["{}".format(self.BROKER)]


class SocGenTradeCSVProcessor(AbstractTradeCSVProcessor):
    column_ins_type = "Underlying Type"
    column_currency = "Underlying Currency"
    column_ins_exp_date = "Expiry Date"
    column_trade_quantity = "Quantity"
    column_trans_ref = "Trade Id (SG Reference)"
    column_trade_date = "Trade Date"
    column_trade_value_date = "Effective Date"
    column_trade_price = "Initial Underlying Price"
    column_strike_price = "Initial Underlying Price"
    column_isin = "Underlying Code"
    column_ins_description = "Underlying Name"
    column_ins_sedol = "Underlying Identifier (Ticker)"
    column_order_type = "Order Type"
    column_trade_status = "Status"
    column_funding_currency = "Funding Currency"

    BROKER = "SocGen"
    BROKER_COUNTERPARTY = "SOCIETE GENERALE"
    DATE_FORMAT = "%d-%m-%Y"
    VOID_STATUS = "CANCELLED_TRADE"
