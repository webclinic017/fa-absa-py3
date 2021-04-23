'''
HISTORY
================================================================================
Date        Change no      Developer          Description
--------------------------------------------------------------------------------
2019-09-27  FAU-417        Tibor Reiss        Quick fix for omsfin
2020-01-29  FAPE-120       Tibor Reiss        Remove code for old funding method
'''

from collections import defaultdict

import acm
from at_time import to_datetime
from at_logging import getLogger
from ABSAPortfolioSwapCustom import LegType
from PS_FundingCalculations import GetReset
import pb_pswap_proxy
reload(pb_pswap_proxy)
from pb_pswap_proxy import PBLegProxy 


LOGGER = getLogger(__name__)
ZAR_CALENDAR = acm.FCalendar['ZAR Johannesburg']  # TODO: might be necessary to have a dynamic calendar
DATE_TODAY = acm.Time.DateToday()


class UnexpectedLegException(Exception):
    pass


class PBPswap(object):
    def __init__(self, start_date=None, end_date=None, system_date=None, adjust_to_business_days=True):
        # No default value for the start/end dates, otherwise it will
        # not be updated when date changes
        if not start_date:
            self.start_date = acm.Time.DateFromYMD(1970, 1, 1)
        else:
            self.start_date = start_date
        
        if not end_date:
            self.end_date = acm.Time.DateToday()
        else:
            self.end_date = end_date
        
        if not system_date:
            self.system_date = acm.Time.DateToday()
        else:
            self.system_date = system_date
        
        # unajusted dates 
        self._start_date = self.start_date
        self._end_date = self.end_date
        
        if adjust_to_business_days:
            if ZAR_CALENDAR.IsNonBankingDay(None, None, self.start_date):
                LOGGER.debug("Adjusting start date: %s", self.start_date)
                self.start_date = ZAR_CALENDAR.AdjustBankingDays(self.start_date, -1)
            
            if ZAR_CALENDAR.IsNonBankingDay(None, None, self.end_date):
                LOGGER.debug("Adjusting end date: %s", self.end_date)
                self.end_date = ZAR_CALENDAR.AdjustBankingDays(self.end_date, 1)
        
        self.next_business_day = ZAR_CALENDAR.AdjustBankingDays(self.end_date, 1)
        self.prev_business_day = ZAR_CALENDAR.AdjustBankingDays(self.end_date, -1)
        LOGGER.debug("Start date: %s", self.start_date)
        LOGGER.debug("End date: %s", self.end_date)
        LOGGER.debug("Prev business date: %s", self.prev_business_day)
        LOGGER.debug("Next business date: %s", self.next_business_day)
        LOGGER.debug("System date: %s", self.system_date)
    
    def get_legs(self, trade, leg_type=[]):
        """Returns a list of legs that correspond to the provided leg type and pay/rec"""
        result = []
        i = trade.Instrument()
        for leg in i.Legs():
            if LegType(leg) in leg_type:
                result.append(leg)
                    
        return result  
    
    def get_live_cashflows(self, leg, start_date, end_date, pay_date=None, cf_types=[]):
        cfs = leg.CashFlows()
        
        for cf in cfs:
            LOGGER.debug("CF '%s': StartDate '%s', EndDate '%s', PayDate '%s', Type '%s'",
                         cf.Oid(), cf.StartDate(), cf.EndDate(), cf.PayDate(), cf.CashFlowType())
        if pay_date:
            cfs = filter(lambda cf: cf.StartDate() <= end_date and cf.EndDate() >= end_date and cf.PayDate() == end_date, cfs)
        else:
            cfs = filter(lambda cf: cf.StartDate() <= end_date and cf.EndDate() >= end_date, cfs)
        
        if not cfs and str(to_datetime(leg.Instrument().UpdateTime())) < end_date:
            cfs = leg.CashFlows()
            cfs = filter(lambda cf: cf.StartDate() <= end_date, cfs)
        
        if cf_types:
            cfs = filter(lambda cf: cf.CashFlowType() in cf_types, cfs)
            LOGGER.debug("Using '%s' cashflows", len(cfs))
            
        return cfs
    
    def get_any_cashflows(self, leg, start_date, end_date, pay_date=None, cf_types=[]):
        cfs = leg.CashFlows()
        
        for cf in cfs:
            LOGGER.debug("CF '%s': StartDate '%s', EndDate '%s', PayDate '%s', Type '%s'",
                         cf.Oid(), cf.StartDate(), cf.EndDate(), cf.PayDate(), cf.CashFlowType())
        if pay_date:
            cfs = filter(lambda cf: cf.StartDate() <= end_date and cf.EndDate() >= start_date and cf.PayDate() == end_date, cfs)
        else:
            cfs = filter(lambda cf: cf.StartDate() <= end_date and cf.EndDate() >= start_date, cfs)
            
        if cf_types:
            cfs = filter(lambda cf: cf.CashFlowType() in cf_types, cfs)
            LOGGER.debug("Using '%s' cashflows", len(cfs))
            
        return cfs
    
    def get_unpaied_cashflows(self, leg, start_date, end_date, pay_date=None, cf_types=[]):
        cfs = leg.CashFlows()
        
        for cf in cfs:
            LOGGER.debug("CF '%s': StartDate '%s', EndDate '%s', PayDate '%s', Type '%s'",
                         cf.Oid(), cf.StartDate(), cf.EndDate(), cf.PayDate(), cf.CashFlowType())

        cfs = filter(lambda cf: cf.StartDate() <= end_date and cf.PayDate() >= end_date, cfs)
            
        if cf_types:
            cfs = filter(lambda cf: cf.CashFlowType() in cf_types, cfs)
            LOGGER.debug("Using '%s' cashflows", len(cfs))
            
        return cfs
    
    def get_mtm(self, leg):
        """market value of position - sum of trade premiums"""
        if LegType(leg) != "MTM":
            raise UnexpectedLegException('The provided leg is not an MTM leg')
        return 0
    
    def get_dividend(self, leg):
        """LDT Position * Dividend"""
        if LegType(leg) != "Dividend":
            raise UnexpectedLegException('The provided leg is not an Dividend leg')
        return 0
    
    def get_overnight_premium(self, leg):
        if LegType(leg) != "Overnight Premium":
            raise UnexpectedLegException('The provided leg is not an Overnight Premium leg')
        return 0
    
    def get_execution_premium(self, leg):
        # Portfolio Swap Execution Premium TPL
        if LegType(leg) != "Execution Fee":
            raise UnexpectedLegException('The provided leg is not an Execution Fee leg')
        return 0
    
    def get_short_premium(self, leg):
        if LegType(leg) != "Short Premium":
            raise UnexpectedLegException('The provided leg is not an Short Premium leg')
        return 0
    
    def get_day_count_method(self, leg):
        days_per_year = 0
        
        if leg.DayCountMethod() == 'Act/365':
            days_per_year = 365
        if leg.DayCountMethod() == 'Act/360':
            days_per_year = 360
        
        if days_per_year == 0:
            raise Exception("Unexpected DayCountMethod: '{0}'".format(leg.DayCountMethod()))
        
        return days_per_year
    
    def get_default_value(self, leg):
        return 0
    
    def get_cf_nominal(self, resets_by_date):
        cf_nominal = 0
        LOGGER.debug("Got %s keys", len(resets_by_date.keys()))
        for key in sorted(resets_by_date.keys()):
            nominal_scaling = 0
            simple_overnight = 0
            start_date = ''
            end_date = ''
            days = 0
            for reset in resets_by_date[key]:
                start_date = reset.StartDate()
                end_date = reset.EndDate()
                days = acm.Time.DateDifference(reset.EndDate(), reset.StartDate())
                if reset.ResetType() == 'Simple Overnight':
                    simple_overnight += reset.FixingValue() 
                if reset.ResetType() == 'Nominal Scaling':
                    nominal_scaling += reset.FixingValue() 
            
            LOGGER.debug("'%s'; '%s'; '%s'; '%s'; '%s'", start_date, end_date, days, simple_overnight, nominal_scaling)
            cf_nominal += nominal_scaling * simple_overnight * days
        
        return cf_nominal

    def calculate_premium_cash_flow(self, cash_flow, calc_type):
        result = 0.0
        reset_day_start = self.start_date
        reset_day_end = self._end_date
        if calc_type == "val":
            if self._end_date != DATE_TODAY or ZAR_CALENDAR.IsNonBankingDay(None, None, self._end_date):
                return result
            reset_day_start = ZAR_CALENDAR.AdjustBankingDays(self._end_date, -1)
            end_reset = GetReset(cash_flow, "Return", reset_day_end, True, False)
        elif calc_type == "cash":
            if self._end_date == DATE_TODAY and not ZAR_CALENDAR.IsNonBankingDay(None, None, self._end_date):
                reset_day_end = ZAR_CALENDAR.AdjustBankingDays(self._end_date, -1)
            end_reset = GetReset(cash_flow, "Return", reset_day_end, False, True, reset_day_start)
        else:
            end_reset = GetReset(cash_flow, "Return", reset_day_end, False, True, reset_day_start)
        if end_reset:
            result += -1.0 * end_reset.FixingValue()
            if calc_type == "val":
                start_reset = GetReset(cash_flow, "Return", reset_day_start, True, False)
            else:
                start_reset = GetReset(cash_flow, "Return", reset_day_start, False, True)
            if start_reset:
                result -= -1.0 * start_reset.FixingValue()
        return result


