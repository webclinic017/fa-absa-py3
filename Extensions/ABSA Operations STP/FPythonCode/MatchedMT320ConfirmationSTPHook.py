"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    MatchedMT320ConfirmationSTPHook

DESCRIPTION
    This module contains a hook for STP (straight-through-processing) triggered
    by the matching of an MT320 confirmation.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-01-31      FAOPS-378       Cuen Edwards            Nicolette Burger        Initial Implementation.
2019-04-08      FAOPS-448       Cuen Edwards            Kgomotso Gumbo          Migrated to Operations STP ATS.
2019-06-04      FAOPS-528       Joash Moodley           Kgomotso Gumbo          Added Fail Safe in case the Confirmation is matched before the settlement is created. 
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import re

import acm

from at_logging import getLogger
import OperationsSTPFunctions
from OperationsSTPHook import OperationsSTPHook


LOGGER = getLogger(__name__)


class MatchedMT320ConfirmationSTPHook(OperationsSTPHook):
    """
    Definition of a hook used to perform STP triggered by the
    matching of an MT320 confirmation.
    """

    def Name(self):
        """
        Get the name of the Operations STP Hook.
        """
        return 'Matched MT320 Confirmation STP Hook'

    def IsTriggeredBy(self, eventObject):
        """
        Determine whether or not to trigger the hooks STP action/s
        for an event on the specified object.
        """
        self.confirmation_obj = None
        if eventObject.IsKindOf(acm.FConfirmation):
            confirmation = eventObject
            if self._validate_confirmation(confirmation):
                self.confirmation_obj = confirmation
                return True
        elif eventObject.IsKindOf(acm.FSettlement):
            settlement = eventObject
            if settlement.Status() != 'Authorised':
                return False
            if settlement.Trade() is None:
                return False
            confirmations = settlement.Trade().Confirmations()
            for confirmation in confirmations:
                if self._validate_confirmation(confirmation):
                    self.confirmation_obj = confirmation
                    return True
        else:
            return False
        
    def PerformSTP(self, eventObject):
        """
        Perform the hooks STP action/s for an event on the specified
        object.

        Please note that the action does not necessarily occur to the
        event object itself but may occur to some related object/s.
        """
        confirmation = self.confirmation_obj
        premium_settlement = self._get_authorised_premium_settlement(confirmation.Trade())
        if premium_settlement is None:
            LOGGER.info('No authorised premium settlement found, skipping.')
            return
        if self._is_vostro_settlement(premium_settlement):
            LOGGER.info('Vostro premium settlement {settlement_oid} found.'.format(
                settlement_oid=premium_settlement.Oid()
            ))
            OperationsSTPFunctions.release_settlement(premium_settlement)
        else:
            LOGGER.info('Non-vostro premium settlement {settlement_oid} found.'.format(
                settlement_oid=premium_settlement.Oid()
            ))
            OperationsSTPFunctions.hold_settlement(premium_settlement)

    def _get_authorised_premium_settlement(self, trade):
        """
        Get any authorised premium settlement for a trade.
        """
        for settlement in trade.Settlements().AsArray():
            if settlement.Status() != 'Authorised':
                continue
            if self._is_premium_settlement(settlement):
                return settlement
        return None

    def _is_premium_settlement(self, settlement):
        """
        Determine whether or not a specified settlement represents a
        premium settlement.
        """
        return settlement.SettlementType() == 'Premium'

    def _is_vostro_settlement(self, settlement):
        """
        Determine whether or not a specified settlement is for a vostro
        account.
        """
        return re.match(r'\d{6}ZAR\d{6}', settlement.CounterpartyAccount()) is not None
    
    def _validate_confirmation(self, confirmation):
        """
        Check if confirmation is valid for STP
        """
        if confirmation.Status() != 'Matched':
            return False
        if confirmation.EventChlItem().Name() != 'New Trade':
            return False
        if confirmation.MTMessages() != '320':
            return False
        trade = confirmation.Trade()
        if trade.Status() not in ['BO Confirmed', 'BO-BO Confirmed']:
            return False
        if trade.Acquirer().Name() != 'Funding Desk':
            return False
        if trade.ValueDay() < acm.Time.DateToday():
            return False
        instrument = trade.Instrument()
        if instrument.InsType() not in ['Deposit', 'FRN']:
            return False
        return True
