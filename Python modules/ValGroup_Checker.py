"""---------------------------------------------------------------------------------------------------------------------
MODULE                  :       ValGroup_Checker
PURPOSE                 :       This module contains details to identify trades with incorrect ValGroup. The report
                                produced shows the trades ValGroup(if incorrect) and the correct ValGroup
------------------------------------------------------------------------------------------------------------------------

HISTORY
========================================================================================================================
Date            Change no       Developer       Requester                           Description
------------------------------------------------------------------------------------------------------------------------
2020-11-09      FAFO-163        Ruth Nkuna      Zanele Ncayiyana                   Initial Implementation
2021-02-01      FAFO-187        Ruth Nkuna      Zanele Ncayiyana                   Removed GTMM/GTMM added CRT
------------------------------------------------------------------------------------------------------------------------

"""

import os
from at_ael_variables import AelVariableHandler
from logging import getLogger
from AMWI_ValGroup import get_csa_val_group
from FAFOUtils import WriteCSVFile


LOGGER = getLogger(__name__)


def is_clearing_trade(acm_trade):
    if acm_trade.AdditionalInfo().CCPclearing_process():
        if acm_trade.AdditionalInfo().CCPclearing_process().startswith('LCH'):
            return True
    if acm_trade.AdditionalInfo().CCPccp_id():
        if acm_trade.AdditionalInfo().CCPccp_id().startswith('LCH'):
            return True
    return False


def get_trade_current_val_group(acm_trade):
    current_val_group = None
    if acm_trade.Instrument().ValuationGrpChlItem():
        current_val_group = acm_trade.Instrument().ValuationGrpChlItem().Name()
    return current_val_group


def get_correct_disc_type(acm_trade):
    correct_disc_type = None
    counterparty = acm_trade.Counterparty()
    if counterparty:
        csa_curr = counterparty.AdditionalInfo().CSA_Collateral_Curr()
        correct_disc_type = 'CSA-' + csa_curr
    return correct_disc_type


def should_include_trade(acm_trade):
    if acm_trade.Acquirer() and acm_trade.Counterparty():
        counter_party = acm_trade.Counterparty().Name()
        acquirer = acm_trade.Acquirer().Name()
        if counter_party in ['STRUCT NOTES DESK', 'PRIME SERVICES DESK']:
            return False
        names = ['ABCAP CRT', 'CREDIT DERIVATIVES DESK']
        if all(p in names for p in [acquirer, counter_party]):
            return False
        if 'CREDIT DERIVATIVES DESK' in [counter_party, acquirer]:
            return False
        if 'ABCAP CRT' in [acquirer, counter_party]:
            return False
        if 'FMAINTENANCE' in [acquirer, counter_party]:
            return False
    current_val_group = get_trade_current_val_group(acm_trade)
    is_clearing = is_clearing_trade(acm_trade)
    correct_csa_val_group = get_csa_val_group(acm_trade, is_clearing)

    if current_val_group is None and acm_trade.Instrument().DiscountingType():

        current_disc_type = acm_trade.Instrument().DiscountingType().Name()
        correct_disc_type = get_correct_disc_type(acm_trade)
        if current_disc_type == correct_disc_type:
            return False

    if current_val_group == correct_csa_val_group:
        return False
    return True


def trade_data(acm_trade):
    is_clearing = is_clearing_trade(acm_trade)
    current_val_group = get_trade_current_val_group(acm_trade)
    correct_csa_val_group = get_csa_val_group(acm_trade, is_clearing)
    current_disc_type = None
    correct_disc_type = None
    if current_val_group is None:
        if acm_trade.Instrument().DiscountingType():
            current_disc_type = acm_trade.Instrument().DiscountingType().Name()
        correct_disc_type = get_correct_disc_type(acm_trade)

    res = [
        acm_trade.Name(), acm_trade.Instrument().Name(), acm_trade.Instrument().InsType(), current_val_group,
        correct_csa_val_group, current_disc_type, correct_disc_type, acm_trade.Portfolio().Name(), acm_trade.Counterparty().Name(),
        acm_trade.Acquirer().Name(), acm_trade.ExecutionTime()
    ]
    return res


