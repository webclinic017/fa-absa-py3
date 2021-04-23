"""
Date                    : 2016-05-31
Purpose                 : Upload Saxo objects into FA.
Department and Desk     : Prime Service
Requester               : Eveshnee Naidoo
Developer               : Ondrej Bahounek

Date            CR              Developer               Change
==========      =========       ======================  ========================================================
2017-01-26      4150840         Ondrej Bahounek         ABITFA-4592 - add STO, FX, FXO instruments
"""

import acm
from at_feed_processing import SimpleCSVFeedProcessor, notify_log
from at_ael_variables import AelVariableHandler
from at_price import set_instrument_price
from PS_Functions import get_pb_fund_counterparty
import FRunScriptGUI
from at_logging import getLogger

import os, sys, string, datetime
import xlrd
from collections import defaultdict
import traceback

from PB_Saxo_general import (
                             SAXO_COUNTERPARTY,
                             get_fund_portf,
                             send_mail,
                             get_account_alias,
                             INT_FUTURES_NAME,
                             INT_CFD_NAME,
                             INT_ETO_NAME,
                             INT_FX_OPTION_NAME,
                             INT_SHARES_NAME,
                             SAXO_FUT_TYPE,
                             SAXO_CFD_TYPE,
                             SAXO_ETO_TYPE,
                             SAXO_FXO_TYPE,
                             SAXO_STO_TYPE,
                             SAXO_FX_TYPE,
                             get_saxo_instype_alias,
                             DATE_LIST,
                             DATE_KEYS,
                             get_backend_date
                             )

LOGGER = getLogger(__name__)

TRADE_DATE = ""
TODAY = acm.Time().DateToday()

DEFAULT_DELIMITER = ","
DELIMITER = DEFAULT_DELIMITER
SET_TODAY_SPOT = True

UPDATE_INSTR = False

FORBIDDEN_CHARS = (":", "/", ",", ".")


class MissingFileException(IOError):
    pass


def save_ins_price(ins, market, price, curr, for_date):
    LOGGER.info("Saving %s price on '%s' for '%s': %f [%s]",
        market.Name(), ins.Name(), for_date, price, curr.Name())
    set_instrument_price(ins, market, price, curr, for_date)


def enable_custom_start_date(selected_variable):
    cust = ael_variables.get("custom_date")
    cust.enabled = (selected_variable.value == 'Custom Date')


def sanitize_code(ins_code):
    return remove_chars()(ins_code).upper()


def remove_nonascii(name):
    return ''.join(chr if ord(chr) < 128 else '' for chr in name)


def get_expiry_name_format(expiry_date):
    months = {'01':'JAN', '02':'FEB', '03':'MAR', '04':'APR', '05':'MAY', '06':'JUN',
        '07':'JUL', '08':'AUG', '09':'SEP', '10':'OCT', '11':'NOV', '12':'DEC'}
    if len(expiry_date) != 8:
        raise RuntimeError("Incorrect expiry date: '%s'" % expiry_date)
    month = months[expiry_date[4:6]]
    year = expiry_date[2:4]
    return "{0}{1}".format(month, year)


def get_ins_name(ins_type, ins_code, ins_curr, **kwargs):

    # USD/INTFUT/SAXO/FEIZ7/DEC17
    if ins_type == SAXO_FUT_TYPE:
        expiry = get_expiry_name_format(kwargs["expiry_date"])
        name = "{0}/{1}/SAXO/{2}/{3}".format(ins_curr, INT_FUTURES_NAME, ins_code, expiry)

    elif ins_type == SAXO_CFD_TYPE:
        name = "{0}/{1}/SAXO/{2}".format(ins_curr, INT_CFD_NAME, ins_code)

    elif ins_type == SAXO_ETO_TYPE:
        expiry = get_expiry_name_format(kwargs["expiry_date"])
        callput = kwargs["callput"].upper()
        if "PUT" in callput:
            callput = "P"
        else:
            callput = "C"
        name = "{0}/{1}/SAXO/{2}/{3}/{4}".format(ins_curr,
                                                 INT_ETO_NAME,
                                                 ins_code,
                                                 callput,
                                                 expiry)

    elif ins_type == SAXO_STO_TYPE:
        name = "{0}/{1}/SAXO/{2}".format(ins_curr, INT_SHARES_NAME, ins_code)

    elif ins_type == SAXO_FXO_TYPE:
        expiry = get_expiry_name_format(kwargs["expiry_date"])
        strike = float(kwargs["strike"])
        name = "{0}/{1}/SAXO/{2}/{3}/{4}".format(ins_curr,
                                             INT_FX_OPTION_NAME,
                                             ins_code,
                                             expiry,
                                             strike)

    else:
        raise RuntimeError("Unrecognizable Saxo instype: '%s'" % ins_type)

    return name


def get_fa_date(saxo_date):
    """Get FA date from SAXO date
    SAXO: 20160429
    FA: 2016-04-29
    """
    if '/' in saxo_date:
        saxo_date = clear_saxo_date(saxo_date)
    return saxo_date[0:4] + "-" + saxo_date[4:6] + "-" + saxo_date[6:]


def clear_saxo_date(saxo_date):
    saxo_date = saxo_date.replace('/', '')
    return saxo_date[4:] + saxo_date[2:4] + saxo_date[0:2]


def do_nothing():
    return lambda x: x


def remove_chars(forbid_chars=FORBIDDEN_CHARS):
    def _rem_chars(name):
        for ch in forbid_chars:
            name = name.replace(ch, "")
        return name
    return _rem_chars


class AssetClass(object):

    def __init__(self, underlying_ins, sheet_indices):
        self._underlying = underlying_ins
        self._sheet_indices = sheet_indices
        self._instr_mapping = None

    @property
    def instruments(self):
        return self._instr_mapping

    @instruments.setter
    def instruments(self, value):
        self._instr_mapping = value

    @property
    def underlying(self):
        return self._underlying

    @property
    def sheet_indices(self):
        return self._sheet_indices

    def has_instrument(self, inscode):
        return inscode in self.instruments


class InstrumentList(object):

    # sheets' indices in the Instrument List file
    SHEETS_EQUITY = ['1', '2']
    SHEETS_COMMODITY = ['4']
    SHEETS_EQUITYINDEX = ['3']


    def __init__(self, wb_file_path, asset_classes, default_underlying="Saxo_equity"):
        self.wb = xlrd.open_workbook(wb_file_path)
        self.default_underlying = default_underlying
        self.asset_classes = asset_classes
        for asset_cls in self.asset_classes:
            asset_cls.instruments = self.values_from_sheets(asset_cls.sheet_indices)

    @staticmethod
    def get_values_from_column(sheet, column=0, from_row=1,
        sanitize_func=sanitize_code):
        LOGGER.info("Reading sheet: '%s' (%d), column: '%d', from row: '%d'",
            str(sheet.name), sheet.number, column, from_row)
        return set([sanitize_func(str(val)) for val in sheet.col_values(column, from_row)])

    def values_from_sheets(self, sheet_indices_lst):
        values = set()
        for sheet_idx in sheet_indices_lst:
            sheet = self.wb.sheet_by_index(sheet_idx)
            values.update(InstrumentList.get_values_from_column(sheet))
        return values


class SectorList(object):

    SECTOR_SHEET_NAME = "Sectors"


    @staticmethod
    def read_sectors(wb_file_path, sheet_name):
        wb = xlrd.open_workbook(wb_file_path)
        sheet = wb.sheet_by_name(sheet_name)
        sector_dict = {}
        for row_index in range(1, sheet.nrows):
            key_sector = str(sheet.cell(row_index, 0).value)
            val = str(sheet.cell(row_index, 1).value)
            if val and len(val) > 0:
                sector_dict[key_sector] = val

        return sector_dict


class InputProperties(object):

    ERRORS = []
    WARNINGS = []

    @staticmethod
    def reset():
        InputProperties.ERRORS = []
        InputProperties.WARNINGS = []

    @staticmethod
    def add_error(error):
        InputProperties.ERRORS.append(error)

    @staticmethod
    def add_warning(warning):
        InputProperties.WARNINGS.append(warning)

    @staticmethod
    def has_errors():
        return len(InputProperties.ERRORS) != 0

    @staticmethod
    def has_warnings():
        return len(InputProperties.WARNINGS) != 0

    @staticmethod
    def get_errors():
        return [str(err) for sub_errors in InputProperties.ERRORS for err in sub_errors]


