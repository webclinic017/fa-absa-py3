'''
MODULE
    Volcker
    
HISTORY
'''

import acm, ael, string, time
from at_time import acm_date, ael_date, to_datetime, to_date
from datetime import datetime
from math import isnan
import cProfile, pstats, StringIO
from collections import defaultdict, namedtuple
import FLogger
from at_ael_variables import AelVariableHandler
import os.path
import csv

CASH_INSTYPE = [
    'Bill',
    'Bond',
    'BuySellback',
    'Commodity',
    'ETF',
    'IndexLinkedBond',
    'SecurityLoan',
    'Stock',
    'Zero'
]

DERIV_INSTYPE = [
    'Cap',
    'CD',
    'CFD',
    'Combination',
    'CreditDefaultSwap',
    'Curr',
    'CurrSwap',
    'Deposit',    
    'EquityIndex',
    'Floor',
    'FRA',
    'FreeDefCF',
    'FRN',
    'Future/Forward',
    'IndexLinkedSwap',
    'Option',
    'Portfolio Swap',
    'PriceSwap',
    'Repo/Reverse',    
    'Swap',
    'TotalReturnSwap',
    'VarianceSwap'
]

IRD_INSTYPE = [
    'Swap',
    'FRA',
    'FRN'
]

REPORT_ENTRY = namedtuple('volcker_report_entry', [
    'TRADE_ID', 'LEG', 'POSITION_ID', 'BOOK', 'INSTRUMENT_IDENTIFIER_TYPE',
    'INSTRUMENT_IDENTIFIER', 'INSTRUMENT_DESCRIPTION', 'TRADE_DATE',
    'TRADE_TIME', 'PRODUCT_NAME', 'BUY_SELL', 'TRADE_STATUS', 'CURRENCY',
    'COUNTERPARTY_TYPE', 'COUNTERPARTY_ID', 'NOTIONAL', 'CONTRACT_SIZE',
    'NUMBER_OF_CONTRACTS', 'UNDERLYING_PRICE', 'DELTA_PERCENTAGE', 'IR01',
    'MARKET_VALUE', 'SOURCE_SYSTEM', 'OPTION_TYPE', 'STRIKE', 'COUPON',
    'UNDERLYING_SYMBOL', 'PRICE', 'MATURITY_DATE', 'CURVE', 'AGE', 
    'BCML_PRODUCT_SUB_TYPE_YN','QUANTITY','AGE_METHODOLOGY'
])
    
TWOBUSDAYSAGO = ael_date('Today').add_banking_day(ael.Calendar['ZAR Johannesburg'], -2)  

START_DATES = {
    'Inception': acm_date('Inception'), 
    'First Of Year': acm_date('FirstDayOfYear'), 
    'First Of Month' :acm_date('FirstDayOfMonth'), 
    'PrevBusDay': acm_date('PrevBusDay'), 
    'TwoBusinessDaysAgo': TWOBUSDAYSAGO.to_string(ael.DATE_ISO), 
    'TwoDaysAgo': acm_date('TwoDaysAgo'), 
    'Yesterday': acm_date('Yesterday'), 
    'Custom Date': acm_date('Today'), 
    'Now': acm_date('Today'), 
} 

END_DATES = {
    'Now': acm_date('Today'), 
    'TwoDaysAgo': acm_date('TwoDaysAgo'),
    'PrevBusDay': acm_date('PrevBusDay'),  
    'Yesterday': acm_date('Yesterday'), 
    'Custom Date': acm_date('Today'), 
}

CALC_SPACE = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FPortfolioSheet')
CALC_SPACE_TRADE = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FTradeSheet')
CALC_SPACE_COLLECTION = acm.Calculations().CreateStandardCalculationsSpaceCollection()

LOGGER = None
LOG_LEVEL = {'DEBUG': 2, 'INFO': 1, 'WARNING':3, 'ERROR':4}

ael_variables = AelVariableHandler()

ael_variables.add(
    'tradeFilter', 
    label = 'TradeFilter', 
    cls = 'string', 
    collection = acm.FTradeSelection.Select(''), 
    default = 'Volcker_Africa',
)

