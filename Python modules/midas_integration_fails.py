"""
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
MODULE
    midas_integration_fails
    
DESCRIPTION
    Date                     : 2018-09-20
    Purpose                  : PCT wants a report that shows trades that failed to integrate with Front Arena, these will have status
                               None or Break in various trade fields e.g. status, amount, currency...
    Department and Desk     :  Product Control Team
    Requester               :  Nikola Selic
    Developer               :  Nkosinathi Sikhakhane
    CR Number               :  CHG1000950672
    

HISTORY
====================================================================================================================================================
Date              CR Number        Developer              Description
----------------------------------------------------------------------------------------------------------------------------------------------------
2018-09-20          CHG1000950672       Nkosinathi Sikhakhane      Initial Implementation.
----------------------------------------------------------------------------------------------------------------------------------------------------
"""


import acm
import os
import string

from at_logging import getLogger
from at_report import CSVReportCreator
from at_ael_variables import AelVariableHandler

LOGGER = getLogger(__name__)

TODAY = acm.Time().DateToday()
ZAR_CAL = acm.FCalendar['ZAR Johannesburg']
YESTERDAY = ZAR_CAL.AdjustBankingDays(TODAY, -1)


OUTPUT_DIR = (r'C:\temp' if os.name == 'nt' 
                  else '/services/frontnt/BackOffice/Atlas-End-Of-Day/TradingManager')
                  
CALC_SPACE = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FTradeSheet')

INVALID_STATUS = ['Break', 'None']

DATE_LIST = {
             'Yesterday': YESTERDAY,
             'Custom Date': YESTERDAY,
            }
DATE_KEYS = DATE_LIST.keys()
DATE_KEYS.sort()

