"""-----------------------------------------------------------------------------
PURPOSE              :  Client Valuation Statements Automation
                        Calculation logic corresponding to each statement type.
DESK                 :  PCG Collateral
DEVELOPER            :  Libor Svoboda
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no      Developer           Description
--------------------------------------------------------------------------------
2019-02-14  CHG1001362755  Libor Svoboda       Initial Implementation (FEC)
2019-03-14  CHG1001488095  Libor Svoboda       Enable Option statements
2019-04-12  CHG1001590405  Libor Svoboda       Enable Swap, Cap & Floor, and 
                                               Structured Deal statements
2019-05-30  CHG1001814126  Libor Svoboda       Update revaluation rate logic
2019-06-14  CHG1001881233  Libor Svoboda       Update FEC layout
2019-10-01  FAU-444        Libor Svoboda       EnumPLEndDate issue workaround
2019-12-12  CHG0072409     Libor Svoboda       Update FEC statement buy/sell
2020-06-03  CHG0103217     Libor Svoboda       Add SBL client statements
2020-10-20  CHG0132720     Libor Svoboda       Enable Deposit statements
"""
from collections import defaultdict, OrderedDict
from math import isnan

import acm

import sl_functions
from at_logging import getLogger
from statements_params import REPORTING_CURR, DATE_PATTERN_VALUES, VALID_SBL_STATUS
from statements_util import (date_to_dt, float_to_percent, float_ignore_none,
                             int_allow_blank, first_day_of_month,
                             last_day_of_month, get_steps, get_first_step)
from PS_BrokerFeesRates import get_vat_for_date


LOGGER = getLogger(__name__)
CALENDAR = acm.FCalendar['ZAR Johannesburg']
CALC_SPACE_TRD = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 
                                                           'FTradeSheet')
CALC_SPACE_MF = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 
                                                          'FMoneyFlowSheet')
CALC_SPACE_PRF = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 
                                                           'FPortfolioSheet')
CALC_SPACE_STD = acm.Calculations().CreateStandardCalculationsSpaceCollection()

DATE_TODAY = acm.Time.DateToday()
CALC_SPACE_MF.SimulateGlobalValue('Valuation Date', DATE_TODAY) 
CALC_SPACE_MF.SimulateGlobalValue('Portfolio Profit Loss End Date', 
                                  'Custom Date')
CALC_SPACE_MF.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', 
                                  DATE_TODAY)
CALC_SPACE_TRD.SimulateGlobalValue('Valuation Date', DATE_TODAY) 
CALC_SPACE_TRD.SimulateGlobalValue('Portfolio Profit Loss End Date', 
                                   'Custom Date')
CALC_SPACE_TRD.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', 
                                   DATE_TODAY)
CALC_SPACE_PRF.SimulateGlobalValue('Valuation Date', DATE_TODAY) 
CALC_SPACE_PRF.SimulateGlobalValue('Portfolio Profit Loss End Date', 
                                   'Custom Date')
CALC_SPACE_PRF.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', 
                                   DATE_TODAY)


def calc_trade_value(trade, val_date, column_id):
    CALC_SPACE_TRD.Clear()
    CALC_SPACE_TRD.SimulateGlobalValue('Valuation Date', val_date) 
    CALC_SPACE_TRD.SimulateGlobalValue('Portfolio Profit Loss End Date', 
                                       'Custom Date')
    CALC_SPACE_TRD.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', 
                                       val_date)
    return CALC_SPACE_TRD.CalculateValue(trade, column_id)


class Calculator(object):
    
    translate_conv = {
        date_to_dt: 'datetime',
        float: 'float',
        float_ignore_none: 'float',
        str: 'string',
        int: 'int',
        float_to_percent: 'percent',
        int_allow_blank: 'int',
    }
    fx_currencies = ['USD', 'GBP', 'EUR']
    internal = acm.FParty['internal']
    column_params = {}
    store_raw_values = False
    
    def __init__(self, trades, val_date, bp):
        self._trades = trades
        self._val_date = val_date
        self._log_str = '%s, %s' % (bp.Subject().Name(), bp.Oid())
    
    @staticmethod
    def get_log_str(calc_object):
        return 'trade %s' % calc_object.Oid()
    
    @staticmethod
    def get_row_id(calc_object):
        return '%011d' % calc_object.Oid()
    
    @staticmethod
    def used_price(ins, date, curr=None, price_find_type='', market=None):
        acm_dict = acm.FDictionary()
        acm_dict['priceDate'] = date
        if curr:
            acm_dict['currency'] = curr
        if price_find_type:
            if price_find_type in ('Ask', 'Bid'):
                acm_dict['typeOfPrice'] = 'Average' + price_find_type + 'Price'
            else:
                acm_dict['typeOfPrice'] = price_find_type + 'Price'
        if market:
            acm_dict['marketPlace'] = market
            acm_dict['useSpecificMarketPlace'] = True
        market_price = ins.Calculation().MarketPriceParams(CALC_SPACE_STD, acm_dict)
        return market_price.Value().Number()
    
    @staticmethod
    def fx_forward_price(curr1, curr2, val_date, forward_date, market=None):
        yc1 = curr1.Calculation().HistoricalDiscountCurve(CALC_SPACE_STD, val_date, True)
        yc2 = curr2.Calculation().HistoricalDiscountCurve(CALC_SPACE_STD, val_date, True)
        spot_price = Calculator.used_price(curr1, val_date, curr2, market=market)
        curr_pair = curr1.CurrencyPair(curr2)
        spot_date = curr_pair.SpotDate(val_date)
        df1 = yc1.Discount(spot_date, forward_date)
        df2 = yc2.Discount(spot_date, forward_date)
        return spot_price * df1 / df2
    
    @classmethod
    def update_column_params(cls, columns):
        for column_name, column_params in cls.column_params.items():
            if column_name in columns:
                columns[column_name].update(column_params)
    
    def _skip_calculation(self, calc_object):
        return False
    
    def _columns(self):
        raise NotImplementedError
    
    def _calc_objects(self):
        return self._trades
    
    def calculate(self):
        summary = defaultdict(float)
        summary_labels = [label for (label, spec) in self._columns().items()
                              if 'summary' in spec and spec['summary']]
        values = defaultdict(lambda: defaultdict(str))
        for calc_object in self._calc_objects():
            if self._skip_calculation(calc_object):
                continue
            row_id = self.get_row_id(calc_object)
            log_str = self.get_log_str(calc_object)
            for label, spec in self._columns().items():
                calc_func = spec['calc']
                conversion = spec['conv']
                pattern = spec['pattern'] if 'pattern' in spec else '{}'
                try:
                    value = conversion(calc_func(calc_object))
                except:
                    msg = ('Failed to calculate "%s" for %s.' 
                           % (label, log_str))
                    LOGGER.exception('%s: %s' % (self._log_str, msg))
                    raise RuntimeError(msg)
                if (conversion in (float, float_to_percent, float_ignore_none) 
                        and isnan(value)):
                    msg = ('Failed to calculate "%s" for %s, value is nan.' 
                           % (label, log_str))
                    LOGGER.error('%s: %s' % (self._log_str, msg))
                    raise RuntimeError(msg)
                
                if (('skip_report' in spec and spec['skip_report'])
                        or self.store_raw_values):
                    values[row_id][label] = value
                else:
                    values[row_id][label] = pattern.format(value)
                
                if label in summary_labels:
                    if self.store_raw_values:
                        summary[label] += float(value)
                        values['SUMMARY_RAW'][label] = summary[label]
                    else:
                        summary[label] += float(pattern.format(value).replace(',', ''))
                    values['SUMMARY'][label] = pattern.format(summary[label])
        LOGGER.info('%s: Values calculated successfully.' % self._log_str)
        return values
    
    def format_raw_values(self, values):
        patterns = {}
        for label, spec in self._columns().items():
            if 'skip_report' in spec and spec['skip_report']:
                continue
            patterns[label] = spec['pattern'] if 'pattern' in spec else '{}'
        
        for label in list(self._columns().keys()):
            if not label in patterns:
                continue
            pattern = patterns[label]
            for row_id in list(values.keys()):
                if 'SUMMARY' in row_id:
                    continue
                values[row_id][label] = pattern.format(values[row_id][label])
    
    def get_column_specs(self):
        specs = OrderedDict()
        for label, spec in self._columns().items():
            if 'skip_report' in spec and spec['skip_report']:
                continue
            specs[label] = {
                'width': spec['width'],
                'datatype': self.translate_conv[spec['conv']],
            }
        return specs
    
    def additional_values(self):
        values = defaultdict(lambda: defaultdict(str))
        for curr in self.fx_currencies:
            curr_pair = '%s/%s' % (REPORTING_CURR.Name(), curr)
            try:
                rate = self.used_price(acm.FCurrency[curr], self._val_date, 
                                       REPORTING_CURR, market=self.internal)
                rate = '{:.4f}'.format(rate)
            except:
                msg = 'Failed to get FX rate %s' % curr_pair
                LOGGER.exception('%s: %s' % (self._log_str, msg))
                raise RuntimeError(msg)
            values['FX Rates'][curr_pair] = rate
        LOGGER.info('%s: Additional values calculated successfully.' % self._log_str)
        return values
    
    
