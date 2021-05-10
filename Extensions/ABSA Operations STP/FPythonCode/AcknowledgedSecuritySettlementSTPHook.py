"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    AcknowledgedSecuritySettlementSTPHook

DESCRIPTION
    This module contains a hook for STP (straight-through-processing) triggered
    by the acknowledgement of a security settlement.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2020-04-29      FAOPS-700       Cuen Edwards            Kgomotso Gumbo          Migration of functionality from FValidation and addition
                                                                                of support for netted settlements.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm

from at_logging import getLogger
import OperationsSTPFunctions
from OperationsSTPHook import OperationsSTPHook


LOGGER = getLogger(__name__)


class AcknowledgedSecuritySettlementSTPHook(OperationsSTPHook):
    """
    Definition of a hook used to perform STP triggered by the
    acknowledgement of a security settlement.
    """

    def Name(self):
        """
        Get the name of the Operations STP Hook.
        """
        return 'Acknowledged Security Settlement STP Hook'

    def IsTriggeredBy(self, eventObject):
        """
        Determine whether or not to trigger the hooks STP action/s
        for an event on the specified object.
        """
        if not eventObject.IsKindOf(acm.FSettlement):
            return False
        settlement = eventObject
        if settlement.Status() != 'Acknowledged':
            return False
        if settlement.AccountType() != 'Security':
            return False
        if len(self._get_bo_confirmable_trades(settlement)) == 0:
            return False
        return True

    def PerformSTP(self, settlement):
        """
        Perform the hooks STP action/s for an event on the specified
        object.

        Please note that the action does not necessarily occur to the
        event object itself but may occur to some related object/s.
        """
        for trade in self._get_bo_confirmable_trades(settlement):
            OperationsSTPFunctions.bo_confirm_trade(trade)

    @classmethod
    def _get_bo_confirmable_trades(cls, settlement):
        """
        Get any trades related to the specified settlement that
        should be automatically BO Confirmed.
        """
        bo_confirmable_trades = set()
        trade = settlement.Trade()
        if trade is not None:
            if cls._is_bo_confirmable_trade(trade):
                bo_confirmable_trades.add(trade)
        for child_settlement in settlement.Children():
            bo_confirmable_trades.update(cls._get_bo_confirmable_trades(child_settlement))
        return bo_confirmable_trades

    @classmethod
    def _is_bo_confirmable_trade(cls, trade):
        """
        Determine whether or not the specified trade is eligible for
        automatic BO Confirming.
        """
        if trade.Status() != 'FO Confirmed':
            return False
        trade_settle_category = trade.SettleCategoryChlItem()
        if trade_settle_category is None:
            return False
        if trade_settle_category.Name() == 'SA_CUSTODIAN':
            # Only auto-bo-confirm security transfer trades.
            trad_area = trade.OptKey1()
            if trad_area is None:
                return False
            return trad_area.Name() in ['Internal Transfer', 'External Transfer', 'SARB Transfer']
        if trade_settle_category.Name() == 'Euroclear':
            # Auto-bo-confirm FICC trades.
            return True
        if trade_settle_category.Name().startswith('SSA_'):
            # Auto-bo-confirm SSA trades.
            return True
        return False
