"""-----------------------------------------------------------------------------
Date                    : 2017-03-07
Purpose                 : Upload GPP objects into FA.
Department and Desk     : Prime Services
Requester               : Eveshnee Naidoo
Developer               : Ondrej Bahounek

HISTORY
================================================================================
Date       Change no     Developer          Description
--------------------------------------------------------------------------------
2017-03-07 4372980       Ondrej Bahounek    ABITFA-4765 - GPP phase 1
2019-12-10 FAPE-168      Tibor Reiss        Update also price on client trade
-----------------------------------------------------------------------------"""

import os
import string
import datetime

import acm

from at_feed_processing import SimpleCSVFeedProcessor, notify_log
from at_ael_variables import AelVariableHandler
from at_price import set_instrument_price
from PS_Functions import get_pb_fund_counterparty
from at_logging import getLogger
import pb_gpp_general


LOGGER = getLogger(__name__)
TODAY = acm.Time().DateToday()
TRADE_DATE = ""

DEFAULT_DELIMITER = ","
DELIMITER = DEFAULT_DELIMITER

UPDATE_INSTR = False
UPDATE_VOIDED = False

FORBIDDEN_CHARS = (":", "/", ",", ".")
FORBIDDEN_CHARS_EXT = FORBIDDEN_CHARS + (" ",)

GPP_CP = pb_gpp_general.get_gpp_cp()
GPP_TRADING_PORTF = pb_gpp_general.get_trading_portf()


class MissingFileException(IOError):
    pass


class GenericContainer(object):
    def __init__(self):
        self.acm_currency = None
        self.ins_expiry_date = None
        self.ins_contract_size = 1
        self.trade_price = None
        self.trade_opt_key = None
        self.trade_date = None
        self.value_date = None
        self.trade_qty = None
        self.acm_portf = None
        self.acm_cparty = None
        self.acm_extern_curr = None
        self.acm_underlying = None
        self.ins_description = None
        self.ins_gpp_instype = None
        self.ins_ext_code = None
        self.option_type = None
        self.exercise_type = None
        self.strike_price = None
        self.eod_price = None
        self.isin = None
        self.exchange = None


class InputProperties(object):

    ERRORS = []

    @staticmethod
    def reset():
        InputProperties.ERRORS = []

    @staticmethod
    def add_error(error):
        InputProperties.ERRORS.append(error)

    @staticmethod
    def has_errors():
        return len(InputProperties.ERRORS) != 0

    @staticmethod
    def print_errors():
        for errors in InputProperties.ERRORS:
            for error in errors:
                print(error)

    @staticmethod
    def get_errors():
        return [str(err) for sub_errors in InputProperties.ERRORS for err in sub_errors]


def get_fa_date(gpp_date):
    """Get FA date
    source: 2017/11/09
    FA: 2016-04-29
    """
    if not gpp_date:
        return None
    if '-' in gpp_date:
        if len(gpp_date) == 10:
            return gpp_date
        raise ValueError("Incorrect date format: '%s'" % gpp_date)
    if '/' in gpp_date:
        if gpp_date[2] == '/':
            gpp_date = clear_date(gpp_date)
        else:
            gpp_date = gpp_date.replace('/', '')
    return gpp_date[0:4] + "-" + gpp_date[4:6] + "-" + gpp_date[6:]


def clear_date(gpp_date):
    gpp_date = gpp_date.replace('/', '')
    return gpp_date[4:] + gpp_date[2:4] + gpp_date[0:2]


def remove_chars(forbid_chars=FORBIDDEN_CHARS):
    def _rem_chars(name):
        for ch in forbid_chars:
            name = name.replace(ch, "")
        return name
    return _rem_chars


def sanitize_code(some_string, forbid_chars=FORBIDDEN_CHARS):
    non_ascii = remove_nonascii(some_string)
    for ch in forbid_chars:
        non_ascii = non_ascii.replace(ch, "")
    return non_ascii


def remove_nonascii(name):
    return ''.join(chr if ord(chr) < 128 else '' for chr in name)


def str_to_float(val):
    """Convert string to float (ignore commas from within the number."""
    try:
        return float(val)
    except ValueError:
        return float(val.replace(',', '')) if val != '' else 0