class AbstractObjectBuilder(object):

    ACM_CLASS = None

    def __init__(self, ins_name, acm_curr, ins_external_id,
        ins_expiry_date, ins_contract_size, trade_price,
        trade_opt_key, trade_date, value_date, trade_qty, acm_portf,
        acm_cparty, acm_extern_curr, ins_saxo_type):

        self.ins_name = ins_name
        self.acm_curr = acm_curr
        self.ins_external_id = ins_external_id
        self.ins_saxo_type = ins_saxo_type
        self.ins_expiry_date = ins_expiry_date
        self.ins_contract_size = float(ins_contract_size)

        self.trade_price = float(trade_price)
        self.trade_opt_key = trade_opt_key
        self.trade_date = trade_date
        if value_date < trade_date:
            LOGGER.warning("Value Date '%s' is prior Trade Date '%s'. "
                "Moving Value Date to '%s'", value_date, trade_date, trade_date)
            value_date = trade_date
        self.value_date = value_date
        self.trade_qty = float(trade_qty)
        self.acm_portf = acm_portf
        self.acm_cparty = acm_cparty
        self.acm_extern_curr = acm_extern_curr

    @staticmethod
    def get_external_id(ins_saxo_type, ins_external_id):
        return "SAXO/{0}/{1}".format(get_saxo_instype_alias(ins_saxo_type),
                                     ins_external_id)

    def _fill_ins(self, ins):
        ins.Name(self.ins_name)
        ins.PayType('Future')
        ins.Currency(self.acm_curr)
        ins.ExternalId1(self.ins_external_id)
        ins.MtmFromFeed(True)
        ins.Otc(True)
        valuationGroup = acm.FChoiceList.Select("list = 'ValGroup' and name ='EQ_NonZAR'")[0]
        ins.ValuationGrpChlItem(valuationGroup)
        ins.Quotation(acm.FQuotation['Per Unit'])
        ins.PriceFindingChlItem(acm.FChoiceList['EQ_Deriv'])
        ins.ExpiryDate(self.ins_expiry_date)
        ins.ContractSize(self.ins_contract_size)

    def update_ins(self, instrument):
        LOGGER.info("Updating instrument '%s'...", instrument.Name())
        self._fill_ins(instrument)
        instrument.Commit()
        return instrument

    def create_ins(self):
        LOGGER.info("Creating new %s (%s) instrument: '%s'", self.ACM_CLASS,
            self.ins_saxo_type, self.ins_name)
        ins = self.ACM_CLASS()
        self._fill_ins(ins)
        ins.Commit()
        self.save_add_infos(ins)
        return ins

    def _prepare_saxo_trade(self):

        LOGGER.info("Booking trades...")

        # trade1 - SAXO facing trade
        # #####################################
        trade1 = acm.FTrade.Select01('optionalKey = "%s"' \
            % self.trade_opt_key, "")
        if not trade1:
            trade1 = acm.FTrade()
        else:
            LOGGER.warning("Updating existing trade: '%d'", trade1.Oid())

        trade1.Instrument(acm.FInstrument[self.ins_name])
        trade1.Price(self.trade_price)
        trade1.Currency(self.acm_curr)
        trade1.OptionalKey(self.trade_opt_key)
        trade1.TradeTime(self.trade_date)
        trade1.ValueDay(self.value_date)
        trade1.AcquireDay(self.value_date)
        trade1.Quantity(float(self.trade_qty))
        trade1.Counterparty(acm.FParty[SAXO_COUNTERPARTY])
        trade1.Acquirer(acm.FParty['PRIME SERVICES DESK'])
        trade1.Portfolio(self.acm_portf)
        trade1.Trader(acm.User())
        trade1.Status('BO Confirmed')
        trade1.RegisterInStorage()
        trade1.AdditionalInfo().ExternalCCY(self.acm_extern_curr.Name())
        return trade1

    def _prepare_client_trade(self, saxo_trade):

        # trade2 - client facing trade
        # #####################################
        trade2 = acm.FTrade.Select01('oid <> %d and contractTrdnbr= %d' \
            % (saxo_trade.Oid(), saxo_trade.Oid()), "")
        if not trade2:
            trade2 = saxo_trade.Clone()
        else:
            LOGGER.warning("Updating existing trade: '%d'", trade2.Oid())
        trade2.OptionalKey('')
        trade2.Quantity(-saxo_trade.Quantity())
        trade2.Counterparty(self.acm_cparty)
        trade2.Contract(saxo_trade)
        trade2.TradeTime(saxo_trade.TradeTime())
        trade2.ValueDay(saxo_trade.ValueDay())
        trade2.AcquireDay(saxo_trade.AcquireDay())
        trade2.RegisterInStorage()
        trade2.AdditionalInfo().ExternalCCY(self.acm_extern_curr.Name())
        return trade2

    def _fill_saxo_trade(self, trade):
        return

    def _fill_client_trade(self, trade):
        return

    def book_trades(self):

        saxo_trade = self._prepare_saxo_trade()
        self._fill_saxo_trade(saxo_trade)
        saxo_trade.Commit()

        client_trade = self._prepare_client_trade(saxo_trade)
        self._fill_client_trade(client_trade)
        client_trade.Commit()

        saxo_trade.Contract(client_trade)
        saxo_trade.Commit()

        LOGGER.info("Trades: '%d', '%d'", saxo_trade.Oid(), client_trade.Oid())

    def _fill_trade_premium(self, trade):
        trade.Premium(trade.Quantity() * trade.Price() * trade.Instrument().ContractSize() * -1)

    def save_add_infos(self, ins):
        LOGGER.info("Saving instrument addinfos...")
# end of Abstract builder


class IntFutureBuilder(AbstractObjectBuilder):

    ACM_CLASS = acm.FFuture

    def __init__(self, ins_name, acm_curr, ins_external_id,
        ins_expiry_date, ins_contract_size, trade_price, trade_opt_key,
        trade_date, value_date, trade_qty, acm_portf, acm_cparty,
        acm_extern_curr, acm_underlying, description, ins_saxo_type):

        super(IntFutureBuilder, self).__init__(ins_name=ins_name,
                                            acm_curr=acm_curr,
                                            ins_external_id=ins_external_id,
                                            ins_expiry_date=ins_expiry_date,
                                            ins_contract_size=ins_contract_size,
                                            trade_price=trade_price,
                                            trade_opt_key=trade_opt_key,
                                            trade_date=trade_date,
                                            value_date=value_date,
                                            trade_qty=trade_qty,
                                            acm_portf=acm_portf,
                                            acm_cparty=acm_cparty,
                                            acm_extern_curr=acm_extern_curr,
                                            ins_saxo_type=ins_saxo_type
                                            )
        self.acm_underlying = acm_underlying
        self.description = description

    def _fill_ins(self, ins):
        super(IntFutureBuilder, self)._fill_ins(ins)
        ins.FreeText(self.description)
        ins.Underlying(self.acm_underlying)
# end of FUT builder


class IntCFDBuilder(AbstractObjectBuilder):

    EXPIRY_DATE = "1900-01-02"
    ACM_CLASS = acm.FCfd

    def __init__(self, ins_name, acm_curr, ins_external_id,
        ins_contract_size, trade_price, trade_opt_key,
        trade_date, value_date, trade_qty, acm_portf, acm_cparty,
        acm_extern_curr, acm_underlying, description, ins_saxo_type):

        super(IntCFDBuilder, self).__init__(ins_name=ins_name,
                                         acm_curr=acm_curr,
                                         ins_external_id=ins_external_id,
                                         ins_expiry_date=self.EXPIRY_DATE,
                                         ins_contract_size=ins_contract_size,
                                         trade_price=trade_price,
                                         trade_opt_key=trade_opt_key,
                                         trade_date=trade_date,
                                         value_date=value_date,
                                         trade_qty=trade_qty,
                                         acm_portf=acm_portf,
                                         acm_cparty=acm_cparty,
                                         acm_extern_curr=acm_extern_curr,
                                         ins_saxo_type=ins_saxo_type
                                         )
        # self.isincode = isincode
        self.acm_underlying = acm_underlying
        self.description = description

    def _fill_ins(self, ins):
        super(IntCFDBuilder, self)._fill_ins(ins)
        # ins.Isin(self.isincode)
        ins.FreeText(self.description)
        ins.Underlying(self.acm_underlying)
        valuationGroup = acm.FChoiceList.Select("list = 'ValGroup' and name ='AC_GLOBAL'")[0]
        ins.ValuationGrpChlItem(valuationGroup)
# end of CFD builder


class IntETOBuilder(AbstractObjectBuilder):

    ACM_CLASS = acm.FOption

    def __init__(self, ins_name, acm_curr, ins_external_id,
        ins_expiry_date, ins_contract_size, trade_price, trade_opt_key,
        trade_date, value_date, trade_qty, acm_portf, acm_cparty,
        acm_extern_curr, acm_underlying, description,
        option_type,
        exercise_type,
        strike_price,
        ins_saxo_type
        ):

        super(IntETOBuilder, self).__init__(ins_name=ins_name,
                                         acm_curr=acm_curr,
                                         ins_external_id=ins_external_id,
                                         ins_expiry_date=ins_expiry_date,
                                         ins_contract_size=ins_contract_size,
                                         trade_price=trade_price,
                                         trade_opt_key=trade_opt_key,
                                         trade_date=trade_date,
                                         value_date=value_date,
                                         trade_qty=trade_qty,
                                         acm_portf=acm_portf,
                                         acm_cparty=acm_cparty,
                                         acm_extern_curr=acm_extern_curr,
                                         ins_saxo_type=ins_saxo_type
                                         )
        self.acm_underlying = acm_underlying
        self.description = description
        self.option_type = self._get_option_type(option_type)
        self.exercise_type = exercise_type
        self.strike_price = float(strike_price)

    def _get_option_type(self, saxo_option_type):
        if "PUT" in saxo_option_type.upper():
            return "Put"
        return "Call"

    def _fill_ins(self, ins):
        super(IntETOBuilder, self)._fill_ins(ins)
        ins.FreeText(self.description)
        ins.Underlying(self.acm_underlying)
        ins.OptionType(self.option_type)
        ins.ExerciseType(self.exercise_type)
        ins.StrikePrice(self.strike_price)

    def _fill_saxo_trade(self, trade):
        self._fill_trade_premium(trade)

    def _fill_client_trade(self, trade):
        self._fill_trade_premium(trade)

# end of ETO builder


class IntStockBuilder(AbstractObjectBuilder):

    EXPIRY_DATE = ""
    ACM_CLASS = acm.FStock

    def __init__(self, ins_name, acm_curr, ins_external_id,
        ins_contract_size, trade_price, trade_opt_key,
        trade_date, value_date, trade_qty, acm_portf, acm_cparty,
        acm_extern_curr, description, isin, ins_saxo_type):

        super(IntStockBuilder, self).__init__(ins_name=ins_name,
                                            acm_curr=acm_curr,
                                            ins_external_id=ins_external_id,
                                            ins_expiry_date=self.EXPIRY_DATE,
                                            ins_contract_size=ins_contract_size,
                                            trade_price=trade_price,
                                            trade_opt_key=trade_opt_key,
                                            trade_date=trade_date,
                                            value_date=value_date,
                                            trade_qty=trade_qty,
                                            acm_portf=acm_portf,
                                            acm_cparty=acm_cparty,
                                            acm_extern_curr=acm_extern_curr,
                                            ins_saxo_type=ins_saxo_type
                                            )
        self.description = description
        self.isin = check_isin_get(ins_name, isin)

    def _fill_ins(self, ins):
        super(IntStockBuilder, self)._fill_ins(ins)
        ins.FreeText(self.description)
        ins.Isin(self.isin)
        ins.PayType("Spot")
        ins.SpotBankingDaysOffset(0)

    def _fill_saxo_trade(self, trade):
        self._fill_trade_premium(trade)

    def _fill_client_trade(self, trade):
        self._fill_trade_premium(trade)

