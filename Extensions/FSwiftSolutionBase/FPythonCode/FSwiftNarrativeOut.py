"""----------------------------------------------------------------------------
MODULE:
    FSwiftCashOut

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

VERSION: 2.2.1-0.5.3155

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
from FNarrativeOutCallbacks import FNarrativeOutCallbacks

FNarrativeOutCallbacks = FNarrativeOutCallbacks()
# The context parameter is an instance of FBusinessProcessCallbackContext
# Conditions return True or False
# Name convention is
# 'condition_' + 'entry_'/'exit_' + state name in lowercase and underscore


def condition_entry_state_ready(context):
    return FNarrativeOutCallbacks.condition_entry_state_ready(context)

def condition_entry_state_swiftmsggenerated(context):
    return FNarrativeOutCallbacks.condition_entry_state_swiftmsggenerated(context)

def condition_entry_state_generationfailed(context):
    return FNarrativeOutCallbacks.condition_entry_state_generationfailed(context)

def condition_entry_state_sendfailed(context):
    return FNarrativeOutCallbacks.condition_entry_state_sendfailed(context)

def condition_entry_state_sent(context):
    return FNarrativeOutCallbacks.condition_entry_state_sent(context)

def condition_entry_state_acknowledged(context):
    return FNarrativeOutCallbacks.condition_entry_state_acknowledged(context)

# ------------------------------------------------------------------------------
def condition_exit_state_ready(context):
    return FNarrativeOutCallbacks.condition_exit_state_ready(context)

def condition_exit_state_swiftmsggenerated(context):
    return FNarrativeOutCallbacks.condition_exit_state_swiftmsggenerated(context)

def condition_exit_state_generationfailed(context):
    return FNarrativeOutCallbacks.condition_exit_state_generationfailed(context)

def condition_exit_state_sendfailed(context):
    return FNarrativeOutCallbacks.condition_exit_state_sendfailed(context)

def condition_exit_state_sent(context):
    return FNarrativeOutCallbacks.condition_exit_state_sent(context)

def condition_exit_state_acknowledged(context):
    return FNarrativeOutCallbacks.condition_exit_state_acknowledged(context)


# Entry/Exit callbacks do not return anything
#
# Name convention is
# 'on_' + 'entry_'/'exit_' + state name in lowercase and underscore
#


def on_entry_state_ready(context):
    FNarrativeOutCallbacks.on_entry_state_ready(context)

def on_entry_state_swiftmsggenerated(context):
    FNarrativeOutCallbacks.on_entry_state_swiftmsggenerated(context)

def on_entry_state_generationfailed(context):
    FNarrativeOutCallbacks.on_entry_state_generationfailed(context)

def on_entry_state_sendfailed(context):
    FNarrativeOutCallbacks.on_entry_state_sendfailed(context)

def on_entry_state_sent(context):
    FNarrativeOutCallbacks.on_entry_state_sent(context)

def on_entry_state_acknowledged(context):
    FNarrativeOutCallbacks.on_entry_state_acknowledged(context)

# ------------------------------------------------------------------------------
def on_exit_state_ready(context):
    FNarrativeOutCallbacks.on_exit_state_ready(context)

def on_exit_state_swiftmsggenerated(context):
    FNarrativeOutCallbacks.on_exit_state_swiftmsggenerated(context)

def on_exit_state_generationfailed(context):
    FNarrativeOutCallbacks.on_exit_state_generationfailed(context)

def on_exit_state_sendfailed(context):
    FNarrativeOutCallbacks.on_exit_state_sendfailed(context)

def on_exit_state_sent(context):
    FNarrativeOutCallbacks.on_exit_state_sent(context)

def on_exit_state_acknowledged(context):
    FNarrativeOutCallbacks.on_exit_state_acknowledged(context)






