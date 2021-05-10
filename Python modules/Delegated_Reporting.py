import acm
import csv
import os

from datetime import datetime
from at_logging import getLogger
from at_ael_variables import AelVariableHandler

LOGGER = getLogger(__name__)
FOOTER = ['*0RCM-END00000001']
VAL_FOOTER = ['*6RCM-END00000001']

VAL_HEADER = ['*Comment', 'Version', 'Message Type', 'Action', 'USI Prefix', 'USI Value', 'Primary Asset Class',
              'Secondary Asset Class', 'Trade Party 1 Prefix', 'Trade Party 1 Value',
              'Trade Party 2 Prefix', 'Trade Party 2 Value', 'Data Submitter Prefix', 'Data Submitter Value',
              'Submitted For Prefix', 'Submitted For Value', 'Cleared Product ID',
              'Valuation Datetime', 'MTM Value', 'MTM Currency', 'Valuation Source', 'Valuation Reference Model',
              'Additional Comments', 'Data Submitter Message Id', 'Valuation Datetime Party 2',
              'MTM Value Party 2', 'MTM Currency Party 2', 'Valuation Type Party 1', 'Valuation Type Party 2',
              'UTI Prefix', 'UTI', 'MTM Value CCP', 'MTM Currency CCP', 'Valuation Type CCP',
              'Valuation Datetime CCP', 'Trade Party 1 Transaction Id', 'Trade Party 2 Transaction Id', 'sendTo',
              'Trade Party 1 - Reporting Destination', 'Party 2 Reporting Obligation',
              'Trade Party 1 -Execution Agent ID Type', 'Trade Party 1 - Execution Agent ID',
              'Trade Party 2 -Execution Agent ID Type', 'Trade Party 2 - Execution Agent ID', 'AI Party 1 - Type',
              'AI Party 1 - ID', 'AI Party 2 - Type', 'AI Party 2 - ID', 'Clearing Status',
              'Trade Party 1 -  Action Type', 'Trade Party 2 - Action Type', 'Level',
              'Trade Party 1 - Third Party Viewer ID Type',
              'Trade Party 1 - Third Party Viewer ID', 'Trade Party 2 - Third Party Viewer ID Type',
              'Trade Party 2 - Third Party Viewer ID', 'Reporting Timestamp']
COL_HEADER = ['*Comment', 'Version', 'Message Type', 'Data Submitter Message ID', 'Action', 'Data Submitter prefix',
              'Data Submitter value', 'Trade Party Prefix', 'Trade Party Value',
              'Execution Agent Party Value Prefix', 'Execution Agent Party Value', 'Collateral Portfolio Code',
              'Collateral Portfolio Indicator', 'Value of the collateral', 'Currency of the collateral',
              'Collateral Valuation Date Time', 'Collateral Reporting Date', 'sendTo', 'Execution Agent Masking Flag',
              'Trade Party - Reporting Obligation', 'Other Party ID Type', 'Other Party ID',
              'Collateralized', 'Initial Margin Posted', 'Currency of the Initial Margin Posted',
              'Initial Margin Received', 'Currency of the Initial Margin Received', 'Variation Margin Posted',
              'Currency of the Variation Margin Posted', 'Variation Margin Received',
              'Currency of the Variation Margin Received', 'Excess Collateral Posted',
              'Currency of the Excess Collateral Posted',
              'Excess Collateral Received', 'Currency of the Excess Collateral received', 'Third Party Viewer',
              'Reserved - Participant Use 1', 'Reserved - Participant Use 2', 'Reserved - Participant Use 3',
              'Reserved - Participant Use 4', 'Reserved - Participant Use 5', 'Action Type Party 1',
              'Third Party Viewer ID Type', 'Level', 'Reporting Timestamp']
NEW_HEADER = ['*Comment', 'Version', 'Message Type', 'Data Submitter Message ID', 'Action', 'Data Submitter prefix',
              'Data Submitter value', 'Trade Party Prefix', 'Trade Party Value',
              'Execution Agent Party Prefix', 'Execution Agent Party Value', 'UTI Prefix', 'UTI Value', 'USI Prefix',
              'USI Value', 'Trade Party Transaction Id', 'Collateral Portfolio code', 'Collateralized',
              'sendTo', 'Trade Party - Reporting Obligation', 'Other Party ID Type', 'Other Party ID',
              'Action Type Party 1', 'Third Party Viewer ', 'Collateral Portfolio Indicator', 'Initial Margin Posted',
              'Currency of the Initial Margin Posted', 'Initial Margin Received',
              'Currency of the Initial Margin Received', 'Variation Margin Posted',
              'Currency of the Variation Margin Posted',
              'Variation Margin Received', 'Currency of the Variation Margin Received', 'Excess Collateral Posted',
              'Currency of the Excess Collateral Posted', 'Excess Collateral Received',
              'Currency of the Excess Collateral received', 'Reserved - Participant Use 1',
              'Reserved - Participant Use 2', 'Reserved - Participant Use 3', 'Reserved - Participant Use 4',
              'Reserved - Participant Use 5', 'Level', 'Third Party Viewer ID Type', 'Execution Agent Masking Flag']