# end of STO builder


class IntFXBuilder(AbstractObjectBuilder):
    """
    USDZAR
    Base currency: USD - is an instrument
    Variable currency: ZAR - is a trade currency
    """


    def __init__(self, acm_base_curr, acm_var_curr,
        spot_price, trade_price, trade_opt_key, trade_date, value_date,
        trade_qty, acm_portf, acm_cparty, acm_extern_curr, ins_saxo_type):

        super(IntFXBuilder, self).__init__(ins_name=acm_base_curr.Name(),
                                           acm_curr=acm_var_curr,
                                           ins_external_id=None,
                                           ins_expiry_date=None,
                                           ins_contract_size=1,
                                           trade_price=trade_price,
                                           trade_opt_key=trade_opt_key,
                                           trade_date=trade_date,
                                           value_date=value_date,
                                           trade_qty=trade_qty,
                                           acm_portf=acm_portf,
                                           acm_cparty=acm_cparty,
                                           acm_extern_curr=acm_extern_curr,
                                           ins_saxo_type=ins_saxo_type
                                           )
        self.spot_price = spot_price

    @staticmethod
    def get_ins_code(saxo_ins_code, fx_type):
        """
        Get ins code from InstrumentCode and its FXType.

        InstrumentCode:
            - currency pair (USDZAR)
        FXType:
            - one of values: ('Spot', 'Forward')
        """
        return "{0}/{1}".format(saxo_ins_code, fx_type)

    @staticmethod
    def get_base_currency(saxo_inscode, variable_curr):
        """Get base currency for a currency pair.

        Base currency is part of saxo ins_code (NZDEUR).
        Usually as first currency in the code.
        But return always different currency from the pair than is the main currency.
        """
        inscode_size = len(saxo_inscode)
        half = inscode_size / 2
        curr1 = saxo_inscode[0 : half]
        curr2 = saxo_inscode[half:]
        if curr1 == variable_curr:
            return curr2
        return curr1

    def create_ins(self):
        return acm.FInstrument[self.ins_name]

    def _fill_saxo_trade(self, trade):
        self._fill_trade_premium(trade)
        trade.ReferencePrice(float(self.spot_price))
        trade.DiscountingType('CCYBasis')

    def _fill_client_trade(self, trade):
        self._fill_trade_premium(trade)
        trade.ReferencePrice(float(self.spot_price))
        trade.DiscountingType('CCYBasis')

# end of FX builder


class IntFXOptionBuilder(AbstractObjectBuilder):
    """
    USDZAR
    baseCurr = USD
    varCurr = ZAR

    tradeCurr = baseCurr = USD
    insCurr = varCurr = ZAR
    underlyingCurr = baseCurr = USD
    strikeCurr = varCurr = ZAR

    name: varCurr/FXO/SAXO/USDZAR/CallPut/expiry/strike
    ZAR/FXO/SAXO/USDZAR/P/NOV16/13.904

    """

    CONTRACT_SIZE = 1
    EXTERNAL_ID = ""
    ACM_CLASS = acm.FOption


    def __init__(self, ins_name, acm_base_curr, acm_var_curr,
        trade_price, ins_expiry_date, trade_opt_key,
        trade_date, value_date, trade_qty, acm_portf, acm_cparty,
        acm_extern_curr, ins_saxo_type, is_call, strike, delivery_date):

        super(IntFXOptionBuilder, self).__init__(ins_name=ins_name,
                                            acm_curr=acm_var_curr,
                                            ins_external_id=self.EXTERNAL_ID,
                                            ins_expiry_date=ins_expiry_date,
                                            ins_contract_size=self.CONTRACT_SIZE,
                                            trade_price=trade_price,
                                            trade_opt_key=trade_opt_key,
                                            trade_date=trade_date,
                                            value_date=value_date,
                                            trade_qty=trade_qty,
                                            acm_portf=acm_portf,
                                            acm_cparty=acm_cparty,
                                            acm_extern_curr=acm_extern_curr,
                                            ins_saxo_type=ins_saxo_type,
                                            )
        self.acm_base_curr = acm_base_curr
        self.acm_var_curr = acm_var_curr
        self.is_call = is_call
        self.strike = strike
        self.delivery_date = delivery_date

    @staticmethod
    def get_ins_code(saxo_ins_code, option_type):
        """
        Get ins code from InstrumentCode and its OptionType.

        InstrumentCode:
            - currency pair (USDZAR)
        OptionType:
            - one of values: ('Call', 'Put')
        """
        if "PUT" in option_type.upper():
            callput = "P"
        else:
            callput = "C"
        return "{0}/{1}".format(saxo_ins_code, callput)

    def _fill_ins(self, ins):
        super(IntFXOptionBuilder, self)._fill_ins(ins)
        ins.PayType('Future')
        ins.Otc(False)
        ins.Underlying(self.acm_base_curr)
        ins.IsCallOption(self.is_call)
        ins.StrikePrice(self.strike)
        ins.StrikeQuotation('Per Unit')
        ins.StrikeCurrency(self.acm_var_curr)
        LOGGER.info("Setting Strike currency: %s", ins.StrikeCurrency().Name())
        ins.PayDate(ins.ExpiryDateOnly())
        if self.delivery_date:
            offset = 0
            ins.PayDayOffset(offset)
            while get_backend_date(ins.DeliveryDate()) != self.delivery_date:
                offset += 1
                ins.PayDayOffset(offset)
                if offset > 10:
                    raise RuntimeError("Offset too big. Something is wrong with ins dates. "
                                       "Expiry: %s. DeliveryDate: %s" % (ins.ExpiryDateOnly(),
                                                                         self.delivery_date))

        else:
            # if 'ExpiryValueDate' in file is empty, use ExpiryDate + 2 as default;
            ins.PayDayOffset(2)

    def _fill_saxo_trade(self, trade):
        trade.Currency(self.acm_base_curr)

    def _fill_client_trade(self, trade):
        trade.Currency(self.acm_base_curr)

# end of FXO builder


def check_instrument(ins_name, ins_code):

    extern_ins = acm.FInstrument.Select('externalId1 = "%s"' % ins_code)
    if extern_ins and extern_ins[0].Name() != ins_name:
        raise ValueError(
            "ERROR: Instrument with ExternalId '%s'" % ins_code +
            " but different name '%s' " % extern_ins[0].Name() +
            "already exists. Skipping this one '%s'." % ins_name)

    ins = acm.FInstrument[ins_name]
    if ins and ins.ExternalId1() != ins_code:
        raise ValueError(
            "ERROR: Instrument with the same name '%s'" % ins.Name() +
            " but different ExternalId '%s' already exists." % ins.ExternalId1() +
            " Skipping this one.")


def check_isin_get(ins_name, isin):
    """
    1)	If there will be an instrument with different name, but same ISIN,
        will use blank ISIN and raise a WARNING.
    2)	If there will be an instrument with same name, but with blank ISIN,
        will consider it as a same instrument and use blank ISIN.
    3)	If there will be an instrument with same name,
        but with nonblank ISIN and different ISIN, will raise an error.
    """

    instr_isin = acm.FInstrument[isin]
    if instr_isin and instr_isin.Name() != ins_name:
        warning = ("Instrument collision: Instrument with same ISIN ('%s'), "
            "but different name ('%s') already exists. "
            "Please update the existing one. Using empty ISIN now."
            % (isin, instr_isin.Name()))
        InputProperties.add_warning(warning)
        LOGGER.warning(warning)
        return ""

    instr = acm.FInstrument[ins_name]
    if instr:
        if not instr.Isin():
            return ""
        if instr.Isin() != isin:
            raise RuntimeError("Instrument '%s' error: "
                "New ISIN ('%s') is different from original ISIN ('%s'). "
                "Please, update instrument manually."
                % (instr.Name(), isin, instr.Isin()))

    return isin


