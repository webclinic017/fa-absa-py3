"""----------------------------------------------------------------------------
MODULE:
    FSwiftFXMMConfirmationOut

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
from FFXMMConfirmationOutCallbacks import FFXMMConfirmationOutCallbacks

fXMMConfOutMsgCallbacks = FFXMMConfirmationOutCallbacks()
# The context parameter is an instance of FBusinessProcessCallbackContext
# Conditions return True or False
# Name convention is
# 'condition_' + 'entry_'/'exit_' + state name in lowercase and underscore
def condition_entry_state_ready(context):
    return fXMMConfOutMsgCallbacks.condition_entry_state_ready(context)

def condition_entry_state_swiftmsggenerated(context):
    return fXMMConfOutMsgCallbacks.condition_entry_state_swiftmsggenerated(context)

def condition_entry_state_generationfailed(context):
    return fXMMConfOutMsgCallbacks.condition_entry_state_generationfailed(context)

def condition_entry_state_sendfailed(context):
    return fXMMConfOutMsgCallbacks.condition_entry_state_sendfailed(context)

def condition_entry_state_sent(context):
    return fXMMConfOutMsgCallbacks.condition_entry_state_sent(context)

def condition_entry_state_acknowledged(context):
    return fXMMConfOutMsgCallbacks.condition_entry_state_acknowledged(context)

# ------------------------------------------------------------------------------
def condition_exit_state_ready(context):
    return fXMMConfOutMsgCallbacks.condition_exit_state_ready(context)

def condition_exit_state_swiftmsggenerated(context):
    return fXMMConfOutMsgCallbacks.condition_exit_state_swiftmsggenerated(context)

def condition_exit_state_generationfailed(context):
    return fXMMConfOutMsgCallbacks.condition_exit_state_generationfailed(context)

def condition_exit_state_sendfailed(context):
    return fXMMConfOutMsgCallbacks.condition_exit_state_sendfailed(context)

def condition_exit_state_sent(context):
    return fXMMConfOutMsgCallbacks.condition_exit_state_sent(context)

def condition_exit_state_acknowledged(context):
    return fXMMConfOutMsgCallbacks.condition_exit_state_acknowledged(context)


# Entry/Exit callbacks do not return anything
#
# Name convention is
# 'on_' + 'entry_'/'exit_' + state name in lowercase and underscore
#


def on_entry_state_ready(context):
    fXMMConfOutMsgCallbacks.on_entry_state_ready(context)

def on_entry_state_swiftmsggenerated(context):
    fXMMConfOutMsgCallbacks.on_entry_state_swiftmsggenerated(context)

def on_entry_state_generationfailed(context):
    fXMMConfOutMsgCallbacks.on_entry_state_generationfailed(context)

def on_entry_state_sendfailed(context):
    fXMMConfOutMsgCallbacks.on_entry_state_sendfailed(context)

def on_entry_state_sent(context):
    fXMMConfOutMsgCallbacks.on_entry_state_sent(context)

def on_entry_state_acknowledged(context):
    fXMMConfOutMsgCallbacks.on_entry_state_acknowledged(context)

# ------------------------------------------------------------------------------
def on_exit_state_ready(context):
    fXMMConfOutMsgCallbacks.on_exit_state_ready(context)

def on_exit_state_swiftmsggenerated(context):
    fXMMConfOutMsgCallbacks.on_exit_state_swiftmsggenerated(context)

def on_exit_state_generationfailed(context):
    fXMMConfOutMsgCallbacks.on_exit_state_generationfailed(context)

def on_exit_state_sendfailed(context):
    fXMMConfOutMsgCallbacks.on_exit_state_sendfailed(context)

def on_exit_state_sent(context):
    fXMMConfOutMsgCallbacks.on_exit_state_sent(context)

def on_exit_state_acknowledged(context):
    fXMMConfOutMsgCallbacks.on_exit_state_acknowledged(context)


