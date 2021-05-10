"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    SSAPremiumNettingSTPHook

DESCRIPTION
    This module contains a hook for netting of MT222 Settlements for Bill / Bond

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date         Change no              Developer               Requester            Description
-----------------------------------------------------------------------------------------------------------------------------------------
22-03-2019   FAOPS-659    Joash Moodley           Kgomotso Gumbo                 Generate MT202's for SSA MT54x securities Funding      

-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm

from at_logging import getLogger
import OperationsSTPFunctions
from OperationsSTPHook import OperationsSTPHook


LOGGER = getLogger(__name__)

TRADE_SETTLE_CATEGORIES = [
    'SSA_BWP_ALL_Custodian',
    'SSA_GHS_ALL_Custodian',
    'SSA_KES_ALL_Custodian',
    'SSA_MUR_ALL_Custodian',
    'SSA_UGX_ALL_Custodian',
    'SSA_ZMW_ALL_Custodian'
]


class SSAPremiumNettingSTPHook(OperationsSTPHook):
    """
    Definition of a hook used to perform Netting for SSA Premium
    """

    def Name(self):
        """
        Get the name of the Operations STP Hook.
        """
        return 'SSA Premium Netting'

    def IsTriggeredBy(self, eventObject):
        """
        Determine whether or not to trigger the hooks STP action/s
        for an event on the specified object.
        """
        if eventObject.IsKindOf(acm.FSettlement):

            settlement = eventObject
            if not settlement.Trade():
                return False
            if settlement.Currency().Name() == 'ZAR':
                return False
            if not settlement.Trade():
                return False
            if settlement.Trade().Nominal() < 0:
                return False
            if 'ATS' not in settlement.UpdateUser().Name():
                return False
            if settlement.Instrument().InsType() in ["Bill", "Bond"]:
                LOGGER.debug('InsType : {ins_type}'.format(ins_type=settlement.Instrument().InsType()))
                if settlement.Status() == 'Authorised':
                    if settlement.Type() in ['Broker Fee', 'Premium', 'Payment Premium']:
                        if settlement.Trade().Status() == 'BO Confirmed':
                            trade_settle_category = settlement.Trade().SettleCategoryChlItem().Name()
                            if trade_settle_category and trade_settle_category in TRADE_SETTLE_CATEGORIES:
                                if settlement.MTMessages() == '222':
                                    LOGGER.debug('Valid Settlement for MT222 Net')
                                    return True
        return False



    def PerformSTP(self, eventObject):
        """
        Perform the hooks STP action/s for an event on the specified
        object.

        Please note that the action does not necessarily occur to the
        event object itself but may occur to some related object/s.
        """
        settlement = None
        
        if eventObject.IsKindOf(acm.FSettlement):
            settlement = eventObject

        if self.net_settlements(settlement):
            LOGGER.info('Netting For SSA Trade')

    def _get_valid_settlements_to_net(self, settlements, allow_types):
        settlements_to_net = []
        for settlement in settlements:
            if settlement.Type()  == None:
                return []
            if settlement.Status() == 'Authorised' and settlement.Type() in allow_types:
                LOGGER.debug('settlement type : {type}'.format(type=settlement.Type()))
                settlements_to_net.append(settlement)
        return settlements_to_net       


    def net_settlements(self, settlement):
        if not settlement or not settlement.Trade():
            return False
        LOGGER.info('checking for valid settlement type')
        allow_types = ['Broker Fee', 'Premium', 'Payment Premium']
        settlements = settlement.Trade().Settlements().AsArray()
        settlements_to_net = self._get_valid_settlements_to_net(
            settlements,
            allow_types
        )

        if len(settlements_to_net) > 1:
            OperationsSTPFunctions.net_settlements(settlements_to_net)
            return True

        LOGGER.info('Not Valid Net Payment')
        return False