class FutOpenTradesCSV(SimpleCSVFeedProcessor):

    FILE_INDEX = "fut_open_pos_file_name"
    LOAD_THIS_INDEX = "fut_load_open_pos"

    col_account_number = "AccountNumber"
    col_account_curr = "AccountCurrency"
    col_ins_type = "InstrumentType"
    col_ins_code = "Instrument"
    col_ins_price = "EODRate"
    col_ins_curr = "InstrumentCurrency"
    col_ins_exp_date = "ExpiryDate"
    col_ins_fig_size = "FigureSize"
    col_trd_qty = "Amount"
    col_trd_nbr = "TradeNumber"
    col_trd_date = "TradeDate"
    col_trd_val_date = "ValueDate"
    col_trd_price = "Price"
    col_eod_date = "ReportingDate"
    col_sector = "Sector"
    col_description = "Description"

    _required_columns = [col_account_number, col_ins_type, col_account_curr,
        col_ins_code, col_ins_curr, col_ins_exp_date, col_trd_qty, col_trd_nbr,
        col_trd_date, col_trd_val_date, col_trd_price, col_eod_date, col_sector,
        col_description]

    def __init__(self, file_path, sectors_dict):
        super(FutOpenTradesCSV, self).__init__(file_path)
        self._dict_reader_kwargs = {'delimiter':DELIMITER}
        self.sectors_dict = sectors_dict

    def _get_underlying(self, sector):
        if not self.sectors_dict.has_key(sector.upper()):
            raise RuntimeError("Sector not recognised: '%s'" % sector)
        instr = acm.FInstrument[self.sectors_dict[sector.upper()]]
        if not instr:
            raise RuntimeError("ERROR: Can't map sector '%s' to any underlying instrument" % sector)
        return instr

    def _process_record(self, record, dry_run):
        print "\n%s processing" % self.__class__.__name__
        (_index, record_data) = record

        try:
            alias = get_account_alias(record_data[self.col_account_number])
            if not alias:
                LOGGER.info("Skipping account '%s' (alias not recognised)...",
                    record_data[self.col_account_number])
                return

            curr = acm.FCurrency[record_data[self.col_ins_curr]]
            external_curr = acm.FCurrency[record_data[self.col_account_curr]]
            underlying = self._get_underlying(record_data[self.col_sector])

            cparty = get_pb_fund_counterparty(alias)
            ins_code = sanitize_code(record_data[self.col_ins_code])
            ins_name = get_ins_name(
                record_data[self.col_ins_type],
                ins_code,
                record_data[self.col_ins_curr],
                expiry_date=record_data[self.col_ins_exp_date])

            external_id = AbstractObjectBuilder.get_external_id(record_data[self.col_ins_type],
                                                                ins_code)
            check_instrument(ins_name, external_id)

            expiry = get_fa_date(record_data[self.col_ins_exp_date])
            constract_size = float(record_data[self.col_ins_fig_size])
            trade_price = float(record_data[self.col_trd_price])
            portf = get_fund_portf(alias)

            if TRADE_DATE:
                trade_date = TRADE_DATE
                value_date = TRADE_DATE
                eod_date = TRADE_DATE
            else:
                trade_date = get_fa_date(record_data[self.col_trd_date])
                value_date = get_fa_date(record_data[self.col_trd_val_date])
                eod_date = get_fa_date(record_data[self.col_eod_date])

            creator = IntFutureBuilder(
                ins_name=ins_name,
                acm_curr=curr,
                ins_external_id=external_id,
                ins_expiry_date=expiry,
                ins_contract_size=constract_size,
                trade_price=trade_price,
                trade_opt_key=record_data[self.col_trd_nbr],
                trade_date=trade_date,
                value_date=value_date,
                trade_qty=float(record_data[self.col_trd_qty]),
                acm_portf=portf,
                acm_cparty=cparty,
                acm_extern_curr=external_curr,
                acm_underlying=underlying,
                description=remove_nonascii(record_data[self.col_description]),
                ins_saxo_type=record_data[self.col_ins_type])

            ins = acm.FInstrument[ins_name]
            if not ins:
                ins = creator.create_ins()
            elif UPDATE_INSTR:
                ins = creator.update_ins(ins)

            LOGGER.info("Instrument loaded: '%s'", ins.Name())

            ins_price = float(record_data[self.col_ins_price])

            save_ins_price(ins, acm.FMTMMarket["internal"], ins_price, curr, eod_date)
            save_ins_price(ins, acm.FMarketPlace["SPOT"], ins_price, curr, eod_date)
            save_ins_price(ins, acm.FMarketPlace["SPOT_MID"], ins_price, curr, eod_date)
            if SET_TODAY_SPOT:
                save_ins_price(ins, acm.FMarketPlace["SPOT"], ins_price, curr, acm.Time.DateToday())

            creator.book_trades()

        except Exception as exc:
            traceback.print_exception(*sys.exc_info())
            raise self.RecordProcessingException(
                "ERROR while processing row #%d of file '%s': %s" \
                    % (_index, os.path.basename(self._file_path), str(exc)))
# end of FUT Open Trades


class CFDOpenTradesCSV(SimpleCSVFeedProcessor):

    FILE_INDEX = "cfd_open_pos_file_name"
    LOAD_THIS_INDEX = "cfd_load_open_pos"

    col_account_number = "AccountNumber"
    col_account_curr = "AccountCurrency"
    col_ins_type = "InstrumentType"
    col_ins_code = "Instrument"
    col_isin_code = "ISINCode"
    col_ins_price = "EODRate"
    col_ins_curr = "InstrumentCurrency"
    col_ins_fig_size = "FigureSize"
    col_trd_qty = "Amount"
    col_trd_nbr = "TradeNumber"
    col_trd_date = "TradeDate"
    col_trd_val_date = "ValueDate"
    col_trd_price = "Price"
    col_eod_date = "ReportingDate"
    col_description = "Description"

    _required_columns = [col_account_number, col_ins_type, col_account_curr, col_ins_code,
        col_ins_curr, col_trd_qty, col_trd_nbr, col_ins_fig_size,
        col_trd_date, col_trd_val_date, col_trd_price, col_eod_date, col_isin_code,
        col_description]

    def __init__(self, file_path, instr_obj):
        super(CFDOpenTradesCSV, self).__init__(file_path)
        self._dict_reader_kwargs = {'delimiter':DELIMITER}
        self.instr_obj = instr_obj

    def _get_underlying(self, inscode):

        # get underlying from instrument list file
        underlying = None
        for asset_class in self.instr_obj.asset_classes:
            if asset_class.has_instrument(inscode):
                underlying = asset_class.underlying
                break

        if underlying:
            return acm.FInstrument[underlying]

        LOGGER.warning("Can't determine underlying for '%s'. Using default one: %s",
            inscode, self.instr_obj.default_underlying)
        return acm.FInstrument[self.instr_obj.default_underlying]

    def _process_record(self, record, dry_run):
        print "\n%s processing" % self.__class__.__name__
        (_index, record_data) = record

        try:
            alias = get_account_alias(record_data[self.col_account_number])
            if not alias:
                LOGGER.info("Skipping account '%s' (alias not recognised)...",
                    record_data[self.col_account_number])
                return

            ins_code = sanitize_code(record_data[self.col_ins_code])
            curr = acm.FCurrency[record_data[self.col_ins_curr]]
            external_curr = acm.FCurrency[record_data[self.col_account_curr]]
            underlying = self._get_underlying(ins_code)

            cparty = get_pb_fund_counterparty(alias)

            ins_name = get_ins_name(
                record_data[self.col_ins_type],
                ins_code,
                record_data[self.col_ins_curr])


            external_id = AbstractObjectBuilder.get_external_id(record_data[self.col_ins_type],
                                                                ins_code)
            check_instrument(ins_name, external_id)

            ins = acm.FInstrument[ins_name]

            constract_size = float(record_data[self.col_ins_fig_size])
            trade_price = float(record_data[self.col_trd_price])
            portf = get_fund_portf(alias)

            if TRADE_DATE:
                trade_date = TRADE_DATE
                value_date = TRADE_DATE
                eod_date = TRADE_DATE
            else:
                trade_date = get_fa_date(record_data[self.col_trd_date])
                value_date = get_fa_date(record_data[self.col_trd_val_date])
                eod_date = get_fa_date(record_data[self.col_eod_date])

            creator = IntCFDBuilder(
                ins_name=ins_name,
                acm_curr=curr,
                ins_external_id=external_id,
                ins_contract_size=constract_size,
                trade_price=trade_price,
                trade_opt_key=record_data[self.col_trd_nbr],
                trade_date=trade_date,
                value_date=value_date,
                trade_qty=float(record_data[self.col_trd_qty]),
                acm_portf=portf,
                acm_cparty=cparty,
                acm_extern_curr=external_curr,
                acm_underlying=underlying,
                description=remove_nonascii(record_data[self.col_description]),
                ins_saxo_type=record_data[self.col_ins_type])

            if not ins:
                ins = creator.create_ins()
            elif UPDATE_INSTR:
                ins = creator.update_ins(ins)

            LOGGER.info("Instrument loaded: '%s'", ins.Name())

            ins_price = float(record_data[self.col_ins_price])

            save_ins_price(ins, acm.FMTMMarket["internal"], ins_price, curr, eod_date)
            save_ins_price(ins, acm.FMarketPlace["SPOT"], ins_price, curr, eod_date)
            save_ins_price(ins, acm.FMarketPlace["SPOT_MID"], ins_price, curr, eod_date)
            if SET_TODAY_SPOT:
                save_ins_price(ins, acm.FMarketPlace["SPOT"], ins_price, curr, acm.Time.DateToday())

            creator.book_trades()

        except Exception as exc:
            traceback.print_exception(*sys.exc_info())
            raise self.RecordProcessingException(
                "ERROR while processing row #%d of file '%s': %s" \
                    % (_index, os.path.basename(self._file_path), str(exc)))
# end of CFD Open Trades


