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
2020-10-21      FAOPS-959       Ncediso Nkambule        Cuen Edwards            Initial create.
2020-10-21      FAOPS-1016      Ncediso Nkambule        Gasant Thulsie          Updated Hook Logger with Hook Name.
2021-03-16      FAOPS-982       Ncediso Nkambule        Gasant Thulsie          Added functions to handle Cashflow driven events.

------------------------------------------------------------------------------------------------------------------------
"""

import acm
from at_logging import getLogger
import sbl_booking_utils as sbl_utils
from NeoXActivityReportHook import ActivityReportsNeoxHook
from NeoXActivityReportsHookBase import CollateralTradeToReport
from NeoXActivityReportsUtils import is_valid_sbl_collateral_trade, get_object_value_by_name


LOGGER = getLogger(__name__)


class SBLCollateralActivityHook(ActivityReportsNeoxHook):
    """
    Definition of a hook used to perform STP triggered by the update or creation of a fixed cash flow on a SBL trade.
    """

    file_identifier = "Collateral_Trade_Activity"

    def Name(self):
        """
        Get the name of the SBL Collateral Activity NeoX Hook.
        """
        return 'SBL Collateral Activity NeoX Hook'

    def IsTriggeredBy(self, event_object, event_message=None):
        """
        Only trigger for the belo matched conditions.
        Other Collateral Trades:
          - Instrument Type in ["Stock", "Bond", "IndexLinkedBond", "CD", "Bill"]
          - Trade Portfolio matches SBL_NONCASH_COLLATERAL
          - Trade Category equals "Collateral"
          - Trade Acquirer equals to SECURITY LENDINGS DESK
          - Trade Counterparty startswith 'SL'
        """

        instrument = None
        trade = self.get_trade_from_event_object(event_object)

        if trade:
            instrument = trade.Instrument()
        if trade and not trade.Acquirer().Name() == sbl_utils.ACQUIRER.Name():
            return False
        if instrument and not instrument.InsType() in sbl_utils.SBL_INSTRUMENTS:
            return False
        if not self._is_collateral_trade(trade):
            return False
        if not is_valid_sbl_collateral_trade(trade):
            return False

        return True

    def PerformEventProcessing(self, event_object, event_message=None):
        """
        Perform the hooks STP action/s for an event on the specified
        object.

        Please note that the action does not necessarily occur to the
        event object itself but may occur to some related object/s.
        """

        message_id = get_object_value_by_name(event_message, 'TXNBR')
        try:
            if event_object.IsKindOf(acm.FTrade):
                LOGGER.info("Processing Collateral Trade Update")
                trade = self.get_trade_from_event_object(event_object)
                if trade:
                    with CollateralTradeToReport(
                            directory=self.temp_directory,
                            file_name=self.file_identifier,
                            acm_trade=trade) as collateral:
                        collateral.process_trade(message_id)
        except Exception as error:
            LOGGER.exception(error)

    def PerformFileProcessing(self):
        with CollateralTradeToReport(
                directory=self.temp_directory,
                file_name=self.file_identifier,
                acm_trade=None) as collateral:
            collateral.move_file(destination_directory=self.final_directory)

    @staticmethod
    def _is_collateral_trade(trade):
        if not trade:
            return False
        if not trade.match_portfolio(sbl_utils.COLLATERAL_PORTFOLIO):
            return False
        if not trade.TradeCategory() == sbl_utils.COLLATERAL_CATEGORY:
            return False
        if not trade.Instrument().InsType() in sbl_utils.COLLATERAL_INSTRUMENTS:
            return False
        return True
