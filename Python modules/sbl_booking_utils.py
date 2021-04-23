"""
--------------------------------------------------------------------------------------------
MODULE
    sbl_booking_utils

DESCRIPTION
    Date                : 2020-02-26
    Purpose             : Utilities for collateral trade booking, loan and
                          collateral returns and auto bo confirmation
    Department and Desk : SBL and Collateral
    Requester           : Shaun Du Plessis, James Stevens
    Developer           : Sihle Gaxa
    JIRA                : PCGDEV-8

HISTORY
================================================================================================
Date            JIRA no       Developer               Description
------------------------------------------------------------------------------------------------
2020-02-26      PCGDEV-8      Sihle Gaxa              Initial implementation.
2020-08-20      PCGDEV-566    Sihle Gaxa              Updated full returns to same-day returns
2020-10-19      PCGDEV-598    Sihle Gaxa              Addition of loan creator class and methods 
                                                      to assist in SBL ACS dual booking hook
2020-11-10      PCGDEV-617    Sihle Gaxa              Updated trade date to match start date
2020-11-11      FAOPS-959     Ncediso Nkambule        Added cash collateral constants
2020-11-11      FAOPS-878     Faize Adams             Added ETF to COLLATERAL_INSTRUMENTS and 
                                                      SBL_INSTRUMENTS
2020-11-19      PCGDEV-623    Sihle Gaxa              Updated sec loan trade date to always be
                                                      today or before today
2021-02-24      PCGDEV-673    Sihle Gaxa              Added logic to check if loan has 
                                                      already been created
2021-03-01                    Faize Adams             Clear Unique_Strate_ID addinfo when creating
                                                      returns
2021-03-16      FAOPS-982     Ncediso Nkambule        Added functions to handle Cashflow driven events.

ENDDESCRIPTION
-----------------------------------------------------------------------------------------------
"""

import acm
import ael
import FBDPGui
import sl_functions

import FCallDepositFunctions
from at_logging import getLogger
import sl_uploader_from_file as sl_uploader
from at_ael_variables import AelVariableHandler
import FValidation_SecLending_Utils as sec_lending_utils

NCD_ADD_INFO = "NCD"
LOGGER = getLogger(__name__)
TODAY = acm.Time().DateNow()
COLLATERAL_CATEGORY = "Collateral"
CALENDAR = acm.FCalendar["ZAR Johannesburg"]
MARKET = acm.FMTMMarket[1563] # internal market
SWIFT_FLAG = acm.FChoiceList["SL_SWIFT"].Choices()
PREVIOUS_DAY = CALENDAR.AdjustBankingDays(TODAY, -1)
INVALID_STATUS = ["Void", "Simulated", "Terminated"]
ACQUIRER = acm.FParty[32668] # SECURITY LENDINGS DESK
RELEVANT_COUNTERPARTIES = [acm.FParty[42119]] # SBL AGENCY I/DESK
VALID_STATUSES = ["FO Confirmed", "BO Confirmed", "BO-BO Confirmed"]
COLLATERAL_INSTRUMENTS = ["Bond", "IndexLinkedBond", "Stock", "CD", "Bill", "ETF"]
AUTO_BO_LOAN_PORTFOLIO = acm.FCompoundPortfolio[2975] # 7268_Prime Services
SBL_INSTRUMENTS = ["SecurityLoan", "Stock", "Bond", "IndexLinkedBond", "CD", "Bill", "ETF"]
COLLATERAL_PORTFOLIO = acm.FCompoundPortfolio[13923]  # SBL_NONCASH_COLLATERAL portfolio
CASH_COLLATERAL_PORTFOLIO = acm.FPhysicalPortfolio['Call_SBL_Agency_Collateral']
CASH_COLLATERAL_INS_TYPES = ["Deposit"]
CASH_COLLATERAL_ACQUIRER = acm.FParty["PRIME SERVICES DESK"]

