"""
-------------------------------------------------------------------------------
MODULE
    ResetConfirmationEventHooks


DESCRIPTION
    Validates if trade meets the minimum requirements for a reset confirmation generation.
    This Module is called in the FConfirmationParameters Module and linked to the 
    Reset Confirmation Event

HISTORY
===============================================================================
2018-08-21      Tawanda Mukhalela   FAOPS:168  initial implementation
2019-03-27      Tawanda Mukhalela              Added Functionality for prime linked
                                               Resets
-------------------------------------------------------------------------------
"""

import acm

import FSQL_functions
from ResetAdviceXMLFunctions import ResetAdviceFunctions


def RESET_CONFIRMATION_HOOK(trade):
    """
    Validates if trade meets the minimum requirements for a reset Confimation generation
    :return: boolean value
    """

    if trade:
        today = acm.Time.DateToday()
        if VALID_TRADE(trade):
            for leg in trade.Instrument().Legs():
                for cashflow in leg.CashFlows():
                    if cashflow.StartDate() <= today < cashflow.EndDate():                    
                        days = leg.Currency().Calendar().BankingDaysBetween(today, cashflow.PayDate())
                        #for compounded resets
                        if cashflow.Resets():
                            if cashflow.Resets()[-1].ResetType() in ('Compound', 'Weighted'):
                                if days == 1:
                                    return True 
                                    
                        #for single resets
                        if days == 2:
                            return True

        return False 


def PRIME_FIXING_HOOK(reset):
    """
    SybType Hook for Prime linked Swap Trades
    """
    
    cashflow = reset.CashFlow()
    leg = cashflow.Leg()    
    today = acm.Time.DateToday()
    days = leg.Currency().Calendar().BankingDaysBetween(today, cashflow.PayDate())

    if leg.FloatRateReference():
        if leg.FloatRateReference().Name() == "ZAR-PRIME" and reset.Day() == today:
            if days == 1:
                return True
            
    return False


def VALID_TRADE(trade):
    """
    Trade filtering hook
    """
    today = acm.Time.DateToday()
    if not FSQL_functions.isBankingDay(today, trade.Currency().Name()):
        return False               
    if not ResetAdviceFunctions.evaluate_confinstruction_and_rule_setup(trade.Counterparty(),
                                                                        trade.Instrument().InsType(),
                                                                        'Reset Confirmation'):
        return False
    if ResetAdviceFunctions.is_valid_swap_trade(trade):
        return True
    if ResetAdviceFunctions.is_valid_ccs_trade(trade):
        return True
    
    return False


