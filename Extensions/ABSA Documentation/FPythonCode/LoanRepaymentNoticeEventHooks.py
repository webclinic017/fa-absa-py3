"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    LoanRepaymentNoticeEventHooks

DESCRIPTION
    This module contains any confirmation event hooks for the Loan Repayment Notice functionality.

    These hooks are plugged into the FConfirmationParameters.confirmationEvents
    confirmation event definitions list and are used by Front Arena to determine
    when a specified confirmation event has occurred.

NOTES:
    Hooks named using uppercase characters to match existing custom ABSA hooks.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2018-11-20                      Stuart Wilson           Loan Ops                Event for repayment notices
-----------------------------------------------------------------------------------------------------------------------------------------
"""


def LOAN_REPAYMENT_NOTICE_EVENT(trade):
    """
    Executed by task therefore not required to have any logic
    """
    return False
