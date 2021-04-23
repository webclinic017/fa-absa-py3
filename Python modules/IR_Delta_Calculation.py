import acm
import csv
import ael
from at_ael_variables import AelVariableHandler
CONTEXT = acm.GetDefaultContext()
CS_TS = acm.Calculations().CreateCalculationSpace(CONTEXT,  'FTradeSheet')
CS_TS.SimulateGlobalValue('Position Currency Choice',  'Fixed Curr')
CS_TS.SimulateGlobalValue('Fixed Currency',  'ZAR')
CS_TS.SimulateGlobalValue('Aggregate Currency Choice',  'Fixed Curr')
ael_variables = AelVariableHandler()
ael_variables.add(
    'trade_filter', 
    label='Trade Filter Name', 
    cls='FTradeSelection', 
    default='CRT_OIS_HEDGE'
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
    
def get_tenor(instrument):
    """
    Returns teners
    """
    daysOffset = instrument.SpotBankingDaysOffset()
    unit = instrument.ExpiryPeriod_unit()
    count = instrument.ExpiryPeriod_count()
    benchmark_type = instrument.InsType()
    if unit == 'Days':
        count = count + daysOffset
        if count < 30:
            return str(count) + 'D'
        elif count <= 360:
            return str(int(round(count/30))) + 'M'
        else:
            return str(int(round(count/365))) + 'Y'
    elif unit == 'Weeks':
        return str(count)+'W'
    elif unit == 'Months':
        return str(count)+'M'
    else:
        return str(count)+'Y'

def get_start_date(instrument):
    benchmark_type = instrument.InsType()
    if benchmark_type == 'FRA':
        start_date = instrument.StartDate()
        return start_date
    else:
        today = ael.date_today()
        return today

def mapped_spread_curves(calculation_note):
    '''get name of mapped price curve'''
    sheet_type = 'FTradeSheet'
    calc_space = get_calculation_space(sheet_type)
    benchmark_curve = 'AllYieldCurvesIncludingInflationInTheoreticalValue'
    top_node = calc_space.InsertItem(calculation_note)
    calc_space.Refresh()
    base_curve = calc_space.CreateCalculation(top_node,  benchmark_curve)
    curve_list = []
    for curve in base_curve.Value():
        curve_list.append(curve.Name())
    return curve_list

def mapped_benchmark_curve(calculation_note):
    '''get name of mapped price curve'''
    sheet_type = 'FTradeSheet'
    calc_space = get_calculation_space(sheet_type)
    benchmark_curve = 'BenchmarkCurvesInTheoreticalValue'
    curve_list = []
    top_node = calc_space.InsertItem(calculation_note)
    calc_space.Refresh()
    base_curve = calc_space.CreateCalculation(top_node,  benchmark_curve)
    for curve in base_curve.Value():
        curve_list.append(curve.Name())
    return curve_list

def curve_combination(calculation_note):
    """"
    combines all the curves 
    """
    mapped_spread_curves_list = mapped_spread_curves(calculation_note)
    mapped_benchmark_curve_list = mapped_benchmark_curve(calculation_note)
    all_curves = mapped_spread_curves_list + mapped_benchmark_curve_list
    full_curve_list = list(dict.fromkeys(all_curves))
    return full_curve_list
    
def calculate_delta(calculation_note, benchmark_name):
    """
        calculate delta for non attribute spread curve
    """
    column_id = 'Benchmark Delta Instruments'
    column_config = acm.Sheet.Column().ConfigurationFromVector(benchmark_name)
    top_node = CS_TS.InsertItem(calculation_note)
    calc = CS_TS.CreateCalculation(top_node,  column_id,  column_config)
    value_number = calc.Value().Number()
    return value_number

def Attributes_spread_delta(curve, bump, calculation_note):
    """
        delta for attributes spread curve
    """
    column_id = 'Portfolio Theoretical Value'
    sheet_type = 'FPortfolioSheet'
    calcSpace = CALC_SPACE = get_calculation_space(sheet_type)
    bucket_delta = {}
    node = calcSpace.InsertItem(calculation_note)         
    calculation = calcSpace.CreateCalculation(node,  column_id)
    PV0 = calculation.Value().Number()
    yield_curve_clone =  curve.Clone()
    for point in curve.Attributes().First().Spreads():   
       point.Spread(point.Spread() + bump)
       curve.RegisterInStorage()
       calculation = calcSpace.CreateCalculation(node,  column_id)
       PV1 = calculation.Value().Number()
       bucket_delta[point.Point().Name()] = PV1 - PV0
       point.Spread(point.Spread() - bump)
       curve.RegisterInStorage()
    return bucket_delta

def get_trade_portfolio(trade_filter):
    """
        returns all portfolio
    """
    trade_portfolio = []
    trade_list = trade_filter.Trades()
    for trd in trade_list:
        port = trd.Portfolio().Name()
        trade_portfolio.append(port)
    unique_port_list = list(dict.fromkeys(trade_portfolio))
    return unique_port_list 

def WriteCSVFile(outputFileLocation, resultsList, HeaderList):
    """
    Create a file to store all results
    """
    with open(outputFileLocation,  'wb') as reconBreaksFile:
        reconWriter = csv.writer(reconBreaksFile,  quoting=csv.QUOTE_ALL)
        reconWriter.writerow(HeaderList)
        for itemInList in resultsList:
            reconWriter.writerow(itemInList)

def ael_main(ael_dict):
    final_results = []
    today = ael.date_today()
    trade_filter_note = ael_dict['trade_filter']  
    outputFileLocation = ael_dict['output_file'] 
    portfolio_list = get_trade_portfolio(trade_filter_note)
    bump = 0.0001
    for portfolio in portfolio_list:
        portfolio = acm.FPhysicalPortfolio[portfolio]
        full_curve_list = curve_combination(portfolio)
        for curve_name in full_curve_list:
            curve = acm.FYieldCurve[curve_name]
            curve_benchmarks  = curve.Benchmarks()
            curve_type = curve.Type()
            curve_currency = curve.Currency().Name()
            if curve_type != 'Attribute Spread':
                for benchmark_name in curve_benchmarks:
                    instrument = benchmark_name.Instrument()
                    benchmark_type = instrument.InsType()
                    tenor = get_tenor(instrument)
                    start_date = get_start_date(instrument)
                    bm_delta = calculate_delta(portfolio, instrument)
                    final_results.append([portfolio.Name(), curve_name, instrument.Name(), bm_delta, benchmark_type, curve_currency, tenor, start_date, curve_type])
    for portfolio in portfolio_list:
        portfolio = acm.FPhysicalPortfolio[portfolio]
        full_curve_list = curve_combination(portfolio)
        for curve_name in full_curve_list:
            curve = acm.FYieldCurve[curve_name]
            curve_benchmarks  = curve.Benchmarks()
            curve_currency = curve.Currency().Name()
            curve_type = curve.Type()
            if curve_type == 'Attribute Spread':
                bm_delta_dict = Attributes_spread_delta(curve, bump, portfolio)
                for bucket in list(bm_delta_dict.keys()):
                    bm_delta = bm_delta_dict[bucket]
                    final_results.append([portfolio.Name(), curve_name, bucket, bm_delta, 'None', curve_currency, bucket, today, curve_type])
    
    HeaderList = ['Portfolio', 'Curve', 'Benchmark', 'Delta', 'InsType', 'Currency', 'Tener', 'ins_date', 'Type']
    WriteCSVFile(outputFileLocation, final_results, HeaderList)
