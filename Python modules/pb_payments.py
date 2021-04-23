'''
Created on 10 Feb 2016

@author: conicova
https://confluence.barcapint.com/display/ABCAPFA/Off+tree+fees
'''
import acm, ael

from PS_Functions import (get_pb_fund_counterparties, get_pb_fund_counterparty, get_pb_fund_shortname, get_pb_reporting_portfolio)
import at_addInfo
import PS_Functions
from PS_Functions import EXCEPTION_MAP
from at_ael_variables import AelVariableHandler
from PS_FormUtils import DateField
from at_time import acm_date

from at_logging import getLogger, bp_start
from ael import Portfolio

LOGGER = getLogger(__name__)

import logging
LOGGER.setLevel(logging.DEBUG)

DEBUG = False
DEBUG_CLIENTS = ['MAP109', 'OAKHAVEN', 'MAP501', 'SIMHFAMS', 'SEFI', 'CORONATION', 'MAP290']  # 'MROC'
CREATE_TRADES = True  # Set to true if the script is allowed to create trades for the payments

GENERATE_PAYMENTS = False
CREATE_MISSING_TRADES = False
DRY_RUN = True

PB_PCG_EXEC_FEE_TRADE = ""
HAS_NO_FINANCING_PORTFOLIO = ['SLMSEC']

CURRENCY = acm.FCurrency['ZAR']
TODAY = ael.date_today()  # acm.Time.DateToday()

context = acm.GetDefaultContext()
calc_space = acm.Calculations().CreateCalculationSpace(context, 'FPortfolioSheet')

def is_closed(short_name):
    # TODO
    if short_name in ['TOWELS', 'VALISTABLE']:
        return True

    return False

class MissingPortfolio(Exception):
    pass

class AddInfoPayType(object):

    TRD_TYPE_ANY = 0
    TRD_TYPE_FEE = 1
    TRD_TYPE_FINANCING = 2

    def __init__(self, add_info_name, trade_type):
        self.add_info_name = add_info_name
        self.trade_type = trade_type

    def _set_trade(self, short_name, trdnbr):
        portfolio = _get_off_tree_portfolio(short_name)
        try:
            if not DRY_RUN:
                if trdnbr < 1:
                    raise Exception("Something went wrong. The trade number should not be negative.")
                at_addInfo.save(portfolio, self.add_info_name, trdnbr)
            LOGGER.info("Additional info '%s' on portfolio '%s' is set to '%s'. (dry run: '%s')",
                        self.add_info_name, portfolio.Name(), trdnbr, DRY_RUN)
        except Exception:
            LOGGER.exception("Failed to set the additional info '%s' on portfolio '%s'. (dry run: '%s')",
                             self.add_info_name, portfolio.Name(), DRY_RUN)

    def get_trade(self, short_name):
        """ Returns the Cash Payment (Curr) trade. Creates it if necessary. """
        portfolio = _get_off_tree_portfolio(short_name)
        trade = at_addInfo.get_value(portfolio, self.add_info_name)

        if not trade:
            trade = self._book_trade(short_name)
            self._set_trade(short_name, trade.Oid())

        return trade

    def _book_trade(self, short_name):
        if not CREATE_MISSING_TRADES:
            LOGGER.warning("The script is not allowed to create new trades.")
            raise Exception("Could not create the trade (not allowed).")
        LOGGER.info("Creating trade: %s", short_name)
        counterparty = get_pb_fund_counterparty(short_name)
        portfolio = _get_on_tree_portfolio(short_name)
        acquirer = acm.FParty['PRIME SERVICES DESK']

        newTrade = acm.FTrade()
        newTrade.Instrument(acm.FInstrument['ZAR'])
        newTrade.Portfolio(portfolio)
        newTrade.Acquirer(acquirer)
        newTrade.Counterparty(counterparty)
        newTrade.ValueDay(TODAY)
        newTrade.AcquireDay(TODAY)
        newTrade.TradeTime(TODAY)
        newTrade.Currency(CURRENCY)
        newTrade.Status('FO Confirmed')
        ins_ovveride = None
        if self.trade_type == AddInfoPayType.TRD_TYPE_FEE:
            ins_ovveride = 'Execution Fee'
        if self.trade_type == AddInfoPayType.TRD_TYPE_FINANCING:
            ins_ovveride = 'Financing Fee'
        newTrade.RegisterInStorage()
        newTrade.AdditionalInfo().InsOverride(ins_ovveride)

        if not DRY_RUN:
            newTrade.Commit()

        LOGGER.info("Trade '%s' created (dry run: %s), %s", newTrade.Oid(), DRY_RUN, short_name)

        return newTrade

    @staticmethod
    def get_add_info_def(trade_types):
        return filter(lambda item:item.trade_type in trade_types, ADD_INFO_DEF.itervalues())

    def get_payments_by_day(self, short_name, payment_info):
        """Return the list of all payments filtered by payment type and with a pay day equal to payment_info pay day"""
        trade = self.get_trade(short_name)
        payments = filter (lambda item:item.Type() == payment_info.payment_type and item.PayDay() == payment_info.pay_day, trade.Payments())

        return payments

    def get_all_payments(self, short_name, payment_info):
        """Return the list of all payments filtered by payment type and with a pay day before or equal to payment_info pay day"""
        trade = self.get_trade(short_name)
        payments = filter (lambda item:item.Type() == payment_info.payment_type and item.PayDay() <= payment_info.pay_day, trade.Payments())

        return payments

    def __str__(self, *args, **kwargs):
        return "Name {0}, Type {1}".format(self.add_info_name, self.trade_type)