RETURN_TYPES = {"FULL": "FULL_RETURN",
                "PARTIAL": "PARTIAL_RETURN"}
RETURN_STATUSES = {"OPEN_END": "Open End",
                   "SIMULATED": "Simulated",
                   "TERMINATED": "Terminated",
                   "FO_CONFIRM": "FO Confirmed",
                   "BO_CONFIRM": "BO Confirmed",
                   "BO-BO_CONFIRM": "BO-BO Confirmed"}
SETTLE_CATEGORY = {"SWIFT": "SL_STRATE",
                   "DOM": "SL_CUSTODIAN"}


class SBLLoanCreator(object):

    def __init__(self, trade, ref_price, start_date, end_date, trade_value):
        self.trade = trade
        self.ref_price = ref_price
        self.start_date = start_date
        self.end_date = end_date
        self.trade_value = trade.FaceValue()
        if trade_value:
            self.trade_value = trade_value
        self.prev_date = CALENDAR.AdjustBankingDays(start_date, -1)

    def create_instrument(self):
        try:
            loan_name = self._get_instrument_name()
            loan_ins = acm.FSecurityLoan()
            loan_ins.RegisterInStorage()
            loan_ins.Name(loan_name)
            loan_ins.Quotation("Clean")
            loan_ins.QuoteType("Clean")
            loan_ins.OpenEnd("Open End")
            loan_ins.StartDate(self.start_date)
            loan_ins.ExpiryDate(self.end_date)
            loan_ins.SpotBankingDaysOffset(1)
            loan_ins.Currency(self.trade.Currency())
            loan_ins.Underlying(self.trade.Instrument())
            self._set_leg_details(loan_ins)
            self._set_ref_value(loan_ins)
            loan_ins.AddInfoValue("SL_CFD", "False")
            loan_ins.AddInfoValue("SL_VAT", "False")
            loan_ins.AddInfoValue("SL_Trading_Capacity", "Principal")
            loan_ins.AddInfoValue("SL_ExternalInternal", "No Collateral")
            loan_ins.Commit()
            return loan_ins
        except Exception as e:
            LOGGER.exception("Could not book security loan because {error}".format(error=str(e)))

    def _get_instrument_name(self):
        instrument = self.trade.Instrument()
        start_date = sl_uploader.MainProcessor()._format_date(self.start_date, format="%y%m%d")
        end_date = sl_uploader.MainProcessor()._format_date(self.end_date, format="%y%m%d")
        name = "ZAR/SELO/{underlying}/{sec_start_date}-{sec_end_date}".format(
                underlying=instrument.Name()[4:],
                sec_start_date=start_date,
                sec_end_date=end_date)
        sec_name = sl_uploader.MainProcessor().sl_construct_name2(name)
        LOGGER.info("Security loan name is {name}".format(name=sec_name))
        return sec_name

    def _set_leg_details(self, loan_ins):
        loan_leg = loan_ins.CreateLeg(True)
        loan_leg.LegType('Fixed')
        loan_leg.EndDate(self.end_date)
        loan_leg.RollingPeriod('1m')
        loan_leg.PayDayMethod('None')
        loan_leg.StartDate(self.start_date)
        loan_leg.DayCountMethod('Act/365')
        loan_leg.PayCalendar('ZAR Johannesburg')
        roll_day = sl_uploader.MainProcessor()._get_roll_base_day(loan_leg.PayCalendar(),
                                            loan_leg.RollingPeriod(), loan_leg.StartDate())
        loan_leg.RollingPeriodBase(roll_day)
        return loan_leg

    def _set_ref_value(self, loan_ins):
        try:
            to_dirty = False
            loan_ins.RefPrice(self.ref_price)
            coll_ins = self.trade.Instrument()
            quotationFactor = loan_ins.Quotation().QuotationFactor()
            calc_space = acm.Calculations().CreateStandardCalculationsSpaceCollection()
            collateral_price = coll_ins.Calculation().PriceToUnitValue(
                                                      calc_space, loan_ins.RefPrice(),
                                                      coll_ins.Quotation(),
                                                      self.start_date, to_dirty)
            all_in_price = round(collateral_price.Number() * 100, 5)
            if loan_ins.RefValue() == 0 and all_in_price != 0.0:
                ref_value = loan_ins.ContractSize() / (all_in_price * quotationFactor)
                loan_ins.RefValue(ref_value)
            return loan_ins
        except Exception as e:
            LOGGER.exception("Could not set ref value {error}".format(error=str(e)))

    def create_trade(self, loan_ins):
        try:
            loan_trade = acm.FTrade()
            loan_trade.RegisterInStorage()
            loan_trade.Instrument(loan_ins)
            loan_trade.Status("FO Confirmed")
            loan_trade.HaircutType("Discount")
            loan_trade.Text2(self.trade.Oid())
            loan_trade.FaceValue(self.trade_value)
            loan_trade.Currency(loan_ins.Currency())
            loan_trade.ValueDay(loan_ins.StartDate())
            loan_trade.Acquirer(self.trade.Acquirer())
            loan_trade.AcquireDay(loan_ins.StartDate())
            loan_trade.TradeTime(self.prev_date)
            if self.prev_date > TODAY:
                loan_trade.TradeTime(TODAY)
            loan_trade.Counterparty(32737) # PRIME SERVICES DESK
            loan_trade.Portfolio(acm.FPhysicalPortfolio[5708])  # Collateral optimize
            loan_trade.MirrorPortfolio(acm.FPhysicalPortfolio[2897])  # SBL LinTradingCFD Loans ACS
            loan_trade.Quantity(self.trade_value/loan_ins.RefValue())
            loan_trade.Commit()
            return loan_trade
        except Exception as e:
            LOGGER.exception("Could not book security loan trade because {error}".format(error=str(e)))


