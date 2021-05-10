"""----------------------------------------------------------------------------
MODULE:
    FSwiftClientStmtOfHoldingIn

DESCRIPTION:
    OPEN EXTENSION MODULE
    Business process state callbacks.

FUNCTIONS:
    For sample state xxx there are always the four standard extension points:
        condition_entry_state_xxx():
            To control if all the pre-requisites to performing the action and
            entering the state are defined.
        on_entry_state_xxx():
            Is the place to perform the action.
            For example, the on_ entry_state_settled is the place to set the
            settlement status to Settled
        condition_exit_state_xxx():
            To control that all pre-requisites for performing the next action
            are fulfilled.
        on_exit_state_xxx():
             Is the place to reset values that you set in the state entry, if
             you are leaving the state to go backwards in the workflow.
             For example if you exit from the "Settled" state to go and re-pair,
             or to manually cancel, then you would want to remove the Settled
             status

VERSION: 3.0.0-0.5.3344
----------------------------------------------------------------------------"""
from FSwiftClientStatementOfHoldingInCallbacks import FSwiftClientStatementOfHoldingInCallbacks

clientStatementOfHoldingCallbacks = FSwiftClientStatementOfHoldingInCallbacks()

# The context parameter is an instance of FBusinessProcessCallbackContext
# Conditions return True or False
# Name convention is
# 'condition_' + 'entry_'/'exit_' + state name in lowercase and underscore
def condition_entry_state_ready(context):
    return clientStatementOfHoldingCallbacks.condition_entry_state_ready(context)

def condition_entry_state_processed(context):
    return clientStatementOfHoldingCallbacks.condition_entry_state_paired(context)

# Entry/Exit callbacks do not return anything
#
# Name convention is
# 'on_' + 'entry_'/'exit_' + state name in lowercase and underscore
#
def on_entry_state_ready(context):
    clientStatementOfHoldingCallbacks.on_entry_state_ready(context)

def on_entry_state_processed(context):
    clientStatementOfHoldingCallbacks.on_entry_state_paired(context)