class FECCalculator(Calculator):
    
    mf_types = (
        'Premium',
        'Premium 2',
    )
    
    @staticmethod
    def get_deal_number(mf):
        trade = mf.Trade()
        deal_number = trade.YourRef()
        if trade.Counterparty().Name() == 'MIDAS DUAL KEY':
            try:
                deal_number = trade.AdditionalInfo().Source_Trade_Id().split('_')[1]
            except IndexError:
                deal_number = ''
        try:
            int(deal_number)
        except ValueError:
            return ''
        return deal_number
    
    @staticmethod
    def get_log_str(calc_object):
        return 'trade %s' % calc_object.Trade().Oid()
    
    @staticmethod
    def get_row_id(calc_object):
        return '%s_%011d_%s' % (calc_object.PayDay(), calc_object.Trade().Oid(), 
                                calc_object.Currency().Name())
    
    @staticmethod
    def _buy_or_sell(mf):
        base_ccy_amount = float(CALC_SPACE_MF.CalculateValue(mf, 'Cash Analysis Projected'))
        if base_ccy_amount < 0:
            return 'Sell'
        return 'Buy'
    
    @classmethod
    def get_rep_mf(cls, trade):
        for mf in trade.MoneyFlows():
            if mf.Type() in cls.mf_types and mf.Currency() == REPORTING_CURR:
                return mf
        return None
    
    def _skip_calculation(self, calc_object):
        if not calc_object.Type() in self.mf_types:
            return True
        if calc_object.Currency() == REPORTING_CURR:
            return True
        return False
    
    def _base_ccy_equiv(self, mf):
        trade = mf.Trade()
        rep_mf = self.get_rep_mf(trade)
        if rep_mf:
            return float(CALC_SPACE_MF.CalculateValue(rep_mf, 'Cash Analysis Projected'))
        projected = float(CALC_SPACE_MF.CalculateValue(mf, 'Cash Analysis Projected'))
        face_value = float(CALC_SPACE_MF.CalculateValue(mf, 'DDM Face Value REP CCY'))
        if projected == 0.0:
            return abs(face_value)
        return -1 * abs(face_value) * projected / abs(projected)
    
    def _exchange_rate(self, mf):
        trade = mf.Trade()
        if (not trade.Currency() == REPORTING_CURR
                and not trade.Instrument() == REPORTING_CURR):
            return trade.Price()
        cp = trade.Instrument().CurrencyPair(trade.Currency())
        if (cp.Currency1() == trade.Instrument() 
                and cp.Currency1() == REPORTING_CURR):
            return 1.0 / trade.Price()
        return trade.Price()
    
    def _revaluation_rate(self, mf):
        trade = mf.Trade()
        value_day = trade.ValueDay()
        if (not trade.Currency() == REPORTING_CURR
                and not trade.Instrument() == REPORTING_CURR):
            return self.fx_forward_price(mf.Currency(), REPORTING_CURR, 
                                         self._val_date, value_day, market=self.internal)
        cp = trade.Instrument().CurrencyPair(trade.Currency())
        forward_price = self.fx_forward_price(cp.Currency1(), cp.Currency2(), 
                                              self._val_date, value_day, market=self.internal)
        if cp.Currency1() == REPORTING_CURR:
            return 1.0 / forward_price
        return forward_price
    
    def _revalued_amount(self, mf):
       base_ccy_amount = float(CALC_SPACE_MF.CalculateValue(mf, 'Cash Analysis Projected'))
       reval_rate = self._revaluation_rate(mf)
       return -1 * float(reval_rate) * base_ccy_amount
    
    def _indicative_pnl(self, mf):
        indicative_pnl = self._base_ccy_equiv(mf) - self._revalued_amount(mf)
        return indicative_pnl
    
    def _pv_on_indicative_pnl(self, mf):
        trade = mf.Trade()
        rep_mf = self.get_rep_mf(trade)
        if rep_mf:
            return CALC_SPACE_TRD.CalculateValue(trade, 
                                                 'DDM Present Value REP CCY')
        return CALC_SPACE_MF.CalculateValue(mf, 'DDM Present Value REP CCY')
    
    def _columns(self):
        return OrderedDict([
            ('Deal Number', {
                'calc': self.get_deal_number,
                'conv': int_allow_blank,
                'width': '1.1cm',
            }),
            ('Reference', {
                'calc': lambda mf: mf.Trade().Oid(),
                'conv': int,
                'width': '1.7cm',
            }),
            ('Trade Date', {
                'calc': lambda mf: mf.Trade().ExecutionDate(),
                'conv': date_to_dt,
                'width': '1.8cm',
                'pattern': '{:%s}' % DATE_PATTERN_VALUES,
            }),
            ('Maturity Date', {
                'calc': lambda mf: mf.PayDay(),
                'conv': date_to_dt,
                'width': '1.8cm',
                'pattern': '{:%s}' % DATE_PATTERN_VALUES,
            }),
            ('CCY', {
                'calc': lambda mf: mf.Currency().Name(),
                'conv': str,
                'width': '1.1cm',
            }),
            ('Base CCY Amount', {
                'calc': lambda mf: CALC_SPACE_MF.CalculateValue(mf, 'Cash Analysis Projected'),
                'conv': float,
                'width': '2.5cm',
                'pattern': '{:,.2f}',
            }),
            ('Exchange Rate', {
                'calc': self._exchange_rate,
                'conv': float,
                'width': '1.5cm',
                'pattern': '{:.5f}',
            }),
            ('Base CCY Equivalent', {
                'calc': self._base_ccy_equiv,
                'conv': float,
                'width': '2.5cm',
                'pattern': '{:,.2f}',
            }),
            ('Revaluation Rate', {
                'calc': self._revaluation_rate,
                'conv': float,
                'width': '1.8cm',
                'pattern': '{:.5f}',
            }),
            ('Revalued Amount (ZAR)', {
                'calc': self._revalued_amount,
                'conv': float,
                'width': '2.6cm',
                'pattern': '{:,.2f}',
            }),
            ('Indicative P/L', {
                'calc': self._indicative_pnl,
                'conv': float,
                'width': '2.7cm',
                'pattern': '{:,.2f}',
            }),
            ('PV on Indicative P/L (ZAR)', {
                'calc': self._pv_on_indicative_pnl,
                'conv': float,
                'width': '2.7cm',
                'pattern': '{:,.2f}',
                'summary': True,
            }),
            ('ABSA Buys/Sells', {
                'calc': self._buy_or_sell,
                'conv': str,
                'width': '1.6cm',
            }),
            ('Days to Maturity', {
                'calc': lambda mf: acm.Time.DateDifference(mf.PayDay(), self._val_date),
                'conv': int,
                'width': '1.4cm',
            }),
        ])
    
    def _calc_objects(self):
        return [mf for trade in self._trades for mf in trade.MoneyFlows()]


class OptionCalculator(Calculator):
    
    underlying_mapping = {}
    
    @classmethod
    def get_underlying(cls, trade):
        underlying = str(trade.Instrument().Underlying().Name())
        try:
            return cls.underlying_mapping[underlying]
        except KeyError:
            return underlying


class EquityOptionCalculator(OptionCalculator):
    
    underlying_mapping = {
        'ZAR/Dummy': 'ZAR',
    }
    
    def _columns(self):
        return OrderedDict([
            ('Reference', {
                'calc': lambda t: t.Oid(),
                'conv': int,
                'width': '1.6cm',
            }),
            ('Product', {
                'calc': self.get_underlying,
                'conv': str,
                'width': '2.2cm',
            }),
            ('Call/Put', {
                'calc': lambda t: t.Instrument().OptionType(),
                'conv': str,
                'width': '1.3cm',
            }),
            ('Acquire Date', {
                'calc': lambda t: t.AcquireDay(),
                'conv': date_to_dt,
                'width': '1.8cm',
                'pattern': '{:%s}' % DATE_PATTERN_VALUES,
            }),
            ('Expiry Date', {
                'calc': lambda t: t.Instrument().ExpiryDate()[:10],
                'conv': date_to_dt,
                'width': '1.8cm',
                'pattern': '{:%s}' % DATE_PATTERN_VALUES,
            }),
            ('Currency', {
                'calc': lambda t: t.Currency().Name(),
                'conv': str,
                'width': '1.5cm',
            }),
            ('Nominal', {
                'calc': lambda t: CALC_SPACE_TRD.CalculateValue(t, 'DDM Face Value TXN CCY'),
                'conv': float,
                'width': '2.3cm',
                'pattern': '{:,.2f}',
            }),
            ('Strike Price', {
                'calc': lambda t: t.Instrument().StrikePrice(),
                'conv': float,
                'width': '1.9cm',
                'pattern': '{:,.4f}',
            }),
            ('Interest Rate', {
                'calc': lambda t: CALC_SPACE_TRD.CalculateValue(t, 'Portfolio Discount Rate'),
                'conv': float_ignore_none,
                'width': '1.4cm',
                'pattern': '{:.4f}',
            }),
            ('Spot Price', {
                'calc': lambda t: CALC_SPACE_TRD.CalculateValue(t, 'Underlying Spot OTC'),
                'conv': float,
                'width': '1.9cm',
                'pattern': '{:,.4f}',
            }),
            ('ABSA Buys/Sells', {
                'calc': lambda t: CALC_SPACE_TRD.CalculateValue(t, 'Bought or Sold'),
                'conv': str,
                'width': '1.6cm',
            }),
            ('Volatility', {
                'calc': lambda t: CALC_SPACE_TRD.CalculateValue(t, 'Portfolio Volatility'),
                'conv': float_to_percent,
                'width': '1.5cm',
                'pattern': '{:.2f}%',
            }),
            ('MTM', {
                'calc': lambda t: CALC_SPACE_TRD.CalculateValue(t, 'DDM Present Value TXN CCY'),
                'conv': float,
                'width': '2.5cm',
                'pattern': '{:,.2f}',
            }),
            ('MTM (ZAR)', {
                'calc': lambda t: CALC_SPACE_TRD.CalculateValue(t, 'DDM Present Value REP CCY'),
                'conv': float,
                'width': '2.5cm',
                'pattern': '{:,.2f}',
                'summary': True,
            }),
        ])


class EquityOptionCalculatorZAR(EquityOptionCalculator):
    
    column_params = {
        'Reference': {'width': '1.6cm'},
        'Product': {'width': '2.5cm'},
        'Call/Put': {'width': '1.4cm'},
        'Acquire Date': {'width': '1.9cm'},
        'Expiry Date': {'width': '1.9cm'},
        'Currency': {'width': '1.6cm'},
        'Nominal': {'width': '2.5cm'},
        'Strike Price': {'width': '2.2cm'},
        'Interest Rate': {'width': '1.5cm'},
        'Spot Price': {'width': '2.2cm'},
        'ABSA Buys/Sells': {'width': '1.8cm'},
        'Volatility': {'width': '1.8cm'},
        'MTM (ZAR)': {'width': '2.9cm'},
    }
    
    def _columns(self):
        columns = super(EquityOptionCalculatorZAR, self)._columns()
        columns.pop('MTM')
        self.update_column_params(columns)
        return columns


class CommodityOptionCalculator(OptionCalculator):
    
    underlying_mapping = {
        'USD/ALUMINIUM_LME/FWD': 'Aluminium',
        'USD/BRENT_CRUDE_ICE/FWD': 'Crude Oil (Brent)',
        'USD/COAL_API4_NYMEX/FWD': 'Coal_API4',
        'USD/COPPER_LME/FWD': 'Copper',
        'USD/GASOIL_ICE/FWD': 'Gasoil',
        'USD/GO05CFS/FWD': 'HSFO 180 Cargoes FOB SGP',
        'USD/GO500PPMCFS/FWD': 'Gold',
        'USD/GOLD_COMEX/FWD': 'Gold',
        'London Gold Market Fixing PM': 'Gold',
        'USD/HSFO180Cargoes_PLATTS/FWD': 'HSFO 180 Cargoes FOB SGP',
        'USD/ICE_GASOIL/FWD': 'Gasoil',
        'USD/JET_CCN_Platts/FWD': 'JET_CCN_Platts',
        'USD/JET_KEROCFS_Platts/FWD': 'JET_KEROCFS',
        'USD/LEAD_LME/FWD': 'Lead',
        'USD/NICKEL_LME/FWD': 'Nickel',
        'USD/PALLADIUM_NYMEX/FWD': 'Palladium',
        'USD/PLATINUM_NYMEX/FWD': 'Platinum',
        'USD/SILVER_COMEX/FWD': 'Silver',
        'USD/TIN_LME/FWD': 'Aluminium',
        'USD/UD10CCN_PLATTS/FWD': 'UD10CCN',
        'USD/WTI_NYMEX/FWD': 'Crude Oil (WTI)',
        'USD/ZINC_LME/FWD': 'Zinc',
        'USD/COTTON/NYBOT': 'Cotton',
    }
    
    quotation_mapping = {
        'Brent Crude oil Bbl': 'Barrels',
        'WTI Crude oil bbl': 'Barrels',
    }
    
    @classmethod
    def get_quotation(cls, trade):
        quotation = str(trade.Instrument().Quotation().Name())
        try:
            return cls.quotation_mapping[quotation]
        except KeyError:
            return quotation
    
    def _columns(self):
        return OrderedDict([
            ('Reference', {
                'calc': lambda t: t.Oid(),
                'conv': int,
                'width': '1.6cm',
            }),
            ('Product', {
                'calc': self.get_underlying,
                'conv': str,
                'width': '2.9cm',
            }),
            ('Call/Put', {
                'calc': lambda t: t.Instrument().OptionType(),
                'conv': str,
                'width': '1.3cm',
            }),
            ('Acquire Date', {
                'calc': lambda t: t.AcquireDay(),
                'conv': date_to_dt,
                'width': '1.8cm',
                'pattern': '{:%s}' % DATE_PATTERN_VALUES,
            }),
            ('Expiry Date', {
                'calc': lambda t: t.Instrument().ExpiryDate()[:10],
                'conv': date_to_dt,
                'width': '1.8cm',
                'pattern': '{:%s}' % DATE_PATTERN_VALUES,
            }),
            ('Currency', {
                'calc': lambda t: t.Currency().Name(),
                'conv': str,
                'width': '1.5cm',
            }),
            ('Nominal', {
                'calc': lambda t: CALC_SPACE_TRD.CalculateValue(t, 'DDM Face Value TXN CCY'),
                'conv': float,
                'width': '2.4cm',
                'pattern': '{:,.2f}',
            }),
            ('Strike Price', {
                'calc': lambda t: t.Instrument().StrikePrice(),
                'conv': float,
                'width': '2.0cm',
                'pattern': '{:,.4f}',
            }),
            ('Spot Price', {
                'calc': lambda t: CALC_SPACE_TRD.CalculateValue(t, 'Underlying Spot OTC'),
                'conv': float,
                'width': '2.0cm',
                'pattern': '{:,.4f}',
            }),
            ('ABSA Buys/Sells', {
                'calc': lambda t: CALC_SPACE_TRD.CalculateValue(t, 'Bought or Sold'),
                'conv': str,
                'width': '1.5cm',
            }),
            ('Quotation', {
                'calc': self.get_quotation,
                'conv': str,
                'width': '2.0cm',
            }),
            ('MTM', {
                'calc': lambda t: CALC_SPACE_TRD.CalculateValue(t, 'DDM Present Value TXN CCY'),
                'conv': float,
                'width': '2.5cm',
                'pattern': '{:,.2f}',
            }),
            ('MTM (ZAR)', {
                'calc': lambda t: CALC_SPACE_TRD.CalculateValue(t, 'DDM Present Value REP CCY'),
                'conv': float,
                'width': '2.5cm',
                'pattern': '{:,.2f}',
                'summary': True,
            }),
        ])