def terminate_trade(parent_trade, return_date, child_trade=None, return_datetime=None):

    LOGGER.info("Terminating parent trade")
    try:
        if parent_trade.Instrument().InsType() == "SecurityLoan":
            parent_instrument = terminate_instrument_leg(parent_trade.Instrument(), return_date)

            if return_datetime:
                parent_trade.AddInfoValue("SL_CustomTradeDate", return_datetime)

            if child_trade:
                connect_trades(parent_trade, child_trade)
        else:
            parent_trade.ConnectedTrade(child_trade)
            parent_trade.Status(RETURN_STATUSES["TERMINATED"])
            parent_trade.Commit()

    except Exception as e:
        raise Exception("Could not terminate parent trade because {error}".format(
                         error=str(e)))

def terminate_instrument_leg(instrument, return_date):

    try:
        parent_leg = instrument.Legs()[0]
        if return_date == parent_leg.StartDate():
            parent_leg.EndDate(return_date)
            parent_leg.Commit()
            for cf in parent_leg.CashFlows():
                cf.Delete()
            instrument.OpenEnd("Terminated")
            instrument.Commit()
        else:
            if return_date < parent_leg.EndDate():
                parent_leg.EndDate(return_date)
                parent_leg.Commit()
            instrument.SLGenerateCashflows()
            instrument = ael.Instrument[instrument.Oid()]
            instrument.terminate_open_end(ael.date(return_date))

        return instrument

    except Exception as e:
        raise Exception("Could not update leg on {parent} because {error}".format(
                        parent=instrument.Name(), error=str(e)))