ael_variables.add(
    'path', 
    label = 'Path', 
    cls = 'string', 
    default = '/services/frontnt/Task/'
)

ael_variables.add(
    'fileName', 
    label = 'File Name', 
    cls = 'string', 
    default = 'Output.txt'
)

ael_variables.add(
    'currency', 
    label = 'Valuation Currency', 
    cls = 'string', 
    collection = sorted([curr.Name() for curr in acm.FCurrency.Select('')]), 
    default = 'ZAR'
)

ael_variables.add(
    'startDate', 
    label = 'Start Date', 
    cls = 'string', 
    collection = START_DATES.keys(), 
    default = 'Inception',
    mandatory = True
)

ael_variables.add(
    'startDateCustom', 
    label = 'Start Date Custom', 
    cls = 'string',  
    default = acm_date('Inception'),
    mandatory = True
)

ael_variables.add(
    'endDate', 
    label = 'End Date', 
    cls = 'string', 
    collection = START_DATES.keys(), 
    default = 'Inception',
    mandatory = True
)

ael_variables.add(
    'endDateCustom', 
    label = 'End Date Custom', 
    cls = 'string',  
    default = acm_date('Inception'),
    mandatory = True
)

ael_variables.add(
    'log_level',
    label='Log Level',
    cls = 'string',
    collection = [
        'DEBUG', 
        'INFO', 
        'WARNING', 
        'ERROR'
    ],
    default = 'INFO',
)

def trdfilterList():
    """
    Returns the list of available trade filters
    """
    TradeFilterList = []
    for tf in acm.FTradeSelection.Select(''):
        TradeFilterList.append(str(tf.Name()))
    return TradeFilterList.sort()

def get_trades_by_filter(trade_filter_name):
    '''
    returns a snapshot of trades matching a trade_filter_name
    '''
    trade_filter = acm.FTradeSelection[trade_filter_name]
    trades = trade_filter.Snapshot()
    #in case memory is a problem, use SnapshotTradeNbrs() to avoid loading all trades at once
    return trades

def _init_logging(log_directory, log_level):
    '''initialize logging'''
    global LOGGER
    LOGGER = FLogger.FLogger('Volcker_IA_Feed')
    LOGGER.Reinitialize(
        level=LOG_LEVEL[log_level], 
        keep=False, 
        logOnce=False, 
        logToConsole=False, 
        logToPrime=True, 
        #logToFileAtSpecifiedPath=os.path.join(log_directory, 
        #    'Repcube_Hedge_Report_%s.log' % acm_datetime('TODAY')
        #), 
        filters=None)

def _get_formated_value(value, default='', title=None):
    result = default
    if hasattr(value, "Number"):
        result = str("%.5f" % value.Number())
    else:
        print "{0}: {1}".format(title, value)
    return result 
 
def _fx_rate(from_currency, to_currency, date):
    """Obtains FX rate for a certain date.
    
    Parameters:
    from_currency -- str, eg. USD
    to_currency -- str, egk. ZAR
    date -- str, eg. 2012-10-10    
    """

    if (from_currency, to_currency, date) not in _fx_rate._ccy_cache.keys():
        from_curr = acm.FCurrency[from_currency]
        to_curr = acm.FCurrency[to_currency]
        _fx_rate._ccy_cache[(from_currency, to_currency, date)] = from_curr.Calculation().FXRate(
            CALC_SPACE_COLLECTION, to_curr, date).Number()
    
    return _fx_rate._ccy_cache[(from_currency, to_currency, date)]

def calculate_value(trade, column_id, cash_qty, date=acm.Time.DateToday()):
    if cash_qty != 0:
        trade.Quantity(cash_qty)
        trade.SimulateRecursive()
    
    #calc_space.SimulateValue(trade, 'Portfolio Profit Loss End Date', 'Custom Date')
    #calc_space.SimulateValue(trade, 'Portfolio Profit Loss End Date Custom', date)
    value = CALC_SPACE.CalculateValue(trade, column_id, None, False)
    if hasattr(value, 'Number'):
        value = value.Number()
        
    trade.Unsimulate()
    
    return value
    
