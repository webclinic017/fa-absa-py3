"""----------------------------------------------------------------------------
MODULE:
    FCashOutCallbacksBase

DESCRIPTION:
    OPEN EXTENSION MODULE
    This is a READ ONLY module. User can override the default logic in derived
    class FFXTradeConfMsgCallbacks
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

MAPPING:
    Below is the mapping of Settlement status against its corresponding document status.
    Settlement Status                   Document Status
    -------------------                 ---------------
    NEW                                 NEW
    EXCEPTION                           EXCEPTION
    PENDING_DOCUMENT_GENERATION         PENDING_GENERATION
    PENDING_APPROVAL                    PENDING_GENERATION
    AUTHORISED                          PENDING_GENERATION
    RELEASED                            GENERATED
    ACKNOWLEDGED                        SENT_SUCCESSFULLY
    NOT_ACKNOWLEDGED                    SEND_FAILED
    PENDING_CLOSURE                     SENT_SUCCESSFULLY
    PENDING_CANCELLATION                SENT_SUCCESSFULLY
    PENDING_MATCHING                    SENT_SUCCESSFULLY

VERSION: 3.0.0-0.5.3383

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.

----------------------------------------------------------------------------"""
# The context parameter is an instance of FBusinessProcessCallbackContext
import time

import FSwiftWriterLogger
import FSwiftMLUtils
import FSwiftWriterUtils

notifier = FSwiftWriterLogger.FSwiftWriterLogger('CashSetlemnt', 'FCashOutNotify_Config')

class FCashOutMT304CallbacksBase(object):
    def __init__(self):
        pass


    # Conditions return True or False
    # Name convention is
    # 'condition_' + 'entry_'/'exit_' + state name in lowercase and underscore
    def condition_entry_state_ready(self, context):
        return FSwiftMLUtils.HasUserRights(FSwiftMLUtils.get_operation_name_from_bpr_context(context))

    def condition_entry_state_swiftmsggenerated(self, context):
        return FSwiftMLUtils.HasUserRights(FSwiftMLUtils.get_operation_name_from_bpr_context(context))

    def condition_entry_state_generationfailed(self, context):
        return FSwiftMLUtils.HasUserRights(FSwiftMLUtils.get_operation_name_from_bpr_context(context))

    def condition_entry_state_sendfailed(self, context):
        return FSwiftMLUtils.HasUserRights(FSwiftMLUtils.get_operation_name_from_bpr_context(context))

    def condition_entry_state_sent(self, context):
        return FSwiftMLUtils.HasUserRights(FSwiftMLUtils.get_operation_name_from_bpr_context(context))

    def condition_entry_state_acknowledged(self, context):
        return FSwiftMLUtils.HasUserRights(FSwiftMLUtils.get_operation_name_from_bpr_context(context))

# ------------------------------------------------------------------------------
    def condition_exit_state_ready(self, context):
        return True

    def condition_exit_state_swiftmsggenerated(self, context):
        return True

    def condition_exit_state_generationfailed(self, context):
        return True

    def condition_exit_state_sendfailed(self, context):
        return True

    def condition_exit_state_sent(self, context):
        return True

    def condition_exit_state_acknowledged(self, context):
        return True

# ------------------------------------------------------------------------------
    # Entry/Exit callbacks do not return anything
    # Name convention is
    # 'on_' + 'entry_'/'exit_' + state name in lowercase and underscore
    def on_entry_state_ready(self, context):
        pass

    def on_entry_state_swiftmsggenerated(self, context):
        pass

    def on_entry_state_generationfailed(self, context):
        msg_type = ''
        try:
            acm_obj, sub_typ, msg_type = FSwiftWriterUtils.get_acmobj_subtyp_msgtyp(context)
            max_retries = FSwiftWriterUtils.get_max_commit_retries()
            bpr = context.CurrentStep().BusinessProcess()
            doc_id = FSwiftMLUtils.get_parameters_from_bpr_state(bpr, 'Ready', 'DOCUMENT_ID')

            counter = 1
            while counter <=max_retries:
                try:
                    FSwiftMLUtils.set_document_status_on_acm_object(acm_obj, 'EXCEPTION', sub_typ, doc_id=doc_id)
                except Exception as e:
                    #raise e
                    if 'Update collision' in str(e):
                        counter = counter + 1
                        notifier.ERROR("{0} Retrying after 8 seconds due to update collision".format(msg_type))
                        time.sleep(8)
                        continue
                    notifier.ERROR('%s Exception in on_entry_state_generationfailed : %s' % (msg_type, str(e)))
                break
        except Exception as e:
            notifier.ERROR('%s Exception caught in on_entry_state_generationfailed : %s' % (msg_type, str(e)))



    def on_entry_state_sendfailed(self, context):
        msg_type = ''
        try:
            acm_obj, sub_typ, msg_type = FSwiftWriterUtils.get_acmobj_subtyp_msgtyp(context)
            max_retries = FSwiftWriterUtils.get_max_commit_retries()
            bpr = context.CurrentStep().BusinessProcess()
            doc_id = FSwiftMLUtils.get_parameters_from_bpr_state(bpr, 'Ready', 'DOCUMENT_ID')

            counter = 1
            while counter <=max_retries:
                event = context.Event().Name()
                if event == 'Nack':
                    try:
                        FSwiftMLUtils.set_document_status_on_acm_object(acm_obj, 'SEND_FAILED', sub_typ, doc_id=doc_id)
                    except Exception as e:
                        #raise e
                        if 'Update collision' in str(e):
                            counter = counter + 1
                            notifier.ERROR("{0} Retrying after 8 seconds due to update collision".format(msg_type))
                            time.sleep(8)
                            continue
                        notifier.ERROR('%s Exception in on_entry_state_sendfailed : %s' % (msg_type, str(e)))
                break
        except Exception as e:
            notifier.ERROR('%s Exception caught in on_entry_state_sendfailed : %s' % (msg_type, str(e)))


    def on_entry_state_sent(self, context):
        pass


    def on_entry_state_acknowledged(self, context):
        msg_type = ''
        try:
            bpr = context.CurrentStep().BusinessProcess()
            doc_id = FSwiftMLUtils.get_parameters_from_bpr_state(bpr, 'Ready', 'DOCUMENT_ID')
            acm_obj, sub_typ, msg_type = FSwiftWriterUtils.get_acmobj_subtyp_msgtyp(context)
            max_retries = FSwiftWriterUtils.get_max_commit_retries()

            counter = 1
            while counter <=max_retries:
                try:
                    FSwiftMLUtils.set_document_status_on_acm_object(acm_obj, 'SENT_SUCCESSFULLY', sub_typ, doc_id=doc_id)
                except Exception as e:
                    #raise e
                    if 'Update collision' in str(e):
                        counter = counter + 1
                        notifier.ERROR("{0} Retrying after 8 seconds due to update collision".format(msg_type))
                        time.sleep(8)
                        continue
                    notifier.ERROR('%s Exception in on_entry_state_acknowledged : %s' % (msg_type, str(e)))
                break
        except Exception as e:
            notifier.ERROR('%s Exception caught in on_entry_state_acknowledged : %s' % (msg_type, str(e)))

# ------------------------------------------------------------------------------
    def on_exit_state_ready(self, context):
        pass

    def on_exit_state_swiftmsggenerated(self, context):
        pass

    def on_exit_state_generationfailed(self, context):
        pass

    def on_exit_state_sendfailed(self, context):
        pass

    def on_exit_state_sent(self, context):
        pass

    def on_exit_state_acknowledged(self, context):
        pass