def get_expiry_name_format(expiry_date):
    """
    Expects date in format '2016-12-24'
    Returns 'DEC16'
    """
    expiry_date = expiry_date.replace("/", "").replace("-", "")
    months = {'01':'JAN', '02':'FEB', '03':'MAR', '04':'APR', '05':'MAY', '06':'JUN',
        '07':'JUL', '08':'AUG', '09':'SEP', '10':'OCT', '11':'NOV', '12':'DEC'}
    if len(expiry_date) != 8:
        raise RuntimeError("Incorrect expiry date: '%s'" % expiry_date)
    month = months[expiry_date[4:6]]
    year = expiry_date[2:4]
    return "{0}{1}".format(month, year)


class InstrumentHelper(object):

    INTERNAL_M = acm.FMTMMarket["internal"]
    SPOT_M = acm.FMarketPlace["SPOT"]
    SPOTMID_M = acm.FMarketPlace["SPOT_MID"]
    MARKETS = [
        INTERNAL_M,
        SPOT_M,
        SPOTMID_M,
        ]

    @staticmethod
    def save_ins_price(ins, market, price, for_date):
        LOGGER.info("Saving '%s' price on '%s' for '%s': %f [%s]" \
            % (market.Name(), ins.Name(), for_date, price, ins.Currency().Name()))
        set_instrument_price(ins, market, price, ins.Currency(), for_date)

    @staticmethod
    def save_prices(ins, price, eod_date):
        for market in InstrumentHelper.MARKETS:
            InstrumentHelper.save_ins_price(ins,
                                            market,
                                            price,
                                            eod_date)
        # always save today's SPOT as well
        # as there should be no live instruments
        # without today's SPOT price
        InstrumentHelper.save_ins_price(ins,
                                        InstrumentHelper.SPOT_M,
                                        price,
                                        acm.Time.DateToday())


    @staticmethod
    def process_raw_ins_code(raw_ins_code):
        code = sanitize_code(raw_ins_code)
        code = code.replace(' ', '')
        if code:
            return code
        raise RuntimeError("Unique instrument ID not present.")


