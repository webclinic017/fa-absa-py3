"""-----------------------------------------------------------------------------------------------------------------
MODULE
    NamibianSettlementsSTPHook

DESCRIPTION
    This module contains a hook for STP (straight-through-processing) triggered
    by the NANX Counterparty BIC Address.

--------------------------------------------------------------------------------------------------------------------
HISTORY
====================================================================================================================
Date            Change no       Developer               Requester               Description
--------------------------------------------------------------------------------------------------------------------
2019-03-26      FAOPS-532       Tawanda Mukhalela       Khanya Modise           Autohold Settlements with NANX Bic
                                                                                for Call Accounts
2021-03-08      FAOPS-1085      Tawanda Mukhalela       Wandile Sithole         Remove auto-hold functionality and
                                                                                Enable Auto release of Namibian
                                                                                Settlements.
--------------------------------------------------------------------------------------------------------------------
"""

import acm

from at_logging import getLogger
import OperationsSTPFunctions
from OperationsSTPHook import OperationsSTPHook
from EnvironmentFunctions import is_production_environment


LOGGER = getLogger(__name__)


class NamibianSettlementsAutoReleaseHook(OperationsSTPHook):
    """
    Definition of a hook used to perform Operations STP.
    """

    def Name(self):
        """
        Get the name of the Operations STP Hook.
        """
        return 'Auto Release Settlements For NANX BIC Address'

    def IsTriggeredBy(self, eventObject):
        """
        Determine whether or not to trigger the hooks STP action/s
        for an event on the specified object.
        """
        if not eventObject.IsKindOf(acm.FSettlement):
            return False
        settlement = eventObject
        if not settlement.Trade():
            return False
        trade = settlement.Trade()
        account_reference = settlement.CounterpartyAccountRef()
        if not account_reference:
            return False
        bic_address = account_reference.Bic().Name()
        if is_production_environment():
            if bic_address[4:] != 'NANX':
                return False
        elif bic_address[4:] != 'NAN0':
            return False
        if trade.Acquirer().Name() != 'Funding Desk':
            return False
        if settlement.Status() == 'Authorised':
            return False
        if settlement.Type() == 'Call Fixed Rate Adjustable':
            return False
        instrument = trade.Instrument()
        if instrument.InsType() != 'Deposit':
            return False
        if instrument.Currency().Name() != 'ZAR':
            return False
        if not instrument.IsCallAccount():
            return False

        return True

    def PerformSTP(self, eventObject):
        """
        Perform the hooks STP action/s for an event on the specified
        object.

        Release Namibian Settlement
        """

        OperationsSTPFunctions.release_settlement(eventObject)