class CommodityOptionCalculatorZAR(CommodityOptionCalculator):
    
    column_params = {
        'Reference': {'width': '1.6cm'},
        'Product': {'width': '3.6cm'},
        'Call/Put': {'width': '1.4cm'},
        'Acquire Date': {'width': '1.9cm'},
        'Expiry Date': {'width': '1.9cm'},
        'Currency': {'width': '1.6cm'},
        'Nominal': {'width': '2.7cm'},
        'Strike Price': {'width': '2.2cm'},
        'Spot Price': {'width': '2.2cm'},
        'ABSA Buys/Sells': {'width': '1.6cm'},
        'Quotation': {'width': '2.2cm'},
        'MTM (ZAR)': {'width': '2.9cm'},
    }
    
    def _columns(self):
        columns = super(CommodityOptionCalculatorZAR, self)._columns()
        columns.pop('MTM')
        self.update_column_params(columns)
        return columns


class FXOptionCalculator(OptionCalculator):
    
    def _columns(self):
        return OrderedDict([
            ('Reference', {
                'calc': lambda t: t.Oid(),
                'conv': int,
                'width': '1.6cm',
            }),
            ('Product', {
                'calc': lambda t: t.Instrument().Underlying().Name(),
                'conv': str,
                'width': '2.0cm',
            }),
            ('Call/Put', {
                'calc': lambda t: t.Instrument().OptionType(),
                'conv': str,
                'width': '1.6cm',
            }),
            ('Acquire Date', {
                'calc': lambda t: t.AcquireDay(),
                'conv': date_to_dt,
                'width': '2.3cm',
                'pattern': '{:%s}' % DATE_PATTERN_VALUES,
            }),
            ('Expiry Date', {
                'calc': lambda t: t.Instrument().ExpiryDate()[:10],
                'conv': date_to_dt,
                'width': '2.3cm',
                'pattern': '{:%s}' % DATE_PATTERN_VALUES,
            }),
            ('Currency', {
                'calc': lambda t: t.Instrument().Underlying().Name(),
                'conv': str,
                'width': '1.9cm',
            }),
            ('Nominal', {
                'calc': lambda t: CALC_SPACE_TRD.CalculateValue(t, 'DDM Face Value TXN CCY'),
                'conv': float,
                'width': '2.9cm',
                'pattern': '{:,.2f}',
            }),
            ('Strike Price', {
                'calc': lambda t: t.Instrument().StrikePrice(),
                'conv': float,
                'width': '2.2cm',
                'pattern': '{:,.4f}',
            }),
            ('Spot Price', {
                'calc': lambda t: CALC_SPACE_TRD.CalculateValue(t, 'Underlying Spot OTC'),
                'conv': float,
                'width': '2.2cm',
                'pattern': '{:,.4f}',
            }),
            ('ABSA Buys/Sells', {
                'calc': lambda t: CALC_SPACE_TRD.CalculateValue(t, 'Bought or Sold'),
                'conv': str,
                'width': '1.9cm',
            }),
            ('Volatility', {
                'calc': lambda t: CALC_SPACE_TRD.CalculateValue(t, 'Portfolio Volatility'),
                'conv': float_to_percent,
                'width': '2.0cm',
                'pattern': '{:.2f}%',
            }),
            ('MTM (ZAR)', {
                'calc': lambda t: CALC_SPACE_TRD.CalculateValue(t, 'DDM Present Value REP CCY'),
                'conv': float,
                'width': '2.9cm',
                'pattern': '{:,.2f}',
                'summary': True,
            }),
        ])


class SwapOptionCalculator(OptionCalculator):
    
    def _columns(self):
        return OrderedDict([
            ('Reference', {
                'calc': lambda t: t.Oid(),
                'conv': int,
                'width': '1.6cm',
            }),
            ('Product', {
                'calc': lambda t: t.Instrument().VerboseName(),
                'conv': str,
                'width': '6.1cm',
            }),
            ('Acquire Date', {
                'calc': lambda t: t.AcquireDay(),
                'conv': date_to_dt,
                'width': '1.9cm',
                'pattern': '{:%s}' % DATE_PATTERN_VALUES,
            }),
            ('Expiry Date', {
                'calc': lambda t: t.Instrument().ExpiryDate()[:10],
                'conv': date_to_dt,
                'width': '1.9cm',
                'pattern': '{:%s}' % DATE_PATTERN_VALUES,
            }),
            ('Currency', {
                'calc': lambda t: t.Currency().Name(),
                'conv': str,
                'width': '1.6cm',
            }),
            ('Nominal', {
                'calc': lambda t: CALC_SPACE_TRD.CalculateValue(t, 'DDM Face Value TXN CCY'),
                'conv': float,
                'width': '2.8cm',
                'pattern': '{:,.2f}',
            }),
            ('Strike Price', {
                'calc': lambda t: t.Instrument().StrikePrice(),
                'conv': float,
                'width': '2.0cm',
                'pattern': '{:,.4f}',
            }),
            ('Interest Rate', {
                'calc': lambda t: CALC_SPACE_TRD.CalculateValue(t, 'Portfolio Discount Rate'),
                'conv': float_ignore_none,
                'width': '1.5cm',
                'pattern': '{:.4f}',
            }),
            ('ABSA Buys/Sells', {
                'calc': lambda t: CALC_SPACE_TRD.CalculateValue(t, 'Bought or Sold'),
                'conv': str,
                'width': '1.8cm',
            }),
            ('Volatility', {
                'calc': lambda t: CALC_SPACE_TRD.CalculateValue(t, 'Portfolio Volatility'),
                'conv': float_to_percent,
                'width': '1.8cm',
                'pattern': '{:.2f}%',
            }),
            ('MTM (ZAR)', {
                'calc': lambda t: CALC_SPACE_TRD.CalculateValue(t, 'DDM Present Value REP CCY'),
                'conv': float,
                'width': '2.8cm',
                'pattern': '{:,.2f}',
                'summary': True,
            }),
        ])


class ValuationsDefaultCalculator(Calculator):
    
    def _notional(self, trade):
        face_value = CALC_SPACE_TRD.CalculateValue(trade, 'DDM Face Value TXN CCY')
        if face_value:
            return face_value
        return 0.0
    
    def _columns(self):
        return OrderedDict([
            ('Reference', {
                'calc': lambda t: t.Oid(),
                'conv': int,
                'width': '1.6cm',
            }),
            ('Instrument', {
                'calc': lambda t: t.Instrument().InsType(),
                'conv': str,
                'width': '3.3cm',
            }),
            ('Acquire Date', {
                'calc': lambda t: t.AcquireDay(),
                'conv': date_to_dt,
                'width': '2.7cm',
                'pattern': '{:%s}' % DATE_PATTERN_VALUES,
            }),
            ('Expiry Date', {
                'calc': lambda t: t.Instrument().ExpiryDate()[:10],
                'conv': date_to_dt,
                'width': '2.7cm',
                'pattern': '{:%s}' % DATE_PATTERN_VALUES,
            }),
            ('Currency', {
                'calc': lambda t: t.Currency().Name(),
                'conv': str,
                'width': '2.2cm',
            }),
            ('Notional', {
                'calc': self._notional,
                'conv': float,
                'width': '3.7cm',
                'pattern': '{:,.2f}',
            }),
            ('ABSA Buys/Sells', {
                'calc': lambda t: CALC_SPACE_TRD.CalculateValue(t, 'Bought or Sold'),
                'conv': str,
                'width': '2.2cm',
            }),
            ('MTM', {
                'calc': lambda t: CALC_SPACE_TRD.CalculateValue(t, 'DDM Present Value TXN CCY'),
                'conv': float,
                'width': '3.7cm',
                'pattern': '{:,.2f}',
            }),
            ('MTM (ZAR)', {
                'calc': lambda t: CALC_SPACE_TRD.CalculateValue(t, 'DDM Present Value REP CCY'),
                'conv': float,
                'width': '3.7cm',
                'pattern': '{:,.2f}',
                'summary': True,
            }),
        ])


class ValuationsDefaultCalculatorZAR(ValuationsDefaultCalculator):
    
    column_params = {
        'Reference': {'width': '1.6cm'},
        'Instrument': {'width': '3.4cm'},
        'Acquire Date': {'width': '3.3cm'},
        'Expiry Date': {'width': '3.3cm'},
        'Currency': {'width': '2.8cm'},
        'Notional': {'width': '4.3cm'},
        'ABSA Buys/Sells': {'width': '2.8cm'},
        'MTM (ZAR)': {'width': '4.3cm'},
    }
    
    def _columns(self):
        columns = super(ValuationsDefaultCalculatorZAR, self)._columns()
        columns.pop('MTM')
        self.update_column_params(columns)
        return columns


class StructuredCalculator(ValuationsDefaultCalculator):
    
    def _notional(self, trade):
        face_value = CALC_SPACE_TRD.CalculateValue(trade, 'DDM Face Value TXN CCY')
        if face_value:
            return face_value
        return CALC_SPACE_TRD.CalculateValue(trade, 'DDM Nominal TXN CCY')


class StructuredCalculatorZAR(StructuredCalculator):
    
    column_params = {
        'Reference': {'width': '1.6cm'},
        'Instrument': {'width': '3.4cm'},
        'Acquire Date': {'width': '3.3cm'},
        'Expiry Date': {'width': '3.3cm'},
        'Currency': {'width': '2.8cm'},
        'Notional': {'width': '4.3cm'},
        'ABSA Buys/Sells': {'width': '2.8cm'},
        'MTM (ZAR)': {'width': '4.3cm'},
    }
    
    def _columns(self):
        columns = super(StructuredCalculatorZAR, self)._columns()
        columns.pop('MTM')
        self.update_column_params(columns)
        return columns


class CurrSwapCalculator(Calculator):
    
    def _currency_1(self, trade):
        return trade.Instrument().PayLeg().Currency().Name()
    
    def _currency_2(self, trade):
        return trade.Instrument().RecLeg().Currency().Name()
    
    def _notional(self, trade, currency):
        notional = 0.0
        for mf in trade.MoneyFlows():
            if (mf.SourceObject().RecordType() == 'CashFlow' 
                    and mf.Currency().Name() == currency
                    and mf.PayDay() > self._val_date):
                notional += float(CALC_SPACE_MF.CalculateValue(mf, 'Cash Analysis Projected'))
        return notional
    
    def _notional_1(self, trade):
        currency = self._currency_1(trade)
        return self._notional(trade, currency)
    
    def _notional_2(self, trade):
        currency = self._currency_2(trade)
        return self._notional(trade, currency)
    
    def _columns(self):
        return OrderedDict([
            ('Reference', {
                'calc': lambda t: t.Oid(),
                'conv': int,
                'width': '1.6cm',
            }),
            ('Instrument', {
                'calc': lambda t: t.Instrument().InsType(),
                'conv': str,
                'width': '3.0cm',
            }),
            ('Acquire Date', {
                'calc': lambda t: t.AcquireDay(),
                'conv': date_to_dt,
                'width': '2.5cm',
                'pattern': '{:%s}' % DATE_PATTERN_VALUES,
            }),
            ('Expiry Date', {
                'calc': lambda t: t.Instrument().ExpiryDate()[:10],
                'conv': date_to_dt,
                'width': '2.5cm',
                'pattern': '{:%s}' % DATE_PATTERN_VALUES,
            }),
            ('Currency 1', {
                'calc': self._currency_1,
                'conv': str,
                'width': '2.0cm',
            }),
            ('Notional 1', {
                'calc': self._notional_1,
                'conv': float,
                'width': '3.4cm',
                'pattern': '{:,.2f}',
            }),
            ('Currency 2', {
                'calc': self._currency_2,
                'conv': str,
                'width': '2.0cm',
            }),
            ('Notional 2', {
                'calc': self._notional_2,
                'conv': float,
                'width': '3.4cm',
                'pattern': '{:,.2f}',
            }),
            ('ABSA Buys/Sells', {
                'calc': lambda t: CALC_SPACE_TRD.CalculateValue(t, 'Bought or Sold'),
                'conv': str,
                'width': '2.0cm',
            }),
            ('MTM (ZAR)', {
                'calc': lambda t: CALC_SPACE_TRD.CalculateValue(t, 'DDM Present Value REP CCY'),
                'conv': float,
                'width': '3.4cm',
                'pattern': '{:,.2f}',
                'summary': True,
            }),
        ])