def get_calcs(trd, cash_qty, value, repday):
    if value == 'delta_pct':
        result = calculate_value(trd, 'Portfolio Delta %', cash_qty, repday)
    elif value == 'interest_rate_01':
        result = calculate_value(trd, 'Portfolio Delta Yield', cash_qty, repday)
    else: 
        # when in doubt, calculate market value
        result = calculate_value(trd, 'Total Val End', cash_qty, repday)    

    return result

def file_data(trade, cash_qty, trade_type, repday, *rest):
    # calculated values #
    market_val = get_calcs(trade, cash_qty, 'market_val', repday)
    if (not market_val) and (not abs(market_val) >= 0):
        market_val = 0.00
    if  isnan(market_val):
        market_val = 0.00
    if trade.Instrument().InsType() in ('Bill',
    'Bond',
    'BuySellback',
    'Commodity',
    'ETF',
    'IndexLinkedBond',
    'SecurityLoan',
    'Stock',
    'Zero') and trade.Quantity() < 0:
        market_val = abs(market_val)
    
    if round(market_val, 2) == 0.00:
        data = []
    else:
        ins = trade.Instrument()
        ins_description = ins.Name()
        ins_type = ins.InsType()
        
        if ins_type == 'Option' and ins.Underlying().InsType() not in IRD_INSTYPE:
            delta_p = get_calcs(trade, cash_qty, 'delta_pct', repday)
        else:
            delta_p = 0.00
            
        if ins_type in IRD_INSTYPE:
            ir = get_calcs(trade, cash_qty, 'interest_rate_01', repday)
            #ir = 1.00
        else:
            ir = 0.00    
    
        if (not delta_p) and (not abs(delta_p) >= 0):
            delta_p = 0.00
        if isnan(delta_p):
            delta_p = 0.00
        if (not ir) and (not abs(ir) >= 0):
            ir = 0.00
        if isnan(ir):
            ir = 0.00

        if ins.Isin() != "":
            id_type = 'ISIN'
            id = ins.Isin()
        elif ins.add_info('SEDOL'):
            id_type = 'SEDOL'
            id = ins.AdditionalInfo().SEDOL()
        else:
            id_type = 'InstrumentName'
            id = ins.Isin()
            
        t_date = datetime.strftime(to_datetime(trade.TradeTime()), '%Y%m%d')
        t_time = datetime.strftime(to_datetime(trade.TradeTime()), '%H:%M:%S')
        
        buysell = ''
        if trade.Quantity() >= 0:
            buysell = 'B'
        else:
            buysell = 'S'
            
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

        
        # contract_size #
        if ins_type in ('Future/Forward', 'Option'):
            contract_size = str(ins.Underlying().ContractSize())
            contract = str(ins.ContractSize())
        else:
            contract_size = str(ins.ContractSize())
            contract = str(ins.ContractSize())
        
        if ins.Underlying():
            und_price = ins.Underlying().Calculation().MarketPrice(CALC_SPACE_COLLECTION)
        else:
            und_price = 0.0
        if isnan(und_price):
            und_price = 0.00
            
            
        source_system = 'ABCAP_FRONT_ARENA'
        option_type = ''
        #ITO
        '''
        if ins_type == 'Option':
            if ins.exercise_type:
                option_type = ins.exercise_type
        '''
        
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
        age_date = ael_date(trade.ValueDay())
        
        age = age_date.days_between(repday)

        # qty & age method #
        if trade_type == 'Cash':
            #ITO no abs on market_val
            #market_val = abs(market_val)
            ageMethod = 'C'
            qty = cash_qty
            if trade.Quantity() != cash_qty:
                nominal = ins.ContractSize() * cash_qty
            else:
                nominal = trade.Calculation().Nominal(CALC_SPACE_COLLECTION, trade.ValueDay())
        else:
            ageMethod = 'D'
            qty = round(trade.Quantity(), 4)
            nominal = CALC_SPACE_TRADE.CreateCalculation(trade, 'Regulatory Notional').Value().Number()
        if isnan(nominal):
            nominal = 0.00
        data = REPORT_ENTRY(
            TRADE_ID = str(trade.Oid()), 
            LEG = '2', 
            POSITION_ID = '', 
            BOOK = str(trade.Portfolio().Oid()), 
            INSTRUMENT_IDENTIFIER_TYPE = id_type, 
            INSTRUMENT_IDENTIFIER = id, 
            INSTRUMENT_DESCRIPTION = ins_description, 
            TRADE_DATE = t_date, 
            TRADE_TIME = t_time, 
            PRODUCT_NAME = ins_type,
            BUY_SELL = buysell, 
            TRADE_STATUS = trade.Status(), 
            CURRENCY = 'ZAR', 
            COUNTERPARTY_TYPE = cpty_type, 
            COUNTERPARTY_ID = cpty_id, 
            NOTIONAL = str(round(nominal, 2)), 
            CONTRACT_SIZE = contract_size, 
            NUMBER_OF_CONTRACTS = contract,
            UNDERLYING_PRICE = str(round(und_price, 2)), 
            DELTA_PERCENTAGE = str(round(delta_p, 2)), 
            IR01 = str(round(ir, 2)), 
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
            AGE_METHODOLOGY = ageMethod)
    
    return data

