"""Report of trades with long dated settlement.

This reports securities and derivatives which have a long dated settlement,
which is specified by task parameters.

"""


import csv
import os

import acm
from at_ael_variables import AelVariableHandler
import FLogger


INS_TYPES_DERIV = ['BondIndex',
    'Cap',
    'CFD',
    'CLN',
    'Combination',
    'Convertible',
    'CreditDefaultSwap',
    'CreditIndex',
    'Curr',
    'CurrSwap',
    'EquityIndex',
    'EquitySwap',
    'Floor',
    'FRA',
    'Future/Forward',
    'FXOptionDatedFwd',
    'FxSwap',
    'IndexLinkedSwap',
    'Option',
    'Portfolio Swap',
    'PriceSwap',
    'Swap',
    'TotalReturnSwap',
    'VarianceSwap']

REPORT_COLUMNS_DERIVATIVE_TRADES = [
    'Trdnbr',
    'Status',
    'Trade Date',
    'TrdCurr',
    'Ctp',
    'Instrument',
    'InsType',
    'Instrument_Expiry',
    'Portfolio',
    'Acquirer',
    'Nominal',
    'ZAR_Nominal',
    'BS',
    'PV']

REPORT_COLUMNS_SECURITY_TRADES = [
    'Trdnbr',
    'Status',
    'TrdCurr',
    'Ctp',
    'Instrument',
    'InsType',
    'Instrument_Expiry',
    'Portfolio',
    'Acquirer',
    'Trade Date',
    'Value Day']

INSTYPE_SPOT_OFFSET = {
    'Deposit':0,
    'Bond':3,
    'Stock':3,
    'FRN':3,
    'SecurityLoan':0
}

STATUS_FILTER = ['Terminated', 'Simulated', 'Void', 'BO Confirmed','BO-BO Confirmed']


def make_sure_path_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_lds_data(compound_portfolio, no_of_days, no_of_months):
    """Retrieve the derivative and security long-dated statement data."""
    derivative_trades = []
    security_trades = []
    date_today = acm.Time.DateNow()
    far_date = acm.Time.DateAddDelta(date_today, 0, no_of_months, 0)

    for portfolio in compound_portfolio.AllPhysicalPortfolios():
        for trade in portfolio.Trades():
            instrument = trade.Instrument()
            if trade.Status() in STATUS_FILTER or instrument.IsExpired():
                continue

            if  instrument.InsType() not in INS_TYPES_DERIV:
                calendar = acm.FInstrument['ZAR'].Calendar()
                trade_date = acm.Time.DateFromTime(trade.TradeTime())
                offSet = no_of_days
                if instrument.InsType() in INSTYPE_SPOT_OFFSET.keys():
                    offSet = INSTYPE_SPOT_OFFSET[instrument.InsType()]                    
                forward_trade_date = calendar.AdjustBankingDays(
                        trade_date, offSet)

                value_day = trade.ValueDay()
                if value_day < date_today:
                    continue
                if acm.Time.DateDifference(value_day, forward_trade_date) > 0:
                    security_trades.append(trade)
                continue

            valid = True
            has_cashflow = False
            for leg in instrument.Legs():
                for cashflow in leg.CashFlows():
                    has_cashflow = True
                    if cashflow.PayDate() <= far_date:
                        valid = False
                        break
                if not valid:
                    break
            if valid and has_cashflow:
                derivative_trades.append(trade)
    return derivative_trades, security_trades

def write_derivatives_trades_report(report_data, file_path, csv_delimiter):
    """Write the derivatives file."""
    context = acm.GetDefaultContext()
    calc_space = acm.Calculations().CreateCalculationSpace(
            context, 'FTradeSheet')

    header_dict = dict(list(zip(
        REPORT_COLUMNS_DERIVATIVE_TRADES, REPORT_COLUMNS_DERIVATIVE_TRADES)))

    with open(file_path, 'wt') as f:

        writer = csv.DictWriter(
                f, REPORT_COLUMNS_DERIVATIVE_TRADES, delimiter=csv_delimiter)
        writer.writerow(header_dict)

        for trade in report_data:
            buy_sell = 'buy' if trade.Quantity() > 0 else 'sell'

            try:
                denominated_value = calc_space.CalculateValue(trade,
                        'Total Val End')
                value = denominated_value.Number()
            except:
                value = 'Error'

            writer.writerow({
                'Trdnbr': trade.Name(),
                'Status': trade.Status(),
                'Trade Date': str(trade.TradeTime()),
                'TrdCurr': trade.Currency().Name(),
                'Ctp': trade.Counterparty().Name(),
                'Instrument': trade.Instrument().Name(),
                'InsType': trade.Instrument().InsType(),
                'Instrument_Expiry': trade.Instrument().ExpiryDate(),
                'Portfolio': trade.Portfolio().Name(),
                'Acquirer': trade.Acquirer().Name(),
                'Nominal': str(trade.Nominal()),
                'ZAR_Nominal': str(trade.Nominal()),
                'BS': buy_sell,
                'PV': str(value)
            })


