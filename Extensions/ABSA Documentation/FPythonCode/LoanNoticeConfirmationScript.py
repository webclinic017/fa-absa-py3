"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    LoanNoticeConfirmationScript.

DESCRIPTION
    This module contains an AEL main script used for the bulk generation of
    rate notices.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-02-26      FAOPS-160       Stuart Wilson           Loan Ops                Initial Implementation.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

from datetime import datetime

import acm

from at_ael_variables import AelVariableHandler
from at_logging import getLogger
import DocumentConfirmationGeneral
import DocumentGeneral
import LoanNoticeGeneral
import MultiTradeConfirmationOwnerProvider


confirmation_owner_trade_provider = MultiTradeConfirmationOwnerProvider.MultiTradeConfirmationOwnerProvider()
LOGGER = getLogger(__name__)
ael_variables = AelVariableHandler()


ael_variables.add(
    'query_folder',
    label='Query Folder',
    collection=[0, 1],
    cls='int',
    default=0)


ael_variables.add(
    'query_folder_name',
    label='Query name',
    cls=acm.FStoredASQLQuery,
    collection=acm.FStoredASQLQuery.Select(
        "subType='FTrade'"),
    mandatory=False,
    alt="Query folder that will be used to generate confirmation for loan notices")


def _get_trades_from_query_folder(name, date=acm.Time.DateToday()):
    query_name = name
    query_nodes = acm.FStoredASQLQuery[query_name].Query().AsqlNodes()
    asql_query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
    asql_query.AsqlNodes(query_nodes)
    asql_query.AddAttrNode('Instrument.Legs.CashFlows.Resets.Day', 'EQUAL', date)

    valid_trades = list()
    for trade in asql_query.Select():
        if not LoanNoticeGeneral.has_facility(trade):
            continue
        if abs(LoanNoticeGeneral.sum_nominal_before_payday(trade)) == 0:
            continue

        valid_trades.append(trade)

    return valid_trades


def ael_main(ael_parameters):
    """
    AEL Main Function.
    """
    document_event_name = 'Rate Notice'
    query_folder_name = ael_parameters['query_folder_name']

    try:
        start_date_time = datetime.today()
        LOGGER.info('Starting at {start_date_time}'.format(start_date_time=start_date_time))
        trades = _get_trades_from_query_folder(query_folder_name.Name())
        party_acquirer = list()
        trade_per_counterparty_acquirer = list()
        for trade in trades:
            if not LoanNoticeGeneral.conf_rate_notice_event(trade):
                continue

            if not LoanNoticeGeneral.have_all_trades_reset(trade):
                continue

            if (trade.Counterparty(), trade.Acquirer()) in party_acquirer:
                continue

            else:
                party_acquirer.append((trade.Counterparty(), trade.Acquirer()))
                trade_per_counterparty_acquirer.append(trade)

        for trade in trade_per_counterparty_acquirer:
            confo_owner_trade = confirmation_owner_trade_provider.provide_owner_trade(
                trade.Acquirer(), trade.Counterparty())
            DocumentConfirmationGeneral.create_document_confirmation(document_event_name, confo_owner_trade)

        end_date_time = datetime.today()
        LOGGER.info('Completed successfully at {end_date_time}'.format(end_date_time=end_date_time))
        duration = end_date_time - start_date_time
        LOGGER.info('Duration: {duration}'.format(duration=duration))
    except Exception as exception:
        DocumentGeneral.handle_script_exception(exception)
