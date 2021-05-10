"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    MatchedAdjustDepositConfirmationSTPHook

DESCRIPTION
    This module contains a hook for STP (straight-through-processing) triggered
    by the matching of an 'Adjust Deposit' confirmation.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-03-26      FAOPS-395       Stuart Wilson           Nicolette Burger        Initial Implementation.
2019-04-08      FAOPS-448       Cuen Edwards            Kgomotso Gumbo          Migrated to Operations STP ATS.
2019-06-04      FAOPS-528       Joash Moodley           Kgomotso Gumbo          Added Fail Safe in case the Confirmation is matched before the settlement is created. 
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm

from at_logging import getLogger
import OperationsSTPFunctions
from OperationsSTPHook import OperationsSTPHook


LOGGER = getLogger(__name__)


class MatchedAdjustDepositConfirmationSTPHook(OperationsSTPHook):
    """
    Definition of a hook used to perform STP triggered by the
    matching of an 'Adjust Deposit' confirmation.
    """

    def Name(self):
        """
        Get the name of the Operations STP Hook.
        """
        return 'Matched Adjust Deposit Confirmation STP Hook'

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
            if not settlement.Instrument().IsCallAccount():
                return False

            confirmations = settlement.Trade().Confirmations()
            for confirmation in confirmations:
                if self._validate_confirmation(confirmation):
                    if settlement.CashFlow() and confirmation.CashFlow():
                        if settlement.CashFlow().Oid() == confirmation.CashFlow().Oid():
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
        adjust_deposit_settlement = self._get_authorised_adjust_deposit_settlement(confirmation)
        if adjust_deposit_settlement is None:
            LOGGER.info('No authorised adjust deposit settlement found, skipping.')
            return
        if self._should_release_settlement(adjust_deposit_settlement):
            LOGGER.info('Adjust deposit settlement {settlement_oid} matches release criteria.'.format(
                settlement_oid=adjust_deposit_settlement.Oid()
            ))
            OperationsSTPFunctions.release_settlement(adjust_deposit_settlement)
        elif self._should_hold_settlement(adjust_deposit_settlement):
            LOGGER.info('Adjust deposit settlement {settlement_oid} matches hold criteria.'.format(
                settlement_oid=adjust_deposit_settlement.Oid()
            ))
            OperationsSTPFunctions.hold_settlement(adjust_deposit_settlement)
        else:
            LOGGER.info('Adjust deposit settlement {settlement_oid} is not eligible for STP, skipping.'.format(
                settlement_oid=adjust_deposit_settlement.Oid()
            ))

    def _get_authorised_adjust_deposit_settlement(self, confirmation):
        """
        Get any authorised settlement related to an 'Adjust Deposit'
        confirmation.
        """
        for settlement in confirmation.Trade().Settlements().AsArray():
            if settlement.Status() != 'Authorised':
                continue
            if settlement.CashFlow() == confirmation.CashFlow():
                return settlement
        return None

    def _should_release_settlement(self, settlement):
        """
        Determine whether or not to change the status of a settlement
        related to a matched 'Adjust Deposit' confirmation to 'Released'.
        """
        bic_address = settlement.CounterpartyAccountRef().Bic().Name()
        if bic_address[4:] == 'NANX':
            return False
        if OperationsSTPFunctions.is_incoming_settlement(settlement):
            return False
        if self._get_cash_flow_settle_type(settlement.CashFlow()) != 'Settle':
            return False
        return True

    def _should_hold_settlement(self, settlement):
        """
        Determine whether or not to change the status of a settlement
        related to a matched 'Adjust Deposit' confirmation to 'Hold'.
        """
        cash_flow_settle_type = self._get_cash_flow_settle_type(settlement.CashFlow())
        if cash_flow_settle_type in ['Reversal', 'Internal', 'Square Off']:
            return True
        if cash_flow_settle_type == 'Settle':
            return OperationsSTPFunctions.is_incoming_settlement(settlement)
        return False

    def _get_cash_flow_settle_type(self, cash_flow):
        """
        Get the settle type additional info value of a cash flow.
        """
        return cash_flow.AddInfoValue('Settle_Type')
    
    def _validate_confirmation(self, confirmation):
        """
        Check if confirmation is valid for STP
        """

        if confirmation.Status() != 'Matched':
            return False
        if confirmation.EventChlItem().Name() != 'Adjust Deposit':
            return False
        if confirmation.Transport() not in ['Email', 'File']:
            return False
        cashFlow = confirmation.CashFlow()
        if cashFlow.CashFlowType() != 'Fixed Amount':
            return False
        trade = confirmation.Trade()
        if trade.Status() not in ['BO Confirmed', 'BO-BO Confirmed']:
            return False
        if trade.Acquirer().Name() != 'Funding Desk':
            return False
        instrument = trade.Instrument()
        if instrument.InsType() != 'Deposit':
            return False
        if not instrument.IsCallAccount():
            return False
        if instrument.Currency().Name() != 'ZAR':
            return False
        return True
