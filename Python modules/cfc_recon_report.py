"""
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
MODULE
    cfc_recon_report
    
DESCRIPTION
    Date                     : 2018-09-20
    Purpose                  : PCT wants to reconcile FA Non-Zar cash balances to the Midas Internal CFC balance and then to Odyssey and the GL.
                               At the moment each desk performs this task separately, extracting data from FA, Midas, Odyssey and then reconciling them and 
                               investigating the differences.
                               PCT wants to perform this recon centrally and to do it at a portfolio level. This is something we would have to create. 
                               Once the balance reconciliation is built they should be able to utilize the Sparks Dashboard to explain the differences between FA and Midas. 
                               Once done the recons team will be able to reconcile FA to Odyssey and the GL
                               For now, the idea is to do this for the Commodities desk
    Department and Desk     :  Product Control Team
    Requester               :  Suveshan Iyaloo
    Developer               :  Nkosinathi Sikhakhane
    CR Number               :  CHG1000950672
    

HISTORY
====================================================================================================================================================
Date              CR Number        Developer              Description
----------------------------------------------------------------------------------------------------------------------------------------------------
2018-09-20        CHG1000950672    Nkosinathi Sikhakhane      Initial Implementation.
2018-10-14          ????           Jaysen Naicker             Optomise runtime of code by using CalSpace object.
2020-03-13        CHG0088536       Bhavnisha Sarawan          Add new currencies. Raised PCGDEV-332 as Tech debt item to optimise currency selection.
----------------------------------------------------------------------------------------------------------------------------------------------------
"""

import acm
import os
import string
import ZAR_1022_GL_Query

from at_logging import getLogger
from at_report import CSVReportCreator
from at_ael_variables import AelVariableHandler

CALC_SPACE = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FTradeSheet')
CALC_SPACE_COLLECTION = acm.Calculations().CreateStandardCalculationsSpaceCollection()
COLUMN_ID = 'Portfolio Cash Vector'
INVALID_STATUS = ['Void', 'Simulated']
LOCAL_CURRENCY = acm.FCurrency['ZAR']
LOGGER = getLogger(__name__)
REPORT_CURRENCIES = acm.FStoredASQLQuery['cfc_recon_report_ccys'].Query().Select()
TODAY = acm.Time().DateToday()
TRADER_NAME = 'STRAUSD'
ZAR_CAL = acm.FCalendar['ZAR Johannesburg']

def midas_dealno(trade):
    if trade.IsFxSwapFarLeg(): trade = trade.FxSwapNearLeg()
    if trade.GroupTrdnbr()!= None: trade = trade.GroupTrdnbr()
    if trade.Trader():
        if trade.Trader().Name() == TRADER_NAME:
            if trade.OptionalKey() == '':
                midas_no = trade.add_info('Source Trade Id')
            else:
                midas_no = trade.OptionalKey()
            if len(midas_no.split('_')) > 1:
                return midas_no.split('_')[1]    
        else:
            if trade.YourRef() == '':
                if len(trade.OptionalKey().split('|')) > 1:
                    optkey = trade.OptionalKey().split('|')[0]
                    return optkey[4:10]
            else:
                return trade.YourRef()
    return '' 
    
def get_currency_vector_and_rates(date, isZAR):
    vector = acm.FArray()
    rates = {}

    if isZAR:
        param = acm.FNamedParameters()
        param.AddParameter('currency', acm.FCurrency['ZAR'])
        vector.Add(param)
        rates['ZAR'] = 1.0

        return vector, rates

    for curr in REPORT_CURRENCIES:
        param  = acm.FNamedParameters()
        curr_ins = acm.FCurrency[curr.Name()]
        param.AddParameter('currency', curr_ins)
        vector.Add(param)
        rate = curr_ins.Calculation().FXRate(CALC_SPACE_COLLECTION, LOCAL_CURRENCY, date)
        if rate.Value():
            rates[curr.Name()] = rate.Value().Number()
        else:
            rates[curr.Name()] = 0.0
    return vector, rates

