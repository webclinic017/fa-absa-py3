"""---------------------------------------------------------------------------------------------------------------------
MODULE
    SBLCollateralActivityNeoxHook
    Hook

DESCRIPTION
    This module contains Neox logic for the SBL Collateral trades.

------------------------------------------------------------------------------------------------------------------------
HISTORY
========================================================================================================================
Date            Change no       Developer               Requester               Description
------------------------------------------------------------------------------------------------------------------------
2021-03-16      FAOPS-982       Ncediso Nkambule        Gasant Thulsie          Initial create.

------------------------------------------------------------------------------------------------------------------------
"""

import acm
from at_logging import getLogger
import sbl_booking_utils as sbl_utils
from NeoXActivityReportHook import ActivityReportsNeoxHook
from NeoXActivityReportsHookBase import CashCollateralCashFlowToReport
import NeoXActivityReportsUtils as NeoXUtils


LOGGER = getLogger(__name__)


class SBLCashCollateralActivityHook(ActivityReportsNeoxHook):
    """
    Definition of a hook used to perform STP triggered by the update or creation of a fixed cash flow on a SBL trade.
    """

    file_identifier = "Cash_Collateral_Trade_Activity"

    def Name(self):
        """
        Get the name of the SBL Cash Collateral Activity NeoX Hook.
        """
        return 'SBL Cash Collateral Activity NeoX Hook'

    def IsTriggeredBy(self, event_object, event_message=None):
        """
        Only trigger for the belo matched conditions.
        Cash Collateral Trades:
          - Trade External ID not None
          - Instrument Type is Call Deposit
          - Trade Portfolio equals to Call_SBL_Agency_Collateral
          - Instrument OpenEnd Status equals to Open End
          - Trade Acquirer equals to PRIME SERVICES DESK
        """

        instrument = None
        trade = self.get_trade_from_event_object(event_object)

        if event_object.IsKindOf(acm.FInstrument):
            instrument = event_object
            trade = NeoXUtils.get_trade_related_to_instrument(event_object)

        if trade is None:
            return False

        if trade.Status() != 'BO Confirmed':
            return False

        if instrument and not instrument.InsType() in sbl_utils.CASH_COLLATERAL_INS_TYPES:
            return False

        if NeoXUtils.is_valid_cash_collateral_trade(trade) is False:
            return False

        if NeoXUtils.has_updated_cashflows(event_message, "Fixed Amount") is False:
            return False

        return True

    def PerformEventProcessing(self, event_object, event_message=None):
        """
        Perform the hooks STP action/s for an event on the specified
        object.

        Please note that the action does not necessarily occur to the
        event object itself but may occur to some related object/s.
        """
        LOGGER.info("Processing Cash Collateral Trade/Instrument/CashFlow Update")
        message_id = NeoXUtils.get_object_value_by_name(event_message, 'TXNBR')
        updated_cashflows = NeoXUtils.get_touched_cashflows(event_message)
        for item in updated_cashflows:
            cashflow_id = NeoXUtils.get_object_value_by_name(item, 'CFWNBR')
            cashflow = acm.FCashFlow[cashflow_id]
            is_delete_operation = NeoXUtils.is_deleted_object(item)
            try:
                trade = None
                if event_object.IsKindOf(acm.FTrade):
                    trade = event_object
                if event_object.IsKindOf(acm.FDeposit):
                    trade = NeoXUtils.get_trade_related_to_instrument(event_object)
                if trade:
                    with CashCollateralCashFlowToReport(
                            directory=self.temp_directory,
                            file_name=self.file_identifier,
                            acm_cash_flow=cashflow) as collateral:
                        collateral.process_cash_flow(message_id, is_delete=is_delete_operation)
            except Exception as error:
                LOGGER.exception(error)

    def PerformFileProcessing(self):
        with CashCollateralCashFlowToReport(
                directory=self.temp_directory,
                file_name=self.file_identifier,
                acm_cash_flow=None) as collateral:
            collateral.move_file(destination_directory=self.final_directory)
