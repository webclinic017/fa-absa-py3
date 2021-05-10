
"""----------------------------------------------------------------------------
MODULE:
    FTRADSStateChartCallbacks

DESCRIPTION:
    OPEN EXTENSION MODULE
    This is where user can override the default callbacks

    Business process conditional_entry/exit and on_entry/exit callbacks.

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

----------------------------------------------------------------------------"""
import FTRADSStateChartCallbacksBase

class FTRADSStateChartCallbacks(FTRADSStateChartCallbacksBase.FTRADSStateChartCallbacksBase):
    def __init__(self):
        super(FTRADSStateChartCallbacks, self).__init__()
