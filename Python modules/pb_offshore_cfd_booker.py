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
from datetime import datetime

import acm

from at_logging import getLogger
from PS_Functions import get_pb_fund_shortname
from pb_offshore_cfd_config import get_exchange_rates
from pb_offshore_cfd_utils import get_fx_rate, get_fa_date


LOGGER = getLogger(__name__)


class GenericContainer(object):
    def __init__(self):
        self.acm_currency = None
        self.acm_portf = None
        self.acm_client_counterparty = None
        self.acm_offshore_counterparty = None
        self.acm_extern_curr = None
        self.acm_underlying = None
        self.ins_expiry_date = None
        self.ins_contract_size = 1
        self.trade_price = None
        self.trade_opt_key = None
        self.trade_date = None
        self.value_date = None
        self.trade_qty = None
        self.ins_description = None
        self.ins_type = None
        self.ins_sedol = None
        self.option_type = None
        self.exercise_type = None
        self.strike_price = None
        self.isin = None
        self.broker = None
        self.funding_currency = None


class AbstractObjectBuilder(object):
    ACM_CLASS = None
    INS_TYPE_ABBR = None
    UPDATE_VOIDED = False
    ACQUIRER = "PRIME SERVICES DESK"

    def __init__(self, generic_container, void_trades):
        self.void_trades = void_trades
        self.acm_currency = generic_container.acm_currency
        self.acm_portfolio = generic_container.acm_portf
        self.acm_client_counterparty = generic_container.acm_client_counterparty
        self.acm_offshore_counterparty = generic_container.acm_offshore_counterparty
        self.acm_external_currency = generic_container.acm_extern_curr
        self.acm_underlying = generic_container.acm_underlying
        self.ins_expiry_date = generic_container.ins_expiry_date
        self.ins_contract_size = generic_container.ins_contract_size
        self.ins_description = self._process_instrument_description(
            generic_container.ins_description
        )
        self.ins_type = generic_container.ins_type
        self.ins_sedol = generic_container.ins_sedol
        self.trade_price = generic_container.trade_price
        self.trade_date = generic_container.trade_date
        self.trade_value_date = generic_container.value_date
        self.trade_quantity = generic_container.trade_qty
        self.broker = generic_container.broker
        self.funding_currency = generic_container.funding_currency
        self.trade_opt_key = "{}_{}".format(
            self.broker, generic_container.trade_opt_key
        )
        self.ins_isin = "{}_{}".format("PRIME", generic_container.isin)

    def get_instrument(self):
        return self.ACM_CLASS[self._get_instrument_name()]

    def create_instrument(self):
        instrument = self.get_instrument()

        if not instrument:
            instrument = self.ACM_CLASS()
            instrument.Name(self._get_instrument_name())

        instrument.PayType("Future")
        instrument.Currency(self.acm_currency)
        instrument.ExternalId1(self._get_external_id())
        instrument.MtmFromFeed(True)
        instrument.Otc(True)
        instrument.ValuationGrpChlItem(
            acm.FChoiceList.Select('list="ValGroup" and name="EQ_NonZAR"')[0]
        )
        instrument.Quotation(acm.FQuotation["Per Unit"])
        instrument.PriceFindingChlItem(acm.FChoiceList["EQ_Deriv"])
        instrument.ExpiryDate(self.ins_expiry_date)
        instrument.ContractSize(float(self.ins_contract_size))

        if self.ins_description:
            instrument.FreeText(self.ins_description)

        if self.acm_underlying:
            instrument.Underlying(self.acm_underlying)

        self._populate_ins_isin(instrument)

        self._add_specific_instrument_details(instrument)

        instrument.Commit()
        LOGGER.info("Created new instrument {}".format(instrument.Name()))

        return instrument

    def book_trades(self):
        trades_exist = False
        offshore_trade = acm.FTrade.Select01(
            "optionalKey = {}".format(self.trade_opt_key, ""), True
        )

        if self.void_trades:
            if not offshore_trade:
                LOGGER.info("None trade to void: ex ref:{}".format(self.trade_opt_key))

            else:
                self._void_trades(offshore_trade)
            return

        if not offshore_trade:
            offshore_trade = acm.FTrade()
        elif self.UPDATE_VOIDED and offshore_trade.Status() == "Void":
            LOGGER.info(
                "Skipping Voided trades: {} & {}".format(
                    offshore_trade.Oid(), offshore_trade.ContractTrade().Oid()
                )
            )
            return
        else:
            trades_exist = True
            LOGGER.info(
                "Updating existing trades: {} & {}".format(
                    offshore_trade.Oid(), offshore_trade.ContractTrade().Oid()
                )
            )

        offshore_trade = self._book_offshore_trade(offshore_trade)
        client_trade = self._book_client_trade(offshore_trade)
        self._link_trades(offshore_trade, client_trade)

        if not trades_exist:
            LOGGER.info(
                "Trades booked: {} and {}".format(
                    offshore_trade.Oid(), client_trade.Oid()
                )
            )

    def _void_trades(self, offshore_trade):
        linked_trades = acm.FTrade.Select(
            "oid<>{} and contractTrdnbr={}".format(
                offshore_trade.Oid(), offshore_trade.Oid()
            )
        )

        offshore_trade.Status("Void")
        offshore_trade.Commit()

        for trade in linked_trades:
            trade.Status("Void")
            trade.Commit()

    def _book_offshore_trade(self, offshore_trade):
        offshore_trade.Instrument(self.get_instrument())
        offshore_trade.Price(float(self.trade_price))
        offshore_trade.Currency(self.acm_currency)
        offshore_trade.OptionalKey(self.trade_opt_key)
        offshore_trade.TradeTime(self.trade_date)
        offshore_trade.ValueDay(self.trade_value_date)
        offshore_trade.AcquireDay(self.trade_value_date)
        offshore_trade.Quantity(float(self.trade_quantity))
        offshore_trade.Counterparty(self.acm_offshore_counterparty)
        offshore_trade.Acquirer(acm.FParty[self.ACQUIRER])
        offshore_trade.Portfolio(self.acm_portfolio)
        offshore_trade.Trader(acm.User())
        offshore_trade.Status("BO Confirmed")
        offshore_trade.RegisterInStorage()

        self._add_specific_offshore_trade_details(offshore_trade)

        offshore_trade.Commit()
        return offshore_trade

    def _book_client_trade(self, offshore_trade):
        client_trade = acm.FTrade.Select01(
            "oid<>{} and contractTrdnbr={} and counterparty<>{}".format(
                offshore_trade.Oid(), offshore_trade.Oid(), "ABSA BANK LIMITED"
            ),
            "",
        )

        if not client_trade:
            client_trade = offshore_trade.Clone()

        client_trade.Instrument(offshore_trade.Instrument())
        client_trade.OptionalKey("")
        client_trade.Quantity(-offshore_trade.Quantity())
        client_trade.Price(offshore_trade.Price())
        client_trade.Counterparty(self.acm_client_counterparty)
        client_trade.Contract(offshore_trade)
        client_trade.TradeTime(offshore_trade.TradeTime())
        client_trade.ValueDay(offshore_trade.ValueDay())
        client_trade.AcquireDay(offshore_trade.AcquireDay())
        client_trade.RegisterInStorage()

        self._add_specific_client_trade_details(client_trade)

        client_trade.Commit()

        self._add_execution_fee(client_trade)

        return client_trade

    def _add_execution_fee(self, client_trade):
        ex_rate = self._get_exec_rate(self.acm_currency.Name(), self.funding_currency)

        ex_fee = abs(client_trade.Price() * client_trade.Quantity() * ex_rate)

        client_payment = acm.FPayment.Select01(
            "trade = {} and type = 'CFD Execution Fee'".format(client_trade.Name()), ""
        )
        if not client_payment:
            client_payment = acm.FPayment()

        client_payment.Amount(ex_fee)
        client_payment.Currency(client_trade.Currency())
        client_payment.Party(acm.FParty[self.ACQUIRER])
        client_payment.Type("CFD Execution Fee")
        client_payment.Trade(client_trade)
        client_payment.PayDay(client_trade.ValueDay())
        client_payment.ValidFrom(client_trade.TradeTime())
        try:
            client_payment.Commit()
        except Exception as e:
            LOGGER.error(
                "Unable to save execution fee of {} for trade {}: {}".format(
                    ex_fee, client_trade.Name(), e
                )
            )

    @staticmethod
    def _link_trades(offshore_trade, client_trade):
        offshore_trade.Contract(client_trade)
        offshore_trade.Commit()

    def _get_cfd_portfolio(self):
        party_alias = get_pb_fund_shortname(acm.FParty(self.acm_client_counterparty))

        query = acm.CreateFASQLQuery("FPhysicalPortfolio", "AND")
        query.AddAttrNode("AdditionalInfo.PS_ClientFundName", "EQUAL", party_alias)
        query.AddAttrNode("AdditionalInfo.PS_PortfolioType", "EQUAL", "CFD")
        return query.Select()[0]

    def _populate_ins_isin(self, instrument):
        isin = self.ins_isin

        if self.ins_isin:
            existing_instrument = acm.FInstrument[isin]

            if not existing_instrument or (
                existing_instrument and existing_instrument.Name() == instrument.Name()
            ):
                instrument.Isin(isin)
            else:
                LOGGER.warning(
                    "ISIN {} not set, already exists on {}".format(
                        isin, existing_instrument.Name()
                    )
                )

    @staticmethod
    def _process_instrument_description(description):
        """Max length of 63 characters in upper case"""
        return description[:63].upper()

    def _get_instrument_sedol(self):
        if self.ins_sedol:
            return self.ins_sedol.upper()

        raise RuntimeError("Instruments SEDOL code is missing.")

    def _get_external_id(self):
        return "PRIME/{0}_{1}".format(
            self._get_instrument_sedol(), self.ins_type
        ).upper()

    def _get_instrument_name(self):
        ins_sedol = self._get_instrument_sedol()
        return "{0}/{1}/PRIME/{2}".format(
            self.acm_currency.Name(), ins_sedol, self.ins_type
        )

    @staticmethod
    def _populate_trade_premium(trade):
        trade.Premium(
            trade.Quantity() * trade.Price() * trade.Instrument().ContractSize() * -1
        )

    @staticmethod
    def _get_expiry_name_format(expiry_date):
        try:
            expiry_date = expiry_date.replace("/", "").replace("-", "")
            expiry_date = datetime.strptime(expiry_date, "%Y%m%d")

            return expiry_date.strftime("%b%y")

        except Exception:
            raise Exception("Incorrect expiry date: {}".format(expiry_date))

    def _add_specific_offshore_trade_details(self, trade):
        raise NotImplementedError(
            "Function _add_specific_offshore_trade_details must be implemented in subclasses."
        )

    def _add_specific_client_trade_details(self, trade):
        raise NotImplementedError(
            "Function _add_specific_client_trade_details must be implemented in subclasses."
        )

    def _add_specific_instrument_details(self, instrument):
        raise NotImplementedError(
            "Function _add_specific_instrument_details must be implemented in subclasses."
        )

    @staticmethod
    def _get_exec_rate(underlying_curr, funding_curr):
        exchange_rates = get_exchange_rates()

        rate_by_both = exchange_rates.get((underlying_curr, funding_curr))
        rate_by_underlying_curr = exchange_rates.get(underlying_curr)
        rate_by_funding_curr = exchange_rates.get(funding_curr)

        return rate_by_both or rate_by_underlying_curr or rate_by_funding_curr or 0


class CFDObjectBuilder(AbstractObjectBuilder):
    ACM_CLASS = acm.FCfd
    INS_TYPE_ABBR = "CFD"
    CFD_UNDERLYING = "GPP_equity"
    CFD_EXPIRY = "9999-12-31"

    def __init__(self, generic_container, void_trades):
        super(CFDObjectBuilder, self).__init__(generic_container, void_trades)
        self.acm_underlying = acm.FInstrument[self.CFD_UNDERLYING]
        self.description = generic_container.ins_description
        self.ins_expiry_date = self.CFD_EXPIRY

    def _add_specific_instrument_details(self, instrument):
        instrument.FreeText(self.description)
        instrument.Underlying(self.acm_underlying)
        instrument.ValuationGrpChlItem(
            acm.FChoiceList.Select('list = "ValGroup" and name ="AC_GLOBAL"')[0]
        )

    def _add_specific_offshore_trade_details(self, trade):
        pass

    def _add_specific_client_trade_details(self, trade):
        pass
