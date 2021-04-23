import traceback
import acm, ael, string, time
from at_time import acm_date, ael_date, to_datetime, to_date
from datetime import datetime
import os.path
import csv
from at_type_helpers import is_acm
from math import isnan
from collections import defaultdict, namedtuple
from Volcker_Metrics import START_DATES, END_DATES, EXCHANGE_TRADED
from copy import copy
import decimal

class RiskException(Exception):
    pass

class Volcker_Report(object):
    '''Base class for all Volcker related metric reports'''

    def __init__(self, ael_dict):
        #main calculation space for all portfolio sheet calculations
        self.CALC_SPACE = acm.Calculations().CreateCalculationSpace(
            acm.GetDefaultContext(), 
            'FPortfolioSheet'
        )
        
        #main calculation space for all deal sheet calculations
        self.deal_sheet_space = acm.Calculations().CreateCalculationSpace(
            acm.GetDefaultContext(), 
            'FDealSheet'
        )

        #calc space collection for all FObjectCalculations methods
        self.CALC_SPACE_COLLECTION = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        
        self.REPORT_ENTRY = None
        self.path = None
        
        if ael_dict['startDate'] == 'Custom Date':
            self.start_date = ael_dict['startDateCustom']
        else:
            self.start_date = str(START_DATES[ael_dict['startDate']])
    
        if ael_dict['endDate'] == 'Custom Date':
            self.endDate = ael_dict['endDateCustom']
        else:
            self.endDate = str(END_DATES[ael_dict['endDate']])
        
        self.calc_size = 0

        self.repday = ael.date_from_string(self.endDate)  #ael.date_today()
        
        self.CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Now')
        
        self.data = None
        
        report_path = os.path.join(ael_dict['path'], datetime.strftime(to_date(END_DATES[ael_dict['endDate']]), '%Y%m%d'))
        if not os.path.exists(report_path):
            try:
                os.makedirs(report_path)
            except OSError as exc:
                if exc.errno != os.errno.EEXIST:
                    raise
            
        self.performance_file_path = os.path.join(
            ael_dict['path'], 
            datetime.strftime(to_date(END_DATES[ael_dict['endDate']]), '%Y%m%d'), 
            '%s.perf'%ael_dict['tradeFilter']
        )
    
    def get_portfolio(self, trade):
        portfolio_list = ['WEL','TKN','RN2','EWH','ERL','NWT','FIX','DAN','AGG','EAB','BOR','EMM','EDI',
        'CCS','BAT','AST','ABT','JOL','AND','HDG','BJS','EBI','DFX','AYX','ADT','BTB','RND','JCB','FIP',
        'BRC','DHJ','ENT','RET','SML','BBL','BBM','BBP','CBB','COM','COR','EBP','DVP','ABC','INS','CAT',
        'CJR','ETA','EUF']
        
        portfolio = trade.Portfolio()
        acquirer = trade.Acquirer().Name()

        routing_portfolios = acm.FPhysicalPortfolio['ROUTING'].AllPhysicalPortfolios()
        routing_portfolios = [p.Name() for p in routing_portfolios]
    
        if portfolio.Name() in portfolio_list:
            return portfolio.Name()

        if portfolio.Name() in routing_portfolios and portfolio.Name().startswith('ROUT_') and portfolio.Name()[-3:] in portfolio_list:
            return portfolio.Name()[-3:]

        else:
            return portfolio.Oid()
        
    def get_currencies(self, trades):
        '''Return all currencies associated with a set of trades. trades can be a collection of a single trade for trade level evaluations.
           Returns a set of FCurrency objects'''

        moneyFlowAndTradesDiscountingUnits = acm.GetFunction('moneyFlowAndTradesDiscountingUnits', 3)
        currenciesFromInstrumentAndTradesDiscountingUnits = acm.GetFunction('currenciesFromInstrumentAndTradesDiscountingUnits', 1)

        discounting_units = moneyFlowAndTradesDiscountingUnits(trades, acm.Time().DateToday(), 381)
        currencies = currenciesFromInstrumentAndTradesDiscountingUnits(discounting_units)

        return currencies
        
    def calculate_value(self, acm_object, column_id, date=acm.Time.DateToday()):
        '''Generic method to call column evaluations values on acm_object. Typically acm_object will be an FAdhocPortfolio or an FTrade'''

        value = self.CALC_SPACE.CalculateValue(acm_object, column_id, None, False)
        if hasattr(value, 'Number'):
            value = value.Number()
    
        return value
    
    def get_position_notional(self, virtual_portfolio, currency = None):
        '''returns the notional in trade of a collection of trades as the sum of the individual notionals'''

        notional = 0.0

        if not currency:
            curr = virtual_portfolio.Trades().At(0).Currency()
            for trade in virtual_portfolio.Trades():
                trade_notional = trade.Calculation().Nominal(self.CALC_SPACE_COLLECTION, self.repday, curr).Number()
                if isnan(notional):
                    notional = 0.00
                notional += trade_notional
        else:
            for trade in virtual_portfolio.Trades():
                trade_notional = trade.Calculation().Nominal(self.CALC_SPACE_COLLECTION, self.repday, currency).Number()
                if isnan(notional):
                    notional = 0.00
                notional += trade_notional
        
        return notional

    def get_trade_notional(self, trade, currency = None):
        '''returns the notional of a trade in the trade currency'''

        if not currency:
            notional = trade.Calculation().Nominal(self.CALC_SPACE_COLLECTION, self.repday, trade.Currency()).Number()
        else:
            notional = trade.Calculation().Nominal(self.CALC_SPACE_COLLECTION, self.repday, currency).Number()

        if isnan(notional):
            notional = 0.00
        
        return notional
    
    def is_internal_trade(self, trade):
        '''returns true if the trade is booked against an internal department'''

        return trade.Counterparty().IsKindOf(acm.FInternalDepartment)

    def get_trade_market_val(self, trade, currency = None):
        '''returns the market value of a trade'''

        ins = trade.Instrument()
        ins_type = ins.InsType()
            
        try:
            if not currency:
                self.CALC_SPACE.SimulateValue(trade, 'Portfolio Currency', trade.Currency())
            else:
                self.CALC_SPACE.SimulateValue(trade, 'Portfolio Currency', currency)

            market_val = self.calculate_value(trade, 'Total Val End', self.repday)
        except Exception, e:
            market_val = 0.0
        finally:
            self.CALC_SPACE.RemoveSimulation(trade, 'Portfolio Currency')
    
        if isnan(market_val):
            market_val = 0.00
            
        if (not market_val) and (not abs(market_val) >= 0):
            market_val = 0.00
            
        return market_val    

    def get_position_market_val(self, virtual_portfolio, currency = None):
        '''returns the market value of a position as the sum of trade nominals (issues with other columns on certain trades)'''

        ins = virtual_portfolio.Trades().At(0).Instrument()
        ins_type = ins.InsType()
        
        try:
            if not currency:
                self.CALC_SPACE.SimulateValue(virtual_portfolio, 'Portfolio Currency', virtual_portfolio.Trades().At(0).Currency())
            else:
                self.CALC_SPACE.SimulateValue(virtual_portfolio, 'Portfolio Currency', currency)
            
            market_val = self.calculate_value(virtual_portfolio, 'Total Val End', self.repday)
        except Exception, e:
            market_val = 0.0
        finally:
            self.CALC_SPACE.RemoveSimulation(virtual_portfolio, 'Portfolio Currency')
    
        if isnan(market_val):
            market_val = 0.00
            
        if (not market_val) and (not abs(market_val) >= 0):
            market_val = 0.00
        
        return market_val
    
    def get_trade_delta(self, trade, currency = None):
        '''evaluate the Portfolio Delta column for a single trade'''

        delta = 0.00
        ins = trade.Instrument()
        ins_type = ins.InsType()
            
        try:
            if not currency:
                self.CALC_SPACE.SimulateValue(trade, 'Portfolio Currency', trade.Currency())
            else:
                self.CALC_SPACE.SimulateValue(trade, 'Portfolio Currency', currency)

            delta = self.calculate_value(trade, 'Portfolio Delta', self.repday)
        except  Exception, e:
            delta = 0.0
        finally:
            self.CALC_SPACE.RemoveSimulation(trade, 'Portfolio Currency')
        
        try:
            if isnan(delta):
                delta = 0.00
        except Exception, e:
            delta = 0.00
    
        if (not delta) and (not abs(delta) >= 0):
            delta = 0.00
    
        return delta    
    
    def get_position_delta(self, virtual_portfolio, currency = None):
        '''evaluate the Portfolio Delta column for a position, passed as an FAdhocPortfolio'''

        try:
            if not currency:
                self.CALC_SPACE.SimulateValue(virtual_portfolio, 'Portfolio Currency', virtual_portfolio.Trades().At(0).Currency())
            else:
                self.CALC_SPACE.SimulateValue(virtual_portfolio, 'Portfolio Currency', currency)

            delta = self.calculate_value(virtual_portfolio, 'Portfolio Delta', self.repday)
        except Exception, e:
            delta = 0.0
        finally:
            self.CALC_SPACE.RemoveSimulation(virtual_portfolio, 'Portfolio Currency')
            
        try:
            if isnan(delta):
                delta = 0.00
        except Exception, e:
            delta = 0.00
    
        if (not delta) and (not abs(delta) >= 0):
            delta = 0.00
    
        return delta
    
    def get_instrument_delta(self, trade_selection, currency = None):
        '''returns the delta theoretical price'''

        root = self.CALC_SPACE.InsertItem(trade_selection)
        self.CALC_SPACE.Refresh()
        root.Expand(True)
        self.CALC_SPACE.Refresh()
        first_row = root.Iterator().FirstChild().Tree().Item()
        self.CALC_SPACE.Refresh()
        
        try:
            if not currency:
                self.CALC_SPACE.SimulateValue(trade_selection, 'Portfolio Currency', trade_selection.Trades().At(0).Currency())
            else:
                self.CALC_SPACE.SimulateValue(trade_selection, 'Portfolio Currency', currency)

            delta = self.CALC_SPACE.CalculateValue(first_row, 'Instrument Delta', None, False)
        except Exception, e:
            delta = 0.0
        finally:
            self.CALC_SPACE.RemoveSimulation(trade_selection, 'Portfolio Currency')
        
        try:
            delta = delta.Number()
            if isnan(delta):
                delta = 0.00
        except:
            delta = 0.00
    
        if (not delta) and (not abs(delta) >= 0):
            delta = 0.00
        self.CALC_SPACE.Clear()
        return delta 
        
    def get_trade_ir01(self, trade, currency = None):
        '''returns the ir01 of a trade'''

        ir01 = 0.00
        try:
            if not currency:
                self.CALC_SPACE.SimulateValue(trade, 'Portfolio Currency', trade.Currency())
            else:
                self.CALC_SPACE.SimulateValue(trade, 'Portfolio Currency', currency)

            ir01 = self.calculate_value(trade, 'Portfolio Delta Yield', self.repday)
        except Exception, e:
            ir01 = 0.0
        finally:
            self.CALC_SPACE.RemoveSimulation(trade, 'Portfolio Currency')
            
        if isnan(ir01):
            ir01 = 0.00
            
        if (not ir01) and (not abs(ir01) >= 0):
            ir01 = 0.00
                
        return ir01

    def get_position_ir01(self, virtual_portfolio, currency = None):
        '''returns the ir01 of a position, passed as an FAdhocPortfolio'''

        ir01 = 0.00
        first_trade = virtual_portfolio.Trades().At(0)
        try:
            if not currency:
                self.CALC_SPACE.SimulateValue(virtual_portfolio, 'Portfolio Currency', first_trade.Currency())
            else:
                self.CALC_SPACE.SimulateValue(virtual_portfolio, 'Portfolio Currency', currency)

            ir01 = self.calculate_value(virtual_portfolio, 'Portfolio Delta Yield', self.repday)
        except Exception, e:
            ir01 = 0.0
        finally:
            self.CALC_SPACE.RemoveSimulation(virtual_portfolio, 'Portfolio Currency')
            
        if is_acm(ir01) and ir01.IsKindOf(acm.FCollection):
            ir01 = ir01.At(0).Number()
            
        if isnan(ir01):
            ir01 = 0.00
            
        if (not ir01) and (not abs(ir01) >= 0):
            ir01 = 0.00
            
        return ir01

    def get_fx_swap_delta(self, fx_swap):
        '''return the fx delta of an FX Swap. fx_swap is an FAdhocportfolio containing both legs of an fx swap.'''

        currencies = self.get_currencies(fx_swap.Trades())
        values = []
        
        for currency in currencies:
            vector = acm.FArray()
            param = acm.FNamedParameters()
            param.AddParameter('currency', currency)
            vector.Add(param)
            config = acm.Sheet.Column().ConfigurationFromVector(vector)
            calc = self.CALC_SPACE.CreateCalculation(fx_swap, 'Portfolio FX Tpl Delta Cash', config)
            values.append(calc.Value())

        return values, list(currencies)
    
    def get_fx_delta_curr(self, virtual_portfolio, currency):
        '''return the fx tpl delta. Usually, for Volcker the passed currency will be the instrument
           currency
        '''
        
        vector = acm.FArray()
        param = acm.FNamedParameters()
        param.AddParameter('currency', currency)
        vector.Add(param)
        config = acm.Sheet.Column().ConfigurationFromVector(vector)
        calc = self.CALC_SPACE.CreateCalculation(virtual_portfolio, 'Portfolio FX Tpl Delta Cash', config)
        value = calc.Value()

        return value.Number()


    def get_ccy_fx_delta_curr(self, ccy_swap, currency):
        '''return the fx delta of an cross currency swap. For Volcker reporting, we need to report the delta per leg.'''
        
        vector = acm.FArray()
        param = acm.FNamedParameters()
        param.AddParameter('currency', currency)
        vector.Add(param)
        config = acm.Sheet.Column().ConfigurationFromVector(vector)
        
        calc = self.CALC_SPACE.CreateCalculation(ccy_swap, 'Portfolio FX Tpl Delta Cash', config)
        value = calc.Value()

        return value.Number()

    def clear_calc_space(self):
        '''garbage collection, etc.'''

        self.CALC_SPACE.RemoveGlobalSimulation('Portfolio Profit Loss End Date')
        #self.CALC_SPACE.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')
        
        self.CALC_SPACE.Clear()
        self.deal_sheet_space.Clear()

        for builder in acm.FCache.Select01('.StringKey = "evaluator builders"', "").Contents():
            builder.Reset()

        acm.Memory().GcWorldStoppedCollect()

    def get_position_id(self, virtual_portfolio):
        trade = virtual_portfolio.Trades().At(0)
        instrument = trade.Instrument()
        if instrument.Isin() != "":
            id_type = 'ISIN'
            id = instrument.Isin()
        elif instrument.add_info('SEDOL'):
            id_type = 'SEDOL'
            id = instrument.AdditionalInfo().SEDOL()
        else:
            id_type = 'InstrumentName'
            id = instrument.Name()
        
        if instrument.InsType() == 'CFD':
            position_ID = '%s-%s-%s-%s-%s' % ('0', instrument.Name(), trade.Currency().Name(), trade.Portfolio().Name(), datetime.strftime(to_datetime(self.repday), '%Y%m%d'))
        elif trade.IsFxSwap():
            position_ID = '%s-%s-%s-%s-%s' % (trade.ConnectedTrade().Oid(), instrument.Name(), trade.Currency().Name(), trade.Portfolio().Name(), datetime.strftime(to_datetime(self.repday), '%Y%m%d'))
        elif (trade.Counterparty().Id2() in EXCHANGE_TRADED or id_type != 'InstrumentName'  or instrument.InsType() == 'Curr') and (not instrument.Otc() or instrument.InsType() in ('Curr')):
            position_ID = '%s-%s-%s-%s-%s' % ('0', instrument.Name(), trade.Currency().Name(), trade.Portfolio().Name(), datetime.strftime(to_datetime(self.repday), '%Y%m%d'))
        else:
            position_ID = '%s-%s-%s-%s-%s' % (str(trade.Oid()), instrument.Name(), trade.Currency().Name(), trade.Portfolio().Name(), datetime.strftime(to_datetime(self.repday), '%Y%m%d'))

        return position_ID

    def get_virtual_portfolio(self, trades):
        virtual_portfolio = acm.FAdhocPortfolio()
        if trades.IsKindOf(acm.FTrade):
            virtual_portfolio.Add(trades)
        else:
            for trade in trades:
                virtual_portfolio.Add(trade)
        return virtual_portfolio