def write_security_trades_report(report_data, file_path, csv_delimiter):
    """Write the securities file."""
    header_dict = dict(list(zip(
        REPORT_COLUMNS_SECURITY_TRADES, REPORT_COLUMNS_SECURITY_TRADES)))

    with open(file_path, 'wt') as f:
        writer = csv.DictWriter(
                f, REPORT_COLUMNS_SECURITY_TRADES, delimiter=csv_delimiter)
        writer.writerow(header_dict)

        for trade in report_data:
            writer.writerow({
                'Trdnbr': trade.Name(),
                'Status': trade.Status(),
                'TrdCurr': trade.Currency().Name(),
                'Ctp': trade.Counterparty().Name(),
                'Instrument': trade.Instrument().Name(),
                'InsType': trade.Instrument().InsType(),
                'Instrument_Expiry': trade.Instrument().ExpiryDate(),
                'Portfolio': trade.Portfolio().Name(),
                'Acquirer': trade.Acquirer().Name(),
                'Trade Date': str(trade.TradeTime()),
                'Value Day': str(trade.ValueDay())
            })


def init_logging(log_level):
    """Get a logger instance."""
    logger = FLogger.FLogger('LDS Report')
    logger.Reinitialize(level=LOG_LEVEL[log_level],
                        keep=False,
                        logOnce=False,
                        logToConsole=True,
                        logToPrime=True,
                        filters=None)

    return logger

ael_gui_parameters = {'hideExtracControls' : True,
                      'windowCaption' : 'LDS Report'}

LOG_LEVEL = {'DEBUG': 2, 'INFO': 1, 'WARNING':2, 'ERROR':3}

compounds = acm.FCompoundPortfolio.Instances()

ael_variables = AelVariableHandler()
ael_variables.add('folder_path',
        default='c:/_temp',
        label='Report Path')
ael_variables.add('csv_delimiter',
        default='Tab',
        collection=['Tab', 'Semicolon', ',', '|'],
        label='CSV Delimiter')
ael_variables.add('no_of_days',
        label='No. Of Days',
        cls='int',
        default=6)
ael_variables.add('no_of_months',
        label='No. Of Months',
        cls='int',
        default=12)
ael_variables.add('compound_portfolio',
        collection=compounds,
        label='Compound Portfolio',
        cls=acm.FPhysicalPortfolio)
ael_variables.add('log_level',
        default='INFO',
        collection=LOG_LEVEL.keys,
        label='Log Level')


def ael_main(params):
    folder_path = params['folder_path']
    make_sure_path_exists(folder_path)

    log = init_logging(params['log_level']).LOG

    if params['csv_delimiter'] == 'Tab':
        params['csv_delimiter'] = '\t'
    elif params['csv_delimiter'] == 'Semicolon':
        params['csv_delimiter'] = ';'

    log('Fetching data...')
    derivatives_trades, security_trades = get_lds_data(
            params['compound_portfolio'], params['no_of_days'],
            params['no_of_months'])
    log('Successfully fetched data.')
    log('Writing reports.')

    file_path = os.path.join(folder_path, 'LDS_Derivatives_Results.tab')
    write_derivatives_trades_report(
            derivatives_trades, file_path, params['csv_delimiter'])
    log('Wrote secondary output to {0}'.format(file_path))

    file_path = os.path.join(folder_path, 'LDS_Securities_Results.tab')
    write_security_trades_report(
            security_trades, file_path, params['csv_delimiter'])
    log('Wrote secondary output to {0}'.format(file_path))

    log('Completed successfully.')