class DepositCalculator(Calculator):
    
    def _interest_rate(self, trade):
        leg = trade.Instrument().Legs()[0]
        if not leg:
            return 0.0
        if leg.LegType() == 'Float' and leg.FloatRateReference():
            float_rate = self.used_price(leg.FloatRateReference(), 
                                         self._val_date, market=self.internal)
            return (float_rate + leg.Spread()) / 100
        return leg.FixedRate() / 100
    
    def _end_cash(self, trade):
        end_cash = 0.0
        for mf in trade.MoneyFlows():
            if (mf.SourceObject().RecordType() == 'CashFlow' 
                    and mf.PayDay() > self._val_date):
                end_cash += float(CALC_SPACE_MF.CalculateValue(mf, 'Cash Analysis Projected'))
        return end_cash
    
    def _funding_instype(self, trade):
        if trade.Instrument().InsType() == 'FRN':
            return 'FRN'
        return trade.AdditionalInfo().Funding_Instype()
    
    def _columns(self):
        return OrderedDict([
            ('Trade Number', {
                'calc': lambda t: t.Oid(),
                'conv': int,
                'width': '1.6cm',
            }),
            ('Execution Date', {
                'calc': lambda t: t.ExecutionDate(),
                'conv': date_to_dt,
                'width': '1.8cm',
                'pattern': '{:%s}' % DATE_PATTERN_VALUES,
            }),
            ('Acquire Date', {
                'calc': lambda t: t.AcquireDay(),
                'conv': date_to_dt,
                'width': '1.8cm',
                'pattern': '{:%s}' % DATE_PATTERN_VALUES,
            }),
            ('Expiry Date', {
                'calc': lambda t: t.Instrument().ExpiryDate()[:10],
                'conv': date_to_dt,
                'width': '1.8cm',
                'pattern': '{:%s}' % DATE_PATTERN_VALUES,
            }),
            ('CCY', {
                'calc': lambda t: t.Currency().Name(),
                'conv': str,
                'width': '1.1cm',
            }),
            ('ABSA Buys/Sells', {
                'calc': lambda t: CALC_SPACE_TRD.CalculateValue(t, 'Bought or Sold'),
                'conv': str,
                'width': '1.6cm',
            }),
            ('Funding InsType', {
                'calc': self._funding_instype,
                'conv': str,
                'width': '1.6cm',
            }),
            ('Interest Rate', {
                'calc': self._interest_rate,
                'conv': float,
                'width': '1.5cm',
                'pattern': '{:,.4f}',
            }),
            ('Settled Interest', {
                'calc': lambda t: CALC_SPACE_TRD.CalculateValue(t, 'Portfolio Settled Interest'),
                'conv': float,
                'width': '2.0cm',
                'pattern': '{:,.2f}',
                'summary': True,
            }),
            ('Annuity Payment', {
                'calc': lambda t: CALC_SPACE_TRD.CalculateValue(t, 'Trade Annuity Payment'),
                'conv': float,
                'width': '2.0cm',
                'pattern': '{:,.2f}',
                'summary': True,
            }),
            ('Accrued Interest', {
                'calc': lambda t: CALC_SPACE_TRD.CalculateValue(t, 'DDM Accrued Interest REP CCY'),
                'conv': float,
                'width': '2.5cm',
                'pattern': '{:,.2f}',
                'summary': True,
            }),
            ('End Cash', {
                'calc': self._end_cash,
                'conv': float,
                'width': '2.5cm',
                'pattern': '{:,.2f}',
                'summary': True,
            }),
            ('Nominal', {
                'calc': lambda t: CALC_SPACE_TRD.CalculateValue(t, 'DDM Nominal REP CCY'),
                'conv': float,
                'width': '2.5cm',
                'pattern': '{:,.2f}',
                'summary': True,
            }),
            ('MTM', {
                'calc': lambda t: CALC_SPACE_TRD.CalculateValue(t, 'DDM Present Value REP CCY'),
                'conv': float,
                'width': '2.5cm',
                'pattern': '{:,.2f}',
                'summary': True,
            }),
        ])


class SBLCalculator(Calculator):
    
    @staticmethod
    def is_loan(trade):
        return trade.Oid() == trade.Contract().Oid()
    
    @staticmethod
    def security_name(trade):
        instrument = trade.Instrument()
        instype = instrument.InsType()
        if instype == 'Deposit':
            return 'Cash'
        if instype in ('CD', 'Bill'):
            isin = instrument.Isin()
            if not isin:
                msg = 'Isin not specified for "%s".' % instrument.Name()
                raise RuntimeError(msg)
            return isin
        security = (instrument.Security().Name() 
                    if instype == 'SecurityLoan' else instrument.Name())
        try:
            return security.split('/')[1]
        except IndexError:
            return security
    
    @staticmethod
    def loan_quantity(trade):
        return abs(trade.Quantity() * trade.Instrument().RefValue())
    
    @staticmethod
    def loan_price(trade):
        quotation_factor = trade.Instrument().Quotation().QuotationFactor()
        return trade.AllInPrice() * quotation_factor 
    
    @staticmethod
    def loan_value(trade):
        return SBLCalculator.loan_quantity(trade) * SBLCalculator.loan_price(trade)
    
    @staticmethod
    def security_price(instrument, date):
        return (sl_functions.security_price(instrument, date)
                * instrument.Quotation().QuotationFactor())

    def market_value(self, trade):
        ins = trade.Instrument()
        if ins.InsType() == 'SecurityLoan':
            market_price = self.security_price(ins, self._val_date)
            if ins.Underlying().InsType() in ('Bond', 'IndexLinkedBond'):
                market_price = round(market_price / ins.Quotation().QuotationFactor(), 7)
            return market_price * self.loan_quantity(trade)
        return CALC_SPACE_TRD.CalculateValue(trade, 'SOB Market Value')
    
    def _get_summary_values(self, values, labels, row_ids=None):
        summary = defaultdict(str)
        summary_numeric = defaultdict(int)
        for row_id in values:
            if row_ids and not row_id in row_ids:
                continue
            for label, spec in self._columns().items():
                if label not in labels:
                    continue
                pattern = spec['pattern'] if 'pattern' in spec else '{}'
                conversion = spec['conv']
                value = values[row_id][label]
                if self.store_raw_values:
                    summary_numeric[label] += value
                else:
                    summary_numeric[label] += conversion(value.replace(',', ''))
                summary[label] = pattern.format(summary_numeric[label])
        return summary


