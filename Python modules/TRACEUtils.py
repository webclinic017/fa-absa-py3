
"""

TRACEUtils
Houses all utils functions for FINRA TRACE reporting

History
=======
2020-08-25 Snowy Mabilu ARR-26/ARR-27/ARR-28 - Added util functions for TRACE reporting

"""

import acm
NEW_TRADE_QUERY = 'FINRA_NEW_TRADES'
CANCELLED_TRADES_QUERY = 'FINRA_CANCEL_TRADES'
FINRA_LIVE_TRADE = 'FINRA_LIVE_TRADES'
FINRA_STATE_CHART = 'FTRACEStateChart_36'
FINRA_SYMBOL = 'FINRA_SYMBOL'
CUSIP = 'CUSIP'


def is_valid_trade(query_folder, trade):
    """
    :param query_folder: The input query folder with the desirable conditions
    :param trade:  
    :return: boolean indicating whether the trade satisfies conditions in the query folder 
    """
    query = acm.FStoredASQLQuery[query_folder]
    if query:
        return query.Query().IsSatisfiedBy(trade)
    return False


def get_alias(f_object, name):
    """
    :param f_object: Front Arena Object
    :param name: name of the alias
    :return: value of the alias
    """
    for a in f_object.Aliases():
        if a.Type().Name() == name:
            return a.Alias()
    return None


def is_trace_eligble(trade):
    """
    Checks if the object is eligible for TRACE reporting or not
    :param trade: 
    :return:boolean indicating whether the trade is eligble for TRACE reporting
    """
    return is_valid_trade(NEW_TRADE_QUERY, trade)


def trigger_finra_send(trade, event):
    """
    Triggers an event on business process
    :param trade: trade that will be used as a business process subject
    :param event: the event that will be triggered
    """
    business_processes = acm.BusinessProcess.FindBySubjectAndStateChart(trade, FINRA_STATE_CHART)
    for process in business_processes:
        if process.CanHandleEvent(event):
            process.HandleEventEx(event)


def was_previously_reported(trade):
    """
    Checks if a trade was reported to TRACE or not
    :param trade: input trade to validate
    :return: bolean indicating whether the trade was reported to TRACE
    """
    processes = acm.BusinessProcess.FindBySubjectAndStateChart(trade, FINRA_STATE_CHART)
    for process in processes:
        if process:
            return process.CurrentStateName() == 'Reported'
    return False


def has_finra_live_trades(instrument):
    """
    Check if an instrument has live trades that have been reported to FINRA
    :param instrument: input instrument to validate
    :return: boolean indicating whether the instrument has trades that have been reported to FINRA
    """
    for trade in instrument.Trades():
        if was_previously_reported(trade):
            return True
    return False


def has_finra_identifier(instrument):
    """
    Checks if the instrument has been marked with a FINRA identifier (FINRA_SYMBOL or CUSIP)
    :param instrument: 
    :return: boolean indicating if the instrument has been marked
    """

    if get_alias(instrument, FINRA_SYMBOL) or get_alias(instrument, CUSIP):
        return True
    return False


def has_finra_bp(trade):
    """
    Verifies if a trade has a FINRA business process
    :param trade: trade
    :return:boolean indicating where the trade has a business process linked to it
    """
    processes = acm.BusinessProcess.FindBySubjectAndStateChart(trade, FINRA_STATE_CHART)
    if len(processes) > 0:
        return True
    return False


def has_live_allocations(trade):
    """
    Checks if a block trade has  live allocations linked to it
    :param trade: block trade
    :return: boolean indicating whether the trade has live allocations or not
    """
    allocations = acm.FTrade.Select('trxTrade = {}'.format(trade.Name()))
    if len(allocations) == 0:
        return False
    for trd in allocations:
        if trd.Status() != 'Void':
            return True
    return False


