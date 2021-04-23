import acm
import csv
from at_logging import getLogger
from at_ael_variables import AelVariableHandler
LOGGER = getLogger(__name__)
ael_variables = AelVariableHandler()
ael_variables.add(
    'trade_filter',
    label='Trade Filter Name',
    cls='FTradeSelection',
    default='DCRM_HEDGES'
)

ael_variables.add(
    'output_file',
    label='Output File',
    default='/services/frontnt/Task/CRT_OIS_HEDGE.csv'
)

def get_calculation_space(sheet_type):
    context = acm.GetDefaultContext()
    calc_space = acm.Calculations().CreateCalculationSpace(context,  sheet_type)
    return calc_space
    
def get_fx_swap_delta(fx_swap):
    '''return the fx delta of an FX Swap. fx_swap is an FAdhocportfolio containing both legs of an fx swap.'''
    sheet_type = 'FPortfolioSheet'
    calc_space = get_calculation_space(sheet_type)
    currencies = get_currencies(fx_swap.Trades())
    values = {}
    try:
        for currency in currencies:
            vector = acm.FArray()
            param = acm.FNamedParameters()
            param.AddParameter('currency', currency)
            vector.Add(param)
            config = acm.Sheet.Column().ConfigurationFromVector(vector)
            calc = calc_space.CreateCalculation(fx_swap, 'Portfolio FX Tpl Delta Cash', config)
            values[currency.Name()] = calc.Value().Number()
    except Exception as exc:
        LOGGER.exception("This is composite curve: %s", exc)
    return values

def get_trade_portfolio(trade_filter):
    """
        returns all curve portfolio
    """
    trade_portfolio = []
    trade_list = trade_filter.Trades()
    for trd in trade_list:
        port = trd.Portfolio().Name()
        trade_portfolio.append(port)
    unique_port_list = list(dict.fromkeys(trade_portfolio))
    return unique_port_list  

def get_currencies(trades):
    '''Return all currencies associated with a set of trades. trades can be a collection of a single trade for trade level evaluations.
       Returns a set of FCurrency objects'''
    moneyFlowAndTradesDiscountingUnits = acm.GetFunction('moneyFlowAndTradesDiscountingUnits', 3)
    currenciesFromInstrumentAndTradesDiscountingUnits = acm.GetFunction('currenciesFromInstrumentAndTradesDiscountingUnits', 1)
    discounting_units = moneyFlowAndTradesDiscountingUnits(trades, acm.Time().DateToday(), 381)
    currencies = currenciesFromInstrumentAndTradesDiscountingUnits(discounting_units)
    return currencies

def WriteCSVFile(outputFileLocation, resultsList, HeaderList):
    """
    Create a file to store all results
    """
    with open(outputFileLocation, 'wb') as reconBreaksFile:
        reconWriter = csv.writer(reconBreaksFile, quoting=csv.QUOTE_ALL)
        reconWriter.writerow(HeaderList)
        for itemInList in resultsList:
            reconWriter.writerow(itemInList)
            
def ael_main(ael_dict):	
    trade_filter_note = ael_dict['trade_filter']  
    outputFileLocation = ael_dict['output_file']
    resultsList = []
    headerList = ['Portfolio', 'Currency', 'FX TPL Delta Cash']
    portfolios_list = get_trade_portfolio(trade_filter_note)
    for portfolio in portfolios_list:
        physical_portfolio = acm.FPhysicalPortfolio[portfolio]
        
        FX_Delta = get_fx_swap_delta(physical_portfolio)
        for fx_d in FX_Delta:
            resultsList.append([portfolio, fx_d, FX_Delta[fx_d]])
    WriteCSVFile(outputFileLocation, resultsList, headerList)

