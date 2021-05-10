"""----------------------------------------------------------------------------
MODULE:
    FTRADSStateChartCallbacksBase

DESCRIPTION:
    This is a READ ONLY module. User can override the default logic in derived
    class FTRADSStateChartCallbacks
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
import acm
from FTRADSUtils import *
class FTRADSStateChartCallbacksBase(object):
    def __init__(self):
        pass

    # The context parameter is an instance of FBusinessProcessCallbackContext
    # Conditions return True or False
    # Name convention is
    # 'condition_' + 'entry_'/'exit_' + state name in lowercase and underscore
    def condition_entry_state_ready(self, context):
        return has_user_rights(get_operation_name_from_bpr_context(context))

    def condition_entry_state_send(self, context):
        return has_user_rights(get_operation_name_from_bpr_context(context))

    def condition_entry_state_reported(self, context):
        return has_user_rights(get_operation_name_from_bpr_context(context))

    def condition_entry_state_published(self, context):
        return has_user_rights(get_operation_name_from_bpr_context(context))

    def condition_entry_state_notpublished(self, context):
        return has_user_rights(get_operation_name_from_bpr_context(context))

    def condition_entry_state_failed(self, context):
        return has_user_rights(get_operation_name_from_bpr_context(context))

    def condition_entry_state_cancelreported(self, context):
        return has_user_rights(get_operation_name_from_bpr_context(context))

    def condition_entry_state_cancelpublished(self, context):
        return has_user_rights(get_operation_name_from_bpr_context(context))

    def condition_entry_state_failedcancel(self, context):
        return has_user_rights(get_operation_name_from_bpr_context(context))

    def condition_entry_state_cancelled(self, context):
        return has_user_rights(get_operation_name_from_bpr_context(context))

# ------------------------------------------------------------------------------
    def condition_exit_state_ready(self, context):
        return True

    def condition_exit_state_send(self, context):
        return True

    def condition_exit_state_reported(self, context):
        return True

    def condition_exit_state_published(self, context):
        return True

    def condition_exit_state_notpublished(self, context):
        return True

    def condition_exit_state_failed(self, context):
        return True

    def condition_exit_state_cancelreported(self, context):
        return True

    def condition_exit_state_cancelpublished(self, context):
        return True

    def condition_exit_state_failedcancel(self, context):
        return True

    def condition_exit_state_cancelled(self, context):
        return True
# ------------------------------------------------------------------------------
    # Entry/Exit callbacks do not return anything
    # Name convention is
    # 'on_' + 'entry_'/'exit_' + state name in lowercase and underscore
    def on_entry_state_ready(self, context):
        bpr = context.CurrentStep().BusinessProcess()
        update_business_process_owner(bpr, '', False)

    def on_entry_state_send(self, context):
        pass

    def on_entry_state_reported(self, context):
        pass

    def on_entry_state_published(self, context):
        pass

    def on_entry_state_notpublished(self, context):
        pass

    def on_entry_state_failed(self, context):
        pass

    def on_entry_state_cancelreported(self, context):
        pass

    def on_entry_state_cancelpublished(self, context):
        pass

    def on_entry_state_failedcancel(self, context):
        pass

    def on_entry_state_cancelled(self, context):
        pass
# ------------------------------------------------------------------------------
    def on_exit_state_ready(self, context):
        pass

    def on_exit_state_send(self, context):
        pass

    def on_exit_state_reported(self, context):
        pass

    def on_exit_state_published(self, context):
        pass

    def on_exit_state_notpublished(self, context):
        pass

    def on_exit_state_failed(self, context):
        pass

    def on_exit_state_cancelreported(self, context):
        pass

    def on_exit_state_cancelpublished(self, context):
        pass

    def on_exit_state_failedcancel(self, context):
        pass

    def on_exit_state_cancelled(self, context):
        pass