class PBPswapDenominated(PBPswap):
    def __init__(self, start_date=None, end_date=None, system_date=None, adjust_to_business_days=True):
        super(PBPswapDenominated, self).__init__(start_date, end_date, system_date, adjust_to_business_days)
    
    def get_mtm(self, leg):
        return self.get_denominated_value(leg, super(PBPswapDenominated, self).get_mtm(leg))
    
    def get_dividend(self, leg):
        return self.get_denominated_value(leg, super(PBPswapDenominated, self).get_dividend(leg))
        
    def get_overnight_premium(self, leg):
        return self.get_denominated_value(leg, super(PBPswapDenominated, self).get_overnight_premium(leg))
        
    def get_execution_premium(self, leg):
        return self.get_denominated_value(leg, super(PBPswapDenominated, self).get_execution_premium(leg))
        
    def get_short_premium(self, leg):
        return self.get_denominated_value(leg, super(PBPswapDenominated, self).get_short_premium(leg))
        
    def get_default_value(self, leg):
        return self.get_denominated_value(leg, super(PBPswapDenominated, self).get_default_value(leg))
        
    def get_denominated_value(self, leg, value, date=None):
        value_date = self.end_date
        if date:
            value_date = date
        return acm.DenominatedValue(value, leg.Instrument().Currency().Name(), value_date)