class ETOTradesExecCSV(SimpleCSVFeedProcessor):

    FILE_INDEX = "eto_trades_file_name"
    LOAD_THIS_INDEX = "eto_load_trades_exec"

    col_account_number = "AccountNumber"
    col_account_curr = "AccountCurrency"
    col_ins_type = "InstrumentType"
    col_ins_code = "InstrumentCode"
    col_ins_price = "EODRate"
    col_ins_curr = "InstrumentCurrency"
    col_ins_exp_date = "ExpiryDate"
    col_ins_fig_size = "FigureSize"
    col_trd_qty = "TradedAmount"
    col_trd_nbr = "TradeNumber"
    col_trd_date = "TradeDate"
    col_trd_val_date = "ValueDate"
    col_trd_price = "Price"
    col_eod_date = "ReportingDate"
    col_sector = "Sector"
    col_description = "InstrumentDescription"
    col_call_put = "CallPut"
    col_option_style = "OptionStyle"
    col_strike_price = "Strike"
    col_underlying_ins_code = "UnderlyingInstrumentCode"

    _required_columns = [col_account_number, col_ins_type, col_account_curr,
        col_ins_code, col_ins_curr, col_ins_exp_date, col_trd_qty, col_trd_nbr,
        col_trd_date, col_trd_val_date, col_trd_price, col_eod_date, col_sector,
        col_description]

    def __init__(self, file_path, sectors_dict):
        super(ETOTradesExecCSV, self).__init__(file_path)
        self._dict_reader_kwargs = {'delimiter':DELIMITER}
        self.sectors_dict = sectors_dict

    def _get_underlying(self, sector):
        if not self.sectors_dict.has_key(sector.upper()):
            raise RuntimeError("ERROR: Sector '%s' not recognised" % sector)
        instr = acm.FInstrument[self.sectors_dict[sector.upper()]]
        if not instr:
            raise RuntimeError("ERROR: Can't map sector '%s' to any underlying instrument" % sector)
        return instr

    def _process_record(self, record, dry_run):
        print "\n%s processing" % self.__class__.__name__
        (_index, record_data) = record

        try:
            alias = get_account_alias(record_data[self.col_account_number])
            if not alias:
                LOGGER.info("Skipping account '%s' (alias not recognised)...",
                    record_data[self.col_account_number])
                return

            curr = acm.FCurrency[record_data[self.col_ins_curr]]
            external_curr = acm.FCurrency[record_data[self.col_account_curr]]
            underlying = self._get_underlying(record_data[self.col_sector])

            cparty = get_pb_fund_counterparty(alias)
            ins_code = sanitize_code(record_data[self.col_ins_code])
            ins_name = get_ins_name(
                record_data[self.col_ins_type],
                ins_code,
                record_data[self.col_ins_curr],
                expiry_date=record_data[self.col_ins_exp_date],
                callput=record_data[self.col_call_put])


            external_id = AbstractObjectBuilder.get_external_id(record_data[self.col_ins_type],
                                                                ins_code)
            check_instrument(ins_name, external_id)

            ins = acm.FInstrument[ins_name]

            expiry = get_fa_date(record_data[self.col_ins_exp_date])
            constract_size = float(record_data[self.col_ins_fig_size])
            trade_price = float(record_data[self.col_trd_price])
            portf = get_fund_portf(alias)

            if TRADE_DATE:
                trade_date = TRADE_DATE
                value_date = TRADE_DATE
                eod_date = TRADE_DATE
            else:
                trade_date = get_fa_date(record_data[self.col_trd_date])
                value_date = get_fa_date(record_data[self.col_trd_val_date])
                eod_date = get_fa_date(record_data[self.col_eod_date])


            creator = IntETOBuilder(
                ins_name=ins_name,
                acm_curr=curr,
                ins_external_id=external_id,
                ins_expiry_date=expiry,
                ins_contract_size=constract_size,
                trade_price=trade_price,
                trade_opt_key=record_data[self.col_trd_nbr],
                trade_date=trade_date,
                value_date=value_date,
                trade_qty=float(record_data[self.col_trd_qty]),
                acm_portf=portf,
                acm_cparty=cparty,
                acm_extern_curr=external_curr,
                acm_underlying=underlying,
                description=remove_nonascii(record_data[self.col_description]),
                option_type=record_data[self.col_call_put],
                exercise_type=record_data[self.col_option_style],
                strike_price=record_data[self.col_strike_price],
                ins_saxo_type=record_data[self.col_ins_type],
                )

            if not ins:
                ins = creator.create_ins()
            elif UPDATE_INSTR:
                ins = creator.update_ins(ins)

            LOGGER.info("Instrument loaded: '%s'", ins.Name())

            ins_price = float(record_data[self.col_ins_price])

            save_ins_price(ins, acm.FMTMMarket["internal"], ins_price, curr, eod_date)
            save_ins_price(ins, acm.FMarketPlace["SPOT"], ins_price, curr, eod_date)
            save_ins_price(ins, acm.FMarketPlace["SPOT_MID"], ins_price, curr, eod_date)
            if SET_TODAY_SPOT:
                save_ins_price(ins, acm.FMarketPlace["SPOT"], ins_price, curr, acm.Time.DateToday())

            creator.book_trades()

        except Exception as exc:
            traceback.print_exception(*sys.exc_info())
            raise self.RecordProcessingException(
                "ERROR while processing row #%d of file '%s': %s" \
                    % (_index, os.path.basename(self._file_path), str(exc)))
# end of ETO Trades Executed


class FutTradesExecCSV(FutOpenTradesCSV):

    FILE_INDEX = "fut_trades_file_name"
    LOAD_THIS_INDEX = "fut_load_trades_exec"

    col_account_number = "AccountNumber"
    col_account_curr = "AccountCurrency"
    col_ins_type = "InstrumentType"
    col_ins_code = "InstrumentCode"
    col_ins_price = "EODRate"
    col_ins_curr = "InstrumentCurrency"
    col_ins_exp_date = "ExpiryDate"
    col_ins_fig_size = "FigureSize"
    col_trd_qty = "TradedAmount"
    col_trd_nbr = "TradeNumber"
    col_trd_fig_size = "FigureSize"
    col_trd_date = "TradeDate"
    col_trd_val_date = "ValueDate"
    col_trd_price = "Price"
    col_eod_date = "ReportingDate"
    col_sector = "Sector"
    col_description = "InstrumentDescription"

    _required_columns = [col_account_number, col_ins_type, col_account_curr, col_ins_code,
        col_ins_curr, col_ins_exp_date, col_trd_qty, col_trd_nbr, col_trd_fig_size,
        col_trd_date, col_trd_val_date, col_trd_price, col_eod_date, col_sector,
        col_description]
# end of FUT Trades Executed


class CFDTradesExecCSV(CFDOpenTradesCSV):

    FILE_INDEX = "cfd_trades_file_name"
    LOAD_THIS_INDEX = "cfd_load_trades_exec"

    col_account_number = "AccountNumber"
    col_account_curr = "AccountCurrency"
    col_ins_type = "InstrumentType"
    col_ins_code = "InstrumentCode"
    col_ins_price = "EODRate"
    col_ins_curr = "InstrumentCurrency"
    col_ins_fig_size = "FigureSize"
    col_trd_qty = "TradedAmount"
    col_trd_nbr = "TradeNumber"
    col_trd_fig_size = "FigureSize"
    col_trd_date = "TradeDate"
    col_trd_val_date = "ValueDate"
    col_trd_price = "Price"
    col_eod_date = "ReportingDate"
    col_isin_code = "ISINCode"
    col_description = "InstrumentDescription"

    _required_columns = [col_account_number, col_ins_type, col_account_curr, col_ins_code,
        col_ins_curr, col_trd_qty, col_trd_nbr, col_trd_fig_size,
        col_trd_date, col_trd_val_date, col_trd_price, col_eod_date, col_isin_code, col_description]
# end of CFD Trades Executed


class ShareTradesExecCSV(SimpleCSVFeedProcessor):

    FILE_INDEX = "sto_trades_exec_file_name"
    LOAD_THIS_INDEX = "sto_load_trades_exec"

    col_account_number = "AccountNumber"
    col_account_curr = "AccountCurrency"
    col_ins_type = "InstrumentType"
    col_ins_code = "InstrumentCode"
    col_ins_price = "EODRate"
    col_ins_curr = "InstrumentCurrency"
    col_ins_fig_size = "FigureSize"
    col_trd_qty = "TradedAmount"
    col_trd_nbr = "TradeNumber"
    col_trd_date = "TradeDate"
    col_trd_val_date = "ValueDate"
    col_trd_price = "Price"
    col_eod_date = "ReportingDate"
    col_description = "InstrumentDescription"
    col_isin_code = "ISINCode"

    _required_columns = [col_account_number, col_ins_type, col_account_curr, col_ins_code,
        col_ins_curr, col_trd_qty, col_trd_nbr, col_ins_fig_size,
        col_trd_date, col_trd_val_date, col_trd_price, col_eod_date,
        col_description, col_isin_code]

    def __init__(self, file_path):
        super(ShareTradesExecCSV, self).__init__(file_path)
        self._dict_reader_kwargs = {'delimiter':DELIMITER}

    def _process_record(self, record, dry_run):
        print "\n%s processing" % self.__class__.__name__
        (_index, record_data) = record

        try:
            alias = get_account_alias(record_data[self.col_account_number])
            if not alias:
                LOGGER.info("Skipping account '%s' (alias not recognised)...",
                    record_data[self.col_account_number])
                return

            ins_code = sanitize_code(record_data[self.col_ins_code])
            curr = acm.FCurrency[record_data[self.col_ins_curr]]
            external_curr = acm.FCurrency[record_data[self.col_account_curr]]

            cparty = get_pb_fund_counterparty(alias)

            ins_name = get_ins_name(
                record_data[self.col_ins_type],
                ins_code,
                record_data[self.col_ins_curr])

            external_id = AbstractObjectBuilder.get_external_id(record_data[self.col_ins_type],
                                                                ins_code)

            check_instrument(ins_name, external_id)

            ins = acm.FInstrument[ins_name]

            constract_size = float(record_data[self.col_ins_fig_size])
            trade_price = float(record_data[self.col_trd_price])
            portf = get_fund_portf(alias)

            if TRADE_DATE:
                trade_date = TRADE_DATE
                value_date = TRADE_DATE
                eod_date = TRADE_DATE
            else:
                trade_date = get_fa_date(record_data[self.col_trd_date])
                value_date = get_fa_date(record_data[self.col_trd_val_date])
                eod_date = get_fa_date(record_data[self.col_eod_date])


            creator = IntStockBuilder(
                ins_name=ins_name,
                acm_curr=curr,
                ins_external_id=external_id,
                ins_contract_size=constract_size,
                trade_price=trade_price,
                trade_opt_key=record_data[self.col_trd_nbr],
                trade_date=trade_date,
                value_date=value_date,
                trade_qty=float(record_data[self.col_trd_qty]),
                acm_portf=portf,
                acm_cparty=cparty,
                acm_extern_curr=external_curr,
                isin=remove_nonascii(record_data[self.col_isin_code]),
                description=remove_nonascii(record_data[self.col_description]),
                ins_saxo_type=record_data[self.col_ins_type])

            if not ins:
                ins = creator.create_ins()
            elif UPDATE_INSTR:
                ins = creator.update_ins(ins)

            LOGGER.info("Instrument loaded: '%s'", ins.Name())

            ins_price = float(record_data[self.col_ins_price])

            save_ins_price(ins, acm.FMTMMarket["internal"], ins_price, curr, eod_date)
            save_ins_price(ins, acm.FMarketPlace["SPOT"], ins_price, curr, eod_date)
            save_ins_price(ins, acm.FMarketPlace["SPOT_MID"], ins_price, curr, eod_date)
            if SET_TODAY_SPOT:
                save_ins_price(ins, acm.FMarketPlace["SPOT"], ins_price, curr, acm.Time.DateToday())

            creator.book_trades()

        except Exception as exc:
            traceback.print_exception(*sys.exc_info())
            raise self.RecordProcessingException(
                "ERROR while processing row #%d of file '%s': %s" \
                    % (_index, os.path.basename(self._file_path), str(exc)))