def connect_trades(parent_trade, child_trade):

    LOGGER.info("Connecting child trade {child} to parent trade {parent}".format(
                child=child_trade.Oid(), parent=parent_trade.Oid()))
    try:
        if parent_trade.Instrument().InsType() == "SecurityLoan":
            parent_trade.ConnectedTrade(child_trade)
            parent_trade.Commit()
            mirror_trade = parent_trade.GetMirrorTrade()
            
            if mirror_trade:
                child_mirror_trade = child_trade.GetMirrorTrade()
                if child_mirror_trade:
                    mirror_trade.ConnectedTrade(child_mirror_trade)
                    mirror_trade.Commit()
        else:
            if child_trade.ContractTrdnbr() != parent_trade.Oid():
                child_trade.ContractTrade(parent_trade)
                child_trade.Commit()

    except Exception as e:
        raise Exception("Could not connect trade {child} to parent trade {parent} because {error}".format(
                child=child_trade.Oid(), parent=parent_trade.Oid(), error=str(e)))


def generate_partial_return(parent_trades, return_date, return_quantity,
                            return_datetime=None, swift_flag=None):

    LOGGER.info("Generating partial return for trade")

    if parent_trades.IsKindOf(acm.FTrade) and parent_trades.Instrument().InsType() == "SecurityLoan":
        child_instrument = create_instrument(parent_trades, return_date)
        child_trade = create_trade(parent_trades, child_instrument, return_quantity,
                      return_date, return_datetime, swift_flag)
        child_trade.Commit()

        child_instrument.SLGenerateCashflows()
        terminate_trade(parent_trades, return_date, child_trade, return_datetime)
    else:
        custody_trade = None
        custody_trades = None
        custody_child_trade = None
        child_trade = create_trade(parent_trades, parent_trades[0].Instrument(),
                      return_quantity, return_date, return_datetime, swift_flag)
        child_trade.Status(RETURN_STATUSES["SIMULATED"])
        child_trade.Commit()

        for trade in parent_trades:
            terminate_trade(trade, return_date, child_trade)
        
        custody_trades = get_custody_trades_list(parent_trades)
 
        if custody_trades:
            custody_trade = custody_trades[0]
            if custody_trade:
                custody_child_trade = create_trade(custody_trades, custody_trade.Instrument(),
                                      -1*return_quantity, return_date, return_datetime, swift_flag)
                custody_child_trade.Status(RETURN_STATUSES["SIMULATED"])
                custody_child_trade.Commit()

                connect_trades(child_trade, custody_child_trade)
                
                for trade in custody_trades:
                    terminate_trade(trade, return_date, custody_child_trade)
                
        child_trade.Status(RETURN_STATUSES["FO_CONFIRM"])
        child_trade.Commit()
        if custody_child_trade:
            custody_child_trade.Status(RETURN_STATUSES["FO_CONFIRM"])
            custody_child_trade.Commit()
    return child_trade


def create_instrument(parent_trade, return_date, close_rate=None):

    LOGGER.info("Creating child instrument from {parent}".format(
                parent=parent_trade.Instrument().Name()))
    try:
        if (sec_lending_utils.user_belongs_to_SBL_operations() and 
            sec_lending_utils.trade_lender_not_allowed(ael.Trade[parent_trade.Oid()])):
            raise Exception("FV120b: Trade in portfolio ACS - Script Lending \
                           does not have SLL ACS Lender. Operation not allowed.")
        parent_instrument = parent_trade.Instrument()
        child_instrument = parent_instrument.Clone()
        new_name = parent_instrument.SuggestName()
        child_instrument.Name(new_name)
        child_instrument.Commit()

        sl_functions.copy_additional_infos(parent_instrument, child_instrument, ["SL_Instruction_Note"])
 
        child_leg = child_instrument.Legs()[0]
        child_leg.StartDate(return_date)
        child_leg.PayDayMethod("None")

        if parent_instrument.OpenEnd() == "Open End":
            set_child_leg_rolling_details(parent_instrument, child_leg, return_date)

        if close_rate == 0.0:
            child_leg.EndDate(return_date)
            child_instrument.Legs()[0].FixedRate(close_rate)
            child_leg.GenerateCashFlows(close_rate)
            child_leg.Commit()
        else:
            fixed_rate = parent_instrument.Legs()[0].FixedRate()
            child_leg.GenerateCashFlows(fixed_rate)
            child_leg.Commit()

        return child_instrument

    except Exception as e:
        raise Exception("Child instrument was not correctly created because {error}".format(error=str(e)))