class PBSwapCashLeg(PBPswapDenominated):
    def __init__(self, start_date=None, end_date=None):
        super(PBSwapCashLeg, self).__init__(start_date, end_date)
    
    def get_mtm(self, leg):
        super(PBSwapCashLeg, self).get_mtm(leg)
        
        result = 0
        cfs = self.get_live_cashflows(leg, self.start_date, self.end_date, self.end_date, cf_types=['Position Total Return'])

        for cf in cfs:
            """
            Have to use only the <b>last</b> 3 resets (sorted by date):
            Nominal scaling - stock position
            1st Return - trade premium
            2nd Return - market price (might be necessary to use the internal price)
            
            MTM = TradePremium - StockPosition * MarketPrice
            """
            stock_position = 0
            market_price = 0
            trade_premium = 0 
            
            resets = sorted(cf.Resets(), key=lambda x: x.StartDate(), reverse=True)
            if len(resets) < 2:
                continue

            if leg.Instrument().OpenEnd() == "Terminated":
                price_date = resets[1].Day()
                price = acm.FPrice.Select01('instrument = "{}" and market = "internal" and day = "{}"'
                                            .format(leg.IndexRef().Name(), price_date), None)
                if price:
                    market_price = price.Settle()
                    if leg.IndexRef().Quotation().Name() == "Per 100 Units":
                        market_price /= 100.0
            else:
                reset = resets[0]
                if reset.ResetType() == 'Return':
                    market_price += reset.FixingValue()
                    if market_price == 0:
                        market_price = leg.IndexRef().used_price() / 100
                else:
                    LOGGER.error("Unexpected reset type: %s (reset: %s)", reset.ResetType(), reset.Oid())
                    continue
            
            reset2 = resets[1]            
            if reset2.ResetType() == 'Return':
                trade_premium += reset2.FixingValue()
            if reset2.ResetType() == 'Nominal Scaling':
                stock_position += reset2.FixingValue()
                
            reset3 = resets[2]
            if reset3.ResetType() == 'Return':
                trade_premium += reset3.FixingValue()
            if reset3.ResetType() == 'Nominal Scaling':
                stock_position += reset3.FixingValue()
            
            LOGGER.debug("%s - %s * %s = %s", trade_premium, stock_position, market_price, trade_premium - stock_position * market_price)
            result += trade_premium - stock_position * market_price
        
        if not leg.PayLeg():
            result = -1 * result
        return self.get_denominated_value(leg, result)

    def get_execution_premium(self, leg):
        super(PBSwapCashLeg, self).get_execution_premium(leg)
        result = 0
        
        cfs = self.get_any_cashflows(leg, self.start_date, self.end_date, cf_types=['Fixed Amount'])

        for cf in cfs:
            LOGGER.debug("Cash flow: %s + %s = %s", result, cf.FixedAmount(), result + cf.FixedAmount())
            result += cf.FixedAmount()
        
        if leg.PayLeg():
            result = -1 * result
        return self.get_denominated_value(leg, result)
    
    def get_dividend(self, leg):
        super(PBSwapCashLeg, self).get_dividend(leg)
        result = 0
            
        cfs = self.get_any_cashflows(leg, self.start_date, self._end_date, cf_types=['Dividend'])
        
        for cf in cfs:
            if cf.PayDate() > self._end_date:
                # if the dividend not payed, we ignore it
                LOGGER.debug("Ignoring cashflow %s, PayDate > end_date (%s > %s)", cf.Oid(), cf.PayDate(), self._end_date)
                continue
            LOGGER.debug("Cash flow: %s + %s = %s", result, cf.FixedAmount(), result + cf.FixedAmount())
            result += -1 * cf.FixedAmount()

        if not leg.PayLeg():
            result = -1 * result
        return self.get_denominated_value(leg, result, self._end_date)

    def get_overnight_premium(self, leg):
        super(PBSwapCashLeg, self).get_overnight_premium(leg)
        return self._get_overnight_premium(leg)

    def _get_overnight_premium(self, leg):
        result = 0.0
        cfs = leg.CashFlows()
        for cf in cfs:
            result += self.calculate_premium_cash_flow(cf, "cash")
        return self.get_denominated_value(leg, result)

    def get_short_premium(self, leg):
        super(PBSwapCashLeg, self).get_short_premium(leg)
        result = -1.0 * self._get_overnight_premium(leg)
        return result


