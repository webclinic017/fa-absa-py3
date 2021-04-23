import acm
from at_logging import getLogger

logger = getLogger(__name__)


class GenerateDividendCashFlow:

    def __init__(self, instrument, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.instrument = instrument

    def get_leg_by_type(self, leg_type):
        for l in self.instrument.Legs():
            if l.LegType() == leg_type:
                if leg_type == 'Fixed' and l.PayLeg():
                    return l
                elif leg_type != 'Fixed':
                    return l
        return None

    def get_ex_day_dividend(self, leg):
        logger.info("Accessing underlying stock")
        dividends = leg.IndexRef().Dividends()
        dividends_length = len(dividends)
        i = dividends_length - 1
        while i > 0:
            ex_day = dividends[i].ExDivDay()
            if self.start_date <= ex_day <= self.end_date:
                return dividends[i]
            i = i - 1
        raise Exception("No dividends issued between  {} and {}".format(self.start_date, self.end_date))

    def create_cash_flow(self, leg, dividend):
        try:
            logger.info("Creating cashflow")
            cashflow = leg.CreateCashFlow()
            cashflow.CashFlowType(15)
            cashflow.FixedAmount(dividend.Amount())
            cashflow.StartDate(dividend.ExDivDay())
            cashflow.EndDate(dividend.RecordDay())
            cashflow.PayDate(dividend.PayDay())
            cashflow.NominalFactor(self.instrument.DividendFactor())
            cashflow.Commit()
        except Exception as e:
            logger.error('Failed to generate cashflow {}'.format(e))

    def get_dividend_leg(self, leg):
        fixed_leg = self.get_leg_by_type('Fixed')
        if fixed_leg is not None:
            return fixed_leg
        else:
            try:
                logger.info("Using new leg")
                fixed_leg = self.instrument.CreateLeg(True)
                fixed_leg.LegType(1)
                fixed_leg.ResetType(0)
                fixed_leg.NominalScaling(8)
                fixed_leg.IndexRef(leg.IndexRef())
                fixed_leg.FloatRateReference(leg.FloatRateReference())
                fixed_leg.AmortDaycountMethod(leg.AmortDaycountMethod())
                fixed_leg.AmortPeriodCount(leg.AmortPeriodCount())
                fixed_leg.AmortPeriodUnit(leg.AmortPeriodUnit())
                fixed_leg.AmortEndDay(leg.AmortEndDay())
                fixed_leg.Currency(leg.Currency())
                fixed_leg.DayCountMethod(leg.DayCountMethod())
                fixed_leg.EndDate(leg.EndDate())
                fixed_leg.EndPeriodCount(leg.EndPeriodCount())
                fixed_leg.EndPeriodUnit(leg.EndPeriodUnit())
                fixed_leg.RollingPeriodBase(leg.RollingPeriodBase())
                fixed_leg.RollingPeriodCount(leg.RollingPeriodCount())
                fixed_leg.RollingPeriodUnit(leg.RollingPeriodUnit())
                fixed_leg.Commit()
                return fixed_leg
            except Exception as e:
                logger.error('Failed to generate dividend leg {}'.format(e))

    def cash_flow_exists(self):
        fixed_leg = self.get_leg_by_type('Fixed')
        if fixed_leg is None:
            return False
        else:
            for flow in fixed_leg.CashFlows():
                if (self.start_date <= flow.StartDate() <= self.end_date) and (flow.CashFlowType() == 'Dividend'):
                    return True
        return False

    def generate_dividend_cash_flow(self):
        try:
            total_return_leg = self.get_leg_by_type('Total Return')
            dividend = self.get_ex_day_dividend(total_return_leg)
            dividend_leg = self.get_dividend_leg(total_return_leg)
            self.create_cash_flow(dividend_leg, dividend)
            logger.info("Successfully generated dividend using fail safe method")
        except Exception as e:
            logger.error('Failed to save cashFlow leg {}'.format(e))