class AbstractObjectBuilder(object):

    ACM_CLASS = None
    GPP_TYPE = None

    def __init__(self, generic_container):

        self.acm_curr = generic_container.acm_currency
        self.ins_expiry_date = generic_container.ins_expiry_date
        self.ins_contract_size = generic_container.ins_contract_size
        self.trade_price = generic_container.trade_price
        self.trade_opt_key = generic_container.trade_opt_key
        self.trade_date = generic_container.trade_date
        self.value_date = generic_container.value_date
        self.trade_qty = generic_container.trade_qty
        self.acm_portf = generic_container.acm_portf
        self.acm_cparty = generic_container.acm_cparty
        self.acm_extern_curr = generic_container.acm_extern_curr
        self.acm_underlying = generic_container.acm_underlying
        self.ins_description = self.process_ins_descr(generic_container.ins_description)
        self.ins_gpp_instype = generic_container.ins_gpp_instype
        self.ins_ext_code = generic_container.ins_ext_code
        self.exchange = generic_container.exchange
        self.isin = generic_container.isin

    def _fill_ins(self, ins):
        ins.PayType('Future')
        ins.Currency(self.acm_curr)
        ins.ExternalId1(self.get_external_id())
        ins.MtmFromFeed(True)
        ins.Otc(True)
        valuationGroup = acm.FChoiceList.Select("list = 'ValGroup' and name ='EQ_NonZAR'")[0]
        ins.ValuationGrpChlItem(valuationGroup)
        ins.Quotation(acm.FQuotation['Per Unit'])
        ins.PriceFindingChlItem(acm.FChoiceList['EQ_Deriv'])
        ins.ExpiryDate(self.ins_expiry_date)
        ins.ContractSize(float(self.ins_contract_size))
        if self.ins_description:
            ins.FreeText(self.ins_description)  # FreeText: 39 chars
        if self.acm_underlying:
            ins.Underlying(self.acm_underlying)
        if self.isin:
            i = acm.FInstrument[self.isin]
            if not i or (i and i.Name() == ins.Name()):
                ins.Isin(self.isin)
            else:
                LOGGER.warning("ISIN '%s' not set, already exists on '%s'",
                    self.isin, i.Name())

    def _save_ins_addinfos(self, ins):
        return

    def process_ins_descr(self, ins_descr):
        return ins_descr[:63].upper()

    def get_inscode(self):
        """
        Default inscode: bloomberg
        """
        if not self.ins_ext_code:
            raise RuntimeError("Instrument's external code is missing.")

        return self.ins_ext_code.upper()

    def get_external_id(self):
        if not self.exchange:
            raise RuntimeError("Instrument's exchange is missing.")

        ins_code = self.get_inscode()
        ext_id = "GPP/{0}/{1}_{2}".format(self.exchange, ins_code, self.ins_gpp_instype)
        return ext_id.upper()

    def construct_ins_name(self):
        raise NotImplementedError("Must be implemented in subclasses.")

    def check_instrument(self):
        ins_name = self.construct_ins_name()
        ins_code = self.get_inscode()
        ext_id = self.get_external_id()

        extern_ins = acm.FInstrument.Select('externalId1 = "%s"' % ins_code)
        if extern_ins and extern_ins[0].Name() != ins_name:
            raise ValueError(
                "ERROR: Instrument with ExternalId '%s'" % ins_code +
                " but different name '%s' " % extern_ins[0].Name() +
                "already exists. Skipping this one '%s'." % ins_name)

        ins = acm.FInstrument[ins_name]
        if ins and ins.ExternalId1() and ins.ExternalId1() != ext_id:
            raise ValueError(
                "ERROR: Instrument with the same name '%s'" % ins.Name() +
                " but different ExternalId '%s' already exists." % ins.ExternalId1() +
                " Skipping this one.")


    def get_instrument(self):
        name = self.construct_ins_name()
        ins = self.ACM_CLASS[name]
        return ins

    def create_ins(self):
        ins = self.get_instrument()
        if not ins:
            name = self.construct_ins_name()
            LOGGER.info("Creating new instrument '%s'" % name)
            ins = self.ACM_CLASS()
            ins.Name(name)
        LOGGER.info("Filling instrument: '%s'" % ins.Name())
        self._fill_ins(ins)
        #LOGGER.info("Committing instrument data...")
        ins.Commit()
        #LOGGER.info("Saving instrument addinfos...")
        self._save_ins_addinfos(ins)
        return ins

    def _prepare_gpp_trade(self):

        LOGGER.info("Booking trades.")
        # trade1 - GPP facing trade
        # #####################################
        trade1 = acm.FTrade.Select01('optionalKey = "%s"' \
            % self.trade_opt_key, "")
        if not trade1:
            trade1 = acm.FTrade()
        elif not UPDATE_VOIDED and trade1.Status() == 'Void':
            LOGGER.info("Skipping Voided trade: %d", trade1.Oid())
            return None
        else:
            LOGGER.info("Updating existing trade: %d", trade1.Oid())

        trade1.Instrument(self.get_instrument())
        trade1.Price(float(self.trade_price))
        trade1.Currency(self.acm_curr)
        trade1.OptionalKey(self.trade_opt_key)
        trade1.TradeTime(self.trade_date)
        trade1.ValueDay(self.value_date)
        trade1.AcquireDay(self.value_date)
        trade1.Quantity(float(self.trade_qty))
        trade1.Counterparty(GPP_CP)
        trade1.Acquirer(acm.FParty['PRIME SERVICES DESK'])
        trade1.Portfolio(self.acm_portf)
        trade1.Trader(acm.User())
        trade1.Status('BO Confirmed')
        trade1.RegisterInStorage()
        #trade1.AdditionalInfo().ExternalCCY(self.acm_extern_curr.Name())
        return trade1

    def _prepare_client_trade(self, gpp_trade):

        # trade2 - client facing trade
        # #####################################
        trade2 = acm.FTrade.Select01('oid <> %d and contractTrdnbr= %d' \
            % (gpp_trade.Oid(), gpp_trade.Oid()), "")
        if not trade2:
            trade2 = gpp_trade.Clone()
        trade2.Instrument(gpp_trade.Instrument())
        trade2.OptionalKey('')
        trade2.Quantity(-gpp_trade.Quantity())
        trade2.Price(gpp_trade.Price())
        trade2.Counterparty(self.acm_cparty)
        trade2.Contract(gpp_trade)
        trade2.TradeTime(gpp_trade.TradeTime())
        trade2.ValueDay(gpp_trade.ValueDay())
        trade2.AcquireDay(gpp_trade.AcquireDay())
        trade2.RegisterInStorage()
        #trade2.AdditionalInfo().ExternalCCY(self.acm_extern_curr.Name())
        return trade2

    def _fill_gpp_trade(self, trade):
        return

    def _fill_client_trade(self, trade):
        return

    def book_trades(self):

        gpp_trade = self._prepare_gpp_trade()
        if not gpp_trade:
            return

        self._fill_gpp_trade(gpp_trade)
        gpp_trade.Commit()

        client_trade = self._prepare_client_trade(gpp_trade)
        self._fill_client_trade(client_trade)
        client_trade.Commit()

        gpp_trade.Contract(client_trade)
        gpp_trade.Commit()

        LOGGER.info("Trades: %d, %d", gpp_trade.Oid(), client_trade.Oid())

    def _fill_trade_premium(self, trade):
        trade.Premium(trade.Quantity() * trade.Price() * trade.Instrument().ContractSize() * -1)