class PBSwapValLeg(PBPswapDenominated):
    def __init__(self, start_date=None, end_date=None, market_price=None):
        self.market_price = market_price
        super(PBSwapValLeg, self).__init__(start_date, end_date)

    def get_mtm(self, leg):
        super(PBSwapValLeg, self).get_mtm(leg)
        result = 0
        cfs = self.get_live_cashflows(leg, self.start_date, self.end_date, cf_types=['Position Total Return'])
        
        for cf in cfs:
            if cf.PayDate() == self.end_date:
                continue
            """
            Have to use only the <b>last</b> 3 resets (sorted by date):
            Nominal scaling - stock position
            1st Return - trade premium
            2nd Return - market price (might be necessary to use the internal price)
            
            MTM = TradePremium - StockPosition * MarketPrice
            """
            stock_position = 0
            if self.market_price is None:
                market_price = 0
                market_price_found = False
            else:
                market_price = self.market_price
                market_price_found = True          
            trade_premium = 0 
            
            resets = filter(lambda r: r.StartDate() == self.end_date or r.EndDate() == self.end_date, cf.Resets())
            resets = sorted(resets, key=lambda x: x.StartDate(), reverse=True)
            
            if len(resets) < 2:
                LOGGER.debug("No resets found for end date <= %s", self.end_date)
                break
            
            stock_position_found = False
            trade_premium_found = False
            for reset in resets:
                LOGGER.debug("Processing reset '%s', ResetType: %s, StartDate: %s, EndDate: %s",
                             reset.Oid(), reset.ResetType(), reset.StartDate(), reset.EndDate())
                if reset.ResetType() == 'Nominal Scaling':
                    stock_position += reset.FixingValue()
                    stock_position_found = True
                
                if reset.ResetType() == 'Return':
                    if cf.EndDate() == reset.StartDate():
                        if market_price_found:
                            continue
                        market_price = reset.FixingValue()
                        LOGGER.debug("Found the market price reset (reset: '%s'): '%s'", reset.Oid(), reset.FixingValue())
                        if market_price == 0:
                            market_price = cf.Leg().IndexRef().used_price() / 100
                            LOGGER.debug("Using the IndexRef price (reset:'%s'): '%s'", reset.Oid(), market_price)
                        market_price_found = True
                    else:
                       trade_premium = reset.FixingValue()  
                       trade_premium_found = True
                       if not market_price_found:
                           # TODO use internal price
                           market_price = cf.Leg().IndexRef().MtMPrice(self._end_date, None, 0) / 100
                           market_price_found = True
                           LOGGER.debug("Using the IndexRef MtMPrice (reset:'%s', Price date: '%s'): '%s'",
                                        reset.Oid(), self._end_date, market_price)
                       
                if stock_position_found and market_price_found and trade_premium_found:
                    break
            if stock_position_found and market_price_found and trade_premium_found:
                LOGGER.debug("%s - %s * %s = %s", trade_premium, stock_position, market_price, trade_premium - stock_position * market_price)            
                result += trade_premium - stock_position * market_price
            else:
                LOGGER.debug("Missing some data!!!")
        
        if not leg.PayLeg():
            result = -1 * result
        return self.get_denominated_value(leg, result)
    
    def get_dividend(self, leg):
        super(PBSwapValLeg, self).get_dividend(leg)
        result = 0
        """ TEST: Reset: 1701523, date 2016-09-23
        TEST: Reset: 1606534, date 2016-02-29
        """   
        cfs = self.get_unpaied_cashflows(leg, self.start_date, self._end_date, cf_types=['Dividend'])
        
        max_date = self.end_date
        for cf in cfs:
            if cf.PayDate() <= self._end_date:
                LOGGER.debug("Ignoring cashflow %s, PayDate <= end_date (%s <= %s)", cf.Oid(), cf.PayDate(), self._end_date)
                continue
            LOGGER.debug("Cash flow: %s + %s = %s", result, cf.FixedAmount(), result + cf.FixedAmount())
            result += -1 * cf.FixedAmount()
            if cf.PayDate() > self._end_date:
                max_date = cf.PayDate()
        
        if not leg.PayLeg():
            result = -1 * result
        return self.get_denominated_value(leg, result, max_date)
    
    def get_overnight_premium(self, leg):
        super(PBSwapValLeg, self).get_overnight_premium(leg)
        return self._get_overnight_premium(leg)

    def _get_overnight_premium(self, leg):
        result = 0.0
        cfs = leg.CashFlows()
        for cf in cfs:
            result += self.calculate_premium_cash_flow(cf, "val")
        return self.get_denominated_value(leg, result)

    def get_short_premium(self, leg):
        super(PBSwapValLeg, self).get_short_premium(leg)
        result = -1.0 * self._get_overnight_premium(leg)
        return result


