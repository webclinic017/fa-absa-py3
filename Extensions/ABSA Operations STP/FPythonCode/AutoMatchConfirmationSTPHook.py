"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    AutoMatchConfirmationSTPHook

DESCRIPTION
    This module contains a hook for auto-matching of confirmations.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2017-02-10      CHNG0004099366  Willie van der Bank                             Initial Implementation.
2019-04-12      FAOPS-483       Cuen Edwards            Kgomotso Gumbo          Migrated to Operations STP ATS.
2019-11-28      FAOPS-439       Tawanda Mukhalela       Latitia Carboni         Removed Trade Confirmation from Auto
                                                                                Matching
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm

from at_logging import getLogger
import OperationsSTPFunctions
from OperationsSTPHook import OperationsSTPHook


LOGGER = getLogger(__name__)


class AutoMatchConfirmationSTPHook(OperationsSTPHook):
    """
    Definition of a hook used to perform auto-matching of
    confirmations.
    """

    def Name(self):
        """
        Get the name of the Operations STP Hook.
        """
        return 'Auto-Match Confirmation STP Hook'

    def IsTriggeredBy(self, eventObject):
        """
        Determine whether or not to trigger the hooks STP action/s
        for an event on the specified object.
        """
        if not eventObject.IsKindOf(acm.FConfirmation):
            return False
        confirmation = eventObject
        if confirmation.Status() != 'Pending Matching':
            return False
        event_name = confirmation.EventChlItem().Name()
        if event_name in ['New Trade', 'Trade Affirmation', 'Trade Confirmation']:
            return False
        if confirmation.Transport() != 'Email':
            return False
        date_today = acm.Time.DateToday()
        expiry_day_cutoff = acm.Time.DateAdjustPeriod(date_today, '-20d')
        if confirmation.ExpiryDay() < expiry_day_cutoff:
            return False
        trade = confirmation.Trade()
        if trade.Acquirer().Name() == 'Funding Desk':
            if event_name in ['Adjust Deposit', 'Prolong Deposit', 'Maturity Notice']:
                return False
        instrument = trade.Instrument()
        if instrument.AdditionalInfo().Demat_Instrument():
            return False
        return True

    def PerformSTP(self, confirmation):
        """
        Perform the hooks STP action/s for an event on the specified
        object.

        Please note that the action does not necessarily occur to the
        event object itself but may occur to some related object/s.
        """
        OperationsSTPFunctions.match_confirmation(confirmation)