class Future(AbstractObjectBuilder):

    ACM_CLASS = acm.FFuture
    GPP_TYPE = pb_gpp_general.GPP_FUT_TYPE


    def __init__(self, generic_container):
        super(Future, self).__init__(generic_container)
        self.acm_underlying = generic_container.acm_underlying

    def _fill_ins(self, ins):
        super(Future, self)._fill_ins(ins)
        ins.Underlying(self.acm_underlying)

    def construct_ins_name(self):
        ins_code = self.get_inscode()
        expiry = get_expiry_name_format(self.ins_expiry_date)
        name = "{0}/GPP/{1}/{2}/{3}".format(
            self.acm_curr.Name(),
            pb_gpp_general.get_fa_instype_alias(self.GPP_TYPE),
            ins_code,
            expiry)

        return name


class Option(AbstractObjectBuilder):

    ACM_CLASS = acm.FOption
    GPP_TYPE = pb_gpp_general.GPP_OPT_TYPE


    def __init__(self, generic_container):
        super(Option, self).__init__(generic_container)

        self.acm_underlying = generic_container.acm_underlying
        self.option_type = self._get_option_type_fa(generic_container.option_type)
        self.exercise_type = "European"
        self.strike_price = float(generic_container.strike_price)

    def _get_option_type_fa(self, gpp_option_type):
        if "P" == gpp_option_type:
            return "Put"
        if "C" == gpp_option_type:
            return "Call"
        raise ValueError("Option type '%s' not recognised" % gpp_option_type)

    def construct_ins_name(self):
        ins_code = self.get_inscode()
        expiry = get_expiry_name_format(self.ins_expiry_date)
        call_put = "C" if self.option_type == "Call" else "P"

        name = "{0}/GPP/{1}/{2}/{3}/{4}".format(
            self.acm_curr.Name(),
            pb_gpp_general.get_fa_instype_alias(self.GPP_TYPE),
            ins_code,
            call_put,
            self.strike_price,
            expiry)

        return name

    def _fill_ins(self, ins):
        super(Option, self)._fill_ins(ins)
        ins.Underlying(self.acm_underlying)
        ins.OptionType(self.option_type)
        ins.ExerciseType(self.exercise_type)
        ins.StrikePrice(self.strike_price)
        ins.PayType("Spot")

    def _fill_gpp_trade(self, trade):
        self._fill_trade_premium(trade)

    def _fill_client_trade(self, trade):
        self._fill_trade_premium(trade)


class Stock(AbstractObjectBuilder):

    ACM_CLASS = acm.FStock
    GPP_TYPE = pb_gpp_general.GPP_STO_TYPE

    def __init__(self, generic_container):
        super(Stock, self).__init__(generic_container)
        self.isin = generic_container.isin + "_EQ"

    def _fill_ins(self, ins):
        super(Stock, self)._fill_ins(ins)
        ins.PayType("Spot")
        #ins.Isin(self.isin)

    def construct_ins_name(self):
        ins_code = self.get_inscode()
        name = "{0}/GPP/{1}/{2}".format(
            self.acm_curr.Name(),
            pb_gpp_general.get_fa_instype_alias(self.GPP_TYPE),
            ins_code)
        return name

    def _fill_gpp_trade(self, trade):
        self._fill_trade_premium(trade)

    def _fill_client_trade(self, trade):
        self._fill_trade_premium(trade)


class CFD(AbstractObjectBuilder):

    ACM_CLASS = acm.FCfd
    GPP_TYPE = pb_gpp_general.GPP_CFD_TYPE

    def __init__(self, generic_container):
        super(CFD, self).__init__(generic_container)
        self.acm_underlying = acm.FInstrument["GPP_equity"]
        self.description = generic_container.ins_description
        self.isin = generic_container.isin + "_SWAP"
        self.ins_expiry_date = "9999-12-31"

    def _fill_ins(self, ins):
        super(CFD, self)._fill_ins(ins)
        #ins.Isin(self.isincode)
        ins.FreeText(self.description)
        ins.Underlying(self.acm_underlying)
        valuationGroup = acm.FChoiceList.Select("list = 'ValGroup' and name ='AC_GLOBAL'")[0]
        ins.ValuationGrpChlItem(valuationGroup)

    def construct_ins_name(self):
        ins_code = self.get_inscode()
        name = "{0}/GPP/{1}/{2}".format(
            self.acm_curr.Name(),
            pb_gpp_general.get_fa_instype_alias(self.GPP_TYPE),
            ins_code)

        return name