class PBSwapOpenValueLeg(PBPswapDenominated):
    def __init__(self, start_date=None, end_date=None):
        super(PBSwapOpenValueLeg, self).__init__(start_date, end_date, None, True)

    def get_overnight_premium(self, leg):
        super(PBSwapOpenValueLeg, self).get_overnight_premium(leg)
        return self._get_overnight_premium(leg)

    def _get_overnight_premium(self, leg):
        result = 0.0
        cfs = leg.CashFlows()
        for cf in cfs:
            result += self.calculate_premium_cash_flow(cf, "val")
        return self.get_denominated_value(leg, result)

    def get_short_premium(self, leg):
        super(PBSwapOpenValueLeg, self).get_short_premium(leg)
        result = -1.0 * self._get_overnight_premium(leg)
        return result


class PBSwapTotalValueLeg(PBPswapDenominated):
    def __init__(self, start_date=None, end_date=None):
        super(PBSwapTotalValueLeg, self).__init__(start_date, end_date, None, False)

    def get_mtm(self, leg):
        super(PBSwapTotalValueLeg, self).get_mtm(leg)
        return get_cash_leg(leg, self.start_date, self.end_date)
    
    def get_execution_premium(self, leg):
        super(PBSwapTotalValueLeg, self).get_execution_premium(leg)
        return get_cash_leg(leg, self.start_date, self.end_date)
    
    def get_overnight_premium(self, leg):
        super(PBSwapTotalValueLeg, self).get_overnight_premium(leg)
        return self._get_overnight_premium(leg)

    def _get_overnight_premium(self, leg):
        result = 0.0
        cfs = leg.CashFlows()
        for cf in cfs:
            result += self.calculate_premium_cash_flow(cf, "total")
        return self.get_denominated_value(leg, result)

    def get_short_premium(self, leg):
        super(PBSwapTotalValueLeg, self).get_short_premium(leg)
        result = -1.0 * self._get_overnight_premium(leg)
        return result