class SBLFeeCalculator(SBLCalculator):
    
    subsummary_cols = (
        'Days',
        'Fee Excl Vat',
        'Vat',
        'Fee Incl Vat',
    )
    mf_types = (
        'Fixed Rate',
    )
    store_raw_values = True
    
    def __init__(self, trades, val_date, bp):
        super(SBLFeeCalculator, self).__init__(trades, val_date, bp)
        self._start_date = first_day_of_month(self._val_date)
        self._end_date = last_day_of_month(self._val_date)
        self._party = bp.Subject()
    
    @staticmethod
    def get_log_str(calc_object):
        return 'trade %s' % calc_object.Trade().Oid()
    
    @staticmethod
    def is_mtm(mf):
        return mf.Trade().Instrument().AdditionalInfo().SL_CFD()
    
    @staticmethod
    def find_minimum_fee_payments(trade, party):
        query = 'trade=%s and type="Cash" and party=%s and text="Minimum Fee"'
        return acm.FPayment.Select(query % (trade.Oid(), party.Oid()))
    
    def get_row_id(self, calc_object, flag='', date=''):
        if not flag:
            flag = self._activity(calc_object)
        if not date:
            date = calc_object.StartDate()
        trade = calc_object.Trade()
        return '%011d_%s_%s_%s' % (trade.Contract().Oid(), date, 
                                   trade.Oid(), flag)
    
    def _calc_objects(self):
        return [mf for trade in self._trades for mf in trade.MoneyFlows()]
    
    def _expiry_on_start_date(self, mf):
        return (mf.EndDate() == self._start_date
                and mf.EndDate() == mf.Trade().Instrument().ExpiryDateOnly())
    
    def _skip_calculation(self, calc_object):
        if not calc_object.Type() in self.mf_types:
            return True
        if self._expiry_on_start_date(calc_object):
            return False
        end_date = acm.Time.DateAddDelta(self._end_date, 0, 0, 1)
        if (calc_object.StartDate() < self._start_date 
                or calc_object.EndDate() > end_date):
            return True
        return False
    
    def _is_bfw(self, mf):
        if self._expiry_on_start_date(mf):
            return True
        return (mf.StartDate() == self._start_date 
                and mf.Trade().Instrument().StartDate() < self._start_date)
    
    def _activity(self, mf, flag=''):
        if flag:
            return flag
        if (self.is_loan(mf.Trade()) 
                and mf.StartDate() == mf.Trade().Instrument().StartDate()
                and mf.StartDate() >= self._start_date):
            return 'SL'
        if (mf.StartDate() == mf.Trade().Instrument().StartDate()
                and mf.StartDate() >= self._start_date):
            return 'SR'
        if self._is_bfw(mf) and not self.is_mtm(mf):
            return 'BFW'
        return 'M'
    
    def _trade_ref(self, mf, flag=''):
        if flag == 'BFW' or (not flag and self._activity(mf) in ('SL', 'BFW', 'SR')):
            return mf.Trade().Oid()
        return ''
    
    def _effective_date(self, mf, flag=''):
        if flag in ('SR', 'MIN FEE'):
            return mf.EndDate()
        if self._expiry_on_start_date(mf):
            return mf.EndDate()
        return mf.StartDate()
    
    @staticmethod
    def _security_name(mf, _flag=''):
        return SBLCalculator.security_name(mf.Trade())
    
    @staticmethod
    def _quantity(mf, flag=''):
        if flag in ('SR', 'MIN FEE'):
            return 0.0
        return SBLCalculator.loan_quantity(mf.Trade())
    
    def _price(self, mf, flag=''):
        if flag in ('SR', 'MIN FEE'):
            return 0.0
        if flag == 'BFW' or not self.is_mtm(mf):
            return self.loan_price(mf.Trade())
        instrument = mf.Trade().Instrument()
        return self.security_price(instrument, mf.StartDate())
    
    @staticmethod
    def _min_fee(mf, _flag=''):
        return mf.Trade().Instrument().AdditionalInfo().SL_Minimum_Fee()
    
    def _days_diff(self, mf, flag=''):
        if flag:
            return 0
        if self._expiry_on_start_date(mf):
            return 0
        return acm.Time.DateDifference(mf.EndDate(), mf.StartDate())
    
    def _fee_incl_vat(self, mf, flag=''):
        if flag == 'MIN FEE':
            payments = self.find_minimum_fee_payments(mf.Trade(), self._party)
            return abs(sum([payment.Amount() for payment in payments]))
        if flag:
            return 0.0
        if self._expiry_on_start_date(mf):
            return 0.0
        return abs(float(CALC_SPACE_MF.CalculateValue(mf, 'Cash Analysis Projected')))
    
    def _vat_rate(self):
        if self._party.AdditionalInfo().TAXABLE_STATUS():
            return get_vat_for_date(self._val_date)
        return 1.0
    
    def _rate(self, mf, _flag=''):
        return mf.Trade().Instrument().Legs()[0].FixedRate() / self._vat_rate()
    
    def _vat(self, mf, flag=''):
        if flag == 'MIN FEE':
            vat_rate = self._vat_rate()
            return self._fee_incl_vat(mf, flag) * (vat_rate - 1) / vat_rate
        if flag:
            return 0.0
        if self._expiry_on_start_date(mf) and flag != 'MIN FEE':
            return 0.0
        vat_rate = self._vat_rate()
        return self._fee_incl_vat(mf) * (vat_rate - 1) / vat_rate
    
    def _fee_excl_vat(self, mf, flag=''):
        if flag == 'MIN FEE':
            return self._fee_incl_vat(mf, flag) - self._vat(mf, flag)
        if flag:
            return 0.0
        return self._fee_incl_vat(mf) - self._vat(mf)
    
    def _columns(self):
        return OrderedDict([
            ('MoneyFlow', {
                'calc': lambda mf: mf,
                'conv': lambda mf: mf,
                'skip_report': True,
            }),
            ('ContractOid', {
                'calc': lambda mf: mf.Trade().Contract().Oid(),
                'conv': int,
                'skip_report': True,
            }),
            ('Trade Ref', {
                'calc': self._trade_ref,
                'conv': int_allow_blank,
                'width': '1.6cm',
            }),
            ('', {
                'calc': self._activity,
                'conv': str,
                'width': '1.1cm',
            }),
            ('Effective Date', {
                'calc': self._effective_date,
                'conv': date_to_dt,
                'width': '1.9cm',
                'pattern': '{:%s}' % DATE_PATTERN_VALUES,
            }),
            ('Security', {
                'calc': self._security_name,
                'conv': str,
                'width': '1.4cm',
            }),
            ('Quantity', {
                'calc': self._quantity,
                'conv': float,
                'width': '1.7cm',
                'pattern': '{:,.0f}',
            }),
            ('Price', {
                'calc': self._price,
                'conv': float,
                'width': '1.7cm',
                'pattern': '{:,.2f}',
            }),
            ('Rate', {
                'calc': self._rate,
                'conv': float,
                'width': '1.7cm',
                'pattern': '{:,.3f}',
            }),
            ('Min Fee', {
                'calc': self._min_fee,
                'conv': float,
                'width': '1.7cm',
                'pattern': '{:,.2f}',
            }),
            ('Days', {
                'calc': self._days_diff,
                'conv': int,
                'width': '1.1cm',
            }),
            ('Fee Excl Vat', {
                'calc': self._fee_excl_vat,
                'conv': float,
                'width': '1.7cm',
                'pattern': '{:,.2f}',
                'summary': True,
            }),
            ('Vat', {
                'calc': self._vat,
                'conv': float,
                'width': '1.7cm',
                'pattern': '{:,.2f}',
                'summary': True,
            }),
            ('Fee Incl Vat', {
                'calc': self._fee_incl_vat,
                'conv': float,
                'width': '1.7cm',
                'pattern': '{:,.2f}',
                'summary': True,
            }),
        ])
        
    @staticmethod
    def _is_full_return(mf):
        trade = mf.Trade()
        instrument = trade.Instrument()
        if mf.EndDate() != instrument.ExpiryDateOnly():
            return False
        contract = trade.Contract().Oid()
        trades = [t for t in acm.FTrade.Select('contract=%s' % contract)
                  if (t.Status() in VALID_SBL_STATUS 
                      and t.Text1() != 'FULL_RETURN')]
        if not trades:
            return False
        max_expiry = max([t.Instrument().ExpiryDateOnly() for t in trades])
        return mf.EndDate() == max_expiry
    
    def _apply_minimum_fee(self, mf):
        trade = mf.Trade()
        if not trade.Instrument().AdditionalInfo().SL_Minimum_Fee():
            return False
        payments = self.find_minimum_fee_payments(trade, self._party)
        if not payments:
            return False
        total_amount = sum([payment.Amount() for payment in payments])
        if total_amount:
            return True
        return False
    
    def _calculate_additional_row(self, mf, flag):
        values = defaultdict(str)
        for label, spec in self._columns().items():
            if 'skip_report' in spec and spec['skip_report']:
                continue
            calc_func = spec['calc']
            conversion = spec['conv']
            pattern = spec['pattern'] if 'pattern' in spec else '{}'
            calc_value = calc_func(mf, flag)
            value = conversion(calc_value)
            if self.store_raw_values:
                values[label] = value
            else:
                values[label] = pattern.format(value)
        return values
    
    def calculate(self):
        values = super(SBLFeeCalculator, self).calculate()
        row_grouper = defaultdict(list)
        additional_rows = []
        for row_id in list(values.keys()):
            if row_id in ('SUMMARY', 'SUMMARY_RAW'):
                continue
            row_grouper[int(values[row_id]['ContractOid'])].append(row_id)
            mf = values[row_id]['MoneyFlow']
            if self._is_bfw(mf) and self.is_mtm(mf):
                additional_rows.append((mf, 'BFW'))
            is_full_return = self._is_full_return(mf)
            if is_full_return and mf.EndDate() <= self._end_date:
                additional_rows.append((mf, 'SR'))
                if self._apply_minimum_fee(mf):
                    LOGGER.info('%s: Applying minimum fee for %s.' 
                                % (self._log_str, self.get_log_str(mf)))
                    additional_rows.append((mf, 'MIN FEE'))
            if (mf.EndDate() == mf.Trade().Instrument().ExpiryDateOnly()
                    and self.is_mtm(mf) and not is_full_return
                    and mf.EndDate() <= self._end_date):
                additional_rows.append((mf, 'M'))
        for mf, flag in additional_rows:
            additional_row = self._calculate_additional_row(mf, flag)
            if flag in ('M', 'SR'):
                row_id = self.get_row_id(mf, flag, mf.EndDate())
            else:
                row_id = self.get_row_id(mf, flag)
            values[row_id] = additional_row
            if flag == 'MIN FEE':
                row_grouper[mf.Trade().Contract().Oid()].append(row_id)
                for label, spec in self._columns().items():
                    if 'summary' in spec and spec['summary']:
                        pattern = spec['pattern'] if 'pattern' in spec else '{}'
                        values['SUMMARY_RAW'][label] += float(additional_row[label])
                        values['SUMMARY'][label] = pattern.format(values['SUMMARY_RAW'][label])
        for contract_oid, row_ids in row_grouper.items():
            subsummary = self._get_summary_values(values, self.subsummary_cols, 
                                                  row_ids)
            row_id = '%011d_SUBSUMMARY' % contract_oid
            values[row_id] = subsummary
        self.format_raw_values(values)
        return values


class SBLFinderFeeCalculator(SBLCalculator):
    
    subsummary_cols = (
        'Days',
        'Fee Excl Vat',
        'Vat',
        'Fee Incl Vat',
    )
    store_raw_values = True
    
    def __init__(self, trades, val_date, bp):
        super(SBLFinderFeeCalculator, self).__init__(trades, val_date, bp)
        self._start_date = first_day_of_month(self._val_date)
        self._end_date = last_day_of_month(self._val_date)
        self._party = bp.Subject()
    
    @staticmethod
    def get_log_str(calc_object):
        return 'trade %s' % calc_object.Oid()
    
    def get_row_id(self, calc_object, flag='', date=''):
        if not flag:
            flag = self._activity(calc_object)
        if not date:
            date = calc_object.Instrument().StartDate()
        return '%011d_%s_%s_%s' % (calc_object.Contract().Oid(), date,
                                   calc_object.Oid(), flag)
    
    def _is_bfw(self, trade):
        return trade.Instrument().StartDate() < self._start_date
    
    def _activity(self, trade, flag=''):
        if flag:
            return flag
        if self._is_bfw(trade):
            return 'BFW'
        if self.is_loan(trade):
            return 'SL'
        return 'SR'
    
    def _trade_ref(self, trade, flag=''):
        if not flag:
            return trade.Oid()
        return ''
    
    def _effective_date(self, trade, flag=''):
        if flag == 'SR':
            return trade.Instrument().ExpiryDateOnly()
        if self._is_bfw(trade):
            return self._start_date
        return trade.Instrument().StartDate()
    
    @staticmethod
    def _security_name(trade, _flag=''):
        return SBLCalculator.security_name(trade)
    
    @staticmethod
    def _quantity(trade, flag=''):
        if flag == 'SR':
            return 0.0
        return SBLCalculator.loan_quantity(trade)
    
    def _price(self, trade, flag=''):
        if flag == 'SR':
            return 0.0
        return self.loan_price(trade)
    
    def _loan_value(self, trade, flag=''):
        return self._price(trade, flag) * self._quantity(trade, flag)
    
    def _days_diff(self, trade, flag=''):
        if flag:
            return 0
        end_date = acm.Time.DateAddDelta(self._end_date, 0, 0, 1)
        end_date = min(end_date, trade.Instrument().ExpiryDateOnly())
        return acm.Time.DateDifference(end_date, self._effective_date(trade))
    
    def _vat_rate(self):
        if self._party.AdditionalInfo().TAXABLE_STATUS():
            return get_vat_for_date(self._val_date)
        return 1.0
    
    def _rate(self, trade, _flag=''):
        return float(trade.AdditionalInfo().SL_G1FinderRate())
    
    def _fee_excl_vat(self, trade, flag=''):
        if flag:
            return 0.0
        return abs(self._price(trade) * self._quantity(trade) * self._rate(trade) 
                    * self._days_diff(trade) / (365.0 * 100))
    
    def _fee_incl_vat(self, trade, flag=''):
        if flag:
            return 0.0
        return self._fee_excl_vat(trade) * self._vat_rate()
    
    def _vat(self, trade, flag=''):
        if flag:
            return 0.0
        return self._fee_incl_vat(trade) - self._fee_excl_vat(trade) 
    
    def _columns(self):
        return OrderedDict([
            ('Trade', {
                'calc': lambda t: t,
                'conv': lambda t: t,
                'skip_report': True,
            }),
            ('ContractOid', {
                'calc': lambda t: t.Contract().Oid(),
                'conv': int,
                'skip_report': True,
            }),
            ('Trade Ref', {
                'calc': self._trade_ref,
                'conv': int_allow_blank,
                'width': '1.6cm',
            }),
            ('', {
                'calc': self._activity,
                'conv': str,
                'width': '1.1cm',
            }),
            ('Effective Date', {
                'calc': self._effective_date,
                'conv': date_to_dt,
                'width': '1.9cm',
                'pattern': '{:%s}' % DATE_PATTERN_VALUES,
            }),
            ('Security', {
                'calc': self._security_name,
                'conv': str,
                'width': '1.4cm',
            }),
            ('Quantity', {
                'calc': self._quantity,
                'conv': float,
                'width': '1.7cm',
                'pattern': '{:,.0f}',
            }),
            ('Price', {
                'calc': self._price,
                'conv': float,
                'width': '1.4cm',
                'pattern': '{:,.2f}',
            }),
            ('Rate', {
                'calc': self._rate,
                'conv': float,
                'width': '1.4cm',
                'pattern': '{:,.3f}',
            }),
            ('Value', {
                'calc': self._loan_value,
                'conv': float,
                'width': '2.3cm',
                'pattern': '{:,.2f}',
            }),
            ('Days', {
                'calc': self._days_diff,
                'conv': int,
                'width': '1.1cm',
            }),
            ('Fee Excl Vat', {
                'calc': self._fee_excl_vat,
                'conv': float,
                'width': '1.7cm',
                'pattern': '{:,.2f}',
                'summary': True,
            }),
            ('Vat', {
                'calc': self._vat,
                'conv': float,
                'width': '1.7cm',
                'pattern': '{:,.2f}',
                'summary': True,
            }),
            ('Fee Incl Vat', {
                'calc': self._fee_incl_vat,
                'conv': float,
                'width': '1.7cm',
                'pattern': '{:,.2f}',
                'summary': True,
            }),
        ])
        
    @staticmethod
    def _is_full_return(trade):
        contract = trade.Contract().Oid()
        trades = [t for t in acm.FTrade.Select('contract=%s' % contract)
                  if (t.Status() in VALID_SBL_STATUS 
                      and t.Text1() != 'FULL_RETURN')]
        if not trades:
            return False
        max_expiry = max([t.Instrument().ExpiryDateOnly() for t in trades])
        return trade.Instrument().ExpiryDateOnly() == max_expiry
    
    def _calculate_additional_row(self, trade, flag):
        values = defaultdict(str)
        for label, spec in self._columns().items():
            if 'skip_report' in spec and spec['skip_report']:
                continue
            calc_func = spec['calc']
            conversion = spec['conv']
            pattern = spec['pattern'] if 'pattern' in spec else '{}'
            calc_value = calc_func(trade, flag)
            value = conversion(calc_value)
            if self.store_raw_values:
                values[label] = value
            else:
                values[label] = pattern.format(value)
        return values
    
    def calculate(self):
        values = super(SBLFinderFeeCalculator, self).calculate()
        row_grouper = defaultdict(list)
        additional_rows = []
        for row_id in list(values.keys()):
            if row_id in ('SUMMARY', 'SUMMARY_RAW'):
                continue
            row_grouper[int(values[row_id]['ContractOid'])].append(row_id)
            trade = values[row_id]['Trade']
            if (self._is_full_return(trade) 
                    and trade.Instrument().ExpiryDateOnly() <= self._end_date):
                additional_rows.append((trade, 'SR'))
        for trade, flag in additional_rows:
            additional_row = self._calculate_additional_row(trade, flag)
            row_id = self.get_row_id(trade, flag, trade.Instrument().ExpiryDateOnly())
            values[row_id] = additional_row
        for contract_oid, row_ids in row_grouper.items():
            subsummary = self._get_summary_values(values, self.subsummary_cols, 
                                                  row_ids)
            row_id = '%011d_SUBSUMMARY' % contract_oid
            values[row_id] = subsummary
        self.format_raw_values(values)
        return values