# end of SHARE Trades Executed


class FXTradesExecCSV(SimpleCSVFeedProcessor):

    FILE_INDEX = "fx_trades_exec_file_name"
    LOAD_THIS_INDEX = "fx_load_trades_exec"

    col_account_number = "AccountNumber"
    col_account_curr = "AccountCurrency"
    col_ins_type = "InstrumentType"
    col_ins_code = "InstrumentCode"
    col_ins_price = "EODRate"
    col_ins_curr = "InstrumentCurrency"
    col_trd_qty = "TradedAmount"
    col_trd_nbr = "TradeNumber"
    col_trd_date = "TradeDate"
    col_trd_val_date = "ValueDate"
    col_trd_price = "Price"  # Price contains Spot + Points, i.e. it's Forward price
    col_spot_price = "SpotPrice"  # in case of Spot trade it's same as Price
    col_fx_type = "FXType"

    _required_columns = [col_account_number, col_ins_type, col_account_curr, col_ins_code,
        col_ins_curr, col_trd_qty, col_trd_nbr, col_spot_price,
        col_trd_date, col_trd_val_date, col_trd_price, col_fx_type]

    def __init__(self, file_path):
        super(FXTradesExecCSV, self).__init__(file_path)
        self._dict_reader_kwargs = {'delimiter':DELIMITER}

    def _process_record(self, record, dry_run):
        print "\n%s processing" % self.__class__.__name__
        (_index, record_data) = record

        try:
            alias = get_account_alias(record_data[self.col_account_number])
            if not alias:
                LOGGER.info("Skipping account '%s' (alias not recognised)...",
                    record_data[self.col_account_number])
                return

            variable_curr = acm.FCurrency[record_data[self.col_ins_curr]]
            external_curr = acm.FCurrency[record_data[self.col_account_curr]]
            ins_code = sanitize_code(record_data[self.col_ins_code])
            base_curr_name = IntFXBuilder.get_base_currency(ins_code, variable_curr.Name())
            base_curr = acm.FCurrency[base_curr_name]

            LOGGER.info("FX Instrument: '%s' \n\tBase Curr: '%s' \n\tVar Curr: '%s'",
                                            record_data[self.col_ins_code],
                                            base_curr.Name(),
                                            variable_curr.Name())

            cparty = get_pb_fund_counterparty(alias)
            spot_price = float(record_data[self.col_spot_price])  # Spot price
            trade_price = float(record_data[self.col_trd_price])  # Spot price + Points = Fwd price
            portf = get_fund_portf(alias)

            if TRADE_DATE:
                trade_date = TRADE_DATE
                value_date = TRADE_DATE
            else:
                trade_date = get_fa_date(record_data[self.col_trd_date])
                value_date = get_fa_date(record_data[self.col_trd_val_date])

            creator = IntFXBuilder(
                acm_base_curr=base_curr,
                acm_var_curr=variable_curr,
                spot_price=spot_price,
                trade_price=trade_price,
                trade_opt_key=record_data[self.col_trd_nbr],
                trade_date=trade_date,
                value_date=value_date,
                trade_qty=float(record_data[self.col_trd_qty]),
                acm_portf=portf,
                acm_cparty=cparty,
                acm_extern_curr=external_curr,
                ins_saxo_type=record_data[self.col_ins_type]
                )
            ins = creator.create_ins()
            LOGGER.info("Instrument loaded: '%s'", ins.Name())

            creator.book_trades()

        except Exception as exc:
            traceback.print_exception(*sys.exc_info())
            raise self.RecordProcessingException(
                "ERROR while processing row #%d of file '%s': %s" \
                    % (_index, os.path.basename(self._file_path), str(exc)))
# end of FX Trades Executed


class FXOptionTradesExecCSV(SimpleCSVFeedProcessor):

    FILE_INDEX = "fxoption_trades_exec_file_name"
    LOAD_THIS_INDEX = "fxoption_load_trades_exec"

    col_account_number = "AccountNumber"
    col_account_curr = "AccountCurrency"
    col_ins_type = "InstrumentType"
    col_ins_code = "InstrumentCode"
    col_ins_price = "EODRate"
    col_ins_curr = "InstrumentCurrency"
    col_trd_qty = "TradedAmount"
    col_trd_nbr = "TradeNumber"
    col_trd_date = "TradeDate"
    col_trd_val_date = "ValueDate"
    col_trd_price = "Price"
    col_eod_date = "ReportingDate"
    col_callput = "CallPut"
    col_strike = "Strike"
    col_ins_exp_date = "ExpiryDate"
    col_option_type = "OptionType"
    col_delivery_date = "ExpiryValueDate"

    _required_columns = [col_account_number, col_ins_type, col_account_curr, col_ins_code,
        col_ins_curr, col_trd_qty, col_trd_nbr,
        col_trd_date, col_trd_val_date, col_trd_price, col_eod_date,
        col_callput, col_strike, col_ins_exp_date, col_delivery_date]

    _supported_option_types = ("Vanilla Option", )

    def __init__(self, file_path):
        super(FXOptionTradesExecCSV, self).__init__(file_path)
        self._dict_reader_kwargs = {'delimiter':DELIMITER}

    def _process_record(self, record, dry_run):
        print "\n%s processing" % self.__class__.__name__
        (_index, record_data) = record

        try:
            alias = get_account_alias(record_data[self.col_account_number])
            if not alias:
                LOGGER.info("Skipping account '%s' (alias not recognised)...",
                    record_data[self.col_account_number])
                return

            if record_data[self.col_option_type] not in self._supported_option_types:
                # There are currently Vanilla Options only that we can test.
                # After a new option type appears, its FA definition needs to be specified
                raise RuntimeError("Unsupported option type: '%s'" % record_data[self.col_option_type])

            variable_curr = acm.FCurrency[record_data[self.col_ins_curr]]
            external_curr = acm.FCurrency[record_data[self.col_account_curr]]
            ins_code = sanitize_code(record_data[self.col_ins_code])
            base_curr_name = IntFXBuilder.get_base_currency(ins_code, variable_curr.Name())
            base_curr = acm.FCurrency[base_curr_name]
            strike = float(record_data[self.col_strike])

            LOGGER.info("FX Option Instrument: '%s' \n\tBase Curr: '%s' \n\tVar Curr: '%s'",
                                            record_data[self.col_ins_code],
                                            base_curr.Name(),
                                            variable_curr.Name())

            cparty = get_pb_fund_counterparty(alias)
            ins_code = IntFXOptionBuilder.get_ins_code(ins_code, record_data[self.col_callput])
            ins_name = get_ins_name(
                record_data[self.col_ins_type],
                ins_code,
                variable_curr.Name(),
                expiry_date=record_data[self.col_ins_exp_date],
                strike=strike
                )

            trade_price = float(record_data[self.col_trd_price])
            portf = get_fund_portf(alias)

            if TRADE_DATE:
                trade_date = TRADE_DATE
                value_date = TRADE_DATE
                eod_date = TRADE_DATE
                delivery_date = TRADE_DATE
            else:
                trade_date = get_fa_date(record_data[self.col_trd_date])
                value_date = get_fa_date(record_data[self.col_trd_val_date])
                eod_date = get_fa_date(record_data[self.col_eod_date])
                if record_data[self.col_delivery_date]:
                    delivery_date = get_fa_date(record_data[self.col_delivery_date])
                else:
                    delivery_date = None

            creator = IntFXOptionBuilder(
                ins_name=ins_name,
                acm_base_curr=base_curr,
                acm_var_curr=variable_curr,
                trade_price=trade_price,
                trade_opt_key=record_data[self.col_trd_nbr],
                trade_date=trade_date,
                value_date=value_date,
                trade_qty=float(record_data[self.col_trd_qty]),
                acm_portf=portf,
                acm_cparty=cparty,
                acm_extern_curr=external_curr,
                ins_expiry_date=get_fa_date(record_data[self.col_ins_exp_date]),
                ins_saxo_type=record_data[self.col_ins_type],
                is_call=True if record_data[self.col_callput].upper() == 'CALL' else False,
                strike=strike,
                delivery_date=delivery_date
                )

            ins = acm.FInstrument[ins_name]
            if not ins:
                ins = creator.create_ins()
            elif UPDATE_INSTR:
                ins = creator.update_ins(ins)

            LOGGER.info("Instrument loaded: '%s'", ins.Name())

            ins_price = float(record_data[self.col_ins_price])

            save_ins_price(ins, acm.FMTMMarket["internal"], ins_price, base_curr, eod_date)
            save_ins_price(ins, acm.FMarketPlace["SPOT"], ins_price, base_curr, eod_date)
            save_ins_price(ins, acm.FMarketPlace["SPOT_MID"], ins_price, base_curr, eod_date)
            if SET_TODAY_SPOT:
                save_ins_price(ins, acm.FMarketPlace["SPOT"], ins_price, base_curr, acm.Time.DateToday())

            creator.book_trades()

        except Exception as exc:
            traceback.print_exception(*sys.exc_info())
            raise self.RecordProcessingException(
                "ERROR while processing row #%d of file '%s': %s" \
                    % (_index, os.path.basename(self._file_path), str(exc)))