class PBSwapForwardValueLeg(PBPswapDenominated):
    def __init__(self, start_date=None, end_date=None):
        super(PBSwapForwardValueLeg, self).__init__(start_date, end_date, None, False)

    def get_mtm(self, leg):
        super(PBSwapForwardValueLeg, self).get_mtm(leg)
        if self.end_date == self.system_date:
            return acm.DenominatedValue(0, leg.Instrument().Currency().Name(), self.end_date)
        
        return get_cash_leg(leg, self.start_date, self.end_date)


class PBSwapUplAdjustmentLeg(PBPswapDenominated):
    def __init__(self, start_date=None, end_date=None):
        super(PBSwapUplAdjustmentLeg, self).__init__(start_date, end_date, None, False)


class PBSwapDividendsLeg(PBPswapDenominated):
    def __init__(self, start_date=None, end_date=None):
        super(PBSwapDividendsLeg, self).__init__(start_date, end_date, None, False)
  
    def get_dividend(self, leg):
        super(PBSwapDividendsLeg, self).get_dividend(leg)
        return get_cash_leg(leg, self.start_date, self.end_date)


class PBSwapNominalFactorLeg(PBPswap):
    def __init__(self, start_date=None, end_date=None):
        super(PBSwapNominalFactorLeg, self).__init__(start_date, end_date, None, False)

    def get_mtm(self, leg):
        super(PBSwapNominalFactorLeg, self).get_mtm(leg)
        result = 0
                
        cfs = self.get_live_cashflows(leg, self.start_date, self.end_date, cf_types=['Position Total Return'])
    
        for cf in cfs:
            if cf.PayDate() == self.end_date:
                continue
            result = cf.NominalFactor()
            
            resets = filter(lambda r: r.StartDate() == self.end_date, cf.Resets())
            resets = sorted(resets, key=lambda x: x.StartDate(), reverse=True)
            
            for reset in resets:
                LOGGER.debug("Processing reset '%s', ResetType: %s, StartDate: %s, EndDate: %s",
                             reset.Oid(), reset.ResetType(), reset.StartDate(), reset.EndDate())
                if reset.ResetType() == 'Nominal Scaling':
                    result = reset.FixingValue()
        
        return result


class PBSwapProjectedDividendsLeg(PBPswapDenominated):
    def __init__(self, start_date=None, end_date=None):
        super(PBSwapProjectedDividendsLeg, self).__init__(start_date, end_date, None, False)

    def get_dividend(self, leg):
        super(PBSwapProjectedDividendsLeg, self).get_dividend(leg)
        result = 0
        
        cfs = self.get_live_cashflows(leg, self.start_date, self.end_date, cf_types=['Dividend'])
        
        max_date = self.end_date
        for cf in cfs:
            if cf.PayDate() <= self.end_date:
                continue
            LOGGER.debug("Cash flow: %s + %s = %s", result, cf.FixedAmount(), result + cf.FixedAmount())
            if cf.PayDate() > self.end_date:
                max_date = cf.PayDate()
        
        return self.get_denominated_value(leg, result)