def set_child_leg_rolling_details(parent_instrument, child_leg, return_date):

    LOGGER.info("Adding leg details to child instrument {child}".format(
                child=child_leg.Instrument().Name()))
    try:
        tomorrow = CALENDAR.AdjustBankingDays(TODAY, 1)
        end_day = max(tomorrow, CALENDAR.AdjustBankingDays(return_date, 1))

        if parent_instrument.AdditionalInfo().SL_CFD():
            child_leg.RollingPeriodBase(return_date)
            child_leg.RollingPeriod("1d")
            child_leg.EndDate(end_day)
        else:
            first_day_of_next_month = acm.Time().FirstDayOfMonth(acm.Time().DateAddDelta(return_date, 0, 1, 0))
            child_leg.RollingPeriodBase(first_day_of_next_month)
            child_leg.RollingPeriod("1m")
            child_leg.FixedCoupon(True)
            child_leg.EndDate(end_day)

    except Exception as e:
        raise Exception("Could not create child instrument leg because {error}".format(error=str(e)))


def create_trade(parent_trade, instrument, return_quantity,
                 return_date, return_datetime=None, swift_flag=None):

    LOGGER.info("Creating return trade")

    if not parent_trade.IsKindOf(acm.FTrade):
        parent_trade = parent_trade[0]

    parent_instrument = parent_trade.Instrument()
    try:
        if parent_instrument.InsType() == "SecurityLoan":

            mirror_trade = parent_trade.GetMirrorTrade()
            parent_quantity = sl_functions.underlying_quantity(parent_trade.Quantity(), parent_instrument)
            child_quantity = sl_functions.trade_quantity(parent_quantity - return_quantity, instrument)
            child_trade = parent_trade.Clone()
            child_trade.TrxTrade(parent_trade)
            child_trade.Quantity(child_quantity)
            child_trade.Contract(parent_trade.Contract())
            child_trade.MirrorTrade(None)
            set_mirror_details(child_trade, mirror_trade)
            child_trade.AddInfoValue("SL_G1SentTime", "")
            child_trade.AddInfoValue("SL_Instruction_Note", "")
            child_trade.AddInfoValue("SL_ConfirmationSent", False)
            child_trade.AddInfoValue("SL_ReturnedQty", return_quantity)
        else:
            child_trade = parent_trade.Clone()
            child_trade.Type("Normal")
            child_trade.ContractTrade(None)
            child_trade.TrxTrade(parent_trade)
            child_trade.FaceValue(return_quantity)
            child_trade.ConnectedTrade(parent_trade)

        child_trade.AddInfoValue("Unique_Strate_ID", "")
        set_trade_details(child_trade, parent_trade, instrument,
                        return_date, return_datetime, swift_flag)

        return child_trade

    except Exception as e:
        raise Exception("Could not create return on trade {trade} because {error}".format(
                        trade=parent_trade.Oid(), error=str(e)))


