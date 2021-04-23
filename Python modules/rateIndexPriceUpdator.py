import acm
from at_price import update_price
from at_ael_variables import AelVariableHandler
from at_logging import getLogger

LOGGER = getLogger(__name__)

ael_variables = AelVariableHandler()

ael_variables.add(
    'market',
    label='Market',
    mandatory = True,
    default = 'SPOT',
    tab = 'Script Inputs'
)

ael_variables.add(
    'base_index',
    label='Base index',
    mandatory = True,
    default = 'ZAR-PRIME',
    tab = 'Script Inputs'
)


ael_variables.add(
    'period',
    label='Number of days',
    mandatory = True,
    default = 60,
    tab = 'Script Inputs'
)

ael_variables.add(
    'spread',
    label='Spread',
    mandatory = True,
    default = 'Zar Prime Rolling 60d Complex',
    tab = 'Script Inputs'
)

ael_variables.add(
    'underlying_index',
    label='Underlying Index',
    mandatory = True,
    default = 'Zar Prime Rolling 60D',
    tab = 'Script Inputs'
)

def get_settle_rate(count, base_index, market):
    query = []
    TODAY = acm.Time.DateToday()
    calendar_name = 'ZAR Johannesburg'
    calendar = acm.FCalendar[calendar_name]
    period = str(-count)+"d"
    business_date  = acm.Time.DateAdjustPeriod(TODAY, period, calendar, 'Mod. Preceding')
    if count == 0:
        prices = acm.FInstrument[base_index].Prices()
        query = [price for price in prices if price.Market().Name() == market and price.Day() == business_date]
    else:
        prices = acm.FInstrument[base_index].HistoricalPrices()
        query = [price for price in prices if price.Market().Name() == market and price.Day() == business_date]
    if query[0].Settle():
        return query[0].Settle()
    else:
        LOGGER.error("Price not found for date %s and market %s " %(business_date, market))

def calculate_average(input_list):
    average = sum(input_list) / len(input_list)
    return average
        
def update_index_price(spread, average_prime, underlying_index):
    float_spread = float(spread.Text())
    prime_rolling = average_prime - float_spread
    rounded_prime_rolling = round(prime_rolling, 3)
    rate_index = acm.FRateIndex[str(underlying_index)]
    LOGGER.info(rate_index.Name())
    price_object = [pr for pr in rate_index.Prices() if pr.Market().Name() == "SPOT"]
    update_price(price_object[0], acm.FCurrency['ZAR'], rounded_prime_rolling)
    LOGGER.info('The %s index has been updated to: %f' %(underlying_index, rounded_prime_rolling))

def get_average_base_index_rate(period, base_index, market):
    prime_list = []
    num = int(period)
    average_prime = 0
    for day in range(0, num):
        settle_rate = get_settle_rate(day, base_index, market)
        prime_list.append(settle_rate)
    average_prime = calculate_average(prime_list)

    LOGGER.info('The average prime rate for the past %s days is: %f' %(period, average_prime)) 
    return average_prime

def ael_main(ael_dict):
    base_index = ael_dict["base_index"]
    market = ael_dict["market"]
    period = ael_dict["period"]
    spread_index_name = ael_dict["spread"]
    spread_index_complex_name = ael_dict["underlying_index"]
    spread = acm.FCustomTextObject[spread_index_name]
    spread_complex = acm.FCustomTextObject[spread_index_complex_name]
    try:
        average_prime = get_average_base_index_rate(period, base_index, market)
        LOGGER.info("Average rate calculation for %s  completed with no erros." %(base_index))
        if spread == None:
            LOGGER.error('Could not update the price. There is no spread for the %s , please update it' %(spread_index_name))
        else:
            update_index_price(spread, average_prime, spread_index_name)
            
        if spread_complex == None:
            LOGGER.error('Could not update the price. There is no spread for the %s, please update it'%(spread_index_complex_name))
        else:
            update_index_price(spread_complex, average_prime, spread_index_complex_name)
        LOGGER.info("Task completed successfully")
    except Exception as e:
        LOGGER.error("Task completed with errors")
        LOGGER.info(e)