class Radial_Trade_Report(Volcker_Report):
    '''Volcker Report class for producing the inventory turnover trade file'''

    def __init__(self, ael_dict):
        super(Radial_Trade_Report, self).__init__(ael_dict)
        self.path = os.path.join(
            ael_dict['path'], 
            datetime.strftime(to_date(END_DATES[ael_dict['endDate']]), '%Y%m%d'), 
            ael_dict['radial_trade_file_name']
        )

        self.REPORT_ENTRY = namedtuple('volcker_report_entry', [
            'TRADE_ID', 
            'LEG', 
            'POSITION_ID', 
            'BOOK', 
            'INSTRUMENT_IDENTIFIER_TYPE',
            'INSTRUMENT_IDENTIFIER', 
            'INSTRUMENT_DESCRIPTION', 
            'TRADE_DATE',
            'TRADE_TIME', 
            'PRODUCT_NAME', 
            'BUY_SELL', 
            'TRADE_STATUS', 
            'CURRENCY',
            'COUNTERPARTY_TYPE', 
            'COUNTERPARTY_ID', 
            'NOTIONAL', 
            'CONTRACT_SIZE',
            'NUMBER_OF_CONTRACTS', 
            'UNDERLYING_PRICE', 
            'PRICE_DELTA',
            'INSTRUMENT_DELTA',
            'IR01',
            'MARKET_VALUE', 
            'SOURCE_SYSTEM', 
            'OPTION_TYPE', 
            'STRIKE', 
            'COUPON',
            'UNDERLYING_SYMBOL', 
            'PRICE', 
            'MATURITY_DATE', 
            'CURVE', 
            'AGE', 
            'BCML_PRODUCT_SUB_TYPE_YN',
            'QUANTITY',
            'AGE_METHODOLOGY', 
            'RATE', 
            'TENYRBOND_IR01',
            'RISKMEASURE',
            'MATURITY',
            'TEN_YEAR_BOND_UNIT',
            'FO_PRODUCT_TYPE',
            'SECTOR',
            'COUNTRY',
            'TRADE_VERSION',
            'IS_MARKET_MAKING',
            'SECONDARY_CURRENCY',
            'FO_SUB_PRODUCT_TYPE',
            'IS_BLOCK_OR_ALLOCATION',
            'IS_INTERNAL_TRADE'
        ])
    
    def load_data(self, trade_data):
        self.cash_trades = trade_data['cash']
        self.deriv_trades = trade_data['deriv']
        self.positions = trade_data['trades_per_position']
        self.fx_swaps = trade_data['fx_swaps_per_contract']
    
    def get_secondary_currency(self, trade, currencies):
        '''returns the secondary currency as defined for the Volcker project, e.g. on an FX trade'''

        secondary = ''
        if len(currencies) > 1:
            primary = trade.Currency()
            for curr in currencies:
                if curr != primary:
                    secondary = curr
                    break

        return secondary

    def get_age_method(self, trade_type):
        '''returns the age method'''

        if trade_type == 'Cash':
            age_method = 'C'
        else:
            age_method = 'D'

        return age_method

    def get_riskmeasure(self, trade, fx_swap):
        '''returns the used risk measure for a given trade or FAdhocPortfolio'''

        if trade.Instrument().InsType() in ('Swap', 'FRA', 'FRN', 'IndexLinkedSwap', 'Cap', 'Floor'):
            riskmeasure = 'IR01'

        elif (trade.Instrument().InsType() in ('Option', 'Future/Forward') and 
              trade.Instrument().Underlying().InsType() in ('Swap', 'FRA', 'FRN', 'IndexLinkedSwap', 'Cap', 'Floor')):

            riskmeasure = 'IR01'

        elif trade.Instrument().InsType() == 'Option':
            riskmeasure = 'Delta'

        elif trade.Instrument().InsType() in ('ETF', 'Stock'):
            riskmeasure = 'Market Value'

        elif trade.Instrument().InsType() in ('TotalReturnSwap'):
            tr_leg = None
            for leg in trade.Instrument().Legs():
                if leg.LegType() == 'Total Return':
                    tr_leg = leg
                    break
            if tr_leg and tr_leg.IndexRef() and tr_leg.IndexRef().InsType() in ('Bond', 'IndexLinkedBond'):
                riskmeasure = 'IR01'
            else:
                riskmeasure = 'Notional'

        elif fx_swap or trade.Instrument().InsType() in ('CurrSwap', 'Curr'):
            riskmeasure = 'FXDelta'
        else:
            riskmeasure = 'Notional'

        return riskmeasure

    def get_nominal(self, trade, fx_swap):
        if not fx_swap and not trade.Instrument().InsType() in ('CurrSwap', 'Curr'):
            nominal = self.get_trade_notional(trade)
        elif not fx_swap and trade.Instrument().InsType() in ('CurrSwap', 'Curr'):
            nominal = self.get_ccy_fx_delta_curr(trade, trade.Currency())
        else:
            nominal = self.get_fx_delta_curr(fx_swap, fx_swap.Trades().At(0).Currency())

        return nominal

    def get_delta(self, trade, fx_swap):

        if not fx_swap and not trade.Instrument().InsType() in ('CurrSwap', 'Curr'):
            delta_p = self.get_trade_delta(trade)
        elif not fx_swap and trade.Instrument().InsType() in ('CurrSwap', 'Curr'):
            delta_p = self.get_fx_delta_curr(trade, trade.Currency())
        else:
            delta_p = self.get_fx_delta_curr(fx_swap, fx_swap.Trades().At(0).Currency())

        return delta_p
    
    def get_currency(self, trade, fx_swap):
        if not fx_swap and not trade.Instrument().InsType() in ('CurrSwap', 'Curr'):
            curr = trade.Currency()
        elif not fx_swap and trade.Instrument().InsType() in ('CurrSwap', 'Curr'):
            curr = trade.Currency()
        else:
            curr = fx_swap.Trades().At(0).Currency()

        return curr
        
    def get_delta_instrument(self, trade):
        virtual_portfolio = acm.FAdhocPortfolio()
        virtual_portfolio.Add(trade)
        delta_i = self.get_instrument_delta(virtual_portfolio)

        return delta_i

    def get_id(self, instrument):
        if instrument.Isin() != "":
            id_type = 'ISIN'
            id = instrument.Isin()
        elif instrument.add_info('SEDOL'):
            id_type = 'SEDOL'
            id = instrument.AdditionalInfo().SEDOL()
        else:
            id_type = 'InstrumentName'
            id = instrument.Name()

        return id_type, id

    def get_buysell(self, trade, fx_swap):
        buysell = ''
        if trade.Quantity() >= 0:
            buysell = 'B'
        else:
            buysell = 'S'

        return buysell

    def get_counterparty_info(self, trade):

        if trade.Counterparty():
            cpty_id = trade.Counterparty().Name()
            try:
                cpty_id = trade.Counterparty().AdditionalInfo().BarCap_SMS_CP_SDSID()
                cpty_type = 'SDS'
            except:
                cpty_id = ''
                cpty_type = ''            
        else:
            cpty_id = ''
            cpty_type = ''

        return cpty_id, cpty_type

    def report_data(self, trade_or_portfolio, cash_qty, trade_type, file_type, repday, *rest):
        '''returns a list of report entries. For FX instruments this implies more than one line in the report'''

        fx_swap = None
        if trade_or_portfolio.IsKindOf(acm.FAdhocPortfolio):
            currencies = self.get_currencies(trade_or_portfolio.Trades())
            currencies = [e.Name() for e in currencies]

            #for fx swap calculation we put near and far leg into an FAdhocPortolio to perform the 
            #aggregated calculations
            fx_swap = trade_or_portfolio 

            version = sum([int(t.VersionId()) for t in trade_or_portfolio.Trades()])
            trade = trade_or_portfolio.Trades().At(0).ConnectedTrade()
            qty = trade.Quantity()
        else:
            trade = trade_or_portfolio
            currencies = self.get_currencies([trade])
            currencies = [e.Name() for e in currencies]
            qty = round(trade.Quantity(), 4)
            version = trade.VersionId()

        primary = self.get_currency(trade, fx_swap)
        secondary = self.get_secondary_currency(trade, currencies)

        age_method = self.get_age_method(trade_type)

        if not fx_swap:
            market_val = self.get_trade_market_val(trade, primary)    
        else:
            market_val = self.get_position_market_val(fx_swap, primary)
        
        riskmeasure = self.get_riskmeasure(trade, fx_swap)
        
        ins = trade.Instrument()
        ins_description = ins.Name()
        ins_type = ins.InsType()
        
        nominal = self.get_nominal(trade, fx_swap)
        delta_p = self.get_delta(trade, fx_swap)
        delta_i = self.get_delta_instrument(trade)
        
        if not fx_swap:
            ir01 = self.get_trade_ir01(trade, primary)
        else:
            ir01 = self.get_position_ir01(fx_swap, primary)

        id_type, id = self.get_id(ins)	
            
        t_date = datetime.strftime(to_datetime(trade.TradeTime()), '%Y%m%d')
        t_time = datetime.strftime(to_datetime(trade.TradeTime()), '%H:%M:%S')
        
        buysell = self.get_buysell(trade, fx_swap)
        cpty_id, cpty_type = self.get_counterparty_info(trade)
        
        # contract_size #
        if ins_type in ('Future/Forward', 'Option'):
            contract_size = str(ins.Underlying().ContractSize())
            contract = str(ins.ContractSize())
        else:
            contract_size = str(ins.ContractSize())
            contract = str(ins.ContractSize())
        
        if ins.Underlying():
            und_price = ins.Underlying().Calculation().MarketPrice(self.CALC_SPACE_COLLECTION, self.repday, True, ins.Underlying().Currency())
        else:
            und_price = 0.0
        if isnan(und_price):
            und_price = 0.00
            
        source_system = 'ABCAP_FRONT_ARENA'
        option_type = ''
        
        strike_price = ins.StrikePrice() if hasattr(ins, 'StrikePrice') else 0.0
        if isnan(strike_price):
            strike_price = 0.00
        
        coupon = ''
        underlying_symbol = ''
        price = trade.Price()

        if isnan(price):
            price = 0.00
        if ins.ExpiryDate():
            mat_date = datetime.strftime(to_datetime(ins.ExpiryDate()), '%Y%m%d')
        else:
            mat_date = datetime.strftime(to_datetime(repday), '%Y%m%d')

        #ITO
        if ins.MappedDiscountLink().Value().Link().YieldCurveComponent().Curve().Name():
            curve = ins.MappedDiscountLink().Value().Link().YieldCurveComponent().Curve().Name()
        else:   
            curve = ''

        # age #
        age_date = ael_date(to_datetime(trade.TradeTime()))
        age = age_date.days_between(repday)

        #Radial only fields
        try:
            rate = ins.FixedLeg.Rate()
        except:
            rate = 0.00
        
        tenYrBond = acm.FInstrument['ZAR/R186']
        try:
            self.CALC_SPACE.SimulateValue(tenYrBond, 'Portfolio Currency', primary)
            tenYrBondYld = self.CALC_SPACE.CalculateValue(tenYrBond, 'Portfolio Delta Yield')
        except Exception, e:
            tenYrBondYld = 0.00
        finally:
            self.CALC_SPACE.RemoveSimulation(tenYrBond, 'Portfolio Currency')
        
        position_ID = self.get_position_id(self.get_virtual_portfolio(trade))
        
        curr = self.get_currency(trade, fx_swap)
        
        print trade.Oid()
        
        data = []

        data.append(self.REPORT_ENTRY(
            TRADE_ID = str(trade.Oid()), 
            LEG = '2', 
            POSITION_ID = position_ID,
            BOOK = str(self.get_portfolio(trade)), 
            INSTRUMENT_IDENTIFIER_TYPE = id_type, 
            INSTRUMENT_IDENTIFIER = id, 
            INSTRUMENT_DESCRIPTION = ins_description, 
            TRADE_DATE = t_date, 
            TRADE_TIME = t_time, 
            PRODUCT_NAME = ins_type,
            BUY_SELL = buysell, 
            TRADE_STATUS = trade.Status(), 
            CURRENCY = curr.Name(), 
            COUNTERPARTY_TYPE = cpty_type, 
            COUNTERPARTY_ID = cpty_id, 
            NOTIONAL = nominal,
            CONTRACT_SIZE = contract_size, 
            NUMBER_OF_CONTRACTS = contract,
            UNDERLYING_PRICE = str(round(und_price, 2)), 
            PRICE_DELTA = str(round(delta_p, 2)), 
            INSTRUMENT_DELTA = str(round(delta_i, 2)),
            IR01 = str(round(ir01, 2)), 
            MARKET_VALUE = str(round(market_val, 2)), 
            SOURCE_SYSTEM = source_system, 
            OPTION_TYPE = option_type, 
            STRIKE = str(round(strike_price, 6)), 
            COUPON = coupon, 
            UNDERLYING_SYMBOL = underlying_symbol, 
            PRICE = str(round(price, 6)), 
            MATURITY_DATE = mat_date, 
            CURVE = str(curve), 
            AGE = str(age), 
            BCML_PRODUCT_SUB_TYPE_YN = 'N', 
            QUANTITY = str(qty), 
            AGE_METHODOLOGY = age_method,
            RATE = str(round(rate, 2)),
            TENYRBOND_IR01 = str(round(tenYrBondYld, 2)),
            RISKMEASURE = riskmeasure,
            MATURITY = trade.maturity_date(),
            TEN_YEAR_BOND_UNIT = trade.Currency().Name(),
            FO_PRODUCT_TYPE = ins_type,
            SECTOR = '',
            COUNTRY = '',
            TRADE_VERSION = str(version),
            IS_MARKET_MAKING = '',
            SECONDARY_CURRENCY = secondary,
            FO_SUB_PRODUCT_TYPE = '',
            IS_BLOCK_OR_ALLOCATION = '',
            IS_INTERNAL_TRADE = 'Yes' if self.is_internal_trade(trade) else 'No'
        ))

        self.CALC_SPACE.Clear()
        return data

    def perform(self):
        with open(self.path, 'w') as f_rad:
            writer = csv.DictWriter(
                f_rad,
                self.REPORT_ENTRY._fields,
                delimiter='|',
                lineterminator = '\n'
            )

            #write header
            writer.writerow(dict(list(zip(self.REPORT_ENTRY._fields, self.REPORT_ENTRY._fields))))
            
            self.calc_size = 0
            for contr, instr, curr, portf in self.positions:
                for trd in self.positions[contr, instr, curr, portf]:
                    if self.calc_size > 1000:
                        self.clear_calc_space()
                        self.CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Now')
                        self.calc_size = 0
                    self.calc_size += 1
                
                    if acm_date(to_datetime(trd.TradeTime())) != acm_date(self.repday):
                        continue
                
                    self.CALC_SPACE.SimulateValue(trd, 'Portfolio Currency', trd.Currency())

                    lines = self.report_data(trd, 0, 'Cash', 'RADIAL', self.repday)

                    self.CALC_SPACE.RemoveSimulation(trd, 'Portfolio Currency')

                    for line in lines:
                        line_temp = line._asdict()
                        writer.writerow(line_temp)
            
            for c in self.fx_swaps:
                if self.calc_size > 1000:
                    self.clear_calc_space()
                    self.CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Now')
                    self.calc_size = 0
                self.calc_size += 1
                
                fx_swap_trades = []
                for t in self.fx_swaps[c]:
                    if acm_date(to_datetime(t.TradeTime())) != acm_date(self.repday):
                        continue
                    #if t.IsFxSwapNearLeg():
                    fx_swap_trades.append(t)
                if len(fx_swap_trades) == 0:
                    break
                
                virtual_portfolio = acm.FAdhocPortfolio()
                for t in fx_swap_trades:
                    virtual_portfolio.Add(t)
                
                self.CALC_SPACE.SimulateValue(virtual_portfolio, 'Portfolio Currency', c.Currency())
                lines = self.report_data(virtual_portfolio, 0, 'Deriv', 'BOTH', self.repday)
                self.CALC_SPACE.RemoveSimulation(virtual_portfolio, 'Portfolio Currency')
                
                for line in lines:
                    line_temp = line._asdict()
                    writer.writerow(line_temp)
                    