ADD_INFO_DEF = {"SAFEXTotFeeTrd":AddInfoPayType("SAFEXTotFeeTrd", AddInfoPayType.TRD_TYPE_FEE),
                "PCGExFeeExchTrd":AddInfoPayType("PCGExFeeExchTrd", AddInfoPayType.TRD_TYPE_FEE),
                "PCGFundingTrd":AddInfoPayType("PCGFundingTrd", AddInfoPayType.TRD_TYPE_FINANCING)
                }

class PaymentInfo(object):

    SINCE_INCEPTION = "SinceInception"  # The sum of all payments until date is the value since inception
    DAILY = "Daily"  # The sum of all payments for the specified date is the value since inception

    DEFAULT_PAYMENT_TYPE = "SAFEX Fees"
    PAYMENT_TYPE_CASH = "Cash"
    PAYMENT_TYPE_EXECUTION_FEES = "Execution Fee"
    PAYMENT_TYPE_BROKER_FEE = "Broker Fee"

    def __init__(self, amount, add_info_pay_type, pay_day=TODAY,
                 payment_type=DEFAULT_PAYMENT_TYPE, val_type=SINCE_INCEPTION, text=""):
        self.amount = amount
        self.add_info_pay_type = add_info_pay_type
        self.pay_day = pay_day
        self.payment_type = payment_type
        self.val_type = val_type
        self.text = text

    def get_key(self):
        return "{0}||{1}||{2}||{3}".format(self.add_info_pay_type.add_info_name,
                                           self.payment_type, self.pay_day, self.val_type)

    def _add_payment(self, trade, payment_amount, short_name):
        if not GENERATE_PAYMENTS:
            LOGGER.warning("The script is not allowed to create new payments. (%s)", short_name)
            raise Exception("Could not create the payment (not allowed).")

        try:
            payment = acm.FPayment()
            payment.Trade = trade.Oid()
            payment.Type = self.payment_type
            payment.Amount = payment_amount
            payment.Currency = trade.Currency()
            payment.ValidFrom = self.pay_day
            payment.PayDay = self.pay_day
            payment.Party = trade.Counterparty()
            payment.Text = self.text

            LOGGER.info("Creating payment")
            if not DRY_RUN:
                payment.Commit()
            LOGGER.info("Payment created")
            LOGGER.info(trade.Oid())
            LOGGER.info(payment.Amount())
            LOGGER.info(payment.Type())
            LOGGER.info("Payment created: trade %s, amount %s, type %s. (dry run: %s) (%s)",
                        trade.Oid(), payment.Amount(), payment.Type(), DRY_RUN, short_name)
        except Exception:
            LOGGER.exception("Failed to create payment. (%s)", short_name)
            raise

    @staticmethod
    def delete_all_payments(add_info_pay_type, short_name):
        trade = add_info_pay_type.get_trade(short_name)
        payments = map(lambda payment: payment.Oid(), trade.Payments())
        for oid in payments:
            acm.FPayment[oid].Delete()

    def _get_total_amount_by_day(self, short_name):
        existing_payments = self.add_info_pay_type.get_payments_by_day(short_name, self)
        total_amount = sum(map(lambda item: item.Amount(), existing_payments))

        return total_amount

    def _get_total_amount(self, short_name):
        existing_payments = self.add_info_pay_type.get_all_payments(short_name, self)
        total_amount = sum(map(lambda item: item.Amount(), existing_payments))

        return total_amount

    def add_payment(self, short_name):
        trade = self.add_info_pay_type.get_trade(short_name)


        total_amount_daily = self._get_total_amount_by_day(short_name)
        if self.val_type == PaymentInfo.DAILY:
            total_amount = total_amount_daily
        else:
            total_amount = self._get_total_amount(short_name)
        LOGGER.info("Adding payment (%s) on trade '%s'. Total Amount %s, ('%s')", self, trade.Oid(), total_amount, short_name)
        new_payment_amount = self.amount - total_amount

        if total_amount_daily != 0:
            LOGGER.info("Payments already exist '%s'. Posting '%s'. (%s)", total_amount_daily, new_payment_amount, short_name)

        self._add_payment(trade, new_payment_amount, short_name)

    def __str__(self, *args, **kwargs):
        return "Amount {0}, PaymentType {1}, PayDay {2}, ValType {3}, AddInfo ({4}), Text ({5})".format(self.amount,
                                                                                          self.payment_type,
                                                                                          self.pay_day,
                                                                                          self.val_type,
                                                                                          self.add_info_pay_type,
                                                                                          self.text)

