"""------------------------------------------------------------------------------------------------------------------
MODULE
    ASUSNewTradeConfirmationEventHooks

DESCRIPTION
    Hooks to define the 10b10 Confirmation Event for Bonds

---------------------------------------------------------------------------------------------------------------------
HISTORY
=====================================================================================================================
Date            Change no       Developer               Requester               Description
---------------------------------------------------------------------------------------------------------------------
2020-02-17      FAOPS-708       Tawanda Mukhalela       Ndivhuwo Mashishimise   ASUS New Trade Confirmations
2020-04-29      FAOPS-748       Tawanda Mukhalela       Ndivhuwo Mashishimise   ASUS DMA New Trade Confirmation event
---------------------------------------------------------------------------------------------------------------------
"""

import ASUSNewTradeConfirmationGeneral


def ASUS_NEW_TRADE_EVENT(trade):
    """
    Event Hook for 10b10 Confirmation
    """
    if _is_valid_bond_new_trade_event(trade):
        return True
    if _is_valid_dma_new_trade_event(trade):
        return True

    return False


def _is_valid_bond_new_trade_event(trade):
    """
    Handles requirements for a New Trade Event
    """
    block_trade = trade if trade.TrxTrade() is None else trade.TrxTrade()
    if block_trade.Status() not in ['FO Confirmed', 'Void']:
        return False
    if not ASUSNewTradeConfirmationGeneral.is_valid_asus_bond_trade(block_trade):
        return False
    if block_trade.Status() == 'Void':
        if not ASUSNewTradeConfirmationGeneral.is_void_and_has_allocations(block_trade):
            return False

    return True


def _is_valid_dma_new_trade_event(trade):
    """
    Rules to define the DMA 10b10 ConfirmtionEvent
    """
    if trade.AdditionalInfo().XtpTradeType() != 'OBP_BROKER_NOTE':
        return False
    if trade.Status() != 'BO Confirmed':
        return False
    if trade.Portfolio().Name() != 'DMA':
        return False
    if not trade.Counterparty().LegalForm():
        return False
    if trade.Counterparty().LegalForm().Name() != '15a6 US client':
        return False
    instrument_type = trade.Instrument().InsType()
    if not ASUSNewTradeConfirmationGeneral.evaluate_conf_instruction_and_rule_setup(trade.Counterparty(),
                                                                                    instrument_type):
        return False

    return True
