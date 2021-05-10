"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    LoanRepaymentNoticeEventHooks

DESCRIPTION
    This module contains any confirmation event hooks for the Loan Rate Notice functionality.

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
2018-02-27                      Adelaide Davhana        Kgomotso Gumbo           ADAPTIV-211: initial implementation
2018-09-20                      Stuart Wilson           Kgomotso Gumbo           FAOPS-97  Refactor
-----------------------------------------------------------------------------------------------------------------------------------------
"""


def CONF_RATE_NOTICE(trade):

    return False
    






