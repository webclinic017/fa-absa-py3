"""----------------------------------------------------------------------------
MODULE:
    FSwiftFXMMConfirmationIn

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
            For example, the on_ entry_state_matched is the place to set the
            confirmation status to Matched
        condition_exit_state_xxx():
            To control that all pre-requisites for performing the next action
            are fulfilled.
        on_exit_state_xxx():
             Is the place to reset values that you set in the state entry, if
             you are leaving the state to go backwards in the workflow.
             For example if you exit from the "Matched" state to go and re-pair,
             or to manually cancel, then you would want to remove the
             confirmation Matched status

VERSION: 3.0.1-0.5.3470
----------------------------------------------------------------------------"""
from FFXMMConfirmationInCallbacks import FFXMMConfirmationInCallbacks

fxMMConfInMsgCallbacks = FFXMMConfirmationInCallbacks()
# The context parameter is an instance of FBusinessProcessCallbackContext
# Conditions return True or False
# Name convention is
# 'condition_' + 'entry_'/'exit_' + state name in lowercase and underscore
def condition_entry_state_ready(context):
    return fxMMConfInMsgCallbacks.condition_entry_state_ready(context)

def condition_entry_state_paired(context):
    return fxMMConfInMsgCallbacks.condition_entry_state_paired(context)

def condition_entry_state_matched(context):
    return fxMMConfInMsgCallbacks.condition_entry_state_matched(context)

def condition_entry_state_unpaired(context):
    return fxMMConfInMsgCallbacks.condition_entry_state_unpaired(context)

def condition_entry_state_cancelled(context):
    return fxMMConfInMsgCallbacks.condition_entry_state_cancelled(context)

def condition_entry_state_difference(context):
    return fxMMConfInMsgCallbacks.condition_entry_state_difference(context)

def condition_entry_state_amended(context):
    return fxMMConfInMsgCallbacks.condition_entry_state_amended(context)

# Entry/Exit callbacks do not return anything
#
# Name convention is
# 'on_' + 'entry_'/'exit_' + state name in lowercase and underscore
#

def on_entry_state_ready(context):
    fxMMConfInMsgCallbacks.on_entry_state_ready(context)

def on_entry_state_paired(context):
    fxMMConfInMsgCallbacks.on_entry_state_paired(context)

def on_entry_state_matched(context):
    #context.Subject().Subject().Status('Matched')
    fxMMConfInMsgCallbacks.on_entry_state_matched(context)

def on_entry_state_unpaired(context):
    fxMMConfInMsgCallbacks.on_entry_state_unpaired(context)

def on_entry_state_cancelled(context):
    fxMMConfInMsgCallbacks.on_entry_state_cancelled(context)

def on_entry_state_difference(context):
    fxMMConfInMsgCallbacks.on_entry_state_difference(context)

def on_entry_state_amended(context):
    fxMMConfInMsgCallbacks.on_entry_state_amended(context)