def performAscendingAgeSorting(list):
    list.sort(key=lambda k: k[5], reverse=False)
    return list

def get_data(tf_name, repday):
    cash_trades = []
    cash_trades_per_instrument = defaultdict(list)
    cash_trades_per_position = defaultdict(list)

    derivate_trades = []
    derivate_trades_per_instrument = defaultdict(list)
    derivate_trades_per_position = defaultdict(list)

    other_trades = []
    other_trades_per_instrument = defaultdict(list)
    other_trades_per_position = defaultdict(list)

    portfolios = set()
    instruments = set()
    #non_live_dates = ['0000-01-01','1970-01-01','9999-12-31']
    
    trades = get_trades_by_filter(tf_name)
    for trade in trades:
        if trade.Instrument().InsType() in CASH_INSTYPE and not trade.Instrument().IsExpiredAt(repday):
            cash_trades.append(trade)
            cash_trades_per_instrument[trade.Instrument()].append(trade)
            cash_trades_per_position[(trade.Instrument(), trade.Portfolio())].append(trade)
            portfolios.add(trade.Portfolio())
            instruments.add(trade.Instrument())
        elif trade.Instrument().InsType() in DERIV_INSTYPE and not trade.Instrument().IsExpiredAt(repday):
            derivate_trades.append(trade)
            derivate_trades_per_instrument[trade.Instrument()].append(trade)
            derivate_trades_per_position[(trade.Instrument(), trade.Portfolio())].append(trade)
        else:
            other_trades.append(trade)
            other_trades_per_instrument[trade.Instrument()].append(trade)
            other_trades_per_position[(trade.Instrument(), trade.Portfolio())].append(trade)
        
    LOGGER.DLOG([p.Name() for p in portfolios])
    LOGGER.DLOG([i.Name() for i in instruments])
    LOGGER.DLOG([t.Oid() for t in cash_trades])
    bookInsFIFO = []
    cashTrades = [] #noFIFO
    
    #FIFO Computation

    fifo = defaultdict(list)

    for instrument, portfolio in cash_trades_per_position:
        position_quantity = sum(t.Quantity() for t in cash_trades_per_position[instrument, portfolio])
        if position_quantity == 0:
            continue
            
        all_trades = sorted(cash_trades_per_position[instrument, portfolio], key=lambda t: t.ValueDay(), reverse = True)
        
        curr_position = 0

        for trade in all_trades:
            if ((trade.Quantity() >= 0 and position_quantity < 0) or
                (trade.Quantity() < 0 and position_quantity >= 0)):
                continue
            
            curr_position += trade.Quantity()
            if abs(curr_position) > abs(position_quantity):
                curr_position -= trade.Quantity()
                if position_quantity == curr_position:
                    break
                    
                fifo[instrument, portfolio].append({
                    'trade': trade, 
                    'value_day': trade.ValueDay(), 
                    'quantity': position_quantity - curr_position,
                    'age': ael_date(trade.ValueDay()).days_between(repday)})
                break;
            else:
                fifo[instrument, portfolio].append({
                    'trade': trade, 
                    'value_day': trade.ValueDay(), 
                    'quantity': trade.Quantity(),
                    'age': ael_date(trade.ValueDay()).days_between(repday)})
            
    result = {}
    result['cashFifo'] = fifo
    result['cash'] = cashTrades
    result['deriv'] = derivate_trades
    result['other_trades'] = other_trades

    '''
    print '\n\n\n', 'cashfifo', result['cashFifo']
    print '\n\n\n', 'cash', result['cash']
    print '\n\n\n', 'deriv', result['deriv']
    '''
    return result

