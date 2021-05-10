"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    CallStatementConfirmationEventHooks
    
DESCRIPTION
    This module contains any confirmation event hooks for the call deposit 
    statement functionality.

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
2018-08-14      FAOPS-167       Cuen Edwards            Elaine Visagie          Initial Implementation
-----------------------------------------------------------------------------------------------------------------------------------------
"""


def CONF_CALL_STATEMENT(trade):
    """
    Determine if the current state of a trade represents a call 
    deposit statement confirmation event.
    
    This hook always returns False as call statement confirmations
    are never generated indirectly (e.g. due to a change to an object,
    or due to a trade being selected by the confirmation EOD process) 
    but rather directly (e.g. either during a statement run or by an
    adhoc statement request).
    """
    return False