class TradeActivityCSV(SimpleCSVFeedProcessor):

    FILE_INDEX = "trade_activity_file_name"
    LOAD_THIS_INDEX = "load_trade_activity"

    col_account_name = "AccountName"
    col_ins_type = "ProductType"
    col_security_type = "SecurityType"
    col_ins_contrsize = "Multiplier"
    col_ins_code_isin = "ISIN"
    col_ins_code_bloom = "Bloomberg"
    col_ins_code_sedol = "Sedol"
    col_exchange = "Exchange"
    col_currency = "TradeCCY"
    col_ins_exp_date = "ExpiryDate"
    col_trd_qty = "Quantity"
    col_trd_nbr = "TransactionRef"
    col_trd_date = "TradeDate"
    col_trd_val_date = "SettleDate"
    col_trd_price = "GrossTradePrice"
    col_eod_date = "BusinessDate"
    col_description = "SecurityDesc"
    col_trans_ref = "TransactionRef"
    col_trade_action = "TradeAction"
    col_put_call = "PutCall"
    col_strike = "StrikePrice"

    _required_columns = [col_account_name, col_ins_type, col_security_type, col_ins_contrsize,
        col_ins_code_isin, col_ins_code_bloom, col_ins_code_sedol, col_currency,
        col_ins_exp_date, col_trd_qty, col_trd_nbr, col_trd_date,
        col_trd_val_date, col_trd_price, col_description, col_exchange,
        col_trans_ref, col_trade_action, col_put_call, col_strike]

    VALID_TRADE_ACTIONS = ("NEW", "NEW/AMEND", "UNWIND", "CORRECTED", "EXPIRED")

    # ins types that have underlyings
    UNDERLYING_TYPES = (pb_gpp_general.GPP_FUT_TYPE,
                        pb_gpp_general.GPP_OPT_TYPE)

    def __init__(self, file_path):
        super(TradeActivityCSV, self).__init__(file_path)
        self._dict_reader_kwargs = {'delimiter':DELIMITER}

    def _get_underlying(self, product_type, bloom_code):
        if product_type not in self.UNDERLYING_TYPES:
            return None
        und_ins_name = pb_gpp_general.get_underlying(bloom_code)
        if not und_ins_name:
            raise RuntimeError("Product type '%s' with code '%s' not recognised. "
                               "Please update Instrument file." % (product_type, bloom_code))
        instr = acm.FInstrument[und_ins_name]
        if not instr:
            raise RuntimeError("Can't map product type '%s' (code: '%s') to any existing "
                               "underlying instrument" % (product_type, bloom_code))
        return instr

    def _process_record(self, record, dry_run):
        LOGGER.info("%s processing %s", "-" * 16, self.__class__.__name__)
        (_index, record_data) = record

        try:
            trd_action = record_data[self.col_trade_action]
            if trd_action.upper() not in self.VALID_TRADE_ACTIONS:
                LOGGER.info("Skipping invalid %s: '%s'", self.col_trade_action,
                                                          trd_action)
                return
            acnt_name = record_data[self.col_account_name]
            alias = pb_gpp_general.get_account_alias(acnt_name)
            if not alias:
                LOGGER.info("Skipping account '%s' (alias not recognised)...",
                    acnt_name)
                return

            gpp_type = record_data[self.col_ins_type]
            if not pb_gpp_general.is_valid_gpp_instype(gpp_type):
                LOGGER.warning("Invalid GPP instype: '%s'", gpp_type)
                return

            trade_date = get_fa_date(record_data[self.col_trd_date])
            if TRADE_DATE and trade_date != TRADE_DATE:
                LOGGER.warning("Skipping trade with trade date '%s'", trade_date)
                return

            bloom_code = sanitize_code(record_data[self.col_ins_code_bloom])
            underlying = self._get_underlying(gpp_type, bloom_code)

            container = GenericContainer()

            container.ins_gpp_instype = gpp_type
            container.acm_underlying = underlying
            container.acm_currency = acm.FCurrency[record_data[self.col_currency]]
            container.ins_expiry_date = get_fa_date(record_data[self.col_ins_exp_date])
            container.ins_contract_size = record_data[self.col_ins_contrsize]

            container.trade_price = str_to_float(record_data[self.col_trd_price])
            container.trade_opt_key = record_data[self.col_trans_ref]

            container.trade_date = trade_date
            container.value_date = get_fa_date(record_data[self.col_trd_val_date])

            container.trade_qty = record_data[self.col_trd_qty]
            container.acm_portf = pb_gpp_general.get_trading_portf()
            container.acm_cparty = get_pb_fund_counterparty(alias)
            container.acm_extern_curr = acm.FCurrency["USD"]
            container.ins_description = remove_nonascii(record_data[self.col_description])
            container.ins_ext_code = InstrumentHelper.process_raw_ins_code(record_data[self.col_ins_code_bloom])
            container.exchange = remove_nonascii(record_data[self.col_exchange])
            container.isin = record_data[self.col_ins_code_isin]
            container.option_type = record_data[self.col_put_call]
            container.strike_price = record_data[self.col_strike]

            builder = None
            if gpp_type == pb_gpp_general.GPP_FUT_TYPE:
                builder = Future(container)
            elif gpp_type == pb_gpp_general.GPP_STO_TYPE:
                builder = Stock(container)
            elif gpp_type == pb_gpp_general.GPP_OPT_TYPE:
                builder = Option(container)
            elif gpp_type == pb_gpp_general.GPP_CFD_TYPE:
                builder = CFD(container)

            if not builder:
                raise RuntimeError("GPP Instrument type '%s' not recognised." % gpp_type)

            builder.check_instrument()

            ins = builder.get_instrument()
            if not ins or UPDATE_INSTR:
                ins = builder.create_ins()

            builder.book_trades()


        except Exception as exc:
            LOGGER.exception(exc)
            raise self.RecordProcessingException(
                "ERROR while processing row #%d of file '%s': %s" \
                    % (_index, os.path.basename(self._file_path), str(exc)))