class SBLLoanMovementCalculator(SBLCalculator):
    
    def __init__(self, trades, val_date, bp):
        super(SBLLoanMovementCalculator, self).__init__(trades, val_date, bp)
        self._party = bp.Subject()
    
    @staticmethod
    def get_row_id(calc_object):
        return '%011d' % calc_object.Oid()
    
    @staticmethod
    def loan_return(trade):
        return 'Loan' if SBLCalculator.is_loan(trade) else 'Return'
    
    @staticmethod
    def quantity(trade):
        return SBLCalculator.loan_quantity(trade)
    
    @staticmethod
    def link_ref(trade):
        return trade.Contract().Oid()
    
    def _borrower_lender(self, _trade):
        return self._party.AdditionalInfo().SL_CptyType()
    
    def _cpty_code(self, _trade):
        return self._party.AdditionalInfo().SL_G1PartyCode()
    
    def _cpty_major(self, _trade):
        return self._party.AdditionalInfo().SL_MajorPtyCode()
    
    def _columns(self):
        return OrderedDict([
            ('B/L', {
                'calc': self._borrower_lender,
                'conv': str,
                'width': '1.5cm',
            }),
            ('Cpty Major', {
                'calc': self._cpty_major,
                'conv': str,
                'width': '2.1cm',
            }),
            ('Cpty Code', {
                'calc': self._cpty_code,
                'conv': str,
                'width': '2.0cm',
            }),
            ('Link Ref', {
                'calc': self.link_ref,
                'conv': int_allow_blank,
                'width': '1.9cm',
            }),
            ('Trade Ref', {
                'calc': lambda t: t.Oid(),
                'conv': int,
                'width': '1.9cm',
            }),
            ('L/R', {
                'calc': self.loan_return,
                'conv': str,
                'width': '1.9cm',
            }),
            ('Security', {
                'calc': self.security_name,
                'conv': str,
                'width': '1.9cm',
            }),
            ('Quantity', {
                'calc': self.quantity,
                'conv': float,
                'width': '2.0cm',
                'pattern': '{:,.0f}',
            }),
            ('Trade Date', {
                'calc': lambda t: t.TradeTime()[:10],
                'conv': date_to_dt,
                'width': '1.9cm',
                'pattern': '{:%s}' % DATE_PATTERN_VALUES,
            }),
            ('Value Date', {
                'calc': lambda t: t.ValueDay(),
                'conv': date_to_dt,
                'width': '1.9cm',
                'pattern': '{:%s}' % DATE_PATTERN_VALUES,
            }),
        ])


class SBLCollateralMovementCalculator(SBLLoanMovementCalculator):
    
    @staticmethod
    def loan_return(trade):
        return ('Return' if trade.Text1() in ('PARTIAL_RETURN', 'FULL_RETURN')
                else 'Loan')
    
    @staticmethod
    def link_ref(trade):
        if SBLCollateralMovementCalculator.loan_return(trade) == 'Loan':
            return trade.Oid()
        return trade.TrxTrade().Oid() if trade.TrxTrade() else ''
    
    @staticmethod
    def quantity(trade):
        return abs(trade.FaceValue())


class SBLCashMovementCalculator(SBLLoanMovementCalculator):
    
    mf_types = (
        'Fixed Amount',
    )
    
    def __init__(self, trades, val_date, bp):
        super(SBLCashMovementCalculator, self).__init__(trades, val_date, bp)
        self._start_date = bp.AdditionalInfo().BP_FromDate()
        self._end_date = bp.AdditionalInfo().BP_ToDate()
    
    @staticmethod
    def get_log_str(calc_object):
        return 'trade %s' % calc_object.Trade().Oid()
    
    @staticmethod
    def get_row_id(calc_object):
        return '%s_%011d' % (calc_object.PayDay(), calc_object.CashFlow().Oid())
    
    def _calc_objects(self):
        return [mf for trade in self._trades 
                    for mf in trade.MoneyFlows(self._start_date, self._end_date)]
    
    def _skip_calculation(self, calc_object):
        return calc_object.Type() not in self.mf_types
    
    def _columns(self):
        return OrderedDict([
            ('B/L', {
                'calc': self._borrower_lender,
                'conv': str,
                'width': '1.5cm',
            }),
            ('Cpty Major', {
                'calc': self._cpty_major,
                'conv': str,
                'width': '2.5cm',
            }),
            ('Cpty Code', {
                'calc': self._cpty_code,
                'conv': str,
                'width': '2.5cm',
            }),
            ('Cash Flow Ref', {
                'calc': lambda mf: mf.CashFlow().Oid(),
                'conv': int,
                'width': '2.5cm',
            }),
            ('Trade Ref', {
                'calc': lambda mf: mf.Trade().Oid(),
                'conv': int,
                'width': '2.5cm',
            }),
            ('Currency', {
                'calc': lambda mf: mf.Currency().Name(),
                'conv': str,
                'width': '1.5cm',
            }),
            ('Amount', {
                'calc': lambda mf: CALC_SPACE_MF.CalculateValue(mf, 'Cash Analysis Projected'),
                'conv': float,
                'width': '3.5cm',
                'pattern': '{:,.2f}',
            }),
            ('Pay Day', {
                'calc': lambda mf: mf.PayDay(),
                'conv': date_to_dt,
                'width': '2.5cm',
                'pattern': '{:%s}' % DATE_PATTERN_VALUES,
            }),
        ])


class SBLOpenPosCalculator(SBLCalculator):
    
    subsummary_cols = (
        'Loan Quantity',
        'Loan Value',
        'Market Value',
    )
    
    @staticmethod
    def link_ref(trade):
        if trade.Instrument().InsType() == 'SecurityLoan':
            return trade.Contract().Oid()
        if trade.Text1() not in ('PARTIAL_RETURN', 'FULL_RETURN'):
            return trade.Oid()
        return trade.TrxTrade().Oid() if trade.TrxTrade() else ''
    
    @staticmethod
    def get_row_id(calc_object, security_name='', suffix=''):
        if calc_object:
            suffix = '%011d' % calc_object.Oid()
            security_name = SBLCalculator.security_name(calc_object)
        return '%s_%s' % (security_name, suffix)
    
    @staticmethod
    def _loan_quantity(trade):
        instype = trade.Instrument().InsType()
        if instype == 'Deposit':
            return 0
        if instype == 'SecurityLoan':
            return round(SBLCalculator.loan_quantity(trade))
        return abs(trade.FaceValue())
    
    @staticmethod
    def _loan_price(trade):
        instype = trade.Instrument().InsType()
        if instype == 'Deposit':
            return 0
        if instype == 'SecurityLoan':
            return SBLCalculator.loan_price(trade)
        return (trade.Price()
                * trade.Instrument().Quotation().QuotationFactor())
    
    def _loan_value(self, trade):
        if trade.Instrument().InsType() == 'SecurityLoan':
            return self.loan_value(trade)
        return self.market_value(trade)
    
    def _market_price(self, trade):
        instype = trade.Instrument().InsType()
        if instype == 'Deposit':
            return 0
        if instype == 'SecurityLoan':
            return SBLCalculator.security_price(trade.Instrument(), 
                                                self._val_date)
        return self.market_value(trade) / abs(trade.FaceValue())
    
    def _columns(self):
        return OrderedDict([
            ('Link Ref', {
                'calc': self.link_ref,
                'conv': int_allow_blank,
                'width': '1.5cm',
            }),
            ('Trade Ref', {
                'calc': lambda t: t.Oid(),
                'conv': int,
                'width': '1.8cm',
            }),
            ('Code', {
                'calc': self.security_name,
                'conv': str,
                'width': '1.8cm',
            }),
            ('Loan Quantity', {
                'calc': self._loan_quantity,
                'conv': float,
                'width': '2.7cm',
                'pattern': '{:,.0f}',
            }),
            ('Loan Date', {
                'calc': lambda t: t.ValueDay(),
                'conv': date_to_dt,
                'width': '2.0cm',
                'pattern': '{:%s}' % DATE_PATTERN_VALUES,
            }),
            ('Loan Price', {
                'calc': self._loan_price,
                'conv': float,
                'width': '1.9cm',
                'pattern': '{:,.2f}',
            }),
            ('Loan Value', {
                'calc': self._loan_value,
                'conv': float,
                'width': '2.7cm',
                'pattern': '{:,.1f}',
                'summary': True,
            }),
            ('Market Price', {
                'calc': self._market_price,
                'conv': float,
                'width': '1.9cm',
                'pattern': '{:,.2f}',
            }),
            ('Market Value', {
                'calc': self.market_value,
                'conv': float,
                'width': '2.7cm',
                'pattern': '{:,.1f}',
                'summary': True,
            }),
        ])
    
    def calculate(self):
        values = super(SBLOpenPosCalculator, self).calculate()
        row_grouper = defaultdict(list)
        for row_id in list(values.keys()):
            if row_id == 'SUMMARY':
                continue
            row_grouper[values[row_id]['Code']].append(row_id)
        for security_code, row_ids in row_grouper.items():
            subsummary = self._get_summary_values(values, self.subsummary_cols, 
                                                  row_ids)
            subsummary['Code'] = '%s Total' % security_code
            row_id = self.get_row_id(None, security_code, 'SUBSUMMARY')
            values[row_id] = subsummary
        return values


class SBLSummaryOpenPosCalculator(SBLCalculator):
    
    subsummary_cols = (
        'Loan Quantity',
        'Loan Value',
        'Market Value',
    )
    
    @staticmethod
    def get_row_id(calc_object, security_name='', suffix=''):
        if calc_object:
            suffix = '%011d' % calc_object.Oid()
            security_name = SBLCalculator.security_name(calc_object)
        return '%s_%s' % (security_name, suffix)
    
    @staticmethod
    def coll_or_scrip(trade):
        if trade.Instrument().InsType() == 'SecurityLoan':
            return 'Scrip'
        return 'Collateral'
    
    @staticmethod
    def _loan_quantity(trade):
        if trade.Instrument().InsType() == 'SecurityLoan':
            return round(SBLCalculator.loan_quantity(trade))
        return abs(trade.FaceValue())
    
    def _loan_value(self, trade):
        if trade.Instrument().InsType() == 'SecurityLoan':
            return self.loan_value(trade)
        return self.market_value(trade)
    
    def _columns(self):
        return OrderedDict([
            ('Collateral or Scrip', {
                'calc': self.coll_or_scrip,
                'conv': str,
                'width': '1.8cm',
            }),
            ('Security Code', {
                'calc': self.security_name,
                'conv': str,
                'width': '4.3cm',
            }),
            ('Loan Quantity', {
                'calc': self._loan_quantity,
                'conv': int_allow_blank,
                'width': '4.3cm',
            }),
            ('Loan Value', {
                'calc': self._loan_value,
                'conv': float,
                'width': '4.3cm',
                'pattern': '{:,.2f}',
                'summary': True,
            }),
            ('Market Value', {
                'calc': self.market_value,
                'conv': float,
                'width': '4.3cm',
                'pattern': '{:,.2f}',
                'summary': True,
            }),
        ])
    
    def calculate(self):
        values = super(SBLSummaryOpenPosCalculator, self).calculate()
        row_grouper = defaultdict(list)
        for row_id in list(values.keys()):
            if row_id == 'SUMMARY':
                continue
            row_grouper[values[row_id]['Security Code']].append(row_id)
        security_codes = sorted(row_grouper.keys())
        for security_code, row_ids in row_grouper.items():
            subsummary = self._get_summary_values(values, self.subsummary_cols, 
                                                  row_ids)
            subsummary['Security Code'] = security_code
            if security_code == security_codes[0]:
                subsummary['Collateral or Scrip'] = values[row_ids[0]]['Collateral or Scrip']
            if security_code == 'Cash':
                subsummary['Loan Quantity'] = ''
            row_id = self.get_row_id(None, security_code, 'SUBSUMMARY')
            values[row_id] = subsummary
        return values


