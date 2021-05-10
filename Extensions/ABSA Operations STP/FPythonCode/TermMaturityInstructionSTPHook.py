"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    TermMaturityInstructionSTPHook

DESCRIPTION
    This module contains a hook for STP (straight-through-processing) triggered
    by the setting of a maturity instruction on a term deposit.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-04-18      FAOPS-425       Cuen Edwards            Kgomotso Gumbo          Behaviour migrated from trade instruction tool with minor
                                                                                improvements.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm

import OperationsSTPFunctions
from at_logging import getLogger
from OperationsSTPHook import OperationsSTPHook


LOGGER = getLogger(__name__)


class TermMaturityInstructionSTPHook(OperationsSTPHook):
    """
    Definition of a hook used to perform STP triggered by the
    setting of a maturity instruction on a term deposit.
    """

    def Name(self):
        """
        Get the name of the Operations STP Hook.
        """
        return 'Term Maturity Instruction STP Hook'

    def IsTriggeredBy(self, eventObject):
        """
        Determine whether or not to trigger the hooks STP action/s
        for an event on the specified object.
        """
        if not eventObject.IsKindOf(acm.FInstrument):
            return False
        instrument = eventObject
        if instrument.InsType() not in ['Deposit', 'FRN']:
            return False
        if instrument.IsCallAccount():
            return False
        if instrument.ExpiryDateOnly() != acm.Time.DateToday():
            return False
        return True

    def PerformSTP(self, instrument):
        """
        Perform the hooks STP action/s for an event on the specified
        object.

        Please note that the action does not necessarily occur to the
        event object itself but may occur to some related object/s.
        """
        maturing_cash_flows = self.get_maturing_cash_flows(instrument)
        if not maturing_cash_flows:
            LOGGER.info('No maturing cash flows found, skipping.')
            return
        for cash_flow in maturing_cash_flows:
            if cash_flow.CashFlowType() not in ['Fixed Amount', 'Fixed Rate', 'Float Rate']:
                message = "Maturing cash flow {cash_flow_oid} of type '{cash_flow_type}' found, skipping."
                LOGGER.info(message.format(
                    cash_flow_oid=cash_flow.Oid(),
                    cash_flow_type=cash_flow.CashFlowType()
                ))
                continue
            settle_type_addinfo_name = 'Settle_Type'
            settle_type = cash_flow.AddInfoValue(settle_type_addinfo_name)
            if not settle_type:
                message = "Additional info '{addinfo_name}' not set on maturing cash flow {cash_flow_oid}, "
                message += "skipping."
                LOGGER.info(message.format(
                    addinfo_name=settle_type_addinfo_name,
                    cash_flow_oid=cash_flow.Oid()
                ))
                continue
            settlements = self._get_cash_flow_settlements(cash_flow)
            if not settlements:
                LOGGER.info('No settlements found for maturing cash flow {cash_flow_oid}, skipping.'.format(
                    cash_flow_oid=cash_flow.Oid()
                ))
                continue
            for settlement in settlements:
                if settlement.Status() not in ['Authorised', 'Exception']:
                    message = "Settlement {settlement_oid} for maturing cash flow {cash_flow_oid} not in "
                    message += "'Authorised' or 'Exception' status, skipping."
                    LOGGER.info(message.format(
                        settlement_oid=settlement.Oid(),
                        cash_flow_oid=cash_flow.Oid()
                    ))
                    continue
                settle_instruct_addinfo_name = 'Settle_Instruct'
                current_settle_instruct = settlement.AddInfoValue(settle_instruct_addinfo_name)
                if current_settle_instruct:
                    message = "Settlement {settlement_oid} for maturing cash flow {cash_flow_oid} already "
                    message += "has additional info '{addinfo_name}' set, skipping."
                    LOGGER.info(message.format(
                        settlement_oid=settlement.Oid(),
                        cash_flow_oid=cash_flow.Oid(),
                        addinfo_name=settle_instruct_addinfo_name
                    ))
                    continue
                LOGGER.info('Processing settlement {settlement_oid} for maturing cash flow {cash_flow_oid}.'.format(
                    settlement_oid=settlement.Oid(),
                    cash_flow_oid=cash_flow.Oid()
                ))
                settlement = settlement.StorageImage()
                # Set Settle_Instruct.
                OperationsSTPFunctions.set_additional_info_value(settlement, settle_instruct_addinfo_name, settle_type)
                # Set Sett_Status_Update.
                OperationsSTPFunctions.set_additional_info_value(settlement, 'Sett_Status_Update', True)
                # Set Settle Amount (if specified).
                settle_amount = cash_flow.AddInfoValue('Settle_Amount')
                if settle_amount:
                    OperationsSTPFunctions.set_additional_info_value(settlement, 'Partial_Amount', settle_amount)
                # Hold settlement if applicable.
                if self._should_hold_settlement(settlement, settle_type):
                    self._hold_settlement(settlement)
                settlement.Commit()

    def get_maturing_cash_flows(self, instrument):
        """
        Get any cash flows maturing (paying out) today.
        """
        maturing_cash_flows = list()
        today = acm.Time.DateToday()
        for cash_flow in instrument.MainLeg().CashFlows().AsArray():
            if cash_flow.PayDate() != today:
                continue
            maturing_cash_flows.append(cash_flow)
        return maturing_cash_flows

    def _get_cash_flow_settlements(self, cash_flow):
        """
        Get any settlements for a cash flow.
        """
        select_expression = 'cashFlow = {cash_flow_oid}'.format(
            cash_flow_oid=cash_flow.Oid()
        )
        return acm.FSettlement.Select(select_expression).AsArray()

    def _should_hold_settlement(self, settlement, settle_type):
        """
        Determine whether or not a settle_type value should result in
        a settlement being set to hold.
        """
        if settlement.Status() != 'Authorised':
            return False
        cash_flow_type = settlement.CashFlow().CashFlowType()
        if cash_flow_type == 'Fixed Amount':
            return self._should_hold_capital_settlement(settle_type)
        elif cash_flow_type in ['Fixed Rate', 'Float Rate']:
            return self._should_hold_interest_settlement(settle_type)
        raise ValueError("Unsupported settlement for cash flow type '{cash_flow_type}' specified.".format(
            cash_flow_type=cash_flow_type
        ))

    def _should_hold_capital_settlement(self, settle_type):
        """
        Determine whether or not to hold a capital settlement for a
        specified settle_type.
        """
        return settle_type in [
            "Term To Term: Capital and Interest",
            "Term To Term: Capital",
            "Term To Term: Partial Capital and Interest",
            "Term To Term: Partial Capital",
            "Term To Call: Capital and Interest",
            "Term To Call: Capital",
            "Term To Call: Partial Capital and Interest",
            "Term To Call: Partial Capital",
            "Term To Multiple",
            "Pay Out : Interest"
        ]

    def _should_hold_interest_settlement(self, settle_type):
        """
        Determine whether or not to hold a interest settlement for a
        specified settle_type
        """
        return settle_type in [
            "Term To Term: Capital and Interest",
            "Term To Term: Interest",
            "Term To Term: Partial Capital and Interest",
            "Term To Call: Capital and Interest",
            "Term To Call: Interest",
            "Term To Call: Partial Capital and Interest",
            "Term To Multiple",
            "Pay Out : Capital"
        ]

    def _hold_settlement(self, settlement):
        """
        Change the status of a settlement to hold.
        """
        LOGGER.info('Holding settlement {settlement_oid}.'.format(
            settlement_oid=settlement.OriginalOrSelf().Oid()
        ))
        settlement.Status('Hold')