def get_trades_data(trade_list):
    LOGGER.info("Filtering and processing {} trades".format(str(len(list(trade_list)))))
    filtered_trades = filter(lambda trade: should_include_trade(trade), trade_list)
    result = [trade_data(res) for res in filtered_trades]
    LOGGER.info("Found {} Trades to process.".format(len(list(result))))
    return result


def get_trades(param_dict):
    trade_filters = param_dict['trade_filters']
    query_folder = param_dict['query_folder']
    portfolios = param_dict['portfolios']
    exclusion_trade_filters = param_dict['exclusion_trade_filters']

    trades = set()
    trades_to_exclude = set()

    if trade_filters:
        for trade_filter in trade_filters:
            LOGGER.info("Fetching Trades from the Trade Filter {}".format(trade_filter.Name()))
            trades.update(trade_filter.Trades())
    if portfolios:
        for portfolio in portfolios:
            LOGGER.info("Fetching Trades from the Portfolio {}".format(portfolio.Name()))
            trades.update(portfolio.Trades())
    if query_folder:
        selection = query_folder.Query().Select()
        LOGGER.info("Fetching Trades from the Query Folder {}".format(query_folder.Name()))
        if query_folder.TypeDisplayName() == 'Trade Filter':
            trades.update(selection)
        elif query_folder.TypeDisplayName() == 'Instrument Filter':
            for instrument in selection:
                trades.update(instrument.Trades())
        elif query_folder.TypeDisplayName() in ['Settlement Filter', 'Confirmation Filter']:
            for item in selection:
                trades.update(item.Trade())
    if exclusion_trade_filters:
        for exclusion_trade_filter in exclusion_trade_filters:
            LOGGER.info("Fetching Trades from the exclusion trade filter  {}".format(exclusion_trade_filter.Name()))
            trades_to_exclude.update(exclusion_trade_filter.Trades())

    trades_to_include = trades-trades_to_exclude
    return trades_to_include


def validate_input(param_dict):
    input_params = [param_dict['trade_filters'], param_dict['query_folder'], param_dict['portfolios']]
    if all([True if _input is None else False for _input in input_params]):
        raise IOError("Invalid input Data.")

    file_path = param_dict['output_directory'].AsString()
    if not os.path.isdir(file_path):
        raise IOError('File does not exist: {}'.format(file_path))


default_path = r"C:\temp"
default_file_name = "Incorrect_Val_Group_Trades.csv"

ael_variables = AelVariableHandler()
ael_variables.add('trade_filters', label='Trade Filter(s)', cls='FTradeSelection', default=None, multiple=True, mandatory=False)
ael_variables.add('query_folder', label='Query Folder', cls='FStoredASQLQuery', default=None, mandatory=False)
ael_variables.add('portfolios', label='Portfolio(s)', cls='FPhysicalPortfolio', default=None, multiple=True, mandatory=False)
ael_variables.add('exclusion_trade_filters', label='Exception Exclusion Filter', cls='FTradeSelection', default=None, multiple=True, mandatory=False)
ael_variables.add_directory('output_directory', label='File Directory', cls='FFileSelection', default=default_path)
ael_variables.add('output_file_name', label='Output File Name', cls='string', default=default_file_name)


def ael_main(ael_dict):
    validate_input(ael_dict)
    output_file_location = ael_dict['output_directory'].AsString()
    file_name = ael_dict['output_file_name']
    header = ["Trade Number", "Instrument Valgroup", "InsType", "Current_val_group", "Correct_Val_group",
              "Current_DiscType", "Correct_DiscType", "Portfolio", "Counterparty", "Acquirer", "Execution Time"]
    try:
        trades = get_trades(ael_dict)
        result = get_trades_data(trades)
        WriteCSVFile(output_file_location, file_name, result, header)
    except Exception as error:
        LOGGER.exception(error)
