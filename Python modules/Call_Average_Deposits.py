"""-----------------------------------------------------------------------------
MODULE                  :       Call_Average_Deposits
PURPOSE                 :       Report for Call Average Deposits

HISTORY
================================================================================
Date            change no       Developer            Description
--------------------------------------------------------------------------------
2021-01-20                      Teboho Lepele        Initial Implementation
"""

import datetime
import acm, csv, os
from at_logging import getLogger
from at_ael_variables import AelVariableHandler
from FCreditLimit import limit_cp
from FBDPCommon import acm_to_ael
from Call_Average_Balances import averageBalance, interestRate, totalInterest
    
DATETODAY = acm.Time.DateToday()
LOGGER = getLogger(__name__)

header = ['Trdnbr', 
          'Insid', 
          'Counterparty', 
          'BarCap_SMS_CP_SDSID', 
          'BarCap_SMS_LE_SDSID', 
          'Portfolio', 
          'Status',
          'Funding_Instype', 
          'Average_Balance', 
          'Interest', 
          'Rate', 
          'Credit_Limit_CP']


def create_row_data(trade, date):
    LOGGER.info('Processing Trade : {}'.format(trade.Name()))
    trade_data = {'Trdnbr': trade.Oid(),
                  'Insid': trade.Instrument().Name(),
                  'Counterparty': trade.Counterparty().Name(),
                  'BarCap_SMS_CP_SDSID': trade.Counterparty().AddInfoValue('BarCap_SMS_CP_SDSID'),
                  'BarCap_SMS_LE_SDSID': trade.Counterparty().AddInfoValue('BarCap_SMS_LE_SDSID'),
                  'Portfolio': trade.Portfolio().Portfolio().Name(),
                  'Status': trade.Status(),
                  'Funding_Instype': trade.AddInfoValue('Funding Instype'),
                  'Average_Balance': round(averageBalance(None, trade.Oid(), date,), 2),
                  'Interest': round(totalInterest(None, trade.Oid(), date, ), 2),
                  'Rate': round(interestRate(None, date, trade.Oid(), ), 2),
                  'Credit_Limit_CP': round(limit_cp(acm_to_ael(trade.Counterparty())), 2)}
    return trade_data


def write_csv_file(output_file_location, results_list, header_list):
    with open(output_file_location, 'wb') as account_balance_file:
        csv_writer = csv.DictWriter(account_balance_file, fieldnames=header_list, quoting=csv.QUOTE_NONE)
        csv_writer.writeheader()
        csv_writer.writerows(results_list)


ael_variables = AelVariableHandler()

ael_variables.add('filter',
                  cls=acm.FTradeSelection,
                  collection=acm.FTradeSelection.Instances(),
                  label='Filter',
                  mandatory=True,
                  default=acm.FTradeSelection['Call_All_Trades'])

ael_variables.add_directory('output_folder',
                  label='Output Folder',
                  mandatory=True,
                  default='/services/frontnt/Task')

ael_variables.add('date',
                  label='Date',
                  mandatory=True,
                  default=acm.Time().DateToday())


def ael_main(ael_dict):
    day = acm.Time.DayOfMonth(acm.Time.AsDate(ael_dict['date']))
    end_date = acm.Time.DateAddDelta(acm.Time.AsDate(ael_dict['date']), 0, 0, (-1 * day))
    month_year = datetime.datetime(int(end_date[:4]), int(end_date[5:7]), 0o1).strftime('%B_%Y')
    file_name = '{directory}/Call_Average_Balances_{date}.csv'.format(date=month_year, directory=ael_dict['output_folder'])
    output_file = os.path.join(file_name)
    trades = ael_dict['filter'].Trades()
    output_data = map(create_row_data, trades, [end_date] * trades.Size())
    try:
        write_csv_file(output_file, output_data, header)
        LOGGER.info('Successfully created file: {}'.format(output_file))
    except Exception, e:
        LOGGER.error('Failed to write to file: {}'.format(e))