class SBLCollateralValueCalculator(SBLCalculator):
    
    @staticmethod
    def get_log_str(calc_object):
        return 'row %s' % str(calc_object)
    
    @staticmethod
    def get_row_id(calc_object):
        return str(calc_object)
    
    @staticmethod
    def _cash_collateral(row):
        if not row.Item().Trades():
            return 0.0
        return CALC_SPACE_PRF.CalculateValue(row, 'Cash Collateral')
    
    @staticmethod
    def _equities_collateral(row):
        if not row.Item().Trades():
            return 0.0
        return CALC_SPACE_PRF.CalculateValue(row, 'Equities Collateral')
    
    @staticmethod
    def _bonds_collateral(row):
        if not row.Item().Trades():
            return 0.0
        return CALC_SPACE_PRF.CalculateValue(row, 'Bonds Collateral')
    
    def _calc_objects(self):
        adhoc_portfolio = acm.FAdhocPortfolio()
        for trade in self._trades:
            adhoc_portfolio.Add(trade)
        tree = CALC_SPACE_PRF.InsertItem(adhoc_portfolio)
        CALC_SPACE_PRF.Refresh()
        return [tree]
    
    def _columns(self):
        return OrderedDict([
            ('Cash', {
                'calc': self._cash_collateral,
                'conv': float,
                'width': '3.8cm',
                'pattern': '{:,.2f}',
            }),
            ('Equities', {
                'calc': self._equities_collateral,
                'conv': float,
                'width': '3.8cm',
                'pattern': '{:,.2f}',
            }),
            ('Bonds', {
                'calc': self._bonds_collateral,
                'conv': float,
                'width': '3.8cm',
                'pattern': '{:,.2f}',
            }),
        ])


class SBLLoanValueCalculator(SBLCalculator):
    
    def _market_value_equity(self, trade):
        if trade.Instrument().Security().InsType() in ('Stock', 'ETF'):
            return self.market_value(trade)
        return 0.0
    
    def _market_value_other(self, trade):
        if trade.Instrument().Security().InsType() not in ('Stock', 'ETF'):
            return self.market_value(trade)
        return 0.0
    
    def _columns(self):
        return OrderedDict([
            ('Equity', {
                'calc': self._market_value_equity,
                'conv': float,
                'width': '3.8cm',
                'pattern': '{:,.2f}',
                'summary': True,
            }),
            ('Bonds', {
                'calc': self._market_value_other,
                'conv': float,
                'width': '3.8cm',
                'pattern': '{:,.2f}',
                'summary': True,
            }),
        ])
    
    def _populate_zero_summary(self, values):
        for label, spec in self._columns().items():
            if 'summary' in spec and spec['summary']:
                pattern = spec['pattern'] if 'pattern' in spec else '{}'
                values['SUMMARY'][label] = pattern.format(0.0)
    
    def calculate(self):
        values = super(SBLLoanValueCalculator, self).calculate()
        if not values:
            self._populate_zero_summary(values)
        return values


class SBLMarginCallCalculator(SBLCalculator):
    
    def __init__(self, trades, val_date, bp):
        super(SBLMarginCallCalculator, self).__init__(trades, val_date, bp)
        self._loan_value = None
        self._collateral_value = None
    
    @staticmethod
    def get_log_str(calc_object):
        return 'row %s' % str(calc_object)
    
    @staticmethod
    def get_row_id(calc_object):
        return str(calc_object)
    
    def _calc_objects(self):
        return [self._trades]
    
    def _get_loan_value(self, trades):
        if self._loan_value != None:
            return self._loan_value
        value = 0.0
        for trade in trades:
            if trade.Instrument().InsType() == 'SecurityLoan':
                value += self.market_value(trade)
        self._loan_value = value
        return self._loan_value
    
    def _get_collateral_value(self, trades):
        if self._collateral_value != None:
            return self._collateral_value
        value = 0.0
        for trade in trades:
            if trade.Instrument().InsType() != 'SecurityLoan':
                value += float(CALC_SPACE_TRD.CalculateValue(trade, 'CollateralMarketValue'))
        self._collateral_value = value
        return self._collateral_value
    
    def _get_margin_call(self, trades, haircut=1.0):
        loan_value = self._get_loan_value(trades)
        collateral_value = self._get_collateral_value(trades)
        return (collateral_value - loan_value) * haircut
    
    def _columns(self):
        return OrderedDict([
            ('MarginValue', {
                'calc':  self._get_margin_call,
                'conv': float,
                'skip_report': True,
            }),
            ('Margin Call 105% (Cash)', {
                'calc': lambda row: self._get_margin_call(row, haircut=1.05),
                'conv': float,
                'width': '4.0cm',
                'pattern': '{:,.2f}',
            }),
            ('Margin Call 110% (Bond)', {
                'calc': lambda row: self._get_margin_call(row, haircut=1.10),
                'conv': float,
                'width': '4.0cm',
                'pattern': '{:,.2f}',
            }),
            ('Margin Call 115% (Equity)', {
                'calc': lambda row: self._get_margin_call(row, haircut=1.15),
                'conv': float,
                'width': '4.0cm',
                'pattern': '{:,.2f}',
            }),
        ])


class SBLDividendCalculator(SBLCalculator):
    
    div_coll_name = ''
    
    def __init__(self, trades, val_date, bp):
        super(SBLDividendCalculator, self).__init__(trades, val_date, bp)
        from SBL_Dividend_Summary_Report import CorporateActionsExtract
        self.corpact_extract = CorporateActionsExtract

    def dividend_vars(self, trade):

        dividend =  acm.FDividend.Select("instrument='%s' and recordDay='%s'" 
                                        % (trade.Instrument().Security().Name(), self._val_date))
        if dividend:
            return {'amount':dividend[0].Amount(), 'ex_div_day':dividend[0].ExDivDay(), 'pay_date':dividend[0].PayDay(), 'record_date':dividend[0].RecordDay()}
        corpact = acm.FCorporateAction.Select("recordDate = '%s' and instrument='%s'"
                                                % (self._val_date, trade.Instrument().Security().Name()))[0]
        dividend_data = self.corpact_extract._dividend_details(corpact, self._val_date)

        if dividend and payment_date:
            return dividend_data.update({'ex_div_day':corpact.ExDate()})
        return []

    @staticmethod
    def get_log_str(trade):
        return 'trade %s' % str(trade)

    def _trade_type(self, trade):
        if self.corpact_extract._is_sec_loan(trade):
            return "Security Loan"
        return "Collateral"
    
    def dividend_calc(self, trade):
        if self.dividend_vars(trade):
            return CALC_SPACE_TRD.CalculateValue(trade, 'Quantity') * self.dividend_vars(trade)['amount']
        return 0.0
    
    def _columns(self):
        return OrderedDict([
            ('Security Code', {
                'calc': lambda trade: SBLCalculator.security_name(trade),
                'conv': str,
                'width': '1.3cm',
            }),
            ('ISIN Code', {
                'calc': lambda trade: trade.Instrument().Security().Isin(),
                'conv': str,
                'width': '2.4cm',
            }),
            ('Ex Date', {
                'calc': lambda trade: self.dividend_vars(trade)['ex_div_day'] if self.dividend_vars(trade) else '',
                'conv': str,
                'width': '2.0cm',
            }),
            ('Record Date', {
                'calc': lambda trade: self.dividend_vars(trade)['record_date'] if self.dividend_vars(trade) else '',
                'conv': str,
                'width': '2.4cm',
            }),
            ('Payment Date', {
                'calc': lambda trade: self.dividend_vars(trade)['pay_date'] if self.dividend_vars(trade) else '',
                'conv': str,
                'width': '2.4cm',
            }),
            ('Dividend (cps)', {
                'calc': lambda trade: self.dividend_vars(trade)['amount'] if self.dividend_vars(trade) else 0.0,
                'conv': float,
                'width': '1.4cm',
                'pattern': '{:,.2f}',
            }),
            ('Trade Type', {
                'calc': self._trade_type,
                'conv': str,
                'width': '2.4cm',
            }),
            ('Quantity', {
                'calc': lambda trade: CALC_SPACE_TRD.CalculateValue(trade, 'Quantity'),
                'conv': float,
                'width': '2.4cm',
                'pattern': '{:,.2f}',
                'summary': True,
            }),
            (self.div_coll_name, {
                'calc': self.dividend_calc,
                'conv': float,
                'width': '2.4cm',
                'pattern': '{:,.2f}',
                'summary': True,
            }),
        ])
    
    def _increment_dictionary_values(self, innerdict, div, quantity):
        if innerdict[self.div_coll_name]:
            div += float(innerdict[self.div_coll_name].replace(',', ''))

        if innerdict["Quantity"]:
            quantity += float(innerdict["Quantity"].replace(',', ''))
        return div, quantity
    
    def calculate(self):
        calculated_values = super(SBLDividendCalculator, self).calculate()
        calculated_values_ = OrderedDict(sorted(list(calculated_values.items()), key=lambda t: t[1]))
        sec_code_set = set()
        div = 0.0
        quantity = 0.0

        securities = [innerdict["Security Code"] for innerdict in list(calculated_values_.values())]
        duplicates = list([i for i in securities if securities.count(i) > 1])

        for index, innerdict in calculated_values_.items():
            popped = None
            security_code = innerdict["Security Code"]

            if security_code and security_code in duplicates:
                dup_index = duplicates.index(security_code)

            if security_code not in sec_code_set:
                div = 0.0
                quantity = 0.0
                sec_code_set.add(security_code)

            if duplicates.count(security_code) > 1:
                div, quantity = self._increment_dictionary_values(innerdict, div, quantity)

                popped = calculated_values.pop(index)
                duplicates.pop(dup_index)

            elif duplicates.count(security_code) == 1:

                duplicates.pop(dup_index)
                div, quantity = self._increment_dictionary_values(innerdict, div, quantity)

                innerdict[self.div_coll_name] = "{:,.2f}".format(div)
                innerdict["Quantity"] = "{:,.2f}".format(quantity)

            if not popped:
                calculated_values[index] = innerdict
        return calculated_values


class SBLPayableDividendCalculator(SBLDividendCalculator):
    
    div_coll_name = 'Dividend Payable ZAR'


class SBLReceivableDividendCalculator(SBLDividendCalculator):
    
    div_coll_name = 'Dividend Receivable ZAR'


class CalcEngine(object):
    
    def __init__(self, trades, val_date, bp):
        self._trades = trades
        self._val_date = val_date
        self._bp = bp
        self._log_str = '%s, %s' % (bp.Subject().Name(), bp.Oid())
    
    def _simulate_globals(self):
        CALC_SPACE_TRD.Clear()
        CALC_SPACE_PRF.Clear()
        CALC_SPACE_MF.Clear()
        CALC_SPACE_MF.SimulateGlobalValue('Valuation Date', self._val_date) 
        CALC_SPACE_MF.SimulateGlobalValue('Portfolio Profit Loss End Date', 
                                          'Custom Date')
        CALC_SPACE_MF.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', 
                                          self._val_date)
        CALC_SPACE_TRD.SimulateGlobalValue('Valuation Date', self._val_date) 
        CALC_SPACE_TRD.SimulateGlobalValue('Portfolio Profit Loss End Date', 
                                           'Custom Date')
        CALC_SPACE_TRD.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', 
                                           self._val_date)
        CALC_SPACE_PRF.SimulateGlobalValue('Valuation Date', self._val_date) 
        CALC_SPACE_PRF.SimulateGlobalValue('Portfolio Profit Loss End Date', 
                                           'Custom Date')
        CALC_SPACE_PRF.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', 
                                           self._val_date)
    
    def _get_calc_groups(self):
        yield ('', Calculator, self._trades, True)
    
    def calculate(self):
        self._simulate_globals()
        results = OrderedDict()
        for group_name, calculator, trade_group, add_vals in self._get_calc_groups():
            calc = calculator(trade_group, self._val_date, self._bp)
            group_values = {}
            group_values['columns'] = calc.get_column_specs()
            group_values['values'] = calc.calculate()
            group_values['add_values'] = {}
            if add_vals:
                group_values['add_values'] = calc.additional_values()
            results[group_name] = group_values
        return results


