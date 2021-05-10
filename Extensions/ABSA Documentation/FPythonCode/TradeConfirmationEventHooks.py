"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    TradeConfirmationEventHooks

DESCRIPTION
    This module contains any confirmation event hooks for trade confirmations.

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
2019-06-14      FAOPS-439       Cuen Edwards            Letitia Carboni         Initial Implementation.
                                Tawanda Mukhalela
2020-02-07      FAOPS-724       Cuen Edwards            Letitia Carboni         Addition of support for approx. load product types.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm

import DocumentConfirmationGeneral
import FXOptionDocumentGeneral
import TradeConfirmationGeneral


def CONF_TRADE_CONFIRMATION(trade):
    """
    Determine whether or not a trade confirmation event should be
    triggered for a trade.
    """
    if _is_fx_option_structure_confirmation_event(trade):
        return True
    if _is_fx_option_standalone_trade_confirmation_event(trade):
        return True
    return False


def _is_fx_option_structure_confirmation_event(trade):
    """
    Determine whether or not a trade matches the criteria for
    generation of an FX Option Structure trade confirmation.
    """
    # The rules around what constitutes the FX Option
    # structures for which confirmations must be generated
    # is somewhat murky so the strategy taken below is to
    # be quite defensive and not accidentally generate
    # confirmations for unexpected scenarios.
    if not FXOptionDocumentGeneral.is_fx_option_structure_trade(trade):
        return False
    prior_fx_option_trade = None
    for fx_option_trade in FXOptionDocumentGeneral.get_supported_fx_option_trades(trade):
        # Check that the trade is valid in isolation.
        if not _is_valid_fx_option_structure_trade(fx_option_trade):
            return False
        # Check that the trade matches all other trades on the required fields.
        if prior_fx_option_trade is None:
            prior_fx_option_trade = fx_option_trade
        elif not _is_matching_fx_option_structure_trade(prior_fx_option_trade, fx_option_trade):
            return False
    # Check that the counterparty has an active confirmation instruction.
    instrument = prior_fx_option_trade.Instrument()
    return DocumentConfirmationGeneral.active_confirmation_instruction_exists(prior_fx_option_trade.Counterparty(),
        TradeConfirmationGeneral.get_trade_confirmation_event_name(), prior_fx_option_trade.Acquirer(),
        instrument.InsType(), instrument.UnderlyingType())


def _is_fx_option_standalone_trade_confirmation_event(trade):
    """
    Determine whether or not a trade matches the criteria for
    generation of an FX Option standalone trade confirmation.
    """
    if not FXOptionDocumentGeneral.is_fx_option_standalone_trade(trade):
        return False
    if trade.Status() != 'BO Confirmed':
        return False
    if not trade.Counterparty().IsdaMember():
        return False
    instrument = trade.Instrument()
    return DocumentConfirmationGeneral.active_confirmation_instruction_exists(trade.Counterparty(), TradeConfirmationGeneral
        .get_trade_confirmation_event_name(), trade.Acquirer(), instrument.InsType(), instrument.UnderlyingType())


def _is_valid_fx_option_structure_trade(fx_option_trade):
    """
    Determine whether or not an FX Option trade is valid for the
    purposes of FX Option Structure confirmation generation.
    """
    # Ensure that trade is BO Confirmed.
    if fx_option_trade.Status() != 'BO Confirmed':
        return False
    instrument = fx_option_trade.Instrument()
    product_type = FXOptionDocumentGeneral.get_product_type(instrument)
    # Ensure valid combination of Approx. load and product type.
    if fx_option_trade.AddInfoValue('Approx. load'):
        if product_type not in TradeConfirmationGeneral.SUPPORTED_PRODUCT_TYPES:
            return False
    else:
        if product_type not in TradeConfirmationGeneral.NON_PRODUCT_TYPES:
            return False
    # Ensure that the counterparty is an ISDA member.
    if not fx_option_trade.Counterparty().IsdaMember():
        return False
    # Ensure that the trade has an exercise type.
    if instrument.ExerciseType() is None:
        return False
    # Ensure that the trade has a settlement type.
    if instrument.SettlementType() is None:
        return False
    # Ensure that the trade has a fixing source.
    if instrument.FixingSource() is None:
        return False
    return True


def _is_matching_fx_option_structure_trade(prior_fx_option_trade, fx_option_trade):
    """
    Determine whether or not two FX Option trades match for the
    purposes of FX Option Structure confirmation generation.
    """
    # Ensure that all trades have the same counterparty.
    if fx_option_trade.Counterparty() != prior_fx_option_trade.Counterparty():
        return False
    # Ensure that all trades have the same acquirer.
    if fx_option_trade.Acquirer() != prior_fx_option_trade.Acquirer():
        return False
    # Ensure that all trades have the same trade date.
    prior_trade_date = acm.Time.DateFromTime(prior_fx_option_trade.TradeTime())
    trade_date = acm.Time.DateFromTime(fx_option_trade.TradeTime())
    if trade_date != prior_trade_date:
        return False
    # Ensure that all trades have the same approx load.
    prior_approx_load = prior_fx_option_trade.AddInfoValue('Approx. load')
    approx_load = fx_option_trade.AddInfoValue('Approx. load')
    if approx_load != prior_approx_load:
        return False
    # Ensure that all trades have the same product type.
    prior_instrument = prior_fx_option_trade.Instrument()
    instrument = fx_option_trade.Instrument()
    prior_product_type = FXOptionDocumentGeneral.get_product_type(prior_instrument)
    product_type = FXOptionDocumentGeneral.get_product_type(instrument)
    if product_type != prior_product_type:
        return False
    # Ensure that all trades have the same exercise type.
    prior_exercise_type = prior_instrument.ExerciseType()
    exercise_type = instrument.ExerciseType()
    if exercise_type != prior_exercise_type:
        return False
    # Ensure that all trades have the same settlement type.
    prior_settlement_type = prior_instrument.SettlementType()
    settlement_type = instrument.SettlementType()
    if settlement_type != prior_settlement_type:
        return False
    # Ensure that all trades have the same fixing source.
    prior_fixing_source = prior_instrument.FixingSource()
    fixing_source = instrument.FixingSource()
    if fixing_source != prior_fixing_source:
        return False
    # Ensure that all trades have the same currency combinations.
    prior_put_currency = FXOptionDocumentGeneral.get_put_currency(prior_instrument)
    prior_call_currency = FXOptionDocumentGeneral.get_call_currency(prior_instrument)
    prior_currencies = [prior_put_currency, prior_call_currency]
    put_currency = FXOptionDocumentGeneral.get_put_currency(instrument)
    if put_currency not in prior_currencies:
        return False
    call_currency = FXOptionDocumentGeneral.get_call_currency(instrument)
    if call_currency not in prior_currencies:
        return False
    return True