class MidasIntegrationFails(CSVReportCreator):
    
    def __init__(self, file, val_date):
        file_name = os.path.basename(file)
        file_name_only = os.path.splitext(file_name)[0]
        file_suffix = os.path.splitext(file_name)[1][1:]
        file_path = os.path.dirname(file)
        self.val_date = val_date
        
        super(MidasIntegrationFails, self).__init__(file_name_only, file_suffix, file_path)
        
    def _header(self):
        """Create column headers for the report"""
        
        field_names = [
            'Trade ID',
            'Portfolio',
            'Status',
            'Currency',
            'Value Date',
            'Currency1',
            'Currency1 Amount',
            'Currency2',
            'Currency2 Amount',
            'MidasStatusRecon',
            'MidasBuyAmountRecon',
            'MidasBuyCurrencyRecon',
            'MidasRateRecon',
            'MidasSellAmountRecon',
            'MidasSellCurrencyRecon'
        ]
        return field_names
        
    def _collect_data(self):
        """Collect data for this report"""
        
        trades = self.get_all_trades()
        try:
            if trades:
                for trade in trades:
                    curr_amt = self.get_currency_and_amount(trade)
                    currency1 = curr_amt['currency1']
                    amount1 = curr_amt['amount1']
                    currency2 = curr_amt['currency2']
                    amount2 = curr_amt['amount2']
                    list_of_trades = [
                        trade.Oid(),
                        trade.Portfolio().Name(),
                        trade.Status(),
                        trade.Currency().Name(),
                        trade.ValueDay(),
                        currency1,
                        amount1,
                        currency2,
                        amount2,
                        trade.MidasStatusRecon(),
                        trade.MidasBuyAmountRecon(),
                        trade.MidasBuyCurrencyRecon(),
                        trade.MidasRateRecon(),
                        trade.MidasSellAmountRecon(),
                        trade.MidasSellCurrencyRecon()
                    ]
                    self.content.append(list_of_trades)
                    
        except Exception as e:
            LOGGER.error('{0}'.format(str(e)))
    
    def get_currency_and_amount(self, acm_trade):
        curr_dict = {}
        try:
            if acm_trade.Instrument().InsType() == 'Curr':
                amt1 = CALC_SPACE.CalculateValue(acm_trade, 'Curr1 Amount')
                amt2 = CALC_SPACE.CalculateValue(acm_trade, 'Curr2 Amount')
                curr1 = CALC_SPACE.CreateCalculation(acm_trade, 'Currency1').Value().Name()
                curr2 = CALC_SPACE.CreateCalculation(acm_trade, 'Currency2').Value().Name()
            elif acm_trade.Instrument().InsType() == 'Option':
                amt1 = CALC_SPACE.CalculateValue(acm_trade, 'Nominal Amount Accounting').Value().Number()
                amt2 = CALC_SPACE.CalculateValue(acm_trade, 'Nominal Amount Accounting Currency 2').Value().Number()
                curr1 = acm_trade.CurrencyPair().Currency1().Name()
                curr2 = acm_trade.CurrencyPair().Currency2().Name()
            else:
                amt1 = CALC_SPACE.CalculateValue(acm_trade, 'Nominal Amount Accounting').Value().Number()
                amt2 = CALC_SPACE.CalculateValue(acm_trade, 'Nominal Amount Accounting Currency 2').Value().Number()
                curr1 = acm_trade.CurrencyPair().Currency2().Name()
                curr2 = acm_trade.CurrencyPair().Currency1().Name()
            
            curr_dict = {'amount1': amt1, 'amount2': amt2, 'currency1': curr1, 'currency2': curr2}
            
        except Exception as e:
            LOGGER.error('{0} : {1}'.format(acm_trade.Oid(), str(e)))
        
        return curr_dict

    def get_trades(self, ins_type, *under_lying):
        """Get all all trades done the previous business day"""
        query = acm.CreateFASQLQuery('FTrade', 'AND')
        query.AddAttrNode('Status', 'NOT_EQUAL', 'FO Sales')
        query.AddAttrNode('Status', 'NOT_EQUAL', 'Simulated')
        query.AddAttrNode('Status', 'NOT_EQUAL', 'Reserved')
        query.AddAttrNode('Counterparty.Name', 'NOT_EQUAL', 'FMAINTENANCE')
        query.AddAttrNode('ValueDay', 'EQUAL', self.val_date)
        query.AddAttrNode('Instrument.InsType', 'EQUAL', ins_type)
        if ins_type != 'Curr':
            query.AddAttrNode('Instrument.UnderlyingType', 'EQUAL', under_lying)

        return list(query.Select())
    
    def get_all_trades(self):
        """Function to combine all trades - fx forwards and fx cash - into one list"""
        trades = []
        all_trades = self.get_trades('Future/Forward', 'Curr') + self.get_trades('Curr')

        if all_trades:
            for trd in all_trades:
                if trd.Status() == 'Void' and trd.MidasStatusRecon() == 'None':
                    continue
                else:
                    if ((trd.MidasStatusRecon() in INVALID_STATUS 
                    or trd.MidasBuyAmountRecon() in INVALID_STATUS 
                    or trd.MidasBuyCurrencyRecon() in INVALID_STATUS 
                    or trd.MidasRateRecon() in INVALID_STATUS 
                    or trd.MidasSellAmountRecon() in INVALID_STATUS 
                    or trd.MidasSellCurrencyRecon() in INVALID_STATUS)
                    and trd.Portfolio().AdditionalInfo().MidasSettleEnabled() == True):
                        trades.append(trd)
        return trades

def enable_custom_start_date(selected_variable):
    cust = ael_variables.get("cust_date")
    cust.enabled = (selected_variable.value == 'Custom Date')
    cust.value = TODAY

ael_variables = AelVariableHandler()

ael_variables.add_directory(
      'output_directory',
       label='Ouput Directory',
       default=OUTPUT_DIR)
                            
ael_variables.add(
      'file_name',
       label='File Name',
       default='midas_integration_fails_report_${DATE}.csv')
                 
ael_variables.add(
      'my_date',
       label='Date',
       cls='string',
       collection=DATE_KEYS,
       hook=enable_custom_start_date,
       default=YESTERDAY,
       mandatory=True)
                  
ael_variables.add(
      'cust_date',
       label='Custom Date',
       cls='string',
       default=YESTERDAY,
       enabled=False)

def ael_main(config):
    fpath_template = string.Template(config['file_name'])
    if config['my_date'] == 'Custom Date':
        run_date = config['cust_date']
    else:
        run_date = config['my_date']
    
    file_path = fpath_template.substitute(DATE=run_date.replace("-", ""))
    output_directory = config['output_directory']
    full_file_path = os.path.join(str(output_directory), file_path)
    report = MidasIntegrationFails(full_file_path, run_date)
    LOGGER.info('Generating midas integration report...')
    report.create_report()
    LOGGER.output(full_file_path, None)
    LOGGER.info('Completed successfully')


