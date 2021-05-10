"""
-------------------------------------------------------------------------------
MODULE
    ResetAdviceEventHooks


DESCRIPTION
    Validates if trade meets the minimum requirements for a reset advice generation.
    This Module is called in the FConfirmationParameters Module and linked to the
    Reset Advice Event

HISTORY
===============================================================================
2018-08-21      Tawanda Mukhalela       FAOPS:168       initial implementation
2019-03-27      Tawanda Mukhalela                       Changed RESET_ADVICE_HOOK to use
                                                        SubType Reset instead of Trade
2019-05-21      Jaysen Naicker          Upgrade2018     Add check for FReset type object
                                                        in RESET_ADVICE_HOOK
2019-11-06      Tawanda Mukhalela       FAOPS-598       Addition of FRA PreSettlement Advices
-------------------------------------------------------------------------------
"""

import acm

from ResetAdviceXMLFunctions import ResetAdviceFunctions


def RESET_ADVICE_TRADES(trade):
    """
    Validates if trade meets the minimum requirements for a reset advice generation
    :return: boolean value
    """
    if not ResetAdviceFunctions.evaluate_confinstruction_and_rule_setup(trade.Counterparty(),
                                                                            trade.Instrument().InsType(),
                                                                            'Reset Advice'):
        return False

    if swap_reset_advice_valid_trade(trade):
        return True

    if fra_reset_advice_valid_trade(trade):
        return True

    if ccs_reset_advice_valid_trade(trade):
        return True

    return False


def RESET_ADVICE_HOOK(reset):
    """
    Validates if trade meets the minimum requirements for a reset advice generation
    :return: boolean value
    """

    date = acm.Time.DateToday()
    if reset and reset.IsKindOf(acm.FReset):
        if reset.ResetType() in ('Compound', 'Weighted'):
            return False

        if reset.Day() == date and reset.FixingValue() != 0.00:
            return True

    return False


def swap_reset_advice_valid_trade(trade):
    """
    Event hook for swap Advices
    """
    if not ResetAdviceFunctions.is_valid_swap_trade(trade):
        return False
    if ResetAdviceFunctions.check_prime_leg(trade):
        return False

    return True


def fra_reset_advice_valid_trade(trade):
    """
    Event hook for fra Advices
    """
    if not ResetAdviceFunctions.is_valid_fra_trade(trade):
        return False

    return True


def ccs_reset_advice_valid_trade(trade):
    """
    Event hook for ccs Advices
    """

    return False