class Radial_Position_Report(Volcker_Report):
    def __init__(self, ael_dict):
        super(Radial_Position_Report, self).__init__(ael_dict)
        self.path = os.path.join(
            ael_dict['path'], 
            datetime.strftime(to_date(END_DATES[ael_dict['endDate']]), '%Y%m%d'), 
            ael_dict['radial_position_file_name']
        )
        
        self.REPORT_ENTRY = namedtuple('radial_position', [
            'POSITION_ID',
            'BOOK',
            'SECURITY_IDENTIFIER',
            'SECURITY_DESCRIPTION',
            'PRODUCT_NAME',
            'LONG_SHORT',
            'CURRENCY',
            'ORIGINAL_NOTIONAL',
            'MARKET_VALUE',
            'DELTA',
            'DELTA_INSTRUMENT',
            'IR01',
            'TENYRIR01',
            'SOURCE_SYSTEM',
            'RISKMEASURE',
            'TEN_YEAR_BOND_UNIT',
            'IS_MARKET_MAKING',
            'SECONDARY_CURRENCY',
            'FO_SUB_PRODUCT_TYPE'
        ])
    
    def get_delta(self, virtual_portfolio):
        first_trade = virtual_portfolio.Trades().At(0)
        if not first_trade.IsFxSwap() and not first_trade.Instrument().InsType() in ('CurrSwap', 'Curr'):
            delta_p = self.get_position_delta(virtual_portfolio)
        elif not first_trade.IsFxSwap() and first_trade.Instrument().InsType() in ('CurrSwap', 'Curr'):
            delta_p = self.get_fx_delta_curr(virtual_portfolio, first_trade.Currency())
        else:
            delta_p = self.get_fx_delta_curr(virtual_portfolio, first_trade.Currency())

        return delta_p
    
    def get_fx_swap_delta(self, fx_swap):
        currencies = set()
        values = []
        first_trade = fx_swap.Trades().At(0)
        currencies.add(first_trade.Currency().Name())
        currencies.add(first_trade.Instrument().Currency().Name())
        
        for currency in currencies:
            vector = acm.FArray()
            param = acm.FNamedParameters()
            param.AddParameter('currency', acm.FInstrument[currency])
            vector.Add(param)
            config = acm.Sheet.Column().ConfigurationFromVector(vector)
            
            calc = self.CALC_SPACE.CreateCalculation(fx_swap, 'Portfolio FX Tpl Delta Cash', config)
            values.append(calc.Value())
        return values, list(currencies)
    
    def get_ccy_fx_delta(self, ccy_swap):
        first_trade = ccy_swap.Trades().At(0)
        currencies = set()
        values = []
        legs = first_trade.Instrument().Legs()
        for leg in legs:
            currencies.add(leg.Currency().Name())
        
        for currency in currencies:
            vector = acm.FArray()
            param = acm.FNamedParameters()
            param.AddParameter('currency', acm.FInstrument[currency])
            vector.Add(param)
            config = acm.Sheet.Column().ConfigurationFromVector(vector)
        
            calc = self.CALC_SPACE.CreateCalculation(ccy_swap, 'Portfolio FX Tpl Delta Cash', config)
            values.append(calc.Value())
        return values, list(currencies)
    
    def radial_position_data(self, virtual_portfolio, trade_type, repday):
        first_trade = virtual_portfolio.Trades().At(0)
        currencies = self.get_currencies(virtual_portfolio.Trades())
        currencies = [e.Name() for e in currencies]
        secondary = ''
        if len(currencies) > 1:
            primary = first_trade.Currency()
            for curr in currencies:
                if curr != primary:
                    secondary = curr
                    break
        #instrument = first_trade.Instrument()
        market_val = self.get_position_market_val(virtual_portfolio)
        #ins_description = instrument.Name()
        
        delta_p = self.get_delta(virtual_portfolio)
        delta_i = self.get_instrument_delta(virtual_portfolio)
        ir = self.get_position_ir01(virtual_portfolio)
        position = self.calculate_value(virtual_portfolio, 'Portfolio Position', repday)
        t_day = datetime.strftime(to_datetime(repday), '%Y%m%d')
        notional = self.get_position_notional(virtual_portfolio)
        
        instrument = first_trade.Instrument()
        ins_description = instrument.Name()
        ins_type = instrument.InsType()
        
        
        if instrument.Isin() != "":
            id_type = 'ISIN'
            id = instrument.Isin()
        elif instrument.add_info('SEDOL'):
            id_type = 'SEDOL'
            id = instrument.AdditionalInfo().SEDOL();
        else:
            id_type = 'InstrumentName'
            id = instrument.Name()
        
        position_ID = self.get_position_id(virtual_portfolio)

        if position >= 0:
            longshort = 'L'
        else:
            longshort = 'S'
        
        tenYrBond = acm.FInstrument['ZAR/R186']
        try:
            self.CALC_SPACE.SimulateValue(tenYrBond, 'Portfolio Currency', first_trade.Currency())
            tenYrBondir01 = self.calculate_value(tenYrBond, 'Portfolio Delta Yield', repday)
        except Exception, e:
            print e
            tenYrBondir01 = 0.00
        finally:
            self.CALC_SPACE.RemoveSimulation(tenYrBond, 'Portfolio Currency')
        
        if type(delta_p) == list:
            currency = currencies
            delta_p = [str(round(e.Number(), 2)) for e in delta_p]
        else:
            currency = str(first_trade.Currency().Name())
            delta_p = str(round(delta_p, 2))
        
        if instrument.InsType() in ('Swap', 'FRA', 'FRN', 'IndexLinkedSwap'):
            riskmeasure = 'IR01'
        elif instrument.InsType() == 'Option':
            riskmeasure = 'Delta'
        elif instrument.InsType() in ('ETF', 'Stock'):
            riskmeasure = 'Market Value'
        elif instrument.InsType() in ('TotalReturnSwap'):
            tr_leg = None
            for leg in instrument.Legs():
                if leg.LegType() == 'Total Return':
                    tr_leg = leg
                    break
            if tr_leg and tr_leg.IndexRef() and tr_leg.IndexRef().InsType() in ('Bond', 'IndexLinkedBond'):
                riskmeasure = 'IR01'
            else:
                riskmeasure = 'Notional'
        elif instrument.InsType() in ('Curr', 'CurrSwap'):
            riskmeasure = 'FXDelta'
        else:
            riskmeasure = 'Notional'
        
        data = self.REPORT_ENTRY(
            POSITION_ID = str(position_ID),
            BOOK = str(self.get_portfolio(virtual_portfolio.Trades().At(0))),
            SECURITY_IDENTIFIER = id,
            SECURITY_DESCRIPTION = id_type,
            PRODUCT_NAME = ins_type,
            LONG_SHORT = longshort,
            CURRENCY = currency,
            ORIGINAL_NOTIONAL = notional,
            MARKET_VALUE = str(round(market_val, 2)),
            DELTA = delta_p,
            DELTA_INSTRUMENT = str(round(delta_i, 2)),	
            IR01 = str(round(ir, 2)),
            TENYRIR01 = str(round(tenYrBondir01, 2)),
            SOURCE_SYSTEM = 'ABCAP_FRONT_ARENA',
            RISKMEASURE = riskmeasure,
            TEN_YEAR_BOND_UNIT = first_trade.Currency().Name(),
            IS_MARKET_MAKING = '',
            SECONDARY_CURRENCY = secondary,
            FO_SUB_PRODUCT_TYPE = ''
        )
        self.CALC_SPACE.Clear()
        return data
        
    def load_data(self, trade_data):
        self.data = trade_data['trades_per_position']
        self.fx_swaps = trade_data['fx_swaps_per_contract']
        
    def perform(self):
        with open(self.path, 'w') as f_rad_pos:
            writer = csv.DictWriter(
                f_rad_pos,
                self.REPORT_ENTRY._fields,
                delimiter='|',
                lineterminator = '\n'
            )
            writer.writerow(dict(list(zip(self.REPORT_ENTRY._fields, self.REPORT_ENTRY._fields))))
            
            calc_size = 0
            for contr, instr, curr, portf in self.data:
                if calc_size > 1000:
                    self.clear_calc_space()
                    self.CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Now')
                    #CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss Use MtM Today', 'Fallback')
                    calc_size = 0
                calc_size += 1
                virtual_portfolio = acm.FAdhocPortfolio()
                #print derivate_trades_per_position[(instr, portf)]
                for t in self.data[(contr, instr, curr, portf)]:
                    virtual_portfolio.Add(t)
                
                first_trade = virtual_portfolio.Trades().At(0)
                self.CALC_SPACE.SimulateValue(virtual_portfolio, 'Portfolio Currency', first_trade.Currency())
                line = self.radial_position_data(virtual_portfolio, '', self.repday)
                self.CALC_SPACE.RemoveSimulation(virtual_portfolio, 'Portfolio Currency')
                line_temp = line._asdict()
   
                writer.writerow(line._asdict())
                    
            for contr in self.fx_swaps:
                if calc_size > 1000:
                    self.clear_calc_space()
                    self.CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Now')
                    #CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss Use MtM Today', 'Fallback')
                    calc_size = 0
                calc_size += 1
                virtual_portfolio = acm.FAdhocPortfolio()
                #print derivate_trades_per_position[(instr, portf)]
                for t in self.fx_swaps[contr]:
                    virtual_portfolio.Add(t)
                
                first_trade = virtual_portfolio.Trades().At(0)
                self.CALC_SPACE.SimulateValue(virtual_portfolio, 'Portfolio Currency', first_trade.Currency())
                line = self.radial_position_data(virtual_portfolio, '', self.repday)
                self.CALC_SPACE.RemoveSimulation(virtual_portfolio, 'Portfolio Currency')
                
                line_temp = line._asdict()
                writer.writerow(line._asdict())

