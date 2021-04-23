import acm
import ael
from at_logging import getLogger
from at_ael_variables import AelVariableHandler
from Spread_Curve_Sorter import *
from FAFOUtils import *

LOGGER = getLogger(__name__)

ael_variables = AelVariableHandler()
ael_variables.add(
    'points_calculated',
    label='points calculated',
    mandatory = True,
    default= '"ZAR/ON","ZAR/1w","ZAR/2w","ZAR/3w","ZAR/1m","ZAR/2m"',
    multiple = True,
    tab = "Spread Calculation"
)
ael_variables.add(
    'curves_name',
    label='curves name',
    mandatory = True,
    default ="ZAR-SWAP",
    multiple = False,
    tab = "Spread Calculation"
)
ael_variables.add(
    'market_name',
    label='market name',
    mandatory = True,
    default ="SPOT",
    multiple = False,
    tab = "Spread Calculation"
)
ael_variables.add(
    'output_file',
    label='output file',
    mandatory = True,
    default ="C:\Temp",
    multiple = False,
    tab = "Spread Calculation"
)


def calculate_spread(curve_name, points_list, mkt_name):
    acm_curve = acm.FYieldCurve[curve_name]
    results = []
    if acm_curve <> None:
        LOGGER.info("Curve {} exist in FA.".format(acm_curve.Name()))
        for ins_name in points_list:
            try:
                LOGGER.info('Calculating spread for point {}.'.format(ins_name))
                ins_obj = acm.FInstrument[ins_name]
                ins_price = get_price(ins_name, mkt_name)
                period = get_period(ins_obj)
                calendar_name = get_calendarname(ins_obj)
                end_date = business_days(acm.Time.DateToday(), period, calendar_name)
                calc_rate = ael.YieldCurve[curve_name].yc_rate(ael.date_today(), end_date, "Quarterly", "Act/365", 'Par Rate') 
                spread = round((ins_price - (calc_rate*100))*100, 4)
                results.append([period, spread])
                LOGGER.info('Spread calculation for point {} was successful.'.format(ins_name))
            except Exception as e:
                LOGGER.error("Failed while trying to calculate spread for point {} due to the following error: {}".format(ins_name, e))
                break
        return results
    else:
        LOGGER.error("Curve {} does not exist in FA.".format(curve_name))

def ael_main(ael_dict):
    output_path = ael_dict['output_file']
    price_market = ael_dict['market_name']
    points = ael_dict['points_calculated']
    curve_name = ael_dict['curves_name']
    HeaderList = ['Point Name', 'Spread in basis points']
    file_name = "ZAR_BASIS_Spreads_"+str(acm.Time.DateToday())+".csv"
    output_results = []
    output_results = calculate_spread(curve_name, points, price_market)
    if len(output_results) >= 1:
        try:
            WriteCSVFile(output_path, file_name, output_results, HeaderList)
            LOGGER.info("Script ran successfully")
        except Exception as e:
            LOGGER.error("Failed due to the following error: {}".format(e))
        
    
