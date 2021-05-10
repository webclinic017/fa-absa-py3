"""----------------------------------------------------------------------------
MODULE:
    FTRADSStateChart_18

DESCRIPTION:
    This is a READ only module
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


----------------------------------------------------------------------------"""
from FTRADSStateChartCallbacks import FTRADSStateChartCallbacks

ftrads_state_chart_callbacks = FTRADSStateChartCallbacks()

# The context parameter is an instance of FBusinessProcessCallbackContext
# Conditions return True or False
# Name convention is
# 'condition_' + 'entry_'/'exit_' + state name in lowercase and underscore
def condition_entry_state_ready(context):
    return ftrads_state_chart_callbacks.condition_entry_state_ready(context)

def condition_entry_state_send(context):
    return ftrads_state_chart_callbacks.condition_entry_state_send(context)

def condition_entry_state_reported(context):
    return ftrads_state_chart_callbacks.condition_entry_state_reported(context)

def condition_entry_state_published(context):
    return ftrads_state_chart_callbacks.condition_entry_state_published(context)

def condition_entry_state_notpublished(context):
    return ftrads_state_chart_callbacks.condition_entry_state_notpublished(context)

def condition_entry_state_failed(context):
    return ftrads_state_chart_callbacks.condition_entry_state_failed(context)

def condition_entry_state_cancelreported(context):
    return ftrads_state_chart_callbacks.condition_entry_state_cancelreported(context)

def condition_entry_state_cancelpublished(context):
    return ftrads_state_chart_callbacks.condition_entry_state_cancelpublished(context)

def condition_entry_state_failedcancel(context):
    return ftrads_state_chart_callbacks.condition_entry_state_failedcancel(context)

def condition_entry_state_cancelled(context):
    return ftrads_state_chart_callbacks.condition_entry_state_cancelled(context)

# Entry/Exit callbacks do not return anything
#
# Name convention is
# 'on_' + 'entry_'/'exit_' + state name in lowercase and underscore
#
def on_entry_state_ready(context):
    ftrads_state_chart_callbacks.on_entry_state_ready(context)

def on_entry_state_send(context):
    ftrads_state_chart_callbacks.on_entry_state_send(context)

def on_entry_state_reported(context):
    ftrads_state_chart_callbacks.on_entry_state_reported(context)

def on_entry_state_published(context):
    ftrads_state_chart_callbacks.on_entry_state_published(context)

def on_entry_state_notpublished(context):
    ftrads_state_chart_callbacks.on_entry_state_notpublished(context)

def on_entry_state_failed(context):
    ftrads_state_chart_callbacks.on_entry_state_failed(context)

def on_entry_state_cancelreported(context):
    ftrads_state_chart_callbacks.on_entry_state_cancelreported(context)

def on_entry_state_cancelpublished(context):
    ftrads_state_chart_callbacks.on_entry_state_cancelpublished(context)

def on_entry_state_failedcancel(context):
    ftrads_state_chart_callbacks.on_entry_state_failedcancel(context)

def on_entry_state_cancelled(context):
    ftrads_state_chart_callbacks.on_entry_state_cancelled(context)