class Radial_RENTD_Report(Volcker_Report):
    def __init__(self, ael_dict):
        super(Radial_RENTD_Report, self).__init__(ael_dict)
        self.path = os.path.join(
            ael_dict['path'], 
            datetime.strftime(to_date(END_DATES[ael_dict['endDate']]), '%Y%m%d'), 
            ael_dict['rentd_file_name']
        )

        self.REPORT_ENTRY = namedtuple('radial_position', [
            'FEEDSYSTEM',
            'RISKSYSTEMTYPE',
            'RISKSYSTEMINSTANCE',
            'RISKCONFIGURATIONID',
            'RISKSUBJECTID',
            'RISKSUBJECTVERSION',
            'TYPENAME',
            'VALUATIONNAME',
            'BOOKID',
            'TRADECCY',
            'SENSITIVITYNAME',
            'SENSTIVITYCONFIGURATIONID',
            'VALUE',
            'DATAOBJECT1ID',
            'DATAOBJECT1TYPE',
            'DATAOBJECT1CURVEID',
            'DATAOBJECT1CCY',
            'DATAOBJECT1INSTRUMENTTYPE',
            'DATAOBJECT1INDEX',
            'DATAOBJECT1INSTRUMENTID',
            'DATAOBJECT1PROJECTIONID',
            'DATAOBJECT1AXIS1',
            'DATAOBJECT1AXIS1PARAM1',
            'DATAOBJECT1AXIS1PARAM2',
            'DATAOBJECT1AXIS1PARAM3',
            'DATAOBJECT1AXIS2',
            'DATAOBJECT1AXIS2PARAM1',
            'DATAOBJECT1AXIS2PARAM2',
            'DATAOBJECT1AXIS2PARAM3',
            'DATAOBJECT1AXIS3',
            'DATAOBJECT1AXIS3PARAM1',
            'DATAOBJECT1AXIS3PARAM2',
            'DATAOBJECT1AXIS3PARAM3',
            'DATAOBJECT2ID',
            'DATAOBJECT2TYPE',
            'DATAOBJECT2CURVEID',
            'DATAOBJECT2CURVECCY',
            'DATAOBJECT2INSTRUMENTTYPE',
            'DATAOBJECT2INDEX',
            'DATAOBJECT2INSTRUMENTID',
            'DATAOBJECT2PROJECTIONID',
            'DATAOBJECT2AXIS1',
            'DATAOBJECT2AXIS1PARAM1',
            'DATAOBJECT2AXIS1PARAM2',
            'DATAOBJECT2AXIS1PARAM3',
            'DATAOBJECT2AXIS2',
            'DATAOBJECT2AXIS2PARAM1',
            'DATAOBJECT2AXIS2PARAM2',
            'DATAOBJECT2AXIS2PARAM3',
            'DATAOBJECT2AXIS3',
            'DATAOBJECT2AXIS3PARAM1',
            'DATAOBJECT2AXIS3PARAM2',
            'DATAOBJECT2AXIS3PARAM3',
            'DATAOBJECT3ID',
            'DATAOBJECT3TYPE',
            'DATAOBJECT3CURVEID',
            'DATAOBJECT3CURVECCY',
            'DATAOBJECT3INSTRUMENTTYPE',
            'DATAOBJECT3INDEX',
            'DATAOBJECT3INSTRUMENTID',
            'DATAOBJECT3PROJECTIONID',
            'DATAOBJECT3AXIS1',
            'DATAOBJECT3AXIS1PARAM1',
            'DATAOBJECT3AXIS1PARAM2',
            'DATAOBJECT3AXIS1PARAM3',
            'DATAOBJECT3AXIS2',
            'DATAOBJECT3AXIS2PARAM1',
            'DATAOBJECT3AXIS2PARAM2',
            'DATAOBJECT3AXIS2PARAM3',
            'DATAOBJECT3AXIS3',
            'DATAOBJECT3AXIS3PARAM1',
            'DATAOBJECT3AXIS3PARAM2',
            'DATAOBJECT3AXIS3PARAM3'
        ])
     
    def get_risk_factor_types(self, instr):
        ir01 = [
            'BasketRepo/Reverse',
            'Deposit',
            'Bill',
            'Bond',
            'BuySellback',
            'Cap',
            'CD',
            'DualCurrBond',
            'Floor',
            'RateIndex',
            'FRA',
            'FreeDefCF',
            'FRN',
            'IndexLinkedBond',
            'IndexLinkedSwap',
            'Repo/Reverse',
            'SecurityLoan',
            'Swap',
            'Zero',
    
        ]

        cs01 = [
            'CLN',
            'CreditDefaultSwap',

        ]
        
        commodity  = ['Commodity', 'Commodity Index', 'Commodity Variant', 'PriceSwap']

        ir_derivatives = [
            'Future/Forward',
            'Option'
        ] 

        equity = [
            'CFD',
            'ETF',
            'Stock',
            'VarianceSwap'    
        ]

        eq_derivatives = [
            'Future/Forward',
            'Option',
            'TotalReturnSwap'
        ]

        
        fx = [
            'Curr',
            'CurrSwap',
            'FXOptionDatedFwd'
        ]

        risk_factors = []
        try:
            if instr.InsType() in ir01:
                risk_factors.append('ir01')
            elif instr.InsType() == 'Option' and instr.Underlying().InsType() in ir01:
                risk_factors.append('ir01')
                risk_factors.append('ir_vega')
            elif instr.InsType() in ir_derivatives and instr.Underlying().InsType() in ir01:
                risk_factors.append('ir01')
            elif instr.InsType() == 'TotalReturnSwap' and instr.FirstTotalReturnLeg().IndexRef().InsType() in ir01:
                risk_factors.append('ir01')
            elif instr.InsType() in cs01:
                risk_factors.append('cs01')
            elif instr.InsType() in commodity:
                risk_factors.append('price01')
            elif instr.InsType() == 'Future/Forward' and instr.Underlying().InsType() in commodity:
                risk_factors.append('price01')
            elif instr.InsType() == 'Option' and instr.Underlying().InsType() in commodity:
                risk_factors.append('price01')
                risk_factors.append('comm_vega')
            elif instr.InsType() in equity:
                risk_factors.append('equity_delta')
            elif instr.InsType() in 'Future/Forward' and instr.Underlying().InsType() in equity:
                risk_factors.append('equity_delta')
            elif instr.InsType() == 'TotalReturnSwap' and instr.FirstTotalReturnLeg().IndexRef().InsType() in equity:
                risk_factors.append('equity_delta')
            elif instr.InsType() == 'Option' and instr.Underlying().InsType() in equity:
                risk_factors.append('equity_delta')
                risk_factors.append('eq_vega')
            elif instr.InsType() in fx:
                risk_factors.append('fx_delta')
            elif instr.InsType() == 'Future/Forward' and instr.Underlying().InsType() in fx:
                risk_factors.append('fx_delta')
            elif instr.InsType() == 'Option' and instr.Underlying().InsType() in fx:
                risk_factors.append('fx_delta')
                risk_factors.append('fx_vega')
            else:
                risk_factors.append('ir01')
        except Exception, e:
            risk_factors.append('ir01')
        return risk_factors

    def load_data(self, trade_data):
        self.positions = trade_data['trades_per_position']
        self.fx_swap = trade_data['fx_swaps_per_contract']

    def get_virtual_portfolio(self, trades):
        virtual_portfolio = acm.FAdhocPortfolio()
        for trade in trades:
            virtual_portfolio.Add(trade)

        return virtual_portfolio
    
    def get_vega(self, instr, virtual_portfolio, curr=None):
        first_trade = virtual_portfolio.Trades().At(0)
        currency = first_trade.Currency()

        node = self.deal_sheet_space.InsertItem(virtual_portfolio)
        self.deal_sheet_space.Refresh()
        node.Expand(True)
        self.deal_sheet_space.Refresh()
        child = node.Iterator().FirstChild().Tree()
        self.deal_sheet_space.Refresh()


        volatility_structure = self.deal_sheet_space.CreateCalculation(child, 'Volatility Structure Name').Value()
    
        node = self.CALC_SPACE.InsertItem(virtual_portfolio)
        self.CALC_SPACE.Refresh()
        node.Expand(True)
        self.CALC_SPACE.Refresh()
        child = node.Iterator().FirstChild().Tree()
        self.CALC_SPACE.Refresh()
        
        self.CALC_SPACE.SimulateValue(node, 'Portfolio Currency', first_trade.Currency())
        
        vega = self.CALC_SPACE.CreateCalculation(node, 'Portfolio Vega')
        
        vega = vega.Value().Number()

        self.CALC_SPACE.RemoveSimulation(node, 'Portfolio Currency')

        return volatility_structure, vega
    
    def get_price_curve_ir01(self, virtual_portfolio, curr=None):
        node = self.CALC_SPACE.InsertItem(virtual_portfolio)
        self.CALC_SPACE.Refresh()

        first_trade = virtual_portfolio.Trades().At(0)
        currency = first_trade.Currency()
        

        relevant_curve = self.CALC_SPACE.CreateCalculation(node, 'BasePriceCurveInTheoreticalValue')
        if not relevant_curve.Value():
            return '', ''
            
        self.CALC_SPACE.SimulateValue(node, 'Portfolio Currency', first_trade.Currency())
        
        delta = self.CALC_SPACE.CreateCalculation(node, 'Price Curve Delta')
        
        price_curve = relevant_curve.Value().Name()
        try:
            p_delta = delta.Value().Number()
        except:
            traceback.print_exc()
            p_delta = ''

        self.CALC_SPACE.RemoveSimulation(node, 'Portfolio Currency')

        return price_curve, p_delta    

    def get_fx_delta(self, virtual_portfolio, curr=None):
        currencies = self.get_currencies(virtual_portfolio.Trades())
    
        resultVector = []
        for curr in currencies:
            params = acm.FNamedParameters()

            params.Name(curr.Name())
            params.UniqueTag(curr.Oid())
            params.AddParameter('currency', curr)
            resultVector.append(params)
    
        config = acm.Sheet.Column().ConfigurationFromVector(resultVector)
        calc  = self.CALC_SPACE.CreateCalculation(virtual_portfolio, 'Portfolio FX Tpl Delta Cash', config)
        deltas = {}
        if len(currencies) > 1:
            for currency, delta in zip(currencies, [elem.Number() for elem in calc.Value()]):
                deltas[currency.Name()] = delta
        else:
            deltas[currencies[0].Name()] = calc.Value().Number()
            
        return deltas
    
    
    def get_equity_delta(self, virtual_portfolio, curr=None):
        first_trade = virtual_portfolio.Trades().At(0)
        currency = first_trade.Currency()

        self.CALC_SPACE.SimulateValue(virtual_portfolio, 'Portfolio Currency', first_trade.Currency())
        calc  = self.CALC_SPACE.CreateCalculation(virtual_portfolio, 'Portfolio Delta Implicit Equity')

        eq_delta = calc.Value()
        if eq_delta:
            eq_delta = eq_delta.Number()
        else:
            eq_delta = 0.0        
        
        self.CALC_SPACE.RemoveSimulation(virtual_portfolio, 'Portfolio Currency')

        return eq_delta
    
    def get_cs_01(self, virtual_portfolio, curr=None):
        first_trade = virtual_portfolio.Trades().At(0)
        currency = first_trade.Currency()

        self.CALC_SPACE.SimulateValue(virtual_portfolio, 'Portfolio Currency', first_trade.Currency())
        calc  = self.CALC_SPACE.CreateCalculation(virtual_portfolio, 'Flat Credit Par Delta')

        instr = virtual_portfolio.Trades().At(0).Instrument()
        credit_curve = instr.Calculation().MappedCreditCurve(self.CALC_SPACE_COLLECTION)

        credit_curve = credit_curve.Name()
        cs01 = calc.Value().Number()

        self.CALC_SPACE.RemoveSimulation(virtual_portfolio, 'Portfolio Currency')

        return credit_curve, cs01

    def get_ir_trs_delta(virtual_portfolio, curr=None):
        pass
    
    def get_ir_01(self, virtual_portfolio, curr=None):
        node = self.CALC_SPACE.InsertItem(virtual_portfolio)
        self.CALC_SPACE.Refresh()
        relevant_curves = self.CALC_SPACE.CreateCalculation(node, 'BenchmarkCurvesInTheoreticalValue')
        vector = acm.FArray()

        first_trade = virtual_portfolio.Trades().At(0)
        currency = first_trade.Currency()

        param = acm.FNamedParameters()

        delta_per_benchmark = defaultdict(list)
        delta_per_curve = {}
        if not relevant_curves.Value():
            return {}, {}
        elif not relevant_curves.Value().IsKindOf(acm.FCollection):
            relevant_curves = [relevant_curves.Value()]
        else:
            relevant_curves = relevant_curves.Value()
        
        for yc in relevant_curves:
            benchmarks = [b.Instrument() for b in yc.Benchmarks()]
            resultVector = []
            delta_per_curve_sum = 0
        
            for ins in benchmarks:
                params = acm.FNamedParameters()

                params.Name(ins.Name())
                params.UniqueTag(ins.Oid())
                params.AddParameter('instrument', ins)
                resultVector.append(params)
            

            config = acm.Sheet.Column().ConfigurationFromVector(resultVector)
            self.CALC_SPACE.SimulateValue(node, 'Portfolio Currency', first_trade.Currency())
            delta_vector = self.CALC_SPACE.CreateCalculation(node, 'Benchmark Delta Instruments', config)
            if (len(benchmarks) > 1):
                for instr, delta in zip(benchmarks, delta_vector.Value()):
                    delta_per_benchmark[yc.Name(), instr.Name()] = delta.Number()
                    delta_per_curve_sum  += delta.Number()
                delta_per_curve[yc.Name()] = delta_per_curve_sum
            else:
                delta_per_benchmark[yc.Name(), benchmarks[0].Instrument().Name()] = delta_vector.Value().Number()
                delta_per_curve_sum  += delta_vector.Value().Number()
            self.CALC_SPACE.RemoveSimulation(node, 'Portfolio Currency')

        return delta_per_curve, delta_per_benchmark

    def write_risk_factor(self, writer, instr, portf, risk_subject_id, risk_subject_type, 
                          sensitivity_name, sensitivity_config, value, **kwargs):

        data = self.REPORT_ENTRY(
            FEEDSYSTEM = 'ABSA',
            RISKSYSTEMTYPE = 'ABCAP_FRONT_ARENA',
            RISKSYSTEMINSTANCE = '',
            RISKCONFIGURATIONID = '',
            RISKSUBJECTID = risk_subject_id,
            RISKSUBJECTVERSION = kwargs['risk_subject_version'] if kwargs.has_key('risk_subject_version') else 0,
            TYPENAME = risk_subject_type,
            VALUATIONNAME = datetime.strftime(to_datetime(self.repday), '%Y%m%d'),
            BOOKID = portf.Trades().At(0).Portfolio().Oid(),
            TRADECCY = portf.Trades().At(0).Currency().Name(),
            SENSITIVITYNAME = sensitivity_name,
            SENSTIVITYCONFIGURATIONID = sensitivity_config,
            VALUE = round(decimal.Decimal(str(value)), 5) if value != '' else 0.0,
            DATAOBJECT1ID = kwargs['data_object1_id'] if kwargs.has_key('data_object1_id')  else '',
            DATAOBJECT1TYPE = kwargs['data_object1_type'] if kwargs.has_key('data_object1_type') else '',
            DATAOBJECT1CURVEID = kwargs['data_object1_curve_id'] if kwargs.has_key('data_object1_curve_id') else '',
            DATAOBJECT1CCY = kwargs['data_object1_ccy'] if kwargs.has_key('data_object1_ccy') else '',
            DATAOBJECT1INSTRUMENTTYPE = kwargs['data_object1_instype'] if kwargs.has_key('data_object1_instype') else '',
            DATAOBJECT1INDEX = kwargs['data_object1_index'] if kwargs.has_key('data_object1_index') else '',
            DATAOBJECT1INSTRUMENTID = kwargs['data_object1_instrument_id'] if kwargs.has_key('data_object1_instrument_id') else '',
            DATAOBJECT1PROJECTIONID = kwargs['data_object1_projection_id'] if kwargs.has_key('data_object1_projection_id') else '',
            DATAOBJECT1AXIS1 = kwargs['data_object1_axis1'] if kwargs.has_key('data_object1_axis1') else '',
            DATAOBJECT1AXIS1PARAM1 = kwargs['data_object1_axis1_param1'] if kwargs.has_key('data_object1_axis1_param1') else '',
            DATAOBJECT1AXIS1PARAM2 = kwargs['data_object1_axis1_param2'] if kwargs.has_key('data_object1_axis1_param2') else '',
            DATAOBJECT1AXIS1PARAM3 = kwargs['data_object1_axis1_param3'] if kwargs.has_key('data_object1_axis1_param3') else '',
            DATAOBJECT1AXIS2 = '',
            DATAOBJECT1AXIS2PARAM1 = '',
            DATAOBJECT1AXIS2PARAM2 = '',
            DATAOBJECT1AXIS2PARAM3 = '',
            DATAOBJECT1AXIS3 = '',
            DATAOBJECT1AXIS3PARAM1 = '',
            DATAOBJECT1AXIS3PARAM2 = '',
            DATAOBJECT1AXIS3PARAM3 = '',
            DATAOBJECT2ID = '',
            DATAOBJECT2TYPE = '',
            DATAOBJECT2CURVEID = '',
            DATAOBJECT2CURVECCY = '',
            DATAOBJECT2INSTRUMENTTYPE = '',
            DATAOBJECT2INDEX = '',
            DATAOBJECT2INSTRUMENTID = '',
            DATAOBJECT2PROJECTIONID = '',
            DATAOBJECT2AXIS1 = '',
            DATAOBJECT2AXIS1PARAM1 = '',
            DATAOBJECT2AXIS1PARAM2 = '',
            DATAOBJECT2AXIS1PARAM3 = '',
            DATAOBJECT2AXIS2 = '',
            DATAOBJECT2AXIS2PARAM1 = '',
            DATAOBJECT2AXIS2PARAM2 = '',
            DATAOBJECT2AXIS2PARAM3 = '',
            DATAOBJECT2AXIS3 = '',
            DATAOBJECT2AXIS3PARAM1 = '',
            DATAOBJECT2AXIS3PARAM2 = '',
            DATAOBJECT2AXIS3PARAM3 = '',
            DATAOBJECT3ID = '',
            DATAOBJECT3TYPE = '',
            DATAOBJECT3CURVEID = '',
            DATAOBJECT3CURVECCY = '',
            DATAOBJECT3INSTRUMENTTYPE = '',
            DATAOBJECT3INDEX = '',
            DATAOBJECT3INSTRUMENTID = '',
            DATAOBJECT3PROJECTIONID = '',
            DATAOBJECT3AXIS1 = '',
            DATAOBJECT3AXIS1PARAM1 = '',
            DATAOBJECT3AXIS1PARAM2 = '',
            DATAOBJECT3AXIS1PARAM3 = '',
            DATAOBJECT3AXIS2 = '',
            DATAOBJECT3AXIS2PARAM1 = '',
            DATAOBJECT3AXIS2PARAM2 = '',
            DATAOBJECT3AXIS2PARAM3 = '',
            DATAOBJECT3AXIS3 = '',
            DATAOBJECT3AXIS3PARAM1 = '',
            DATAOBJECT3AXIS3PARAM2 = '',
            DATAOBJECT3AXIS3PARAM3 = ''
        )

        writer.writerow(data._asdict())

    def get_benchmark_order(self, insid, ycid):
        yc = acm.FYieldCurve[ycid]
        benchmarks = yc.Benchmarks()
        instruments = [b.Instrument() for b in benchmarks]
        instruments = sorted(instruments, key = lambda e: e.maturity_date())
        instruments = [i.Name() for i in instruments]

        return instruments.index(insid)

    def get_period_identifier(self, insid):
        return acm.FInstrument[insid].maturity_date()

    def get_start_date(self, insid):
        return self.repday

    def get_end_date(self, insid):
        return acm.FInstrument[insid].maturity_date()

    def write_risk_data(self, instr, portf, risk_factor_types, writer, risk_subject_id, subject_type):

        self.write_risk_factor(writer, instr, portf, risk_subject_id, subject_type, 'MARK_TO_MARKET_VALUE', 'SCALAR', self.get_position_market_val(portf))
        self.write_risk_factor(writer, instr, portf, risk_subject_id, subject_type, 'NOTIONAL', 'SCALAR', self.get_position_notional(portf))

        for risk_factor in risk_factor_types:
            if risk_factor == 'ir01':
                delta_per_curve, delta_per_benchmark = self.get_ir_01(portf)
                for yc in delta_per_curve:
                    if yc:
                        self.write_risk_factor(writer, instr, portf, risk_subject_id, subject_type, 'IRDELTA', 'SCALAR', 
                                               delta_per_curve[yc], data_object1_id=yc, data_object1_type = 'Yield Curve')

            elif risk_factor == 'cs01':
                credit_curve, cs01 = self.get_cs_01(portf)
                if credit_curve:
                    self.write_risk_factor(writer, instr, portf, risk_subject_id, subject_type, 'CREDITDELTA', 'SCALAR', 
                                           cs01, data_object1_id=credit_curve, data_object1_type = 'Credit Curve')

            elif risk_factor == 'price01':
                price_curve, price_delta = self.get_price_curve_ir01(portf)
                if price_curve:
                    self.write_risk_factor(writer, instr, portf, risk_subject_id, subject_type, 'PRICEDELTA', 'SCALAR', 
                                           price_delta, data_object1_id=price_curve, data_object1_type = 'Price Curve')

            elif risk_factor == 'fx_vega':
                volatility_structure, vega = self.get_vega(instr, portf)
                if volatility_structure:
                    self.write_risk_factor(writer, instr, portf, risk_subject_id, subject_type, 'FXVEGA', 'SCALAR', 
                                           vega, data_object1_id=volatility_structure, data_object1_type = 'Volatility Surface')
            elif risk_factor == 'comm_vega':
                volatility_structure, vega = self.get_vega(instr, portf)
                if volatility_structure:
                    self.write_risk_factor(writer, instr, portf, risk_subject_id, subject_type, 'COMMVEGA', 'SCALAR', 
                                           vega, data_object1_id=volatility_structure, data_object1_type = 'Volatility Surface')
            elif risk_factor == 'ir_vega':
                volatility_structure, vega = self.get_vega(instr, portf)
                if volatility_structure:
                    self.write_risk_factor(writer, instr, portf, risk_subject_id, subject_type, 'IRVEGA', 'SCALAR', 
                                           vega, data_object1_id=volatility_structure, data_object1_type = 'Volatility Surface')
            elif risk_factor == 'eq_vega':
                volatility_structure, vega = self.get_vega(instr, portf)
                if volatility_structure:
                    self.write_risk_factor(writer, instr, portf, risk_subject_id, subject_type, 'EQVEGA', 'SCALAR', 
                                           vega, data_object1_id=volatility_structure, data_object1_type = 'Volatility Surface')

            elif risk_factor == 'fx_delta':
                fx_delta_per_currency = self.get_fx_delta(portf)
                for curr in fx_delta_per_currency:
                    self.write_risk_factor(writer, instr, portf, risk_subject_id, subject_type, 'FXDELTA', 'SCALAR', 
                                           fx_delta_per_currency[curr], data_object1_id=curr, data_object1_type = 'FX Rate')

            elif risk_factor == 'equity_delta':
                equity_delta = self.get_equity_delta(portf)
                self.write_risk_factor(writer, instr, portf, risk_subject_id, subject_type, 'EQDELTA', 'SCALAR', 
                                           '', data_object1_id=equity_delta, data_object1_type = 'Equity Price')

            self.deal_sheet_space.Clear()
            self.CALC_SPACE.Clear()
    
    def perform(self):
        with open(self.path, 'w') as rentd_file:
            writer = csv.DictWriter(
                rentd_file,
                self.REPORT_ENTRY._fields,
                delimiter='|',
                lineterminator = '\n'
            )
            writer.writerow(dict(list(zip(self.REPORT_ENTRY._fields, self.REPORT_ENTRY._fields))))
            
            calc_size = 0
            for contr, instr, curr, portf in self.positions:
                if calc_size > 1000:
                    self.clear_calc_space()
                    self.CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Now')
                    #CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss Use MtM Today', 'Fallback')
                    calc_size = 0
                calc_size += 1
        
                trades = self.positions[contr, instr, curr, portf]
                portf = self.get_virtual_portfolio(trades)

                risk_factor_types = self.get_risk_factor_types(instr)
                currencies = self.get_currencies(trades)
                if 'fx_delta' not in risk_factor_types and (len(currencies) > 1 or currencies[0].Name() != 'ZAR'):
                    risk_factor_types.append('fx_delta')
                self.write_risk_data(instr, portf, risk_factor_types, writer, self.get_position_id(portf), 'Position')

            for contr, instr, curr, portf in self.positions:
                for trade in self.positions[contr, instr, curr, portf]:
                    if acm_date(to_datetime(trade.TradeTime())) != acm_date(self.repday):
                        continue
                    if calc_size > 1000:
                        self.clear_calc_space()
                        self.CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Now')
                        #CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss Use MtM Today', 'Fallback')
                        calc_size = 0
                    calc_size += 1
        
                    portf = self.get_virtual_portfolio([trade])

                    risk_factor_types = self.get_risk_factor_types(instr)
                    if 'fx_delta' not in risk_factor_types and (len(currencies) > 1 or currencies[0].Name() != 'ZAR'):
                        risk_factor_types.append('fx_delta')

                    self.write_risk_data(instr, portf, risk_factor_types, writer, trade.Oid(), 'Trade')

            for c in self.fx_swap:
                if calc_size > 1000:
                    self.clear_calc_space()
                    self.CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Now')
                    #CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss Use MtM Today', 'Fallback')
                    calc_size = 0
                calc_size += 1
                trades = []
                for t in self.fx_swap[c]:
                    if acm_date(to_datetime(t.TradeTime())) != acm_date(self.repday):
                        continue
                    trades.append(t)
                if not len(trades) > 0:
                    continue
                    
                portf = self.get_virtual_portfolio(trades)
                risk_factor_types = self.get_risk_factor_types(instr)
                if 'fx_delta' not in risk_factor_types and (len(currencies) > 1 or currencies[0].Name() != 'ZAR'):
                        risk_factor_types.append('fx_delta')

                self.write_risk_data(instr, portf, risk_factor_types, writer, self.get_position_id(portf), 'Position')

            for c in self.fx_swap:
                if calc_size > 1000:
                    self.clear_calc_space()
                    self.CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Now')
                    #CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss Use MtM Today', 'Fallback')
                    calc_size = 0
                calc_size += 1

                trades = []
                for t in self.fx_swap[c]:
                    if acm_date(to_datetime(t.TradeTime())) != acm_date(self.repday):
                        continue
                    trades.append(t)
                if not len(trades) > 0:
                    continue
                portf = self.get_virtual_portfolio(trades)
                risk_factor_types = self.get_risk_factor_types(instr)
                if 'fx_delta' not in risk_factor_types and (len(currencies) > 1 or currencies[0].Name() != 'ZAR'):
                        risk_factor_types.append('fx_delta')

                self.write_risk_data(instr, portf, risk_factor_types, writer, portf.Trades().At(0).ConnectedTrade().Oid(), 'Trade')