def _get_on_tree_portfolio(short_name):
    if short_name in EXCEPTION_MAP.keys():
        short_name = EXCEPTION_MAP[short_name]

    portfolio_name = "PB_FINANCING_{0}".format(short_name)
    portfolio = acm.FPhysicalPortfolio[portfolio_name]
    if not portfolio:
        raise MissingPortfolio("Could not find the portfolio '{0}'".format(portfolio_name))

    return portfolio

def _get_off_tree_portfolio(short_name):
    counterparty = get_pb_fund_counterparty(short_name)
    portfolio = get_pb_reporting_portfolio(counterparty)  # PB_client_CR
    if not portfolio:
        raise Exception("Could not find the portfolio for counterparty '{0}'".format(short_name))

    return portfolio

def _calc_value(entity, column_name):
    LOGGER.info("Computing '%s'", column_name)
    value = 0.0
    try:
        value = float(calc_space.CalculateValue(entity, column_name))
    except Exception:
        LOGGER.info("Column '%s' returned an invalid value, returning 0.0 instead", column_name)
    return value

def _get_off_tree_payments(entity, category, date):
    payments_info = []

    if category == AddInfoPayType.TRD_TYPE_FINANCING:
        amount = -1.0 * _calc_value(entity, "Since Inception Funding")
        new_pay = PaymentInfo(amount, ADD_INFO_DEF["PCGFundingTrd"],
                              date, PaymentInfo.PAYMENT_TYPE_CASH,
                              PaymentInfo.SINCE_INCEPTION)
        payments_info.append(new_pay)
        LOGGER.debug("%s", new_pay)

    if category == AddInfoPayType.TRD_TYPE_FEE:
        safex_fee_incl_vat = _calc_value(entity, "SAFEX Total Fee Incl VAT")
        safex_fee_excl_vat = _calc_value(entity, "SAFEX Total Fee Excl VAT")
        new_pay = PaymentInfo(safex_fee_excl_vat, ADD_INFO_DEF["SAFEXTotFeeTrd"],
                              date, PaymentInfo.PAYMENT_TYPE_CASH,
                              PaymentInfo.SINCE_INCEPTION,
                              text="SAFEX Total Fee")
        payments_info.append(new_pay)
        LOGGER.debug("%s", new_pay)
        new_pay = PaymentInfo(safex_fee_incl_vat - safex_fee_excl_vat,
                              ADD_INFO_DEF["SAFEXTotFeeTrd"],
                              date, PaymentInfo.PAYMENT_TYPE_CASH,
                              PaymentInfo.SINCE_INCEPTION,
                              text="VAT")
        payments_info.append(new_pay)
        LOGGER.debug("%s", new_pay)

        amount = _calc_value(entity, "Internal Date Range Execution Fee")
        new_pay = PaymentInfo(amount, ADD_INFO_DEF["PCGExFeeExchTrd"],
                              date, PaymentInfo.PAYMENT_TYPE_EXECUTION_FEES,
                              PaymentInfo.SINCE_INCEPTION,
                              text="Execution Fee")
        payments_info.append(new_pay)
        LOGGER.debug("%s", new_pay)

    if category == AddInfoPayType.TRD_TYPE_ANY:
        pass

    return payments_info

