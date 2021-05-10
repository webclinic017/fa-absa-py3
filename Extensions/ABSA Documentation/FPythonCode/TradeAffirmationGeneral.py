"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    TradeAffirmationGeneral

DESCRIPTION
    This module contains general functionality related to trade affirmations.

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

import DocumentGeneral
import FXOptionDocumentGeneral


def get_trade_affirmation_event_name():
    """
    Get the name of the event to associate with trade affirmation
    confirmations.
    """
    return 'Trade Affirmation'


def get_trade_affirmation_template_name():
    """
    Get the name of the template to associate with trade
    affirmation confirmations.
    """
    return 'ABSA_Trade_Affirmation'


def get_event_description(confirmation):
    """
    Get a description of the confirmation event type.
    """
    event_type = get_trade_type_description(confirmation) + ' Affirmation'
    if confirmation.Type() in ['Amendment', 'Cancellation']:
        event_type += ' ' + confirmation.Type()
    return event_type


def get_trade_type_description(confirmation):
    """
    Get a description of the confirmation trade type.
    """
    instrument = confirmation.Trade().Instrument()
    if FXOptionDocumentGeneral.is_fx_option(instrument):
        return 'FX Option'
    elif instrument.InsType() in ['Swap', 'FRA']:
        return instrument.InsType()
    elif instrument.InsType() == 'CurrSwap':
        return 'Currency Swap'
    else:
        raise ValueError("Unsupported confirmation trade specified.")


def is_markit_wire_affirmed(trade):
    """
    Determine whether or not a trade is affirmed via the MarkitWire
    platform.
    """
    return DocumentGeneral.is_string_value_present(trade.AddInfoValue('CCPmiddleware_id'))
