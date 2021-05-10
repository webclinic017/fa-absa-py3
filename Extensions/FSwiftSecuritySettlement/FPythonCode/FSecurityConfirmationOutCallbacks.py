"""----------------------------------------------------------------------------
MODULE:
    FSecurityConfirmationOutCallbacks

DESCRIPTION:
    OPEN EXTENSION MODULE
    FFXTradeConfMsgCallbacks class for user customization.
    Business process conditional_entry/exit and on_entry/exit callbacks.
    User can override the logic written in the base class FFXTradeConfMsgCallbacksBase

    If user wishes to add some extra processing for conditional entry state
     e.g. 'ready' he can implement method as
    def condition_entry_state_ready(self):
        # Custom logic before core logic
        super(FFXTradeConfMsgCallbacks, self).condition_entry_state_ready()
        # Custom logic after core logic

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
             For example if you exit from the ?Matched? state to go and re-pair,
             or to manually cancel, then you would want to remove the
             confirmation Matched status

VERSION: 3.0.0-0.5.3344
----------------------------------------------------------------------------"""
# The context parameter is an instance of FBusinessProcessCallbackContext
import FSecurityConfirmationOutCallbacksBase
import FSwiftWriterLogger
notifier = FSwiftWriterLogger.FSwiftWriterLogger('SecConOut', 'FSecuritySettlementOutNotify_Config')

class FSecurityConfirmationOutCallbacks(FSecurityConfirmationOutCallbacksBase.FSecurityConfirmationOutCallbacksBase):
    def __init__(self):
        super(FSecurityConfirmationOutCallbacks, self).__init__()