def set_trade_details(child_trade, parent_trade, instrument, 
                      return_date, return_datetime=None, swift_flag=None):

    try:
        child_trade.OptKey1("")
        child_trade.ExecutionTime("")
        child_trade.OptionalKey(None)
        child_trade.ValueDay(return_date)
        child_trade.Instrument(instrument)
        child_trade.AcquireDay(return_date)
        child_trade.Text1(RETURN_TYPES["PARTIAL"])
        child_trade.AddInfoValue("SL_IsCorpAction", "")
        child_trade.Status(RETURN_STATUSES["FO_CONFIRM"])
        
        # Remove existing payments
        for payment in child_trade.Payments()[:]:
            child_trade.Payments().Remove(payment)

        if return_datetime:
            child_trade.TradeTime(return_datetime)
        else:
            return_date = ("{date} {time_now}".format(
                          date=return_date, time_now=acm.Time().TimeOnlyMs()))
            child_trade.TradeTime(min(return_date[:-4], acm.Time().TimeNow()))

        if swift_flag:
            child_trade.AddInfoValue("SL_SWIFT", swift_flag)
        else:
            child_trade.AddInfoValue("SL_SWIFT", parent_trade.AddInfoValue("SL_SWIFT"))
            
    except Exception as e:
        raise Exception("Could not cretae child from {trade} because {error}".format(
                        trade=parent_trade.Oid(), error=str(e)))

def set_mirror_details(child_trade, mirror_trade):

    LOGGER.info("Adding mirror details to trade {trade}".format(
                trade=child_trade.Oid()))
    mirror_prf = None
    child_cpty_portfolio = None
    child_instrument = child_trade.Instrument()
    child_cp_portfolio = child_trade.Portfolio().AdditionalInfo().CP_Portfolio()

    if child_cp_portfolio:
        child_cpty_portfolio = acm.FPhysicalPortfolio[child_cp_portfolio]

    if (child_cp_portfolio and
        child_cpty_portfolio and
        child_trade.Counterparty().Type() == "Intern Dept" and
        child_trade.Counterparty().Oid() == RELEVANT_COUNTERPARTIES[0].Oid()):
        child_trade_mirror = child_trade.GetMirrorTrade()

        if (child_trade_mirror == None and
            child_trade.Status() in VALID_STATUSES and
            child_instrument.OpenEnd() == "Open End"):
            mirror_prf = child_cpty_portfolio
    else:
        if mirror_trade:
            mirror_prf = mirror_trade.Portfolio()

    if mirror_prf:
        child_trade.MirrorPortfolio(mirror_prf)


def generate_full_return(parent_trade, return_date, return_quantity,
                        return_datetime=None, swift_flag=None, is_corp_action=None):

    LOGGER.info("Creating close instrument for {ins}".format(
                ins=parent_trade.Instrument().Name()))
    try:
        if parent_trade.Instrument().InsType() == "SecurityLoan":
            mirror_trade = parent_trade.GetMirrorTrade()
            lender = parent_trade.add_info("SL_G1Counterparty2")
            borrower = parent_trade.add_info("SL_G1Counterparty1")
            if mirror_trade:
                mirror_lender = mirror_trade.add_info("SL_G1Counterparty2")
                mirror_borrower = mirror_trade.add_info("SL_G1Counterparty1")
            if mirror_trade and not (lender or borrower or mirror_lender or mirror_borrower):
                LOGGER.info("Terminating internal trade {}".format(parent_trade.Oid()))
                terminate_trade(parent_trade, return_date, None, return_datetime)
                return parent_trade
            if not (mirror_trade or lender or borrower):
                LOGGER.info("Terminating internal trade {}".format(parent_trade.Oid()))
                terminate_trade(parent_trade, return_date, None, return_datetime)
                return parent_trade
            if mirror_trade and not (lender or borrower) and mirror_lender and mirror_borrower:
                parent_trade = mirror_trade

            close_rate = 0.0
            close_instrument = create_instrument(parent_trade, return_date, close_rate)
            close_trade = create_trade(parent_trade, close_instrument,
                            return_quantity, return_date, return_datetime, swift_flag)
            close_trade.Type("Closing")
            close_trade.ExecutionTime("")
            close_trade.Text1(RETURN_TYPES["FULL"])
            close_trade.Quantity(parent_trade.FaceValue())
            close_trade.FaceValue(parent_trade.FaceValue())
            close_trade.ConnectedTrade(parent_trade.ContractTrade())
            close_trade.AddInfoValue("SL_G1Fee2", close_rate)
            close_trade.AddInfoValue("SL_ConfirmationSent", False)
            close_trade.AddInfoValue("SL_ReturnedQty", parent_trade.FaceValue())
            close_trade.MirrorTrade(None)
            close_trade.MirrorPortfolio(None)
            if is_corp_action:
                close_trade.AddInfoValue("SL_SWIFT", "")

            close_trade.Commit()
            close_instrument.SLGenerateCashflows()
            close_instrument.OpenEnd(RETURN_STATUSES["OPEN_END"])
            close_instrument.Commit()
            terminate_trade(parent_trade, return_date, close_trade, return_datetime)

            return close_trade

    except Exception as e:
        raise Exception("Could not create full return on {trade} because {error}".format(
                        trade=parent_trade.Oid(), error=str(e)))


