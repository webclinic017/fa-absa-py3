"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    PSVostroSTPAutoReleaseHook

DESCRIPTION
    This module contains a hook for STP (straight-through-processing) triggered
    by the adjusting of a deposit and the acquirer (Prime Service Desk).

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2020-12-10      FAOPS-925       Metse Moshobane         Wandile Sithole         Auto releasing of Vostro accounts settlements for Prime Service Desk.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import ael, acm
import re
import EnvironmentFunctions
from OperationsSTPFunctions import release_settlement
from OperationsSTPHook import OperationsSTPHook


class VostroSTPAutoReleaseHook(OperationsSTPHook):
    """
    Definition of a hook used to perform Auto Releasing of Vostro Settlements
    """
    def Name(self):
        """
        Get the name of the Operations STP Hook.
        """
        return 'Auto Release Prime Services Vostro Settlement'

    def IsTriggeredBy(self, eventObject):
        """
        Determine whether or not to trigger the hooks STP action/s
        for an event on the specified object.
        """
        if not eventObject.IsKindOf(acm.FSettlement):
            return False

        if eventObject.Instrument().InsType() != 'Deposit':
            return False
        if eventObject.Currency().Name() != 'ZAR':
            return False
        if eventObject.Type() != 'Fixed Amount':
            return False
        if eventObject.AcquirerName() != 'PRIME SERVICES DESK':
            return False
        if not EnvironmentFunctions.is_production_environment():
            if eventObject.CounterpartyAccountRef().Bic().Name() not in ('ABSAZAJ0', 'ABSAZAJJ'):
                return False
        elif eventObject.CounterpartyAccountRef().Bic().Name() != 'ABSAZAJJ':
            return False
        if not self._is_vostro_settlement(eventObject):
            return False
        if eventObject.Status() != 'Authorised':
            return False
        if eventObject.ValueDay() != acm.Time.DateToday():
            return False

        return True

    def _is_vostro_settlement(self, settlement):
        """
        Determine whether or not a specified settlement is for a vostro
        account.
        """
        return re.match(r'\d{6}ZAR\d{6}', settlement.CounterpartyAccount()) is not None

    def PerformSTP(self, eventObject):
        """
        Perform the hooks STP action/s for an event on the specified
        object.

        Please note that the action does not necessarily occur to the
        event object itself but may occur to some related object/s.
        """
        release_settlement(eventObject)


