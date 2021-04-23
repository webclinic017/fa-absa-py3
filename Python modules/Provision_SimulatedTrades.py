"""
-------------------------------------------------------------------------------
MODULE
    Provision

DESCRIPTION
    Date                : 05/08/2014
    Purpose             : Main provision module.
    Department and Desk : Middle Office
    Requester           : Helder Loio
    Developer           : Jakub Tomaga
    CR Number           : CHNG0002036323

HISTORY
===============================================================================
Date        CR number   Developer       Description
-------------------------------------------------------------------------------
05-09-2014  2234300      Jakub Tomaga   - MOPL provision handler modified:
                                          typo corrected and yield curve
                                          conversion added
                                        - end date added to the composite key
                                          for caching rates
                                        - 'future' trades excluded from
                                          calculation
02/10/2014  2325358     Jakub Tomaga    Support for price testing added.
2015-01-14  2562289     Hynek Urban     Use sum_over_multiple where appropriate.
2018-04-19  CHG1000369866 Anil Parbhoo  Change script to apply only to Simulated trades. This py script is based on the py script = Provision
                                        Any Changes (other than trade status) to the Prosion script should also be mirored in this script
                                        
                                        
-------------------------------------------------------------------------------
"""

import ael
import acm

from at_decorators import sum_over_multiple
from collections import defaultdict
from IRDShortEndCurveProvision import market_rate
from PS_Provision import GetProvision, hist_valuation
from at_logging import getLogger

LOGGER = getLogger(__name__)
#LOGGER.setLevel(10)#DEBUG

VALID_TRADE_STATUSES = [
    'FO Confirmed',
    'BO Confirmed',
    'BO-BO Confirmed',
    'Terminated',
    'Simulated'
]


class ProvisionNotApplicable(Exception):
    """Provision not applicable."""


def calculate(trade):
    """Return provision per trade (ZAR-SWAP only)."""
    yield_curve = acm.FYieldCurve['ZAR-SWAP']
    handler = ProvisionHandler(yield_curve)
    try:
        trade_provision = handler.calculate(trade)
    except ProvisionNotApplicable:
        LOGGER.debug("Provision not applicable for trade %s", trade.Oid(), exc_info=1)
        trade_provision = 0.0
    LOGGER.debug("Provision for trade '%s': %s", trade.Oid(), trade_provision)
    return trade_provision


@sum_over_multiple('portfolio_swap')
def calculate_provision_start_end(trades, instrument, portfolio_swap,
        start_date, end_date, warehousing_type='Daily'):
    """Return provision within the date range (per instrument type).

    Historical provision is stored on the Total Return leg of a portfolio swap
    on an instrument level. This function returns the sum of all provision
    resets for a given date range for a particular instrument type.

    For intraday it should calculate the provision from the yield curve.

    """
    
    start_provision = GetProvision(instrument, portfolio_swap, start_date)
    LOGGER.debug("Start provision '%s': %s", instrument.Name(), start_provision)
    
    end_provision = 0.0
    today = acm.Time.DateToday()

    if today == end_date and not hist_valuation():
        for trade in trades.AsList():
            funding_instrument = trade.Portfolio().AdditionalInfo().PS_FundingIns()
            if funding_instrument != portfolio_swap:
                continue  # Trade doesn't belong to the processed portfolio swap.
            end_provision += calculate(trade)
    else:
        LOGGER.debug("Historical valuation. Using PSwap to retrieve provision: '%s'", portfolio_swap.Name())
        end_provision = GetProvision(instrument, portfolio_swap, end_date)
        
    LOGGER.debug("End provision '%s': %s", instrument.Name(), end_provision)
    
    provision = end_provision - start_provision
    return provision


def calculate_provision(trade, yield_curve):
    """Return provision per trade (using a given yield curve).

    This is a special function used in MOPL returning provision in form of
    a dictionary (later used in MOPL reporting).

    Note: MOPL handles provision exception (ProvisionNotApplicable) from
    within its own scripts.

    """

    if yield_curve.Name() in ('ZAR-SWAP-SPREAD-1m', 'ZAR-SWAP-SPREAD-6m',
            'ZAR-SWAP-SPREAD-9m', 'ZAR-SWAP-SPREAD-12m'):
        yield_curve = acm.FYieldCurve['ZAR-SWAP']
    elif yield_curve.Name() in ('ZAR-SWAP', 'USD-SWAP'):
        pass
    else:
        message = 'Provision not applicable for the curve'
        raise ProvisionNotApplicable(message)

    my_provision = MOPLProvisionHandler(yield_curve)
    return my_provision.calculate(trade)