def get_remaining_collateral(trades, return_quantity, child_trade):
    try:
        summed_quantity = 0
        remaining_collateral = 0
        for trade in trades:
            summed_quantity += trade.FaceValue()
        if abs(summed_quantity) > abs(return_quantity):
            remaining_collateral = abs(summed_quantity) - abs(return_quantity)
        if child_trade.FaceValue()*remaining_collateral < 0:
            return remaining_collateral
        return (-1*remaining_collateral)
    except Exception as e:
        raise Exception("Could not get remaining collateral because {error}".format(error=str(e)))


def get_custody_trades_list(trades):

    LOGGER.info("Checking if there is a custody trade linked to trades")
    try:
        custody_trades = acm.FArray()
        for trade in trades:
            custody_trade = get_custody_trade(trade)
            if custody_trade:
                custody_trades.Add(custody_trade)
        return custody_trades
    except Exception as e:
        raise Exception("Could not get custody trade list because {error}".format(error=str(e)))


def get_custody_trade(parent_trade):

    try:
        custody_trade = None
        contract_trade = parent_trade.ContractTrdnbr()
        custody_list = [trade for trade in acm.FTrade.Select("contractTrdnbr = {contract} and oid <> {parent}".format(
                                                            contract=contract_trade, parent=contract_trade))]
        if parent_trade.Oid() != contract_trade:
            custody_trade = acm.FTrade[contract_trade]
        elif custody_list:
            custody_trade = custody_list[0]
        return custody_trade
    except Exception as e:
        raise Exception("Could not get custody trade because {error}".format(error=str(e)))


def get_collateral_trades():
    acs_portfolio = acm.FPhysicalPortfolio[13927]  # SBL_NonCash_Collateral_ACSMB
    acs_counterparty = acm.FParty["SLB ACS MAIN"]
    collateral_trades_query = "acquirer = '{acq}' and portfolio = '{portf}' and counterparty = '{cpty}' "
    collateral_trades_query += "and tradeCategory = 'Collateral' and text1 = '' and status in {statuses}"
    collateral_trades = [
        trade for trade in acm.FTrade.Select(
            collateral_trades_query.format(
                acq=ACQUIRER.Name(),
                portf=acs_portfolio.Name(),
                cpty=acs_counterparty.Name(),
                statuses=("BO Confirmed", "BO-BO Confirmed")
            )
        )
    ]
    return collateral_trades


def get_acs_loans():
    loan_portfolio = acm.FPhysicalPortfolio[5708]  # Collateral optimize
    acs_loan_trades_query = "counterparty = '{party}' and acquirer = '{acquirer}' "
    acs_loan_trades_query += "and portfolio = '{portfolio}' and status in {statuses}"
    acs_loan_trades = [trade for trade in acm.FTrade.Select(
                        acs_loan_trades_query.format(
                        party="PRIME SERVICES DESK",
                        acquirer=ACQUIRER.Name(),
                        portfolio=loan_portfolio.Name(),
                        statuses=("FO Confirmed", "BO Confirmed", "BO-BO Confirmed")))]
    return acs_loan_trades


