"""----------------------------------------------------------------------------
MODULE:
    FSwiftSettStatusProcessAdviceInCallbacksBase

DESCRIPTION:
    OPEN EXTENSION MODULE
    This is a READ ONLY module. User can override the default logic in derived
    class FSwiftSettStatusProcessAdviceInCallbacks
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

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import acm

import FSwiftReaderLogger

notifier = FSwiftReaderLogger.FSwiftReaderLogger('SecSetlConf', 'FSecuritySettlementInNotify_Config')
import FSwiftMLUtils


class FSecuritySettlementStatusProcessAdviceInCallbacksBase(object):
    def __init__(self):
        pass

    # The context parameter is an instance of FBusinessProcessCallbackContext
    # Conditions return True or False
    # Name convention is
    # 'condition_' + 'entry_'/'exit_' + state name in lowercase and underscore
    def condition_entry_state_ready(self, context):
        return FSwiftMLUtils.HasUserRights(FSwiftMLUtils.get_operation_name_from_bpr_context(context))

    def condition_entry_state_paired(self, context):
        return FSwiftMLUtils.HasUserRights(FSwiftMLUtils.get_operation_name_from_bpr_context(context))

    def condition_entry_state_acknowledged(self, context):
        return FSwiftMLUtils.HasUserRights(FSwiftMLUtils.get_operation_name_from_bpr_context(context))

    def condition_entry_state_notmatched(self, context):
        return FSwiftMLUtils.HasUserRights(FSwiftMLUtils.get_operation_name_from_bpr_context(context))

    def condition_entry_state_matched(self, context):
        return FSwiftMLUtils.HasUserRights(FSwiftMLUtils.get_operation_name_from_bpr_context(context))

    def condition_entry_state_pendingsettlement(self, context):
        return FSwiftMLUtils.HasUserRights(FSwiftMLUtils.get_operation_name_from_bpr_context(context))

    def condition_entry_state_failingsettlement(self, context):
        return FSwiftMLUtils.HasUserRights(FSwiftMLUtils.get_operation_name_from_bpr_context(context))

    def condition_entry_state_rejected(self, context):
        return FSwiftMLUtils.HasUserRights(FSwiftMLUtils.get_operation_name_from_bpr_context(context))

    def condition_entry_state_amendcancelrequested(self, context):
        return FSwiftMLUtils.HasUserRights(FSwiftMLUtils.get_operation_name_from_bpr_context(context))

    def condition_entry_state_amendcancelcompleted(self, context):
        return FSwiftMLUtils.HasUserRights(FSwiftMLUtils.get_operation_name_from_bpr_context(context))

    def condition_entry_state_amendcancelpending(self, context):
        return FSwiftMLUtils.HasUserRights(FSwiftMLUtils.get_operation_name_from_bpr_context(context))

    def condition_entry_state_cancelled(self, context):
        return FSwiftMLUtils.HasUserRights(FSwiftMLUtils.get_operation_name_from_bpr_context(context))

    def condition_entry_state_processed(self, context):
        return FSwiftMLUtils.HasUserRights(FSwiftMLUtils.get_operation_name_from_bpr_context(context))

    # ------------------------------------------------------------------------------
    def condition_exit_state_ready(self, context):
        return True

    def condition_exit_state_paired(self, context):
        return True

    def condition_exit_state_acknowledged(self, context):
        return True

    def condition_exit_state_notmatched(self, context):
        return True

    def condition_exit_state_matched(self, context):
        return True

    def condition_exit_state_pendingsettlement(self, context):
        return True

    def condition_exit_state_failingsettlement(self, context):
        return True

    def condition_exit_state_rejected(self, context):
        return True

    def condition_exit_state_amendcancelrequested(self, context):
        return True

    def condition_exit_state_amendcancelcompleted(self, context):
        return True

    def condition_exit_state_amendcancelpending(self, context):
        return True

    def condition_exit_state_cancelled(self, context):
        return True

    def condition_exit_state_processed(self, context):
        return True

    # ------------------------------------------------------------------------------
    # Entry/Exit callbacks do not return anything
    # Name convention is
    # 'on_' + 'entry_'/'exit_' + state name in lowercase and underscore
    def on_entry_state_ready(self, context):
        pass

    def on_entry_state_paired(self, context):
        pass

    def on_entry_state_acknowledged(self, context):
        pass

    def on_entry_state_notmatched(self, context):
        pass

    def on_entry_state_matched(self, context):
        pass

    def on_entry_state_pendingsettlement(self, context):
        pass

    def on_entry_state_failingsettlement(self, context):
        pass

    def on_entry_state_rejected(self, context):
        pass

    def on_entry_state_amendcancelrequested(self, context):
        pass

    def on_entry_state_amendcancelcompleted(self, context):
        pass

    def on_entry_state_amendcancelpending(self, context):
        pass

    def on_entry_state_cancelled(self, context):
        pass

    def on_entry_state_processed(self, context):
        pass

    # ------------------------------------------------------------------------------
    def on_exit_state_ready(self, context):
        pass

    def on_exit_state_paired(self, context):
        pass

    def on_exit_state_acknowledged(self, context):
        pass

    def on_exit_state_notmatched(self, context):
        pass

    def on_exit_state_matched(self, context):
        pass

    def on_exit_state_pendingsettlement(self, context):
        pass

    def on_exit_state_failingsettlement(self, context):
        pass

    def on_exit_state_rejected(self, context):
        pass

    def on_exit_state_amendcancelrequested(self, context):
        pass

    def on_exit_state_amendcancelcompleted(self, context):
        pass

    def on_exit_state_amendcancelpending(self, context):
        pass

    def on_exit_state_cancelled(self, context):
        pass

    def on_exit_state_processed(self, context):
        pass


# ------------------------------------------------------------------------------



