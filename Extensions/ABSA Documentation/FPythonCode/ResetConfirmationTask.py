"""
-------------------------------------------------------------------------------
MODULE
    ResetConfirmationCreator


DESCRIPTION
    Task to generate confirmations for IRS. Based on the cash flow Pay Date the 
    task will generate a document according to the business rules defined for 
    IRS Presettlement Confirmations

HISTORY
===============================================================================
2018-08-21   Tawanda Mukhalela   FAOPS:168  initial implementation
-------------------------------------------------------------------------------
"""

import acm

from at_ael_variables import AelVariableHandler
from at_logging import getLogger
from DocumentConfirmationGeneral import create_document_confirmation
from ResetConfirmationEventHooks import RESET_CONFIRMATION_HOOK
from ResetAdviceXMLFunctions import ResetAdviceFunctions


ael_variables = AelVariableHandler()
today = acm.Time.DateToday()
LOGGER = getLogger(__name__)
SWAP_TRADES = 'IRS_PRESETTLEMENT_SWAP_TRADES'
CCY_TRADES = 'CCY_PRESETTLEMENT_TRADES'
event_name = 'Reset Confirmation'


def ael_main(dict_param):
    swap_trades = acm.FStoredASQLQuery[SWAP_TRADES].Query().Select()
    ccs_trades = acm.FStoredASQLQuery[CCY_TRADES].Query().Select()
    process_trades_for_confirmation_generation(swap_trades)
    process_trades_for_confirmation_generation(ccs_trades)


def process_trades_for_confirmation_generation(trades):
    """
    Process trades for confirmation Generation.
    """
    for trade in trades:
        try:
            LOGGER.info('Processing trade: {trade_oid}'.format(trade_oid=trade.Oid()))
            if ResetAdviceFunctions.check_prime_leg(trade):
                LOGGER.info('Trade is linked to ZAR-PRIME, skipping...')
                continue
            if ResetAdviceFunctions.is_compound(trade):
                LOGGER.info('Trade has compound/weighted resets, skipping...')
                continue
            if not RESET_CONFIRMATION_HOOK(trade):
                LOGGER.info('Trade does not match event hook, skipping...')
                continue
            if _confirmation_already_created_today(trade):
                LOGGER.info('A confirmation has already been created today, skipping...')
                continue
            date_list = []
            date_list.extend(ResetAdviceFunctions.get_multiple_reset_dates_from_legs(trade))
            if len(date_list) > 1:
                generate_confirmation(trade, date_list[0], date_list[1])
            elif len(date_list) == 1:
                generate_confirmation(trade, date_list[0], date_list[0])
        except Exception as exception:
            # Prevent an exception during the generation of one confirmation
            # from preventing the creation of others.
            message = "An exception occurred processing trade '{trade_oid}', "
            message += "skipping..."
            LOGGER.warning(message.format(trade_oid=trade.Oid()), exc_info=True)


def generate_confirmation(trade, from_date, to_date):
    if ResetAdviceFunctions.evaluate_confinstruction_and_rule_setup(trade.Counterparty(),
                                                                    trade.Instrument().InsType(),
                                                                    event_name):
        create_document_confirmation(event_name, trade, None, from_date, to_date, False)


def _confirmation_already_created_today(trade):
    for confirmation in trade.Confirmations():
        if confirmation.EventChlItem().Name() != event_name:
            continue
        if confirmation.CreateDay() == acm.Time.DateToday():
            return True
    return False
