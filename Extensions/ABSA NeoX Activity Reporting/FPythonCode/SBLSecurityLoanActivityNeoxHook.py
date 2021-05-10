"""---------------------------------------------------------------------------------------------------------------------
MODULE
    SBLSecurityLoanActivityNeoxHook

DESCRIPTION
    This module contains STP logic to terminate manually settled full returns.

------------------------------------------------------------------------------------------------------------------------
HISTORY
========================================================================================================================
Date            Change no        Developer            Requester               Description
------------------------------------------------------------------------------------------------------------------------
2020-10-21      FAOPS-959        Ncediso Nkambule     Cuen Edwards            Initial implementation.
2020-10-21      FAOPS-1016       Ncediso Nkambule     Gasant Thulsie          Updated Hook Logger with Hook Name.
2021-03-16      FAOPS-982        Ncediso Nkambule     Gasant Thulsie          Added functions to handle Cashflow driven events.

------------------------------------------------------------------------------------------------------------------------
"""

import acm
from at_logging import getLogger
import NeoXActivityReportsConstants as Constants
from NeoXActivityReportHook import ActivityReportsNeoxHook
from NeoXActivityReportsHookBase import SecurityLoanTradeToReport
from NeoXActivityReportsUtils import is_valid_sbl_loan_trade, get_object_value_by_name


LOGGER = getLogger(__name__)


class SBLSecurityLoansActivityNeoxHook(ActivityReportsNeoxHook):
    """
    Definition of a hook used to perform STP triggered
    by creation of a Collateral or SBL trade in FO Confirmed status.
    """

    file_identifier = "SBL_Trade_Activity"

    def Name(self):
        """
        Get the name of the SBL Security Loans Activity Neox Hoo.
        """
        return "SBL Security Loans Activity Neox Hook"

    def IsTriggeredBy(self, event_object, event_message=None):

        if event_object.IsKindOf(acm.FSettlement) and not self.is_valid_sbl_settlement(event_object):
            return False
        if event_object.IsKindOf(acm.FSettlement):
            return False

        trade = self.get_trade_from_event_object(event_object)
        if trade and not is_valid_sbl_loan_trade(trade):
            return False
        return True

    def PerformEventProcessing(self, event_object, event_message=None):
        """
        Auto BO Confirm trades that meet the above criteria
        """
        message_id = get_object_value_by_name(event_message, 'TXNBR')
        if event_object.IsKindOf(acm.FTrade):
            LOGGER.info("Processing SecurityLoan Trade Update")
            trade = self.get_trade_from_event_object(event_object)
            if trade:
                with SecurityLoanTradeToReport(
                        directory=self.temp_directory,
                        file_name=self.file_identifier,
                        acm_trade=trade) as sec_loan:
                    sec_loan.process_trade(message_id)
        elif event_object.IsKindOf(acm.FInstrument) and event_object.InsType() == Constants.LOAN_INS_TYPE:
            LOGGER.info("Processing SecurityLoan Instrument Update")
            trades = [trade for trade in event_object.Trades() if is_valid_sbl_loan_trade(trade)]
            for trade in trades:
                with SecurityLoanTradeToReport(
                        directory=self.temp_directory,
                        file_name=self.file_identifier,
                        acm_trade=trade,
                        is_instrument_update=True) as collateral:
                    collateral.process_trade(message_id)

    def PerformFileProcessing(self):
        with SecurityLoanTradeToReport(
                directory=self.temp_directory,
                file_name=self.file_identifier,
                acm_trade=None) as sec_loan:
            sec_loan.move_file(destination_directory=self.final_directory)

    @staticmethod
    def is_valid_sbl_settlement(event_object):
        """
        Checks if given settlement is a valid settlement
        for the SBL Business
        """
        trade = event_object.Trade()
        if not trade:
            return False
        acquirer = trade.Acquirer().Name()
        instrument = trade.Instrument().InsType()
        if instrument != "SecurityLoan":
            return False
        if acquirer != "SECURITY LENDINGS DESK":
            return False
        if not trade.Status() in Constants.VALID_TRADE_STATUS:
            return False
        if event_object.Type() not in ["Security Nominal", "End Security"]:
            return False
        return True

    @staticmethod
    def is_settled(trade):
        """
        returns True if any of the loan Security Settlements are Settled
        """
        end_security_settled = False
        security_nominal_settled = False
        settlements = trade.Settlements().AsArray()
        if settlements:
            if trade.add_info("SL_SWIFT") == "DOM":
                for settlement in settlements:
                    if settlement.Status() == "Settled":
                        return True
            elif trade.add_info("SL_SWIFT") == "SWIFT":
                for settlement in settlements:
                    if settlement.Type() == "Security Nominal" and settlement.Status() == "Settled":
                        security_nominal_settled = True
                    elif settlement.Type() == "End Security" and settlement.Status() == "Settled":
                        end_security_settled = True
                if end_security_settled and security_nominal_settled:
                    return True
        return False