class FECCalcEngine(CalcEngine):
    
    def _get_calc_groups(self):
        yield ('', FECCalculator, self._trades, True)


class DepositCalcEngine(CalcEngine):
    
    def _get_calc_groups(self):
        yield ('', DepositCalculator, self._trades, False)


class SBLFeeCalcEngine(CalcEngine):
    
    calc_class = SBLFeeCalculator
    label_mapping = {
        'Fee Incl Vat': 'Total Fee',
    }
    
    @staticmethod
    def trade_grouper(trade):
        isin = trade.Instrument().Security().Isin()
        security_name = SBLCalculator.security_name(trade)
        if not isin:
            return security_name
        return '%s - %s' % (security_name, isin)
    
    @classmethod
    def _get_calc_groups(cls, trades):
        trade_groups = defaultdict(list)
        for trade in trades:
            group_name = cls.trade_grouper(trade)
            trade_groups[group_name].append(trade)
        for group_name in sorted(trade_groups.keys()):
            yield (group_name, cls.calc_class, trade_groups[group_name])
    
    @classmethod
    def _map_labels(cls, values):
        for old_key, new_key in cls.label_mapping.items():
            if old_key in values:
                values[new_key] = values.pop(old_key)
    
    def _columns_totals(self):
        return OrderedDict([
            ('', {
                'conv': str,
                'width': '2.0cm',
            }),
            ('Fee Excl Vat', {
                'conv': float,
                'width': '2.0cm',
                'pattern': '{:,.2f}',
                'total': True,
            }),
            ('Vat', {
                'conv': float,
                'width': '2.0cm',
                'pattern': '{:,.2f}',
                'total': True,
            }),
            ('Fee Incl Vat', {
                'conv': float,
                'width': '2.0cm',
                'pattern': '{:,.2f}',
                'total': True,
            }),
        ])
    
    def _get_column_specs(self):
        specs = OrderedDict()
        for label, spec in self._columns_totals().items():
            if 'skip_report' in spec and spec['skip_report']:
                continue
            specs[label] = {
                'width': spec['width'],
                'datatype': Calculator.translate_conv[spec['conv']],
            }
        self._map_labels(specs)
        return specs
    
    def _get_invoice_nbr(self):
        generated_steps = get_steps(self._bp, 'Generated')
        return '%s-%s' % (self._bp.Oid(), len(generated_steps) + 1)
    
    def _calculate_totals(self, results):
        totals = defaultdict(str)
        totals_numeric = defaultdict(int)
        columns_totals = self._columns_totals()
        for group_name, group in results.items():
            group_values = group['values']
            if not 'SUMMARY_RAW' in group_values:
                LOGGER.warning('%s: SUMMARY not found for %s.' % (self._log_str, group_name))
                continue
            values = group_values['SUMMARY_RAW']
            for label in values:
                if (label in columns_totals and 'total' in columns_totals[label]
                        and columns_totals[label]['total']):
                    spec = columns_totals[label]
                    pattern = spec['pattern'] if 'pattern' in spec else '{}'
                    totals_numeric[label] += values[label]
                    totals[label] = pattern.format(totals_numeric[label])
        self._map_labels(totals)
        return totals
    
    def _calculate_groups(self, trades):
        self._simulate_globals()
        results = OrderedDict()
        for group_name, calculator, trade_group in self._get_calc_groups(trades):
            calc = calculator(trade_group, self._val_date, self._bp)
            group_values = {}
            group_values['columns'] = calc.get_column_specs()
            group_values['values'] = calc.calculate()
            group_values['add_values'] = {}
            results[group_name] = group_values
        return results
    
    def _calculate(self, trades):
        results = self._calculate_groups(trades)
        row_totals = {}
        row_totals['SUMMARY'] = self._calculate_totals(results)
        total_values = {}
        total_values['columns'] = self._get_column_specs()
        total_values['values'] = row_totals
        results['STATEMENT_TOTALS'] = total_values
        results['INVOICE_NBR'] = self._get_invoice_nbr()
        return results
    
    def calculate(self):
        # Support for multiple counterparties per statement
        results = OrderedDict()
        results[self._bp.Subject().Name()] = self._calculate(self._trades)
        return results


class SBLFinderFeeCalcEngine(SBLFeeCalcEngine):
    
    calc_class = SBLFinderFeeCalculator


class SBLMovementCalcEngine(CalcEngine):
    
    def _get_calc_groups(self):
        trade_groups = defaultdict(list)
        for trade in self._trades:
            if trade.Instrument().InsType() == 'SecurityLoan':
                trade_groups['Loans'].append(trade)
            elif trade.Instrument().InsType() == 'Deposit':
                trade_groups['Cash'].append(trade)
            else:
                trade_groups['Collateral'].append(trade)
        yield ('Scrip', SBLLoanMovementCalculator, trade_groups['Loans'], False)
        yield ('Collateral', SBLCollateralMovementCalculator, trade_groups['Collateral'], False)
        yield ('Cash', SBLCashMovementCalculator, trade_groups['Cash'], False)
    
    def calculate(self):
        results = super(SBLMovementCalcEngine, self).calculate()
        results['PARAMS'] = {}
        results['PARAMS']['start_date'] = self._bp.AdditionalInfo().BP_FromDate()
        results['PARAMS']['end_date'] = self._bp.AdditionalInfo().BP_ToDate()
        return results


class SBLOpenPosCalcEngine(CalcEngine):
    
    def _get_calc_groups(self):
        trade_groups = defaultdict(list)
        for trade in self._trades:
            if trade.Instrument().InsType() == 'SecurityLoan':
                trade_groups['Loans'].append(trade)
            else:
                trade_groups['Collateral'].append(trade)
        yield ('Loans', SBLOpenPosCalculator, trade_groups['Loans'], False)
        yield ('Collateral', SBLOpenPosCalculator, trade_groups['Collateral'], False)


class SBLSummaryOpenPosCalcEngine(CalcEngine):
    
    @staticmethod
    def trade_grouper(trade):
        return SBLSummaryOpenPosCalculator.coll_or_scrip(trade)
    
    def _get_calc_groups(self):
        trade_groups = defaultdict(list)
        for trade in self._trades:
            group_name = self.trade_grouper(trade)
            trade_groups[group_name].append(trade)
        for group_name in sorted(list(trade_groups.keys()), reverse=True):
            yield (group_name, SBLSummaryOpenPosCalculator, 
                   trade_groups[group_name], False)


class SBLMarginCallCalcEngine(CalcEngine):
    
    def _get_calc_groups(self):
        trade_groups = defaultdict(list)
        for trade in self._trades:
            if trade.Instrument().InsType() == 'SecurityLoan':
                trade_groups['Loans'].append(trade)
            else:
                trade_groups['Collateral'].append(trade)
        yield ('Collateral', SBLCollateralValueCalculator, trade_groups['Collateral'], False)
        yield ('Loans', SBLLoanValueCalculator, trade_groups['Loans'], False)
        yield ('Margin Call', SBLMarginCallCalculator, self._trades, False)


class ValuationsDefaultCalcEngine(CalcEngine):
    
    trade_types = OrderedDict([
        ('Default', {
            'group_name': '',
            'calculator': ValuationsDefaultCalculator,
            'calculatorZAR': ValuationsDefaultCalculatorZAR,
        }),
    ])
    default_group_name = ''
    include_additional_values = False
    
    @staticmethod
    def zar_only_trades(trades):
        return all([t.Currency().Name() == 'ZAR' for t in trades])
    
    @staticmethod
    def trade_grouper(trade):
        return ''
    
    def _group_trades(self):
        trade_groups = defaultdict(list)
        for trade in self._trades:
            grouper = self.trade_grouper(trade)
            if grouper in self.trade_types:
                group_name = self.trade_types[grouper]['group_name']
                trade_groups[group_name].append(trade)
            else:
                trade_groups[self.default_group_name].append(trade)
        return trade_groups
    
    def _get_calc_groups(self):
        trade_groups = self._group_trades()
        for params in list(self.trade_types.values()):
            group_name = params['group_name']
            if not group_name in trade_groups:
                continue
            trades = trade_groups.pop(group_name)
            if not trades:
                continue
            if 'calculatorZAR' in params and self.zar_only_trades(trades):
                calculator = params['calculatorZAR']
            else:
                calculator = params['calculator']
            include_add_vals = self.include_additional_values and not len(trade_groups)
            yield (group_name, calculator, trades, include_add_vals)
    
    
class OptionCalcEngine(ValuationsDefaultCalcEngine):
    
    trade_types = OrderedDict([
        ('Commodity', {
            'group_name': 'Commodity',
            'calculator': CommodityOptionCalculator,
            'calculatorZAR': CommodityOptionCalculatorZAR,
        }),
        ('EquityIndex', {
            'group_name': 'Equity Index',
            'calculator': EquityOptionCalculator,
            'calculatorZAR': EquityOptionCalculatorZAR,
        }),
        ('Stock', {
            'group_name': 'Equity',
            'calculator': EquityOptionCalculator,
            'calculatorZAR': EquityOptionCalculatorZAR,
        }),
        ('Curr', {
            'group_name': 'FX',
            'calculator': FXOptionCalculator,
        }),
        ('Swap', {
            'group_name': 'Swap',
            'calculator': SwapOptionCalculator,
        }),
    ])
    default_group_name = 'Equity'
    include_additional_values = True
    
    @staticmethod
    def trade_grouper(trade):
        return trade.Instrument().UnderlyingType()


class SwapCalcEngine(ValuationsDefaultCalcEngine):
    
    trade_types = OrderedDict([
        ('CurrSwap', {
            'group_name': 'Currency',
            'calculator': CurrSwapCalculator,
        }),
        ('Default', {
            'group_name': '',
            'calculator': ValuationsDefaultCalculator,
            'calculatorZAR': ValuationsDefaultCalculatorZAR,
        }),
    ])
    default_group_name = ''
    
    @staticmethod
    def trade_grouper(trade):
        return trade.Instrument().InsType()


class StructuredCalcEngine(ValuationsDefaultCalcEngine):
    
    trade_types = OrderedDict([
        ('Default', {
            'group_name': '',
            'calculator': StructuredCalculator,
            'calculatorZAR': StructuredCalculatorZAR,
        }),
    ])
    default_group_name = ''


class SBLDividendNotificationCalcEngine(CalcEngine):

    def _get_calc_groups(self):
        trade_groups = defaultdict(list)
        client = self._bp.Subject()

        for trade in self._trades:
            receivable_div = SBLReceivableDividendCalculator([trade], self._val_date, self._bp)
            payable_div = SBLPayableDividendCalculator([trade], self._val_date, self._bp)

            if not (receivable_div.dividend_vars(trade) or payable_div.dividend_vars(trade)):
                continue

            if client.Name().startswith('SLL') and trade.Instrument().InsType() == 'SecurityLoan':
                trade_groups['Payable'].append(trade)
            elif client.Name().startswith('SLB') and trade.Instrument().InsType() == 'SecurityLoan':
                trade_groups['Receivable'].append(trade)
            elif client.Name().startswith('SLL') and not trade.Instrument().InsType() == 'SecurityLoan':
                trade_groups['Receivable'].append(trade)
            elif client.Name().startswith('SLB') and not trade.Instrument().InsType() == 'SecurityLoan':
                trade_groups['Payable'].append(trade)

        if trade_groups['Payable']:
            yield ('Payable', SBLPayableDividendCalculator, trade_groups['Payable'], False)
        if trade_groups['Receivable']:
            yield ('Receivable', SBLReceivableDividendCalculator, trade_groups['Receivable'], False)