def _get_value(pb_pswap_calc, leg):
    result = pb_pswap_calc.get_default_value(leg)
    try:
        leg = PBLegProxy.loader(leg)
        leg_type = LegType(leg)
        if leg_type == "MTM":
            result = pb_pswap_calc.get_mtm(leg)
        if leg_type == "Dividend":
            result = pb_pswap_calc.get_dividend(leg)
        if leg_type == "Execution Fee":
            result = pb_pswap_calc.get_execution_premium(leg)
        if leg_type == "Short Premium":
            result = pb_pswap_calc.get_short_premium(leg)
        if leg_type == "Overnight Premium":
            result = pb_pswap_calc.get_overnight_premium(leg)
        
        LOGGER.debug("Unexpected leg type: %s", leg_type)
    except:
        LOGGER.debug("Failed to calculate the value.", exc_info=1)
    
    LOGGER.debug("Result: %s", result)
    return result


def get_cash_leg(leg, start_date=None, end_date=None, *args):
    LOGGER.debug("%s %s %s %s", "*"*25, "Cash", leg.Oid(), "*"*25)
    pb_pswap_calc = PBSwapCashLeg(start_date, end_date)
    return _get_value(pb_pswap_calc, leg)


def get_val_leg(leg, start_date=None, end_date=None, *args):
    LOGGER.debug("%s %s %s %s", "*"*25, "Val", leg.Oid(), "*"*25)
    pb_pswap_calc = PBSwapValLeg(start_date, end_date)
    return _get_value(pb_pswap_calc, leg)


def get_val_leg_market(leg, start_date=None, end_date=None, market_price=None, *args):
    LOGGER.debug("%s %s %s %s", "*"*25, "Val", leg.Oid(), "*"*25)
    if market_price is None:
        market_price = 0
    else:
        market_price = market_price.Number()
    pb_pswap_calc = PBSwapValLeg(start_date, end_date, market_price)
    return _get_value(pb_pswap_calc, leg)


def get_open_value_leg(leg, start_date=None, end_date=None, *args):
    LOGGER.debug("%s %s %s %s", "*"*25, "Open Value", leg.Oid(), "*"*25)
    pb_pswap_calc = PBSwapOpenValueLeg(start_date, end_date)
    return _get_value(pb_pswap_calc, leg)


def get_total_value_leg(leg, start_date=None, end_date=None, *args):
    LOGGER.debug("%s %s %s %s", "*"*25, "Total Value", leg.Oid(), "*"*25)
    pb_pswap_calc = PBSwapTotalValueLeg(start_date, end_date)
    return _get_value(pb_pswap_calc, leg)


def get_forward_value_leg(leg, start_date=None, end_date=None, *args):
    LOGGER.debug("%s %s %s %s", "*"*25, "Forward Value", leg.Oid(), "*"*25)
    pb_pswap_calc = PBSwapForwardValueLeg(start_date, end_date)
    return _get_value(pb_pswap_calc, leg)


def get_upl_adjustment_leg(leg, start_date=None, end_date=None, *args):
    LOGGER.debug("%s %s %s %s", "*"*25, "Upl Adjustment", leg.Oid(), "*"*25)
    pb_pswap_calc = PBSwapOpenValueLeg(start_date, end_date)
    return _get_value(pb_pswap_calc, leg)


def get_dividends_leg(leg, start_date=None, end_date=None, *args):
    LOGGER.debug("%s %s %s %s", "*"*25, "Dividends", leg.Oid(), "*"*25)
    pb_pswap_calc = PBSwapDividendsLeg(start_date, end_date)
    return _get_value(pb_pswap_calc, leg)


def get_projected_dividends_leg(leg, start_date=None, end_date=None, *args):
    LOGGER.debug("%s %s %s %s", "*"*25, "Projected Dividends", leg.Oid(), "*"*25)
    pb_pswap_calc = PBSwapProjectedDividendsLeg(start_date, end_date)
    return _get_value(pb_pswap_calc, leg)


def get_nominal_factor_leg(leg, start_date=None, end_date=None, *args):
    LOGGER.debug("%s %s %s %s", "*"*25, "Nominal Factor", leg.Oid(), "*"*25)
    pb_pswap_calc = PBSwapNominalFactorLeg(start_date, end_date)
    return _get_value(pb_pswap_calc, leg)