# end of FX Options Trades Executed


class PricesCSV(SimpleCSVFeedProcessor):
    """
    Set instrument price of all Saxo instrument types.
    """

    FILE_INDEX = "ins_prices_file_name"
    LOAD_THIS_INDEX = "load_ins_prices"

    col_account_number = "AccountNumber"
    col_ins_type = "InstrumentType"
    # col_ins_code = "InstrumentCode"  # used for trades executedExecuted file - for closed pos prices

    col_ins_code = "Instrument"  # in OpenPositions prices
    col_ins_code2 = "InstrumentCode"  # in CFD OpenPositions

    col_ins_price = "EODRate"
    col_ins_curr = "InstrumentCurrency"
    col_ins_exp_date = "ExpiryDate"
    col_eod_date = "ReportingDate"
    col_ins_fig_size = "FigureSize"
    col_callput = "CallPut"
    col_strike = "Strike"

    _required_columns = [col_ins_type, col_ins_price,
        col_ins_curr, col_eod_date]

    _ins_codes = (col_ins_code, col_ins_code2)

    def __init__(self, file_path):
        super(PricesCSV, self).__init__(file_path)
        self._dict_reader_kwargs = {'delimiter':DELIMITER}

    def _get_ins_code(self, rec_data):
        ins_code = ""
        for ic in self._ins_codes:
            if ic in rec_data:
                ins_code = rec_data[ic]
                break

        if not ins_code:
            raise RuntimeError("Instrument ID column not found")

        return sanitize_code(ins_code)

    def _process_record(self, record, dry_run):
        print "\n%s processing" % self.__class__.__name__
        (_index, record_data) = record

        try:
            alias = get_account_alias(record_data[self.col_account_number])
            if not alias:
                LOGGER.info("Skipping account '%s' (alias not recognised)...",
                    record_data[self.col_account_number])
                return

            curr = acm.FCurrency[record_data[self.col_ins_curr]]
            ins_code = self._get_ins_code(record_data)

            the_kwargs = {}
            if record_data[self.col_ins_type] == SAXO_FUT_TYPE:
                the_kwargs['expiry_date'] = record_data[self.col_ins_exp_date]

            elif record_data[self.col_ins_type] == SAXO_ETO_TYPE:
                the_kwargs['expiry_date'] = record_data[self.col_ins_exp_date]
                the_kwargs['callput'] = record_data[self.col_callput]

            elif record_data[self.col_ins_type] == SAXO_FXO_TYPE:
                ins_code = IntFXOptionBuilder.get_ins_code(ins_code, record_data[self.col_callput])
                the_kwargs['expiry_date'] = record_data[self.col_ins_exp_date]
                the_kwargs['strike'] = record_data[self.col_strike]

            elif record_data[self.col_ins_type] == SAXO_FX_TYPE:
                return

            ins_name = get_ins_name(
                record_data[self.col_ins_type],
                ins_code,
                record_data[self.col_ins_curr],
                **the_kwargs)

            ins = acm.FInstrument[ins_name]

            # save price only if both name and external ID match
            if not ins:
                raise self.RecordProcessingException(
                    "WARING: No FA instrument found '%s'. Price won't be uploaded." % ins_name)

            LOGGER.info("Instrument loaded: '%s'", ins.Name())

            if TRADE_DATE:
                eod_date = TRADE_DATE
            else:
                eod_date = get_fa_date(record_data[self.col_eod_date])
            ins_price = float(record_data[self.col_ins_price])

            save_ins_price(ins, acm.FMTMMarket["internal"], ins_price, curr, eod_date)
            save_ins_price(ins, acm.FMarketPlace["SPOT"], ins_price, curr, eod_date)
            save_ins_price(ins, acm.FMarketPlace["SPOT_MID"], ins_price, curr, eod_date)
            if SET_TODAY_SPOT:
                save_ins_price(ins, acm.FMarketPlace["SPOT"], ins_price, curr, acm.Time.DateToday())

        except Exception as exc:
            traceback.print_exception(*sys.exc_info())
            raise self.RecordProcessingException(
                "ERROR while processing row #%d of file '%s': %s" \
                    % (_index, os.path.basename(self._file_path), str(exc)))


class AccountsCSV(SimpleCSVFeedProcessor):
    FILE_INDEX = "accounts_file_name"
    LOAD_THIS_INDEX = "load_accounts"

    account_col = "Account"
    date_col = "Date"
    currency_col = "AccountCurrency"
    margin_col = "MarginForTrading"

    _required_columns = [account_col, date_col, currency_col, margin_col]

    def __init__(self, file_path):
        super(AccountsCSV, self).__init__(file_path, do_logging=False)
        self._dict_reader_kwargs = {'delimiter':DEFAULT_DELIMITER}
        self.accounts_dict = defaultdict(defaultdict)

    def _process_record(self, record, dry_run):
        (_, record_data) = record

        alias = get_account_alias(record_data[self.account_col])
        if not alias:
            # print "\t '%s' account skipped." %record_data[self.account_col]
            return
        curr = record_data[self.currency_col]
        margin = float(record_data[self.margin_col])
        self.accounts_dict[alias][curr] = margin

        LOGGER.info("\t %s margin: %f [%s]", alias, margin, curr)

    def get_fund_curr_margin_dict(self):
        return self.accounts_dict

    @staticmethod
    def get_accounts_from_file(accounts_file_path):
        accounts_proc = AccountsCSV(accounts_file_path)
        accounts_proc.add_error_notifier(notify_log)
        accounts_proc.process(False)
        fund_dict = accounts_proc.get_fund_curr_margin_dict()
        return fund_dict



ael_variables = AelVariableHandler()
ael_variables.add("date",
                  label="Date",
                  cls="string",
                  default="PrevNonWeekendDay",
                  collection=DATE_KEYS,
                  hook=enable_custom_start_date,
                  mandatory=True,
                  alt=("A date for which files will be taken. "
                       "Used for {DATE} template."))
ael_variables.add("custom_date",
                  label="Custom Date",
                  cls="string",
                  default=TODAY,
                  enabled=False,
                  alt=("A date for which files will be taken. "
                       "Used for {DATE} template. "
                       "Format: '2016-09-30'."))
ael_variables.add("trade_date",
                  label="Trades Date",
                  cls="date",
                  default="",
                  mandatory=False,
                  alt=("If set, this date will be used for trades value dates "
                       "and instruments prices."
                       "If empty, dates from report will be used. "
                       "Use only in special cases - very rarely. "
                       "Format: '2016-09-30'"))
ael_variables.add("file_dir",
                  label="Directory",
                  default=r"c:\DEV\Perforce\bahouneo\InternationalFutures\Input files\${DATE}",
                  alt=("A Directory template with all input files. "
                       "It can contain the variable DATE (\"$DATE\") "
                       "which will be replaced by the today's date (format YYYY-MM-DD)"))
ael_variables.add(FutTradesExecCSV.FILE_INDEX,
                  label="FUT Trades Executed filename",
                  default="FuturesTradesExecuted_${DATE}.csv",
                  alt=("A path template to the trades executed input file. "
                       "It can contain the variable DATE (\"$DATE\") "
                       "which will be replaced by the today's date (format DD-MM-YYYY)"))
ael_variables.add(CFDTradesExecCSV.FILE_INDEX,
                  label="CFD Trades Executed filename",
                  default="CFDTradesExecuted_${DATE}.csv",
                  alt=("A path template to the trades executed input file. "
                       "It can contain the variable DATE (\"$DATE\") "
                       "which will be replaced by the today's date (format DD-MM-YYYY)"))
ael_variables.add(ETOTradesExecCSV.FILE_INDEX,
                  label="ETO Trades Executed filename",
                  default="ETOTradesExecuted_${DATE}.csv",
                  alt=("A path template to the trades executed ETO input file. "
                       "It can contain the variable DATE (\"$DATE\") "
                       "which will be replaced by the today's date (format DD-MM-YYYY)"))
ael_variables.add(ShareTradesExecCSV.FILE_INDEX,
                  label="STO Trades Executed filename",
                  default="ShareTradesExecuted_${DATE}.csv",
                  alt=("A path template to the trades executed Share input file. "
                       "It can contain the variable DATE (\"$DATE\") "
                       "which will be replaced by the today's date (format DD-MM-YYYY)"))
ael_variables.add(FXTradesExecCSV.FILE_INDEX,
                  label="FX Trades Executed filename",
                  default="FXTradesExecuted_${DATE}.csv",
                  alt=("A path template to the trades executed FX input file. "
                       "It can contain the variable DATE (\"$DATE\") "
                       "which will be replaced by the today's date (format DD-MM-YYYY)"))
ael_variables.add(FXOptionTradesExecCSV.FILE_INDEX,
                  label="FXO Trades Executed filename",
                  default="FXOptionTradesExecuted_${DATE}.csv",
                  alt=("A path template to the trades executed FXO input file. "
                       "It can contain the variable DATE (\"$DATE\") "
                       "which will be replaced by the today's date (format DD-MM-YYYY)"))
ael_variables.add(PricesCSV.FILE_INDEX,
                  label="EOD prices filename",
                  default="FuturesOpenPositions_${DATE}.csv",
                  alt=("A path template to the instrument prices input file. "
                       "It can contain the variable DATE (\"$DATE\") "
                       "which will be replaced by the today's date (format DD-MM-YYYY)"))

ael_variables.add(FutTradesExecCSV.LOAD_THIS_INDEX,
                  label="Load FUT Trades Executed File?",
                  cls="bool",
                  collection=(True, False),
                  default=False)
ael_variables.add(CFDTradesExecCSV.LOAD_THIS_INDEX,
                  label="Load CFD Trades Executed File?",
                  cls="bool",
                  collection=(True, False),
                  default=False)
ael_variables.add(ETOTradesExecCSV.LOAD_THIS_INDEX,
                  label="Load ETO Trades Executed File?",
                  cls="bool",
                  collection=(True, False),
                  default=False)