class CfCReconReport(CSVReportCreator):
    """Creates the report"""
    
    def __init__(self, file, query_folder, report_date, isZAR):
        file_name = os.path.basename(file)
        file_name_only = os.path.splitext(file_name)[0]
        file_suffix = os.path.splitext(file_name)[1][1:]
        file_path = os.path.dirname(file)
        self.report_date = report_date
        self.curr_vector, self.rates = get_currency_vector_and_rates(self.report_date, isZAR)
        self.cash_column_config = acm.Sheet.Column().ConfigurationFromVector(self.curr_vector)
        CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
        CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', self.report_date)
        CALC_SPACE.SimulateGlobalValue('Valuation Date', self.report_date)
        TradeGrouper = acm.FAttributeGrouper('Trade.Oid')
        cash_value = CALC_SPACE.InsertItem(query_folder)
        cash_value.ApplyGrouper(TradeGrouper)
        CALC_SPACE.Refresh()
        super(CfCReconReport, self).__init__(file_name_only, file_suffix, file_path)
        
    def _collect_data(self):
        """Collect data for this report"""
        LOGGER.info('collecting .... {0}'.format(acm.Time.TimeNow()))

        trade_filter_iterator = CALC_SPACE.RowTreeIterator().FirstChild()
        child_iter = trade_filter_iterator.FirstChild()
        while child_iter:
            item = child_iter.Tree().Iterator().FirstChild()
            while item:
                cash_value = CALC_SPACE.CalculateValue(item.Tree(), COLUMN_ID, self.cash_column_config)
                try:
                    for value in cash_value.Value():
                        self.add_columns(item, value)
                except:
                    self.add_columns(item, cash_value)
                item = item.NextSibling()  
            child_iter = child_iter.NextSibling()
    
        CALC_SPACE.RemoveGlobalSimulation('Valuation Date')
        CALC_SPACE.RemoveGlobalSimulation('Valuation Parameter Date')
        CALC_SPACE.RemoveGlobalSimulation('Portfolio Profit Loss End Date')
        CALC_SPACE.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')
        CALC_SPACE.Clear()
        LOGGER.info('finished reading data {0}'.format(acm.Time.TimeNow()))
    
    def add_columns(self, item, value):

        if hasattr(value, "Number") and value.Number() <> 0.0:
            trade = item.Tree().Item().Trade()
            self.content.append([
                self.report_date,
                trade.Oid(), 
                trade.Portfolio().Name(), 
                trade.Counterparty().Name(),
                trade.Portfolio().Oid(), 
                trade.Instrument().InsType(),
                trade.Portfolio().AdditionalInfo().MIDAS_Customer_Num(), 
                str(value.Unit()), 
                round(value.Number(), 2), 
                self.rates[str(value.Unit())], 
                midas_dealno(trade),
                trade.MidasSettlement()
                ])

    def _header(self):
        """Define column headers for the report """
        field_names = [
            'Run Date',
            'Trade ID',
            'Portfolio Name',
            'Counterparty',
            'Book ID',
            'Instrument Type',
            'Midas Customer Number',
            'Currency',
            'Amount in Currency',
            'FX Rate to ZAR',
            'Midas Deal Number',
            'Midas Settled?'
        ]
        return field_names
        
ael_variables = AelVariableHandler()

ael_variables.add_directory(
        'output_directory',
        label='Ouput Directory',
        default=r'/services/frontnt/Task')
                            
ael_variables.add(
        'file_name',
        label='File Name',
        default='cfc_recon_report.csv')
                 
ael_variables.add(
        'query_folder',
        label='Query Folder',
        cls=acm.FTradeSelection,
        collection=sorted(acm.FTradeSelection.Select('')),
        default=acm.FTradeSelection['Themba CFC CRT'])
                 
ael_variables.add(
        'date',
        label='Date',
        cls='string',
        default='Today')

ael_variables.add(
        'desk_name',
        label='Desk Name',
        cls='string',
        mandatory=False,
        collection=['FX', 'CRT', 'PRIME', 'TREASURY', 'ST'])

ael_variables.add(
        'is_ZAR',
        label='Is ZAR?',
        cls='bool',
        collection=[True, False],
        default=False)

                          
def ael_main(config):

    LOGGER.msg_tracker.reset()
    file_name = config['file_name']
    report_date = config['date']
    desk_name = config["desk_name"]
    is_ZAR = config["is_ZAR"]

    if report_date == 'Today': 
        report_date = TODAY

    if desk_name:
        ZAR_1022_GL_Query.extend_query(desk_name)

    full_file_path = os.path.join(str(config['output_directory']), file_name)
    query_folder = config['query_folder']

    report = CfCReconReport(full_file_path, query_folder, report_date, is_ZAR)
    LOGGER.info('Generating cfc recon report...{0}'.format(acm.Time.TimeNow()))
    report.create_report()

    if LOGGER.msg_tracker.errors_counter:
        raise RuntimeError('ERRORS occurred. Please check the log.')
    LOGGER.info('Output wrote to {0} at {1}'.format(full_file_path, acm.Time.TimeNow()))
    LOGGER.info('Completed successfully')