ael_variables = AelVariableHandler()
ael_variables.add('output_folder',
                  label='Output Folder',
                  mandatory=True,
                  default='Y:\Jhb\FAReports\AtlasEndOfDay\Delegated_Reporting')

ael_variables.add('input_folder',
                  label='Input Folder',
                  mandatory=True,
                  default='Y:\Jhb\IT_Pricing_Risk\Data\Prod\MarketRisk\Apex')

ael_variables.add('collateral_position_file',
                  label='Collateral Position File',
                  mandatory=True,
                  default='CollateralBalancePositions.csv')

ael_variables.add('collateral_portfolios',
                  label='Counterparty Collateral Choice List',
                  cls=acm.FChoiceList,
                  collection=sorted(acm.FChoiceList.Choices()),
                  default=acm.FChoiceList['EMIR Collateral Portfolio List'])

ael_variables.add('delegated_reporting_new_deals',
                  label='Delegated Reporting New Deals',
                  cls=acm.FStoredASQLQuery,
                  collection=sorted(acm.FStoredASQLQuery.Select("subType='FTrade'")),
                  default=acm.FStoredASQLQuery['DelegatedReportingNewDeals'])

ael_variables.add('delegated_reporting_valuation',
                  label='Delegated Reporting Valuation Deals',
                  cls=acm.FStoredASQLQuery,
                  collection=sorted(acm.FStoredASQLQuery.Select("subType='FTrade'")),
                  default=acm.FStoredASQLQuery['DelegateReporting_All'])

ael_variables.add('data_submitter_value',
                  label='Data Submitter Value',
                  mandatory=True,
                  default='SLI1CVYMJ21DST0Q8K25')

ael_variables.add('trade_prefix',
                  label='Trade Party Prefix',
                  mandatory=True,
                  default='LEI')


def validate(date_text):
    try:
        if datetime.strptime(date_text, '%Y-%m-%d'):
            return True
    except ValueError:
        return False


def return_latest_date_folder(path):
    return sorted([name for name in os.listdir(path) if validate(name) and os.path.isdir('{}/{}'.format(path, name))],
                  reverse=True)[0]


def create_output_location(output_file):
    try:
        if not os.path.exists(output_file):
            os.makedirs(output_file)
            return True
    except ValueError:
        return False


def preprocess_collateral_data(collateral_input_file):
    """
      This will compile all collateral data needed
    """
    collateral_data = {}
    with open(collateral_input_file) as data:
        results_reader = csv.reader(data, delimiter=',')
        for row in results_reader:
            agreement_id = row[0]
            collateral_balance = row[24]
            collateral_currency = row[25]
            collateral_data[agreement_id] = {'CollateralBalance': collateral_balance,
                                             'CollateralCurrency': collateral_currency}
    return collateral_data


def write_csv_file(output_location, result_list, header_list, footer):
    """
    Create a file to store all results
    """
    with open(output_location, 'wb') as recon_file:
        recon_writer = csv.writer(recon_file)
        recon_writer.writerow(header_list)
        for item in result_list:
            recon_writer.writerow(item)
        recon_writer.writerow(footer)


