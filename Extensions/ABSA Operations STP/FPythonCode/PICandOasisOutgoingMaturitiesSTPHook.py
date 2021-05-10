"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    PICandOasisOutgoingMaturitiesSTPHook

DESCRIPTION
    This module contains a hook for STP (straight-through-processing) triggered
    by the matching of Zar Maturity Notice confirmation.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-11-21      FAOPS-635       Tawanda Mukhalela       Wandile Sithole         PIC and Oasis Zar Deposits Autorelease on Matched Maturity
                                                                                Notice
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm

from at_logging import getLogger
import OperationsSTPFunctions
from OperationsSTPHook import OperationsSTPHook


LOGGER = getLogger(__name__)


class PICandOasisOutgoingMaturitiesSTPHook(OperationsSTPHook):
    """
    Definition of a hook used to perform STP triggered by the
    matching of a Zar Maturity Notice confirmation.
    """

    # noinspection PyPep8Naming
    def Name(self):
        """
        Get the name of the Operations STP Hook.
        """
        return 'PIC and Oasis Outgoing Maturities STP Hook'

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
        netting_rules = [rule_link
                         for rule_link in trade.Counterparty().NettingRuleLinks()
                         if rule_link.NettingRule().Name() == 'Zar Maturity Nett'
                         ]
        netting_rule = netting_rules[0] if len(netting_rules) >= 1 else None
        today = acm.Time.DateToday()
        for settlement in trade.Settlements().AsArray():
            if not self._is_valid_settlement(settlement):
                continue
            if settlement.ValueDay() == today and netting_rule:
                OperationsSTPFunctions.release_settlement(settlement)
                message = 'Released Zar Maturity Settlement : {settlement} for Trade : {trade}'
                LOGGER.info(message.format(settlement=settlement.Oid(), trade=settlement.Trade().Oid()))

    @staticmethod
    def is_valid_confirmation(eventObject):
        """
        Check Confirmation Validity
        """
        confirmation = eventObject
        if confirmation.Status() != 'Matched':
            return False
        if confirmation.EventChlItem().Name() != 'Maturity Notice':
            return False
        trade = confirmation.Trade()
        if trade.Acquirer().Name() != 'Funding Desk':
            return False
        instrument = trade.Instrument()
        if instrument.InsType() != 'Deposit':
            return False
        if instrument.Currency().Name() != 'ZAR':
            return False

        return True

    @staticmethod
    def _is_valid_settlement(settlement):
        """
        Check Settlement Validity
        """
        if settlement.Status() != 'Authorised':
            return False
        if OperationsSTPFunctions.is_incoming_settlement(settlement):
            return False
        if settlement.Type() != 'None':
            return False

        return True