ael_variables.add(ShareTradesExecCSV.LOAD_THIS_INDEX,
                  label="Load STO Trades Executed File?",
                  cls="bool",
                  collection=(True, False),
                  default=False)
ael_variables.add(FXTradesExecCSV.LOAD_THIS_INDEX,
                  label="Load FX Trades Executed File?",
                  cls="bool",
                  collection=(True, False),
                  default=False)
ael_variables.add(FXOptionTradesExecCSV.LOAD_THIS_INDEX,
                  label="Load FXO Trades Executed File?",
                  cls="bool",
                  collection=(True, False),
                  default=False)
ael_variables.add(PricesCSV.LOAD_THIS_INDEX,
                  label="Load EOD Prices File?",
                  cls="bool",
                  collection=(True, False),
                  default=False,
                  alt=("Load prices from instrument prices file."))


# ##################################
# SETTINGS TAB
ael_variables.add("csv_delimiter",
                  label="CSV Delimiter (default=;)_Settings",
                  cls="string",
                  default=DEFAULT_DELIMITER,
                  mandatory=False,
                  alt=("A delimiter character used in input csv file. "
                    "Comma (',') will be used as default if field is left empty."))
ael_variables.add("set_today_spot",
                  label="Set Todays SPOT_Settings",
                  default=SET_TODAY_SPOT,
                  cls="bool",
                  collection=(True, False),
                  alt="Set price also as today's SPOT price?")
ael_variables.add("update_instr",
                  label="Update instruments?_Settings",
                  default=False,
                  cls="bool",
                  collection=(True, False),
                  alt="Update instruments during the run? "
                      "Only applicable for TradesExecuted runs.")


# ##################################
# INSTRUMENTS_FILE TAB

fileFilter = "*.xlsx|Excel|*.*|All"
inputFile = FRunScriptGUI.InputFileSelection(FileFilter=fileFilter)
inputFile.SelectedFile(r"c:\DEV\Perforce\FA\features\ABITFA-4413 - Saxo - underlying instruments amendment.br\Input\Instrument List.xlsx")

ael_variables.add('file_instr_list',
                  label="Instrument List file_Instrument File",
                  cls="FFileSelection",
                  default=inputFile,
                  multiple=True,
                  alt=("Excel file with instruments grouped into sheets based on their asset class."))
ael_variables.add('sheets_equity',
                  label="Equity sheets_Instrument File",
                  cls="int",
                  default=",".join(InstrumentList.SHEETS_EQUITY),
                  multiple=True,
                  alt=("Indices of equity sheets in the input excel file (indexed from 0)."))
ael_variables.add('sheets_comm',
                  label="Commodity sheets_Instrument File",
                  cls="int",
                  default=",".join(InstrumentList.SHEETS_COMMODITY),
                  multiple=True,
                  alt=("Indices of commodity sheets in the input excel file (indexed from 0)."))
ael_variables.add('sheets_eqindex',
                  label="Eq Index sheets_Instrument File",
                  cls="int",
                  default=",".join(InstrumentList.SHEETS_EQUITYINDEX),
                  multiple=True,
                  alt=("Indices of equity index sheets in the input excel file (indexed from 0)."))


# ##################################
# EMAIL TAB
ael_variables.add("send_mail",
                  label="Send Mails?_Email",
                  default=False,
                  cls="bool",
                  collection=(True, False),
                  alt="Should errors be sent via email?")
ael_variables.add("email_recipients",
                  label="Recipients_Email",
                  default="PrimeServicesTS@absacapital.com,CIBAfricaTSDevPrime@internal.barclayscapital.com",
                  multiple=True,
                  alt="Email destinations. Use comma seperated email addresses \
                       if you want to send report to multiple users.")

def load_instrumentlist(ael_dict):
    if not ael_dict[CFDTradesExecCSV.LOAD_THIS_INDEX]:
        return None

    file_instrs = str(ael_dict['file_instr_list'])
    sheets_equity = ael_dict['sheets_equity']
    sheets_comm = ael_dict['sheets_comm']
    sheets_eqindex = ael_dict['sheets_eqindex']

    equities = AssetClass("Saxo_equity", sheets_equity)
    commodities = AssetClass("Saxo_commodity", sheets_comm)
    eqindices = AssetClass("Saxo_equityindex", sheets_eqindex)

    inslist = InstrumentList(file_instrs, [equities, commodities, eqindices])
    return inslist


def load_sectors(ael_dict):

    file_instrs = str(ael_dict['file_instr_list'])
    sectors = SectorList.read_sectors(file_instrs, SectorList.SECTOR_SHEET_NAME)
    return sectors


def get_input_date(ael_dict):
    # date in string
    if ael_dict['date'] == 'Custom Date':
        the_date = ael_dict['custom_date']
    else:
        the_date = DATE_LIST[ael_dict['date']]
    return the_date


def get_file_path(ael_dict, file_class):

    the_date = get_input_date(ael_dict)

    # file date will be converted to "dd-mm-YYYY"
    # directory date will be converted to "YYYY-mm-dd"
    _dt = datetime.datetime.strptime(the_date, "%Y-%m-%d")
    file_date_string = _dt.strftime("%d-%m-%Y")
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
            LOGGER.info("Loading file: '%s'", file_path)
            return file_path


def ael_main(ael_dict):
    dry_run = False
    InputProperties.reset()

    for_date = get_input_date(ael_dict)

    LOGGER.info("Uploading Saxo files for date '%s'...", for_date)

    global TRADE_DATE
    if ael_dict['trade_date']:
        TRADE_DATE = ael_dict['trade_date'].to_string("%Y-%m-%d")
    else:
        TRADE_DATE = None

    global DELIMITER
    DELIMITER = DEFAULT_DELIMITER
    if ael_dict['csv_delimiter']:
        DELIMITER = ael_dict['csv_delimiter']

    global SET_TODAY_SPOT
    SET_TODAY_SPOT = ael_dict['set_today_spot']

    global UPDATE_INSTR
    UPDATE_INSTR = ael_dict["update_instr"]

    SECTORS_DEPENDENTS = (FutTradesExecCSV, ETOTradesExecCSV)
    INSLIST_DEPENDENTS = (CFDTradesExecCSV,)
    INDEPENDENTS = (ShareTradesExecCSV,
                    FXTradesExecCSV,
                    FXOptionTradesExecCSV,
                    PricesCSV)  # prices has to be loaded as very last thing

    try:
        sectors_dict = None
        inslist = None
        for sector_dep_cls in SECTORS_DEPENDENTS:
            file_path = get_file_object(ael_dict, sector_dep_cls)
            if file_path:
                if not sectors_dict:
                    sectors_dict = load_sectors(ael_dict)
                proc = sector_dep_cls(file_path, sectors_dict)
                proc.add_error_notifier(notify_log)
                proc.add_error_notifier(InputProperties.add_error)
                proc.process(dry_run)

        for inslist_dep_cls in INSLIST_DEPENDENTS:
            file_path = get_file_object(ael_dict, inslist_dep_cls)
            if file_path:
                if not inslist:
                    inslist = load_instrumentlist(ael_dict)
                proc = inslist_dep_cls(file_path, inslist)
                proc.add_error_notifier(notify_log)
                proc.add_error_notifier(InputProperties.add_error)
                proc.process(dry_run)

        for indep_cls in INDEPENDENTS:
            file_path = get_file_object(ael_dict, indep_cls)
            if file_path:
                proc = indep_cls(file_path)
                proc.add_error_notifier(notify_log)
                proc.add_error_notifier(InputProperties.add_error)
                proc.process(dry_run)


    except MissingFileException as exc:
        msg = "Missing file: '%s'." % str(exc)
        LOGGER.error(msg)

        if ael_dict["send_mail"]:
            subj = "Saso files: missing files"
            recipients = ael_dict['email_recipients']
            body = """This is an automated message.
            <BR><BR>
            Task for uploading Saxo trades could not run due to missing Saxo files.
            <BR><BR>
            Please, copy files and rerun the task <b>manually</b>.
            <BR><BR>
            <b>%(error)s</b>
            <BR><BR>
            Thank you.
            <BR><BR>
            Best regards,
            Prime and Equities
            """ % {'error':msg}
            send_mail(subj, body, list(recipients))
        raise RuntimeError(msg)
    except Exception as exc:
        msg = "Upload of files failed: '%s'" % str(exc)
        LOGGER.error(msg)

        if ael_dict["send_mail"]:
            subj = "Saxo files: upload error"
            recipients = ael_dict['email_recipients']
            body = """This is an automated message.
            <BR><BR>
            Task for uploading Saxo trades into FA failed.
            <BR><BR>
            Error details: <b>%(error)s</b>
            <BR><BR>
            Please, correct files and rerun the task <b>manually</b>.
            <BR><BR>
            Thank you.
            <BR><BR>
            Best regards,
            Prime and Equities
            """ % {'error':str(exc)}
            send_mail(subj, body, list(recipients))
        raise

    if InputProperties.has_errors():
        LOGGER.error("Saxo files are in incorrect format or contain invalid data.")
        errors = "<BR>".join(map(str, InputProperties.get_errors()))
        # send email
        if ael_dict["send_mail"]:
            subj = "Saxo files: upload error"
            recipients = ael_dict['email_recipients']
            body = """This is an automated message.
            <BR><BR>
            Task for uploading Saxo trades into FA failed.
            <BR><BR>
            Errors:<BR><b>
            %(errors)s
            </b><BR><BR>
            Please, correct files and rerun the task <b>manually</b>.
            <BR><BR>
            Thank you.
            <BR><BR>
            Best regards,
            Prime and Equities
            """ % {'errors':errors}
            send_mail(subj, body, list(recipients))
        raise RuntimeError("ERROR while files upload.")

    if InputProperties.has_warnings():
        LOGGER.warning("Warnings occurred (%d)", len(InputProperties.WARNINGS))


    LOGGER.info("Completed successfully.")
