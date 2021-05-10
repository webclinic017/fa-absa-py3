"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    DematSTPAutoReleaseHook

DESCRIPTION
    This module contains a hook for auto releasing demat settlements.

------------------------------------------------------------------------------------------------------------------------
HISTORY
========================================================================================================================
Date            Change no           Developer               Requester               Description
------------------------------------------------------------------------------------------------------------------------
15/01/2020      FAOPS-631           Joash Moodley           Kgomotso Gumbo          Auto Release Demat Settlements
                                                                                    as apart of postprocessingats decom.
03/08/2020      FAOPS-850           Tawanda Mukhalela       Linda Breytenbach       Removed STP for Money Market
                                                                                    and Funding Desk
09/11/2020      FAOPS-931           Tawanda Mukhalela       Linda Breytenbach       Added Support for MT298 settlements
------------------------------------------------------------------------------------------------------------------------
"""

import acm

from at_logging import getLogger
import OperationsSTPFunctions
from OperationsSTPHook import OperationsSTPHook

LOGGER = getLogger(__name__)

ALLOWED_ACQUIRERS = (
    'IMPUMELELO SERIES 1', 'IMPUMELELO SERIES 1 ACQUIRER',
    'IMPUMELELO SERIES 2', 'IMPUMELELO SERIES 2 ACQUIRER',
    'IMPUMELELO', 'Funding Desk', 'Money Market Desk', 'MONEY MARKET DESK'
)

FUNDING_ACQUIRERS = ('Funding Desk', 'Money Market Desk', 'MONEY MARKET DESK')


def check_for_stand_alone_payment(settlement):
    if settlement.Type() == 'Stand Alone Payment':
        LOGGER.info('{sett_id} is a Stand Alone Payment...checking for MT202 doc type'.format(
                sett_id=settlement.Oid()))
        if str(settlement.MTMessages()) == '202':
            return True
    return False


def check_demat_payment(settlement, trade, instrument):
    LOGGER.info('checking if {sett_id}  is a valid demat payment'.format(
                sett_id=settlement.Oid()))
    today = acm.Time.DateToday()
    last_month = acm.Time.DateAdjustPeriod(today, '-1m')
    if trade.Premium() > 0:
        return False
    if instrument.InsType() not in ('Bill', 'CD', 'FRN'):
        return False
    if trade.AdditionalInfo().Demat_Deliv_vs_Paym() is True:
        if settlement.CreateDay() >= last_month:
            if settlement.CreateDay() <= today:
                return True

    return False


class DematSTPAutoReleaseHook(OperationsSTPHook):
    """
    Definition of a hook used to perform Auto Releasing of Demat Settlements
    """

    def Name(self):
        """
        Get the name of the Operations STP Hook.
        """
        return 'Auto Release Demat Settlements'

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
        instrument = trade.Instrument()
        if settlement.Status() != 'Authorised':
            return False

        if not instrument.AdditionalInfo().Demat_Instrument():
            return False

        if trade.Acquirer().Name() not in ALLOWED_ACQUIRERS:
            return False

        if settlement.Type() == 'Premium' and trade.Acquirer().Name() in FUNDING_ACQUIRERS:
            return False

        if check_for_stand_alone_payment(settlement):
            LOGGER.info(
                'MT202 doc type found for {sett_id}'.format(sett_id=settlement.Oid())
            )
            return True
        elif check_demat_payment(settlement, trade, instrument):
            LOGGER.info(
                '{sett_id} is a valid demat payment'.format(sett_id=settlement.Oid())
            )
            return True

        return False

    def PerformSTP(self, eventObject):
        """
        Perform the hooks STP action/s for an event on the specified
        object.

        Please note that the action does not necessarily occur to the
        event object itself but may occur to some related object/s.
        """
        
        if eventObject.IsKindOf(acm.FSettlement):
            settlement = eventObject
            LOGGER.info('Performing STP for Demat Settlement')
            OperationsSTPFunctions.release_settlement(settlement)


class AuthoriseMT298STPHook(OperationsSTPHook):
    """
    STP Hook for Authorising MT298 Settlements
    """

    def Name(self):
        """
        Name of the hook
        """
        return 'Authorise MT298 Settlement on 202 Acknowledgement'

    def IsTriggeredBy(self, eventObject):
        """
        Check if event object qualifies for Authorising the MT298 Settlement
        """
        if not eventObject.IsKindOf(acm.FSettlement):
            return False
        settlement = eventObject
        if not settlement.Trade():
            return False
        instrument = settlement.Trade().Instrument()
        if not instrument.AdditionalInfo().Demat_Instrument():
            return False
        if settlement.Type() != 'Stand Alone Payment':
            return False
        if settlement.Status() != 'Acknowledged':
            return False
        if not self._related_mt298_is_hold(settlement):
            return False

        return True

    def PerformSTP(self, settlement):
        """
        Authorise MT298 Settlement
        """
        related_settlements = self._get_related_mt298(settlement)
        for mt298_settlement in related_settlements:
            OperationsSTPFunctions.authorise_settlement(mt298_settlement)

    def _related_mt298_is_hold(self, settlement):
        """
        Validates the related 298
        """
        related_settlements = self._get_related_mt298(settlement)
        if related_settlements:
            return True

        return False

    @staticmethod
    def _get_related_mt298(settlement):
        """
        gets the related MT298 settlement
        """
        trade = settlement.Trade()
        cash_flow = settlement.CashFlow()
        trade_settlements = trade.Settlements()
        qualifying_settlements = list()
        for _settlement in trade_settlements:
            if _settlement.CashFlow() != cash_flow:
                continue
            if _settlement.Status() != 'Hold':
                continue
            if ':910' not in _settlement.AdditionalInfo().Call_Confirmation():
                continue
            qualifying_settlements.append(_settlement)

        if len(qualifying_settlements) > 0:
            return qualifying_settlements

        return None
