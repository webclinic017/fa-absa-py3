'''
MODULE
    Volcker
    
HISTORY
'''

import acm, ael, string, time
from datetime import datetime
from at_time import acm_date, ael_date, to_datetime, to_date
from datetime import datetime

import cProfile, pstats, StringIO
import FLogger
from at_ael_variables import AelVariableHandler
from collections import defaultdict, namedtuple
import os.path

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

EXCHANGE_TRADED = [
    'JSE', 
    'SAFEX', 
    'JSE SECURITIES EXCHANGE SOUTH AFRICA', 
    'BESA'
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


#Underlying instype lists
IRD_INSTYPE = [
    'FRA',
    'FRN',
    'IndexLinkedSwap',
    'Swap'
]


EQ_INSTYPE = [
    'CFD',
    'EquityIndex',
    'ETF',
    'Future/Forward',
    'SecurityLoan',
    'Stock'    
]


CO_INSTYPE = [
    'Commodity'    
]


FX_INSTYPE = [
    'Curr',
    'CurrSwap'
]    
    
TWOBUSDAYSAGO = ael_date('Today').add_banking_day(ael.Calendar['ZAR Johannesburg'], -2)  

START_DATES = {
    'Inception': acm_date('Inception'), 
    'First Of Year': acm_date('FirstDayOfYear'), 
    'First Of Month': acm_date('FirstDayOfMonth'), 
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

from volcker_perform import Radial_Trade_Report, Radial_Position_Report, Radial_RENTD_Report

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
    'motif_file_name', 
    label = 'Motif File Name', 
    cls = 'string', 
    default = '',
    mandatory = False
)


ael_variables.add(
    'radial_trade_file_name', 
    label = 'Radial Trade File Name', 
    cls = 'string', 
    default = 'Output_Trade_Radial.txt',
    mandatory = False
)

ael_variables.add(
    'radial_position_file_name', 
    label = 'Radial Position File Name', 
    cls = 'string', 
    default = 'Output_Position_Radial.txt',
    mandatory = False
)

ael_variables.add(
    'rentd_file_name', 
    label = 'RENTD File Name', 
    cls = 'string', 
    default = 'Output_RENTD.txt',
    mandatory = False
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
    collection = END_DATES.keys(), 
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
    LOGGER = FLogger.FLogger('CRT Feed')
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

def performAscendingAgeSorting(list):
    list.sort(key=lambda k: k[5], reverse=False)
    return list

def performFIFOComputation(tradeList):
    bookAggregate = 0
    for singleTrade in tradeList:
        bookAggregate = bookAggregate + singleTrade[4]

    bookAggregate = round(bookAggregate, 2)    
    if bookAggregate == 0:
        return []
    elif bookAggregate > 0:
        bookDirection = 'B'
    else:
        bookDirection = 'S'
    LOGGER.DLOG('Book aggregate value: %s' % bookAggregate)

    bookDirList = []
    for singleTrade in tradeList:
        if singleTrade[3] == bookDirection:
            bookDirList.append(singleTrade)
            
    sortedTradeList = performAscendingAgeSorting(bookDirList)

    fifoComputationList = []
    absoluteBookAggregate = abs(bookAggregate)
    difference = absoluteBookAggregate
    total = 0
    
    for singleTrade in sortedTradeList:
        valueFromSingleTrade = singleTrade[4]
        absoluteValue = abs(valueFromSingleTrade)
        if (total+absoluteValue) <= absoluteBookAggregate:
            fifoComputationList.append(singleTrade)
            total = total + absoluteValue
        else:
            difference = absoluteBookAggregate - total
            total = total + difference
            if bookDirection == 'S':
                difference = difference * -1
            singleTrade[4] = round(difference, 2)
            fifoComputationList.append(singleTrade)
            #print 'EQUAL', total, absoluteBookAggregate
            break
    
    return fifoComputationList

def get_data(tf_name, repday):
    trades_per_position = defaultdict(list)
    
    cash_trades = []
    cash_trades_per_instrument = defaultdict(list)
    cash_trades_per_position = defaultdict(list)
    cash_trades_per_position_full = defaultdict(list)
    trades_per_portfolio = defaultdict(list)

    derivate_trades = []
    derivate_trades_per_instrument = defaultdict(list)
    derivate_trades_per_position = defaultdict(list)

    other_trades = []
    other_trades_per_instrument = defaultdict(list)
    other_trades_per_position = defaultdict(list)
    fx_swaps_per_contract = defaultdict(list)
    
    portfolios = set()
    instruments = set()
    #non_live_dates = ['0000-01-01','1970-01-01','9999-12-31']
    
    trades = get_trades_by_filter(tf_name)
    for trade in trades:
        #if (trade.Instrument().InsType() == 'Curr' and not trade.IsFxSwap()):
        #    continue
            
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
            trades_per_position[(0, trade.Instrument(), trade.Currency(), trade.Portfolio())].append(trade)
        elif not trade.IsFxSwap() and (trade.Counterparty().Id2() in EXCHANGE_TRADED or id_type != 'InstrumentName' or instrument.InsType()) and (not instrument.Otc() or instrument.InsType() in ('Curr')):
            trades_per_position[(0, trade.Instrument(), trade.Currency(), trade.Portfolio())].append(trade)
        elif not trade.IsFxSwap():
            trades_per_position[(trade.Oid(), trade.Instrument(), trade.Currency(), trade.Portfolio())].append(trade)
        
        trades_per_portfolio[trade.Portfolio().Name()].append(trade)
        
        if trade.Instrument().InsType() in CASH_INSTYPE and not trade.Instrument().IsExpiredAt(repday) and not trade.IsFxSwap():
            cash_trades.append(trade)
            cash_trades_per_instrument[trade.Instrument()].append(trade)
            cash_trades_per_position[(trade.Instrument(), trade.Portfolio())].append(trade)
            cash_trades_per_position_full[(trade.Instrument(), trade.Portfolio())].append(trade)
            portfolios.add(trade.Portfolio())
            instruments.add(trade.Instrument())
        elif trade.Instrument().InsType() in DERIV_INSTYPE and not trade.Instrument().IsExpiredAt(repday) and not trade.IsFxSwap():
            derivate_trades.append(trade)
            derivate_trades_per_instrument[trade.Instrument()].append(trade)
            derivate_trades_per_position[(trade.Instrument(), trade.Portfolio())].append(trade)
        elif trade.IsFxSwap():
            fx_swaps_per_contract[trade.ConnectedTrade()].append(trade)
        else:
            other_trades.append(trade)
            other_trades_per_instrument[trade.Instrument()].append(trade)
            other_trades_per_position[(trade.Instrument(), trade.Portfolio())].append(trade)
        
    LOGGER.DLOG([p.Name() for p in portfolios])
    LOGGER.DLOG([i.Name() for i in instruments])
    LOGGER.DLOG([t.Oid() for t in cash_trades])
    bookInsFIFO = []
    cashTrades = [] #noFIFO
    
    for portfolio in portfolios:
        #live positions in cash trades
        fifo = []
        #LOGGER.DLOG('get_data processing portfolio %s' % portfolio.Name())
        for instrument in instruments:
            book_ins_trades = []
            #LOGGER.DLOG('\tget_data processing instrument %s' % instrument.Name())
            import copy
            #trades = cash_trades_per_position[(instrument, portfolio)]
            trades = copy.copy(cash_trades_per_position[(instrument, portfolio)])
            for trade in trades:
                #print 'trade ', trade.Name()
                LOGGER.DLOG('get_data processing portfolio %s, instrument %s,  trade %s' % (
                    portfolio.Name(), instrument.Name(), trade.Name()))
                if trade.Quantity() >= 0:
                    buysell = 'B'
                else:
                    buysell = 'S'  
                qty = round(trade.Quantity(), 4)
                age_date = ael_date(trade.ExecutionDate())
                age = age_date.days_between(repday)
                book_ins_trades.append([trade.Oid(), portfolio.Name(), instrument.Name(), buysell, qty, age])
                cashTrades.append([trade.Oid(), portfolio.Name(), instrument.Name(), buysell, qty, age])

            LOGGER.DLOG('FIFO on %s %s %s' % (portfolio.Name(), instrument.Name(), book_ins_trades))
            fifo = performFIFOComputation(book_ins_trades)
            
            LOGGER.DLOG('FIFO LIST %s' % fifo)
            bookInsFIFO = bookInsFIFO + fifo

            
    result = {}
    result['cashFifo'] = bookInsFIFO
    result['cash'] = cashTrades
    result['deriv'] = derivate_trades
    result['cash_trades_per_position'] = cash_trades_per_position_full
    result['derivate_trades_per_position'] = derivate_trades_per_position
    result['other_trades_per_position'] = other_trades_per_position
    result['trades_per_position'] = trades_per_position
    result['trades_per_portfolio'] = trades_per_portfolio
    result['fx_swaps_per_contract'] = fx_swaps_per_contract
    #for i, p in result['cash_trades_per_position']:
    #    print i.Name(), p.Name(), [e.Oid() for e in cash_trades_per_position[i,p]]
    #print 'DERIVATIVES'
    #for i, p in result['derivate_trades_per_position']:
    #    print i.Name(), p.Name(), [e.Oid() for e in derivate_trades_per_position[i,p]]

    '''
    print '\n\n\n', 'cashfifo', result['cashFifo']
    print '\n\n\n', 'cash', result['cash']
    print '\n\n\n', 'deriv', result['deriv']
    '''
    return result

def ael_main(ael_dict):
    #enable profiling
    pr = cProfile.Profile()
    pr.enable()
    
    #prepare logging
    _init_logging('', ael_dict['log_level'])
    LOGGER.DLOG('Start timestamp: %s' % time.ctime())
    
    radial_trade_report = Radial_Trade_Report(ael_dict)
    radial_position_report = Radial_Position_Report(ael_dict)
    radial_rentd_report = Radial_RENTD_Report(ael_dict)
    
    repday = radial_trade_report.repday
    
    full_trade_datafull_trade_data = {} 
    tfname = ael_dict['tradeFilter']
    
    #load and orginize data
    full_trade_data = get_data(tfname, repday)
    
    radial_trade_report.load_data(full_trade_data)
    radial_position_report.load_data(full_trade_data)
    radial_rentd_report.load_data(full_trade_data)
    
    if ael_dict['radial_trade_file_name']:
        radial_trade_report.perform()
    if ael_dict['radial_position_file_name']:
        radial_position_report.perform()
    if ael_dict['rentd_file_name']:
        radial_rentd_report.perform()
    
    LOGGER.LOG('Wrote radial trade output to: %s' % radial_trade_report.path)
    LOGGER.LOG('Wrote radial position output to: %s' % radial_position_report.path)    
    LOGGER.LOG('Wrote rentd output to: %s' % radial_rentd_report.path)
    #LOGGER.LOG('Wrote secondary output to: %s' %motif_filePath)
    #LOGGER.LOG('Wrote secondary output to: %s' %radial_trade_filePath)
    #LOGGER.LOG('Wrote secondary output to: %s' %radial_pos_filePath)
    LOGGER.LOG('Completed successfully')
    LOGGER.DLOG('End timestamp %s' % time.ctime())
    
    performance_file_path = os.path.join(ael_dict['path'], datetime.strftime(to_date(END_DATES[ael_dict['endDate']]), '%Y%m%d'), '%s.perf'%ael_dict['tradeFilter'])
    with open(performance_file_path, 'w') as performance_file:
        pr.disable()
        s = StringIO.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=performance_file).sort_stats(sortby)
        ps.print_stats()
        #LOGGER.DLOG(s.getvalue())
