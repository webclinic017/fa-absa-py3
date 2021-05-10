"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    MatchedTradeAffirmationSTPHook

DESCRIPTION
    This module contains a hook for STP (straight-through-processing) triggered
    by the matching of a 'Trade Affirmation' confirmation.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2018-11-30      FAOPS-226       Cuen Edwards            Letitia Carboni         Initial Implementation.
2019-04-08      FAOPS-448       Cuen Edwards            Kgomotso Gumbo          Migrated to Operations STP ATS.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm

from at_logging import getLogger
import OperationsSTPFunctions
from OperationsSTPHook import OperationsSTPHook


LOGGER = getLogger(__name__)


class MatchedTradeAffirmationSTPHook(OperationsSTPHook):
    """
    Definition of a hook used to perform STP triggered by the
    matching of an 'Trade Affirmation' confirmation.
    """

    def Name(self):
        """
        Get the name of the Operations STP Hook.
        """
        return 'Matched Trade Affirmation STP Hook'

    def IsTriggeredBy(self, eventObject):
        """
        Determine whether or not to trigger the hooks STP action/s
        for an event on the specified object.
        """
        if not eventObject.IsKindOf(acm.FConfirmation):
            return False
        confirmation = eventObject
        if confirmation.Status() != 'Matched':
            return False
        if confirmation.EventChlItem().Name() != 'Trade Affirmation':
            return False
        trade = confirmation.Trade()
        if trade.Status() != 'FO Confirmed':
            return False
        return True

    def PerformSTP(self, confirmation):
        """
        Perform the hooks STP action/s for an event on the specified
        object.

        Please note that the action does not necessarily occur to the
        event object itself but may occur to some related object/s.
        """
        OperationsSTPFunctions.bo_confirm_trade(confirmation.Trade())