# end of TradeActivity file processor


class PositionsCSV(SimpleCSVFeedProcessor):

    FILE_INDEX = "positions_file_name"
    LOAD_THIS_INDEX = "load_positions"

    col_report_date = "\xef\xbb\xbfTradeDate"
    col_report_date2 = "TradeDate"
    col_account_name = "AccountName"
    col_ins_type = "ProductDescription"
    col_ins_code_isin = "ISIN"
    col_ins_code_bloom = "Bloomberg"
    col_ins_code_sedol = "Sedol"
    col_exchange = "Exchange"
    col_currency = "Currency"
    col_eod_price = "ClosingPrice"
    col_ins_exp_date = "ExpiryDate"
    col_put_call = "PutCall"
    col_strike = "StrikePrice"
    col_description = "SecurityDesc"

    _required_columns = [col_report_date, col_account_name, col_ins_type,
        col_ins_code_isin, col_ins_code_bloom, col_ins_code_sedol,
        col_currency, col_eod_price, col_description, col_exchange,
        col_ins_exp_date, col_put_call, col_strike]

    def __init__(self, file_path):
        super(PositionsCSV, self).__init__(file_path)

    def _process_record(self, record, dry_run):
        LOGGER.info("%s processing %s", "-" * 16, self.__class__.__name__)
        (_index, record_data) = record

        try:
            alias = pb_gpp_general.get_account_alias(record_data[self.col_account_name])
            if not alias:
                LOGGER.info("Skipping account '%s' (alias not recognised)...",
                    record_data[self.col_account_name])
                return

            gpp_type = record_data[self.col_ins_type]

            container = GenericContainer()

            container.ins_gpp_instype = gpp_type
            container.acm_currency = acm.FCurrency[record_data[self.col_currency]]
            container.ins_expiry_date = get_fa_date(record_data[self.col_ins_exp_date])
            container.ins_ext_code = InstrumentHelper.process_raw_ins_code(record_data[self.col_ins_code_bloom])
            container.option_type = record_data[self.col_put_call]
            container.strike_price = record_data[self.col_strike]
            container.ins_description = remove_nonascii(record_data[self.col_description])
            container.exchange = remove_nonascii(record_data[self.col_exchange])
            container.isin = record_data[self.col_ins_code_isin]

            builder = None
            if gpp_type == pb_gpp_general.GPP_FUT_TYPE:
                builder = Future(container)
            elif gpp_type == pb_gpp_general.GPP_STO_TYPE:
                builder = Stock(container)
            elif gpp_type == pb_gpp_general.GPP_OPT_TYPE:
                builder = Option(container)
            elif gpp_type == pb_gpp_general.GPP_CFD_TYPE:
                builder = CFD(container)

            if not builder:
                raise RuntimeError("GPP Instrument type '%s' not recognised." % gpp_type)

            builder.check_instrument()
            ins = builder.get_instrument()
            if not ins:
                raise RuntimeError("%s instrument '%s' not found: '%s'"
                    % (gpp_type, container.ins_ext_code, builder.construct_ins_name()))


            eod_price = str_to_float(record_data[self.col_eod_price])
            eod_date = get_fa_date(record_data[self.col_report_date])
            InstrumentHelper.save_prices(ins, eod_price, eod_date)

        except Exception as exc:
            LOGGER.exception(exc)
            raise self.RecordProcessingException(
                "ERROR while processing row #%d of file '%s': %s" \
                    % (_index, os.path.basename(self._file_path), str(exc)))


