"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    MatchedNonZarMT320ConfirmationSTPHook

DESCRIPTION
    This module contains a hook for STP (straight-through-processing) triggered
    by the matching of an MT320 confirmation.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-06-19      FAOPS-393       Tawanda Mukhalela       Wandile Sithole         Non-Zar Deposits and FRN Autorelease on Matched MT320
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import datetime

import acm

from at_logging import getLogger
import OperationsSTPFunctions
from OperationsSTPHook import OperationsSTPHook


LOGGER = getLogger(__name__)
EARLY_CUTOFF_CURRENCIES = ['AUD', 'NZD', 'JPY', 'SGD', 'HKD']


class MatchedNonZarMT320ConfirmationSTPHook(OperationsSTPHook):
    """
    Definition of a hook used to perform STP triggered by the
    matching of a Non-Zar MT320 confirmation.
    """

    # noinspection PyPep8Naming
    def Name(self):
        """
        Get the name of the Operations STP Hook.
        """
        return 'Matched Non-Zar MT320 Confirmation STP Hook'

    # noinspection PyPep8Naming,PyPep8Naming
    def IsTriggeredBy(self, eventObject):
        """
        Determine whether or not to trigger the hooks STP action/s
        for an event on the specified object.
        """
        if eventObject.IsKindOf(acm.FConfirmation):
            if self.is_valid_confirmation(eventObject):
                return True
        elif eventObject.IsKindOf(acm.FSettlement):
            if self._is_valid_settlement(eventObject):
                if not eventObject.Trade():
                    return False
                trade = eventObject.Trade()
                for confirmation in trade.Confirmations():
                    if self.is_valid_confirmation(confirmation):
                        return True
        else:
            return False

    # noinspection PyPep8Naming
    def PerformSTP(self, eventObject):
        """
        Perform the hooks STP action/s for an event on the specified
        object.

        Please note that the action does not necessarily occur to the
        event object itself but may occur to some related object/s.
        """
        trade = eventObject.Trade()
        current_hour = datetime.datetime.now().hour
        if current_hour >= 14:
            self._release_non_zar_settlement(trade)

    def _release_non_zar_settlement(self, trade):
        """
        Release early cutoff non-Zar settlements on ValueDay(T-1)
        Release normal cutoff non-Zar settlements on ValueDay
        """
        today = acm.Time.DateToday()
        calendar = trade.Instrument().Currency().Calendar()
        next_business_day = calendar.AdjustBankingDays(today, 1)
        for settlement in trade.Settlements().AsArray():
            if not self._is_valid_settlement(settlement):
                continue
            is_early_cutoff_currency = settlement.Currency().Name() in EARLY_CUTOFF_CURRENCIES
            if settlement.ValueDay() == today:
                OperationsSTPFunctions.release_settlement(settlement)
                message = 'Released Non-Zar settlement : {settlement} for Trade : {trade}'
                LOGGER.info(message.format(settlement=settlement.Oid(), trade=settlement.Trade().Oid()))
            if settlement.ValueDay() == next_business_day and is_early_cutoff_currency:
                OperationsSTPFunctions.release_settlement(settlement)
                message = 'Released Non-Zar settlement : {settlement} for Trade : {trade}'
                LOGGER.info(message.format(settlement=settlement.Oid(), trade=settlement.Trade().Oid()))

    @staticmethod
    def is_valid_confirmation(eventObject):
        """
        Check Confirmation Validity
        """
        confirmation = eventObject
        if confirmation.Status() != 'Matched':
            return False
        if confirmation.EventChlItem().Name() != 'New Trade':
            return False
        if confirmation.MTMessages() != '320':
            return False
        trade = confirmation.Trade()
        if trade.Acquirer().Name() != 'MONEY MARKET DESK':
            return False
        instrument = trade.Instrument()
        if instrument.InsType() not in ['Deposit', 'FRN']:
            return False
        if instrument.Currency().Name() == 'ZAR':
            return False

        return True

    @staticmethod
    def _is_valid_settlement(eventObject):
        """
        Check Settlement Validity
        """
        settlement = eventObject
        if settlement.Status() != 'Authorised':
            return False
        if OperationsSTPFunctions.is_incoming_settlement(settlement):
            return False
        if settlement.Type() != 'None':
            return False

        return True
