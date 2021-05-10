"""---------------------------------------------------------------------------------------------------------------------
MODULE
    SBLSecurityLoanUpdateSTPHook

DESCRIPTION
    This module contains STP logic to terminate manually settled full returns.

------------------------------------------------------------------------------------------------------------------------
HISTORY
========================================================================================================================
Date            Change no        Developer            Requester               Description
------------------------------------------------------------------------------------------------------------------------
2020-07-23      PCGDEV-532       Sihle Gaxa           James Stevens           Initial implementation.

------------------------------------------------------------------------------------------------------------------------
"""
import acm

import OperationsSTPFunctions

from at_logging import getLogger
from OperationsSTPHook import OperationsSTPHook

LOGGER = getLogger(__name__)
VALID_TRADE_STATUS = ["BO Confirmed", "BO-BO Confirmed"]


class SBLTerminateFullReturnSTPHook(OperationsSTPHook):
    """
    Definition of a hook used to perform STP triggered
    by creation of a Collateral or SBL trade in FO Confirmed status.
    """

    def Name(self):
        """
        Get the name of the Operations STP Hook.
        """
        return "SBL Terminate Full Return STP Hook"


    def IsTriggeredBy(self, eventObject):

        if not eventObject.IsKindOf(acm.FSettlement):
            return False

        if not self.is_valid_sbl_settlement(eventObject):
            return False

        if not eventObject.UpdateUser().UserGroup().Name() in ["IT RTB", "OPS SecLend"]:
            return False

        trade = eventObject.Trade()
        if not (trade.Type() == "Closing" or trade.Text1() == "FULL_RETURN"):
            return False

        if not self.is_settled(trade):
            return False

        return True


    def PerformSTP(self, settlement):
        """
        Auto BO Confirm trades that meet the above criteria
        """
        trade = settlement.Trade()
        instrument = trade.Instrument()
        if instrument.OpenEnd() != "Terminated":
            instrument.OpenEnd("Terminated")
            instrument.Commit()

    def is_valid_sbl_settlement(self, settlement):
        """
        Checks if given settlement is a valid settlement
        for the SBL Business
        """
        trade = settlement.Trade()
        if not trade:
            return False
        acquirer = trade.Acquirer().Name()
        instrument = trade.Instrument().InsType()
        if instrument != "SecurityLoan":
            return False
        if acquirer != "SECURITY LENDINGS DESK":
            return False
        if not trade.Status() in VALID_TRADE_STATUS:
            return False
        if settlement.Type() not in ["Security Nominal", "End Security"]:
            return False
        return True

    def is_settled(self, trade):
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
