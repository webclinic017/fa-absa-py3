"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    LoanBalanceStatementEventHooks

DESCRIPTION
    This module contains any confirmation event hooks for the loan balance statement functionality.

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
2019-05-29      FAOPS-513       Stuart Wilson           Kershia Perumal         Initial Implementation
-----------------------------------------------------------------------------------------------------------------------------------------
"""


def LOAN_BALANCE_STATEMENT_EVENT(trade):

    return False