class ProvisionHandlerError(Exception):
    """General provision handler error."""


class ProvisionHandler(object):
    """Class for provision calculation."""

    def __init__(self, yield_curve, market_rate_instruments=None):
        """Initialise provision object."""
        self.forward_yield_curve = yield_curve
        self.forward_yield_curve_ael = ael.YieldCurve[yield_curve.Name()]
        self.currency = self.forward_yield_curve.Currency()

        self.mapped_forward_curve = None

        if self.currency.Name() == 'ZAR':
            self.calendar = acm.FCalendar['ZAR Johannesburg']
        elif self.currency.Name() == 'USD':
            self.calendar = acm.FCalendar['USD New York']
        else:
            message = "Currency not supported: {0}".format(
                self.currency.Name())
            raise ProvisionHandlerError(message)

        # Already once calculated rates (key depends on data).
        self.rates_key = None
        # Dictionary of rates. Every value is a list of two items:
        #     self.rates[key][0] --> short_end_rate
        #     self.rates[key][1] --> forward_rate
        self.rates = {}

        self.start_date = acm.Time().DateToday()
        # Will be adjusted later on once leg will be retrieved
        self.end_date = acm.Time().DateAddDelta(self.start_date, 0, 9, 0)

        # Will be filled with all pay calendars on the leg
        self.pay_calendars = []

        self.leg = None

        # 'None' indicates column calculation
        self.report_type = None

        # Market rate instruments (e.g. for price testing)
        self.market_rate_instruments = market_rate_instruments

    def _first_leg(self, instrument):
        """Return first float/fixed leg for the instrument based on type."""
        if instrument.InsType() == 'CurrSwap':
            for leg in instrument.Legs():
                if leg.IsFixedLeg() and leg.Currency().Name() == 'ZAR':
                    return leg
            else:
                return None
        return instrument.FirstFloatLeg()

    def _mapped_forward_curve(self, leg):
        """Return forward curve from leg."""
        if leg.LegType() == 'Fixed':
            forward_curve = acm.FYieldCurve['ZAR-SWAP']
            self.mapped_forward_curve = forward_curve.Name()
        else:
            yc_component = leg.MappedForwardLink().Link().YieldCurveComponent()
            if 'FYCAttribute' in str(yc_component.Class()):
                forward_curve = yc_component.Curve()
            else:
                forward_curve = yc_component

            self.mapped_forward_curve = forward_curve.Name()

            if forward_curve.Name() in ('ZAR-SWAP-SPREAD-1m', 'ZAR-SWAP-SPREAD-6m',
                    'ZAR-SWAP-SPREAD-9m', 'ZAR-SWAP-SPREAD-12m'):
                forward_curve = acm.FYieldCurve['ZAR-SWAP']

        return forward_curve

    def _is_valid_cashflow(self, cash_flow):
        """Return True if cash flow is valid, otherwise return False."""
        if not cash_flow.StartDate() or not cash_flow.EndDate():
            return False

        if (cash_flow.EndDate() >= self.start_date and
                cash_flow.StartDate() <= self.end_date):
            if cash_flow.Instrument().InsType() == 'CurrSwap':
                if (cash_flow.CashFlowType() == 'Fixed Rate' and
                        cash_flow.StartDate() >= self.start_date):
                    return True
            else:
                return True

        return False

    def _is_valid_reset(self, reset):
        """Return True if reset is valid, otherwise return False."""
        if reset.ResetType() in ('Single', 'Compound', 'Weighted'):
            reset_date = reset.Day()
            if reset_date >= self.start_date and reset_date <= self.end_date:
                return True

        return False

    def _is_valid_trade(self, trade):
        """Verify if the trade is valid for provision calculation."""
        if not trade:
            return False

        if trade.Status() in VALID_TRADE_STATUSES:
            if acm.Time().AsDate(trade.TradeTime()) > self.start_date:
                return False
            print '1'
            ins_type = trade.Instrument().InsType()
            if ins_type == 'Curr':
                if trade.ValueDay() > self.start_date:
                    return True
            elif ins_type == 'Combination':
                for comb_ins in trade.Instrument().Instruments():
                    trades = comb_ins.Trades()
                    if trades and trades[0] in VALID_TRADE_STATUSES:
                        trade = trades[0]
                        ins_type = trade.Instrument().InsType()
                        if (self._is_basis_trade(trade) and
                                ins_type in ('Swap', 'FRA')):
                            return True
            elif ins_type == 'CurrSwap':
                if trade.Instrument().ExpiryDateOnly() > self.start_date:
                    return True
            else:
                if trade.Instrument().ExpiryDateOnly() > self.start_date:
                    if (self._is_basis_trade(trade) and
                            ins_type in ('Swap', 'FRA')):
                        return True

        return False

    @staticmethod
    def _is_basis_trade(trade):
        """Return True if trade is a basis trade."""
        basis_flag = 0
        for leg in trade.Instrument().Legs():
            if leg.IsFloatLeg():
                basis_flag += 1
            else:
                basis_flag -= 1

        if basis_flag < 2:
            return True

        return False

    def _is_valid_leg(self, leg):
        """Return True if  leg contains suitable data for provision."""
        if not leg:
            return False

        if (leg.LegType() == 'Float' and
                leg.FloatRateReference() and
                leg.Currency().Name() == self.currency.Name()):
            return True
        elif leg.LegType() == 'Fixed':
            return True

        return False

    def _rate_dates(self, common_object):
        """Start and end date for rates (based on object type."""
        if common_object.IsKindOf(acm.FCashFlow):
            start_date = common_object.StartDate()
        elif common_object.IsKindOf(acm.FReset):
            start_date = common_object.Day()
        else:
            message = "Rate dates for {0} object are not defined".format(
                type(common_object))
            raise ProvisionHandlerError(message)

        end_date = acm.Time().DateAddDelta(start_date, 0, 3, 0)
        end_date = self._adjust_to_banking_day(end_date)

        return (start_date, end_date)

    def _reset_period(self, common_object):
        """Return reset period."""
        if (common_object.IsKindOf(acm.FCashFlow) or
                common_object.IsKindOf(acm.FReset)):
            start_date = common_object.StartDate()
            end_date = common_object.EndDate()
            if common_object.IsKindOf(acm.FReset) and not start_date and not end_date:
                start_date = common_object.CashFlow().StartDate()
                end_date = common_object.CashFlow().EndDate()
                LOGGER.debug("Reset '%s' has not start/end date. Using Cashflow values.", common_object.Oid())
            LOGGER.debug("Reset period for '%s' with id '%s'. Start date '%s', End Date '%s'", 
                         type(common_object), common_object.Oid(), start_date, end_date)
            return acm.Time().DateDifference(end_date, start_date) / 365.0
        else:
            message = "Reset period for {0} object is not defined.".format(
                type(common_object))
            raise ProvisionHandlerError(message)

    def _fx_rate(self):
        """Return FX rate."""
        base_currency = ael.Instrument['ZAR']
        currency = ael.Instrument[self.currency.Name()]
        return 1.0 / base_currency.used_price(ael.date(self.start_date),
            currency.insid)

    def _trade_nominal(self, trade, cash_flow):
        """Return trade nominal."""
        calc_space = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        return cash_flow.Calculation().Nominal(calc_space, trade).Number() * self._fx_rate()

    def _partial_provision(self, trade, common_object):
        """Return provision per cash flow/reset."""
        day_count_method = common_object.Leg().DayCountMethod()
        rate_start_date, rate_end_date = self._rate_dates(common_object)

        key = (rate_start_date, rate_end_date, day_count_method)
        if key in self.rates:
            LOGGER.debug("Using provided rates")
            short_end_rate = self.rates[key][0]
            forward_rate = self.rates[key][1]
        else:
            LOGGER.debug("Using FA rates")
            short_end_rate = market_rate(ael.date(rate_start_date),
                ael.date(self.start_date), self.currency.Name(),
                self.market_rate_instruments) / 100
            
            LOGGER.debug("Getting forward rate: start_date: '%s', end_date: '%s', day_count_method: '%s'",
                         rate_start_date, rate_end_date, day_count_method)
            forward_rate = self.forward_yield_curve_ael.yc_rate(
                ael.date(rate_start_date), ael.date(rate_end_date),
                'Quarterly', day_count_method, 'Forward Rate')

            self.rates[key] = [short_end_rate, forward_rate]
        LOGGER.debug("Short end rate: '%s'. Forward rate: '%s'", short_end_rate, forward_rate)
        
        # Calculate provision
        reset_period = self._reset_period(common_object)
        if common_object.IsKindOf(acm.FCashFlow):
            cash_flow = common_object
        else:
            cash_flow = common_object.CashFlow()
        nominal = self._trade_nominal(trade, cash_flow)
        provision = nominal / 100 * reset_period * 96 * (
            short_end_rate - forward_rate)

        if trade.Instrument().InsType() == 'CurrSwap':
            provision *= -1

        # Create report record if used as part of report
        if self.report_type:
            self._create_report_record(trade, common_object, reset_period,
                nominal, provision, short_end_rate, forward_rate)
        
        LOGGER.debug("Trade: '%s'. Provision: '%s', Nominal: '%s', Reset period: '%s'", trade.Oid(), provision, nominal, reset_period)
        
        return provision

    def _create_report_record(self, trade, common_object, reset_period,
            nominal, provision, short_end_rate, forward_rate):
        """Create record to be added to the report.

        Basic ProvisionHandler class is used for provision calculation for
        columns or reports that don't need information about partial provision
        per reset, cash flow, etc. Otherwise override this method accordingly.

        """
        pass

    def _validate(self, trade):
        """Validate if provision applies to trade."""
        LOGGER.debug("Validating trade %s", trade.Oid())
        # Check if provision is applicable for given trade
        if not self._is_valid_trade(trade):
            message = "Invalid trade"
            raise ProvisionNotApplicable(message)

        # Check if provision is applicable for leg
        leg = self._first_leg(trade.Instrument())
        if not self._is_valid_leg(leg):
            message = "Invalid leg"
            raise ProvisionNotApplicable(message)

        # Check if forward curve matches
        if self.forward_yield_curve != self._mapped_forward_curve(leg):
            message = "Forward curve doesn't match. Leg '{0}'. Curves: {1} != {2}".format(leg.Oid(), 
                                                                                          self.forward_yield_curve.Name(), 
                                                                                          self._mapped_forward_curve(leg).Name())
            raise ProvisionNotApplicable(message)

        # Trade validated
        self.leg = leg

        # Fill-in calendars for banking days.
        self.pay_calendars = self._get_pay_calendars(leg)

    def _get_pay_calendars(self, leg):
        """Return pay calendars on the leg (used for day adjustments)."""
        pay_calendars = [
            leg.PayCalendar(),
            leg.Pay2Calendar(),
            leg.Pay3Calendar(),
            leg.Pay4Calendar(),
            leg.Pay5Calendar()
        ]
        return [cal for cal in pay_calendars if cal is not None]

    def _adjust_to_banking_day(self, date):
        """Adjust date to next banking day according to all pay calendars."""
        adjusted_date = date
        non_banking_flag = True

        while non_banking_flag:
            current_adjusted_date = adjusted_date
            for calendar in self.pay_calendars:
                if calendar.IsNonBankingDay(None, None, adjusted_date):
                    # Adjust date and test against all pay calendars again
                    adjusted_date = calendar.AdjustBankingDays(adjusted_date, 1)
                    break

            # No change in the last round
            if adjusted_date == current_adjusted_date:
                non_banking_flag = False

        return adjusted_date

    def _calculate(self, trade):
        """Calculate provision for trade."""
        LOGGER.debug("Calculating provision for trade '%s'", trade.Oid())
        total_provision = 0.0
        for cash_flow in self.leg.CashFlows():
            LOGGER.debug("Calculating provision for cashflow '%s'", cash_flow.Oid())
            # Verify if provision is applicable for cash flow
            if not self._is_valid_cashflow(cash_flow):
                continue
            if trade.Instrument().InsType() == 'CurrSwap':
                provision = self._partial_provision(trade, cash_flow)
                total_provision += provision
            else:
                for reset in cash_flow.Resets():
                    LOGGER.debug("Calculating provision for reset '%s'", reset.Oid())
                    # Verify if provision is applicable for reset
                    if not self._is_valid_reset(reset):
                        continue
                    provision = self._partial_provision(trade, reset)
                    total_provision += provision

        return total_provision

    def calculate(self, trade):
        """Return provision calculated for trade. Default provision is 0."""
        self._validate(trade)
        return self._calculate(trade)


class MOPLProvisionHandler(ProvisionHandler):
    """Specific provision handler for MOPL."""

    def _calculate(self, trade):
        """Specific provision calculation for MOPL."""
        total_provision = defaultdict(float)
        key = (
            trade.Oid(),
            self.leg.Currency().Name(),
            self.mapped_forward_curve
        )
        for cash_flow in self.leg.CashFlows():
            # Verify if provision is applicable for cash flow
            if not self._is_valid_cashflow(cash_flow):
                continue
            if trade.Instrument().InsType() == 'CurrSwap':
                provision = self._partial_provision(trade, cash_flow)
                total_provision[key] += provision
            else:
                for reset in cash_flow.Resets():
                    # Verify if provision is applicable for reset
                    if not self._is_valid_reset(reset):
                        continue
                    provision = self._partial_provision(trade, reset)
                    total_provision[key] += provision

        return total_provision