def clear_calc_space():
    CALC_SPACE.RemoveGlobalSimulation('Portfolio Profit Loss End Date')
    CALC_SPACE.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')
    
    CALC_SPACE.Clear()
    for builder in acm.FCache.Select01('.StringKey = "evaluator builders"', "").Contents():
        builder.Reset()
    acm.Memory().GcWorldStoppedCollect()

def ael_main(ael_dict):
    #enable profiling
    pr = cProfile.Profile()
    pr.enable()
    _init_logging('', ael_dict['log_level'])
    
    filePath = os.path.join(ael_dict['path'], datetime.strftime(to_date(END_DATES[ael_dict['endDate']]), '%Y%m%d'))
    if not os.path.exists(filePath):
        os.makedirs(filePath)
    filePath = os.path.join(filePath, ael_dict['fileName'])
    
    with open(filePath, 'w') as f:
        # _fx_rate._ccy_cache = {}
        writer = csv.DictWriter(
            f,
            REPORT_ENTRY._fields,
            delimiter='|',
            lineterminator = '\n'
        )
        writer.writerow(dict(list(zip(REPORT_ENTRY._fields, REPORT_ENTRY._fields))))
    
        if ael_dict['startDate'] == 'Custom Date':
            startDate = ael_dict['startDateCustom']
        else:
            startDate = str(START_DATES[ael_dict['startDate']])
    
        if ael_dict['endDate'] == 'Custom Date':
            endDate = ael_dict['enddateCustom']
        else:
            endDate = str(END_DATES[ael_dict['endDate']])
    
    
        LOGGER.DLOG('Start timestamp: %s' % time.ctime())
        
        fullTradeData = {}
        repday = ael.date_from_string(endDate)  #ael.date_today()
        
        CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
        CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', repday)
        
        tfname = ael_dict['tradeFilter']
        
        fullTradeData = get_data(tfname, repday)
        derivTradeList = fullTradeData['deriv']
        cashTradeList = fullTradeData['cashFifo']
        other_trades = fullTradeData['other_trades']
        
        calc_size = 0
        
        for instrument, portfolio in cashTradeList:
            for t in cashTradeList[instrument, portfolio]:
                if calc_size > 1000:
                    clear_calc_space()
                    CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
                    CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', repday)
                    calc_size = 0
                calc_size += 1
                
                line = file_data(t['trade'], t['quantity'], 'Cash', repday)
                if type(line) == REPORT_ENTRY:
                    writer.writerow(line._asdict())
            
        for t in derivTradeList:
            #print t.Oid()
            if calc_size > 1000:
                clear_calc_space()
                CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
                CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', repday)
                calc_size = 0
            calc_size += 1
            
            line = file_data(t, 0, 'Deriv', repday)
            if type(line) == REPORT_ENTRY:
                writer.writerow(line._asdict())

        for t in other_trades:
            #print t.Oid()
            if calc_size > 1000:
                clear_calc_space()
                CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
                CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', repday)
                calc_size = 0
            calc_size += 1
            
            line = file_data(t, 0, 'Deriv', repday)
            if type(line) == REPORT_ENTRY:
                writer.writerow(line._asdict())
    
    LOGGER.LOG('Wrote secondary output to: %s' % filePath)
    LOGGER.LOG('Completed successfully')
    LOGGER.DLOG('End timestamp %s' % time.ctime())
    
    pr.disable()
    s = StringIO.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    #LOGGER.DLOG(s.getvalue())
