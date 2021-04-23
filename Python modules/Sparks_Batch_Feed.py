'''-----------------------------------------------------------------------------
TASK                    :  Spark Code Optimization
PURPOSE                 :  To improve performance and memory usage of the process
DEPATMENT AND DESK      :  PCG/Ops
REQUESTER               :  Richard Gwilt\Linda Breytenbach
DEVELOPER               :  Paseka Motsoeneng
CR NUMBER               :  ABITFA-4028
--------------------------------------------------------------------------------
HISTORY
================================================================================
Date        Change no      Developer               Description
--------------------------------------------------------------------------------
??????????  ??????????                             Initial Implementation
2018-07-19  CHG1000679237  Libor Svoboda           Fix the Front - Sparks
'''
import datetime
import acm
import ael
from Sparks_Util import SparksUtil
from Sparks_Config import SparksConfig
from at_logging import getLogger


LOGGER = getLogger(__name__)

CALENDAR = acm.FCalendar['ZAR Johannesburg']
TODAY = acm.Time().DateToday()
PREVBUSDAY = CALENDAR.AdjustBankingDays(TODAY, -1)
NEXTBUSDAY = CALENDAR.AdjustBankingDays(TODAY, 1)


def convertListToString(list):
    list_to_string = str(list)
    return list_to_string[list_to_string.index('[')+1:list_to_string.index(']')]


def getRecordsFromQuery(query_name, parameter_list): 
    records = []
    LOGGER.info('Searching for query: %s' % query_name)
    query = acm.FSQL[query_name]
    
    if parameter_list:
        portfolios = parameter_list[1].replace("', '", "',\n'")
        query_object = query.Text().format(parameter_list[0], portfolios)
    else:
        query_object = query.Text()
        
    LOGGER.info('Running query: %s' % query_object)
    start_time = datetime.datetime.now()
    LOGGER.info('Query start time: %s' % start_time)
    result_set = ael.asql(query_object)
    end_time = datetime.datetime.now()
    LOGGER.info('Query end time: %s' % end_time)
    time_taken = end_time - start_time
    LOGGER.info('Query total time: %s' % time_taken)
    for tuple in result_set[1][0]:
        records.append(tuple[0])
    return records
    

def slicePortfoliosInHalf(parameter, active_portfolios_list): #Portfolio split
    if parameter['Type'] == 'EVEN':
        new_active_portfolios_list = active_portfolios_list[::2] 
    elif parameter['Type'] == 'ODD':
        new_active_portfolios_list = active_portfolios_list[1::2] 
    else:
        new_active_portfolios_list = []
    return new_active_portfolios_list



"""
 - Addition of a new key/value pair (Type), in the two new Sparks_Batch_Feed_SERVER tasks.
 - The batch process will now run using two ATS's - this improves performance.
 - One ATS will take one half of the portfolios and the other will take the remaining half.
 - The value of the 'Type' key (ODD/EVEN) will be used to divide the processing of the batch between the two ATS's.
"""
 
ael_variables = [
['Date', 'Date', 'string', ['TODAY', 'PREVBUSDAY', 'NEXTBUSDAY'], 'TODAY', 1, 0, 'Date to run feed against', None, 1],
['Type', 'Type', 'string', ['ODD', 'EVEN'], 'ODD', 1, 0, 'Used to divide the portfolios into two', None, 1]
]


def ael_main(parameter):
    try:
        if parameter['Date'].upper() == 'TODAY':
            runDate = TODAY
        elif parameter['Date'].upper() == 'PREVBUSDAY':
            runDate = PREVBUSDAY 
        elif parameter['Date'].upper() == 'NEXTBUSDAY':
            runDate = NEXTBUSDAY
        else:
            runDate = ael.date(parameter['Date'])
            runDate = parameter['Date']            
    except Exception as exc:
        LOGGER.exception('Error parsing date input: %s' % str(exc))
        raise

    sparks_util = SparksUtil(runDate)
    config = SparksConfig('Send')
    
    active_portfolios_list = getRecordsFromQuery(config.active_portfolios_query, None)
    
    #Portfolio split
    new_active_portfolios_list = slicePortfoliosInHalf(parameter, active_portfolios_list) 
                
    INSTRUMENT_EXPIRYWINDOW = CALENDAR.AdjustBankingDays(runDate, -10)

    active_portfolios = convertListToString(new_active_portfolios_list)
    
    active_portfolios_string = [INSTRUMENT_EXPIRYWINDOW, active_portfolios]
    active_trades_list = getRecordsFromQuery(config.active_trades_query, active_portfolios_string)
    
    try:
        sparks_util.process_trades(active_trades_list)
        #Only one ATS needs to reprocess failed money flows
        if parameter['Type'] == 'EVEN': 
            sparks_util.resend_failed_messages()
    except Exception as exc:
        LOGGER.exception('Sparks Batch feed failed: %s' % str(exc))
        raise
    else:
        LOGGER.info('Completed successfully')