def _get_fees_qfs(short_name):
    portfolio = _get_off_tree_portfolio(short_name)
    qfs = []
    qf_names = ['SAFEX exchange', 'YieldX exchange', 'PB_OFF_TREE_FEES']

    portfolios = [portfolio]
    if portfolio.Name() == "PB_OAKHAVEN_NEW_CR":
        portfolios.append(acm.FPhysicalPortfolio["PB_OAKHAVEN_OLD_CR"])
    if short_name == "MATRIXZAR":
        # Once upon a time there was a once off 34200 booked on this portfolio as execution on MatrixZar.
        portfolios.append(acm.FPhysicalPortfolio["PB_MONEYMARKET_FF_MATRIXZAR_CR"])

    for qf_name in qf_names:
        for portfolio in portfolios:
            LOGGER.info("Preparing fee QF '%s' for portfolio %s, (%s)", qf_name, portfolio.Name(), short_name)
            query_folder = acm.FStoredASQLQuery[qf_name]
            query = query_folder.Query()
            query = PS_Functions.modify_asql_query(
                query,
                "Portfolio.Name",
                False,
                new_value=portfolio.Name())

            qf_clone = query_folder.Clone()
            qf_clone.Query(query)
            qfs.append((qf_name, qf_clone, portfolio.Name()))

    return qfs

def _get_financing_qfs(short_name):
    portfolio = _get_off_tree_portfolio(short_name)
    qfs = []
    qf_names = ['PB_OFF_TREE_FINANCING']

    portfolios = [portfolio]
    if portfolio.Name() == "PB_OAKHAVEN_NEW_CR":
        portfolios.append(acm.FPhysicalPortfolio["PB_OAKHAVEN_OLD_CR"])

    for qf_name in qf_names:
        for portfolio in portfolios:
            LOGGER.info("Preparing financing QF '%s' for portfolio %s, (%s)", qf_name, portfolio.Name(), short_name)
            query_folder = acm.FStoredASQLQuery[qf_name]
            query = query_folder.Query()
            query = PS_Functions.modify_asql_query(
                query,
                "Portfolio.Name",
                False,
                new_value=portfolio.Name())

            qf_clone = query_folder.Clone()
            qf_clone.Query(query)
            qfs.append((qf_name, qf_clone, portfolio.Name()))

    return qfs