def get_loan_positions(loan_portfolio):
    loan_position = 0
    loan_instruments = {}
    loan_trades = loan_portfolio.Trades()

    for loan_trade in loan_trades:
        loan_instrument = loan_trade.Instrument()
        if loan_trade.Status() in ["Void", "Simulated", "FO Confirmed"]:
            continue
        elif loan_instrument.InsType() == "SecurityLoan":
            underlying = loan_instrument.Underlying()
            if (underlying and underlying.InsType() == "Stock" and
                loan_instrument.OpenEnd() != "Terminated"):
                loan_underlying = underlying.Name()
                loan_value = round(loan_trade.FaceValue(), 0)
                loan_position += loan_value

                if not loan_value:
                    continue
                if loan_underlying not in list(loan_instruments.keys()):
                    loan_instruments[loan_underlying] = loan_value
                else:
                    loan_instruments[loan_underlying] += loan_value
    LOGGER.info("Loan position = {loan_pos}".format(loan_pos=loan_position))
    return [loan_position, loan_instruments]


def get_coll_position(coll_trades):
    coll_position = 0
    coll_instruments = {}
    for coll_trade in coll_trades:
        coll_ins = coll_trade.Instrument().Name()
        coll_value = round(coll_trade.FaceValue(), 0)
        if not coll_value:
            continue
        coll_position += coll_value
        if coll_ins not in list(coll_instruments.keys()):
            coll_instruments[coll_ins] = coll_value
        else:
            coll_instruments[coll_ins] += coll_value
    LOGGER.info("Collateral position = {pos}".format(pos=coll_position))
    return [coll_position, coll_instruments]


def get_loan_trades(ins_name, loan_instruments):
    loan_trades = []
    for loan_instrument in loan_instruments:
        if loan_instrument:
            for loan_trade in loan_instrument.Trades():
                if (loan_instrument.Underlying() and
                    loan_instrument.Underlying().Name() == ins_name):
                    loan_trades.append(loan_trade)
    return loan_trades


def get_collateral_trade(ins_name):
    collateral_trades = get_collateral_trades()
    if collateral_trades:
        for coll_trade in collateral_trades:
            if coll_trade.Instrument().Name() == ins_name:
                return coll_trade


def get_ael_variables():

    def enable_tradetime(ael_var):
        for var in variables:
            if var[0] == "return_tradetime":
                var.enabled = ael_var.value == "true"

    def return_quantity_hook(ael_var):
        value = FCallDepositFunctions.NumberFormatting(0, [ael_var.value])
        if value:
            ael_var.value = value[0]

    variables = AelVariableHandler()
    variables.add(
    "return_date",
    label="Return date",
    default=TODAY,
    mandatory=False,
    multiple=False,
    alt="Date to be used when creating return trade"
    )
    variables.add(
    "return_quantity",
    label="Return quantity",
    mandatory=False,
    multiple=False,
    alt="Amount to return",
    hook=return_quantity_hook
    )
    variables.add(
    "swift_flag",
    label="Swift flag",
    mandatory=False,
    multiple=False,
    collection=SWIFT_FLAG,
    alt="DOM or SWIFT flag for settlement"
    )
    variables.add(
    name="explicit_tradetime",
    label="Set Trade Time Explicitly",
    cls="bool",
    collection=(True, False),
    default="bool",
    mandatory=False,
    multiple=False,
    hook=enable_tradetime,
    alt="Click checkbox to backdate trade"
    )
    variables.add(
    "return_tradetime",
    label="Return tradetime",
    cls="string",
    enabled = False,
    mandatory = False,
    alt="Explicit trade time"
    )
    variables.add(
    name="is_corp_action",
    label="Is Corporate Action?",
    cls="bool",
    collection=(True, False),
    default="bool",
    mandatory=False,
    multiple=False,
    alt="Click checkbox to backdate trade"
    )
    variables.extend(FBDPGui.LogVariables())
    return variables