class MarginCSV(SimpleCSVFeedProcessor):

    col_account_name = "AccountName"
    col_currency = "Currency"
    col_margin = "TotalMarginReq"

    _required_columns = [col_account_name, col_currency, col_margin]

    def __init__(self, file_path):
        super(MarginCSV, self).__init__(file_path, do_logging=False)
        self._dict_reader_kwargs = {'delimiter':DEFAULT_DELIMITER}
        self.accounts_dict = defaultdict(defaultdict)

    def _process_record(self, record, dry_run):
        (_, record_data) = record

        alias = get_account_alias(record_data[self.col_account_name])
        if not alias:
            return
        curr = record_data[self.col_currency]
        margin = str_to_float(record_data[self.col_margin])
        self.accounts_dict[alias][curr] = margin

        LOGGER.info("%s margin: %f [%s]", alias, margin, curr)

    def get_fund_curr_margin_dict(self):
        return self.accounts_dict

    @staticmethod
    def get_margins_from_file(accounts_file_path):
        margin_proc = MarginCSV(accounts_file_path)
        margin_proc.add_error_notifier(notify_log)
        margin_proc.process(False)
        fund_dict = margin_proc.get_fund_curr_margin_dict()
        return fund_dict


def enable_custom_start_date(selected_variable):
    cust = ael_variables.get("custom_date")
    cust.enabled = (selected_variable.value == 'Custom Date')


def hook_trade_activity(selected_variable):
    vars = (TradeActivityCSV.FILE_INDEX, "trade_date")
    for variable in vars:
        cust = ael_variables.get(variable)
        cust.enabled = selected_variable.value


def hook_positions(selected_variable):
    vars = (PositionsCSV.FILE_INDEX, )
    for variable in vars:
        cust = ael_variables.get(variable)
        cust.enabled = selected_variable.value


ael_variables = AelVariableHandler()
ael_variables.add("date",
                  label="Date",
                  cls="string",
                  default="PrevNonWeekendDay",
                  collection=pb_gpp_general.DATE_KEYS,
                  hook=enable_custom_start_date,
                  mandatory=True,
                  alt=("A date for which files will be taken."))
ael_variables.add("custom_date",
                  label="Custom Date",
                  cls="string",
                  default=TODAY,
                  enabled=False,
                  alt=("Format: '2016-09-30'."))
ael_variables.add("file_dir",
                  label="Directory",
                  default=r"c:\DEV\Perforce\bahouneo\GPP\Input\testing\${DATE}",
                  alt=("A Directory template with all input files. "
                       "It can contain the variable DATE (\"$DATE\") "
                       "which will be replaced by the today's date (format YYYY-MM-DD)"))
ael_variables.add(TradeActivityCSV.FILE_INDEX,
                  label="Trade Activity filename",
                  default="TradeActivity_${DATE}.csv",
                  alt=("A path template to the trades executed input file. "
                       "It can contain the variable DATE (\"$DATE\") "
                       "which will be replaced by the today's date (format YYYYMMDD)"))
ael_variables.add(PositionsCSV.FILE_INDEX,
                  label="Positions filename",
                  default="Positions_${DATE}.csv",
                  alt=("A path template to the positions input file "
                       "which is used for instruments prices. "
                       "It can contain the variable DATE (\"$DATE\") "
                       "which will be replaced by the today's date (format YYYYMMDD)"))


ael_variables.add(TradeActivityCSV.LOAD_THIS_INDEX,
                  label="Load Trade Activity File?",
                  cls="bool",
                  collection=(True, False),
                  default=False,
                  hook=hook_trade_activity)
ael_variables.add(PositionsCSV.LOAD_THIS_INDEX,
                  label="Load Prices from Positions File?",
                  cls="bool",
                  collection=(True, False),
                  default=False,
                  hook=hook_positions)
