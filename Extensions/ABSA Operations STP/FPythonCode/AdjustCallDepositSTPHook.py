"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    AdjustCallDepositSTPHook

DESCRIPTION
    This module contains a hook for STP (straight-through-processing) triggered
    by the adjusting of a call deposit.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-04-18      FAOPS-425       Cuen Edwards            Kgomotso Gumbo          Behaviour migrated from adjust deposit tool with minor
                                                                                improvements.
2019-05-20      FAOPS-474       Cuen Edwards            Nicolette Burger        Addition of holding of settlements for reversals.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm

import OperationsSTPFunctions
from at_logging import getLogger
from OperationsSTPHook import OperationsSTPHook


LOGGER = getLogger(__name__)

CALL_SETTLE_METHOD_ADD_INFO = 'Call_Settle_Method'
SETTLE_TYPE_ADD_INFO = 'Settle_Type'
SETTLE_INSTRUCT_ADD_INFO = 'Settle_Instruct'
REVERSED_CF_REF_ADD_INFO = 'Reversed_CF_Ref'


class AdjustCallDepositSTPHook(OperationsSTPHook):
    """
    Definition of a hook used to perform STP triggered by the
    adjusting of a call deposit.
    """

    def Name(self):
        """
        Get the name of the Operations STP Hook.
        """
        return 'Adjust Call Deposit STP Hook'

    def IsTriggeredBy(self, eventObject):
        """
        Determine whether or not to trigger the hooks STP action/s
        for an event on the specified object.
        """
        if not eventObject.IsKindOf(acm.FSettlement):
            return False
        settlement = eventObject
        if settlement.Status() not in ['Authorised', 'Exception']:
            return False
        cash_flow = settlement.CashFlow()
        if cash_flow is None:
            return False
        if cash_flow.CashFlowType() not in ['Fixed Rate Adjustable', 'Fixed Amount']:
            return False
        instrument = cash_flow.Instrument()
        if instrument.InsType() != 'Deposit':
            return False
        if not instrument.IsCallAccount():
            return False
        if settlement.AddInfoValue(CALL_SETTLE_METHOD_ADD_INFO):
            return False
        return True

    def PerformSTP(self, settlement):
        """
        Perform the hooks STP action/s for an event on the specified
        object.

        Please note that the action does not necessarily occur to the
        event object itself but may occur to some related object/s.
        """
        settlement = settlement.StorageImage()
        # Perform actions that is performed for all adjust deposit settlements.
        self._copy_settle_type_to_settlement(settlement)
        # Perform actions for reinvestments.
        if self._is_reinvestment_settlement(settlement):
            self._perform_reinvestment_stp(settlement)
        # Perform actions for reversals.
        if self._is_reversal_settlement(settlement):
            self._perform_reversal_stp(settlement)
        settlement.Commit()

    def _copy_settle_type_to_settlement(self, settlement):
        """
        Copy the settle type from the cash flow to the settlement.
        """
        cash_flow = settlement.CashFlow()
        settle_type = cash_flow.AddInfoValue(SETTLE_TYPE_ADD_INFO)
        OperationsSTPFunctions.set_additional_info_value(settlement, CALL_SETTLE_METHOD_ADD_INFO, settle_type)

    def _is_reinvestment_settlement(self, settlement):
        """
        Determine whether or not a settlement is for a reinvestment.
        """
        cash_flow = settlement.CashFlow()
        if cash_flow.CashFlowType() != 'Fixed Amount':
            return False
        settle_type = cash_flow.AddInfoValue(SETTLE_TYPE_ADD_INFO)
        return settle_type in [
            'Call to Term',
            'Term To Call: Capital and Interest',
            'Term To Call: Capital',
            'Term To Call: Interest',
            'Term To Call: Partial Capital and Interest',
            'Term To Call: Partial Capital',
            'Term To Multiple'
        ]

    def _perform_reinvestment_stp(self, settlement):
        """
        Perform the STP actions for a reinvestment settlement.
        """
        cash_flow = settlement.CashFlow()
        settle_type = cash_flow.AddInfoValue(SETTLE_TYPE_ADD_INFO)
        OperationsSTPFunctions.set_additional_info_value(settlement, SETTLE_INSTRUCT_ADD_INFO, settle_type)
        if settlement.Status() == 'Authorised':
            self._hold_settlement(settlement)

    def _is_reversal_settlement(self, settlement):
        """
        Determine whether or not a settlement is for a reversal.
        """
        cash_flow = settlement.CashFlow()
        settle_type = cash_flow.AddInfoValue(SETTLE_TYPE_ADD_INFO)
        if settle_type is None:
            return False
        if settle_type.startswith('Backdate: Reversal'):
            return True
        return settle_type == 'Reversal'

    def _perform_reversal_stp(self, settlement):
        """
        Perform the STP actions for a reversal settlement.
        """
        if settlement.Status() == 'Authorised':
            self._hold_settlement(settlement)
        cash_flow = settlement.CashFlow()
        holdable_reversed_settlement = self._get_holdable_reversed_settlement(cash_flow)
        if holdable_reversed_settlement:
            holdable_reversed_settlement = holdable_reversed_settlement.StorageImage()
            self._hold_settlement(holdable_reversed_settlement)
            holdable_reversed_settlement.Commit()

    def _get_holdable_reversed_settlement(self, cash_flow):
        """
        Get any holdable settlement for a reversed cash flow.
        """
        reversed_cf_oid = cash_flow.AddInfoValue(REVERSED_CF_REF_ADD_INFO)
        if not reversed_cf_oid:
            warning_message = "No reversed cash flow referenced by reversal cash flow "
            warning_message += "{reversal_cf_oid}, skipping..."
            LOGGER.warning(warning_message.format(
                reversal_cf_oid=cash_flow.Oid()
            ))
            return None
        reversed_cash_flow = acm.FCashFlow[reversed_cf_oid]
        if not reversed_cash_flow:
            warning_message = "Reversed cash flow {reversed_cf_oid} referenced by reversal "
            warning_message += "cash flow {reversal_cf_oid} does not exist, skipping..."
            LOGGER.warning(warning_message.format(
                reversed_cf_oid=reversed_cf_oid,
                reversal_cf_oid=cash_flow.Oid()
            ))
            return None
        if reversed_cash_flow.Instrument() != cash_flow.Instrument():
            warning_message = "Reversed cash flow {reversed_cf_oid} referenced by reversal "
            warning_message += "cash flow {reversal_cf_oid} does not belong to the same "
            warning_message += "instrument, skipping..."
            LOGGER.warning(warning_message.format(
                reversed_cf_oid=reversed_cf_oid,
                reversal_cf_oid=cash_flow.Oid()
            ))
            return None
        if reversed_cash_flow.CashFlowType() != 'Fixed Amount':
            warning_message = "Reversed cash flow {reversed_cf_oid} referenced by reversal "
            warning_message += "cash flow {reversal_cf_oid} is not a fixed amount cash flow, "
            warning_message += "skipping..."
            LOGGER.warning(warning_message.format(
                reversed_cf_oid=reversed_cf_oid,
                reversal_cf_oid=cash_flow.Oid()
            ))
            return None
        if reversed_cash_flow.PayDate() != cash_flow.PayDate():
            warning_message = "Reversed cash flow {reversed_cf_oid} referenced by reversal "
            warning_message += "cash flow {reversal_cf_oid} is not for the same pay date, "
            warning_message += "skipping..."
            LOGGER.warning(warning_message.format(
                reversed_cf_oid=reversed_cf_oid,
                reversal_cf_oid=cash_flow.Oid()
            ))
            return None
        if not self._amounts_are_equal_and_opposite(reversed_cash_flow.FixedAmount(), cash_flow.FixedAmount()):
            warning_message = "Reversed cash flow {reversed_cf_oid} referenced by reversal "
            warning_message += "cash flow {reversal_cf_oid} is not for the equal and opposite "
            warning_message += "amount, skipping..."
            LOGGER.warning(warning_message.format(
                reversed_cf_oid=reversed_cf_oid,
                reversal_cf_oid=cash_flow.Oid()
            ))
            return None
        select_expression = "cashFlow = {reversed_cash_flow_oid} and status = 'Authorised'".format(
            reversed_cash_flow_oid=reversed_cash_flow.Oid()
        )
        exception_message = "Expecting zero or one settlement for cash flow "
        exception_message += "{reversed_cash_flow_oid} and status 'Authorised'."
        exception_message += exception_message.format(
            reversed_cash_flow_oid=reversed_cash_flow.Oid()
        )
        return acm.FSettlement.Select01(select_expression, exception_message)

    def _amounts_are_equal_and_opposite(self, amount1, amount2):
        """
        Determine if two amounts are equal but with the opposite
        signs.
        """
        if amount1 > 0 and amount2 > 0:
            return False
        if amount1 < 0 and amount2 < 0:
            return False
        sum_of_amounts = amount1 + amount2
        return self._is_almost_zero(sum_of_amounts)

    def _is_almost_zero(self, amount, epsilon=0.009):
        """
        Determine if an amount is 'almost zero'.
        """
        almost_zero = acm.GetFunction('almostZero', 2)
        return almost_zero(abs(amount), epsilon)

    def _hold_settlement(self, settlement):
        """
        Change the status of a settlement to hold.
        """
        LOGGER.info('Holding settlement {settlement_oid}.'.format(
            settlement_oid=settlement.OriginalOrSelf().Oid()
        ))
        settlement.Status('Hold')
