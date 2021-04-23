"""
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
MODULE
    swaps_trade_data
    
DESCRIPTION
    Date                    : 2018-11-19
    Purpose                 : PCT requires a report that shows data on currency and normal swaps, spefically they need to see pay and 
                              receive leg cashflows happening between yesterday and today
    Department and Desk     : Product Control Team
    Requester               : Nhlanhleni Mchunu
    Developer               : Nkosinathi Sikhakhane
    CR Number               :  
    

HISTORY
====================================================================================================================================================
Date              CR Number        Developer              Description
----------------------------------------------------------------------------------------------------------------------------------------------------
2018-11-19                       Nkosinathi Sikhakhane      Initial Implementation.
----------------------------------------------------------------------------------------------------------------------------------------------------
"""

import acm
import csv
import os

from at_logging import getLogger
from at_report import CSVReportCreator
from at_time import acm_date
from at_ael_variables import AelVariableHandler


CALC_SPACE = acm.Calculations().CreateStandardCalculationsSpaceCollection()

TODAY = acm.Time().DateToday()

LOGGER = getLogger(__name__)
               
FILE_PATH = (r'/services/frontnt/Task')
FILE_NAME = 'Swap_Trade_Data.csv'

START_DATES = {
                'Inception': acm_date('Inception'), 
                'First Of Year': acm_date('FirstDayOfYear'), 
                'First Of Month': acm_date('FirstDayOfMonth'), 
                'PrevBusDay': acm_date('PrevBusDay'), 
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

class SwapsTradeData(CSVReportCreator):
    
    
    def __init__(self, file, tf, date_from, date_to):
        file_name = os.path.basename(file)
        file_name_only = os.path.splitext(file_name)[0]
        file_suffix = os.path.splitext(file_name)[1][1:]
        file_path = os.path.dirname(file)
        self.date_from = date_from
        self.date_to = date_to
        self.tf = tf
        
        super(SwapsTradeData, self).__init__(file_name_only, file_suffix, file_path)
    
    
    def get_valid_trades(self):
        trade_filter = acm.FTradeSelection[self.tf]
        trades = trade_filter.Snapshot()
        return list(trades)
    

    def get_pay_receive_amount(self, trade):

        ins_leg0 = trade.Instrument().Legs()[0]
        ins_leg1 = trade.Instrument().Legs()[1]
        values_dict = {}
        
        values_dict['pay_amount'] = ''
        values_dict['pay_date'] = ''
        values_dict['receive_amount'] = ''
        values_dict['receive_date'] = ''
        
        if not trade.AdditionalInfo().CCPccp_id():
           return values_dict
           
        for c0 in ins_leg0.CashFlows():
            if c0.PayDate() >= self.date_from and c0.PayDate() <= self.date_to:
                amount = c0.Calculation().Projected(CALC_SPACE, trade).Number()
                pay_date = c0.PayDate()
                if ins_leg0.PayLeg():
                    values_dict['pay_amount'] = amount
                    values_dict['pay_date'] = pay_date
                else:
                    values_dict['receive_amount'] = amount
                    values_dict['receive_date'] = pay_date
                    break
                    
        for c1 in ins_leg1.CashFlows():
            if c1.PayDate() >= self.date_from and c1.PayDate() <= self.date_to:
                amount = c1.Calculation().Projected(CALC_SPACE, trade).Number()
                pay_date = c1.PayDate()
                if ins_leg1.PayLeg():
                    values_dict['pay_amount'] = amount
                    values_dict['pay_date'] = pay_date
                else:
                    values_dict['receive_amount'] = amount
                    values_dict['receive_date'] = pay_date
                    break
                    
        return values_dict
        
    def _header(self):
        
        field_names = [
            'TrdNo', 
            'Type', 
            'Portfolio', 
            'Status', 
            'PayDay', 
            'PaymentType', 
            'Curr', 
            'Payment',
            'PayLegAmount', 
            'PayDate', 
            'ReceiveLegAmount', 
            'ReceiveDate', 
            'Counterparty', 
            'Acquirer', 
            'CCPTradeID'
        ]
        return field_names
    
    def _collect_data(self):

        trades = self.get_valid_trades()
        for trade in trades:
            if trade.Payments():
                pay = trade.Payments()[-1]
                payment_day = pay.PayDay()
                payment_type = pay.Type()
                payment = pay.Amount()
            else:
                payment_day = ''
                payment_type = ''
                payment = ''
                
            pay_receive = self.get_pay_receive_amount(trade)
                    
            list_of_trades = [
                   trade.Oid(),
                   trade.Instrument().InsType(),
                   trade.Portfolio().Name(),
                   trade.Status(),
                   payment_day,
                   payment_type,
                   trade.Currency().Name(),
                   payment,
                   pay_receive['pay_amount'],
                   pay_receive['pay_date'],
                   pay_receive['receive_amount'],
                   pay_receive['receive_date'],
                   trade.CounterpartyId(),
                   trade.Acquirer().Name(),
                   trade.AdditionalInfo().CCPccp_id()
                ]
            self.content.append(list_of_trades)

ael_variables = AelVariableHandler()
            

ael_variables.add_directory(
      'output_directory',
       label='Ouput Directory',
       default=FILE_PATH)


ael_variables.add(
      'file_name',
       label='File Name',
       default=FILE_NAME)

ael_variables.add(
    'tradeFilter', 
    label = 'TradeFilter', 
    cls = 'string', 
    collection = acm.FTradeSelection.Select(''), 
    default = 'Swap_Trade_Data')


ael_variables.add(
      'startDate',
       label='Start Date',
       cls='string',
       collection=START_DATES.keys(),
       default='PrevBusDay',
       mandatory=True)

ael_variables.add(
    'startDateCustom', 
    label = 'Start Date Custom', 
    cls = 'string',  
    default = acm_date('Inception'),
    mandatory = True)

ael_variables.add(
      'endDate',
       label='End Date',
       cls='string',
       collection=END_DATES.keys(),
       default='Now',
       mandatory=True)

ael_variables.add(
    'endDateCustom', 
    label = 'End Date Custom', 
    cls = 'string',  
    default = acm_date('Inception'),
    mandatory = True)

def ael_main(config):
    
    my_start_date = str(START_DATES[config['startDate']])
    my_end_date = str(END_DATES[config['endDate']])
    trade_filter = str(config['tradeFilter'])
    
    if config['startDate'] == 'Custom Date':
        my_start_date = config['startDateCustom']
    if config['endDate'] == 'Custom Date':
        my_end_date = config['endDateCustom']
        
    full_file_path = os.path.join(str(config['output_directory']), str(config['file_name']))
    report = SwapsTradeData(full_file_path, trade_filter, my_start_date, my_end_date)
    LOGGER.info('Generating swap trade data report...')
    report.create_report()
    LOGGER.output(full_file_path, None)
    LOGGER.info('Completed successfully')