ael_variables.add("trade_date",
                  label="Trade Date",
                  cls="date",
                  default="",
                  mandatory=False,
                  alt=("If set, this date will be used during "
                       "processing TradeActivity file. "
                       "Only trades with this date will be read. "
                       "Format: '2016-09-30'"))

# ##################################
# SETTINGS TAB
ael_variables.add("csv_delimiter",
                  label="CSV Delimiter (default=;)_Settings",
                  cls="string",
                  default=DEFAULT_DELIMITER,
                  mandatory=False,
                  alt=("A delimiter character used in input csv file. "
                    "Comma (',') will be used as default if field is left empty."))
ael_variables.add("update_instr",
                  label="Update instruments?_Settings",
                  default=False,
                  cls="bool",
                  collection=(True, False),
                  alt="Update instruments during the run? "
                      "Only applicable for TradeActivity runs.")
ael_variables.add("update_voided",
                  label="Update voided?_Settings",
                  default=False,
                  cls="bool",
                  collection=(True, False),
                  alt="Update and reinstate voided trades? "
                      "Only applicable for TradeActivity runs.")

pb_gpp_general.add_common_aelvars(ael_variables)


def get_input_date(ael_dict):
    # date in string
    if ael_dict['date'] == 'Custom Date':
        the_date = ael_dict['custom_date']
    else:
        the_date = pb_gpp_general.DATE_LIST[ael_dict['date']]
    return the_date


def get_file_path(ael_dict, file_class):

    the_date = get_input_date(ael_dict)

    # file date will be converted to "dd-mm-YYYY"
    # directory date will be converted to "YYYY-mm-dd"
    _dt = datetime.datetime.strptime(the_date, "%Y-%m-%d")
    file_date_string = _dt.strftime("%Y%m%d")
    dir_date_string = the_date

    # directory in string
    file_dir = ael_dict["file_dir"]
    fdir_template = string.Template(file_dir)
    file_dir = fdir_template.substitute(DATE=dir_date_string)
    # filename in string
    file_name = ael_dict[file_class.FILE_INDEX]
    fname_template = string.Template(file_name)
    file_name = fname_template.substitute(DATE=file_date_string)

    return os.path.join(file_dir, file_name)


def get_file_object(ael_dict, csv_class):
    if ael_dict[csv_class.LOAD_THIS_INDEX]:
        file_path = get_file_path(ael_dict, csv_class)
        if not os.path.exists(file_path):
            raise MissingFileException(file_path)
        else:
            LOGGER.info("Loading file: '%s'" % file_path)
            return file_path


def ael_main(ael_dict):

    pb_gpp_general.set_general_input(ael_dict)

    dry_run = False
    InputProperties.reset()
    LOGGER.msg_tracker.reset()

    for_date = get_input_date(ael_dict)
    LOGGER.info("Uploading for date: '%s'" % for_date)

    global TRADE_DATE
    if ael_dict['trade_date']:
        TRADE_DATE = ael_dict['trade_date'].to_string("%Y-%m-%d")
        LOGGER.info("Acceptting just trades with TradeDate: '%s'" % TRADE_DATE)
    else:
        TRADE_DATE = None

    global DELIMITER
    DELIMITER = DEFAULT_DELIMITER
    if ael_dict['csv_delimiter']:
        DELIMITER = ael_dict['csv_delimiter']

    global UPDATE_INSTR
    UPDATE_INSTR = ael_dict["update_instr"]

    global UPDATE_VOIDED
    UPDATE_VOIDED = ael_dict["update_voided"]

    file_path_ta = get_file_object(ael_dict, TradeActivityCSV)
    if file_path_ta:
        processor = TradeActivityCSV(file_path_ta)
        processor.add_error_notifier(notify_log)
        processor.add_error_notifier(InputProperties.add_error)
        processor.process(dry_run)

    file_path_pos = get_file_object(ael_dict, PositionsCSV)
    if file_path_pos:
        processor = PositionsCSV(file_path_pos)
        processor.add_error_notifier(notify_log)
        processor.add_error_notifier(InputProperties.add_error)
        processor.process(dry_run)

    if InputProperties.has_errors() or LOGGER.msg_tracker.errors_counter:
        msg = "Errors occurred. Please check the log."
        LOGGER.error(msg)
        raise RuntimeError(msg)

    if LOGGER.msg_tracker.warnings_counter:
        LOGGER.warning("Completed with some warnings.")
    else:
        LOGGER.info("Completed successfully.")