def new_deals_event(new_trades_list, data_submitter, trade_prefix):
    """
    This creates csv data for new deals events
    """
    LOGGER.info("Processing new trades event")

    new_deals_data = []
    for trade in new_trades_list:
        uti = 'MARKITWIRE{0}'.format(trade.add_info('CCPmiddleware_id'))
        counterparty_lei = trade.Counterparty().LegalEntityId()
        new_deals_data.append(
            ['Trade', 'Coll1.0', 'CollateralLink', '', 'NEW', trade_prefix, data_submitter,
             trade_prefix, counterparty_lei, '', '', '0000452A', uti, '', '', '',
             '1001', 'Partial', '', 'ESMA', trade_prefix, data_submitter, 'V', '', 'Y', '', '', '', '',
             '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
    return new_deals_data


def collateral_valuation_event(collateral_dictionary, collateral_choice_list, data_submitter, trade_prefix):
    """
        This will create  csv data for valuation on collateral
    """
    LOGGER.info("Processing collateral valuation event")
    col_data = []
    for choice in collateral_choice_list.Choices():
        portfolio = choice.Name()
        currency = collateral_dictionary[portfolio]['CollateralCurrency']
        balance = collateral_dictionary[portfolio]['CollateralBalance']
        valuation_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        if acm.FCounterParty[choice.Description()]:
            counterparty_lei = acm.FCounterParty[choice.Description()].LegalEntityId()
        elif acm.FClient[choice.Description()]:
            counterparty_lei = acm.FClient[choice.Description()].LegalEntityId()
        else:
            counterparty_lei = ""
        col_data.append(
            ['ABSA Collateral', 'Coll1.0', 'CollateralValue', '', 'New', trade_prefix, data_submitter,
             trade_prefix, counterparty_lei, '', '', '1001', 'Y', '', '', valuation_time, '', '', '',
             'ESMA', trade_prefix, data_submitter, 'Partially', '', '', '', '', '0', currency,
             balance, currency, '0', currency, '0', currency, '', '', '', '', '', '', 'V', '', '',
             valuation_time])
    return col_data


def valuation_event(trade_list, data_submitter, trade_prefix):
    """
    This will create csv data for valuation event
    """
    LOGGER.info("Processing valuation event")
    std_calculation_space_collection = acm.Calculations().CreateStandardCalculationsSpaceCollection()
    val_data = []
    for trade in trade_list:
        counterparty_name = trade.Counterparty().Name()
        trd_nbr = trade.Name()
        uti = 'MARKITWIRE{0}'.format(trade.add_info('CCPmiddleware_id'))
        mtm_value = trade.Calculation().MarkToMarketValue(std_calculation_space_collection).Number()
        valuation_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        counterparty_lei = trade.Counterparty().LegalEntityId()
        currency = trade.Currency().Name()
        val_data.append(
            [trd_nbr, '', 'Valuation', 'New', '', '', 'InterestRate', '', trade_prefix, counterparty_lei,
             trade_prefix, data_submitter, trade_prefix, data_submitter,
             trade_prefix, counterparty_lei, '', valuation_time, mtm_value, currency, '', '', '',
             counterparty_name, '', '', '', 'MarkToMarket', '', '0000452A', uti, '', '', '', '', trd_nbr, 'EXTERNAL',
             '', 'ESMA', '', '', '', '', '', '', '', '', '', 'FALSE', 'V', '', 'T', '', '', '', '',
             valuation_time])
    return val_data


def ael_main(ael_dict):
    LOGGER.info("Start processing EMIR reporting data")
    today = datetime.now().strftime('%Y-%m-%d')
    folder = "{0}/{1}".format(ael_dict['output_folder'], today)
    create_output_location(folder)
    new_trades = ael_dict['delegated_reporting_new_deals'].Query().Select()
    if len(new_trades) > 0:
        new_deals = new_deals_event(new_trades, str(ael_dict['trade_prefix']), str(ael_dict['data_submitter_value']))
        new_deals_file = "{0}/New Deals  - Reported_{1}.csv".format(folder,
                                                                     today)
        LOGGER.info("Writing  new deals event data to {}".format(new_deals_file))
        write_csv_file(new_deals_file, new_deals, NEW_HEADER, FOOTER)
    else:
        LOGGER.info("No new trades")

    collateral_input_file = r'{0}/{1}/{2}'.format(ael_dict['input_folder'],
                                                    return_latest_date_folder(ael_dict['input_folder']),
                                                    ael_dict['collateral_position_file'])
    collateral_data = preprocess_collateral_data(collateral_input_file)
    col_data = collateral_valuation_event(collateral_data, ael_dict['collateral_portfolios'],
                                          str(ael_dict['trade_prefix']), str(ael_dict['data_submitter_value']))
    collateral_file = "{0}/Collateral_Reported_{1}.csv".format(folder,
                                                                   today)
    LOGGER.info("Writing  collateral valuation event data to {}".format(collateral_file))
    write_csv_file(collateral_file, col_data, COL_HEADER, FOOTER)

    val_data = valuation_event(ael_dict['delegated_reporting_valuation'].Query().Select(),
                               str(ael_dict['trade_prefix']), str(ael_dict['data_submitter_value']))
    valuation_file = "{0}/Valuation_Reported_{1}.csv".format(folder,
                                                                 today)
    LOGGER.info("Writing  valuation event data to {}".format(valuation_file))
    write_csv_file(valuation_file, val_data, VAL_HEADER, VAL_FOOTER)
    LOGGER.info("Processing Done")
