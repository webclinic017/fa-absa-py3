"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    BrokerNoteConfirmationEventHooks

DESCRIPTION
    This module contains any confirmation event hooks for the Broker Note functionality.

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
2018-08-28      FAOPS-61        Stuart Wilson           Capital Markets         Event trigger for broker note trades.
2019-04-08      FAOPS-379       Stuart Wilson           FICC                    Allow for ZAU isin.
2020-02-10      FAOPS-725       Cuen Edwards            Kgomotso Gumbo          Changes to prevent generation for approximately loaded
                                                                                trades and some minor refactoring.
2020-05-15      FAOPS-795       Cuen Edwards            Kgomotso Gumbo          Changed update-to-recent-trade check from calendar days
                                                                                to business days.
2020-05-22      FAOPS-739       Ntokozo Skosana         Nqubeko Zondi           Added event trigger for broker note for combination
                                                                                trades.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm

import BrokerNoteGeneral
import DocumentConfirmationGeneral


def CONF_BROKER_NOTE(trade):
    """
    Determine whether or not a broker note event should be triggered
    for a trade.
    """
    if _is_valid_broker_note_trade(trade):
        if BrokerNoteGeneral.is_broker_note_trade(trade):
            return True
        if BrokerNoteGeneral.is_broker_note_combination_trade(trade):
            return True
    return False


def _is_valid_broker_note_trade(trade):
    if not _is_update_to_recent_trade(trade):
        return False
    instrument = trade.Instrument()
    return DocumentConfirmationGeneral.active_confirmation_instruction_exists(trade.Counterparty(), BrokerNoteGeneral
                                                                              .get_broker_note_event_name(),
                                                                              trade.Acquirer(), instrument.InsType(),
                                                                              instrument.UnderlyingType())


def _is_update_to_recent_trade(trade):
    """
    Determine whether or not a recently created trade has been
    updated.

    The purpose of this check is to only allow broker notes to
    generate for recent trades - preventing generation if an older
    trade is touched.
    """
    today = acm.Time.DateToday()
    if trade.UpdateDay() != today:
        return False
    calendar = trade.Currency().Calendar()
    two_business_days_ago = calendar.AdjustBankingDays(today, -2)
    return trade.CreateDay() >= two_business_days_ago
