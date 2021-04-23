"""-----------------------------------------------------------------------------
MODULE                  :       FAAggregateCommodityTradePNL
PURPOSE                 :       Automatically aggregate commodity trade PNL into a trade

HISTORY
================================================================================
Date            change no       Developer            Description
--------------------------------------------------------------------------------
2020-11-09                      Teboho Lepele        Initial Implementation
"""

import acm
from at_logging import getLogger
from at_ael_variables import AelVariableHandler
from FTradeCreator import DecoratedTradeCreator
import datetime

ACM_CALC = acm.Calculations()
STD_CALC_SPACE_COLLECTION = ACM_CALC.CreateStandardCalculationsSpaceCollection()
DATETODAY = acm.Time.DateToday()
LOGGER = getLogger(__name__)


class GroupTrades:

    def __init__(self, filter):
        self.trades = filter.Trades()

    def group_trades(self):
        portfolio_names = {trade.Portfolio().Name() for trade in self.trades}
        # group trades by portfolio
        for portfolio_name in portfolio_names:
            trade_list = []
            for trade in self.trades:
                if trade.Portfolio().Name() == portfolio_name:
                    trade_list.append(trade)
            yield (trade_list, portfolio_name)

    # sum projected values by portfolio
    def get_projected_value_sum(self):
        sum_projected_val = 0
        projected_val_sums = dict()
        for trades in self.group_trades():
            for trade in trades[0]:
                for money_flow in trade.MoneyFlows():
                    trade_date = self.get_trade_date(money_flow)
                    # only usd cashflows with a paydate or
                    # previous business days when payment is back dated
                    if str(money_flow.PayDate()) == str(DATETODAY) or self.is_back_dated(money_flow):
                        if money_flow.Currency().Name() != 'USD':
                            continue
                        calc_value = money_flow.Calculation().Projected(STD_CALC_SPACE_COLLECTION)
                        if type(calc_value) == int:
                            value = float(calc_value)
                        else:
                            value = calc_value.Value().Number()
                        sum_projected_val += value
            projected_val_sums[trades[1]] = sum_projected_val
            sum_projected_val = 0
        return projected_val_sums

    def is_back_dated(self, money_flow):
        trade_date = acm.Time.AsDate(money_flow.Trade().TradeTime())
        acquirer_day = money_flow.Trade().AcquireDay()
        if (str(trade_date) == str(DATETODAY) or str(acquirer_day) == str(DATETODAY)) and \
                str(money_flow.PayDate()) == str(self.get_previous_business_day(money_flow)):
            return True
        return False

    def get_previous_business_day(self, money_flow):
        return money_flow.Currency().Calendar().AdjustBankingDays(DATETODAY, -1)

    def get_trade_date(self, money_flow):
        cont = acm.GetDefaultContext()
        cal_space = acm.Calculations().CreateCalculationSpace(cont, 'FMoneyFlowSheet')
        time = cal_space.CalculateValue(money_flow, 'Cash Analysis Trade Time')
        return acm.Time.AsDate(time)


class CreateFXTrade:

    def __init__(self, portfolio, amount, acquirer, instrument='USD', currency='ZAR'):
        self.cty_portfolio = portfolio
        self.pv_sum = amount
        self.acquirer = acquirer
        self.instrument = instrument
        self.currency = currency

    def get_price(self, instrument, currency):
        usd_prices = acm.FCurrency[instrument].Prices()
        for price in usd_prices:
            if price.Market().Name() == 'SPOT' and price.Currency().Name() == currency and price.Day() == DATETODAY:
                return price.Settle()

    def get_spot_rate(self):
        fx_rate = acm.FCurrency['USD'].Calculation().FXRate(STD_CALC_SPACE_COLLECTION, acm.FCurrency['ZAR'],
                                                            acm.Time.DateToday()).Number()
        return round(fx_rate, 6)

    def format_trade_dict(self):
        formatted_dict = dict()
        formatted_dict['Instrument'] = self.instrument
        formatted_dict['Currency'] = self.currency
        formatted_dict['Quantity'] = float(self.pv_sum)
        formatted_dict['Portfolio'] = self.get_portfolio(self.cty_portfolio)
        formatted_dict['Counterparty'] = str(self.acquirer)
        formatted_dict['Acquirer'] = str(self.acquirer)
        formatted_dict['MirrorPortfolio'] = self.cty_portfolio
        formatted_dict['ValueDay'] = str(DATETODAY)
        formatted_dict['AcquireDay'] = str(DATETODAY)
        formatted_dict['Price'] = self.get_spot_rate()
        formatted_dict['Type'] = 'Normal'
        formatted_dict['TradeProcess'] = 8192
        formatted_dict['DiscountingType'] = 'CCYBasis'
        formatted_dict['ReferencePrice'] = self.get_price(self.instrument, self.currency)
        return formatted_dict

    def get_portfolio(self, portfolio_name):
        params = acm.GetDefaultContext().GetExtension('FParameters', 'FObject', 'MetalPortfolioGroups')
        params = params.Value()
        return params.At(portfolio_name)

    def _process_record(self):
        try:
            formatted_dict = self.format_trade_dict()
            creator = DecoratedTradeCreator(formatted_dict)
            trade = creator.CreateTrade()
            trade.Commit()
            LOGGER.info("Successfully booked FX Cash trade {}".format(trade.Oid()))
        except Exception as exc:
            msg = 'Failed to save trade: {}'.format(exc)
            LOGGER.exception(msg)


ael_variables = AelVariableHandler()

ael_variables.add('filter',
                  cls=acm.FTradeSelection,
                  collection=acm.FTradeSelection.Instances(),
                  label='Filter',
                  mandatory=True,
                  default=acm.FTradeSelection['Metals Filter NS'])

ael_variables.add('acquirer',
                  label='Acquirer',
                  cls=acm.FParty,
                  collection=acm.FParty.Select(''),
                  mandatory=True,
                  default=acm.FParty['Gold Desk'])


def ael_main(ael_dict):
    try:
        trade_groupings = GroupTrades(ael_dict['filter'])
        projected_sum = trade_groupings.get_projected_value_sum()
        for portfolio, aggregate_val in projected_sum.items():
            if aggregate_val == 0:
                continue
            party = ael_dict['acquirer']
            trade_creator = CreateFXTrade(portfolio, aggregate_val, str(party.Name()))
            trade_creator._process_record()
    except Exception as exc:
        LOGGER.error(exc)