def _get_payments_by_qf(short_name, qfs, category, date):
    payments = []
    for qf_name, qf, pf_name in qfs:
        LOGGER.info("QF %s, PF: %s: number of trades %s, (%s)", qf_name, pf_name, len(qf.Query().Select()), short_name)
        # log("QF: {0}".format(qf.Query()), False)
        payments_exchnage = _get_off_tree_payments(qf, category, date)
        payments.extend(payments_exchnage)
        payments_any = _get_off_tree_payments(qf, AddInfoPayType.TRD_TYPE_ANY, date)
        payments.extend(payments_any)

    return payments

def _set_payments_by_qf(short_name, date):

    payments = []
    LOGGER.info("Processing 'fees' trades (%s)", short_name)
    payments.extend(_get_payments_by_qf(short_name, _get_fees_qfs(short_name), AddInfoPayType.TRD_TYPE_FEE, date))
    LOGGER.info("Processing 'financing' trades (%s)", short_name)
    payments.extend(_get_payments_by_qf(short_name, _get_financing_qfs(short_name), AddInfoPayType.TRD_TYPE_FINANCING, date))

    LOGGER.info("Aggregating payments(%s)", short_name)
    final_payments = {}
    for payment in payments:
        key = payment.get_key()
        if not final_payments.has_key(key):
            final_payments[key] = PaymentInfo(0, payment.add_info_pay_type, payment.pay_day, payment.payment_type,
                                              payment.val_type, payment.text)
        LOGGER.debug("Payment: %s, amount %s", key, payment.amount)
        final_payments[key].amount += payment.amount

    LOGGER.info("Saving payments(%s)", short_name)
    for payment in final_payments.itervalues():
        payment.add_payment(short_name)

START_DATES = DateField.get_captions([
    'Inception',
    'First Of Year',
    'First Of Month',
    'Last of Previous Month',
    'TwoBusinessDaysAgo',
    'PrevBusDay',
    'Now',
    'Custom Date'])

END_DATES = DateField.get_captions([
    'Now',
    'PrevBusDay',
    'Custom Date'])

def custom_start_date_hook(selected_variable):
    """Enable/Disable Custom Start Date base on Start Date value."""
    start_date = ael_variables.get('start_date')
    start_date_custom = ael_variables.get('start_date_custom')

    if start_date.value == 'Custom Date':
        start_date_custom.enabled = True
    else:
        start_date_custom.enabled = False

def custom_end_date_hook(selected_variable):
    """Enable/Disable Custom End Date base on End Date value."""
    end_date = ael_variables.get('end_date')
    end_date_custom = ael_variables.get('end_date_custom')

    if end_date.value == 'Custom Date':
        end_date_custom.enabled = True
    else:
        end_date_custom.enabled = False

def _get_cp_short_names():
    cp_short_names = map(lambda cp: get_pb_fund_shortname(cp), get_pb_fund_counterparties())
    cp_short_names.sort()

    return cp_short_names

ael_variables = AelVariableHandler()
ael_variables.add('start_date',
                  label='Start Date (relative to End Date)',
                  default='PrevBusDay',
                  collection=START_DATES,
                  alt='Start date'
                      '(relative to the end date)',
                  hook=custom_start_date_hook)

ael_variables.add('start_date_custom',
                  label='Start Date Custom',
                  default=DateField.read_date('TwoBusinessDaysAgo'),
                  alt='Custom start date',
                  enabled=False)

ael_variables.add('end_date',
                  label='End Date',
                  default='PrevBusDay',
                  collection=END_DATES,
                  alt='End date',
                  hook=custom_end_date_hook)

ael_variables.add('end_date_custom',
                  label='End Date Custom',
                  default=DateField.read_date('PrevBusDay'),
                  alt='Custom end date',
                  enabled=False)
cps = ['All']
cps.extend(_get_cp_short_names())
ael_variables.add('counterparty',
                  label="Counterparty",
                  default="All",
                  collection=cps)

ael_variables.add_bool(
    "generate_payments",
    label="Generate payments",
    default=False)
ael_variables.add_bool(
    "create_missing_trades",
    label="Create missing trades",
    default=False)
