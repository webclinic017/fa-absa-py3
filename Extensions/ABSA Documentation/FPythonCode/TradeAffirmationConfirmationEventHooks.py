"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    TradeAffirmationConfirmationEventHooks

DESCRIPTION
    This module contains any confirmation event hooks for trade affirmations.

    These hooks are plugged into the FConfirmationParameters.confirmationEvents
    confirmation event definitions list and are used by Front Arena to determine
    when a specified confirmation event has occurred.

NOTES:
    Hooks named using uppercase characters to match existing custom ABSA hooks.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2018-10-25      FAOPS-226       Cuen Edwards            Letitia Carboni         Initial Implementation.
2019-03-01      FAOPS-385       Cuen Edwards            Letitia Carboni         Addition of support for FX Barrier Options.
2019-04-30      FAOPS-461       Cuen Edwards            Letitia Carboni         Addition of support for Swaps.
2019-05-10      FAOPS-497       Cuen Edwards            Letitia Carboni         Addition of support for FRAs.
2019-08-28      FAOPS-606       Cuen Edwards            Letitia Carboni         Prevent generation for MarkitWire confirmed trades.
2020-05-18      FAOPS-511       Cuen Edwards            Letitia Carboni         Addition of support for Currency Swaps.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import DocumentConfirmationGeneral
import FXOptionDocumentGeneral
import TradeAffirmationGeneral


def CONF_TRADE_AFFIRMATION(trade):
    """
    Determine whether or not a trade affirmation event should be
    triggered for a trade.
    """
    if _is_fx_option_trade_affirmation_event(trade):
        return True
    if _is_swap_trade_affirmation_event(trade):
        return True
    if _is_fra_trade_affirmation_event(trade):
        return True
    if _is_currency_swap_trade_affirmation_event(trade):
        return True
    return False


def _is_fx_option_trade_affirmation_event(trade):
    """
    Determine whether or not a trade matches the criteria for
    generation of an FX Option trade affirmation.
    """
    if not FXOptionDocumentGeneral.is_supported_fx_option_trade(trade):
        return False
    if trade.Status() != 'FO Confirmed':
        return False
    instrument = trade.Instrument()
    return DocumentConfirmationGeneral.active_confirmation_instruction_exists(trade.Counterparty(),
        TradeAffirmationGeneral.get_trade_affirmation_event_name(), trade.Acquirer(),
        instrument.InsType(), instrument.UnderlyingType())


def _is_swap_trade_affirmation_event(trade):
    """
    Determine whether or not a trade matches the criteria for
    generation of a Swap trade affirmation.
    """
    instrument = trade.Instrument()
    if instrument.InsType() != 'Swap':
        return False
    if trade.Status() != 'FO Confirmed':
        return False
    if trade.Type() != 'Normal':
        return False
    if TradeAffirmationGeneral.is_markit_wire_affirmed(trade):
        return False
    return DocumentConfirmationGeneral.active_confirmation_instruction_exists(trade.Counterparty(),
        TradeAffirmationGeneral.get_trade_affirmation_event_name(), trade.Acquirer(),
        instrument.InsType(), instrument.UnderlyingType())


def _is_fra_trade_affirmation_event(trade):
    """
    Determine whether or not a trade matches the criteria for
    generation of a FRA trade affirmation.
    """
    instrument = trade.Instrument()
    if instrument.InsType() != 'FRA':
        return False
    if trade.Status() != 'FO Confirmed':
        return False
    if trade.Type() != 'Normal':
        return False
    if TradeAffirmationGeneral.is_markit_wire_affirmed(trade):
        return False
    return DocumentConfirmationGeneral.active_confirmation_instruction_exists(trade.Counterparty(),
        TradeAffirmationGeneral.get_trade_affirmation_event_name(), trade.Acquirer(),
        instrument.InsType(), instrument.UnderlyingType())


def _is_currency_swap_trade_affirmation_event(trade):
    """
    Determine whether or not a trade matches the criteria for
    generation of a Currency Swap trade affirmation.
    """
    instrument = trade.Instrument()
    if instrument.InsType() != 'CurrSwap':
        return False
    if trade.Status() != 'FO Confirmed':
        return False
    if trade.Type() not in ['Normal', 'Closing']:
        return False
    if TradeAffirmationGeneral.is_markit_wire_affirmed(trade):
        return False
    return DocumentConfirmationGeneral.active_confirmation_instruction_exists(trade.Counterparty(),
        TradeAffirmationGeneral.get_trade_affirmation_event_name(), trade.Acquirer(),
        instrument.InsType(), instrument.UnderlyingType())
