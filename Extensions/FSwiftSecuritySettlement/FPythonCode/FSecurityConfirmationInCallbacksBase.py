"""----------------------------------------------------------------------------
MODULE:
    FSecurityConfirmationInCallbacksBase

DESCRIPTION:
    OPEN EXTENSION MODULE
    This is a READ ONLY module. User can override the default logic in derived
    class FSecurityConfirmationInCallbacks
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

class FSecurityConfirmationInCallbacksBase(object):
    def __init__(self):
        pass

    def getStateBeforePairing(self, bpr):
        prevStatus = None
        for step in bpr.Steps():
            if step.State().Name() == 'Paired':
                diaryEntry = step.DiaryEntry()
                if diaryEntry:
                    param = diaryEntry.Parameters()
                    if param:
                        prevStatus = param.At('AcmObjectStatusBeforePairing', None)
                        break
        return prevStatus

    # Conditions return True or False
    # Name convention is
    # 'condition_' + 'entry_'/'exit_' + state name in lowercase and underscore
    def condition_entry_state_ready(self, context):
        return FSwiftMLUtils.HasUserRights(FSwiftMLUtils.get_operation_name_from_bpr_context(context))

    def condition_entry_state_paired(self, context):
        return FSwiftMLUtils.HasUserRights(FSwiftMLUtils.get_operation_name_from_bpr_context(context))

    def condition_entry_state_matched(self, context):
        return FSwiftMLUtils.HasUserRights(FSwiftMLUtils.get_operation_name_from_bpr_context(context))

    def condition_entry_state_unpaired(self, context):
        return FSwiftMLUtils.HasUserRights(FSwiftMLUtils.get_operation_name_from_bpr_context(context))

    def condition_entry_state_cancelled(self, context):
        return FSwiftMLUtils.HasUserRights(FSwiftMLUtils.get_operation_name_from_bpr_context(context))

    def condition_entry_state_difference(self, context):
        return FSwiftMLUtils.HasUserRights(FSwiftMLUtils.get_operation_name_from_bpr_context(context))

# ------------------------------------------------------------------------------
    def condition_exit_state_ready(self, context):
        return True

    def condition_exit_state_paired(self, context):
        return True

    def condition_exit_state_matched(self, context):
        return True

    def condition_exit_state_unpaired(self, context):
        return True

    def condition_exit_state_cancelled(self, context):
        return True

    def condition_exit_state_difference(self, context):
        return True

# ------------------------------------------------------------------------------
    # Entry/Exit callbacks do not return anything
    # Name convention is
    # 'on_' + 'entry_'/'exit_' + state name in lowercase and underscore
    def on_entry_state_ready(self, context):
        pass

    def on_entry_state_paired(self, context):
        try:
            bpr = context.CurrentStep().BusinessProcess()
            conf_obj = FSwiftMLUtils.get_acm_object_from_bpr(bpr)
            conf_obj.AddDiaryNote('SWIFTREADER_PAIRED_CONF_BPR:%s->%s' % (str(conf_obj.Oid()), str(bpr.Oid())))
            FSwiftMLUtils.commit_and_retry(conf_obj)
        except Exception as error:
            notifier.ERROR("Error occurred in on_entry_state_paired: %s" % str(error))
            notifier.DEBUG(str(error), exc_info=1)


    def on_entry_state_matched(self, context):
        #context.Subject().Subject().Status('Matched')
        try:
            # No need to send refresh on confirmation as we are updating it already.
            bpr = context.CurrentStep().BusinessProcess()
            conf_obj = FSwiftMLUtils.get_acm_object_from_bpr(bpr)
            conf_obj.Status('Matched')
            FSwiftMLUtils.commit_and_retry(conf_obj)
        except Exception as error:
            notifier.ERROR("Error occurred in on_entry_state_matched: %s"%str(error))
            notifier.DEBUG(str(error), exc_info=1)

    def on_entry_state_unpaired(self, context):
        try:
            # Get the handle of linked confirmation
            bpr = context.CurrentStep().BusinessProcess()
            conf_obj = FSwiftMLUtils.get_acm_object_from_bpr(bpr)
            if conf_obj:

                prevStatus = self.getStateBeforePairing(bpr)

                if prevStatus and prevStatus != conf_obj.Status():
                    try:
                        conf_obj.Status(prevStatus)
                        FSwiftMLUtils.commit_and_retry(conf_obj)
                    except Exception as e:
                        notifier.ERROR("Cannot move Confirmation %s to %s status" % (conf_obj.Oid(), prevStatus))
                        notifier.DEBUG(str(e), exc_info=1)
                FSwiftMLUtils.FSwiftExternalObject.unlink_acm_object(bpr, 'Confirmation')
        except Exception as error:
            notifier.ERROR("Error occurred in on_entry_state_unpaired: %s"%str(error))
            notifier.DEBUG(str(error), exc_info=1)

    def on_entry_state_cancelled(self, context):
        try:
            bpr = context.CurrentStep().BusinessProcess()
            conf_obj = FSwiftMLUtils.get_acm_object_from_bpr(bpr)

            if conf_obj:
                prevStatus = self.getStateBeforePairing(bpr)
                conf_obj.AddDiaryNote("Cancelled with reference to BusinessProcess Id %d and Subject Id %d."%(bpr.Oid(), bpr.Subject().Oid()))
                FSwiftMLUtils.commit_and_retry(conf_obj) # No Need to send refresh to acm object as we are updating it already.

                if prevStatus and prevStatus != conf_obj.Status():
                    try:
                        conf_obj.Status(prevStatus)
                        FSwiftMLUtils.commit_and_retry(conf_obj)
                    except Exception as e:
                        notifier.ERROR("Cannot move Confirmation %s to %s status" % (conf_obj.Oid(), prevStatus))
                        notifier.DEBUG(str(e), exc_info=1)

                FSwiftMLUtils.unlink_references(bpr)
        except Exception as error:
            notifier.ERROR("Error occurred in on_entry_state_cancelled: %s"%str(error))
            notifier.DEBUG(str(error), exc_info=1)

    def on_entry_state_difference(self, context):
        try:
            bpr = context.CurrentStep().BusinessProcess()
            conf_obj = FSwiftMLUtils.get_acm_object_from_bpr(bpr)
            conf_obj.Status('Matching Failed')
            FSwiftMLUtils.commit_and_retry(conf_obj)
        except Exception as error:
            notifier.ERROR("Error occurred in on_entry_state_difference: %s"%str(error))
            notifier.DEBUG(str(error), exc_info=1)


# ------------------------------------------------------------------------------
    def on_exit_state_ready(self, context):
        pass

    def on_exit_state_paired(self, context):
        pass

    def on_exit_state_matched(self, context):
        pass

    def on_exit_state_unpaired(self, context):
        pass

    def on_exit_state_cancelled(self, context):
        pass

    def on_exit_state_difference(self, context):
        pass