ael_variables.add_bool(
    "dry_run",
    label="Dry run",
    default=True)

def _work(date, cp_short_name=None):
    calc_space.Clear()
    calc_space.Refresh()
    calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom')
    calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', date)

    to_process = []

    if cp_short_name == None:
        to_process = _get_cp_short_names()
    else:
        to_process = [cp_short_name]

    import threading
    # threads = []
    for short_name in to_process:
        if is_closed(short_name):
            LOGGER.info("Client '%s' is closed. Payments will not be computed.", short_name)
            continue
        if short_name in DEBUG_CLIENTS or not DEBUG:
            LOGGER.info("Processing the client '%s' for date '%s'", short_name, date)
            target = lambda: _set_payments_by_qf(short_name, date)
            try:
                _set_payments_by_qf(short_name, date)
            except MissingPortfolio:
                if short_name not in HAS_NO_FINANCING_PORTFOLIO:
                    LOGGER.exception("Failed to set the payments")
            except Exception:
                LOGGER.exception("Failed to set the payments")

#     for thr in threads:
#         if thr.is_alive():
#             try:
#                 thr.join()
#             except Exception:
#                 LOGGER.exception("Failed to join the threads")
#         LOGGER.info("%s has finished", thr.name)

def _create_trades(cp_short_name):
    counterparties = []
    if cp_short_name:
        counterparties.append(cp_short_name)
    else:
        counterparties = _get_cp_short_names()
    for short_name in counterparties:
        if is_closed(short_name):
            LOGGER.info("Client '%s' is closed. Trades will not be created.", short_name)
            continue

        if short_name in DEBUG_CLIENTS or not DEBUG:
            try:
                for add_info_pay_type in ADD_INFO_DEF.itervalues():
                    add_info_pay_type.get_trade(short_name)
            except MissingPortfolio:
                if short_name not in HAS_NO_FINANCING_PORTFOLIO:
                    LOGGER.exception("Failed to set the payments")
            except Exception:
                LOGGER.exception("Could not get the trade")

def ael_main(config):
    global GENERATE_PAYMENTS
    global CREATE_MISSING_TRADES
    global DRY_RUN

    cp_short_name = config['counterparty']
    if cp_short_name == 'All':
        cp_short_name = None

    process_name = "ps.payments.all"
    if cp_short_name:
        process_name = "ps.payments.{0}".format(cp_short_name)

    with bp_start(process_name, ael_main_args=config):
        if config['end_date'] == 'Custom Date':
            end_date = acm_date(config['end_date_custom'])
        else:
            end_date = DateField.read_date(config['end_date'])

        if config['start_date'] == 'Custom Date':
            start_date = acm_date(config['start_date_custom'])
        else:
            start_date = DateField.read_date(config['start_date'], end_date)

        if  start_date > end_date:
            LOGGER.error("Error: The start date ('%s') cannot be bigger than end date ('%s')", start_date, end_date)
            return

        GENERATE_PAYMENTS = config['generate_payments']
        CREATE_MISSING_TRADES = config['create_missing_trades']
        DRY_RUN = config['dry_run']

        if CREATE_MISSING_TRADES:
            _create_trades(cp_short_name)

        if GENERATE_PAYMENTS:
            while start_date <= end_date:
                _work(start_date, cp_short_name)
                start_date = acm.Time().DateAddDelta(start_date, 0, 0, 1)

        LOGGER.info("Completed Successfully")

def _clean():
    for counterparty in get_pb_fund_counterparties():
        short_name = get_pb_fund_shortname(counterparty)
        if short_name in DEBUG_CLIENTS or not DEBUG:
            LOGGER.info("Processing the client '%s'. Deleting payments.", short_name)
            try:
                for add_info_pay_type in ADD_INFO_DEF.itervalues():
                    PaymentInfo.delete_all_payments(add_info_pay_type, short_name)
            except Exception:
                LOGGER.exception("Something went wrong")

